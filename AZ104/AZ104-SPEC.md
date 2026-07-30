# AZ-104 練習頁 — 規格與交接文件

參考 `AZ900/AZ900-SPEC.md` 的做法改寫，讓任何一個新的 session 能接手繼續轉錄題庫。
**讀完這份就能直接動工，不需要回頭問前一個 session。**

---

## 1. 這是什麼

單一檔案的 AZ-104 練習網頁：`az104-practice.html`（純本機自用，不上 GitHub、不連外）。

沿用 AZ900 的練習引擎（洗牌、四種題型、成績單、進度續作等）。跟 AZ900 一樣，**裡面有兩份完全獨立的題庫**，
頂列可切換（進度、統計、星號、錯題本各自獨立）：

| 代號 | UI 標籤 | 來源 | 題數 |
|---|---|---|---|
| `BANK_MINE`（`bank_az104.current.js`） | 自製題庫 | Build School 課程「AZ104 Azure 系統管理員認證練習題庫」的多個測驗頁（LearnDash `wpProQuiz`），逐頁另存 HTML 轉錄 | 372（進行中，見第 2 節） |
| `BANK_DOC`（`bank_doc.current.js`） | 文件題庫 | PDF 考古題逐題轉錄，Question Set 1（`sec:"S1"`），欄位含 `sec`/`no` 標示原始文件位置 | 40（已完成） |

（UI 標籤沿用 AZ900 的「自製／文件」命名，但跟 AZ900 的語意不完全對應——AZ104 的「自製題庫」也是
逐頁轉錄自 Build School 網站，不是真的自行編寫；純粹是兩個題庫槽位的代稱，不影響任何功能。）

`BANK_MINE` 這邊：

| 項目 | 說明 |
|---|---|
| 來源 | Build School 課程「AZ104 Azure 系統管理員認證練習題庫」的**多個測驗頁**（LearnDash `wpProQuiz`），使用者逐頁另存為 HTML |
| 題目呈現 | 兩種都有，逐卷不同，見第 3 節：一種選項/正解直接在 HTML 裡（免看圖）、一種只有一張答案截圖要看圖還原 |
| 進度單位 | 一次一個 quiz 分卷（quiz1~quiz19、quiz20），每卷各自 15～42 題 |

已確認**全套課程共 20 卷、748 題，題號連續無跳號**（AZ104-Q1 ~ Q748，quiz1 是 Q1~Q40，quiz20 是 Q712~Q748）。

---

## 2. 目前進度（2026-07-30，本次交接重點）

**已完成 10 卷、共 372 題**，寫在 `tools/bank_az104.current.js` 的 `BANK_AZ104`，已組出可直接用瀏覽器開啟的 `az104-practice.html`：

| 卷 | 題號範圍 | 題數 | 狀態 |
|---|---|---|---|
| Quiz1 | Q1～Q40 | 40 | ✅ 已完成 |
| Quiz2 | Q41～Q80 | 40 | ✅ 已完成 |
| Quiz3 | Q81～Q120 | 40 | ✅ 已完成 |
| Quiz4 | Q121～Q160 | 40 | ✅ 已完成 |
| Quiz5 | Q161～Q200 | 40 | ✅ 已完成 |
| Quiz6 | Q201～Q215 | 15 | ✅ 已完成 |
| Quiz7～Quiz9 | Q216～Q322 | 107 | ⛔ **跳過，見下方說明** |
| Quiz10 | Q323～Q362 | 40 | ✅ 已完成 |
| Quiz11 | Q363～Q402 | 40 | ✅ 已完成 |
| Quiz12 | Q403～Q442 | 40 | ✅ 已完成，jsdom 全量驗證通過（372 題、0 error） |
| Quiz13～Quiz19 | Q443～Q711 | 268 | ⬜ 已取得來源 HTML（`source/quizN.html`），尚未轉錄 |
| Quiz20 | Q712～Q748 | 37 | ✅ 已完成 |

**Quiz7～Quiz9 為什麼跳過**：使用者在對話中明確說「Quiz7~Quiz9 有問題，直接跳過，從 Quiz10 開始」。
這個判斷是在**被壓縮掉、目前看不到的對話段落**裡做的，交接時**不要花時間回去重跑 Quiz7~Quiz9 或
猜測問題出在哪**，除非使用者之後主動要求重新處理。`source/quiz7_questions.json`～`quiz9_questions.json`
可能已經存在（是舊版 extract_quiz.py 擷取的，欄位可能不全，見第 4-2 節「拿到新分卷」的做法，
真的要重做記得先用**目前版本**的 `extract_quiz.py` 重新擷取一次）。

**使用者的排程指示**：「照順序一卷一卷做，每次對話處理一卷」，後來又放寬成「直接做到 Quiz4」
（一次做完好幾卷），現在最新的指示是**每完成一卷就自行評估 session／context 使用量，接近上限就
把交接狀態寫進本文件，讓新 session 接手**——也就是現在這個做法。**新 session 接手時：不用再問
使用者要怎麼排程，直接照這份交接記錄的「下一步」繼續做 Quiz11 即可**，除非使用者又給新指示。

**Git 狀態**：`.gitignore` 已比照 AZ900 加了 AZ104 的白名單例外（`AZ104-SPEC.md`、
`az104-practice.html`、`tools/extract_quiz.py`／`build_practice_html.js`／`merge_batch.js`），
**`bank_az104.current.js` 與 `batch_quizN.js` 系列刻意不追蹤**（同 AZ900 慣例，資料可以從
`az104-practice.html` 反查）。2026-07-30 已經 commit 並 push 過一次（含 Quiz1~6、Quiz20，
commit message「新增 AZ104 練習頁初版(Quiz1~6、Quiz20 共 252 題)」）。**Quiz10 合併之後
的這次改動（292 題）截至本次交接時還沒有 commit**，新 session 接手時如果使用者要求 commit/push，
記得比照第一次的做法（`git add AZ104/ ; git status` 先確認只有白名單檔案被加入，再 commit）。

題號是課程站台自己編的連續流水號（`AZ104-Q<n>`），不是官方考試題號，純粹用來對照原始出處。
**資料裡 `n` 欄位存的是純數字部份**（例如 `21`），`AZ104-Q` 前綴另外存在 `code` 欄位——這是為了
相容 AZ900 引擎裡所有假設 `n` 是數字的邏輯（跳題、缺號檢查、成績單顯示「第 N 題」等），見第 5 節。

**分類標籤「這屬自製題庫」的說明**：使用者曾在對話中提過這句，經確認**不需要更動現有架構**——
題庫變數名稱維持 `BANK_AZ104`（內部仍別名成 `BANK_DOC` 給引擎用），UI 標籤維持「Quiz20 題庫」，
不要因為這句話去改架構或改名，除非使用者再次明確要求。

---

## 3. 來源網頁的長相（兩種格式，逐卷不同）

共通點：
- 網址型式：`https://learn.build-school.com/zh-hant/courses/az104-.../quizzes/az104-quizN/`
- 課程用 WordPress + LearnDash + WpProQuiz 外掛，每卷一頁
- 題幹在 `<legend class="wpProQuiz_question_text">` 底下，一行一個 `<div>`，可以直接抓純文字
- 題幹前面通常有 `AZ104-Qnnn` 這個課程自己的流水號（有些卷包在 `<strong>` 裡，有些直接混在第一行文字裡）
- 每題有一個「類別（`類別：<span>...</span>`）」欄位，**這是官方 AZ-104 技能領域的英文名稱**
  （例如 `Manage Azure identities and governance`），比自己判斷準，優先拿來對應 `od`（見第 5 節）

**格式 A：`data-type="single"` / `data-type="multiple"`（Quiz1 用的是這種）**
- 介面是真的選擇題，`wpProQuiz_questionListItem` 底下每個選項都有實際文字
- 正解直接用 class 標記：該選項的 class 含 `wpProQuiz_answerCorrect`（單選是 `wpProQuiz_answerCorrectIncomplete`，複選也是同一個字串出現在每個正解選項上）
- 很多題目 `wpProQuiz_AnswerMessage` 裡已經有現成的英文解析（含 `Reference:` 連結），品質不一，有時完整有時只有連結
- **不需要看截圖就能轉錄**：選項、正解、解析都能直接從 HTML 抓到，Python 腳本全自動化，人只需要翻譯＋補強解析
- 少數題目的題幹裡有 `<img>`（多半是情境用的使用者/資源表格截圖），這種要另外看圖確認情境細節

**格式 B：`data-type="free_answer"`（Quiz20 用的是這種）**
- 介面永遠是一個停用的輸入框「See answer below」，**沒有任何可讀的選項文字**
- 點「檢查」固定判「不正確」，顯示一張答案截圖（`xxx_ans.png` 或 `rIdNN.jpg`），選項／正解／配對關係全部要看圖還原
- `wpProQuiz_AnswerMessage` 裡通常沒有解析文字（Explanation 後面是空的），要靠 Azure 知識自己寫

**兩種格式怎麼判斷**：`extract_quiz.py` 已經自動判斷並在輸出的 `raw_type` 欄位標出來
（`single`／`multiple`／`free_answer`），也會印出 `by raw_type` 統計。拿到新分卷先跑一次擷取，
看 `by raw_type` 就知道這卷是哪種、要不要看圖。

---

## 4. 工作流程

### 4-1. 取得新的分卷

**quiz1~quiz20 全部 20 卷的來源 HTML 使用者都已經另存好並給過了**，在 `AZ104/source/quizN.html`
＋`AZ104/source/quizN_files/`（quiz1 的資料夾名稱比較特殊，含逗號，複製時注意）。
之後不需要再跟使用者要檔案，除非要重新整份重存。

### 4-2. 抽出題幹（options／正解／解析／inline 圖片都會一起抽出來）

```bash
cd AZ104/tools
python extract_quiz.py ../source/quizN.html ../source/quizN_questions.json
```

輸出每一題的 `code`／`qnum`／`qtotal`／`raw_type`／`category`／`question`／`inline_images`／
`answer_images`／`explanation`，格式 A 的題目還會多一個 `options: [{text, correct}, ...]`。
跑完看終端機印出的 `by raw_type` 與 `WARNING no option marked correct`（有警告要先查清楚，
不要忽略）。

### 4-3. 轉錄

- **格式 A**：把 `quizN_questions.json` 的 `question`／`options`／`category`／`explanation` 直接
  當底稿，翻成中文（風格見第 7 節），`options` 裡 `correct:true` 的就是 `a[]`；`category` 對應 `od`
  （見第 5 節）；`explanation` 有內容就順著它的論點寫、擴充成完整解析，全空的話就靠 Azure 知識自己寫。
  若 `inline_images` 非空，要用 Read 工具看一下確認情境細節（通常是使用者/資源對照表）。
- **格式 B**：跟 Quiz20 的做法一樣，用 Read 工具看 `answer_images` 裡的截圖，逐題判斷題型
  （`mc`／`hs`／`dd`／`dl`，見第 6 節）與正解，選項/題幹翻成中文，解析靠 Azure 知識寫。
  一次讀 3–5 張圖比較不會爆 context。

### 4-4. 寫成 batch 檔、合併進題庫

跟 AZ900 用 `append.py`/`splice.py` 分開改來源檔／灌回 HTML 不同，AZ104 用兩支自己的腳本：

```bash
# 1. 把這一卷的新題目寫成 tools/batch_quizN.js（格式照現有 batch_quiz1.js 抄，
#    const BATCH_QUIZN = [ {...}, {...} ]; module.exports 那行照抄）
# 2. 合併進 bank_az104.current.js（插在 const BANK_AZ104 = [ 後面）
node tools/merge_batch.js tools/batch_quizN.js BATCH_QUIZN
# 3. 重新組出 az104-practice.html
node tools/build_practice_html.js
```

`merge_batch.js` 只是機械式地把 batch 陣列內容插進 `bank_az104.current.js`，不會做欄位檢查，
所以下一步驗證不可省略。

### 4-5. 驗證（每一卷都要做，別漏）

```bash
cd AZ104/tools
node --check bank_az104.current.js   # 語法
node validate.js                     # 資料完整性、中英對應、答案範圍、螢光筆與輕量 markdown 成對
```

`validate.js` 會擋：
- `o`/`items`/`s`/`dd` 的中英陣列長度不一致
- `a[]` 索引超出範圍
- 可選項目（`o`／`items`／`dd`）帶了 `⟦⟧` 螢光筆標記（洩題）
- `q`／`e`／`en.q`／`en.e` 留空、或 `⟦⟧` 沒成對
- **`d` 不是 1/2/3**（分頁桶，見第 5 節），不是官方 `od` 的 1–5——這是 Quiz1 那次真的犯過的錯
  （6 題誤填 `d:4`，靠事後跑迴圈統計每個 `d` 值的題數、加總跟 `BANK_AZ104.length` 對不起來才抓到）
- **輕量 markdown（`**`／`` ` ``／` ``` `）沒成對**（見第 9 節與 AZ900-SPEC.md §9-1b）：
  `mdHtml()` 對落單的標記不做任何處理，落單就會直接字面顯示在畫面上

還要手動做（`validate.js` 顧不到）：
- 用 jsdom 把整份 `az104-practice.html` 跑一次：載入無錯誤、新題目逐題「看答案」都有 verdict、
  分頁題數加總要等於題庫總數。範例見這次轉錄 Quiz1 時用的手法（讀 `az104-practice.html`、
  `new JSDOM(html, {runScripts:'dangerously', ...})`、跑 `jumpForm` 逐題跳＋`btnReveal`）。
  沒有真的瀏覽器可以測時，這是目前最接近的替代方案。

---

## 5. `BANK_AZ104` 資料格式

**與 AZ900 的 `BANK_DOC` 完全相同的 schema**，直接照抄 `AZ900-SPEC.md` 第 5 節：

- 省略 `k` = 單選／複選（`mc`），`o[]` + `a[]`
- `k:"hs"` = 多句是非，`s[]` + `a[]`（逐句 1/0）
- `k:"dd"` = 拖放配對／排序，`items[]` + `tgt[]` + `a[]`
- `k:"dl"` = 下拉選單，`sent` + `dd[][]` + `a[]`

補充欄位對照 AZ900：`n`（**純數字**，例如 `712`，等於課程流水號 `AZ104-Q712` 去掉前綴；
理由見第 2 節）、`code`（**AZ104 新增欄位**：完整流水號字串 `"AZ104-Q712"`，只作顯示／追溯用，
引擎不讀這個欄位）、`d`（**分頁用的領域桶，只能是 1/2/3**，見下）、`od`（**AZ104 新增欄位**：
對照官方五大技能領域的原始編號 1–5，見下）、`t`/`tEn`、`v0`（存這一題在來源截圖上的原始樣子，
方便日後核對，目前 37 題尚未補這個欄位）、`src`（**AZ104 新增欄位**：記錄是哪一卷、哪張截圖轉錄的，
例如 `"quiz20:118080_ans.png"`，因為 AZ104 沒有頁碼可查，只能靠這個回頭找原圖）。

### 為什麼 `d` 只有 1/2/3，不是官方的五大領域

AZ900 引擎的分頁 UI 是寫死的：分頁代碼 `0` 全部／`1`–`3` 三個領域／`4` 錯題本／`5` 星號題
（`4`、`5` 在程式碼裡被攔截成「錯題本」「星號題」，不會落到 `q.d===tab` 的一般過濾邏輯，
見 `az104-practice.html` 裡 `if(tab===4) return ...wrongSet...; if(tab===5) return ...starSet...;`
之後才是 `return BANK.filter(q=>q.d===tab)`）。所以**題庫的 `d` 欄位最多只能用到 3**，
官方 AZ-104 考綱的五大技能領域（見下表）在轉錄時先歸併成三個分頁桶：

| `d`（分頁桶） | 桶名稱 | 包含的官方領域（`od`） |
|---|---|---|
| `1` | 身分與治理 | `od=1` 身分識別與治理 |
| `2` | 儲存體與運算 | `od=2` 儲存體、`od=3` 運算資源 |
| `3` | 網路與維運 | `od=4` 虛擬網路、`od=5` 監視與維護 |

官方五大技能領域（`od` 欄位，只作標記與未來細分用，目前分頁 UI 不讀這個欄位）：

| `od` | 官方領域 |
|---|---|
| `1` | 管理 Azure 身分識別、governance、成本與治理 |
| `2` | 實作與管理儲存體 |
| `3` | 部署與管理 Azure 運算資源 |
| `4` | 設定與管理虛擬網路 |
| `5` | 監視與維護 Azure 資源 |

（若日後官方考綱調整，以 Microsoft Learn 上 AZ-104 的「Skills measured」頁面為準，回頭調整對照表。
若題庫成長到想要五個分頁而不是三個，要先改 `az104-practice.html` 裡 `TAB_ZH`/`TAB_EN` 陣列長度、
`nav.tabs` 的按鈕數量，並把錯題本／星號題的分頁代碼從 `4`/`5` 改成 `6`/`7`，見第 11 節待辦。）

**`category` → `od` 對照表**（來源 HTML 的「類別」欄位，目前看過的兩種文字）：

| 來源 `category` 文字 | `od` |
|---|---|
| `Manage Azure identities and governance` | `1` |
| `Implement and manage storage` | `2` |
| （其餘三個官方領域對應的英文 category 字串，等實際遇到再補進這張表） | `3`／`4`／`5` |

`category` 是 `None` 或沒有這個欄位時（Quiz20 那種 `free_answer` 卷就沒有），才需要自己依題目內容判斷。

---

## 6. 題型對應規則

**兩種來源格式各自的處理方式不同**（見第 3 節）：

- **格式 A**（`single`/`multiple`，Quiz1 這類）：全部轉成 `k`（省略）= `mc`。`single` 對應 `a` 只有
  一個索引，`multiple` 對應 `a` 有多個索引（引擎會自動顯示「需選 N 項」徽章，不用手動設定）。
  這種格式**目前沒遇過** `hs`/`dd`/`dl`，如果之後某一卷用格式 A 卻出現拖放/下拉題，代表 LearnDash
  用了別的 `data-type`（例如 `sort_answer`／`matrix_sort_answer`），`extract_quiz.py` 目前只認得
  `single`/`multiple`/`free_answer` 三種，遇到新的 `raw_type` 要先擴充腳本再轉錄。
- **格式 B**（`free_answer`，Quiz20 這類）：跟原本寫的一樣，要看答案截圖判斷實際題型。Quiz20 抽樣結果
  **37 題全部是 `free_answer` 包裝**，實際原題型全是「拖放配對」「排序」或「下拉選單選擇角色/服務」，
  沒有一題是純文字選擇題（純文字選擇題被格式 A 的卷用掉了，兩種格式在不同卷分開出現，不會混在同一卷）。

轉錄時比照 AZ900 第 6 節的判斷方式：
- 截圖裡如果是「左邊清單拖到右邊格子」→ `dd`
- 截圖裡如果是「句子挖空、選單選項」→ `dl`
- 截圖裡如果是「每一句各自 Yes/No」→ `hs`
- 截圖裡如果是「單選/複選清單打勾」→ `mc`

**洗牌規則沿用 AZ900 第 6 節同一張表**（`mc` 洗選項、`dd` 洗兩邊、`dl` 逐格洗、`fix:true` 的例外情形一樣適用）。

---

## 7. 中文翻譯風格

**直接沿用 AZ900-SPEC.md 第 7 節的定案寫法**，不重新制定：

| 不要這樣 | 要這樣 |
|---|---|
| 解決方案：你應該使用 X。 | 解法：使用 X。 |
| 此解決方案是否符合目標？ | 這個解法是否達成目標？ |
| 貴公司 / 你獲知 / 你的任務是 | 你的公司 / 你得知 / 你要 |

原則：**照意思翻，不照語序翻**；被動語態改主動；長句斷成短句。英文題幹完全照原文，不改寫
（Build School 的英文題幹本身就是照抄考古題，轉錄時原樣保留即可，只需把 OCR/排版造成的斷行黏回整句）。

---

## 8. 解析風格

**沿用 AZ900-SPEC.md 第 8 節全部原則**：整組列出可比較的選項／角色／方案、`\n` 分段、
配對題用「共用對照一次＋逐格重點」格式、`【…】` 小標必須與 `tgt` 逐字相等。

**AZ104 額外要求**：兩種來源格式待遇不同（見第 3 節）。格式 B（`free_answer`，Quiz20 這類）跟 AZ900
的 PDF 一樣完全沒有解析文字，**解析內容一律要靠 Azure 知識自行撰寫**，只有正確答案本身是從截圖忠實
轉錄。格式 A（`single`/`multiple`，Quiz1 這類）常常**已經有現成的英文解析**（`explanation` 欄位），
品質不一——有的完整（含推理與 Reference 連結），有的只剩一行 `Reference:` 加連結。轉錄時**以來源解析
的論點為底稿**去擴充改寫成中文（不是重新發明），來源解析太薄弱時再靠 Azure 知識補完整；不可以把來源
解析原文的架構完全丟掉、憑空重寫，避免跟原本的判斷理由脫節。連續同情境的解答系列題（`Note: This
question is part of a series...`，例如 AZ104-Q1~Q3、Q25~Q27）之間可以互相參照複用同一段情境說明，
不用每題都重複整段題幹翻譯，照 Quiz1 batch 檔裡 Q2/Q3、Q26/Q27 的寫法（開頭寫「情境同 Qn」）即可。

---

## 9. 螢光筆標記

沿用 AZ900-SPEC.md 第 9-1 節規則：`⟦…⟧` 只標題幹／`s[]`／`tgt[]`／`sent`，絕不標 `o`／`items`／`dd` 這些可選項目。

輕量 markdown：引擎的 `mdHtml()` 另外支援 `**粗體**`、`` `行內程式碼` ``、``` ``` 換行 區塊 ``` ```
（渲染成 `<pre class="code">`，保留縮排），詳見 AZ900-SPEC.md 第 9-1b 節。標記必須成對，落單會直接字面顯示。

服務圖示（`ico`）欄位：AZ104 的答案截圖若是入口網站畫面（服務清單、刀鋒選單），比照 AZ900 第 9-2 節，
優先直接從答案截圖裁切（`tools/icons_pdf.py` 的邏輯可以照搬，只是輸入源從 PDF 換成 PNG），
裁不到才用 `AZ900/Azure_Public_Service_Icons_V24/` 官方圖示包（授權範圍涵蓋 AZ104，同一包可共用）。

---

## 10. 檔案清單

```
az104-practice.html          主檔，可直接用瀏覽器開（由 tools/build_practice_html.js 組出來，不要手改）
AZ104-SPEC.md                本文件
source/
  quiz1.html ~ quiz20.html     20 卷原始存檔（路徑都已改指向對應的 quizN_files，quiz1 資料夾名稱特殊見 §4-1）
  quiz1_files/ ~ quiz20_files/ 各卷的圖片等素材
  quiz1_questions.json 等      各卷抽出的題幹/選項/正解/解析（extract_quiz.py 的輸出，尚未轉錄的卷也可以先跑抽取）
tools/
  extract_quiz.py              從任一 quizN.html 抽出題幹、選項、正解、解析、inline 圖片 → quizN_questions.json
                                （single/multiple 格式選項與正解直接抓 HTML；free_answer 格式只給答案截圖清單）
  bank_az104.current.js        BANK_MINE（自製題庫槽位）真實來源，const BANK_AZ104 = [...]
                                （改題庫改這個檔案，不要改 batch_*.js；build script 裡別名成 BANK_MINE）
  batch_quiz1.js                Quiz1 的轉錄批次檔（保留供追溯／參考格式，已合併進 bank_az104.current.js）
  merge_batch.js                把 batch_quizN.js 的陣列內容插進 bank_az104.current.js 的 BANK_AZ104 開頭
                                （usage: `node merge_batch.js batch_quizN.js BATCH_QUIZN`）
  bank_doc.current.js          BANK_DOC（文件題庫槽位）真實來源，const BANK_DOC = [...]。轉錄自
                                az104-skeleton 分支的 PDF 考古題 Question Set 1（40 題，`sec`/`no` 定位）
  validate.js                   驗證 bank_az104.current.js 與 bank_doc.current.js 兩份題庫（見第 4-5 節）
  build_practice_html.js       組頁腳本：讀 AZ900/az900-practice.html 抽出引擎、讀兩份題庫檔灌入資料，
                                組出 ../az104-practice.html。每次改任一份題庫後要重跑：
                                `node tools/build_practice_html.js`
  （check_layout.js／audit.js 等 AZ900 的其餘驗證工具還沒有對應版本，見第 11 節；
  AZ900 的 append.py／splice.py 沒有用到，AZ104 用自己的 merge_batch.js）
```

**組頁流程**：改 `tools/bank_az104.current.js` 或 `tools/bank_doc.current.js` →
`node tools/validate.js` → `node tools/build_practice_html.js` → 用瀏覽器開 `az104-practice.html` 檢查。
`build_practice_html.js` 內建安全網：少了任何一個預期字串就會直接丟錯（`mustReplace()`），組完後也會
自我檢查輸出裡沒有殘留 `az900.` 開頭的 key，避免 AZ900 原始檔改版後腳本悄悄組出壞掉的頁面。

---

## 11. 待辦（交接時從這裡接手）

**已完成 10 卷、372 題，練習網頁可正常使用**（完整清單見第 2 節表格）。Quiz7~Quiz9 是使用者
明確指示跳過的，**不是還沒做**，不要主動回去補。目前已知的來源資料分歧／錯誤（累計，供參考）：
- `AZ104-Q375` 與 `AZ104-Q204`（Quiz6）同一題但兩份來源正解不同（已各自忠實轉錄、解析互相註明）
- `AZ104-Q411` 與 `AZ104-Q90`（Quiz3）同一題但兩份來源正解組合不同（同上處理方式）
- `AZ104-Q401` 的來源標記正解跟來源自己附的解析文字矛盾，已依 Azure 實際知識修正，解析裡註明理由

日後再遇到類似「正解與解析互相矛盾」的情況，可以比照 Q401 的處理方式（修正＋註明理由），
不是每次都要忠實照抄有問題的標記；遇到「同一題不同來源卷正解不同」則比照 Q375/Q411 的做法
（忠實各自轉錄＋解析互相註明，不擅自二選一）。

**下一卷是 Quiz13（AZ104-Q443~Q484，42 題）**。接手時**直接開始做 Quiz13**，不用再問方向、
不用再跟使用者確認要不要繼續。來源 HTML 已經在 `source/quiz13.html`，流程：

```bash
cd AZ104/tools
python extract_quiz.py ../source/quiz13.html ../source/quiz13_questions.json
```

看終端機印出的 `by raw_type`（目前看過的卷全部是格式 A：`single`/`multiple`，選項與正解直接從
HTML 抓，不用看截圖——但還是要先看 `by raw_type` 確認，別預設每卷都一樣）；`category` 欄位
Quiz1~Quiz6 都有給、Quiz10 是空的（`None`），兩種情況都有可能，遇到空的就依題目內容自己判斷
`d`/`od`（第 5 節有 `category`→`od` 對照表，遇到新的英文 category 字串記得補進那張表）。

轉錄完寫成 `tools/batch_quiz11.js`（格式照現有 `batch_quiz10.js` 抄），跑：

```bash
node merge_batch.js batch_quiz11.js BATCH_QUIZ11
node --check bank_az104.current.js
node build_practice_html.js
```

再用 jsdom 掃一次全部題號（範例見這次交接前用過的手法：`new JSDOM(html,{runScripts:'dangerously',...})`
配合 `jumpForm` 逐題跳 + `btnReveal`，檢查 `errors.length === 0` 且每題都有 `verdict`）。

**每做完一卷，比照這次交接的做法自我檢查 context 使用量**：如果明顯偏長（例如已經連續做了
好幾卷、對話輪數很多），就把最新進度更新回本文件的第 2 節與這一節，再結束這個 session，
不用等使用者提醒。

下一步優先順序：

1. **繼續轉錄剩下的卷**（quiz11~quiz19，共 348 題）：來源 HTML 都已經在 `source/` 底下。
2. **真的用瀏覽器開一次 `az104-practice.html`**：目前只用 jsdom（Node 模擬 DOM）驗證過語法與渲染，
   沒有真人點過拖放 (`dd`) 題型的實際拖曳互動、模擬考流程、統計面板、深色模式等。照 AZ900 的
   `tools/uitest.py`（Playwright）模式，之後可以幫 AZ104 也寫一份，或至少手動點過一輪。
3. ~~驗證工具正式化~~ **已完成**：`tools/validate.js` 仿照 AZ900 的同名腳本寫好了，涵蓋
   「`d` 只能 1/2/3」「`a[]` 索引界限」「中英陣列長度」「選項不可帶螢光筆標記」「螢光筆與
   輕量 markdown（`**`／`` ` ``／` ``` `）成對」，`node tools/validate.js` 直接跑（見第 4-5 節）。
   `check_layout.js`／`audit.js` 這兩支還沒有對應版本，之後題庫夠大、需要查重複題或排版檢查時再補。
4. **分頁桶不夠用時**：見第 5 節「為什麼 `d` 只有 1/2/3」，題庫變大想拆更細的分頁，要同時改
   `az104-practice.html` 的 `TAB_ZH`/`TAB_EN`／`nav.tabs` 按鈕／錯題本與星號題的分頁代碼。
5. **`category` → `od` 對照表要補完**：目前只確認過兩個官方領域的英文字串（見第 5 節），
   其餘三個等實際遇到（Implement and manage compute/networking/monitoring 等字樣）要記得補進表格。
6. **環境清理**：這次為了用 jsdom 驗證頁面，在 `AZ104/` 目錄跑過 `npm install jsdom`，
   `node_modules/`、`package.json`、`package-lock.json` 還留在資料夾裡（刪除時被安全機制擋下來，
   之後方便的話可以手動清掉，不影響 `az104-practice.html` 本身運作）。
   `source/all_q1.txt`（debug 用的暫存檔）也還留著，同樣刪不掉，可忽略。
