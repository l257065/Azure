# -*- coding: utf-8 -*-
"""冒煙測試：這一頁本身有沒有壞掉。

`uitest.py` 那一組要有題目才跑得動（它會實際點是非表、拖曳配對、選下拉），
在收錄任何題目之前完全跑不了。這一支填的就是那段空窗，收錄開始之後也繼續有用：
確認沒有 JS 例外、分頁數對、五個領域名對、AZ-104 的常數對、題號編碼算得出來，
以及題庫空的時候有好好講人話、有題目的時候真的畫得出來。

    python tools/smoke.py        # 需要 pip install playwright && playwright install chromium
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

# Windows 主控台預設是 cp950，印到 ✗ / ★ 這種字就會整支掛掉
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

ROOT = Path(__file__).resolve().parent.parent
URL = (ROOT / "az104-practice.html").as_uri()

DOMAINS = ["身分與治理", "儲存體", "運算資源", "虛擬網路", "監控與維護"]
TABS = ["全部", "身分治理", "儲存體", "運算", "網路", "監控", "錯題本", "星號題"]

fails = []


def check(name, ok, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + name + (("  — " + str(detail)) if detail else ""))
    if not ok:
        fails.append(name)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        pg = browser.new_page(viewport={"width": 1280, "height": 900})

        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)

        pg.goto(URL)
        pg.wait_for_timeout(400)

        check("載入時沒有 JS 例外", not errors, errors[:3])

        tabs = pg.eval_on_selector_all("nav.tabs button", "els => els.map(e => e.textContent.trim())")
        check("分頁有 8 個（全部＋五領域＋錯題本＋星號題）", len(tabs) == 8, tabs)
        check("分頁名稱是 AZ-104 的", all(t.endswith(x) for t, x in zip(tabs, TABS)), tabs)

        n_mine, n_doc = pg.evaluate("[BANK_MINE.length, BANK_DOC.length]")
        print("  題庫 A（自製）%d 題　題庫 B（文件）%d 題" % (n_mine, n_doc))

        check("領域常數是 AZ-104 的五個",
              pg.evaluate("Object.values(DOMAIN_NAME)") == DOMAINS)
        check("分頁索引：錯題本 6、星號題 7",
              pg.evaluate("[TAB_WRONG, TAB_STAR, TAB_MAX]") == [6, 7, 7])
        check("模擬考參數：50 題 / 100 分鐘",
              pg.evaluate("[EXAM_N, EXAM_SEC/60, PASS]") == [50, 100, 70])

        # 題號編碼：題組 S 第 q 題 = S*1000+q、案例 T 第 q 題 = 10000+T*100+q
        check("題號解碼正確（2017 → 題組 2 第 17 題、10302 → 案例 3 第 2 題）",
              pg.evaluate("[docNo(2017), docNo(10302)]")
              == [{"kind": "s", "sec": 2, "q": 17}, {"kind": "t", "sec": 3, "q": 2}])
        gaps = pg.evaluate("docGaps()")
        check("段內缺號算得出來，而且不會把別段的號碼當缺號",
              gaps["total"] == n_doc and len(gaps["gaps"]) == 0,
              "共 %d 題、%d 段、缺號 %s"
              % (gaps["total"], len(gaps["secs"]), gaps["gaps"] or "無"))

        # 開頁預設是題庫 A。兩份題庫各自檢查：有題目就要畫得出題目，
        # 沒題目就要給說明而不是白畫面。
        for src, label, cnt in (("mine", "A 自製", n_mine), ("doc", "B 文件", n_doc)):
            errors.clear()
            pg.click("#cfgBtn")                 # 切題庫的按鈕在設定面板裡
            pg.wait_for_timeout(120)
            pg.click('#srcSeg button[data-src="%s"]' % src)
            pg.wait_for_timeout(150)
            if pg.is_visible("#cfgClose"):      # 切題庫時面板通常會自己關掉
                pg.click("#cfgClose")
                pg.wait_for_timeout(150)
            body = pg.inner_text("#qbox").strip()
            preview = body[:40].replace("\n", " ")
            if cnt:
                check("題庫 %s（%d 題）真的畫得出題目" % (label, cnt), len(body) > 40, preview)
            else:
                check("題庫 %s 是空的，有給說明而不是白畫面" % label, len(body) > 0, preview)
            check("切到題庫 %s 不會出錯" % label, not errors, errors[:2])

        # 每個分頁都切一次，確認切分頁不會炸
        for i in range(8):
            errors.clear()
            pg.click("nav.tabs button#t%d" % i)
            pg.wait_for_timeout(80)
            check("切到分頁 %d（%s）不會出錯" % (i, TABS[i]), not errors, errors[:2])

        # 三種語言模式
        for lang in ("zh", "zhen", "en"):
            errors.clear()
            pg.click('#langSeg button[data-lang="%s"]' % lang)
            pg.wait_for_timeout(80)
            check("語言切到 %s 不會出錯" % lang, not errors, errors[:2])

        # 回到「全部」＋有題目的題庫再截圖，不然只會拍到迴圈最後停在的那個空分頁
        pg.click('#langSeg button[data-lang="zh"]')
        pg.click("nav.tabs button#t0")
        pg.wait_for_timeout(200)
        (ROOT / "shots").mkdir(exist_ok=True)
        pg.screenshot(path=str(ROOT / "shots" / "smoke.png"), full_page=False)
        print("  截圖 shots/smoke.png")

        # 題數說明面板：題號編碼規則與逐段題數，改過就順手看一眼
        pg.click("#infoBtn")
        pg.wait_for_timeout(250)
        pg.screenshot(path=str(ROOT / "shots" / "smoke_numbering.png"), full_page=False)
        print("  截圖 shots/smoke_numbering.png")

        browser.close()

    print("")
    if fails:
        print("FAIL：%d 項未通過 —— %s" % (len(fails), "、".join(fails)))
        sys.exit(1)
    print("冒煙測試全部通過")


if __name__ == "__main__":
    main()
