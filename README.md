# Azure 考照練習

👉 **入口：https://l257065.github.io/Azure/** — 選 AZ-900 或 AZ-104

| 考試 | 練習頁 | 題數 |
|---|---|---|
| AZ-900 Azure Fundamentals | [az900-practice.html](https://l257065.github.io/Azure/AZ900/az900-practice.html) 🔒 | 718（自製 244 ＋ 文件 474） |
| AZ-104 Azure Administrator | [az104-practice.html](https://l257065.github.io/Azure/AZ104/az104-practice.html) 🔒 | 563（Q606 題庫） |

兩份都**需要密碼**。解鎖其中一份之後，切到另一份不用再輸入（同一個分頁工作階段內），
解鎖後頁首會出現互跳連結。

## 為什麼要密碼

兩份練習頁都是**單檔自足**的——題目連正解與解析全部內嵌在 HTML 裡。而
**GitHub Pages 在個人帳號上沒有任何存取控制**（官方寫明：存取控制要 Enterprise Cloud
＋組織持有的 repo，而且「即使 repo 是 private，Pages 網站預設仍然公開在網際網路上」），
所以唯一的辦法是把內容本身加密，只有拿到密碼的人解得開。

這也是為什麼**題庫明文與工具不在這個 repo 裡**：明文只要還在同一個公開 repo，
點進 repo 就繞過密碼了。細節見 [AZ900/README.md](AZ900/README.md)、[AZ104/README.md](AZ104/README.md)。

## 這個 repo 裡有什麼

只有發布用的東西：一個入口頁、兩個**加密後**的練習頁、三份說明。
`.gitignore` 是「預設全擋、逐檔放行」，就是為了防止明文不小心被加回來。
