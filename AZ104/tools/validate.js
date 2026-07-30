const fs = require('fs');
const src = fs.readFileSync(process.argv[2], 'utf8');
const MINE = eval('[' + src.match(/const BANK_MINE = \[([\s\S]*?)\n\];/)[1] + ']');
const DOC = eval('[' + src.match(/const BANK_DOC = \[([\s\S]*?)\n\];/)[1] + ']');

const HL_RE = /⟦([^⟧]*)⟧/g;
const stripHl = s => String(s).replace(HL_RE, '$1');
const kindOf = q => q.k || 'mc';

let bad = 0;
const fail = msg => { console.log(msg); bad++; };
/* 題目的來源座標：sec（"S1"／"T3"／"NewQ"）+ no（文件上印的 Question #）。
   每一段的題號都從 1 重新算，所以要兩格才認得出是哪一題。 */
const qid = q => (q.sec && Number.isFinite(q.no)) ? q.sec + "#" + q.no
                                                  : (q.t || String(q.q || "").slice(0, 18));

DOC.forEach(q => {
  const k = kindOf(q);
  if (!q.sec || !Number.isFinite(q.no)) fail('缺來源座標 sec/no：' + qid(q));
  if (!q.q || !q.a || !q.en) fail('缺欄位 ' + qid(q));
  if (!q.e || !q.e.trim()) fail('缺中文解析 ' + qid(q));
  if (!q.en.e || !q.en.e.trim()) fail('缺英文解析 ' + qid(q));

  /* 各題型的必要欄位、中英對應與答案範圍 */
  if (k === 'mc') {
    if (!q.o || !q.en.o) { fail('單複選缺選項 ' + qid(q)); return; }
    if (q.en.o.length !== q.o.length) fail('中英選項數不符 ' + qid(q));
    if (q.a.some(x => x < 0 || x >= q.o.length)) fail('索引越界 ' + qid(q));
    if (!q.a.length) fail('沒有正解 ' + qid(q));
  } else if (k === 'hs') {
    if (!q.s || !q.en.s) { fail('是非表缺敘述 ' + qid(q)); return; }
    if (q.en.s.length !== q.s.length) fail('中英敘述數不符 ' + qid(q));
    if (q.a.length !== q.s.length) fail('答案數與敘述數不符 ' + qid(q));
    if (q.a.some(v => v !== 0 && v !== 1)) fail('是非答案只能是 0 或 1 ' + qid(q));
  } else if (k === 'dd') {
    if (!q.items || !q.tgt || !q.en.items || !q.en.tgt) { fail('配對題缺欄位 ' + qid(q)); return; }
    if (q.en.items.length !== q.items.length) fail('中英項目數不符 ' + qid(q));
    if (q.en.tgt.length !== q.tgt.length) fail('中英答案區數不符 ' + qid(q));
    if (q.a.length !== q.tgt.length) fail('答案數與答案區數不符 ' + qid(q));
    if (q.a.some(v => v < 0 || v >= q.items.length)) fail('配對索引越界 ' + qid(q));
  } else if (k === 'dl') {
    if (!q.sent || !q.dd || !q.en.sent || !q.en.dd) { fail('下拉題缺欄位 ' + qid(q)); return; }
    if (q.en.dd.length !== q.dd.length) fail('中英下拉格數不符 ' + qid(q));
    q.dd.forEach((list, g) => {
      if (!q.en.dd[g] || q.en.dd[g].length !== list.length) fail('第 ' + (g + 1) + ' 格中英選項數不符 ' + qid(q));
    });
    if (q.a.length !== q.dd.length) fail('答案數與下拉格數不符 ' + qid(q));
    if (q.a.some((v, g) => v < 0 || v >= q.dd[g].length)) fail('下拉索引越界 ' + qid(q));
    /* 句子裡的 {n} 要和 dd 的格數對得上，否則會有下拉畫不出來 */
    [['中', q.sent], ['EN', q.en.sent]].forEach(([tag, s]) => {
      const got = (String(s).match(/\{(\d+)\}/g) || []).map(m => +m.slice(1, -1)).sort((a, b) => a - b);
      const want = q.dd.map((_, i) => i);
      if (got.join() !== want.join()) fail('挖空編號與下拉格數不符 ' + qid(q) + ' ' + tag + ' → ' + JSON.stringify(got));
    });
  } else {
    fail('未知題型 ' + k + ' ' + qid(q));
  }

  /* 標記必須成對 */
  [q.q, q.e, q.en.q, q.en.e, q.sent, q.en.sent]
    .concat(q.s || [], q.en.s || [], q.tgt || [], q.en.tgt || [])
    .forEach((s, i) => {
      if (s === undefined) return;
      const a = (String(s).match(/⟦/g) || []).length;
      const b = (String(s).match(/⟧/g) || []).length;
      if (a !== b) fail('標記不成對 ' + qid(q) + ' 欄位' + i);
    });

  /* 可以「選」的東西絕不能帶標記（會洩題）。
     是非表的敘述、配對題答案區的描述屬於題幹，可以標。 */
  (q.o || []).concat(q.en.o || [], q.items || [], q.en.items || [],
                     (q.dd || []).flat(), (q.en.dd || []).flat())
    .forEach(o => { if (/⟦|⟧/.test(o)) fail('!! 選項帶螢光筆標記 ' + qid(q)); });
});

const kinds = DOC.reduce((a, q) => (a[kindOf(q)] = (a[kindOf(q)] || 0) + 1, a), {});
const hlZh = DOC.reduce((n, q) => n + (String(q.q + (q.sent || '')).match(/⟦/g) || []).length, 0);
const hlEn = DOC.reduce((n, q) => n + (String(q.en.q + (q.en.sent || '')).match(/⟦/g) || []).length, 0);
console.log('題庫 A:', MINE.length, '題（無標記）　題庫 B:', DOC.length, '題');
console.log('題型分布：', JSON.stringify(kinds), '（mc 單複選 / hs 是非表 / dd 配對拖放 / dl 下拉）');
console.log('題幹螢光筆標記：中文', hlZh, '處　英文', hlEn, '處');

const noHl = DOC.filter(q => !/⟦/.test(String(q.q) + (q.sent || '') + (q.tgt || []).join('') + (q.s || []).join('')));
console.log('題幹完全沒標記的題目:', noHl.length
  ? noHl.length + ' 題（' + noHl.slice(0, 12).map(q => qid(q)).join(',') + (noHl.length > 12 ? '…' : '') + '）'
  : '無');

const lens = DOC.map(q => stripHl(q.e).length);
console.log('中文解析長度： 最短', Math.min(...lens), '　最長', Math.max(...lens),
            '　平均', Math.round(lens.reduce((a, b) => a + b, 0) / lens.length));
console.log('含條列（含「・」）的解析:', DOC.filter(q => q.e.includes('・')).length, '/', DOC.length);
console.log(bad ? 'FAIL（' + bad + ' 項）' : '全部檢查通過');
process.exit(bad ? 1 : 0);
