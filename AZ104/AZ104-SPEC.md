# AZ-104 練習頁 — 規格與交接文件

這份文件讓任何一個新的 session（或人）能接手把 AZ-104 的題庫做出來。

**與 AZ-900 的分工：引擎、資料格式、撰寫風格全部沿用 AZ-900，不重寫一份。**
共用的規則一律指向 [AZ900-SPEC.md](../AZ900/AZ900-SPEC.md)，這裡只寫 **AZ-104 差在哪**、
**目前做到哪**、**下一步做什麼**。兩份都要看。

考試本身怎麼考、練到什麼程度算完成，見 [AZ104-EXAM-TDD.md](AZ104-EXAM-TDD.md)。

---

## 1. 目前狀態：只有骨架，還沒有題目

2026-07-30 建立。`az104-practice.html` 是**可以開、可以切分頁、可以切語言的空殼**——
引擎完整（四種原廠題型、模擬考、錯題本、星號題、統計、進度續作、匯出匯入全都在），
但**兩份題庫都是 0 題**。

| 代號 | 名稱 | 來源 | 題數 |
|---|---|---|---|
| `BANK_MINE` | 自製題庫 | 依官方考試大綱自行編寫 | **0（未開始）** |
| `BANK_DOC` | 文件題庫 | 考古題文件逐題轉錄 | **0（來源文件還沒放進來）** |

**還沒決定的事**（要先問使用者，不要自己選）：

1. **來源文件是什麼**——AZ-900 是一份 138 頁的 ExamTopics 型式 PDF。AZ-104 用什麼還沒定。
   放進 `AZ104/` 底下即可，`render.py` 會自己找（見 §4-1）。
2. **先做哪一份題庫**——AZ-900 是先自製、後轉錄；AZ-104 可以反過來。
3. **自製題庫要不要做**——AZ-104 是 associate 等級，實作題比重高，自己編寫的成本比 AZ-900 高很多。

---

## 2. 與 AZ-900 的差異（只有這些）

`az104-practice.html` 是由 `az900-practice.html` 換殼而來，差異全部列在下表。
換殼腳本是 [tools/build_skeleton.py](tools/build_skeleton.py)，
**AZ-900 的引擎日後有修正，就改那支腳本再跑一次**，不要兩邊手動同步。

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
az104-practice.html          主檔（單一檔案，直接用瀏覽器開）
AZ104-SPEC.md                本文件（題庫怎麼做）
AZ104-EXAM-TDD.md            原廠考試方式與練習方式的 TDD 規格
pages/                       render.py 產出的來源文件頁面圖（不進版控）
shots/                       驗證腳本的截圖（不進版控）
tools/
  build_skeleton.py          一次性：由 az900-practice.html 產生本頁骨架（見 §2）
  port_tools.py              一次性：把 AZ900/tools 的通用工具搬過來（見下）
  smoke.py                   骨架冒煙測試：空題庫下這一頁本身有沒有壞掉
  bank_doc.current.js        文件題庫的**唯一真實來源**（改這個，再 splice）

  ── 以下由 port_tools.py 從 AZ900/tools 搬來 ──
  render.py                  來源 PDF 頁面 → PNG
  clip.py                    把 PDF 的任一塊放大存成圖，用來量座標／看小字
  extract_html.py            抽出 <script> 內容供檢查
  append.py                  把 batch 接到 bank_doc.current.js
  splice.py                  bank_doc.current.js → 灌回 HTML
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
沒有就抓 `AZ104/` 底下第一個 `.pdf`。輸出目錄可用 `AZ104_PAGES` 覆寫。需要 `pip install pymupdf`。

### 4-2. 用 Read 工具「看」圖片並逐題轉錄

一次讀 3–4 頁比較不會爆 context。要同時產出：中文題目、英文題目、中英選項、中英解析、螢光筆標記、換行。

### 4-3. 把新題目寫成一個 batch 檔

格式見 [AZ900-SPEC.md §5](../AZ900/AZ900-SPEC.md)。用 `append.py` 接在陣列尾端時，檔案開頭必須是 `,`。

### 4-4. 附加並灌回 HTML

```bash
python tools/append.py tools/bank_doc.current.js <你的batch檔>
python tools/splice.py tools/bank_doc.current.js
```

`bank_doc.current.js` 是**唯一真實來源**，永遠先改它再 splice。

### 4-5. 驗證（每批都要跑）

```bash
python tools/extract_html.py check.js
node --check check.js               # 語法
node tools/validate.js check.js     # 資料完整性、標記成對、選項無標記
node tools/check_layout.js check.js # 題目分段
node tools/check_review.js check.js # 成績單四種狀態
node tools/audit.js tools/bank_doc.current.js
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
4. **案例研究（case study）。** AZ-104 可能出現一組共用情境、底下掛好幾題。
   目前引擎**沒有這個題型**，遇到時要先決定：拆成各自獨立的題（把情境複製進每一題），
   還是替引擎加一個新的 `k`。**先問使用者，不要自己決定。**
5. **實作題（lab）。** 官方沒有公布哪些考試有 lab，AZ-104 的作答時間是 100 分鐘
   （官方分類是「不含 lab」的那一檔），但仍可能出現。練習頁不模擬 lab，
   這件事記在 [AZ104-EXAM-TDD.md](AZ104-EXAM-TDD.md)。

---

## 6. 待辦（交接時從這裡接手）

- [ ] **決定來源文件**，放進 `AZ104/`（§1）
- [ ] 決定先做自製題庫還是文件題庫（§1）
- [ ] 第一批題目收錄後，回頭確認：領域 `d` 的判定標準（AZ-104 的五個領域邊界比 AZ-900 模糊，
      例如「用 Azure Policy 管儲存體帳戶」算 `1` 還是 `2`）→ **定案後寫進本節，不要每批重新想**
- [ ] 補 AZ-104 專屬術語進 `GLOSSARY_MAP`（§2）
- [ ] 遇到第一題含程式碼片段的題目時，確認排版（§5-2）
- [ ] 遇到第一題 case study 時，問使用者要怎麼處理（§5-4）
- [ ] `az104-practice.html` 頂列的瀏覽次數徽章指向 `l257065.github.io/az104-practice`，
      這一頁還沒發布——**要嘛先發布、要嘛把徽章拿掉**（在 `<h1>` 下方那個 `<a class="hits">`）

### 每次改完一定要跑

§4-5 那一整串。改引擎的話再加 `smoke.py`。
