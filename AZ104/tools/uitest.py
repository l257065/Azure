# -*- coding: utf-8 -*-
"""在真的瀏覽器裡開 az104-practice.html，逐一操作三種原廠題型並確認批改結果。
用法： python tools/uitest.py
"""
import os, sys, json, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
URL = (ROOT / "az104-practice.html").as_uri()
SHOT = ROOT / "shots"
SHOT.mkdir(exist_ok=True)

# 直接把某一題塞進當前這一輪，避免靠亂數等到想要的題型
FORCE = """
(kind) => {
  setSource('doc');
  const q = BANK_DOC.find(x => (x.k || 'mc') === kind);
  if (!q) return null;
  S.exam = false; S.tab = 0;
  S.pool = [q]; S.idx = 0; S.right = 0; S.total = 0; S.answers = []; S.graded = false;
  report.classList.remove('show');
  renderQ();
  return {n: q.n, k: kind, a: q.a};
}
"""

results = []
def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))
    print(("  PASS  " if cond else "  FAIL  ") + name + ("  " + detail if detail else ""))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 900, "height": 1200})
    errors = []
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.on("console", lambda m: errors.append("console." + m.type + ": " + m.text)
          if m.type == "error" else None)
    pg.goto(URL)
    pg.wait_for_selector("#qbox")

    # 這一支從頭到尾都在操作原廠題型與複選題，題庫 B 還沒有這些題型的時候
    # 一格都跑不動。缺什麼就講清楚缺什麼再結束，不要讓它撞成 TypeError
    # ——收錄到第一題 hs / dd / dl 與第一題複選之後就會自己開始跑。
    have = pg.evaluate("""() => {
      const kinds = new Set(BANK_DOC.map(q => q.k || 'mc'));
      return {kinds:[...kinds], total:BANK_DOC.length,
              multi:BANK_DOC.some(q => (q.k||'mc') === 'mc' && q.a.length > 1)};
    }""")
    missing = [k for k in ("hs", "dd", "dl") if k not in have["kinds"]]
    if not have["multi"]:
        missing.append("複選（a 有兩個以上）")
    if missing:
        print("SKIP：題庫 B 目前 %d 題，題型只有 %s。"
              % (have["total"], "、".join(have["kinds"]) or "無"))
        print("      這支測試要有 %s 才跑得動，收錄到那些題型之後再跑。"
              % "、".join(missing))
        b.close()
        sys.exit(0)

    # ---------- 1. HOTSPOT 是非表 ----------
    print("\n[1] HOTSPOT 是非表 hs")
    info = pg.evaluate(FORCE, "hs")
    print("  題號 #%s  正解 %s" % (info["n"], info["a"]))
    rows = pg.query_selector_all(".hs .hrow")
    check("畫出是非表列數 == 敘述數", len(rows) == len(info["a"]), "rows=%d" % len(rows))
    check("每列都有「是 / 否」兩顆按鈕",
          all(len(r.query_selector_all(".yn button")) == 2 for r in rows))
    # 故意第一句答錯，其餘答對
    for i, r in enumerate(rows):
        want = info["a"][i] if i else (1 - info["a"][i])
        r.query_selector('.yn button[data-v="%d"]' % want).click()
    pg.click("#btnCheck")
    pg.wait_for_selector(".verdict.show")
    v = pg.inner_text("#verdict")
    check("答錯一格 → 判定為答錯", "答錯" in v, v.split("　")[0])
    check("答錯的那一列標紅", "bad" in (rows[0].get_attribute("class") or ""))
    check("答對的那一列標綠", "ok" in (rows[1].get_attribute("class") or ""))
    check("批改後鎖住不能再改", rows[0].query_selector(".yn button").is_disabled())
    pg.screenshot(path=str(SHOT / "hs.png"), full_page=True)

    # 全部答對
    pg.evaluate(FORCE, "hs")
    rows = pg.query_selector_all(".hs .hrow")
    for i, r in enumerate(rows):
        r.query_selector('.yn button[data-v="%d"]' % info["a"][i]).click()
    pg.click("#btnCheck")
    check("全部答對 → 判定為答對", "答對" in pg.inner_text("#verdict"))

    # ---------- 2. DRAG DROP 配對 ----------
    print("\n[2] DRAG DROP 配對 dd")
    info = pg.evaluate(FORCE, "dd")
    print("  題號 #%s  正解 %s" % (info["n"], info["a"]))
    chips = pg.query_selector_all(".dd .chip")
    slots = pg.query_selector_all(".dd .slot")
    check("項目欄與答案區都畫出來", len(chips) > 0 and len(slots) == len(info["a"]),
          "chips=%d slots=%d" % (len(chips), len(slots)))
    check("未作答時空格顯示提示字", "拖曳到這裡" in slots[0].inner_text())
    # 點選項目 → 點空格（觸控式操作路徑）
    for i, slot in enumerate(slots):
        chips[info["a"][i]].click()
        slot.click()
    filled = [s.inner_text().strip() for s in pg.query_selector_all(".dd .slot")]
    check("點選後每一格都填上了", all(t and "拖曳" not in t for t in filled), " / ".join(filled)[:70])
    pg.click("#btnCheck")
    pg.wait_for_selector(".verdict.show")
    check("全部配對正確 → 判定為答對", "答對" in pg.inner_text("#verdict"))
    check("每一列都標綠", all("ok" in (r.get_attribute("class") or "")
                             for r in pg.query_selector_all(".dd .drow")))
    pg.screenshot(path=str(SHOT / "dd.png"), full_page=True)

    # 故意放錯一格，確認會標紅並顯示正解
    if len(chips) > 1:
        pg.evaluate(FORCE, "dd")
        chips = pg.query_selector_all(".dd .chip")
        slots = pg.query_selector_all(".dd .slot")
        wrong = (info["a"][0] + 1) % len(chips)
        for i, slot in enumerate(slots):
            idx = wrong if i == 0 else info["a"][i]
            chips[idx].click(); slot.click()
        pg.click("#btnCheck")
        row0 = pg.query_selector_all(".dd .drow")[0]
        check("配對錯的那一列標紅", "bad" in (row0.get_attribute("class") or ""))
        check("配對錯時顯示正解", row0.query_selector(".fix") is not None,
              (row0.query_selector(".fix").inner_text() if row0.query_selector(".fix") else ""))

    # ---------- 3. HOTSPOT 下拉 ----------
    print("\n[3] HOTSPOT 下拉 dl")
    info = pg.evaluate("""
      () => { setSource('doc');
        const q = BANK_DOC.find(x => x.k === 'dl' && x.dd.length > 1);
        S.exam=false; S.tab=0; S.pool=[q]; S.idx=0; S.right=0; S.total=0; S.answers=[]; S.graded=false;
        report.classList.remove('show'); renderQ();
        return {n:q.n, a:q.a}; }
    """)
    print("  題號 #%s  正解 %s（多格）" % (info["n"], info["a"]))
    sels = pg.query_selector_all(".dl select")
    check("下拉數量 == 挖空數", len(sels) == len(info["a"]), "selects=%d" % len(sels))
    check("預設是未選擇狀態", all(s.input_value() == "" for s in sels))
    pg.click("#btnCheck")
    check("沒填完就批改 → 擋下來並提示", "還有空格" in pg.inner_text("#verdict") or
                                          "還沒有作答" in pg.inner_text("#verdict"),
          pg.inner_text("#verdict")[:34])
    for g, s in enumerate(sels):
        s.select_option(str(info["a"][g]))
    pg.click("#btnCheck")
    pg.wait_for_selector(".verdict.show")
    check("全部選對 → 判定為答對", "答對" in pg.inner_text("#verdict"))
    check("每個下拉都標綠", all("ok" in (s.get_attribute("class") or "")
                                for s in pg.query_selector_all(".dl select")))
    pg.screenshot(path=str(SHOT / "dl.png"), full_page=True)

    # ---------- 4. 切換語言不會弄丟作答 ----------
    print("\n[4] 切換語言")
    pg.evaluate(FORCE, "hs")
    rows = pg.query_selector_all(".hs .hrow")
    rows[0].query_selector('.yn button[data-v="1"]').click()
    pg.click('#langSeg button[data-lang="en"]')
    pressed = pg.eval_on_selector_all(
        '.hs .hrow:first-child .yn button',
        "els => els.map(e => e.getAttribute('aria-pressed'))")
    check("切成英文後仍保留原本的作答", pressed[0] == "true", str(pressed))
    check("英文介面的按鈕文字是 Yes / No",
          pg.inner_text(".hs .hrow:first-child .yn button") == "Yes")
    pg.click('#langSeg button[data-lang="zh"]')

    # ---------- 4b. 模擬考回頭改答案，先前作答要還原 ----------
    print("\n[4b] 模擬考上一題／下一題")
    pg.evaluate("""
      () => { setSource('doc');
        const pick = k => BANK_DOC.find(x => (x.k||'mc') === k);
        S.exam = true; S.pool = ['hs','dd','dl'].map(pick);
        S.idx = 0; S.answers = []; S.right = 0; S.total = 0; S.graded = false;
        report.classList.remove('show'); renderQ(); }
    """)
    # 第 1 題（hs）作答：多格題型要整題填完才換得了題，先確認沒填完真的走不掉
    hrows = pg.query_selector_all(".hs .hrow")
    if len(hrows) > 1:
        hrows[0].query_selector('.yn button[data-v="1"]').click()
        pg.click("#btnCheck")                   # 只填一列就想跳題
        check("模擬考多格題型沒填完就按下一題 → 擋在原地",
              pg.evaluate("() => S.idx") == 0 and "還有空格" in pg.inner_text("#verdict"),
              pg.inner_text("#verdict")[:34])
    # 每一列都選滿，才換得了題
    for r in pg.query_selector_all(".hs .hrow"):
        r.query_selector('.yn button[data-v="1"]').click()
    pg.click("#btnCheck")                       # 模擬考的「下一題」
    pg.wait_for_selector(".dd .slot")
    # 第 2 題（dd）作答：一樣要整題填完
    chips = pg.query_selector_all(".dd .chip")
    slots = pg.query_selector_all(".dd .slot")
    for i, slot in enumerate(slots):
        chips[i % len(chips)].click(); slot.click()
    first_slot = slots[0].inner_text().strip()
    pg.click("#btnPrev")                        # 回上一題
    pg.wait_for_selector(".hs .hrow")
    back = pg.eval_on_selector_all('.hs .hrow:first-child .yn button',
                                   "els => els.map(e => e.getAttribute('aria-pressed'))")
    check("回上一題後，是非表的作答還在", back and back[0] == "true", str(back))
    pg.click("#btnCheck")                       # 再往下一題
    pg.wait_for_selector(".dd .slot")
    again = pg.query_selector_all(".dd .slot")[0].inner_text().strip()
    check("再回來後，配對題放好的項目還在", again == first_slot, again[:40])

    # ---------- 4c. 練習模式翻回上一題，作答與批改結果要還原 ----------
    print("\n[4c] 練習模式上一題")
    pg.evaluate("""
      () => { setSource('doc');
        const pick = k => BANK_DOC.find(x => (x.k||'mc') === k);
        S.exam = false; S.tab = 0; S.pool = [pick('dd'), pick('dl')];
        S.idx = 0; S.answers = []; S.gr = []; S.right = 0; S.total = 0; S.graded = false;
        report.classList.remove('show'); renderQ(); }
    """)
    chips = pg.query_selector_all(".dd .chip")
    slots = pg.query_selector_all(".dd .slot")
    for i, slot in enumerate(slots):
        chips[i % len(chips)].click(); slot.click()
    placed = [s.inner_text().strip() for s in pg.query_selector_all(".dd .slot")]
    pg.click("#btnCheck")                       # 批改
    pg.wait_for_selector(".verdict.show")
    verdict_was = pg.inner_text("#verdict")
    pg.click("#btnCheck")                       # 批改後變成「下一題」
    pg.wait_for_selector(".dl select")
    pg.click("#btnPrev")                        # 翻回上一題
    pg.wait_for_selector(".dd .slot")
    again = [s.inner_text().strip() for s in pg.query_selector_all(".dd .slot")]
    check("翻回上一題，配對題的作答還原", again == placed, " / ".join(again)[:60])
    check("翻回上一題，批改結果也還原",
          pg.inner_text("#verdict")[:12] == verdict_was[:12], pg.inner_text("#verdict")[:30])
    check("還原後不能再改答案",
          pg.query_selector(".dd .chip").is_disabled())

    # ---------- 4d. 答案區順序固定的題目（#227）----------
    print("\n[4d] #227 答案區順序固定")
    order = []
    for _ in range(6):
        pg.evaluate("""
          () => { setSource('doc');
            const q = BANK_DOC.find(x => String(x.n) === '227');
            BANK_DOC.forEach(permuteOptions);
            S.exam=false; S.tab=0; S.pool=[q]; S.idx=0; S.answers=[]; S.gr=[];
            S.right=0; S.total=0; S.graded=false; report.classList.remove('show'); renderQ(); }
        """)
        order.append([d.inner_text().strip() for d in pg.query_selector_all(".dd .desc")])
    check("重洗多輪後答案區順序不變", all(o == order[0] for o in order), str(order[0])[:60])
    chip_orders = set()
    for _ in range(8):
        pg.evaluate("""
          () => { const q = BANK_DOC.find(x => String(x.n) === '227');
            permuteOptions(q); S.pool=[q]; S.idx=0; S.graded=false; S.answers=[]; renderQ(); }
        """)
        chip_orders.add("|".join(c.inner_text().strip() for c in pg.query_selector_all(".dd .chip")))
    check("可拖曳項目仍然會洗牌", len(chip_orders) > 1, "%d 種排列" % len(chip_orders))

    # ---------- 5. 模擬考交卷與成績單 ----------
    print("\n[5] 模擬考成績單")
    pg.evaluate("""
      () => { setSource('doc');
        const pick = k => BANK_DOC.find(x => (x.k||'mc') === k);
        S.exam = true; S.pool = ['hs','dd','dl','mc'].map(pick).filter(Boolean);
        S.idx = 0; S.answers = []; S.right = 0; S.total = 0;
        // 每一題都填正解
        S.pool.forEach((q,i) => { S.answers[i] = q.a.slice(); });
        finishRound(); }
    """)
    pg.wait_for_selector(".report.show")
    pct = pg.inner_text(".bigscore .pct")
    check("四種題型全對 → 成績 100%", pct.strip() == "100%", pct)
    check("成績單逐題檢討有列出每一格", len(pg.query_selector_all(".rev .rh")) > 0,
          "rh=%d" % len(pg.query_selector_all(".rev .rh")))
    pg.screenshot(path=str(SHOT / "report.png"), full_page=True)

    # ---------- 6. 複選題「需選 N 項」的硬性規則 ----------
    print("\n[6] 複選題需選 N 項")
    FORCE_MULTI = """
    (exam) => {
      setSource('doc');
      const q = BANK_DOC.find(x => (x.k || 'mc') === 'mc' && x.a.length === 2 && x.o.length > 2);
      if (!q) return null;
      S.exam = exam; S.tab = 0; S.lang = 'zh';
      S.pool = [q]; S.idx = 0; S.right = 0; S.total = 0;
      S.answers = []; S.gr = []; S.flags = []; S.notes = []; S.graded = false;
      report.classList.remove('show'); applyLang(); renderQ();
      return {n: q.n, a: q.a, o: q.o.length};
    }
    """
    info = pg.evaluate(FORCE_MULTI, False)
    print("  題號 #%s  正解 %s  共 %d 個選項" % (info["n"], info["a"], info["o"]))
    badge = lambda: pg.inner_text(".prompt .multi")
    bclass = lambda: pg.get_attribute(".prompt .multi", "class")
    check("徽章顯示需選幾項與已選幾項", badge() == "需選 2 項 · 已選 0", badge())

    opts = pg.query_selector_all(".opts .opt")
    opts[info["a"][0]].click()
    check("選一項後徽章跟著更新", badge() == "需選 2 項 · 已選 1", badge())
    check("只選一項時徽章還不是完成色", "done" not in (bclass() or ""), bclass())
    pg.click("#btnCheck")
    check("只選一項就批改 → 擋下來並說還差幾項",
          "再選 1 項" in pg.inner_text("#verdict"), pg.inner_text("#verdict")[:40])
    check("被擋下來時不算分", pg.inner_text("#score").strip() == "0 / 0", pg.inner_text("#score"))

    opts[info["a"][1]].click()
    check("選滿兩項後徽章轉成完成色", "done" in (bclass() or ""), badge())
    check("補齊後剛才的提醒收掉", "show" not in (pg.get_attribute("#verdict", "class") or ""))

    # 想選第三項：擋下來，選的還是原本那兩項
    third = next(i for i in range(info["o"]) if i not in info["a"])
    opts[third].click()
    picked = pg.eval_on_selector_all(".opts .opt",
             "els => els.map((e,i) => e.getAttribute('aria-pressed') === 'true' ? i : -1).filter(i => i >= 0)")
    check("選滿之後不吃第三項", picked == info["a"], str(picked))
    check("擋第三項時徽章閃紅並說明", "warn" in (bclass() or "") and "先取消" in badge(), badge())

    pg.click("#btnCheck")
    pg.wait_for_selector(".verdict.show")
    check("選滿兩項就能批改（兩項全中→答對）", "答對" in pg.inner_text("#verdict"),
          pg.inner_text("#verdict")[:30])
    pg.screenshot(path=str(SHOT / "multi.png"), full_page=True)

    # 模擬考：沒選滿不能按「下一題」
    pg.evaluate("""
      () => { setSource('doc');
        const two = BANK_DOC.filter(x => (x.k||'mc') === 'mc' && x.a.length === 2 && x.o.length > 2);
        S.exam = true; S.tab = 0; S.lang = 'zh'; S.pool = two.slice(0, 2);
        S.idx = 0; S.answers = []; S.gr = []; S.flags = []; S.notes = [];
        S.right = 0; S.total = 0; S.graded = false;
        report.classList.remove('show'); applyLang(); renderQ(); }
    """)
    pg.click("#btnCheck")                       # 一項都沒選就想往下一題
    # 一項都沒選＝整題空白，提示走「你還沒作答」那條；「再選 N 項」是留給選一半的
    check("模擬考沒作答就按下一題 → 擋在原地",
          pg.evaluate("() => S.idx") == 0 and "還沒作答" in pg.inner_text("#verdict"),
          pg.inner_text("#verdict")[:40])
    check("沒作答時徽章仍標示需選幾項", pg.inner_text(".prompt .multi") == "需選 2 項 · 已選 0",
          pg.inner_text(".prompt .multi"))
    pg.query_selector_all(".opts .opt")[0].click()
    pg.click("#btnCheck")
    check("模擬考只選一項也擋住", pg.evaluate("() => S.idx") == 0, "idx=%d" % pg.evaluate("() => S.idx"))
    check("只選一半不列入「已作答」", "已作答 0 /" in pg.inner_text("#score"), pg.inner_text("#score"))
    pg.query_selector_all(".opts .opt")[1].click()
    check("只選一半在總覽算未作答",
          pg.evaluate("() => { const q=S.pool[0]; return ansDone(q,[0]) === false && ansDone(q,[0,1]) === true; }"))
    pg.click("#btnCheck")
    check("選滿兩項就放行到下一題", pg.evaluate("() => S.idx") == 1, "idx=%d" % pg.evaluate("() => S.idx"))
    pg.keyboard.press("ArrowRight")             # 最後一題，本來就不該動
    pg.evaluate("() => { S.idx = 0; renderQ(); }")
    pg.keyboard.press("ArrowRight")             # 已作答的題目：方向鍵放行
    check("方向鍵對選滿的題目照樣放行", pg.evaluate("() => S.idx") == 1, "idx=%d" % pg.evaluate("() => S.idx"))
    pg.evaluate("() => { S.idx = 0; S.answers[0] = [0]; renderQ(); }")
    pg.keyboard.press("ArrowRight")
    check("方向鍵對沒選滿的題目也擋住", pg.evaluate("() => S.idx") == 0, "idx=%d" % pg.evaluate("() => S.idx"))

    # 單選題不受影響
    pg.evaluate("""
      () => { setSource('doc');
        const q = BANK_DOC.find(x => (x.k||'mc') === 'mc' && x.a.length === 1);
        S.exam = false; S.tab = 0; S.pool = [q]; S.idx = 0; S.answers = []; S.gr = [];
        S.right = 0; S.total = 0; S.graded = false;
        report.classList.remove('show'); renderQ(); }
    """)
    check("單選題不畫「需選 N 項」徽章", pg.query_selector(".prompt .multi") is None)
    pg.query_selector_all(".opts .opt")[0].click()
    pg.click("#btnCheck")
    pg.wait_for_selector(".verdict.show")
    check("單選題照樣能批改", "正確答案" in pg.inner_text("#verdict"), pg.inner_text("#verdict")[:26])

    check("整段操作沒有 JS 例外", not errors, "; ".join(errors[:3]))
    b.close()

print("\n" + "=" * 46)
ok = sum(1 for _, c, _ in results if c)
print("通過 %d / %d" % (ok, len(results)))
for n, c, d in results:
    if not c:
        print("  FAIL: " + n + "  " + d)
sys.exit(0 if ok == len(results) else 1)
