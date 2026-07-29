/* 校對用：檢查標準驗證腳本沒有涵蓋的東西。
   用法：node tools/audit.js [檔案]  （預設 tools/bank_doc.current.js）

   查七件事：
     1. v0 記的正解與資料裡的 a 是否一致（v0 是人手寫的，可能與資料對不上）
     2. v0 記的選項數與資料的格數是否一致
     3. ⟦⟧ 是否成對（含解析，validate.js 只查題幹）
     4. 可選的東西（o / items / dd）不可有標記
     5. dl 的 sent 佔位符 {0}…{n-1} 是否剛好對上 dd 格數，中英都要
     6. 中英各陣列長度是否相等
     7. 合併型解析是否還有整段重複殘留

   輸出分三級：
     【要修】      —— 必須清零
     【待確認】    —— 需要人判斷
     【已知差異】  —— 已判定不是問題的兩類（dd 描述的動詞形式改寫、圖形題的 v0），
                     只印總數與題號，避免真正要看的東西被淹沒。判別法見 normDesc
                     與 soft.diagram / soft.manual 三處註解。
*/
const fs = require("fs"), vm = require("vm");

const path = process.argv[2] || require("path").join(__dirname, "bank_doc.current.js");
const ctx = { out: null };
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path, "utf8") + ";out=BANK_DOC;", ctx);
const BANK = ctx.out;

const bad = [];
const warn = [];
const add = (list, n, msg) => list.push("#" + n + "  " + msg);
const paired = s => (String(s).match(/⟦/g) || []).length === (String(s).match(/⟧/g) || []).length;
const strip = s => String(s).replace(/[⟦⟧]/g, "");
// 比對用：去掉標點、空白、大小寫差異，只留字母數字
const norm = s => strip(s).toLowerCase().replace(/[^a-z0-9]/g, "");

/* dd 答案區描述專用的比對：容許一種**刻意的**改寫。
   原廠答案區的描述是祈使句（`Provide operating system virtualization`），
   因為原題是「描述」與「服務名」分兩欄並排；我們的介面把服務名填進描述裡連讀成
   一句，所以資料改成第三人稱（`provides operating system virtualization`）。
   這是轉錄時的統一決定，不是偏差，`norm` 卻會逐字報差異。
   這裡把兩邊都收斂成同一個基準形：去掉句首助動詞與 `used to`、去掉冠詞、
   去掉句首動詞的第三人稱 -s。同一套規則套在兩邊，所以就算某個字被削過頭也是對稱的。 */
const normDesc = s => norm(String(strip(s))
  .replace(/^\s*(?:is|are|will)\s+/i, "")
  .replace(/^\s*used\s+to\s+/i, "")
  .replace(/\b(?:a|an|the)\b/gi, "")
  .replace(/^(\s*\w+?)s\b/, "$1"));

/* 被歸類成「已知差異」而不再列進待確認的項目，最後只印總數 */
const soft = { desc: [], diagram: [], manual: [] };

for (const q of BANK) {
  const n = q.n, k = q.k || "mc";

  /* ---- 3. 標記成對 ---- */
  for (const [lab, v] of [["q", q.q], ["e", q.e], ["en.q", q.en && q.en.q], ["en.e", q.en && q.en.e],
                          ["sent", q.sent], ["en.sent", q.en && q.en.sent]]) {
    if (v && !paired(v)) add(bad, n, "標記不成對：" + lab);
  }
  for (const [lab, arr] of [["s", q.s], ["tgt", q.tgt], ["en.s", q.en && q.en.s], ["en.tgt", q.en && q.en.tgt]]) {
    if (arr) arr.forEach((v, i) => { if (!paired(v)) add(bad, n, "標記不成對：" + lab + "[" + i + "]"); });
  }

  /* ---- 4. 可選的東西不可有標記 ---- */
  const sel = [];
  if (q.o) sel.push(["o", q.o]);
  if (q.items) sel.push(["items", q.items]);
  if (q.dd) q.dd.forEach((g, i) => sel.push(["dd[" + i + "]", g]));
  if (q.en) {
    if (q.en.o) sel.push(["en.o", q.en.o]);
    if (q.en.items) sel.push(["en.items", q.en.items]);
    if (q.en.dd) q.en.dd.forEach((g, i) => sel.push(["en.dd[" + i + "]", g]));
  }
  for (const [lab, arr] of sel)
    arr.forEach((v, i) => { if (/[⟦⟧]/.test(v)) add(bad, n, "選項帶標記：" + lab + "[" + i + "]"); });

  /* ---- 6. 中英陣列長度 ---- */
  for (const f of ["o", "s", "items", "tgt"])
    if (q[f] && q.en && q.en[f] && q[f].length !== q.en[f].length)
      add(bad, n, `中英 ${f} 長度不等 ${q[f].length} vs ${q.en[f].length}`);
  if (q.dd && q.en && q.en.dd) {
    if (q.dd.length !== q.en.dd.length) add(bad, n, `中英 dd 格數不等 ${q.dd.length} vs ${q.en.dd.length}`);
    else q.dd.forEach((g, i) => { if (g.length !== q.en.dd[i].length) add(bad, n, `中英 dd[${i}] 選項數不等`); });
  }

  /* ---- 5. dl 佔位符 ---- */
  if (k === "dl") {
    for (const [lab, sent, dd] of [["sent", q.sent, q.dd], ["en.sent", q.en && q.en.sent, q.en && q.en.dd]]) {
      if (!sent || !dd) { add(bad, n, "dl 缺 " + lab + " 或 dd"); continue; }
      const found = [...String(sent).matchAll(/\{(\d+)\}/g)].map(m => +m[1]).sort((a, b) => a - b);
      const want = dd.map((_, i) => i);
      if (JSON.stringify(found) !== JSON.stringify(want))
        add(bad, n, `${lab} 佔位符 [${found}] 對不上 dd 格數 ${dd.length}`);
    }
  }

  /* ---- a 值範圍 ---- */
  if (k === "mc" && q.o) q.a.forEach(v => { if (!(v >= 0 && v < q.o.length)) add(bad, n, "a 超出 o 範圍：" + v); });
  if (k === "hs" && q.s) {
    if (q.a.length !== q.s.length) add(bad, n, `hs a 長度 ${q.a.length} ≠ s 長度 ${q.s.length}`);
    q.a.forEach(v => { if (v !== 0 && v !== 1) add(bad, n, "hs a 只能是 0/1，出現 " + v); });
  }
  if (k === "dd" && q.items) {
    if (q.a.length !== q.tgt.length) add(bad, n, `dd a 長度 ${q.a.length} ≠ tgt 長度 ${q.tgt.length}`);
    q.a.forEach(v => { if (!(v >= 0 && v < q.items.length)) add(bad, n, "dd a 超出 items 範圍：" + v); });
  }
  if (k === "dl" && q.dd) {
    if (q.a.length !== q.dd.length) add(bad, n, `dl a 長度 ${q.a.length} ≠ dd 格數 ${q.dd.length}`);
    q.a.forEach((v, i) => { if (q.dd[i] && !(v >= 0 && v < q.dd[i].length)) add(bad, n, `dl a[${i}] 超出範圍：` + v); });
  }

  /* ---- 解析不可留空 ---- */
  if (!q.e || !q.e.trim()) add(bad, n, "e 是空的");
  if (!q.en || !q.en.e || !q.en.e.trim()) add(bad, n, "en.e 是空的");

  /* ---- ico 服務圖示：只用在 mc，且必須與 o 逐項對應 ----
     洗牌時 permuteOptions() 會把 ico 跟著 o 一起換位，長度對不上就會錯位。 */
  if (q.ico) {
    if (k !== "mc") add(bad, n, `ico 只能用在 mc，這題是 ${k}`);
    else if (!q.o || q.ico.length !== q.o.length)
      add(bad, n, `ico 有 ${q.ico.length} 個，o 有 ${q.o ? q.o.length : 0} 個`);
    q.ico.forEach((v, i) => {
      if (!/^data:image\/(svg\+xml|png|jpeg);base64,/.test(v))
        add(bad, n, `ico[${i}] 不是內嵌的 data URI（不可連外）`);
    });
    /* 有圖示＝答案區是入口網站的截圖，順序是畫面的一部分，洗過就跟文件對不起來 */
    if (!q.fix) add(bad, n, "有 ico 卻沒有 fix:true，選項會被洗牌，順序就跟原文件不一致了");
  }

  /* ---- 1 & 2. v0 與資料對照 ---- */
  if (q.v0) {
    if (k === "dd") {
      const rows = [...q.v0.matchAll(/^\s*(\d+)\.\s*(.+?)\s*→\s*(.+?)\s*$/gm)];
      /* 排序題（#162）的答案區只有「1. 項目」沒有描述，巢狀圖（#227）連編號都沒有，
         兩種都不是「描述 → 項目」的格式，各自用自己的方式比對 */
      const plain = rows.length ? [] : [...q.v0.matchAll(/^\s*(\d+)\.\s*(.+?)\s*$/gm)];
      if (plain.length) {
        if (plain.length !== q.tgt.length)
          add(bad, n, `v0 記了 ${plain.length} 個排序項，資料有 ${q.tgt.length} 格`);
        else plain.forEach((m, i) => {
          const want = q.en && q.en.items ? q.en.items[q.a[i]] : null;
          if (want && norm(want) !== norm(m[2]))
            add(bad, n, `v0 第 ${i + 1} 位「${m[2]}」對不上資料的「${want}」`);
        });
      } else if (!rows.length) {
        /* 巢狀圖／四象限圖這種 v0，本來就不是「描述 → 項目」的文字格式。
           已經 vf:true 就代表人工核對過了，不必每次再提醒一遍。 */
        if (q.vf) soft.manual.push(n);
        else add(warn, n, "v0 不是可自動比對的格式（圖示題），需人工核對");
      }
      if (rows.length && rows.length !== q.tgt.length)
        add(bad, n, `v0 記了 ${rows.length} 組配對，資料有 ${q.tgt.length} 格`);
      else if (rows.length) rows.forEach((m, i) => {
        const want = q.en && q.en.items ? q.en.items[q.a[i]] : null;
        if (want && norm(want) !== norm(m[3])) {
          // 中文 items 有時寫成「中文（English）」，比對英文那半就好
          const zh = q.items[q.a[i]];
          if (norm(zh).indexOf(norm(m[3])) < 0 && norm(m[3]).indexOf(norm(want)) < 0)
            add(bad, n, `v0 第 ${i + 1} 格正解「${m[3]}」對不上資料的「${want}」`);
        }
        const wantDesc = q.en && q.en.tgt ? q.en.tgt[i] : null;
        if (wantDesc && norm(wantDesc) !== norm(m[2])) {
          if (!norm(m[2]))
            /* v0 的描述沒有任何可比對的英數字（例如 #469 記的是四象限圖的位置
               「左上（高安全性、不便利）」），跟英文描述本來就對不起來 */
            soft.diagram.push(`#${n}[${i + 1}]`);
          else if (normDesc(wantDesc) === normDesc(m[2]))
            soft.desc.push(`#${n}[${i + 1}]`);            // 只差在動詞形式，見 normDesc
          else
            add(warn, n, `v0 第 ${i + 1} 格描述與 en.tgt 用字不同\n      v0: ${m[2]}\n      資料: ${strip(wantDesc)}`);
        }
      });
    }
    if (k === "dl") {
      const opts = [...q.v0.matchAll(/下拉選項[：:]\s*(.+)/g)].map(m => m[1].split("｜").map(s => s.trim()));
      const ans = [...q.v0.matchAll(/正解[：:]\s*(.+)/g)].map(m => m[1].trim());
      if (opts.length && opts.length !== q.dd.length)
        add(bad, n, `v0 記了 ${opts.length} 格下拉，資料有 ${q.dd.length} 格`);
      if (ans.length && ans.length !== q.a.length)
        add(bad, n, `v0 記了 ${ans.length} 個正解，資料有 ${q.a.length} 格`);
      opts.forEach((g, i) => {
        if (q.dd[i] && g.length !== q.dd[i].length)
          add(bad, n, `v0 第 ${i + 1} 格 ${g.length} 個選項，資料有 ${q.dd[i].length} 個`);
      });
      ans.forEach((t, i) => {
        const want = q.en && q.en.dd && q.en.dd[i] ? q.en.dd[i][q.a[i]] : null;
        if (want && norm(want) !== norm(t))
          add(bad, n, `v0 第 ${i + 1} 格正解「${t}」對不上資料的「${want}」`);
      });
    }
  }

  /* ---- 7. 合併型解析的重複殘留 ---- */
  if (q.mg && q.e) {
    const segs = q.e.split(/\n(?=【)/);
    if (segs.length > 1) {
      const seen = new Map();   // 一整行 -> 第一次出現在第幾段
      let dup = 0, sample = null;
      segs.forEach((seg, si) => {
        for (const line of seg.split("\n")) {
          const t = strip(line).trim();
          if (t.length < 24) continue;              // 短行不算重複
          if (seen.has(t) && seen.get(t) !== si) {
            dup += t.length;
            if (!sample) sample = t.slice(0, 46);
          } else if (!seen.has(t)) seen.set(t, si);
        }
      });
      if (dup > 200) add(warn, n, `解析仍有 ${dup} 字整行重複（例：${sample}…）`);
    }
  }
}

/* ---- 8. 內容完全相同的重複題 ----
   原始文件本身就重複收錄了一些題目。都保留，但兩題的解析都要註明是哪一組，
   否則作答的人會以為自己記錯了。 */
const dupKey = q => {
  const e = q.en || {};
  return norm((e.q || "") + "|" + (e.o || e.items || []).map(norm).sort().join("~")
    + "|" + (e.s || e.tgt || []).map(norm).sort().join("~") + "|" + (e.sent || "")
    + "|" + (e.dd || []).map(g => g.map(norm).sort().join("_")).join("~"));
};
const groups = new Map();
for (const q of BANK) {
  const kk = dupKey(q);
  if (!groups.has(kk)) groups.set(kk, []);
  groups.get(kk).push(q);
}
/* 「有沒有註明」＝解析或題幹裡有沒有指名對方的題號。
   用題號比對而不是找「重複」這種關鍵字——#347 就是寫成「與第 188、280 題考的是
   同一個知識點」，意思到了但沒有關鍵字，用關鍵字判斷會誤報。 */
const mentions = (q, other) =>
  new RegExp(`(第\\s*${other}\\s*[、,，]|第\\s*${other}\\s*題|questions?\\s+[\\d,\\s和and]*\\b${other}\\b|#${other}\\b)`)
    .test(q.e + "\n" + q.q + "\n" + (q.en ? q.en.e + "\n" + q.en.q : ""));
for (const g of [...groups.values()].filter(v => v.length > 1)) {
  const ns = g.map(q => q.n);
  for (const q of g) {
    const missing = ns.filter(x => x !== q.n && !mentions(q, x));
    if (missing.length)
      add(warn, q.n, `與 #${missing.join("、#")} 內容相同，但解析沒有指名對方的題號`);
  }
}

const mg = BANK.filter(x => x.mg), vf = BANK.filter(x => x.vf);
console.log(`題數 ${BANK.length}　mg ${mg.length}　vf ${vf.length}　有 v0 ${BANK.filter(x => x.v0).length}`);
console.log(`題型 ${JSON.stringify(BANK.reduce((m, x) => (m[x.k || "mc"] = (m[x.k || "mc"] || 0) + 1, m), {}))}`);
console.log();
console.log(bad.length ? "【要修】\n" + bad.join("\n") : "【要修】無");
console.log();
console.log(warn.length ? "【待確認】\n" + warn.join("\n") : "【待確認】無");

/* 已知差異：判定為「不是問題」，但要留下數字，免得哪天真的變多了沒人發現 */
const softLines = [];
if (soft.desc.length)
  softLines.push(`　${soft.desc.length} 格 v0 描述只差在動詞形式（Provide→provides 等，見 normDesc）：` + soft.desc.join("、"));
if (soft.diagram.length)
  softLines.push(`　${soft.diagram.length} 格 v0 描述是圖形位置、無英數字可比對：` + soft.diagram.join("、"));
if (soft.manual.length)
  softLines.push(`　${soft.manual.length} 題 v0 是圖示格式且已 vf:true（人工核對過）：` + soft.manual.map(n => "#" + n).join("、"));
if (softLines.length) console.log("\n【已知差異，不列入待確認】\n" + softLines.join("\n"));

console.log(`\n合計：要修 ${bad.length} 項、待確認 ${warn.length} 項` +
  (softLines.length ? `、已知差異 ${soft.desc.length + soft.diagram.length + soft.manual.length} 項` : ""));
