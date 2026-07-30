// 一次性腳本：從 AZ900/az900-practice.html 抽出可重用引擎（樣式＋渲染／洗牌／進度／成績單邏輯），
// 拿掉 AZ900 專屬的 BANK_MINE 資料與英文術語對照表，換上 AZ104 的 BANK_AZ104，組出 az104-practice.html。
// 詳見 AZ104-SPEC.md 第 11 節。之後如果 AZ900 引擎有 bug 修正，可以重跑本腳本重新套用。
const fs = require("fs");
const path = require("path");

const AZ900_HTML = path.join(__dirname, "..", "..", "AZ900", "az900-practice.html");
const BANK_JS = path.join(__dirname, "bank_az104.current.js");
const OUT_HTML = path.join(__dirname, "..", "az104-practice.html");

const src = fs.readFileSync(AZ900_HTML, "utf8").replace(/\r\n/g, "\n");
const lines = src.split("\n"); // 1-indexed 使用時記得 -1

const L = (a, b) => lines.slice(a - 1, b).join("\n"); // 含頭尾行號（1-indexed, inclusive）

// ---- 1. 頭部：<head> + <style>，到 </head> 為止 ------------------------------
let head = L(1, 800);
head = head.replace(
  "<title>AZ-900 練習 · Azure Fundamentals Drill</title>",
  "<title>AZ-104 練習 · Azure Administrator Drill</title>"
);
head = head.replace(/az900\.theme\.v1/g, "az104.theme.v1");

// ---- 2. body 開頭到 </script> 前一行（916），也就是所有 UI 標記 ----------------
let body = L(801, 916);

body = body.replace("<h1>AZ-900 練習</h1>", "<h1>AZ-104 練習</h1>");

// 拿掉瀏覽次數徽章（外部連結，AZ104 專案不上 GitHub、不連外）
body = body.replace(
  /\s*<a class="hits"[\s\S]*?<\/a>\n/,
  "\n"
);

body = body.replace(
  '<span class="sub" id="srcTag" title="目前題庫（在設定裡切換）">自製題庫</span>',
  '<span class="sub" id="srcTag" title="目前題庫">Quiz20 題庫</span>'
);

body = body.replace(
  'title="題數說明：文件題庫的題數與跳號說明"',
  'title="題數說明：目前題庫的題數"'
);

body = body.replace(
  '<button role="tab" id="t1" aria-selected="false" aria-controls="pane"><span class="num">01</span>雲端概念</button>',
  '<button role="tab" id="t1" aria-selected="false" aria-controls="pane"><span class="num">01</span>身分與治理</button>'
);
body = body.replace(
  '<button role="tab" id="t2" aria-selected="false" aria-controls="pane"><span class="num">02</span>架構與服務</button>',
  '<button role="tab" id="t2" aria-selected="false" aria-controls="pane"><span class="num">02</span>儲存體與運算</button>'
);
body = body.replace(
  '<button role="tab" id="t3" aria-selected="false" aria-controls="pane"><span class="num">03</span>管理與治理</button>',
  '<button role="tab" id="t3" aria-selected="false" aria-controls="pane"><span class="num">03</span>網路與維運</button>'
);

// 題庫切換：AZ104 目前只有一份題庫，拿掉「自製題庫」按鈕，只留一顆已按下的「Quiz20 題庫」
body = body.replace(
`      <div class="langseg srcseg" id="srcSeg" role="group" aria-label="題庫來源">
        <button type="button" data-src="mine" aria-pressed="true"  title="我依官方大綱自行編寫的題庫">自製題庫</button>
        <button type="button" data-src="doc"  aria-pressed="false" title="由 AZ-900 PDF 逐題轉錄的題庫">文件題庫</button>
      </div>
    </div>
    <p class="cfghint" id="cfgSrcHint">兩份題庫的進度、統計、星號、錯題本各自獨立。</p>`,
`      <div class="langseg srcseg" id="srcSeg" role="group" aria-label="題庫來源">
        <button type="button" data-src="doc" aria-pressed="true" title="Build School 課程 Quiz20 逐題轉錄的題庫">Quiz20 題庫</button>
      </div>
    </div>
    <p class="cfghint" id="cfgSrcHint">目前只有一份題庫（Build School Quiz20，37 題，AZ104-Q712～Q748）。</p>`
);

// ---- 3. <script> 開場：換成 AZ104 版本的說明註解 -----------------------------
const scriptOpen = `<script>
"use strict";

/* =====================================================================
   題庫：來源見 AZ104-SPEC.md。轉錄自 Build School 課程 Quiz20（AZ104-Q712~Q748，37 題）
   d = 分頁用的領域桶：1 身分與治理｜2 儲存體與運算｜3 網路與維運（依官方五大技能領域歸併）
   od = 官方五大技能領域原始編號：1 身分治理｜2 儲存體｜3 運算｜4 網路｜5 監控維運（見 AZ104-SPEC.md §5）
   o/items/s/dd = 選項　a = 正確答案索引　e = 解析
   ===================================================================== */
`;

// ---- 4. BANK_AZ104 資料 -------------------------------------------------------
let bankJs = fs.readFileSync(BANK_JS, "utf8");
bankJs = bankJs.replace(/\nif \(typeof module.*\n/, "\n"); // 拿掉 module.exports，瀏覽器不需要
// AZ900 引擎裡到處寫死 BANK_DOC 這個名字（setSource／restoreSessions／sigOf…），
// 用別名保留 BANK_AZ104 這個語意化的名字當唯一真實來源，同時讓引擎不用大改
bankJs += "\nconst BANK_DOC = BANK_AZ104; // 別名，給沿用自 AZ900 的引擎程式碼用\n";

// ---- 5. 引擎本體：BANK_DOC 陣列結束（第 6342 行 "];"）之後，到 EN 對照表區塊開始之前 --
// 6344~8762：BANK 切換／洗牌／渲染／進度／統計／設定面板等所有邏輯，含通用術語表 GLOSSARY_MAP。
// 8763~9756：AZ900 專屬的「自製題庫」英文逐題對照表（Object.assign(EN, {...}) x5），與 AZ104 無關，整段不收。
// 9758~9776：語言／題庫還原、開場流程。
let engineA = L(6344, 8761); // 8762 是「EN：領域 1 雲端概念」註解，屬於下面被排除的 Object.assign(EN,...) 區塊，不含
let engineB = L(9758, 9775); // 9776 是原始檔案自己的 </script>，不含，最後統一由 scriptClose 補上

function mustReplace(text, oldStr, newStr, label) {
  if (text.indexOf(oldStr) === -1) throw new Error("找不到片段，AZ900 原始檔可能已變動：" + label);
  return text.split(oldStr).join(newStr);
}

// BANK 預設指向 BANK_DOC（唯一題庫），不再有 BANK_MINE
engineA = mustReplace(engineA, "let BANK = BANK_MINE;", "let BANK = BANK_DOC;", "let BANK = BANK_MINE;");
// mergeEN() 是「自製題庫」專用（把中文題幹對照到英文），AZ104 沒有這份資料，改成空陣列，函式維持存在但永遠是 no-op
engineA = mustReplace(engineA, "BANK_MINE.forEach(q=>{", "[].forEach(q=>{", "BANK_MINE.forEach 於 mergeEN()");
// persistSess()：不分 mine/doc，一律用 BANK_DOC 算簽章
engineA = mustReplace(
  engineA,
  'o.sig = sigOf(src === "mine" ? BANK_MINE : BANK_DOC);',
  "o.sig = sigOf(BANK_DOC);",
  "persistSess 的 sigOf 三元運算"
);
// restoreSessions()：只需要還原 doc 這一份（不再有 mine）
engineA = mustReplace(engineA, '["mine","doc"].forEach(src=>{', '["doc"].forEach(src=>{', "restoreSessions 的 mine/doc 陣列");
engineA = mustReplace(
  engineA,
  'const bank = src === "mine" ? BANK_MINE : BANK_DOC;',
  "const bank = BANK_DOC;",
  "restoreSessions 的 bank 三元運算"
);
engineA = mustReplace(
  engineA,
  'BANK = src === "mine" ? BANK_MINE : BANK_DOC;',
  "BANK = BANK_DOC;",
  "setSource 的 BANK 三元運算"
);

// 預設題庫來源、目前作答統計指標都指向 doc（唯一題庫）
engineA = mustReplace(engineA, 'src:  "mine",    // mine 自製題庫 / doc 文件題庫', 'src:  "doc",     // 目前只有一份題庫（Quiz20）', "S.src 預設值");
engineA = mustReplace(engineA, "let wrongSet = WRONG.mine;", "let wrongSet = WRONG.doc;", "wrongSet 預設值");
engineA = mustReplace(engineA, "let starSet = STAR.mine;", "let starSet = STAR.doc;", "starSet 預設值");
engineA = mustReplace(engineA, "let qstat = QSTAT.mine, hist = HIST.mine;", "let qstat = QSTAT.doc, hist = HIST.doc;", "qstat/hist 預設值");

// 模擬考：AZ104 目前只有 37 題（小於 AZ900 的 40 題設定），一律全部抽出
engineA = mustReplace(engineA, "const EXAM_N = 40, EXAM_SEC = 45*60, PASS = 70;", "const EXAM_N = 37, EXAM_SEC = 45*60, PASS = 70;", "EXAM_N 常數");

// 解析標題：AZ900 寫死「PDF question / 原始文件第 N 題」，AZ104 的來源是 Build School 的 Quiz20 網頁，不是 PDF
engineA = mustReplace(
  engineA,
  "? (EN ? `Explanation · PDF question #${q.n}` : `解析 · 原始文件第 ${q.n} 題`)",
  "? (EN ? `Explanation · ${q.code || ('#' + q.n)}` : `解析 · ${q.code || ('第 ' + q.n + ' 題')}`)",
  "解析標題的 PDF question 字樣"
);

// 題目上方 meta 列的領域名稱（跟分頁標籤是兩個獨立的常數，各自要改）
engineA = mustReplace(
  engineA,
  'const DOMAIN_NAME = {1:"雲端概念", 2:"Azure 架構與服務", 3:"管理與治理"};',
  'const DOMAIN_NAME = {1:"身分與治理", 2:"儲存體與運算", 3:"網路與維運"};',
  "DOMAIN_NAME"
);
engineA = mustReplace(
  engineA,
  'const DOMAIN_NAME_EN = {1:"Cloud concepts", 2:"Azure architecture & services", 3:"Management & governance"};',
  'const DOMAIN_NAME_EN = {1:"Identity & Governance", 2:"Storage & Compute", 3:"Networking & Monitoring"};',
  "DOMAIN_NAME_EN"
);

// 分頁標籤：從 AZ900 的三個領域改成 AZ104 的三個技能桶
engineA = mustReplace(
  engineA,
  'const TAB_ZH = ["全部","雲端概念","架構與服務","管理與治理","錯題本","星號題"];',
  'const TAB_ZH = ["全部","身分與治理","儲存體與運算","網路與維運","錯題本","星號題"];',
  "TAB_ZH"
);
engineA = mustReplace(
  engineA,
  'const TAB_EN = ["All","Cloud concepts","Architecture","Governance","Review","Starred"];',
  'const TAB_EN = ["All","Identity & Governance","Storage & Compute","Networking & Monitoring","Review","Starred"];',
  "TAB_EN"
);

// localStorage 鍵一律改用 az104.* 前綴，不與 AZ900 混用
engineA = engineA.replace(/az900\./g, "az104.");
engineA = engineA.replace(/az900-practice/g, "az104-practice");
engineA = engineA.replace(/az900-progress/g, "az104-progress");

// 題庫標籤文字：唯一題庫一律顯示「Quiz20 題庫」，不再是「文件題庫／自製題庫」二選一
engineA = engineA.replace(/文件題庫/g, "Quiz20 題庫");
engineA = engineA.replace(/"document bank"/g, '"Quiz20 bank"');
engineA = engineA.replace(/"Doc bank"/g, '"Quiz20 bank"');

// 使用說明文字裡「自製題庫沒有題號」那段是描述 AZ900 雙題庫的邊界案例，AZ104 用不到
engineA = mustReplace(
  engineA,
  "（自製題庫沒有題號，就直接輸入本輪的第幾題。按 <code>/</code> 鍵可以快速對焦）",
  "（按 <code>/</code> 鍵可以快速對焦）",
  "practice_zh 的自製題庫說明"
);
engineA = mustReplace(
  engineA,
  "(the hand-written bank has no numbers, so there the box takes the position instead; press <code>/</code> to focus it)",
  "(press <code>/</code> to focus it)",
  "practice_en 的 hand-written bank 說明"
);

// docEmpty 的提示文字：原本會叫使用者「切回自製題庫」，AZ104 沒有那顆按鈕了（這支分支目前不會被觸發，因為
// BANK_DOC 一定有 37 題，但文字留著不對就先修掉，以防日後不小心把 BANK_AZ104 清空）
engineA = mustReplace(
  engineA,
  '"Quiz20 題庫還沒有匯入題目。<br>轉錄完成後這裡就會出現題目，切回「自製題庫」可以照常練習。"',
  '"Quiz20 題庫還沒有匯入題目。<br>轉錄完成後這裡就會出現題目。"',
  "docEmpty 中文提示"
);
engineA = mustReplace(
  engineA,
  '"The document question bank has not been imported yet."',
  '"The Quiz20 question bank has not been imported yet."',
  "docEmpty 英文提示"
);

// restore-session 區塊：唯一題庫一律還原 doc，不用管 mine
engineB = mustReplace(
  engineB,
  'if(savedSrc === "doc" && BANK_DOC.length){    /* 文件題庫還沒匯入就不還原 */\n    S.src = "doc"; BANK = BANK_DOC; wrongSet = WRONG.doc; starSet = STAR.doc;\n  }',
  'if(BANK_DOC.length){ BANK = BANK_DOC; wrongSet = WRONG.doc; starSet = STAR.doc; }',
  "還原題庫來源區塊"
);

const scriptClose = "</script>";

const out = [head, body, scriptOpen, bankJs, engineA, engineB, scriptClose].join("\n");

if (out.includes("BANK_MINE")) throw new Error("組出來的檔案還殘留 BANK_MINE 參照，沒清乾淨");
if (/\baz900\./.test(out)) throw new Error("組出來的檔案還殘留 az900. 開頭的 key，沒改成 az104.");

fs.writeFileSync(OUT_HTML, out, "utf8");
console.log("wrote", OUT_HTML, "(" + out.length + " bytes)");
