#!/usr/bin/env python3
"""把引擎樣板與兩份題庫組成可以直接開的單一檔案。

    az104-engine.html          引擎樣板（題庫是空的，只有標記）
    banks/bank_a_mine.js       題庫 A：自製
    banks/bank_b_doc.js        題庫 B：文件轉錄
                ↓
    az104-practice.html        產出物（直接用瀏覽器開的就是這個）

為什麼要拆：A 與 B 由兩個人各自維護，兩邊同時加題目時只會改到自己那支
banks/*.js，git 不會衝突。產出物 az104-practice.html 在 .gitattributes 裡
標成不可自動合併，**併版時衝突一律用重跑這支腳本解決，不要手改**。

用法：
    python tools/build.py            # 建置
    python tools/build.py --check    # 只檢查產出物是否為最新，不寫檔（CI 用）
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, "az104-engine.html")
OUT = os.path.join(ROOT, "az104-practice.html")
BANKS = [
    ("A", "/*__BANK_A__*/", "/*__END_BANK_A__*/",
     os.path.join(ROOT, "banks", "bank_a_mine.js"), "const BANK_MINE = ["),
    ("B", "/*__BANK_B__*/", "/*__END_BANK_B__*/",
     os.path.join(ROOT, "banks", "bank_b_doc.js"), "const BANK_DOC = ["),
]

BANNER = (
    "<!-- ===================================================================\n"
    "     產出物，請勿手動編輯。手改的東西下一次建置就會被蓋掉。\n"
    "       改引擎（版面、作答邏輯、模擬考設定）→ az104-engine.html\n"
    "       改題庫 A（自製）                     → banks/bank_a_mine.js\n"
    "       改題庫 B（文件轉錄）                 → banks/bank_b_doc.js\n"
    "     然後跑 python tools/build.py\n"
    "     ================================================================ -->\n"
)


def fail(msg):
    print("FAIL: " + msg)
    sys.exit(1)


def main():
    check_only = "--check" in sys.argv[1:]

    if not os.path.exists(ENGINE):
        fail("找不到引擎樣板 %s" % ENGINE)
    html = open(ENGINE, encoding="utf-8").read()

    counts = []
    for name, begin, end, path, decl in BANKS:
        if not os.path.exists(path):
            fail("找不到題庫 %s：%s" % (name, path))
        body = open(path, encoding="utf-8").read().rstrip("\n")

        if decl not in body:
            fail("題庫 %s 裡找不到宣告 %r" % (name, decl))
        if not body.rstrip().endswith("];"):
            fail("題庫 %s 的結尾不是 '];'" % name)

        if html.count(begin) != 1 or html.count(end) != 1:
            fail("引擎樣板裡的 %s 標記不是剛好一組" % name)

        # 樣板裡的標記區塊必須永遠是空宣告。有人（或某次併版）把真的題目寫進
        # 樣板時就停在這裡——否則下面的取代會把那些題目靜靜蓋掉。
        pat = re.compile(re.escape(begin) + r"(.*?)" + re.escape(end), re.S)
        held = pat.search(html).group(1)
        if count_items(held):
            fail("az104-engine.html 的題庫 %s 區塊裡有 %d 題。樣板不放題目，"
                 "請把它們搬到 %s 再重跑。"
                 % (name, count_items(held), os.path.relpath(path, ROOT)))

        html, n = pat.subn(lambda _m, b=body: begin + "\n" + b + "\n" + end, html, count=1)
        if n != 1:
            fail("題庫 %s 取代失敗" % name)

        counts.append((name, os.path.basename(path), count_items(body), len(body)))

    html = BANNER + html

    old = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else None
    if check_only:
        if old != html:
            fail("az104-practice.html 不是最新的，請跑 python tools/build.py")
        print("OK: 產出物與來源一致")
        return
    open(OUT, "w", encoding="utf-8").write(html)

    for name, fn, items, chars in counts:
        print("題庫 %s  %-18s %4d 題  %8d 字元" % (name, fn, items, chars))
    print("已寫出 %s（%d 字元%s）" % (
        os.path.basename(OUT), len(html),
        "，內容未變" if old == html else ""))


def count_items(body):
    """數陣列裡有幾筆題目：只算頂層以 '{' 開頭的行。"""
    inside = False
    n = 0
    for line in body.splitlines():
        s = line.strip()
        if not inside:
            if s.endswith("= ["):
                inside = True
            continue
        if s == "];":
            break
        if s.startswith("{"):
            n += 1
    return n


if __name__ == "__main__":
    main()
