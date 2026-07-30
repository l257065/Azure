# 把 az104-practice.html 裡的 <script> 內容抽出成 .js，供 node --check 與驗證腳本使用。
# 用法: python tools/extract_html.py <輸出的.js路徑>
import re, sys, os

HTML = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "az104-practice.html")
out = sys.argv[1] if len(sys.argv) > 1 else "scratch_script.js"

html = open(HTML, encoding="utf-8").read()
# 檔案裡可能有多個 <script>（例如 <head> 裡的佈景主題初始化），
# 只取含有題庫的那一塊；非貪婪比對，才不會把兩塊接在一起。
blocks = re.findall(r"<script[^>]*>(.*?)</script>", html, re.S)
if not blocks:
    print("FAIL: 找不到 <script> 區塊")
    sys.exit(1)
main = [b for b in blocks if "const BANK_DOC" in b]
if not main:
    print("FAIL: 找不到含 BANK_DOC 的 <script> 區塊")
    sys.exit(1)
body = max(main, key=len)

open(out, "w", encoding="utf-8").write(body)
print("已輸出 %s（%d 字元，共 %d 個 script 區塊）" % (out, len(body), len(blocks)))
