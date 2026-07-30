// 一次性腳本：從 AZ900/az900-practice.html 抽出可重用引擎（樣式＋渲染／洗牌／進度／成績單邏輯），
// 拿掉 AZ900 專屬的英文術語對照表，換上 AZ104 的兩份題庫（BANK_MINE／BANK_DOC），組出 az104-practice.html。
// 詳見 AZ104-SPEC.md 第 11 節。之後如果 AZ900 引擎有 bug 修正，可以重跑本腳本重新套用。
const fs = require("fs");
const path = require("path");

const AZ900_HTML = path.join(__dirname, "..", "..", "AZ900", "az900-practice.html");
const BANK_MINE_JS = path.join(__dirname, "bank_az104.current.js");
const BANK_DOC_JS = path.join(__dirname, "bank_doc.current.js");
const OUT_HTML = path.join(__dirname, "..", "az104-practice.html");

const src = fs.readFileSync(AZ900_HTML, "utf8").replace(/\r\n/g, "\n");
const lines = src.split("\n"); // 1-indexed 使用時記得 -1

const L = (a, b) => lines.slice(a - 1, b).join("\n"); // 含頭尾行號（1-indexed, inclusive）

// ---- 1. 頭部：<head> + <style>，到 </head> 為止 ------------------------------
let head = L(1, 816);
head = head.replace(
  "<title>AZ-900 練習 · Azure Fundamentals Drill</title>",
  "<title>AZ-104 練習 · Azure Administrator Drill</title>"
);
head = head.replace(/az900\.theme\.v1/g, "az104.theme.v1");

// ---- 2. body 開頭到 </script> 前一行（932），也就是所有 UI 標記 ----------------
let body = L(817, 932);

body = body.replace("<h1>AZ-900 練習</h1>", "<h1>AZ-104 練習</h1>");

// 拿掉瀏覽次數徽章（外部連結，AZ104 專案不上 GitHub、不連外）
body = body.replace(
  /\s*<a class="hits"[\s\S]*?<\/a>\n/,
  "\n"
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

// 題庫切換：AZ104 有兩份獨立題庫（見 AZ104-SPEC.md 第 5 節），沿用 AZ900 的雙題庫切換 UI，
// 只把按鈕的 title 換成 AZ104 自己的來源說明（AZ900 的原文是「我依官方大綱自行編寫的題庫」／
// 「由 AZ-900 PDF 逐題轉錄的題庫」，跟 AZ104 的實際來源對不上）
body = body.replace(
  'title="我依官方大綱自行編寫的題庫">自製題庫</button>',
  'title="Build School 課程逐題轉錄的題庫（Quiz1~12）">自製題庫</button>'
);
body = body.replace(
  'title="由 AZ-900 PDF 逐題轉錄的題庫">文件題庫</button>',
  'title="PDF 考古題逐題轉錄的題庫（Question Set 1）">文件題庫</button>'
);

// ---- 3. <script> 開場：換成 AZ104 版本的說明註解 -----------------------------
const scriptOpen = `<script>
"use strict";

/* =====================================================================
   兩份題庫，來源見 AZ104-SPEC.md：
     BANK_MINE（自製題庫）：轉錄自 Build School 課程 Quiz1~12（372 題）
     BANK_DOC （文件題庫）：轉錄自 az104-skeleton 分支的 PDF 考古題 Question Set 1（40 題）
   兩份題庫的分數、錯題本、星號題、統計、進度各自獨立（沿用 AZ900 的雙題庫機制）。
   d = 分頁用的領域桶：1 身分與治理｜2 儲存體與運算｜3 網路與維運（依官方五大技能領域歸併）
   od = 官方五大技能領域原始編號：1 身分治理｜2 儲存體｜3 運算｜4 網路｜5 監控維運（見 AZ104-SPEC.md §5）
   o/items/s/dd = 選項　a = 正確答案索引　e = 解析
   ===================================================================== */
`;

// ---- 4. 兩份題庫資料 -----------------------------------------------------------
let bankMineJs = fs.readFileSync(BANK_MINE_JS, "utf8");
bankMineJs = bankMineJs.replace(/\nif \(typeof module.*\n/, "\n"); // 拿掉 module.exports，瀏覽器不需要
// AZ900 引擎裡到處寫死 BANK_MINE 這個名字（setSource／restoreSessions／sigOf…），
// 用別名保留 BANK_AZ104 這個語意化的名字當唯一真實來源，同時讓引擎不用大改
bankMineJs += "\nconst BANK_MINE = BANK_AZ104; // 別名，給沿用自 AZ900 的引擎程式碼用\n";

let bankDocJs = fs.readFileSync(BANK_DOC_JS, "utf8");
bankDocJs = bankDocJs.replace(/\nif \(typeof module.*\n/, "\n");

const bankJs = bankMineJs + "\n" + bankDocJs;

// ---- 5. 引擎本體：兩份題庫陣列結束之後，到 EN 對照表區塊開始之前 --
// 6360~8792：BANK 切換／洗牌／渲染／進度／統計／設定面板等所有邏輯，含通用術語表 GLOSSARY_MAP。
// 8793~9787：AZ900 專屬的「自製題庫」英文逐題對照表（Object.assign(EN, {...}) x5），與 AZ104 無關，整段不收
//            （AZ104 的 BANK_MINE 每一題都自帶 en:{q,o,e}，不需要這份對照表，mergeEN() 找不到對應項目時
//            會直接跳過、不覆寫既有的 q.en，見 mergeEN() 本體，所以留著原樣呼叫也不會出錯）。
// 9789~9806：語言／題庫還原、開場流程。
// （這五個行號會隨 az900-practice.html 引擎改動而位移；改動後若這裡 mustReplace 找不到片段，
//  先用 grep -n 對照本檔案原本引用的錨點文字，重新算出新行號）
let engineA = L(6360, 8792); // 8793 是「EN：領域 1 雲端概念」註解，屬於下面被排除的 Object.assign(EN,...) 區塊，不含
let engineB = L(9789, 9806); // 9807 是原始檔案自己的 </script>，不含，最後統一由 scriptClose 補上

function mustReplace(text, oldStr, newStr, label) {
  if (text.indexOf(oldStr) === -1) throw new Error("找不到片段，AZ900 原始檔可能已變動：" + label);
  return text.split(oldStr).join(newStr);
}

// 解析標題：AZ900 寫死「PDF question / 原始文件第 N 題」，AZ104 兩份題庫都用自己的 code 顯示（AZ104-Q403／S1#1）
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

// 分頁標籤：從 AZ900 的三個領域改成 AZ104 的三個技能桶（兩份題庫的 d 都已歸併成同一套 1-3 桶，見 SPEC §5）
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

// 使用說明文字裡「自製題庫沒有題號」那段是描述 AZ900 自己那份手寫題庫沒有外部題號的邊界案例；
// AZ104 的兩份題庫（Build School 流水號、PDF 的 Question #）都有真實題號，這段提示不適用
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

const scriptClose = "</script>";

const out = [head, body, scriptOpen, bankJs, engineA, engineB, scriptClose].join("\n");

if (/\baz900\./.test(out)) throw new Error("組出來的檔案還殘留 az900. 開頭的 key，沒改成 az104.");

fs.writeFileSync(OUT_HTML, out, "utf8");
console.log("wrote", OUT_HTML, "(" + out.length + " bytes)");
