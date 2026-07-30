# -*- coding: utf-8 -*-
"""驗證新加的功能：星號題、練習模式回上一題、模擬考標記待複習與交卷前確認。
用法： python tools/check_star_flag.py
"""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
SHOT = ROOT / "shots"; SHOT.mkdir(exist_ok=True)
URL = (ROOT / "az104-practice.html").as_uri()

fails = []

def mc_only(pg):
    """把這一輪過濾成單選題並回到第 1 題。
    複選題有「必須剛好選滿 N 項才能批改」的規則，會讓固定點某一顆的測試步驟卡住，
    這裡先排除掉，讓每個案例驗的是它真正要驗的東西。"""
    pg.evaluate("""
      S.pool = S.pool.filter(q => q.o && (q.a||[]).length === 1 && !q.s && !q.dd && !q.items);
      S.idx = 0; S.answers = []; S.gr = []; S.right = 0; S.total = 0; S.logged = false;
      renderQ();
    """)
    pg.wait_for_selector(".opts .opt")

def answer_next(pg):
    """把目前這題答對、批改，然後前進一題（批改後主鈕就是「下一題」）"""
    pg.wait_for_selector(".opts .opt")
    for k in pg.evaluate("S.pool[S.idx].a"):
        pg.click(".opts .opt >> nth=%d" % k)
    pg.click("#btnCheck")
    pg.click("#btnCheck")

CFG_CLOSED = "!document.getElementById('cfgwrap').classList.contains('show')"

def restart(pg):
    """設定面板裡的「重新開始」，按兩次才算數"""
    pg.click("#cfgBtn"); pg.wait_for_selector("#cfgwrap.show")
    pg.click("#cfgReset"); pg.click("#cfgReset")
    pg.wait_for_function(CFG_CLOSED)

def set_src(pg, src):
    pg.click("#cfgBtn"); pg.wait_for_selector("#cfgwrap.show")
    if pg.evaluate("S.src") == src:
        pg.click("#cfgClose")
    else:
        pg.click("[data-src='%s']" % src)
    pg.wait_for_function(CFG_CLOSED)

def ck(name, cond, extra=""):
    print(("  OK  " if cond else "  FAIL") + "  " + name + (("  " + str(extra)) if extra else ""))
    if not cond: fails.append(name)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(accept_downloads=True, viewport={"width": 430, "height": 900})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.add_init_script("window.addEventListener('error', e => { window.__lastErr = String(e.message) + ' @ ' + e.lineno; });")
    pg.on("console", lambda m: errs.append("console." + m.type + ": " + m.text) if m.type == "error" else None)
    pg.goto(URL)
    pg.wait_for_function("typeof S !== 'undefined' && S.pool.length > 0")

    print("\n=== 1. 練習模式：星號 ===")
    ck("星號鈕存在", not pg.is_hidden("#starBtn"))
    ck("練習模式沒有標記鈕（標記只屬於考試）", pg.locator(".qtools .tbtn.flag").count() == 0)
    ck("練習模式沒有備註框", pg.locator(".qtools .notebox").count() == 0)
    q1 = pg.evaluate("S.pool[0].q")
    pg.click("#starBtn")
    ck("按下後 aria-pressed=true", pg.get_attribute("#starBtn", "aria-pressed") == "true")
    ck("寫進 starSet", pg.evaluate("starSet.has(S.pool[0].q)"))
    ck("寫進 localStorage",
       q1 in pg.evaluate("localStorage.getItem('az104.star.v1')"))
    pg.screenshot(path=str(SHOT / "star_practice.png"))

    # 再星第二題，然後切到星號題分頁（沒有「跳過」了，用跳題直接換一題）
    pg.evaluate("S.idx = 1; renderQ()")
    q2 = pg.evaluate("S.pool[S.idx].q")
    pg.click("#starBtn")
    pg.click("#t5")
    ck("星號題分頁只出兩題", pg.evaluate("S.pool.length") == 2, pg.evaluate("S.pool.length"))
    ck("星號題分頁題目正確",
       sorted(pg.evaluate("S.pool.map(q=>q.q)")) == sorted([q1, q2]))
    ck("分頁標題是星號題", "星號題" in pg.inner_text("#t5"))

    # 取消星號
    pg.click("#starBtn")
    ck("取消後 starSet 剩一題", pg.evaluate("starSet.size") == 1)
    pg.click("#t0")

    print("\n=== 2. 練習模式：回到上一題 ===")
    pg.evaluate("S.tab=0; startRound(true)")
    mc_only(pg)
    ck("第一題時上一題是灰的", pg.is_disabled("#btnPrev"))
    # 第一題選 A 並批改
    first_q = pg.evaluate("S.pool[0].q")
    pg.click(".opts .opt >> nth=0")
    pg.click("#btnCheck")
    graded_verdict = pg.inner_text("#verdict")
    ck("批改後有判定", "正確答案" in graded_verdict or "答對" in graded_verdict)
    ck("批改後主鈕變下一題", pg.inner_text("#btnCheck").strip() == "下一題")
    tot1 = pg.evaluate("S.total")
    pg.click("#btnCheck")            # 前往第 2 題
    ck("已到第 2 題", pg.evaluate("S.idx") == 1)
    ck("上一題可按", not pg.is_disabled("#btnPrev"))
    pg.click("#btnPrev")
    ck("回到第 1 題", pg.evaluate("S.idx") == 0)
    ck("回來還是同一題", pg.evaluate("S.pool[0].q") == first_q)
    ck("先前選的答案有還原", pg.evaluate("S.ans.length") == 1 and pg.evaluate("S.ans[0]") == 0)
    ck("選項高亮有還原", pg.get_attribute(".opts .opt >> nth=0", "aria-pressed") == "true")
    ck("判定與解析有還原", pg.inner_text("#verdict") == graded_verdict)
    ck("解析有顯示", "expl show" in pg.get_attribute("#expl", "class"))
    ck("沒有重複計分", pg.evaluate("S.total") == tot1, pg.evaluate("S.total"))
    ck("已批改的題目不能再改答案", pg.is_disabled(".opts .opt >> nth=1"))
    ck("已批改時看答案鈕收起來", pg.is_hidden("#btnReveal"))
    pg.screenshot(path=str(SHOT / "practice_back.png"))
    # 鍵盤翻題
    pg.keyboard.press("ArrowRight")
    ck("→ 前往下一題", pg.evaluate("S.idx") == 1)
    pg.keyboard.press("ArrowLeft")
    ck("← 回上一題", pg.evaluate("S.idx") == 0)

    print("\n=== 2b. 原廠規則：不給空著跳過 ===")
    pg.evaluate("S.tab=0; startRound(true)")
    mc_only(pg)
    ck("作答中沒有「跳過」按鈕", pg.is_hidden("#btnNext"))
    ck("作答中看得到批改與看答案",
       not pg.is_hidden("#btnCheck") and not pg.is_hidden("#btnReveal"))
    pg.keyboard.press("ArrowRight")
    ck("沒作答按 → 不會前進", pg.evaluate("S.idx") == 0)
    ck("沒作答按 → 會出現提醒", "還沒作答" in pg.inner_text("#verdict"), pg.inner_text("#verdict"))
    ck("被擋下來時不會計分", pg.evaluate("S.total") == 0)
    pg.click(".opts .opt >> nth=0")
    pg.keyboard.press("ArrowRight")
    ck("選好後按 → 會先幫你批改", pg.evaluate("S.graded") is True)
    ck("先批改的那一下還不會跳題", pg.evaluate("S.idx") == 0)
    ck("批改後主鈕才變「下一題」", pg.inner_text("#btnCheck").strip() == "下一題")
    pg.keyboard.press("ArrowRight")
    ck("批改完按 → 才前進", pg.evaluate("S.idx") == 1)
    pg.click("#btnPrev")
    ck("批改過的題目往回翻不會被擋", pg.evaluate("S.idx") == 0)

    print("\n=== 3. 模擬考：標記待複習 + 備註 ===")
    pg.click("#examBtn")
    pg.wait_for_function("S.exam === true && S.pool.length > 1")
    ck("抽 40 題", pg.evaluate("S.pool.length") == 40, pg.evaluate("S.pool.length"))
    ck("計時器有出現", not pg.is_hidden("#timer"))
    ck("考試中有標記鈕", pg.locator(".qtools .tbtn.flag").count() == 1)
    ck("考試中沒有星號鈕（星號只屬於練習）", pg.is_hidden("#starBtn"))
    ck("考試中也有上一題鈕", not pg.is_hidden("#btnPrev"))
    ck("未標記時備註框是收起來的", pg.is_hidden(".qtools .notebox"))
    pg.click(".qtools .tbtn.flag")
    ck("標記後備註框展開", pg.is_visible(".qtools .notebox"))
    pg.fill(".qtools .notebox", "在 B 跟 D 之間猶豫")
    ck("備註存進 S.notes", pg.evaluate("S.notes[0]") == "在 B 跟 D 之間猶豫")
    pg.screenshot(path=str(SHOT / "exam_flag.png"))

    # 第一題作答、第二題留白也標記、第三題作答
    pg.evaluate("S.idx=0; renderQ()")
    if pg.locator(".opts .opt").count():
        pg.click(".opts .opt >> nth=0")
    pg.click("#btnCheck")                       # 到第 2 題
    pg.click(".qtools .tbtn.flag")              # 第 2 題標記但不作答
    ck("第 2 題標記獨立", pg.evaluate("!!S.flags[1] && !!S.flags[0]"))
    ck("第 2 題備註是空的", pg.evaluate("S.notes[1] || ''") == "")
    pg.click("#btnPrev")
    ck("模擬考也能回上一題", pg.evaluate("S.idx") == 0)
    ck("回來時標記狀態正確", pg.get_attribute(".qtools .tbtn.flag", "aria-pressed") == "true")
    ck("回來時備註文字還在", pg.input_value(".qtools .notebox") == "在 B 跟 D 之間猶豫")
    ck("回來時作答有還原", pg.evaluate("S.ans.length > 0"))

    print("\n=== 3b. 模擬考：沒作答不給按下一題 ===")
    pg.evaluate("S.idx = 3; S.answers[3] = undefined; renderQ()")
    pg.click("#btnCheck")                       # 下一題
    ck("考試中沒作答不給前進", pg.evaluate("S.idx") == 3)
    ck("考試中會提示還沒作答", "還沒作答" in pg.inner_text("#verdict"), pg.inner_text("#verdict"))
    ck("提示有告訴你可以從總覽跳走", "作答總覽" in pg.inner_text("#verdict"))
    pg.click("#btnPrev")
    ck("但「上一題」不受限制", pg.evaluate("S.idx") == 2)
    pg.click("#btnReveal")
    ck("「作答總覽」也不受限制", pg.is_visible("#ovwrap"))
    pg.click(".ovbtns [data-act='back']")
    pg.evaluate("S.idx = 0; renderQ()")

    print("\n=== 4. 交卷前的作答總覽 ===")
    pg.click("#btnNext")                        # 交卷
    ck("跳出總覽而不是直接給分", pg.is_visible("#ovwrap"))
    ck("此時還沒有成績單", not pg.evaluate("report.classList.contains('show')"))
    ck("標題是確認交卷", "確定要交卷嗎" in pg.inner_text(".ovcard h2"))
    ck("總覽有 40 格", pg.locator(".ovcell").count() == 40, pg.locator(".ovcell").count())
    ck("已作答的格子標 done", pg.locator(".ovcell.done").count() >= 1)
    ck("未作答的格子標 blank", pg.locator(".ovcell.blank").count() >= 38)
    ck("標記的格子標 flag", pg.locator(".ovcell.flag").count() == 2, pg.locator(".ovcell.flag").count())
    ck("標記清單列出備註", "在 B 跟 D 之間猶豫" in pg.inner_text(".ovnotes"))
    ck("沒寫備註的顯示佔位字", "（沒有備註）" in pg.inner_text(".ovnotes"))
    pg.screenshot(path=str(SHOT / "exam_overview.png"))

    # 返回作答
    pg.click(".ovbtns [data-act='back']")
    ck("返回作答會關掉總覽", pg.is_hidden("#ovwrap"))
    ck("返回後考試還在進行", pg.evaluate("S.exam === true && !report.classList.contains('show')"))

    # 從總覽跳題
    pg.click("#btnReveal")                      # 作答總覽
    ck("作答總覽鈕也能開", pg.is_visible("#ovwrap"))
    ck("非交卷時標題是作答總覽", pg.inner_text(".ovcard h2").strip() == "作答總覽")
    pg.click(".ovcell >> nth=11")
    ck("點題號跳到第 12 題", pg.evaluate("S.idx") == 11)
    ck("跳題後總覽關閉", pg.is_hidden("#ovwrap"))

    # 從標記清單跳題
    pg.click("#btnNext")
    pg.click(".ovnote >> nth=1")
    ck("點標記清單跳到第 2 題", pg.evaluate("S.idx") == 1)

    print("\n=== 5. 確定交卷才給分 ===")
    pg.click("#btnNext")
    pg.click(".ovbtns [data-act='submit']")
    ck("確定交卷後出現成績單", pg.evaluate("report.classList.contains('show')"))
    ck("成績單標題是模擬考", "模擬考" in pg.inner_text("#eyebrow"))
    ck("逐題檢討有 40 題", pg.locator(".rev .item").count() == 40, pg.locator(".rev .item").count())
    ck("檢討帶出標記與備註",
       pg.locator(".rev .flagln").count() == 2 and "在 B 跟 D 之間猶豫" in pg.inner_text(".rev"))
    ck("交卷後總覽關閉", pg.is_hidden("#ovwrap"))
    ck("交卷後計時停止", pg.evaluate("S.timerId === null"))
    ck("交卷後上一題收起來", pg.is_hidden("#btnPrev"))
    ck("主鈕變再來一輪", pg.inner_text("#btnCheck").strip() == "再來一輪")
    pg.screenshot(path=str(SHOT / "exam_report_flag.png"), full_page=False)

    print("\n=== 6. 時間到自動交卷 ===")
    pg.click("#btnCheck")                       # 再來一輪（仍在模擬考模式）
    pg.wait_for_function("S.exam === true && S.pool.length === 40")
    pg.evaluate("S.left = 1")
    pg.wait_for_function("report.classList.contains('show')", timeout=5000)
    ck("時間到自動結算", pg.evaluate("report.classList.contains('show')"))

    print("\n=== 7. 英文模式與重新載入 ===")
    pg.click("#examBtn")                        # 離開模擬考
    pg.click("[data-lang='en']")
    ck("EN 分頁名稱", pg.inner_text("#t5").strip().endswith("Starred"))
    ck("EN 星號鈕", "Star" in (pg.get_attribute("#starBtn", "title") or ""))
    ck("EN 上一題鈕", pg.get_attribute("#btnPrev", "aria-label") == "Back")
    pg.click("[data-lang='zh']")

    pg.reload()
    pg.wait_for_function("typeof S !== 'undefined' && S.pool.length > 0")
    ck("重新載入後星號有留著", pg.evaluate("starSet.size") == 1, pg.evaluate("starSet.size"))
    pg.click("#t5")
    ck("重新載入後星號題分頁仍可用", pg.evaluate("S.pool.length") == 1)

    print("\n=== 8. 空的星號題分頁 ===")
    pg.evaluate("starSet.clear(); saveStar(); S.tab=5; startRound(true)")
    ck("清空後顯示提示", "還沒有打星號的題目" in pg.inner_text("#qbox"))

    print("\n=== 9. 分頁進度不會被切分頁洗掉 ===")
    pg.evaluate("Object.keys(SESS).forEach(k=>delete SESS[k]); S.tab=1; startRound(true)")
    pg.click("#t1")
    ck("分頁 01 有題目", pg.evaluate("S.pool.length") > 0)
    n1 = pg.evaluate("S.pool.length")
    # 在 01 作答三題
    for _ in range(3):
        pg.wait_for_selector(".opts .opt, .hs, .dd, .dl")
        if pg.locator(".opts .opt").count():
            for k in pg.evaluate("S.pool[S.idx].a"):   # 複選題要選滿才批得動
                pg.click(".opts .opt >> nth=%d" % k)
            pg.click("#btnCheck")     # 批改
        pg.click("#btnCheck")         # 批改後主鈕就是「下一題」
    idx1  = pg.evaluate("S.idx")
    tot1  = pg.evaluate("S.total")
    right1 = pg.evaluate("S.right")
    q_at_idx = pg.evaluate("S.pool[S.idx].q")
    ck("01 已經做到第 4 題", idx1 == 3, idx1)
    ck("01 有計分", tot1 >= 1, tot1)
    ck("01 分頁出現進度圓點", pg.locator("#t1 .dot").count() == 1)

    # 切到 02 做一題
    pg.click("#t2")
    ck("02 從第 1 題開始", pg.evaluate("S.idx") == 0)
    ck("02 分數是新的", pg.evaluate("S.total") == 0)
    ck("切走後 01 的圓點還在", pg.locator("#t1 .dot").count() == 1)
    if pg.locator(".opts .opt").count():
        pg.click(".opts .opt >> nth=0")
        pg.click("#btnCheck")
    q2_at_idx = pg.evaluate("S.pool[S.idx].q")

    # 切回 01
    pg.click("#t1")
    ck("回到 01 進度沒被洗掉", pg.evaluate("S.idx") == idx1, pg.evaluate("S.idx"))
    ck("回到 01 分數沒被洗掉", pg.evaluate("S.total") == tot1 and pg.evaluate("S.right") == right1)
    ck("回到 01 題目順序沒重洗", pg.evaluate("S.pool[S.idx].q") == q_at_idx)
    ck("回到 01 題數不變", pg.evaluate("S.pool.length") == n1)
    ck("回到 01 已批改的題目翻回去仍有解析",
       (pg.click("#btnPrev") or "expl show" in pg.get_attribute("#expl", "class")))
    pg.click("#btnCheck")             # 回到原本那一題
    ck("進度列顯示正確題號", ("第 %d /" % (idx1 + 1)) in pg.inner_text("#eyebrow"), pg.inner_text("#eyebrow"))

    # 切回 02 檢查它也記得
    pg.click("#t2")
    ck("02 也記得自己的進度", pg.evaluate("S.pool[S.idx].q") == q2_at_idx)
    ck("02 分數是自己的", pg.evaluate("S.total") == 1, pg.evaluate("S.total"))

    print("\n=== 10. 洗牌不會污染其他分頁的作答 ===")
    pg.click("#t1")
    snap = pg.evaluate("S.pool[S.idx].o.slice()")
    ans_snap = pg.evaluate("S.pool[S.idx].a.slice()")
    pg.click("#t3"); pg.click("#t0"); pg.click("#t3")   # 到處切、觸發多次洗牌
    pg.click("#t1")
    ck("01 當前題目的選項順序沒被別的分頁洗掉", pg.evaluate("S.pool[S.idx].o.slice()") == snap)
    ck("01 當前題目的正解索引沒跑掉", pg.evaluate("S.pool[S.idx].a.slice()") == ans_snap)

    print("\n=== 11. 手動歸零與做完自動歸零 ===")
    pg.click("#cfgBtn"); pg.wait_for_selector("#cfgwrap.show")
    ck("設定裡有重新開始鈕", pg.is_visible("#cfgReset"))
    pg.click("#cfgReset")
    ck("按一次只是進入確認狀態", "再按一次" in pg.inner_text("#cfgReset"))
    ck("按一次還沒歸零", pg.evaluate("S.idx") == idx1)
    pg.click("#cfgReset")
    pg.wait_for_function(CFG_CLOSED)
    ck("按第二次才真的歸零", pg.evaluate("S.idx") == 0 and pg.evaluate("S.total") == 0)
    ck("歸零後圓點消失", pg.locator("#t1 .dot").count() == 0)
    ck("歸零後題數不變", pg.evaluate("S.pool.length") == n1)

    # 整輪做完 → 自動歸零
    pg.evaluate("S.idx = S.pool.length - 1; renderQ()")
    ck("做到最後一題時有圓點", pg.locator("#t1 .dot").count() == 1)
    for k in pg.evaluate("S.pool[S.idx].a"):
        pg.click(".opts .opt >> nth=%d" % k)
    pg.click("#btnCheck"); pg.click("#btnCheck")     # 批改 → 下一題（最後一題就結算）
    ck("做完出現成績單", pg.evaluate("report.classList.contains('show')"))
    ck("做完後圓點消失（進度歸零）", pg.locator("#t1 .dot").count() == 0)
    pg.click("#t2"); pg.click("#t1")
    ck("做完再回來是從第 1 題開始", pg.evaluate("S.idx") == 0 and pg.evaluate("S.total") == 0)

    print("\n=== 12. 模擬考不影響練習進度 ===")
    pg.click("#t1")
    pg.wait_for_selector(".opts .opt")
    answer_next(pg)
    keep_idx = pg.evaluate("S.idx"); keep_q = pg.evaluate("S.pool[S.idx].q")
    pg.click("#examBtn")
    pg.wait_for_function("S.exam === true")
    ck("考試中重新開始鈕仍在設定裡", pg.evaluate("!!document.getElementById('cfgReset')"))
    ck("考試中 01 的圓點還在", pg.locator("#t1 .dot").count() == 1)
    pg.click("#examBtn")
    pg.wait_for_function("S.exam === false")
    ck("離開考試回到原本的練習進度", pg.evaluate("S.idx") == keep_idx and pg.evaluate("S.pool[S.idx].q") == keep_q)

    print("\n=== 13. 題庫來源各自記進度 ===")
    ck("切到文件題庫", pg.evaluate("BANK_DOC.length") > 0)
    set_src(pg, "doc")
    ck("文件題庫是新的一輪", pg.evaluate("S.idx") == 0 and pg.evaluate("S.src") == "doc")
    ck("切題庫後圓點跟著換", pg.locator("#t1 .dot").count() == 0)
    set_src(pg, "mine")
    ck("切回自製題庫，進度還在", pg.evaluate("S.idx") == keep_idx and pg.evaluate("S.pool[S.idx].q") == keep_q)
    ck("切回來圓點也回來", pg.locator("#t1 .dot").count() == 1)

    print("\n=== 14. 重新整理後進度還在 ===")
    pg.evaluate("""
      Object.keys(SESS).forEach(k=>delete SESS[k]);
      Object.keys(localStorage).filter(k=>k.startsWith('az104.sess')).forEach(k=>localStorage.removeItem(k));
      S.tab=1; startRound(true);
    """)
    pg.click("#t1")
    mc_only(pg)
    # 作答四題，其中一題只按「看答案」
    for j in range(4):
        pg.wait_for_selector(".opts .opt")
        if j == 2:
            pg.click("#btnReveal")          # 這題只看答案，不算分
        else:
            pg.click(".opts .opt >> nth=1")
            pg.click("#btnCheck")
        pg.click("#btnCheck")               # 批改／看答案之後，主鈕就是「下一題」
    before = pg.evaluate("""({
      idx:S.idx, right:S.right, total:S.total, len:S.pool.length,
      order:S.pool.map(q=>q.q),
      opts:S.pool[0].o.slice(), a:S.pool[0].a.slice(),
      ans:S.answers.map(x=>x?x.slice():null),
      gr:S.gr.map(x=>x?!!x.reveal:null)
    })""")
    ck("有寫進 localStorage",
       pg.evaluate("!!localStorage.getItem('az104.sess.v1|mine|1')"))
    size = pg.evaluate("(localStorage.getItem('az104.sess.v1|mine|1')||'').length")
    print("       進度大小：%.1f KB / %d 題" % (size / 1024.0, before["len"]))

    pg.reload()
    pg.wait_for_function("typeof S !== 'undefined' && S.pool.length > 0")
    ck("重整後自動回到原本的分頁", pg.evaluate("S.tab") == 1, pg.evaluate("S.tab"))
    after = pg.evaluate("""({
      idx:S.idx, right:S.right, total:S.total, len:S.pool.length,
      order:S.pool.map(q=>q.q),
      opts:S.pool[0].o.slice(), a:S.pool[0].a.slice(),
      ans:S.answers.map(x=>x?x.slice():null),
      gr:S.gr.map(x=>x?!!x.reveal:null)
    })""")
    ck("重整後做到第幾題一樣", after["idx"] == before["idx"], (before["idx"], after["idx"]))
    ck("重整後分數一樣", (after["right"], after["total"]) == (before["right"], before["total"]),
       (before["right"], before["total"], after["right"], after["total"]))
    ck("重整後題數一樣", after["len"] == before["len"])
    ck("重整後出題順序一樣", after["order"] == before["order"])
    ck("重整後選項洗牌順序一樣", after["opts"] == before["opts"])
    ck("重整後正解索引一樣", after["a"] == before["a"])
    ck("重整後每題的作答一樣", after["ans"] == before["ans"], (before["ans"][:4], after["ans"][:4]))
    ck("重整後批改狀態一樣（含只看答案的那題）", after["gr"] == before["gr"], (before["gr"][:4], after["gr"][:4]))
    ck("重整後圓點還在", pg.locator("#t1 .dot").count() == 1)
    # 翻回已作答的題目，選項高亮要對得上原本選的那一個
    for _ in range(after["idx"]):
        pg.click("#btnPrev")
    ck("重整後翻回第 1 題", pg.evaluate("S.idx") == 0)
    ck("重整後第 1 題仍標示原本選的 B", pg.get_attribute(".opts .opt >> nth=1", "aria-pressed") == "true")
    ck("重整後第 1 題解析仍在", "expl show" in pg.get_attribute("#expl", "class"))

    print("\n=== 15. 題庫改過就讓舊進度作廢 ===")
    pg.evaluate("""
      const k='az104.sess.v1|mine|1';
      const o=JSON.parse(localStorage.getItem(k)); o.sig='bogus.sig';
      localStorage.setItem(k, JSON.stringify(o));
    """)
    pg.reload()
    pg.wait_for_function("typeof S !== 'undefined' && S.pool.length > 0")
    ck("指紋對不上就丟掉舊進度", pg.evaluate("S.idx") == 0 and pg.evaluate("S.total") == 0)
    ck("壞掉的進度會從 localStorage 清掉",
       not pg.evaluate("!!localStorage.getItem('az104.sess.v1|mine|1')"))
    ck("剛開一輪沒進度時不寫檔",
       not pg.evaluate("!!localStorage.getItem('az104.sess.v1|mine|0')"))
    # 壞掉的 JSON 也不能讓程式掛掉
    pg.evaluate("localStorage.setItem('az104.sess.v1|mine|2', '{壞掉的 json')")
    pg.reload()
    pg.wait_for_function("typeof S !== 'undefined' && S.pool.length > 0")
    ck("壞掉的 JSON 不會讓程式掛掉", pg.evaluate("S.pool.length") > 0)

    print("\n=== 16. 做完 / 重新開始會清掉存檔 ===")
    pg.click("#t1")
    pg.wait_for_selector(".opts .opt")
    answer_next(pg)
    ck("有存檔", pg.evaluate("!!localStorage.getItem('az104.sess.v1|mine|1')"))
    restart(pg)
    ck("重新開始後存檔清空",
       not pg.evaluate("!!localStorage.getItem('az104.sess.v1|mine|1')"))
    pg.evaluate("S.idx = S.pool.length - 1; renderQ()")
    ck("重新開始後又有存檔", pg.evaluate("!!localStorage.getItem('az104.sess.v1|mine|1')"))
    pg.evaluate("S.idx = S.pool.length; finishRound()")     # 直接結算最後一輪
    ck("整輪做完後存檔清空",
       not pg.evaluate("!!localStorage.getItem('az104.sess.v1|mine|1')"))

    print("\n=== 17. 統計：常錯題與領域答對率 ===")
    pg.evaluate("""
      ['mine','doc'].forEach(k=>{ QSTAT[k]={}; HIST[k]=[]; });
      qstat = QSTAT.mine; hist = HIST.mine; saveQstat(); saveHist();
      Object.keys(SESS).forEach(k=>delete SESS[k]);
      Object.keys(localStorage).filter(k=>k.startsWith('az104.sess')).forEach(k=>localStorage.removeItem(k));
      starSet.clear(); saveStar();
      S.tab=1; startRound(true);
    """)
    pg.click("#t1")
    mc_only(pg)
    # 第 1 題故意答錯兩次（做完一輪、重來一輪再錯一次），第 2 題答對
    wrong_q = pg.evaluate("S.pool[0].q")
    wrong_pick = pg.evaluate("S.pool[0].a.includes(0) ? 1 : 0")   # 挑一個一定錯的選項
    pg.click(".opts .opt >> nth=%d" % wrong_pick)
    pg.click("#btnCheck")
    ck("答錯有記進 qstat", pg.evaluate("qstat[%r] && qstat[%r].n === 1 && qstat[%r].w === 1"
                                       % (wrong_q, wrong_q, wrong_q)))
    ck("qstat 有寫進 localStorage", pg.evaluate("!!localStorage.getItem('az104.qstat.v1')"))
    pg.click("#btnCheck")            # 下一題
    right_pick = pg.evaluate("S.pool[1].a[0]")
    pg.click(".opts .opt >> nth=%d" % right_pick)
    pg.click("#btnCheck")
    ck("答對也記一次", pg.evaluate("qstat[S.pool[1].q].n === 1 && qstat[S.pool[1].q].w === 0"))
    ck("最近紀錄字串有累積", pg.evaluate("qstat[S.pool[1].q].l") == "1")
    pg.click("#btnCheck")
    pg.click("#btnReveal")           # 第 3 題直接看答案 → 也算錯
    ck("直接看答案算一次不會", pg.evaluate("qstat[S.pool[2].q].w === 1 && qstat[S.pool[2].q].v === 1"))

    pg.click("#statBtn")
    ck("統計面板打得開", pg.is_visible("#statwrap"))
    ck("有三條領域長條", pg.locator("#statwrap .dbar").count() == 3)
    ck("領域 01 有算出百分比", "%" in pg.inner_text("#statwrap .dbar >> nth=0"))
    ck("常錯題列出剛剛錯的兩題", pg.locator("#statwrap .wq").count() == 2,
       pg.locator("#statwrap .wq").count())
    ck("常錯題顯示做幾次錯幾次", "做 1 次錯 1 次" in pg.inner_text("#statwrap"))
    ck("本輪進度有顯示", "這一輪" in pg.inner_text("#statwrap .stnow"))
    pg.screenshot(path=str(SHOT / "stats.png"), full_page=True)

    # 點常錯題打星號
    ck("常錯題預設沒星號", pg.get_attribute("#statwrap .wq >> nth=0", "aria-pressed") == "false")
    pg.click("#statwrap .wq >> nth=0")
    ck("點一下就打星號", pg.get_attribute("#statwrap .wq >> nth=0", "aria-pressed") == "true")
    ck("星號真的進了 starSet", pg.evaluate("starSet.size") == 1)
    pg.click("#statwrap [data-act='close']")
    ck("關閉統計面板", pg.is_hidden("#statwrap"))

    print("\n=== 18. 歷次成績：每一輪各自一筆 ===")
    ck("還沒封存任何一輪", pg.evaluate("hist.length") == 0, pg.evaluate("hist.length"))
    restart(pg)   # 手動歸零 → 封存這一輪
    ck("重新開始會封存一筆", pg.evaluate("hist.length") == 1, pg.evaluate("hist.length"))
    ck("那一筆是練習、算 2 題（看答案的不算）",
       pg.evaluate("hist[0].k === 'practice' && hist[0].t === 2 && hist[0].r === 1"),
       pg.evaluate("JSON.stringify(hist[0])"))
    ck("那一筆有三領域細項", pg.evaluate("!!hist[0].d && hist[0].d['1'][1] === 2"))
    ck("歷次成績有寫進 localStorage", pg.evaluate("!!localStorage.getItem('az104.hist.v1')"))

    # 第二輪：兩題全部答對 → 應該看得出進步
    pg.wait_for_selector(".opts .opt")
    for _ in range(2):
        for k in pg.evaluate("S.pool[S.idx].a"):        # 複選題要把正解全點滿
            pg.click(".opts .opt >> nth=%d" % k)
        pg.click("#btnCheck"); pg.click("#btnCheck")
    restart(pg)
    ck("第二輪也各自一筆", pg.evaluate("hist.length") == 2, pg.evaluate("hist.length"))
    ck("兩輪分數各自獨立（新的在上面）",
       pg.evaluate("hist[0].r === 2 && hist[0].t === 2 && hist[1].r === 1 && hist[1].t === 2"),
       pg.evaluate("JSON.stringify(hist.map(h=>[h.r,h.t]))"))
    pg.click("#statBtn")
    ck("歷次成績列出兩筆", pg.locator("#statwrap .hrow2").count() == 2)
    ck("有標出進步（▲ 50%→100%）", "▲" in pg.inner_text("#statwrap"),
       pg.inner_text("#statwrap .hrow2 >> nth=0"))
    pg.screenshot(path=str(SHOT / "stats_hist.png"), full_page=True)
    pg.click("#statwrap [data-act='close']")

    # 同一題重複做，統計要累加：星號題分頁只有 1 題，做兩輪最好驗
    pg.click("#t5")
    star_q = pg.evaluate("S.pool[0].q")
    n0 = pg.evaluate("qstat[%r] ? qstat[%r].n : 0" % (star_q, star_q))
    for _ in range(2):
        pg.wait_for_selector(".opts .opt")
        for k in pg.evaluate("S.pool[0].a"):
            pg.click(".opts .opt >> nth=%d" % k)
        pg.click("#btnCheck")                 # 批改
        pg.click("#btnCheck")                 # 只有一題，按下一題就結算
        ck("單題分頁做完會出成績單", pg.evaluate("report.classList.contains('show')"))
        pg.click("#btnCheck")                 # 再來一輪
    n1 = pg.evaluate("qstat[%r].n" % star_q)
    ck("同一題重複做，次數會累加", n1 >= n0 + 2, (n0, n1))
    pg.click("#t1")

    print("\n=== 19. 模擬考也計入統計 ===")
    h_before = pg.evaluate("hist.length")
    pg.click("#examBtn")
    pg.wait_for_function("S.exam === true")
    pg.evaluate("""
      S.pool.forEach((q,i)=>{ if(i < 5) S.answers[i] = q.a.slice(); });
      S.idx = 0; renderQ();
    """)
    pg.click("#btnNext"); pg.click(".ovbtns [data-act='submit']")
    ck("考試封存一筆", pg.evaluate("hist.length") == h_before + 1)
    ck("那一筆標成 exam", pg.evaluate("hist[0].k") == "exam")
    ck("考試只把作答過的題目計入 qstat（未作答不灌爆常錯題）",
       pg.evaluate("S.pool.filter(q=>{const r=qstat[q.q]; return r && r.n>0;}).length") <= 8,
       pg.evaluate("S.pool.filter(q=>{const r=qstat[q.q]; return r && r.n>0;}).length"))
    pg.click("#examBtn")
    pg.wait_for_function("S.exam === false")

    print("\n=== 20. 匯出／匯入存檔 ===")
    pg.click("#statBtn")
    with pg.expect_download() as dl:
        pg.click("#statwrap [data-act='export']")
    path = dl.value.path()
    import json
    saved = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    ck("匯出檔有 app 標記", saved.get("app") == "az900-practice")
    ck("匯出檔含統計", "az104.qstat.v1" in saved["data"])
    ck("匯出檔含歷次成績", "az104.hist.v1" in saved["data"])
    ck("匯出檔含星號", "az104.star.v1" in saved["data"])
    ck("匯出檔含錯題本", "az104.wrong.v1" in saved["data"])
    ck("檔名有日期", dl.value.suggested_filename.startswith("az900-progress-"))
    print("       匯出檔：%s（%.1f KB）" % (dl.value.suggested_filename,
                                          pathlib.Path(path).stat().st_size / 1024.0))
    hist_len = pg.evaluate("hist.length")
    star_n   = pg.evaluate("starSet.size")

    # 砍掉所有資料，再匯入回來
    pg.evaluate("Object.keys(localStorage).filter(k=>k.startsWith('az104.')).forEach(k=>localStorage.removeItem(k))")
    pg.reload()
    pg.wait_for_function("typeof S !== 'undefined' && S.pool.length > 0")
    ck("清空後統計是空的", pg.evaluate("hist.length") == 0 and pg.evaluate("Object.keys(qstat).length") == 0)
    pg.click("#statBtn")
    pg.set_input_files("#impFile", path)
    pg.wait_for_function("typeof hist !== 'undefined' && hist.length > 0", timeout=8000)
    ck("匯入後歷次成績回來", pg.evaluate("hist.length") == hist_len, pg.evaluate("hist.length"))
    ck("匯入後統計回來", pg.evaluate("Object.keys(qstat).length") > 0)
    ck("匯入後星號回來", pg.evaluate("starSet.size") == star_n, pg.evaluate("starSet.size"))

    # 匯入不是存檔的檔案要擋下來
    bad = ROOT / "shots" / "_notasave.json"
    bad.write_text('{"hello":"world"}', encoding="utf-8")
    pg.click("#statBtn")
    pg.set_input_files("#impFile", str(bad))
    pg.wait_for_selector("#stmsg.bad", timeout=5000)
    ck("不是存檔的檔案會被擋下", "匯入失敗" in pg.inner_text("#stmsg"))
    ck("擋下後資料沒被清掉", pg.evaluate("hist.length") == hist_len)
    pg.click("#statwrap [data-act='close']")
    bad.unlink()

    print("\n=== 21. 清除統計不會動到星號與錯題本 ===")
    pg.click("#statBtn")
    w_before = pg.evaluate("wrongSet.size"); s_before = pg.evaluate("starSet.size")
    pg.click("#statwrap [data-act='clear']")
    ck("按一次只是確認狀態", "再按一次" in pg.inner_text("#statwrap [data-act='clear']"))
    ck("按一次還沒清掉", pg.evaluate("hist.length") > 0)
    pg.click("#statwrap [data-act='clear']")
    ck("按第二次才清掉統計", pg.evaluate("hist.length") == 0 and pg.evaluate("Object.keys(qstat).length") == 0)
    ck("星號沒被清掉", pg.evaluate("starSet.size") == s_before)
    ck("錯題本沒被清掉", pg.evaluate("wrongSet.size") == w_before)
    pg.click("#statwrap [data-act='close']")

    print("\n=== JS 錯誤 ===")
    ck("沒有 JS 錯誤", not errs, errs[:3])
    b.close()

print("\n" + ("全部通過" if not fails else "失敗 %d 項：%s" % (len(fails), fails)))
