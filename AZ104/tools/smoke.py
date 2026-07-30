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
        gaps = pg.evaluate("docGaps()")
        check("段內缺號算得出來，而且不會把別段的號碼當缺號",
              gaps["total"] == n_doc and len(gaps["gaps"]) == 0,
              "共 %d 題、%d 段（%s）、缺號 %s"
              % (gaps["total"], len(gaps["secs"]),
                 "／".join(x["sec"] for x in gaps["secs"]), gaps["gaps"] or "無"))

        # 真的操作跳題那兩格。端對端才驗得到 select 的選項、input 的
        # pattern／maxlength、以及瀏覽器的表單驗證有沒有把輸入擋在程式之外
        # ——上一版右格是單一欄位又帶 pattern="[0-9]*"，打「1-6」會被擋在
        # 「請符合要求的格式」，連跳題邏輯都進不去。
        pg.click("#cfgBtn")
        pg.wait_for_timeout(120)
        pg.click('#srcSeg button[data-src="doc"]')
        pg.wait_for_timeout(200)
        if pg.is_visible("#cfgClose"):
            pg.click("#cfgClose")
            pg.wait_for_timeout(150)

        opts = pg.eval_on_selector_all(
            "#jumpSec option", "els => els.map(e => [e.value, e.textContent])")
        check("左格就是這一輪有的區段，沒有多加別的選項",
              [o[0] for o in opts] == ["S1"] and opts[0][1] == "題組 1", opts)
        check("這一輪有來源座標，左格看得見", not pg.is_hidden("#jumpSec"))

        for sec, num, want in (("S1", "6", ("S1", 6)), ("S1", "13", ("S1", 13))):
            errors.clear()
            pg.select_option("#jumpSec", sec)
            pg.fill("#jumpNo", num)
            pg.press("#jumpNo", "Enter")
            pg.wait_for_timeout(200)
            valid = pg.evaluate("document.getElementById('jumpNo').checkValidity()")
            cur = pg.evaluate("({sec:S.pool[S.idx].sec, no:S.pool[S.idx].no})")
            check("跳題〔%s〕〔%s〕→ %s#%d" % (sec, num, want[0], want[1]),
                  valid and (cur["sec"], cur["no"]) == want,
                  "valid=%s 目前在 %s#%s" % (valid, cur["sec"], cur["no"]))
            check("跳題〔%s〕〔%s〕不會出錯" % (sec, num), not errors, errors[:2])

        # 跳不存在的題號要講話，而不是靜靜不動或炸掉
        errors.clear()
        pg.select_option("#jumpSec", "S1")
        pg.fill("#jumpNo", "999")
        pg.press("#jumpNo", "Enter")
        pg.wait_for_timeout(200)
        msg = pg.inner_text("#jumpMsg").strip()
        check("跳到不存在的題號會說明", "沒有" in msg, msg[:44])
        check("跳到不存在的題號不會出錯", not errors, errors[:2])
        pg.fill("#jumpNo", "")

        # 題庫裡每一種題型都畫一次，確認格數對得上資料。
        # uitest.py 是深入的互動測試（真的拖、真的點），但它要 hs/dd/dl 與複選題
        # 全都到齊才跑得動；收錄過程中會有一段時間只有部分題型，這裡先做結構檢查，
        # 新題型第一次進題庫就有人守著。
        kinds = pg.evaluate("[...new Set(BANK_DOC.map(q => q.k || 'mc'))].sort()")
        print("  題庫 B 目前的題型：%s" % "、".join(kinds))
        SHAPE = {
            "mc": (".opts .opt", "o", "選項"),
            "hs": (".hs .hrow", "s", "敘述列"),
            "dd": (".dd .slot", "tgt", "答案格"),
            "dl": (".dl select", "dd", "下拉格"),
        }
        for k in kinds:
            sel, field, what = SHAPE[k]
            info = pg.evaluate("""(k) => {
              const q = BANK_DOC.find(x => (x.k || 'mc') === k);
              S.exam = false; S.tab = 0;
              S.pool = [q]; S.idx = 0; S.right = 0; S.total = 0;
              S.answers = []; S.gr = []; S.graded = false;
              report.classList.remove('show');
              renderQ();
              return {sec:q.sec, no:q.no, want:(q[%r] || []).length, a:q.a.length};
            }""" % field, k)
            got = pg.locator(sel).count()
            check("%s 題（%s#%d）畫出 %d 個%s"
                  % (k, info["sec"], info["no"], info["want"], what),
                  got == info["want"], "實際 %d 個" % got)
            if k != "mc":       # 多格題型：答案格數要等於答案數
                check("%s 題的答案數對得上格數" % k, info["a"] == info["want"],
                      "a=%d 格=%d" % (info["a"], info["want"]))
        # 模擬考成績單：領域細項必須有 D_MAX 格。
        # 這一段原本寫死三格（AZ-900 的殘留），只要抽到領域 4／5 的題目，
        # byD[4] 就是 undefined，整張成績單會爆掉——題庫只有領域 1-3 時看不出來。
        if n_doc:
            errors.clear()
            pg.click("#examBtn")
            pg.wait_for_function("S.exam === true && S.pool.length > 0")
            pg.evaluate("() => finishRound()")
            pg.wait_for_function("report.classList.contains('show')", timeout=10000)
            d_max = pg.evaluate("() => D_MAX")
            rows = pg.eval_on_selector_all(".dbreak .row .n", "els => els.map(e => e.textContent)")
            check("模擬考成績單的領域細項有 D_MAX（%d）格" % d_max,
                  len(rows) == d_max, "實際 %d 格：%s" % (len(rows), rows))
            check("成績單逐題檢討的筆數等於抽題數",
                  pg.locator(".rev .item").count() == pg.evaluate("S.pool.length"),
                  "%d vs %d" % (pg.locator(".rev .item").count(),
                                pg.evaluate("S.pool.length")))
            check("結算成績單不會出錯", not errors, errors[:2])
            pg.click("#examBtn")
            pg.wait_for_function("S.exam === false")

        pg.evaluate("S.tab = 0; startRound(true)")
        pg.wait_for_timeout(150)

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
