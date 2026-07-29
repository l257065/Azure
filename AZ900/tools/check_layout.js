const fs = require('fs');
const src = fs.readFileSync(process.argv[2], 'utf8');
const DOC = eval('[' + src.match(/const BANK_DOC = \[([\s\S]*?)\n\];/)[1] + ']');
const stripHl = s => String(s).replace(/⟦([^⟧]*)⟧/g, '$1');
const isNote = s => /^(注意：|Note:|（原題|（原始|\(The |DRAG DROP)/.test(stripHl(s));

let bad = 0;
DOC.forEach(q => {
  [['中', q.q], ['EN', q.en.q]].forEach(([tag, text]) => {
    const segs = String(text).split('\n').map(s => s.trim()).filter(Boolean);
    // 有前言的題目，前言必須自成一段，且後面還要有真正的題目
    const hasNote = isNote(segs[0]);
    if (hasNote && segs.length < 2) { console.log('!! #' + q.n + ' ' + tag + ' 前言後沒有題目'); bad++; }
    segs.slice(1).forEach(s => {
      if (isNote(s)) { console.log('!! #' + q.n + ' ' + tag + ' 前言不在第一段'); bad++; }
    });
  });
});

console.log('=== 排版預覽（中文，第 18 題）===');
const q18 = DOC.find(q => q.n === 18);
String(q18.q).split('\n').map(s => s.trim()).filter(Boolean).forEach(s => {
  console.log('[' + (isNote(s) ? '前言 · 小字灰底' : '題目 · 粗體') + '] ' + stripHl(s));
});

console.log('');
console.log('=== 排版預覽（英文，第 20 題）===');
const q20 = DOC.find(q => q.n === 20);
String(q20.en.q).split('\n').map(s => s.trim()).filter(Boolean).forEach(s => {
  console.log('[' + (isNote(s) ? 'note' : 'question') + '] ' + stripHl(s));
});

const seg = DOC.map(q => String(q.q).split('\n').filter(s => s.trim()).length);
console.log('');
console.log('題幹段數分布：', JSON.stringify(seg.reduce((a, n) => (a[n] = (a[n] || 0) + 1, a), {})));
console.log(bad ? 'FAIL' : '分段檢查通過');
