# Azure 考照練習

| 考試 | 練習頁 | 狀態 |
|---|---|---|
| AZ-900 Azure Fundamentals | https://l257065.github.io/Azure/AZ900/az900-practice.html | 題庫完成（自製 244 題＋文件 474 題） |
| AZ-104 Azure Administrator | https://l257065.github.io/Azure/AZ104/az104-practice.html 🔒 **要密碼** | Q606 題庫已收完 563 / 606 題（其餘 43 題是已知重複）。原始碼在另一個**私有** repo，見 [AZ104/README.md](AZ104/README.md) |

## AZ-104 為什麼要密碼

那一頁是**單檔自足**的——563 題連正解與解析全部內嵌在 HTML 裡。而
**GitHub Pages 在個人帳號上沒有任何存取控制**（官方寫明：存取控制要 Enterprise Cloud
＋組織持有的 repo，而且「即使 repo 是 private，Pages 網站預設仍然公開在網際網路上」），
所以唯一的辦法是把內容本身加密，只有拿到密碼的人解得開。

這也是為什麼 AZ-104 的題庫明文與工具**不在這個 repo 裡**：明文只要還在同一個公開
repo，點進 repo 就繞過密碼了。細節見 [AZ104/README.md](AZ104/README.md)。
