// 把 batch_quizN.js 的內容接進 bank_az104.current.js 的 BANK_AZ104 陣列最前面（照題號小到大排）。
// usage: node merge_batch.js <batch_file.js> <BATCH_VAR_NAME>
const fs = require("fs");
const path = require("path");

const batchFile = process.argv[2];
const varName = process.argv[3];
if (!batchFile || !varName) {
  console.error("usage: node merge_batch.js <batch_file.js> <BATCH_VAR_NAME>");
  process.exit(1);
}

const bankPath = path.join(__dirname, "bank_az104.current.js");
let bankSrc = fs.readFileSync(bankPath, "utf8");

const batchSrc = fs.readFileSync(path.resolve(batchFile), "utf8");
const m = batchSrc.match(new RegExp("const " + varName + " = \\[([\\s\\S]*)\\];\\s*\\nif \\(typeof module"));
if (!m) throw new Error("找不到 " + varName + " 陣列內容");
const batchEntries = m[1].trim();

const marker = "const BANK_AZ104 = [";
const idx = bankSrc.indexOf(marker);
if (idx === -1) throw new Error("bank_az104.current.js 裡找不到 const BANK_AZ104 = [");
const insertAt = idx + marker.length;

bankSrc = bankSrc.slice(0, insertAt) + "\n\n" + batchEntries + "\n" + bankSrc.slice(insertAt);
fs.writeFileSync(bankPath, bankSrc, "utf8");
console.log("merged", batchFile, "into", bankPath);
