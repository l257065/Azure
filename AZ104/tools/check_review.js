const fs = require('fs');
const src = fs.readFileSync(process.argv[2], 'utf8');
const DOC = eval('[' + src.match(/const BANK_DOC = \[([\s\S]*?)\n\];/)[1] + ']');
const MINE = eval('[' + src.match(/const BANK_MINE = \[([\s\S]*?)\n\];/)[1] + ']');
const LETTER = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"];
const kindOf = q => q.k || "mc";
const stripHl = s => String(s).replace(/⟦([^⟧]*)⟧/g, '$1');

// 重現 finishRound 裡逐題檢討的選項狀態判定
function review(q, mine, EN) {
  const o = EN ? q.en.o : q.o;
  return o.map((text, oi) => {
    const isAns = q.a.includes(oi), isMine = mine.includes(oi);
    const cls = isAns ? (isMine ? "ok" : "miss") : (isMine ? "bad" : "none");
    const tag = isAns
      ? (isMine ? (EN ? "✓ correct · your pick" : "✓ 正解 · 你選的")
                : (EN ? "✓ correct answer" : "✓ 正解"))
      : (isMine ? (EN ? "✗ your pick" : "✗ 你選的") : "");
    return { L: LETTER[oi], cls, tag, text: stripHl(text) };
  });
}

const LABEL = { ok: "綠底實線", miss: "綠底虛線", bad: "紅底", none: "灰淡" };

/* 情境 1–4 的樣本動態挑；題庫還沒收錄時跳過，骨架階段才不會爆掉。 */
const mcOf = bank => bank.find(q => kindOf(q) === "mc" && q.o && q.o.length >= 2);
const q8 = mcOf(DOC);
if (q8) {
  console.log("=== 情境 1：文件題庫第 " + q8.n + " 題，你選 A，正解 " + LETTER[q8.a[0]] + " ===");
  review(q8, [0], false).forEach(r =>
    console.log(`  ${r.L}  [${LABEL[r.cls].padEnd(5)}] ${r.text}  ${r.tag}`));
}

const q4 = MINE.find(q => kindOf(q) === "mc" && q.o && q.o.length === 4 && q.a.length === 1);
if (q4) {
  console.log("\n=== 情境 2：四選一，你選 C，正解 " + LETTER[q4.a[0]] + "（自製題庫）===");
  const wrongPick = [0, 1, 2, 3].find(i => i !== q4.a[0]);
  review(q4, [wrongPick], false).forEach(r =>
    console.log(`  ${r.L}  [${LABEL[r.cls].padEnd(5)}] ${r.text.slice(0, 30)}  ${r.tag}`));
}

const qm = DOC.concat(MINE).find(q => kindOf(q) === "mc" && q.a.length === 2);
if (qm) {
  console.log("\n=== 情境 3：複選題答對一半（需選 2 項）===");
  review(qm, [qm.a[0]], false).forEach(r =>
    console.log(`  ${r.L}  [${LABEL[r.cls].padEnd(5)}] ${r.text.slice(0, 30)}  ${r.tag}`));
}

if (q8) {
  console.log("\n=== 情境 4：未作答（模擬考跳過）===");
  review(q8, [], false).forEach(r =>
    console.log(`  ${r.L}  [${LABEL[r.cls].padEnd(5)}] ${r.text}  ${r.tag}`));
}

if (!q8 && !q4) console.log("=== 成績單狀態預覽：兩份題庫都還沒有題目，跳過 ===");

// 檢查：單複選題一定要有恰好 q.a.length 個綠色
let bad = 0;
DOC.concat(MINE).filter(q => kindOf(q) === "mc").forEach(q => {
  const rs = review(q, [0], false);
  const greens = rs.filter(r => r.cls === "ok" || r.cls === "miss").length;
  if (greens !== q.a.length) { console.log("!! 綠色數量不符", q.n || q.q.slice(0, 20)); bad++; }
});
console.log("\n單複選題的正解標示數量正確:", bad ? "FAIL" : "OK");

/* 原廠題型：逐格作答，全部格子都對才算這一題答對 */
const YN = v => v === 1 ? "是" : v === 0 ? "否" : "—";
const hs = DOC.find(q => kindOf(q) === "hs");
if (hs) {
  console.log("\n=== 情境 5：是非表（第 " + hs.n + " 題），第一句故意選反 ===");
  const mine = hs.a.map((v, i) => i === 0 ? (v ? 0 : 1) : v);
  hs.s.forEach((t, i) => console.log("  [" + (mine[i] === hs.a[i] ? "✓" : "✗") + "] " +
    stripHl(t).slice(0, 32) + "　你:" + YN(mine[i]) + " / 正解:" + YN(hs.a[i])));
  console.log("  → 整題判定：" + (mine.every((v, i) => v === hs.a[i]) ? "答對" : "答錯（有一格不符）"));
}
const dd = DOC.find(q => kindOf(q) === "dd");
if (dd) {
  console.log("\n=== 情境 6：配對拖放（第 " + dd.n + " 題），全部答對 ===");
  console.log("  可拖曳項目：" + dd.items.map(stripHl).join(" ｜ "));
  dd.tgt.forEach((t, i) => console.log("  [✓] " + stripHl(t).slice(0, 32) + "　→ " + stripHl(dd.items[dd.a[i]])));
}
const dl = DOC.find(q => kindOf(q) === "dl" && q.dd.length > 1);
if (dl) {
  console.log("\n=== 情境 7：多格下拉（第 " + dl.n + " 題），填入正解 ===");
  console.log("  " + stripHl(dl.sent)
    .replace(/\{(\d+)\}/g, (m, g) => "［" + stripHl(dl.dd[+g][dl.a[+g]]) + "］")
    .replace(/\n/g, "\n  "));
}
let bad2 = 0;
DOC.filter(q => kindOf(q) !== "mc").forEach(q => {
  const n = kindOf(q) === "hs" ? q.s.length : kindOf(q) === "dd" ? q.tgt.length : q.dd.length;
  if (q.a.length !== n) { console.log("!! 逐格答案數不符 #" + q.n); bad2++; }
});
console.log("\n原廠題型的逐格答案數正確:", bad2 ? "FAIL" : "OK");
