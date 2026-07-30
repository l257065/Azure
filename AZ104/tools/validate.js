// AZ104 題庫驗證。仿照 AZ900/tools/validate.js 的精神，驗證兩份獨立題庫
// （bank_az104.current.js = BANK_MINE 自製題庫、bank_doc.current.js = BANK_DOC 文件題庫，
// 見 AZ104-SPEC.md 第 5 節），並新增輕量 markdown（**／`／```）成對檢查——這是解析支援
// mdHtml() 之後才需要的，標記沒成對就會在畫面上字面顯示，見 az900-practice.html 的 mdHtml() 註解。
// usage: node tools/validate.js
const path = require('path');
const { BANK_AZ104 } = require(path.join(__dirname, 'bank_az104.current.js'));
const { BANK_DOC } = require(path.join(__dirname, 'bank_doc.current.js'));

const HL_RE = /⟦([^⟧]*)⟧/g;
const stripHl = s => String(s).replace(HL_RE, '$1');
const kindOf = q => q.k || 'mc';
const qid = q => q.code || ('#' + q.n);

let bad = 0;
const fail = msg => { console.log(msg); bad++; };

function validateBank(label, bank) {
  bank.forEach(q => {
    const k = kindOf(q);
    if (!q.n || !q.q || !q.a || !q.en) fail(label + ' 缺欄位 ' + qid(q));
    if (!q.e || !q.e.trim()) fail(label + ' 缺中文解析 ' + qid(q));
    if (!q.en.e || !q.en.e.trim()) fail(label + ' 缺英文解析 ' + qid(q));
    /* 分頁桶只能是 1-3（見 AZ104-SPEC.md §5），Quiz1 曾經誤填官方 od 的 1-5 導致成績單分頁加總對不起來 */
    if (!Number.isInteger(q.d) || q.d < 1 || q.d > 3) fail(label + ' d 只能是 1-3 ' + qid(q) + ' d=' + q.d);

    /* 各題型的必要欄位、中英對應與答案範圍 */
    if (k === 'mc') {
      if (!q.o || !q.en.o) { fail(label + ' 單複選缺選項 ' + qid(q)); return; }
      if (q.en.o.length !== q.o.length) fail(label + ' 中英選項數不符 ' + qid(q));
      if (q.a.some(x => x < 0 || x >= q.o.length)) fail(label + ' 索引越界 ' + qid(q));
      if (!q.a.length) fail(label + ' 沒有正解 ' + qid(q));
    } else if (k === 'hs') {
      if (!q.s || !q.en.s) { fail(label + ' 是非表缺敘述 ' + qid(q)); return; }
      if (q.en.s.length !== q.s.length) fail(label + ' 中英敘述數不符 ' + qid(q));
      if (q.a.length !== q.s.length) fail(label + ' 答案數與敘述數不符 ' + qid(q));
      if (q.a.some(v => v !== 0 && v !== 1)) fail(label + ' 是非答案只能是 0 或 1 ' + qid(q));
    } else if (k === 'dd') {
      if (!q.items || !q.tgt || !q.en.items || !q.en.tgt) { fail(label + ' 配對題缺欄位 ' + qid(q)); return; }
      if (q.en.items.length !== q.items.length) fail(label + ' 中英項目數不符 ' + qid(q));
      if (q.en.tgt.length !== q.tgt.length) fail(label + ' 中英答案區數不符 ' + qid(q));
      if (q.a.length !== q.tgt.length) fail(label + ' 答案數與答案區數不符 ' + qid(q));
      if (q.a.some(v => v < 0 || v >= q.items.length)) fail(label + ' 配對索引越界 ' + qid(q));
    } else if (k === 'dl') {
      if (!q.sent || !q.dd || !q.en.sent || !q.en.dd) { fail(label + ' 下拉題缺欄位 ' + qid(q)); return; }
      if (q.en.dd.length !== q.dd.length) fail(label + ' 中英下拉格數不符 ' + qid(q));
      q.dd.forEach((list, g) => {
        if (!q.en.dd[g] || q.en.dd[g].length !== list.length) fail(label + ' 第 ' + (g + 1) + ' 格中英選項數不符 ' + qid(q));
      });
      if (q.a.length !== q.dd.length) fail(label + ' 答案數與下拉格數不符 ' + qid(q));
      if (q.a.some((v, g) => v < 0 || v >= q.dd[g].length)) fail(label + ' 下拉索引越界 ' + qid(q));
      /* 句子裡的 {n} 要和 dd 的格數對得上，否則會有下拉畫不出來 */
      [['中', q.sent], ['EN', q.en.sent]].forEach(([tag, s]) => {
        const got = (String(s).match(/\{(\d+)\}/g) || []).map(m => +m.slice(1, -1)).sort((a, b) => a - b);
        const want = q.dd.map((_, i) => i);
        if (got.join() !== want.join()) fail(label + ' 挖空編號與下拉格數不符 ' + qid(q) + ' ' + tag + ' → ' + JSON.stringify(got));
      });
    } else {
      fail(label + ' 未知題型 ' + k + ' ' + qid(q));
    }

    /* 螢光筆標記必須成對 */
    [q.q, q.e, q.en.q, q.en.e, q.sent, q.en.sent]
      .concat(q.s || [], q.en.s || [], q.tgt || [], q.en.tgt || [])
      .forEach((s, i) => {
        if (s === undefined) return;
        const a = (String(s).match(/⟦/g) || []).length;
        const b = (String(s).match(/⟧/g) || []).length;
        if (a !== b) fail(label + ' 螢光筆標記不成對 ' + qid(q) + ' 欄位' + i);
      });

    /* 可以「選」的東西絕不能帶螢光筆標記（會洩題）。
       是非表的敘述、配對題答案區的描述屬於題幹，可以標。 */
    (q.o || []).concat(q.en.o || [], q.items || [], q.en.items || [],
                       (q.dd || []).flat(), (q.en.dd || []).flat())
      .forEach(o => { if (/⟦|⟧/.test(o)) fail(label + ' !! 選項帶螢光筆標記 ' + qid(q)); });

    /* 輕量 markdown（見 az900-practice.html 的 mdHtml()）：**／`／``` 沒成對，畫面上就會字面顯示。
       mdHtml() 對落單的標記不做任何處理，所以只能在這裡擋。只查題幹與解析，選項不會走 mdHtml。 */
    [['q', q.q], ['e', q.e], ['en.q', q.en.q], ['en.e', q.en.e]].forEach(([lab, v]) => {
      if (typeof v !== 'string') return;
      const fence = (v.match(/```/g) || []).length;
      if (fence % 2) fail(label + ' ``` 沒成對 ' + qid(q) + ' ' + lab + '（' + fence + ' 個）');
      const bold = (v.match(/\*\*/g) || []).length;
      if (bold % 2) fail(label + ' ** 沒成對 ' + qid(q) + ' ' + lab + '（' + bold + ' 個）');
      /* 反引號要成對，但程式碼區塊裡的內容不算（PowerShell 的續行符號本身就是反引號） */
      const outside = v.replace(/```[\s\S]*?```/g, '');
      const tick = (outside.match(/`/g) || []).length;
      if (tick % 2) fail(label + ' 行內反引號沒成對 ' + qid(q) + ' ' + lab + '（' + tick + ' 個）');
    });
  });

  const kinds = bank.reduce((a, q) => (a[kindOf(q)] = (a[kindOf(q)] || 0) + 1, a), {});
  const hlZh = bank.reduce((n, q) => n + (String(q.q + (q.sent || '')).match(/⟦/g) || []).length, 0);
  const hlEn = bank.reduce((n, q) => n + (String(q.en.q + (q.en.sent || '')).match(/⟦/g) || []).length, 0);
  console.log(label + ':', bank.length, '題');
  console.log('　題型分布：', JSON.stringify(kinds), '（mc 單複選 / hs 是非表 / dd 配對拖放 / dl 下拉）');
  console.log('　題幹螢光筆標記：中文', hlZh, '處　英文', hlEn, '處');

  const lens = bank.map(q => stripHl(q.e).length);
  console.log('　中文解析長度： 最短', Math.min(...lens), '　最長', Math.max(...lens),
              '　平均', Math.round(lens.reduce((a, b) => a + b, 0) / lens.length));
}

validateBank('BANK_MINE（自製題庫／bank_az104.current.js）', BANK_AZ104);
validateBank('BANK_DOC（文件題庫／bank_doc.current.js）', BANK_DOC);

/* 兩份題庫各自獨立記分，但 n 值不需要跨題庫唯一（見 sigOf()／wrongSet 用 q.q 文字當鍵，不是 n），
   這裡只提醒一下，不是錯誤：*/
console.log(bad ? 'FAIL（' + bad + ' 項）' : '全部檢查通過');
process.exit(bad ? 1 : 0);
