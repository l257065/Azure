# -*- coding: utf-8 -*-
"""骨架冒煙測試：題庫還是空的時候，這一頁本身有沒有壞掉。

`uitest.py` 那一組要有題目才跑得動（它會實際點是非表、拖曳配對、選下拉），
在收錄任何題目之前完全跑不了。這一支填的就是那段空窗：確認引擎搬過來之後
還是活的——沒有 JS 例外、分頁數對、五個領域名對、空題庫有好好講人話。

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

        check("題庫是空的（骨架階段本來就該是空的）",
              pg.evaluate("BANK_MINE.length + BANK_DOC.length") == 0)
        check("領域常數是 AZ-104 的五個",
              pg.evaluate("Object.values(DOMAIN_NAME)") == DOMAINS)
        check("分頁索引：錯題本 6、星號題 7",
              pg.evaluate("[TAB_WRONG, TAB_STAR, TAB_MAX]") == [6, 7, 7])
        check("模擬考參數：50 題 / 100 分鐘",
              pg.evaluate("[EXAM_N, EXAM_SEC/60, PASS]") == [50, 100, 70])

        empty = pg.inner_text("#qbox").strip()
        check("空題庫有給說明而不是白畫面", len(empty) > 0, empty[:40])

        # 每個分頁都切一次，確認空題庫下切分頁不會炸
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

        pg.click('#langSeg button[data-lang="zh"]')
        (ROOT / "shots").mkdir(exist_ok=True)
        pg.screenshot(path=str(ROOT / "shots" / "skeleton.png"), full_page=False)
        print("  截圖 shots/skeleton.png")

        browser.close()

    print("")
    if fails:
        print("FAIL：%d 項未通過 —— %s" % (len(fails), "、".join(fails)))
        sys.exit(1)
    print("骨架冒煙測試全部通過")


if __name__ == "__main__":
    main()
