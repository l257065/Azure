#!/usr/bin/env python3
"""掃過來源 PDF，列出每一題在哪幾頁、疑似題型、有沒有圖、標的答案是什麼。

轉錄前先跑這支，得到一份工作清單，就不用一頁一頁翻著找題號邊界。

    AZ104_PDF="AZ104考題/NEW-AZ-104-470Q.pdf" python tools/scan_pdf.py
    AZ104_PDF="..." python tools/scan_pdf.py --json out/index.json
    AZ104_PDF="..." python tools/scan_pdf.py --stats

欄位：
    n        題庫裡用的題號，**已編碼進區段**（見下）
    sec      來源區段，例如 "Question Set 2" / "Testlet 3" / "NewQ"
    q        該區段內的題號
    pages    這一題橫跨的頁碼（1-based，含）
    k        疑似題型：mc / hs / dd / dl（看關鍵字猜的，轉錄時要自己確認）
    img      這幾頁裡的圖片數。>0 就要 render.py 出圖用眼睛看
    ans      文件標的 Correct Answer（可能是錯的，見 AZ104考題/*Correct.txt 的更正）

**題號會撞號，所以要編碼。** 三份來源檔各有各的編號方式：

    NEW-AZ-104-470Q.pdf   分成 Question Set 1–6 與 Testlet 1–10，
                          每一段的 `Question #` 都從 1 重新算
    增題 62Q ＋ NewQ63-Q76  用的是 `NewQ #N`，兩份接在一起是 NewQ #1–#76

編碼規則：

    Question Set S 的第 q 題  →  n = S*1000 + q         1001…6047
    Testlet T 的第 q 題       →  n = 10000 + T*100 + q    10101…11004
    NewQ #q                   →  n = 20000 + q            20001…20076

這樣 n 仍然是數字（跳題功能要數字），而且看得懂：`2017` = Question Set 2 第 17 題，
`10302` = Testlet 3 第 2 題，`20063` = NewQ #63。
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


def encode(kind, sec_no, q):
    """把「區段 + 區段內題號」壓成一個看得懂的數字題號（見檔頭說明）。"""
    if kind == "NewQ":
        return 20000 + q
    if kind == "Question Set":
        return sec_no * 1000 + q
    return 10000 + sec_no * 100 + q


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
        head, q = m.group(1), int(m.group(2))
        this_kind, this_sec = ("NewQ", 0) if head == "NewQ" else (kind, sec_no)
        n = encode(this_kind, this_sec, q)
        if starts and starts[-1]["n"] == n:
            continue                      # 同一題的標題重複出現（跨頁頁眉）
        label = "NewQ" if this_kind == "NewQ" else "%s %d" % (this_kind, this_sec)
        starts.append({"n": n, "sec": label, "q": q, "pos": pos})

    out = []
    for idx, s in enumerate(starts):
        end = starts[idx + 1]["pos"] if idx + 1 < len(starts) else len(full)
        body = full[s["pos"]:end]
        p0, p1 = page_of(offs, s["pos"]), page_of(offs, max(s["pos"], end - 1))
        am = ANS_RE.search(body)
        out.append({
            "n": s["n"],
            "sec": s["sec"],
            "q": s["q"],
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
    noans = [r["n"] for r in rows if not r["ans"]]
    print("疑似題型 %s　有圖的題 %d　沒抓到答案的題 %d %s"
          % (kinds, withimg, len(noans), noans[:20] if noans else ""))

    ns = [r["n"] for r in rows]
    dup = sorted({x for x in ns if ns.count(x) > 1})
    print("編碼後題號重複：%s" % (dup or "無"))
    print()

    # 逐段報告：每一段內部有沒有跳號才是有意義的
    print("%-16s %5s  %-11s %-5s %s" % ("區段", "題數", "頁", "有圖", "段內缺號"))
    order, seen = [], set()
    for r in rows:
        if r["sec"] not in seen:
            seen.add(r["sec"])
            order.append(r["sec"])
    for sec in order:
        rs = [r for r in rows if r["sec"] == sec]
        qs = [r["q"] for r in rs]
        gap = [x for x in range(1, max(qs) + 1) if x not in qs]
        print("%-16s %5d  %4d-%-6d %-5d %s"
              % (sec, len(rs), rs[0]["pages"][0], rs[-1]["pages"][1],
                 sum(1 for r in rs if r["img"]), gap or "無"))

    if "--stats" in sys.argv:
        return
    print()
    print("  n    sec                 pages     k   img  ans")
    for r in rows:
        print("%-6d %-18s %4d-%-4d %-4s %3d  %s"
              % (r["n"], r["sec"], r["pages"][0], r["pages"][1], r["k"],
                 r["img"], (r["ans"] or "—")[:50]))


if __name__ == "__main__":
    main()
