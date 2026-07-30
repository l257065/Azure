# -*- coding: utf-8 -*-
"""驗設定裡的「出題順序」：預設依題號、可切隨機、模擬考一律隨機、做到一半不會被洗掉。
用法： python tools/uitest_order.py
"""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
URL = (ROOT / "az104-practice.html").as_uri()
SHOT = ROOT / "shots"
SHOT.mkdir(exist_ok=True)

NUMS = "() => S.pool.map(q => q.n)"          # 本輪題號（文件題庫才有 n）

results = []
def check(name, cond, detail=""):
    results.append(bool(cond))
    print(("  PASS  " if cond else "  FAIL  ") + name + ("  " + detail if detail else ""))

def asc(xs):
    return all(b > a for a, b in zip(xs, xs[1:]))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 900, "height": 1100})
    errors = []
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.on("console", lambda m: errors.append("console." + m.type + ": " + m.text)
          if m.type == "error" else None)
    pg.goto(URL)
    pg.wait_for_selector("#qbox")
    pg.evaluate("() => { try{ localStorage.clear(); }catch(e){} }")
    pg.reload()
    pg.wait_for_selector("#qbox")
    pg.evaluate("() => setSource('doc')")    # 文件題庫才有題號可以驗順序

    print("\n[1] 預設：依題號")
    check("S.order 預設 seq", pg.evaluate("() => S.order") == "seq")
    ns = pg.evaluate(NUMS)
    check("本輪題號由小到大", asc(ns), "%s ... %s" % (ns[:5], ns[-2:]))
    # AZ-104 的題號把題組編了進去（題組 1 第 1 題 = 1001），所以最小題號不是 1。
    # 拿題庫實際的最小題號來比，別寫死。
    lo = pg.evaluate("() => Math.min(...BANK.map(q => q.n))")
    check("第 1 題就是最小題號 #%d" % lo, ns[0] == lo, "n=%s" % ns[0])

    print("\n[2] 設定面板")
    pg.click("#cfgBtn")
    pg.wait_for_selector("#cfgwrap.show")
    check("有「出題順序」這一列", pg.is_visible("#orderSeg"))
    check("標籤是「出題順序」", pg.inner_text("#cfgOrderLab").strip() == "出題順序",
          pg.inner_text("#cfgOrderLab").strip())
    check("「依題號」是按下的狀態",
          pg.get_attribute('#orderSeg button[data-order="seq"]', "aria-pressed") == "true")
    check("「隨機」沒被按下",
          pg.get_attribute('#orderSeg button[data-order="rand"]', "aria-pressed") == "false")
    pg.screenshot(path=str(SHOT / "cfg_order.png"), full_page=True)

    print("\n[3] 切成隨機（這一輪還沒作答 → 立刻套用）")
    pg.click('#orderSeg button[data-order="rand"]')
    check("S.order = rand", pg.evaluate("() => S.order") == "rand")
    ns2 = pg.evaluate(NUMS)
    check("題號不再照順序", not asc(ns2), "%s ..." % ns2[:6])
    check("題數沒少", len(ns2) == len(ns), "%d vs %d" % (len(ns2), len(ns)))
    check("題目一題不差", sorted(ns2) == sorted(ns))
    check("寫進 localStorage",
          pg.evaluate("() => { try{ return localStorage.getItem('az104.order.v1'); }catch(e){ return 'n/a'; } }") in ("rand", "n/a"))

    print("\n[4] 重新載入還記得")
    pg.reload()
    pg.wait_for_selector("#qbox")
    check("重開還是 rand", pg.evaluate("() => S.order") == "rand")
    pg.evaluate("() => setSource('doc')")
    check("重開後的順序仍是打散的", not asc(pg.evaluate(NUMS)))

    print("\n[5] 切回依題號")
    pg.evaluate("() => setOrder('seq')")
    check("S.order = seq", pg.evaluate("() => S.order") == "seq")
    check("題號又照順序了", asc(pg.evaluate(NUMS)))

    print("\n[6] 做到一半改設定：不洗掉進度，下一輪才換")
    need = pg.evaluate("() => S.pool[S.idx].a.length")
    for i in range(need):
        pg.query_selector_all(".opt")[i].click()
    pg.click("#btnCheck")
    pg.click("#btnCheck")                     # 批改後主鈕＝下一題
    before = pg.evaluate("() => ({i:S.idx, t:S.total, ns:S.pool.map(q=>q.n)})")
    pg.evaluate("() => setOrder('rand')")
    after = pg.evaluate("() => ({i:S.idx, t:S.total, ns:S.pool.map(q=>q.n)})")
    check("設定有記下來", pg.evaluate("() => S.order") == "rand")
    check("這一輪順序沒被動", after["ns"] == before["ns"])
    check("停在原本那一題", after["i"] == before["i"], "idx=%d" % after["i"])
    check("分數沒歸零", after["t"] == before["t"] == 1, "total=%d" % after["t"])

    print("\n[7] 按「重新開始」才依新設定重出")
    pg.click("#cfgBtn")
    pg.click("#cfgReset")                     # 第一下：待確認
    pg.click("#cfgReset")                     # 第二下：真的重來
    pg.wait_for_selector("#qbox .prompt")
    check("回到第 1 題", pg.evaluate("() => S.idx") == 0)
    check("新一輪是打散的", not asc(pg.evaluate(NUMS)))

    print("\n[8] 模擬考：設定依題號也照樣隨機")
    pg.evaluate("() => setOrder('seq')")
    pg.click("#examBtn")
    pg.wait_for_selector("#qbox .prompt")
    ex = pg.evaluate(NUMS)
    # 模擬考抽 EXAM_N 題，但題庫還沒收滿 EXAM_N 題時就只能抽到題庫的全部。
    # 別寫死題數，否則收錄過程中這一項會一直是紅的。
    want = min(pg.evaluate("() => EXAM_N"), pg.evaluate("() => BANK.length"))
    check("抽 %d 題" % want, len(ex) == want, "n=%d" % len(ex))
    check("不是照題號排的", not asc(ex), "%s ..." % ex[:6])

    print("\n[9] console")
    check("沒有 JS 錯誤", not errors, "; ".join(errors[:3]))

    b.close()

bad = results.count(False)
print("\n%d 項檢查，%d 失敗" % (len(results), bad))
raise SystemExit(1 if bad else 0)
