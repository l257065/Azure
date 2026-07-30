# -*- coding: utf-8 -*-
"""
由 AZ900/az900-practice.html 產生 AZ104/az104-practice.html 的骨架。

只做「換殼」：把 AZ-900 的引擎原封不動搬過來，
清空兩份題庫、拿掉只服務 BANK_MINE 的 EN 對照表，
再把品牌、localStorage 鍵、領域（3 → 5）、分頁索引、考試參數換成 AZ-104 的。

這支是一次性的腳本，跑完就不需要再跑；保留下來是為了讓人看得出
az104-practice.html 到底跟 AZ-900 差在哪，日後 AZ-900 引擎有修正時，
也可以照同一份對照表重新搬一次。

    python tools/build_skeleton.py

輸出：AZ104/az104-practice.html
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
AZ104 = os.path.dirname(HERE)
ROOT = os.path.dirname(AZ104)
SRC = os.path.join(ROOT, "AZ900", "az900-practice.html")
DST = os.path.join(AZ104, "az104-practice.html")


def read(path):
    with io.open(path, encoding="utf-8") as f:
        return f.read()


def empty_array(lines, head):
    """把 `const XXX = [` 到對應的 `];` 之間整段清空。"""
    i = next(k for k, l in enumerate(lines) if l.startswith(head))
    j = next(k for k in range(i + 1, len(lines)) if lines[k] == "];")
    return lines[:i + 1] + lines[j:]


def drop_between(lines, start_marker, end_marker):
    """刪掉 start_marker 那一行到 end_marker 那一行（不含）之間的所有行。"""
    i = next(k for k, l in enumerate(lines) if l.startswith(start_marker))
    j = next(k for k in range(i + 1, len(lines)) if lines[k].startswith(end_marker))
    return lines[:i] + lines[j:]


def sub(text, old, new, count=None):
    """一定要有東西被換掉，否則就是上游 HTML 改過了 —— 直接爆掉比默默漏掉好。"""
    n = text.count(old)
    if n == 0:
        raise SystemExit("找不到要取代的片段（AZ900 的 HTML 改過了？）：\n" + old[:200])
    if count is not None and n != count:
        raise SystemExit("取代次數不符（預期 %d，實際 %d）：\n%s" % (count, n, old[:200]))
    return text.replace(old, new)


# ---------------------------------------------------------------- 1. 清空題庫
lines = read(SRC).split("\n")
lines = empty_array(lines, "const BANK_MINE = [")
lines = empty_array(lines, "const BANK_DOC = [")
# 只服務 BANK_MINE 的 EN 對照表，題庫清空後整批沒有意義
lines = drop_between(lines, "/* ============ EN：領域 1", "try{")
h = "\n".join(lines)

# ------------------------------------------------------- 2. 品牌與 localStorage
h = sub(h, "az900.", "az104.")
h = sub(h, "az900-practice", "az104-practice")
h = sub(h, "az900-progress-", "az104-progress-")
h = sub(h, "not an az900 save file", "not an az104 save file")
h = sub(h, "AZ-900 練習 · Azure Fundamentals Drill",
        "AZ-104 練習 · Azure Administrator Drill", 1)
h = sub(h, "<h1>AZ-900 練習</h1>", "<h1>AZ-104 練習</h1>", 1)
h = sub(h, "題庫：依 AZ-900 官方大綱自行編寫（非考古題）",
        "題庫：依 AZ-104 官方大綱自行編寫（非考古題）", 1)
h = sub(h, 'title="由 AZ-900 PDF 逐題轉錄的題庫"',
        'title="由 AZ-104 考古題文件逐題轉錄的題庫"', 1)

# --------------------------------------------------------------- 3. 五個領域
h = sub(h, '''const DOMAIN_NAME = {1:"雲端概念", 2:"Azure 架構與服務", 3:"管理與治理"};
const DOMAIN_NAME_EN = {1:"Cloud concepts", 2:"Azure architecture & services", 3:"Management & governance"};''',
        '''const DOMAIN_NAME = {1:"身分與治理", 2:"儲存體", 3:"運算資源", 4:"虛擬網路", 5:"監控與維護"};
const DOMAIN_NAME_EN = {1:"Identities & governance", 2:"Storage", 3:"Compute", 4:"Virtual networking", 5:"Monitor & maintain"};
const D_MAX = 5;                      /* 領域數；分頁 1..D_MAX 就是各領域 */
const TAB_WRONG = D_MAX + 1;          /* 錯題本 */
const TAB_STAR  = D_MAX + 2;          /* 星號題 */
const TAB_MAX   = TAB_STAR;''', 1)

h = sub(h, "   d = 領域：1 雲端概念｜2 Azure 架構與服務｜3 管理與治理",
        "   d = 領域：1 身分與治理｜2 儲存體｜3 運算資源｜4 虛擬網路｜5 監控與維護", 1)

h = sub(h, "  tab: 0,          // 0 全部 / 1-3 領域 / 4 錯題本 / 5 星號題",
        "  tab: 0,          // 0 全部 / 1-5 領域 / 6 錯題本 / 7 星號題", 1)

h = sub(h, '''  <nav class="tabs" role="tablist">
    <button role="tab" id="t0" aria-selected="true" aria-controls="pane"><span class="num">ALL</span>全部</button>
    <button role="tab" id="t1" aria-selected="false" aria-controls="pane"><span class="num">01</span>雲端概念</button>
    <button role="tab" id="t2" aria-selected="false" aria-controls="pane"><span class="num">02</span>架構與服務</button>
    <button role="tab" id="t3" aria-selected="false" aria-controls="pane"><span class="num">03</span>管理與治理</button>
    <button role="tab" id="t4" aria-selected="false" aria-controls="pane"><span class="num">✗</span>錯題本</button>
    <button role="tab" id="t5" aria-selected="false" aria-controls="pane"><span class="num">★</span>星號題</button>
  </nav>''',
        '''  <nav class="tabs" role="tablist">
    <button role="tab" id="t0" aria-selected="true" aria-controls="pane"><span class="num">ALL</span>全部</button>
    <button role="tab" id="t1" aria-selected="false" aria-controls="pane"><span class="num">01</span>身分治理</button>
    <button role="tab" id="t2" aria-selected="false" aria-controls="pane"><span class="num">02</span>儲存體</button>
    <button role="tab" id="t3" aria-selected="false" aria-controls="pane"><span class="num">03</span>運算</button>
    <button role="tab" id="t4" aria-selected="false" aria-controls="pane"><span class="num">04</span>網路</button>
    <button role="tab" id="t5" aria-selected="false" aria-controls="pane"><span class="num">05</span>監控</button>
    <button role="tab" id="t6" aria-selected="false" aria-controls="pane"><span class="num">✗</span>錯題本</button>
    <button role="tab" id="t7" aria-selected="false" aria-controls="pane"><span class="num">★</span>星號題</button>
  </nav>''', 1)

h = sub(h, '''const TAB_ZH = ["全部","雲端概念","架構與服務","管理與治理","錯題本","星號題"];
const TAB_EN = ["All","Cloud concepts","Architecture","Governance","Review","Starred"];''',
        '''const TAB_ZH = ["全部","身分治理","儲存體","運算","網路","監控","錯題本","星號題"];
const TAB_EN = ["All","Identity","Storage","Compute","Network","Monitor","Review","Starred"];''', 1)

# -------------------------------------------------- 4. 分頁索引：4/5 → 6/7
h = sub(h, '''function poolFor(tab){
  if(tab === 4) return BANK.filter(q => wrongSet.has(q.q));
  if(tab === 5) return BANK.filter(q => starSet.has(q.q));''',
        '''function poolFor(tab){
  if(tab === TAB_WRONG) return BANK.filter(q => wrongSet.has(q.q));
  if(tab === TAB_STAR)  return BANK.filter(q => starSet.has(q.q));''', 1)

h = sub(h, "    for(let tab=0; tab<=5; tab++){", "    for(let tab=0; tab<=TAB_MAX; tab++){", 1)
h = sub(h, "  if(savedTab >= 0 && savedTab <= 5) S.tab = savedTab;",
        "  if(savedTab >= 0 && savedTab <= TAB_MAX) S.tab = savedTab;", 1)
h = sub(h, "  if(S.tab === 4 || S.tab === 5){", "  if(S.tab === TAB_WRONG || S.tab === TAB_STAR){", 1)
h = sub(h, '''    eyebrow.textContent = S.tab === 4 ? (en?"Review list":"錯題本")
                        : S.tab === 5 ? (en?"Starred":"星號題")''',
        '''    eyebrow.textContent = S.tab === TAB_WRONG ? (en?"Review list":"錯題本")
                        : S.tab === TAB_STAR ? (en?"Starred":"星號題")''', 1)
h = sub(h, "        : S.tab === 4\n", "        : S.tab === TAB_WRONG\n", 1)
h = sub(h, "        : S.tab === 5\n", "        : S.tab === TAB_STAR\n", 1)

# --------------------------------------------------------- 5. 領域統計五格
h = sub(h, "  const out = {1:{n:0,w:0,seen:0,tot:0}, 2:{n:0,w:0,seen:0,tot:0}, 3:{n:0,w:0,seen:0,tot:0}};",
        "  const out = {};\n  for(let d = 1; d <= D_MAX; d++) out[d] = {n:0, w:0, seen:0, tot:0};", 1)

# ------------------------------------------- 6. 分頁多了兩個，窄螢幕要再縮
h = sub(h, '''/* 多了「星號題」變成 6 個分頁，窄螢幕要縮字才不會把「架構與服務」折行 */
@media (max-width:560px){
  nav.tabs button{font-size:.71rem;padding:9px 1px 10px;white-space:nowrap}
  nav.tabs button .num{font-size:.58rem;letter-spacing:.06em}
}
@media (max-width:380px){
  nav.tabs button{font-size:.66rem}
}''',
        '''/* AZ-104 有五個領域，加上全部／錯題本／星號題共 8 個分頁，
   比 AZ-900 的 6 個更擠，窄螢幕要再縮一級才不會折行 */
@media (max-width:560px){
  nav.tabs button{font-size:.66rem;padding:9px 0 10px;white-space:nowrap}
  nav.tabs button .num{font-size:.54rem;letter-spacing:.04em}
}
@media (max-width:380px){
  nav.tabs button{font-size:.6rem}
  nav.tabs button .num{font-size:.5rem;letter-spacing:0}
}''', 1)

# ------------------------------------------------------------- 7. 考試參數
# AZ-104：作答 100 分鐘（座位 120 分鐘）、官方只說多數考試 40–60 題、700/1000 換算分數
h = sub(h, "const EXAM_N = 40, EXAM_SEC = 45*60, PASS = 70;",
        "const EXAM_N = 50, EXAM_SEC = 100*60, PASS = 70;", 1)
h = sub(h, 'title="模擬考：抽 40 題、45 分鐘限時，作答期間不顯示答案，交卷後一次檢討"',
        'title="模擬考：抽 50 題、100 分鐘限時，作答期間不顯示答案，交卷後一次檢討"', 1)
h = sub(h, '<span class="score timer" id="timer" hidden>⏱ 45:00</span>',
        '<span class="score timer" id="timer" hidden>⏱ 100:00</span>', 1)
h = sub(h, "模擬考：隨機抽 ${EXAM_N} 題、限時 45 分鐘", "模擬考：隨機抽 ${EXAM_N} 題、限時 100 分鐘", 1)
h = sub(h, "Mock exam: ${EXAM_N} random questions, 45-minute limit",
        "Mock exam: ${EXAM_N} random questions, 100-minute limit", 1)
h = sub(h, '? "Mock exam: 40 questions, 45 minutes, answers hidden until you submit"',
        '? "Mock exam: 50 questions, 100 minutes, answers hidden until you submit"', 1)
h = sub(h, ': "模擬考：抽 40 題、45 分鐘限時，作答期間不顯示答案，交卷後一次檢討";',
        ': "模擬考：抽 50 題、100 分鐘限時，作答期間不顯示答案，交卷後一次檢討";', 1)

with io.open(DST, "w", encoding="utf-8", newline="\n") as f:
    f.write(h)

print("已輸出 %s（%d 行、%.1f KB）" % (
    os.path.relpath(DST, ROOT), h.count("\n") + 1, len(h.encode("utf-8")) / 1024.0))
