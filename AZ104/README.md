# AZ-104 練習頁（加密）

這個資料夾**只有一個檔**：`az104-practice.html`，而且它是**加密過的**。
打開需要密碼；沒有密碼看到的是一個輸入框，題目與答案都在密文裡。

👉 https://l257065.github.io/Azure/AZ104/az104-practice.html

## 原始碼不在這裡

題庫明文（563 題連正解與解析）、`AZ104-SPEC.md`、全部工具都在**另一個私有 repo**。

**為什麼要拆**：練習頁是單檔自足的——整份題庫內嵌在 HTML 裡。放上 GitHub Pages
就等於開放下載，而 **GitHub Pages 在個人帳號上沒有任何存取控制**：

> 官方〈Changing the visibility of your GitHub Pages site〉：存取控制需要
> GitHub Enterprise Cloud ＋組織持有的 repo，而且「除非用 Enterprise Managed Users，
> **即使 repo 是 private 或 internal，Pages 網站預設仍然公開在網際網路上**」。

⚠️ 所以**把 repo 轉成私有是沒有用的**，網站照樣公開。唯一可行的是把內容本身加密，
而那又要求**明文不能待在同一個公開 repo 裡**——否則點進 repo 就繞過密碼了。
這就是為什麼原始碼搬走、這裡只留密文。

## 加密方式

`PBKDF2-HMAC-SHA256`（60 萬次迭代、16 bytes 隨機 salt）導出 256-bit 金鑰
→ `AES-256-GCM`（12 bytes 隨機 IV）加密整份 HTML → 瀏覽器用 WebCrypto 解密後
`document.write` 出來。全部走 Node 與瀏覽器內建的原語，**沒有任何相依套件**。

⚠️ **這是客戶端加密，要知道它擋得住什麼**：沒有密碼的人拿到的是密文，這是真的
（不像「JS 跳個輸入框」那種一看原始碼就破）。但**密文會落在對方電腦上、可以離線
暴力破解**，所以密碼長度比複雜度重要。目前用的是短密碼，實際效果是擋掉搜尋引擎、
掃描機器人與隨手點進來的人。

⚠️ 這一頁 2026-08-17 之前曾經以**明文**公開在同一個網址上，可能已被搜尋引擎或
快取抓走。加密是止血，不是收回。
