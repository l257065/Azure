# 把新一批題目接到題庫檔的陣列尾端（在最後的 "];" 之前）
#
#   python tools/append.py banks/bank_b_doc.js <batch檔>
#   python tools/build.py                       # 別忘了，不 build 不會進練習頁
#
# batch 檔的開頭必須是 ","（因為是接在既有元素後面）。
import sys

BANK = sys.argv[1]
BATCH = sys.argv[2]

bank = open(BANK, encoding="utf-8").read().rstrip()
batch = open(BATCH, encoding="utf-8").read().strip()

if not bank.endswith("];"):
    print("FAIL: %s 結尾不是 '];'" % BANK)
    sys.exit(1)

merged = bank[:-2].rstrip() + "\n" + batch + "\n];\n"
open(BANK, "w", encoding="utf-8").write(merged)
print("已附加，%s 長度 %d -> %d" % (BANK, len(bank), len(merged)))
print("記得跑：python tools/build.py")
