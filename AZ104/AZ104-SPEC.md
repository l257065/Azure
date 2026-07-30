# AZ-104 練習頁 — 規格與交接文件

這份文件讓任何一個新的 session（或人）能接手把 AZ-104 的題庫做出來。

**與 AZ-900 的分工：引擎、資料格式、撰寫風格全部沿用 AZ-900，不重寫一份。**
共用的規則一律指向 [AZ900-SPEC.md](../AZ900/AZ900-SPEC.md)，這裡只寫 **AZ-104 差在哪**、
**目前做到哪**、**下一步做什麼**。兩份都要看。

考試本身怎麼考、練到什麼程度算完成，見 [AZ104-EXAM-TDD.md](AZ104-EXAM-TDD.md)。

---

## 0. 兩個人同時做：誰動哪些檔案 `[必讀]`

AZ-104 的兩份題庫由**兩個人分頭做**，各自在自己的分支上跑，之後才併回 `main`。
所以檔案是刻意拆開的——**只要各自只動自己那一支，git 永遠不會衝突**。

| 檔案 | 主人 | 說明 |
|---|---|---|
| `banks/bank_a_mine.js` | 做**題庫 A** 的人 | `const BANK_MINE`，自製題庫的唯一真實來源 |
| `banks/bank_b_doc.js` | 做**題庫 B** 的人 | `const BANK_DOC`，文件題庫的唯一真實來源 |
| `az104-engine.html` | **兩人共用，改前先講** | 引擎樣板：版面、作答邏輯、模擬考設定。題庫區塊只有標記，**不放題目** |
| `az104-practice.html` | **沒有主人：這是產出物** | 由 `tools/build.py` 產生。**絕對不要手改** |

```
az104-engine.html  +  banks/bank_a_mine.js  +  banks/bank_b_doc.js
                            │
                     tools/build.py
                            ↓
                   az104-practice.html      ← 用瀏覽器開的是這個
```

**三條規則**

1. 加題目只改 `banks/` 底下自己那一支，然後跑 `python tools/build.py`。
   不 build，練習頁不會變。
2. **不要把題目寫進 `az104-engine.html`。** 寫進去下次 build 會被蓋掉——
   `build.py` 有擋，發現樣板的題庫區塊裡有題目就直接報錯不寫檔。
3. `az104-practice.html` 在 [.gitattributes](.gitattributes) 裡標成 `-merge`，
   併版時它會直接變成整檔衝突（不會憑行號亂拼）。解法固定是**重建**，不是手改：

   ```bash
   git checkout --ours AZ104/az104-practice.html   # 挑哪一邊都可以，內容不重要
   python AZ104/tools/build.py
   git add AZ104/az104-practice.html
   ```

**併回 `main` 時要注意的一件事**：如果對方的分支還沒接上這個結構，
還在直接改舊的 `az104-practice.html`，那他的引擎修改會落在**產出物**上而不是樣板上，
重建就會沖掉。所以**併版時先確認 `az104-engine.html` 有沒有漏收對方的引擎修改**，
再跑 `build.py`。對方一旦接上這個結構，之後就不會再有這個問題。

`python tools/build.py --check` 只檢查產出物是不是最新的、不寫檔，
可以拿來當 commit 前的最後一道關卡。

---

## 1. 目前狀態

2026-07-30 建立骨架。`az104-practice.html` 是**可以開、可以切分頁、可以切語言的空殼**——
引擎完整（四種原廠題型、模擬考、錯題本、星號題、統計、進度續作、匯出匯入全都在）。

| 代號 | 名稱 | 檔案 | 來源 | 題數 |
|---|---|---|---|---|
| `BANK_MINE` | 題庫 A：自製 | `banks/bank_a_mine.js` | 依官方考試大綱自行編寫 | **0（由另一位負責）** |
| `BANK_DOC` | 題庫 B：文件 | `banks/bank_b_doc.js` | `AZ104考題/` 的 PDF 逐題轉錄 | **13 / 約 505（進行中）** |

題庫 B 的進度：題組 1 的 #1–#13 已完成（`n` 1001–1013），全部是純文字單選題。

分母是「約 505」而不是 546 或 470，理由見 §1-1-1：**三份來源檔的題數會有出入**，
原始合計 546 題裡有 41 題是真重複。

### 1-1. 來源文件（題庫 B）

放在 `AZ104考題/`，**不進版控**（檔案太大，且是使用者自備的文件）。

| 檔案 | 頁數 | 題數 | 題號格式 | 答案來源 |
|---|---|---|---|---|
| `NEW-AZ-104-470Q.pdf` | 759 | 470 | `Question #N`，分 Question Set／Testlet | 文件內自帶 `Correct Answer:` |
| `New-AZ-104-增題62Q.pdf` | 62 | 62 | `NewQ #1`–`#62` | 同上 |
| `NewQuestion-AZ-104-NewQ63-Q76.pdf` | 13 | 14 | `NewQ #63`–`#76` | `Q63-Q76 Correct.txt` |

⚠️ 兩份增題用的是 **`NewQ #N`** 而不是 `Question #N`，而且是接續編號的同一個系列
（#1–#62 加 #63–#76 共 76 題）。`scan_pdf.py` 兩種標題都認得。
單獨掃 `NewQ63-Q76` 那份時，「段內缺號」會報 1–62 缺號——那是因為它從 #63 起跳，
不是真的缺題。

### 1-1-1. 「AZ-104 有幾題」有三個答案 `[已查證]`

**題數會有出入，這是來源文件本身的性質，不是掃描錯誤。** 用 `tools/dupes.py` 查證過：

| 算法 | 題數 |
|---|---|
| 三份檔案原始題數合計 | **546** |
| 只看 `NEW-AZ-104-470Q.pdf` 一份 | **470** |
| 扣掉真重複之後的唯一題數 | **約 505** |

出入來自三件事：

1. **兩份增題有 76 題**，但**其中 19 組其實已經在 470Q 裡**（NewQ#1 = 題組 2 #32、
   NewQ#31 = 題組 4 #32…）。而且兩份增題彼此也重疊（NewQ#25 = NewQ#67、
   NewQ#26 = NewQ#68、NewQ#27 = NewQ#69、NewQ#28 = NewQ#70、NewQ#2 = NewQ#63）。
2. **470Q 自己內部也重複**：同一題在不同 Question Set 出現好幾次，
   例如題組 5 的 #16／#85／#103／#119 是同一題。真重複共 **29 組、多出 41 題**。
3. **系列題不是重複，不能砍**：有 22 組、共 86 題屬於「同一段共用情境、每題提出不同
   `Solution:`、答案也不同」的題型（`n:1002`–`1004` 就是一組）。
   單純比文字相似度會把它們誤判成重複——實測 Jaccard 0.90 會多算 55 題。
   `dupes.py` 因此把每題切成「情境」與「解法」兩段分別比，**兩段都相同才算重複**。

#### 有 14 組重複題的標的答案互相矛盾 `[要人工裁決]`

這是收錄時最需要小心的一類。最乾淨的例子是題組 4 的 #43 與 #81：

- 題目、四個選項、附的表格**一字不差**，但一處標 **A（Proximity2 only）**、
  另一處標 **C（Proximity1 only）**。
- 連文件自己的說明都互相打臉：一邊寫「Only Proximity2, which also in RG2」，
  另一邊寫「Only Proximity1, which also in RG2」。
- 兩處都要看那張表格的圖才能判斷誰對。

**處理原則**：遇到已收錄過的重複題就跳過（`audit.js` 會抓到題目文字重複）；
遇到答案矛盾的，**出圖把題目與表格看清楚、自己判斷正解**，並在解析裡寫明
「原始文件在 X 與 Y 兩處給了不同答案，這裡採用 Z，理由是…」。
`tools/dupes.py --list` 會把 14 組全部列出來。

### 1-1-2. 470Q 的結構與工作量

**轉錄順序：先 `NEW-AZ-104-470Q.pdf`**，把領域判定、程式碼排版、case study 這些
規則在主題庫上一次定案，再回頭撿兩份增題裡**獨有**的那些題。

`tools/scan_pdf.py` 掃出來的結構（**這份 PDF 的文字是可以抽的**，
純文字題直接用 `tools/qtext.py` 讀，不必出圖）：

| 區段 | 題數 | 頁 | 有圖的題 |
|---|---|---|---|
| Question Set 1 | 40 | 1–33 | 4 |
| Question Set 2 | 79 | 33–146 | 57 |
| Question Set 3 | 70 | 146–261 | 62 |
| Question Set 4 | 90 | 261–395 | 67 |
| Question Set 5 | 121 | 395–586 | 97 |
| Question Set 6 | 47 | 586–664 | 37 |
| Testlet 1–10（案例研究） | 23 | 664–759 | 23 |

- 題組共 **447 題**、案例共 **23 題**，段內都沒有跳號。
- **470 題裡有 347 題有圖**（表格、入口網站截圖、是非表、拖放答案區），那些一定要
  `render.py` 出圖用眼睛看；剩下 123 題可以純文字轉錄，快得多。
- 疑似題型：`mc` 310、`hs` 140（含 `dl`，都寫 HOTSPOT 所以要看圖才分得出來）、`dd` 20。
- **44 題抓不到 `Correct Answer:`**（答案畫在圖上），轉錄到那幾題要特別確認。
- 這份 PDF 是轉賣品，每隔幾頁夾一行賣家浮水印網址，`scan_pdf.py` 在讀取階段就清掉了。

#### `AZ-104-26.95-Correct.txt` 的題號對不上這份 PDF `[待決]`

那份更正檔列了 10 條（`Q57:NYN`、`Q133:C`、`Q253:YNN`…）。已經驗過：

- 把它當「跨全份攤平的 1–470」→ 只有 6/10 的答案形狀對得上題型
  （`Q57:NYN` 是三句是非，卻落在單選題上；`Q133:C` 是單選，卻落在是非表上）。
- 再從 −30 到 +30 逐一試偏移 → 最高也只有 6/10，**沒有任何偏移能全部吻合**。

所以它八成是**另一個版本的題庫**（檔名的 26.95 像是版號）的更正，不是這份 470Q。
**要問使用者這份更正檔是哪來的、對應哪一份文件**；在確認之前不要拿它去覆蓋答案。
遇到 PDF 自己標的答案看起來有問題時，照
[AZ900-SPEC.md §8-3](../AZ900/AZ900-SPEC.md) 的規則辦：忠實轉錄標記的答案，
但在解析裡講清楚爭議（`n:1008` 就是第一個這樣的例子）。

---

## 1-2. 題號怎麼編 `[已定案]`

三份來源檔各有各的編號方式，而且 470Q 那份還分成 Question Set 1–6 與 Testlet 1–10、
**每一段的 `Question #` 都從 1 重新算**，直接拿 `#N` 當 `n` 一定撞號。所以把區段編進題號：

| 來源 | `n` | 範圍 |
|---|---|---|
| 470Q 的 Question Set `S` 第 `q` 題 | `S*1000 + q` | 1001…6047 |
| 470Q 的 Testlet `T` 第 `q` 題 | `10000 + T*100 + q` | 10101…11004 |
| 兩份增題的 `NewQ #q` | `20000 + q` | 20001…20076 |

`2017` 就是題組 2 第 17 題，`10302` 就是案例 3 第 2 題，`20063` 就是 NewQ #63。
這樣 `n` 仍然是數字（跳題功能要數字比對），而且看得懂、回原始文件查得到。

因為增題與 470Q 大量重疊（見 §1-1-1），**收錄時以 470Q 的題號為主**：
同一題已經用 `1xxx`–`6xxx` 收過了，就不要再用 `20xxx` 收一次。只有增題獨有的那些題
才會出現 `20xxx` 的題號。

**連帶影響**：引擎的 `docGaps()` 原本從 1 數到最大題號、把每個不存在的整數都當缺號，
在新編號下會把 1040→2001 之間 960 個「別段的號碼」全當成缺號。已改成先用 `docNo()`
把題號解碼回「區段 + 段內題號」，**只在同一段之內算缺號**；題數說明面板也改成逐段
列出題數與段內缺號，並說明編碼規則。`smoke.py` 有守這件事。

---

## 2. 與 AZ-900 的差異（只有這些）

引擎是由 `az900-practice.html` 換殼而來，差異全部列在下表。
換殼腳本是 [tools/build_skeleton.py](tools/build_skeleton.py)，
**AZ-900 的引擎日後有修正，就改那支腳本再跑一次**，不要兩邊手動同步。

> `build_skeleton.py` 是骨架階段的一次性腳本，它產生的是 `az104-practice.html`。
> 現在那個檔名已經是產出物，**再跑一次的話要把輸出改成 `az104-engine.html`
> 並重新補上 `/*__BANK_A__*/` 等四個標記**，然後跑 `tools/build.py`。

| 項目 | AZ-900 | AZ-104 |
|---|---|---|
| 領域數 | 3 | **5** |
| 分頁 | `0` 全部／`1-3` 領域／`4` 錯題本／`5` 星號題 | `0` 全部／**`1-5` 領域**／**`6` 錯題本**／**`7` 星號題** |
| 分頁索引 | 寫死 4／5 | 改成常數 `D_MAX` / `TAB_WRONG` / `TAB_STAR` / `TAB_MAX` |
| 模擬考 | 40 題 / 45 分鐘 | **50 題 / 100 分鐘** |
| localStorage 前綴 | `az900.` | `az104.` |
| 存檔檔名 | `az900-progress-*.json` | `az104-progress-*.json` |
| 領域統計 | 寫死三格 | 依 `D_MAX` 動態產生 |
| 窄螢幕分頁字級 | 6 個分頁 | 8 個分頁，再縮一級（560px / 380px 兩個斷點都調過） |

**五個領域的 `d` 值**（權重見 [AZ104-EXAM-TDD.md](AZ104-EXAM-TDD.md) §1-2）：

| `d` | 中文 | English | 分頁標籤 |
|---|---|---|---|
| `1` | 身分與治理 | Identities & governance | 身分治理 |
| `2` | 儲存體 | Storage | 儲存體 |
| `3` | 運算資源 | Compute | 運算 |
| `4` | 虛擬網路 | Virtual networking | 網路 |
| `5` | 監控與維護 | Monitor & maintain | 監控 |

**沒有動的東西**（所以 AZ-900 的規格直接適用）：

- `BANK_DOC` 的資料格式與四種題型 `mc` / `hs` / `dd` / `dl` → [AZ900-SPEC.md §5](../AZ900/AZ900-SPEC.md)
- 題型對應規則、洗牌規則 → §6
- 中文翻譯風格 → §7
- 解析風格（整組列出、排版、標出可疑答案、長度、配對題格式）→ §8
- 螢光筆標記 `⟦⟧`、服務圖示 `ico` → §9-1、§9-2
- 題目換行 → §10
- HTML 內部架構速查（函式在哪、localStorage 有哪些鍵）→ §11（鍵的前綴換成 `az104.`）
- 成績單的四種選項狀態 → §12
- 使用者已定案的決策 → §13，**全部繼續適用**

**`GLOSSARY_MAP` 沿用 AZ-900 那一份**（約 150 條）。裡面是通用 Azure 術語，AZ-104 也用得到，
但缺 AZ-104 才會考的東西（Bicep、NSG 有效規則、Bastion、Site Recovery、Recovery Services 保存庫、
擴展集、容器應用程式…）。**收錄題目時順手補**，加在 `const GLOSSARY_MAP` 裡就會即時生效。

---

## 3. 檔案清單

```
az104-practice.html          ★ 產出物：直接用瀏覽器開的就是這個。不要手改（見 §0）
az104-engine.html            引擎樣板（兩人共用，題庫區塊只有標記）
.gitattributes               把產出物標成 -merge，衝突一律重建
banks/
  bank_a_mine.js             題庫 A：自製。**唯一真實來源**
  bank_b_doc.js              題庫 B：文件轉錄。**唯一真實來源**
AZ104-SPEC.md                本文件（題庫怎麼做）
AZ104-EXAM-TDD.md            原廠考試方式與練習方式的 TDD 規格
AZ104考題/                   來源 PDF 與答案 txt（不進版控，見 §1-1）
pages/                       render.py 產出的來源文件頁面圖（不進版控）
shots/                       驗證腳本的截圖（不進版控）
tools/
  build.py                   ★ 樣板 + 兩份題庫 → az104-practice.html（見 §0）
  scan_pdf.py                掃來源 PDF：每題的題號、區段、頁碼、疑似題型、有沒有圖、標的答案
  qtext.py                   倒出指定題目的原文，純文字題直接讀這個不用出圖
  dupes.py                   跨三份來源找重複題，並區分「真重複」與「同情境不同解法的系列題」
  build_skeleton.py          一次性：由 az900-practice.html 產生本頁骨架（見 §2）
  port_tools.py              一次性：把 AZ900/tools 的通用工具搬過來（見下）
  smoke.py                   冒煙測試：這一頁本身有沒有壞掉、題號編碼算不算對

  ── 以下由 port_tools.py 從 AZ900/tools 搬來 ──
  render.py                  來源 PDF 頁面 → PNG
  clip.py                    把 PDF 的任一塊放大存成圖，用來量座標／看小字
  extract_html.py            抽出 <script> 內容供檢查
  append.py                  把 batch 接到 banks/ 底下的題庫檔
  patch_fields.py            逐題換欄位的共用工具，吃 JSON 補丁檔
  vfy.py                     核對原文的共用小工具
  icons.py                   服務圖示：取自官方圖示包（圖示包沿用 AZ900 底下那一份）
  icons_pdf.py               服務圖示：裁 PDF
  validate.js                資料完整性、逐格對應、標記成對、選項無標記
  check_layout.js            題目分段檢查
  check_review.js            成績單狀態模擬（四種題型）
  audit.js                   校對：查標準腳本沒涵蓋的九件事
  test_shuffle.js            洗牌不變式測試：載入 HTML 裡真正的 permuteOptions() 跑 200 輪
  uitest.py                  Playwright：實際操作三種原廠題型並驗證批改
  uitest_order.py            Playwright：出題順序
  uitest_skip.py             Playwright：跳題
  check_star_flag.py         Playwright：星號題與待複習標記
```

`icons.py` 與 `icons_pdf.py` 的題號對照表**搬過來時已清空**（AZ-900 的座標對 AZ-104 沒意義），
要用的時候照 AZ-900 版的寫法逐題加。

---

## 4. 工作流程

跟 AZ-900 完全一樣，只有路徑不同。詳細說明見 [AZ900-SPEC.md §4](../AZ900/AZ900-SPEC.md)。

### 4-1. 把來源文件頁面轉成圖片

```bash
python tools/render.py <起始頁> <結束頁> [dpi]
```

輸出到 `AZ104/pages/pNNN.png`。**PDF 檔名不寫死**：先看環境變數 `AZ104_PDF`，
沒有就抓 `AZ104/`（含 `AZ104考題/`）底下第一個 `.pdf`。輸出目錄可用 `AZ104_PAGES` 覆寫。
現在有三份 PDF，**一定要明確指定**：

```bash
AZ104_PDF="AZ104考題/NEW-AZ-104-470Q.pdf" python tools/render.py 1 12
```

需要 `pip install pymupdf`。

### 4-2. 用 Read 工具「看」圖片並逐題轉錄

一次讀 3–4 頁比較不會爆 context。要同時產出：中文題目、英文題目、中英選項、中英解析、螢光筆標記、換行。

### 4-3. 把新題目寫成一個 batch 檔

格式見 [AZ900-SPEC.md §5](../AZ900/AZ900-SPEC.md)。用 `append.py` 接在陣列尾端時，檔案開頭必須是 `,`。

### 4-4. 附加並重建

```bash
python tools/append.py banks/bank_b_doc.js <你的batch檔>
python tools/build.py
```

`banks/bank_b_doc.js` 是**唯一真實來源**，永遠先改它再 build。
`az104-practice.html` 是產出物，手改會被下一次 build 蓋掉（見 §0）。

### 4-5. 驗證（每批都要跑）

```bash
python tools/build.py               # 先 build，下面驗的是產出物
python tools/extract_html.py check.js
node --check check.js               # 語法
node tools/validate.js check.js     # 資料完整性、標記成對、選項無標記
node tools/check_layout.js check.js # 題目分段
node tools/check_review.js check.js # 成績單四種狀態
node tools/audit.js banks/bank_b_doc.js
node tools/test_shuffle.js          # 洗牌不變式
rm check.js
```

全部通過才算完成一批。**這七支在題庫是空的時候也全部會過**（骨架階段已驗證），
所以任何一支變紅就是這一批改壞了，不會有「本來就紅」的雜訊。

改到作答邏輯時，還要跑真的瀏覽器：

```bash
python tools/smoke.py            # 空題庫也能跑：確認頁面本身沒壞
python tools/uitest.py           # 要有題目才跑得動
python tools/uitest_order.py
python tools/uitest_skip.py
python tools/check_star_flag.py
```

需要 `pip install playwright && playwright install chromium`。截圖放在 `shots/`。

---

## 5. 收錄 AZ-104 題目時要特別注意的事

AZ-900 是 fundamentals，題目大多是「這個服務是做什麼的」。AZ-104 是 associate，
題型的**重心不一樣**，轉錄時會踩到 AZ-900 沒踩過的坑：

1. **情境題會長很多。** 一題常常是「某公司有 A、B、C 三個環境，需求是 X，你該怎麼做」。
   換行分段（[AZ900-SPEC.md §10](../AZ900/AZ900-SPEC.md)）會比 AZ-900 更吃重，前言、需求、問句要分開。
2. **PowerShell / Azure CLI / ARM / Bicep 的程式碼片段。** AZ-900 沒有這種東西。
   `q` 是純文字欄位，程式碼要靠換行排版；**收錄第一題含程式碼的題目時，
   先確認排版看得懂**，必要時再回頭改引擎（那就要跑 `uitest.py`）。
3. **入口網站截圖題會更多。** 只要選項是入口網站畫面（側欄、刀鋒、設定清單），
   就一定要設 `fix:true` 不洗選項，`audit.js` 會擋。規則見 [AZ900-SPEC.md §5](../AZ900/AZ900-SPEC.md) 的 `fix` 欄。
4. **案例研究（case study）＝ Testlet，確定會遇到 `[待決]`。** 掃描結果是
   **10 組 Testlet、共 23 題**，在 PDF 第 664–759 頁，每一組都有一段共用的
   Introductory Info（公司現況、需求、既有環境），底下掛 1–4 題。
   目前引擎**沒有這個題型**。兩條路：
   - **拆成獨立題**：把共用情境複製進每一題的 `q`。不用動引擎，但同一段情境會重複
     2–4 次，題目會變得很長。
   - **替引擎加一個 `case` 欄位**：一組情境存一份，掛在題目上，渲染時折疊顯示。
     比較貼近原廠，但要動引擎（就得跑 `uitest.py`）。

   **先問使用者，不要自己決定。** 題組 1–6 的 447 題可以先做完，不必卡在這裡。
5. **實作題（lab）。** 官方沒有公布哪些考試有 lab，AZ-104 的作答時間是 100 分鐘
   （官方分類是「不含 lab」的那一檔），但仍可能出現。練習頁不模擬 lab，
   這件事記在 [AZ104-EXAM-TDD.md](AZ104-EXAM-TDD.md)。

---

## 6. 待辦（交接時從這裡接手）

- [x] ~~決定來源文件~~ → `AZ104考題/` 三份 PDF，先做 `NEW-AZ-104-470Q.pdf`（§1-1）
- [x] ~~決定先做哪一份題庫~~ → 兩份並行，本分支做題庫 B（文件），題庫 A 由另一位在 `main` 做（§0）
- [x] ~~拆檔以免兩人互相覆蓋~~ → `banks/` + `tools/build.py`（§0）
- [x] ~~領域 `d` 的判定標準~~ → 見下面「領域怎麼判」，**照那份表走，不要每批重新想**
- [ ] 補 AZ-104 專屬術語進 `GLOSSARY_MAP`（§2）
- [ ] 遇到第一題含程式碼片段的題目時，確認排版（§5-2）
- [ ] 遇到第一題 case study 時，問使用者要怎麼處理（§5-4）
- [ ] 瀏覽次數徽章指向 `l257065.github.io/az104-practice`，這一頁還沒發布——
      **要嘛先發布、要嘛把徽章拿掉**（在 `az104-engine.html` 的 `<h1>` 下方那個 `<a class="hits">`）
- [ ] 告知做題庫 A 的 coworker 接上 §0 的結構（拉這個分支或等併版），
      在那之前他的引擎修改會落在產出物上

### 領域怎麼判 `[已定案]`

AZ-104 的五個領域邊界比 AZ-900 模糊，容易每批重新糾結。規則：**看題目在問「哪一種資源
的哪一個操作」，資源歸誰就歸誰**；只有在題目真的是在問治理機制本身時才算 `1`。

| `d` | 收哪些 | 邊界案例 |
|---|---|---|
| `1` 身分與治理 | Entra ID／Azure AD 使用者群組、RBAC 角色指派、條件式存取、MFA、AD Connect 同步、訂用帳戶與管理群組、資源群組、標記、Azure Policy、成本管理、鎖定、ARM／Bicep 範本與部署歷程 | 「用 Azure Policy 限制儲存體帳戶的 SKU」→ **`1`**（在問 Policy 怎麼運作）<br>「儲存體帳戶要選哪個備援等級」→ `2` |
| `2` 儲存體 | 儲存體帳戶、Blob／檔案／佇列／表格、存取層與生命週期、備援（LRS…RA-GZRS）、共用存取簽章、Azure Files 與 File Sync、Import/Export、AzCopy、儲存體防火牆 | 「給儲存體帳戶指派 RBAC 角色」→ **`2`**（資源是儲存體）<br>「建立一個自訂 RBAC 角色」→ `1` |
| `3` 運算資源 | 虛擬機器與磁碟、可用性設定組與可用性區域、擴展集、VM 擴充功能、映像與快照、App Service、容器實例與 Azure Container Apps、AKS | 「VM 的網路介面要接哪個子網」→ `4`（在問網路）<br>「VM 大小改不了怎麼辦」→ `3` |
| `4` 虛擬網路 | 虛擬網路與子網、NSG 與應用程式安全群組、有效規則、對等互連、VPN 與 ExpressRoute、路由表、DNS、負載平衡器、應用程式閘道、Bastion、Firewall、Network Watcher | 「負載平衡器的健康探查」→ `4`<br>「用 Network Watcher 抓封包來查問題」→ `4`（不是 `5`，工具歸網路） |
| `5` 監控與維護 | Azure Monitor 與計量、Log Analytics 與 KQL、警示與動作群組、活動記錄、Application Insights、備份與 Recovery Services 保存庫、Site Recovery、VM 的備份還原 | 「資源鎖被移除時要寄信」→ **`5`**（在問警示怎麼設）<br>「資源鎖要怎麼設」→ `1` |

判不出來時的順位：**題目問的動作 > 題目提到的資源**。例如「設定警示，在有人刪掉
儲存體帳戶時通知」——動作是設警示，所以是 `5` 而不是 `2`。

### 每次改完一定要跑

§4-5 那一整串。改引擎的話再加 `smoke.py`。
commit 前再補一發 `python tools/build.py --check`，確認產出物沒有忘記重建。
