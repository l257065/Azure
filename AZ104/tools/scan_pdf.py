#!/usr/bin/env python3
"""掃過來源 PDF，列出每一題在哪幾頁、疑似題型、有沒有圖、標的答案是什麼。

轉錄前先跑這支，得到一份工作清單，就不用一頁一頁翻著找題號邊界。

    AZ104_PDF="AZ104考題/NEW-AZ-104-470Q.pdf" python tools/scan_pdf.py
    AZ104_PDF="..." python tools/scan_pdf.py --json out/index.json
    AZ104_PDF="..." python tools/scan_pdf.py --stats

欄位：
    sec      區段代號："S1"…"S6" 題組／"T1"…"T10" 案例／"NewQ" 增題
    no       這一題在該區段裡的 Question #（就是文件上印的那個號碼）
    label    給人看的位置，例如 "S2#17"
    pages    這一題橫跨的頁碼（1-based，含）
    k        疑似題型：mc / hs / dd / dl（看關鍵字猜的，轉錄時要自己確認）
    img      這幾頁裡的圖片數。>0 就要 render.py 出圖用眼睛看
    ans      文件標的 Correct Answer（可能是錯的，見 AZ104考題/*Correct.txt 的更正）

**要 sec + no 兩格才認得出是哪一題。** 三份來源檔各有各的編號方式，而且
**每一段的題號都從 1 重新算**，所以單一個號碼一定撞號：

    NEW-AZ-104-470Q.pdf   分成 Question Set 1–6（→ S1…S6）
                          與 Testlet 1–10（→ T1…T10），各自從 #1 起算
    增題 62Q ＋ NewQ63-Q76  用的是 `NewQ #N`，兩份接在一起是 NewQ #1–#76

題庫檔（banks/bank_b_doc.js）就照這兩格存：`{sec:"S2", no:17, …}`。
維護的人打開題庫檔就能一比一對回 PDF，不必心算合成題號。
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fitz  # noqa: E402

Q_RE = re.compile(r"(Question|NewQ)\s*#\s*(\d+)")
SEC_RE = re.compile(r"(Question Set|Testlet)\s*(\d+)")
ANS_RE = re.compile(r"Correct\s*Answer\s*:?\s*(.*)")


def sec_code(kind, sec_no):
    """PDF 上的區段標題 → 短代號。Question Set 3 → "S3"、Testlet 7 → "T7"。"""
    if kind == "NewQ":
        return "NewQ"
    return ("S" if kind == "Question Set" else "T") + str(sec_no)


def sec_rank(sec):
    """排序用：題組 → 案例 → 增題，段內再依題號。"""
    if sec.startswith("S"):
        return 1000 + int(sec[1:])
    if sec.startswith("T"):
        return 2000 + int(sec[1:])
    return 3000


def find_pdf():
    env = os.environ.get("AZ104_PDF")
    if env:
        return env
    raise SystemExit("請設環境變數 AZ104_PDF 指定要掃哪一份 PDF")


def guess_kind(text):
    t = text.upper()
    if "DRAG DROP" in t or "DRAG AND DROP" in t:
        return "dd"
    if "HOTSPOT" in t:
        return "hs"          # hs 或 dl，得看圖才能分：是非表 vs 下拉
    return "mc"


# 這份 PDF 是轉賣品，每隔幾頁就夾一行賣家浮水印網址。轉錄時當然不能抄進去，
# 而且它會夾在題目中間把句子切斷，所以在這裡就先清掉。
JUNK_RE = re.compile(
    r"^[ \t]*(?:https?\s*:\s*//(?:reurl\.cc|www\.ruten\.com\.tw)\S*)[ \t]*$",
    re.M | re.I)


def clean(text):
    return JUNK_RE.sub("", text)


def read_pages(path):
    """回傳 (整份的純文字, 每頁的起始位移, 每頁的圖片數)。

    把全部頁面接成一條字串再找標題，題目的文字範圍才切得準——題目與題目在
    同一頁上是常態，只按頁切會把前一題的 Correct Answer 算進來。
    """
    doc = fitz.open(path)
    buf, offs, imgs = [], [], []
    pos = 0
    for i in range(doc.page_count):
        t = clean(doc[i].get_text())
        offs.append(pos)
        imgs.append(len(doc[i].get_images()))
        buf.append(t)
        pos += len(t)
    doc.close()
    return "".join(buf), offs, imgs


def page_of(offs, pos):
    """字元位移 → 1-based 頁碼"""
    lo, hi = 0, len(offs) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if offs[mid] <= pos:
            lo = mid
        else:
            hi = mid - 1
    return lo + 1


def scan(path):
    full, offs, imgs = read_pages(path)

    # 區段標題與題號標題會出現在頁面中間，所以在整份字串上按位移排序找，
    # 不能只看「在哪一頁」——Question Set 6 的最後一題與 Testlet 1 的開頭
    # 就在同一頁上。
    marks = [(m.start(), "sec", m) for m in SEC_RE.finditer(full)]
    marks += [(m.start(), "q", m) for m in Q_RE.finditer(full)]

    starts = []
    kind, sec_no = "Question Set", 1     # 第一段沒有標題，就是 Question Set 1
    for pos, what, m in sorted(marks, key=lambda x: x[0]):
        if what == "sec":
            kind, sec_no = m.group(1), int(m.group(2))
            continue
        # 兩種題號標題：470Q 那份是 "Question #N"（歸在目前的 Question Set／Testlet），
        # 兩份增題用的是 "NewQ #N"，自成一段、不吃 Question Set 狀態。
        head, no = m.group(1), int(m.group(2))
        this_kind, this_sec = ("NewQ", 0) if head == "NewQ" else (kind, sec_no)
        sec = sec_code(this_kind, this_sec)
        if starts and starts[-1]["sec"] == sec and starts[-1]["no"] == no:
            continue                      # 同一題的標題重複出現（跨頁頁眉）
        starts.append({"sec": sec, "no": no, "pos": pos})

    out = []
    for idx, s in enumerate(starts):
        end = starts[idx + 1]["pos"] if idx + 1 < len(starts) else len(full)
        body = full[s["pos"]:end]
        p0, p1 = page_of(offs, s["pos"]), page_of(offs, max(s["pos"], end - 1))
        am = ANS_RE.search(body)
        out.append({
            "sec": s["sec"],
            "no": s["no"],
            "label": "%s#%d" % (s["sec"], s["no"]),
            "pages": [p0, p1],
            "k": guess_kind(body),
            "img": sum(imgs[p - 1] for p in range(p0, p1 + 1)),
            "ans": (am.group(1).strip() if am else "").strip() or None,
            "text": body,
        })
    return out, len(offs)


def main():
    path = find_pdf()
    rows, npages = scan(path)

    if "--json" in sys.argv:
        dst = sys.argv[sys.argv.index("--json") + 1]
        os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
        slim = [{k: v for k, v in r.items() if k != "text"} for r in rows]
        json.dump(slim, open(dst, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print("已寫出 %s（%d 題）" % (dst, len(rows)))
        return

    print("%s：%d 頁、%d 題" % (os.path.basename(path), npages, len(rows)))

    kinds = {}
    for r in rows:
        kinds[r["k"]] = kinds.get(r["k"], 0) + 1
    withimg = sum(1 for r in rows if r["img"])
    noans = [r["label"] for r in rows if not r["ans"]]
    print("疑似題型 %s　有圖的題 %d　沒抓到答案的題 %d %s"
          % (kinds, withimg, len(noans), noans[:16] if noans else ""))

    labels = [r["label"] for r in rows]
    dup = sorted({x for x in labels if labels.count(x) > 1})
    print("sec+no 重複：%s" % (dup or "無"))
    print()

    # 逐段報告：每一段內部有沒有跳號才是有意義的（段與段之間本來就各自從 1 起算）
    print("%-8s %5s  %-11s %-5s %s" % ("區段", "題數", "頁", "有圖", "段內缺號"))
    order, seen = [], set()
    for r in rows:
        if r["sec"] not in seen:
            seen.add(r["sec"])
            order.append(r["sec"])
    for sec in sorted(order, key=sec_rank):
        rs = [r for r in rows if r["sec"] == sec]
        nos = [r["no"] for r in rs]
        gap = [x for x in range(1, max(nos) + 1) if x not in nos]
        print("%-8s %5d  %4d-%-6d %-5d %s"
              % (sec, len(rs), rs[0]["pages"][0], rs[-1]["pages"][1],
                 sum(1 for r in rs if r["img"]), gap or "無"))

    if "--stats" in sys.argv:
        return
    print()
    print("  sec+no     pages       k    img  ans")
    for r in rows:
        print("  %-10s %4d-%-6d %-4s %3d  %s"
              % (r["label"], r["pages"][0], r["pages"][1], r["k"],
                 r["img"], (r["ans"] or "—")[:50]))


if __name__ == "__main__":
    main()
