# -*- coding: utf-8 -*-
"""冒煙測試：這一頁本身有沒有壞掉。

`uitest.py` 那一組要有題目才跑得動（它會實際點是非表、拖曳配對、選下拉），
在收錄任何題目之前完全跑不了。這一支填的就是那段空窗，收錄開始之後也繼續有用：
確認沒有 JS 例外、分頁數對、五個領域名對、AZ-104 的常數對、來源座標 sec+no 解得出來，
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

        # 來源座標 sec + no：區段名稱與跳題寫法的解析
        check("區段代號翻得出名字（S2 / T3 / NewQ）",
              pg.evaluate("[secName('S2',false), secName('T3',false), secName('NewQ',false),"
                          " secName('S2',true)]")
              == ["題組 2", "案例 3", "增題", "Question Set 2"])
        check("跳題吃「段-題號」與純數字兩種寫法",
              pg.evaluate("[parseJump('2-17'), parseJump('T3-2'), parseJump('N63'),"
                          " parseJump('17'), parseJump('亂打')]")
              == [{"sec": "S2", "no": 17}, {"sec": "T3", "no": 2},
                  {"sec": "NewQ", "no": 63}, {"pos": 17}, None])
        gaps = pg.evaluate("docGaps()")
        check("段內缺號算得出來，而且不會把別段的號碼當缺號",
              gaps["total"] == n_doc and len(gaps["gaps"]) == 0,
              "共 %d 題、%d 段（%s）、缺號 %s"
              % (gaps["total"], len(gaps["secs"]),
                 "／".join(x["sec"] for x in gaps["secs"]), gaps["gaps"] or "無"))

        # 真的在跳題框裡打字並送出。上面驗 parseJump() 是驗函式，驗不到
        # input 自己的 pattern／maxlength——那個欄位原本有 pattern="[0-9]*"，
        # 打「1-6」會被瀏覽器擋在「請符合要求的格式」，連 parseJump() 都進不去。
        pg.click("#cfgBtn")
        pg.wait_for_timeout(120)
        pg.click('#srcSeg button[data-src="doc"]')
        pg.wait_for_timeout(200)
        if pg.is_visible("#cfgClose"):
            pg.click("#cfgClose")
            pg.wait_for_timeout(150)

        check("跳題框沒有把非數字擋掉的 pattern",
              not pg.get_attribute("#jumpNo", "pattern"),
              pg.get_attribute("#jumpNo", "pattern"))
        check("跳題框裝得下 NewQ-63 這種長度",
              int(pg.get_attribute("#jumpNo", "maxlength") or 0) >= 7,
              pg.get_attribute("#jumpNo", "maxlength"))

        for typed, want in (("1-6", ("S1", 6)), ("S1-13", ("S1", 13)), ("3", None)):
            errors.clear()
            pg.fill("#jumpNo", typed)
            pg.press("#jumpNo", "Enter")
            pg.wait_for_timeout(200)
            valid = pg.evaluate("document.getElementById('jumpNo').checkValidity()")
            cur = pg.evaluate("({sec:S.pool[S.idx].sec, no:S.pool[S.idx].no, idx:S.idx})")
            if want:
                ok = valid and (cur["sec"], cur["no"]) == want
                check("跳題框打「%s」→ %s#%d" % (typed, want[0], want[1]), ok,
                      "valid=%s 目前在 %s#%s" % (valid, cur["sec"], cur["no"]))
            else:
                check("跳題框打「%s」→ 本輪第 %s 題" % (typed, typed),
                      valid and cur["idx"] == int(typed) - 1,
                      "valid=%s idx=%s" % (valid, cur["idx"]))
            check("跳題「%s」不會出錯" % typed, not errors, errors[:2])

        # 兩份題庫各自檢查：有題目就要畫得出題目，沒題目就要給說明而不是白畫面。
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
