import fitz, os, sys

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


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRATCH = os.environ.get("AZ104_PAGES") or os.path.join(ROOT, "pages")
os.makedirs(SCRATCH, exist_ok=True)
doc = fitz.open(find_pdf())

start = int(sys.argv[1])          # 1-based, 含
end = int(sys.argv[2])            # 1-based, 含
dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 130

for i in range(start - 1, min(end, doc.page_count)):
    pix = doc[i].get_pixmap(dpi=dpi)
    path = os.path.join(SCRATCH, "p%03d.png" % (i + 1))
    pix.save(path)
    print(path, pix.width, "x", pix.height, os.path.getsize(path) // 1024, "KB")
