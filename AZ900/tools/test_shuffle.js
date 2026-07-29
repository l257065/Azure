/* 洗牌不變式測試：直接載入 HTML 裡真正的 permuteOptions()，跑 200 輪。
   用法：node tools/test_shuffle.js

   要驗的是「洗完之後，每一個東西還指著原本那個東西」：
     mc  選項文字 ↔ 英文選項 ↔ 服務圖示 ↔ 正解索引
     hs  敘述 ↔ 英文敘述 ↔ 逐句答案
     dd  可拖曳項目 ↔ 英文項目、答案區 ↔ 英文答案區、a 指到正確項目
     dl  每格選項 ↔ 英文選項 ↔ 該格答案
   以及帶入先前的 _p 能不能洗回一模一樣的順序（進度續作靠這個）。
*/
const fs = require("fs"), vm = require("vm"), path = require("path");

const html = fs.readFileSync(path.join(__dirname, "..", "az900-practice.html"), "utf8");
const grab = (name) => {
  const i = html.indexOf("const " + name);
  const j = html.indexOf("\n];", i);
  return html.slice(i, j + 3);
};
const fn = (name) => {
  const i = html.indexOf("function " + name + "(");
  // 從函式開頭數大括號，數到配對的那一個為止
  let depth = 0, started = false;
  for (let k = i; k < html.length; k++) {
    if (html[k] === "{") { depth++; started = true; }
    else if (html[k] === "}") { depth--; if (started && depth === 0) return html.slice(i, k + 1); }
  }
  throw new Error("找不到 " + name);
};

const ctx = { out: null, console };
vm.createContext(ctx);
vm.runInContext(grab("BANK_DOC") + ";out=BANK_DOC;", ctx);
const BANK = ctx.out;

// permuteOptions 依賴 shuffle 與 kindOf，這兩個是 const 箭頭函式，整行抓
const line = (re) => html.split("\n").find(L => re.test(L));
vm.runInContext([line(/^const kindOf\s*=/), line(/^const shuffle\s*=/), fn("permuteOptions")].join("\n"), ctx);
const permute = (q, p) => vm.runInContext("permuteOptions", ctx)(q, p);

const ROUNDS = 200;
const bad = [];
const clone = o => JSON.parse(JSON.stringify(o));

for (const orig of BANK) {
  const k = orig.k || "mc";
  for (let r = 0; r < ROUNDS / (BANK.length > 100 ? 20 : 1); r++) {
    const q = clone(orig);
    permute(q);

    if (k === "mc") {
      /* fix:true＝答案區是入口網站的截圖，順序本身就是題目的一部分，一格都不能動 */
      if (orig.fix) {
        if (JSON.stringify(q.o) !== JSON.stringify(orig.o))
          bad.push(`#${orig.n} mc fix:true 但選項被洗了`);
        if (JSON.stringify(q.a) !== JSON.stringify(orig.a))
          bad.push(`#${orig.n} mc fix:true 但答案索引被改了`);
        if (q.ico && JSON.stringify(q.ico) !== JSON.stringify(orig.ico))
          bad.push(`#${orig.n} mc fix:true 但圖示被洗了`);
      }
      // 正解的文字內容必須還是原本那些
      const want = orig.a.map(i => orig.o[i]).sort();
      const got = q.a.map(i => q.o[i]).sort();
      if (JSON.stringify(want) !== JSON.stringify(got))
        bad.push(`#${orig.n} mc 洗完正解對不上：${got} ≠ ${want}`);
      // 中英必須成對
      if (q.en && q.en.o) q.o.forEach((t, i) => {
        const oi = orig.o.indexOf(t);
        if (oi >= 0 && orig.en.o[oi] !== q.en.o[i])
          bad.push(`#${orig.n} mc 中英錯位：「${t}」配到「${q.en.o[i]}」`);
      });
      // 圖示必須跟著選項走
      if (q.ico) q.o.forEach((t, i) => {
        const oi = orig.o.indexOf(t);
        if (oi >= 0 && orig.ico[oi] !== q.ico[i])
          bad.push(`#${orig.n} mc 圖示錯位：「${t}」配到別的圖`);
      });
    }

    if (k === "hs") {
      q.s.forEach((t, i) => {
        const oi = orig.s.indexOf(t);
        if (oi >= 0 && orig.a[oi] !== q.a[i])
          bad.push(`#${orig.n} hs 逐句答案錯位：「${t.slice(0,20)}」`);
        if (q.en && q.en.s && oi >= 0 && orig.en.s[oi] !== q.en.s[i])
          bad.push(`#${orig.n} hs 中英錯位`);
      });
    }

    if (k === "dd") {
      q.tgt.forEach((t, i) => {
        const oi = orig.tgt.indexOf(t);
        if (oi >= 0 && orig.items[orig.a[oi]] !== q.items[q.a[i]])
          bad.push(`#${orig.n} dd 配對錯位：「${t.slice(0,20)}」`);
      });
      if (orig.fix && JSON.stringify(q.tgt) !== JSON.stringify(orig.tgt))
        bad.push(`#${orig.n} dd fix:true 但答案區被洗了`);
    }

    if (k === "dl") {
      q.dd.forEach((list, g) => {
        if (list[q.a[g]] !== orig.dd[g][orig.a[g]])
          bad.push(`#${orig.n} dl 第 ${g + 1} 格答案錯位`);
        if (q.en && q.en.dd && q.en.dd[g]) list.forEach((t, i) => {
          const oi = orig.dd[g].indexOf(t);
          if (oi >= 0 && orig.en.dd[g][oi] !== q.en.dd[g][i])
            bad.push(`#${orig.n} dl 第 ${g + 1} 格中英錯位`);
        });
      });
    }

    // 進度續作：帶回 _p 必須洗出一模一樣的結果
    const again = clone(orig);
    permute(again, q._p);
    for (const f of ["o", "s", "items", "tgt", "dd", "a", "ico"]) {
      if (q[f] && JSON.stringify(q[f]) !== JSON.stringify(again[f]))
        bad.push(`#${orig.n} 帶入 _p 沒有重播出相同的 ${f}（進度續作會錯位）`);
    }
  }
}

const icoQs = BANK.filter(q => q.ico);
console.log(`題數 ${BANK.length}　有服務圖示的題 ${icoQs.length}（${icoQs.map(q => "#" + q.n).join(", ") || "—"}）`);
if (bad.length) {
  const uniq = [...new Set(bad)];
  console.log(`\n洗牌不變式失敗 ${uniq.length} 項：`);
  uniq.slice(0, 20).forEach(m => console.log("  " + m));
  process.exit(1);
}
console.log("洗牌不變式全部通過（中英配對、答案索引、服務圖示、fix 不洗、_p 可重播）");
