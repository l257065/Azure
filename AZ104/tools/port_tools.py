# -*- coding: utf-8 -*-
"""把 AZ900/tools 底下**與題目內容無關**的工具搬到 AZ104/tools。

AZ-900 的驗證腳本幾乎都是「吃題庫檔、查資料格式」，沒有綁死領域數或題目內容，
所以絕大多數是原封不動複製，只有路徑、檔名、localStorage 前綴要換。

    python tools/port_tools.py

AZ-900 的工具日後有修正時，再跑一次就好；有 `KEEP` 標記的檔案不會被蓋掉。
"""
import io
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
AZ104 = os.path.dirname(HERE)
ROOT = os.path.dirname(AZ104)
SRC = os.path.join(ROOT, "AZ900", "tools")

# ---------------------------------------------------------------------------
# 1. 完全通用，逐位元組複製
#    這幾支只吃「題庫檔」，不管是哪一張考試、幾個領域
# ---------------------------------------------------------------------------
VERBATIM = [
    "append.py",         # 把 batch 接到 bank_doc.current.js 尾端
    "validate.js",       # 資料完整性、逐格對應、標記成對、選項無標記
    "audit.js",          # 校對：v0 與 a 是否一致等九件事
    "patch_fields.py",   # 逐題換欄位的共用工具，吃 JSON 補丁檔
    "vfy.py",            # 核對原文的共用小工具
]

# ---------------------------------------------------------------------------
# 2. 只有路徑／檔名／前綴要換
# ---------------------------------------------------------------------------
SWAP = {
    "extract_html.py": [("az900-practice.html", "az104-practice.html")],
    "splice.py":       [("az900-practice.html", "az104-practice.html")],
    "test_shuffle.js": [("az900-practice.html", "az104-practice.html")],
    "uitest.py":       [("az900-practice.html", "az104-practice.html")],
    "uitest_order.py": [("az900-practice.html", "az104-practice.html"),
                        ("az900.order.v1", "az104.order.v1")],
    "uitest_skip.py":  [("az900-practice.html", "az104-practice.html")],
    "check_star_flag.py": [("az900-practice.html", "az104-practice.html"),
                           ("az900.", "az104.")],
}

# ---------------------------------------------------------------------------
# 3. 要動內容的：PDF 檔名不同（AZ-104 的來源文件還沒放進來），
#    而且圖示腳本的題號對照表是 AZ-900 專屬的，搬過來要清空
# ---------------------------------------------------------------------------
FIND_PDF = '''
def find_pdf():
    """AZ-104 的來源文件檔名還沒定案，所以不寫死：
    先看環境變數 AZ104_PDF，沒有就抓 AZ104/ 底下第一個 .pdf。"""
    env = os.environ.get("AZ104_PDF")
    if env:
        return env
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    pdfs = sorted(f for f in os.listdir(base) if f.lower().endswith(".pdf"))
    if not pdfs:
        raise SystemExit("AZ104/ 底下找不到 PDF；把來源文件放進去，或設環境變數 AZ104_PDF")
    return os.path.join(base, pdfs[0])
'''


def port_verbatim(name):
    shutil.copyfile(os.path.join(SRC, name), os.path.join(HERE, name))
    return name + "（原封不動）"


def port_swap(name, pairs):
    text = io.open(os.path.join(SRC, name), encoding="utf-8").read()
    for old, new in pairs:
        if old not in text:
            raise SystemExit("%s 裡找不到 %r" % (name, old))
        text = text.replace(old, new)
    io.open(os.path.join(HERE, name), "w", encoding="utf-8", newline="\n").write(text)
    return "%s（換 %d 處路徑／前綴）" % (name, len(pairs))


def port_render():
    text = io.open(os.path.join(SRC, "render.py"), encoding="utf-8").read()
    text = text.replace('SCRATCH = os.environ.get("AZ900_PAGES")',
                        'SCRATCH = os.environ.get("AZ104_PAGES")')
    text = text.replace('doc = fitz.open(os.path.join(ROOT, "(new)AZ-900.pdf"))',
                        "doc = fitz.open(find_pdf())")
    text = text.replace("ROOT = os.path.dirname", FIND_PDF.strip() + "\n\n\nROOT = os.path.dirname")
    io.open(os.path.join(HERE, "render.py"), "w", encoding="utf-8", newline="\n").write(text)
    return "render.py（PDF 路徑改成動態尋找）"


def port_clip():
    text = io.open(os.path.join(SRC, "clip.py"), encoding="utf-8").read()
    text = text.replace('PDF = os.path.join(BASE, "..", "(new)AZ-900.pdf")', "PDF = find_pdf()")
    text = text.replace('OUT = os.environ.get("AZ900_PAGES"', 'OUT = os.environ.get("AZ104_PAGES"')
    text = text.replace("BASE = os.path.dirname", FIND_PDF.strip() + "\n\n\nBASE = os.path.dirname")
    io.open(os.path.join(HERE, "clip.py"), "w", encoding="utf-8", newline="\n").write(text)
    return "clip.py（PDF 路徑改成動態尋找）"


def port_icons():
    """icons.py / icons_pdf.py 的對照表是逐題寫死的 AZ-900 座標與檔名，
    搬過來只留骨架；圖示包沿用 AZ900 底下那一份，不重複放。"""
    out = []

    text = io.open(os.path.join(SRC, "icons.py"), encoding="utf-8").read()
    text = text.replace('PACK = os.path.join(BASE, "..", "Azure_Public_Service_Icons_V24", "Icons")',
                        'PACK = os.path.join(BASE, "..", "..", "AZ900",\n'
                        '                    "Azure_Public_Service_Icons_V24", "Icons")')
    text = re.sub(r"MAP = \{.*?\n\}\n", 'MAP = {\n    # 題號: [(選項的英文名, 圖示相對路徑), …]  ← 逐題自己加\n}\n',
                  text, count=1, flags=re.S)
    io.open(os.path.join(HERE, "icons.py"), "w", encoding="utf-8", newline="\n").write(text)
    out.append("icons.py（清空題號對照表，圖示包沿用 AZ900 那一份）")

    text = io.open(os.path.join(SRC, "icons_pdf.py"), encoding="utf-8").read()
    text = text.replace('PDF = os.path.join(BASE, "..", "(new)AZ-900.pdf")', "PDF = find_pdf()")
    text = text.replace('PAGES = os.path.join(BASE, "..", "pages")', 'PAGES = os.path.join(BASE, "..", "pages")')
    text = text.replace("BASE = os.path.dirname", FIND_PDF.strip() + "\n\n\nBASE = os.path.dirname")
    text = re.sub(r"JOBS = \{.*?\n\}\n", 'JOBS = {\n    # 題號: (PDF 頁, [(名稱, x0, x1, y0, y1), …]) 或 (頁, [框…], dpi)  ← 逐題自己加\n}\n',
                  text, count=1, flags=re.S)
    io.open(os.path.join(HERE, "icons_pdf.py"), "w", encoding="utf-8", newline="\n").write(text)
    out.append("icons_pdf.py（清空裁圖座標表）")
    return out


def port_check_layout():
    """AZ-900 版把預覽樣本寫死成 #18／#20。AZ-104 的題號不一樣，
    而且骨架階段題庫是空的，寫死會直接 TypeError 爆掉。改成動態挑樣本。"""
    text = io.open(os.path.join(SRC, "check_layout.js"), encoding="utf-8").read()
    old = text[text.index("console.log('=== 排版預覽（中文，第 18 題）===');"):
               text.index("const seg = DOC.map(")]
    new = """/* 排版預覽：樣本動態挑，不寫死題號（AZ-104 的題號與 AZ-900 不同）；
   題庫還沒收錄時整段跳過，骨架階段才不會爆掉。 */
const sampleZh = DOC.find(q => String(q.q).includes('\\n')) || DOC[0];
if (sampleZh) {
  console.log('=== 排版預覽（中文，第 ' + sampleZh.n + ' 題）===');
  String(sampleZh.q).split('\\n').map(s => s.trim()).filter(Boolean).forEach(s => {
    console.log('[' + (isNote(s) ? '前言 · 小字灰底' : '題目 · 粗體') + '] ' + stripHl(s));
  });

  const sampleEn = DOC.find(q => q.en && String(q.en.q).includes('\\n')) || DOC[0];
  console.log('');
  console.log('=== 排版預覽（英文，第 ' + sampleEn.n + ' 題）===');
  String(sampleEn.en.q).split('\\n').map(s => s.trim()).filter(Boolean).forEach(s => {
    console.log('[' + (isNote(s) ? 'note' : 'question') + '] ' + stripHl(s));
  });
} else {
  console.log('=== 排版預覽：文件題庫還沒有題目，跳過 ===');
}

"""
    text = text.replace(old, new)
    io.open(os.path.join(HERE, "check_layout.js"), "w", encoding="utf-8", newline="\n").write(text)
    return "check_layout.js（預覽樣本改成動態挑、空題庫跳過）"


def port_check_review():
    """同上：情境 1–4 原本寫死 #8 與自製題庫的樣本，改成動態挑並在缺樣本時跳過。
    情境 5–7 原本就有 if 保護，不用動。"""
    text = io.open(os.path.join(SRC, "check_review.js"), encoding="utf-8").read()
    old = text[text.index('console.log("=== 情境 1：'):
               text.index("// 檢查：單複選題一定要有恰好")]
    new = '''/* 情境 1–4 的樣本動態挑；題庫還沒收錄時跳過，骨架階段才不會爆掉。 */
const mcOf = bank => bank.find(q => kindOf(q) === "mc" && q.o && q.o.length >= 2);
const q8 = mcOf(DOC);
if (q8) {
  console.log("=== 情境 1：文件題庫第 " + q8.n + " 題，你選 A，正解 " + LETTER[q8.a[0]] + " ===");
  review(q8, [0], false).forEach(r =>
    console.log(`  ${r.L}  [${LABEL[r.cls].padEnd(5)}] ${r.text}  ${r.tag}`));
}

const q4 = MINE.find(q => kindOf(q) === "mc" && q.o && q.o.length === 4 && q.a.length === 1);
if (q4) {
  console.log("\\n=== 情境 2：四選一，你選 C，正解 " + LETTER[q4.a[0]] + "（自製題庫）===");
  const wrongPick = [0, 1, 2, 3].find(i => i !== q4.a[0]);
  review(q4, [wrongPick], false).forEach(r =>
    console.log(`  ${r.L}  [${LABEL[r.cls].padEnd(5)}] ${r.text.slice(0, 30)}  ${r.tag}`));
}

const qm = DOC.concat(MINE).find(q => kindOf(q) === "mc" && q.a.length === 2);
if (qm) {
  console.log("\\n=== 情境 3：複選題答對一半（需選 2 項）===");
  review(qm, [qm.a[0]], false).forEach(r =>
    console.log(`  ${r.L}  [${LABEL[r.cls].padEnd(5)}] ${r.text.slice(0, 30)}  ${r.tag}`));
}

if (q8) {
  console.log("\\n=== 情境 4：未作答（模擬考跳過）===");
  review(q8, [], false).forEach(r =>
    console.log(`  ${r.L}  [${LABEL[r.cls].padEnd(5)}] ${r.text}  ${r.tag}`));
}

if (!q8 && !q4) console.log("=== 成績單狀態預覽：兩份題庫都還沒有題目，跳過 ===");

'''
    text = text.replace(old, new)
    io.open(os.path.join(HERE, "check_review.js"), "w", encoding="utf-8", newline="\n").write(text)
    return "check_review.js（情境 1–4 改成動態挑樣本、空題庫跳過）"


def main():
    done = []
    for name in VERBATIM:
        done.append(port_verbatim(name))
    done.append(port_check_layout())
    done.append(port_check_review())
    for name, pairs in SWAP.items():
        done.append(port_swap(name, pairs))
    done.append(port_render())
    done.append(port_clip())
    done.extend(port_icons())

    for line in done:
        print("  " + line)
    print("共 %d 支工具已就位" % len(done))


if __name__ == "__main__":
    main()
