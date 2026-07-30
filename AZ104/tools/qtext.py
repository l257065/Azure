#!/usr/bin/env python3
"""把指定題目的原文倒出來，轉錄時讀這個而不是一頁一頁看圖。

這份 PDF 的文字是可以抽的，純文字題（`img` 為 0 的那些）直接讀這裡就夠了。
題目裡有表格、入口網站截圖、HOTSPOT 是非表、DRAG DROP 答案區的，`img` 會大於 0，
那種還是得 render.py 出圖用眼睛看——文字抽出來會缺格線與版面。

位置寫法（大小寫都可以，就是題庫檔裡的 sec + no）：

    S1-1        題組 1 第 1 題
    S1-14..27   題組 1 第 14 到 27 題
    S1          整個題組 1
    T3-2        案例 3 第 2 題
    NewQ-63     增題 NewQ 第 63 題

    AZ104_PDF="AZ104考題/NEW-AZ-104-470Q.pdf" python tools/qtext.py S1-14..27
    AZ104_PDF="..." python tools/qtext.py S2-17 T3-2
    AZ104_PDF="..." python tools/qtext.py S1            # 整段
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scan_pdf import find_pdf, scan, sec_rank  # noqa: E402

# S1-14..27 / S1-14 / S1
SPEC = re.compile(r"^(S\d+|T\d+|NewQ)(?:-(\d+)(?:\.\.(\d+))?)?$", re.I)


def norm_sec(sec):
    return "NewQ" if sec.lower() == "newq" else sec[0].upper() + sec[1:]


def want(argv):
    """→ [(sec, lo, hi)]，lo/hi 為 None 表示整段"""
    out = []
    for a in argv:
        m = SPEC.match(a.strip())
        if not m:
            raise SystemExit("看不懂的位置寫法：%r\n%s" % (a, __doc__))
        sec, lo, hi = norm_sec(m.group(1)), m.group(2), m.group(3)
        lo = int(lo) if lo else None
        hi = int(hi) if hi else lo
        out.append((sec, lo, hi))
    return out


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    ranges = want(sys.argv[1:])

    path = find_pdf()
    rows, _ = scan(path)

    def hit(r):
        for sec, lo, hi in ranges:
            if r["sec"] != sec:
                continue
            if lo is None or lo <= r["no"] <= hi:
                return True
        return False

    picked = sorted((r for r in rows if hit(r)),
                    key=lambda r: (sec_rank(r["sec"]), r["no"]))
    if not picked:
        raise SystemExit("這些位置在 %s 裡找不到" % os.path.basename(path))

    for r in picked:
        p0, p1 = r["pages"]
        print("=" * 72)
        print("%s  （Question #%d）  p.%d-%d  k?=%s  img=%d  ans=%s"
              % (r["label"], r["no"], p0, p1, r["k"], r["img"], r["ans"]))
        if r["img"]:
            print("!! 這幾頁有 %d 張圖，文字抽出來會缺表格與版面，要出圖用眼睛看：" % r["img"])
            print("   AZ104_PDF=%s python tools/render.py %d %d 150"
                  % (os.path.basename(path), p0, p1))
        print("=" * 72)
        print(re.sub(r"\n{3,}", "\n\n", r["text"]).strip())
        print()

    print("—— 共 %d 題（%s）" % (len(picked), ", ".join(r["label"] for r in picked)))


if __name__ == "__main__":
    main()
