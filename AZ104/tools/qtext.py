#!/usr/bin/env python3
"""把指定題目的原文倒出來，轉錄時讀這個而不是一頁一頁看圖。

這份 PDF 的文字是可以抽的，純文字題（沒有圖的那 121 題）直接讀這裡就夠了。
題目裡有表格、入口網站截圖、HOTSPOT 是非表、DRAG DROP 答案區的，
`img` 會大於 0，那種還是得 render.py 出圖用眼睛看——文字抽出來會缺格線與版面。

    AZ104_PDF="AZ104考題/NEW-AZ-104-470Q.pdf" python tools/qtext.py 1001-1010
    AZ104_PDF="..." python tools/qtext.py 1001 1005 2017

題號是 scan_pdf.py 的編碼題號（題組 S 第 q 題 = S*1000+q）。
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scan_pdf import find_pdf, scan  # noqa: E402


def want(argv):
    out = []
    for a in argv:
        if "-" in a.strip("-") and re.match(r"^\d+-\d+$", a):
            lo, hi = (int(x) for x in a.split("-"))
            out.append((lo, hi))
        else:
            out.append((int(a), int(a)))
    return out


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    ranges = want(sys.argv[1:])

    path = find_pdf()
    rows, _ = scan(path)

    picked = [r for r in rows if any(lo <= r["n"] <= hi for lo, hi in ranges)]
    if not picked:
        raise SystemExit("這些題號在 %s 裡找不到" % os.path.basename(path))

    for r in picked:
        p0, p1 = r["pages"]
        print("=" * 72)
        print("n=%d  %s  Question #%d  p.%d-%d  k?=%s  img=%d  ans=%s"
              % (r["n"], r["sec"], r["q"], p0, p1, r["k"], r["img"], r["ans"]))
        if r["img"]:
            print("!! 這幾頁有 %d 張圖，文字抽出來會缺表格與版面，要出圖用眼睛看：" % r["img"])
            print("   AZ104_PDF=%s python tools/render.py %d %d 150"
                  % (os.path.basename(path), p0, p1))
        print("=" * 72)
        print(re.sub(r"\n{3,}", "\n\n", r["text"]).strip())
        print()


if __name__ == "__main__":
    main()
