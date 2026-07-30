# -*- coding: utf-8 -*-
"""驗練習模式的「跳過」：能跳、不計分、不進錯題本、回頭還原，模擬考則照舊擋。
用法： python tools/uitest_skip.py
"""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
URL = (ROOT / "az104-practice.html").as_uri()
SHOT = ROOT / "shots"
SHOT.mkdir(exist_ok=True)

# 固定三題純選擇題的練習輪，避免亂數影響
FORCE3 = """
() => {
  setSource('doc');
  const qs = BANK_DOC.filter(x => (x.k || 'mc') === 'mc').slice(0, 3);
  S.exam = false; S.tab = 0;
  S.pool = qs; S.idx = 0; S.right = 0; S.total = 0;
  S.answers = []; S.gr = []; S.graded = false;
  wrongSet.clear();
  report.classList.remove('show');
  renderQ();
  return qs.length;
}
"""

results = []
def check(name, cond, detail=""):
    results.append(bool(cond))
    print(("  PASS  " if cond else "  FAIL  ") + name + ("  " + detail if detail else ""))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 900, "height": 1100})
    errors = []
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.on("console", lambda m: errors.append("console." + m.type + ": " + m.text)
          if m.type == "error" else None)
    pg.goto(URL)
    pg.wait_for_selector("#qbox")

    print("\n[1] 練習模式：跳過鈕")
    n = pg.evaluate(FORCE3)
    check("湊到三題", n == 3, "n=%d" % n)
    check("第 1 題看得到「跳過」", pg.is_visible("#btnNext"))
    check("按鈕文字是「跳過」", pg.inner_text("#btnNext").strip() == "跳過",
          pg.inner_text("#btnNext").strip())
    check("批改鈕仍在", pg.is_visible("#btnCheck"))
    pg.screenshot(path=str(SHOT / "skip_practice.png"), full_page=True)

    print("\n[2] 沒作答直接跳過")
    pg.click("#btnNext")
    st = pg.evaluate("() => ({i:S.idx, r:S.right, t:S.total, w:wrongSet.size, g:S.gr.filter(Boolean).length})")
    check("跳到第 2 題", st["i"] == 1, "idx=%d" % st["i"])
    check("不計分", st["t"] == 0 and st["r"] == 0, "%d/%d" % (st["r"], st["t"]))
    check("不進錯題本", st["w"] == 0, "wrong=%d" % st["w"])
    check("不留批改紀錄", st["g"] == 0)
    check("沒有跳出「你還沒作答」", "還沒作答" not in pg.inner_text("#verdict"))

    print("\n[3] 選了答案但不批改就跳過 → 回上一題還原")
    pg.click(".opt")
    picked = pg.evaluate("() => S.ans.slice()")
    pg.click("#btnNext")
    check("跳到第 3 題", pg.evaluate("() => S.idx") == 2)
    check("跳過後仍不計分", pg.evaluate("() => S.total") == 0)
    check("最後一題不給跳（跳過鈕收起）", not pg.is_visible("#btnNext"))
    pg.click("#btnPrev")
    check("回到第 2 題", pg.evaluate("() => S.idx") == 1)
    check("剛才選的答案有還原", pg.evaluate("() => S.ans.slice()") == picked,
          str(pg.evaluate("() => S.ans.slice()")))
    check("還原後還沒批改", pg.evaluate("() => S.graded") is False)

    print("\n[4] → 鍵等同跳過")
    pg.evaluate(FORCE3)
    pg.keyboard.press("ArrowRight")
    st = pg.evaluate("() => ({i:S.idx, t:S.total})")
    check("→ 直接跳走", st["i"] == 1, "idx=%d" % st["i"])
    check("→ 也不計分", st["t"] == 0)

    print("\n[5] 批改之後主鈕變「下一題」，跳過收起")
    pg.evaluate(FORCE3)
    need = pg.evaluate("() => S.pool[S.idx].a.length")   # 複選題要選滿才批改得動
    for i in range(need):
        pg.query_selector_all(".opt")[i].click()
    pg.click("#btnCheck")
    check("批改後不再顯示跳過", not pg.is_visible("#btnNext"))
    check("主鈕變「下一題」", pg.inner_text("#btnCheck").strip() == "下一題",
          pg.inner_text("#btnCheck").strip())
    check("有計分", pg.evaluate("() => S.total") == 1)

    print("\n[6] 模擬考：照舊不能空著跳過")
    pg.evaluate("() => { S.exam = false; }")
    pg.click("#examBtn")
    pg.wait_for_selector("#qbox .prompt")
    check("模擬考底部第三顆是「交卷」", pg.inner_text("#btnNext").strip() == "交卷",
          pg.inner_text("#btnNext").strip())
    idx0 = pg.evaluate("() => S.idx")
    pg.click("#btnCheck")           # 考試模式的「下一題」
    check("沒作答被擋住", pg.evaluate("() => S.idx") == idx0)
    check("有提示還沒作答", "還沒作答" in pg.inner_text("#verdict"), pg.inner_text("#verdict")[:24])
    pg.keyboard.press("ArrowRight")
    check("考試的 → 也擋住", pg.evaluate("() => S.idx") == idx0)

    print("\n[7] console")
    check("沒有 JS 錯誤", not errors, "; ".join(errors[:3]))

    b.close()

bad = results.count(False)
print("\n%d 項檢查，%d 失敗" % (len(results), bad))
raise SystemExit(1 if bad else 0)
