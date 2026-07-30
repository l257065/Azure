const fs = require('fs');
/* 來源座標 sec+no（每一段題號都從 1 重新算，要兩格才認得出是哪一題）*/
const qid = q => (q.sec && Number.isFinite(q.no)) ? q.sec + "#" + q.no
                                                  : (q.t || String(q.q || "").slice(0, 18));

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
    if (hasNote && segs.length < 2) { console.log('!! ' + qid(q) + ' ' + tag + ' 前言後沒有題目'); bad++; }
    segs.slice(1).forEach(s => {
      if (isNote(s)) { console.log('!! ' + qid(q) + ' ' + tag + ' 前言不在第一段'); bad++; }
    });
  });
});

/* 排版預覽：樣本動態挑，不寫死題號（AZ-104 的題號與 AZ-900 不同）；
   題庫還沒收錄時整段跳過，骨架階段才不會爆掉。 */
const sampleZh = DOC.find(q => String(q.q).includes('\n')) || DOC[0];
if (sampleZh) {
  console.log('=== 排版預覽（中文，第 ' + sampleZh.n + ' 題）===');
  String(sampleZh.q).split('\n').map(s => s.trim()).filter(Boolean).forEach(s => {
    console.log('[' + (isNote(s) ? '前言 · 小字灰底' : '題目 · 粗體') + '] ' + stripHl(s));
  });

  const sampleEn = DOC.find(q => q.en && String(q.en.q).includes('\n')) || DOC[0];
  console.log('');
  console.log('=== 排版預覽（英文，第 ' + sampleEn.n + ' 題）===');
  String(sampleEn.en.q).split('\n').map(s => s.trim()).filter(Boolean).forEach(s => {
    console.log('[' + (isNote(s) ? 'note' : 'question') + '] ' + stripHl(s));
  });
} else {
  console.log('=== 排版預覽：文件題庫還沒有題目，跳過 ===');
}

const seg = DOC.map(q => String(q.q).split('\n').filter(s => s.trim()).length);
console.log('');
console.log('題幹段數分布：', JSON.stringify(seg.reduce((a, n) => (a[n] = (a[n] || 0) + 1, a), {})));
console.log(bad ? 'FAIL' : '分段檢查通過');
