#!/usr/bin/env python3
"""跨三份來源 PDF 找重複題，並且**不要把「同情境、不同解法」的系列題誤判成重複**。

為什麼需要這支：三份檔案的原始題數合計 546，但裡面有大量重複——同一題在不同
Question Set 出現好幾次，兩份增題又跟 470Q 撞題。所以「AZ-104 有幾題」這個問題，
看你怎麼算會得到 546 / 470 / 唯一題數三個不同數字。

坑：這份文件有一整類系列題，樣板長這樣

    Note: This question is part of a series of questions that present the same scenario…
    （一大段共用情境）
    Solution: 你要做 X
    Does the solution meet the goal?  A. Yes  B. No

同一組系列題的共用情境完全一樣，**只有 Solution: 那一行不同，答案也不同**。
它們是不同的題目，不是重複。單純比整段文字相似度（Jaccard 0.90 甚至 0.97）
會把它們黏成一組，於是重複數被嚴重高估。

所以這支把每一題切成兩段分別比：

    情境 = 去掉樣板前言、去掉 Solution: 之後的部分
    解法 = Solution: 那一行（沒有就是空字串）

**情境相同且解法相同** → 真的重複。
**情境相同但解法不同** → 系列題，分開報，不算重複。

    python tools/dupes.py            # 摘要
    python tools/dupes.py --list     # 連每一組都列出來
    python tools/dupes.py --series   # 只列系列題，附每題的 Solution 與標的答案
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scan_pdf import scan, sec_rank  # noqa: E402

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = [
    os.path.join(HERE, "AZ104考題", "NEW-AZ-104-470Q.pdf"),
    os.path.join(HERE, "AZ104考題", "New-AZ-104-增題62Q.pdf"),
    os.path.join(HERE, "AZ104考題", "NewQuestion-AZ-104-NewQ63-Q76.pdf"),
]

# 系列題的樣板前言，兩份檔案的用字略有不同
BOILER = re.compile(
    r"Note: (This|The) question is (included in a number of questions|part of a series of questions)"
    r".*?(?=(You |Your |A company|Contoso|HOTSPOT|DRAG))", re.S)
SOLUTION = re.compile(r"Solution\s*:\s*(.*?)(?=(Does the solution meet the goal)|$)", re.S)

# 案例研究（Testlet）的題目前面掛著一大段共用的 Introductory Info。同一份案例會被
# 好幾個 Testlet 重複使用，那段情境動輒四千字，直接比整段文字的話所有案例題都會
# 長得一模一樣（實測 T1#1 / T3#3 / T7#1 被誤判成同一題，其實三題完全不同）。
# 真正的問句在最後一個單獨的 "Question" 之後（不是 "Question Set"、不是 "Question #"、
# 也不是說明文字裡的 "return to the question"）。
CASE_SPLIT = re.compile(r"\bQuestion\b(?!\s*(?:Set|#))")


def words(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def split_q(text, is_case=False):
    """→ (情境, 解法)。解法就是 Solution: 那一行，沒有就是空字串。"""
    body = text.split("Correct Answer")[0]
    if is_case:
        hits = list(CASE_SPLIT.finditer(body))
        if hits:
            body = body[hits[-1].end():]      # 砍掉共用的案例情境，只留真正的問句
    body = re.sub(r"(Question|NewQ)\s*#\s*\d+", " ", body)
    body = BOILER.sub(" ", body)
    m = SOLUTION.search(body)
    sol = words(m.group(1)) if m else ""
    scen = words(SOLUTION.sub(" ", body))
    return scen, sol


def short(r):
    return "%s %s" % (r["tag"], r["label"])


def jac(a, b):
    A, B = set(a.split()), set(b.split())
    return len(A & B) / len(A | B) if A | B else 0.0


def topic(scen, n=58):
    """從共用情境裡抓一句當標題用"""
    s = re.sub(r"\s+", " ", scen).strip()
    return (s[:n] + "…") if len(s) > n else s


def print_series(系列題):
    """系列題工作清單：同一段共用情境、每題不同 Solution，全部都要收。"""
    total = sum(len(g) for g, _ in 系列題)
    print("\n" + "=" * 78)
    print("系列題清單：%d 組、共 %d 題（都是不同的題目，不可以只收一題）"
          % (len(系列題), total))
    print("=" * 78)

    order = sorted(系列題, key=lambda gb: min((sec_rank(r["sec"]), r["no"]) for r in gb[0]))
    for i, (grp, buckets) in enumerate(order, 1):
        grp = sorted(grp, key=lambda r: (sec_rank(r["sec"]), r["no"]))
        print("\n[%2d] %d 題 / %d 種解法    n = %s"
              % (i, len(grp), len(buckets),
                 ", ".join(r["label"] for r in grp)))
        print("     文件位置：%s" % "、".join(short(r) for r in grp))
        print("     共用情境：%s" % topic(grp[0]["scen"], 66))
        for r in grp:
            sol = re.sub(r"\s+", " ", r["sol"]).strip()
            print("       %-11s %-13s ans=%-4s %s"
                  % (r["label"], r["tag"],
                     (r["ans"] or "—")[:4],
                     ("解法：" + sol[:52] + ("…" if len(sol) > 52 else "")) if sol
                     else "（這一題沒有 Solution: 行）"))

    dup_in = [gb for gb in order if len(gb[1]) < len(gb[0])]
    if dup_in:
        print("\n注意 1：有 %d 組的解法數少於題數，代表組內還有解法重複的題"
              "（那幾題才是真重複，已另計在真重複裡）：" % len(dup_in))
        for grp, buckets in dup_in:
            print("        %d 題 / %d 種解法：%s"
                  % (len(grp), len(buckets),
                     ", ".join(r["label"] for r in sorted(grp, key=lambda r: (sec_rank(r["sec"]), r["no"])))))

    # 這類系列題的答案只有 Yes/No。原廠樣板明說「有些系列可能沒有正確解法」，
    # 所以整組都是 No 是合法的；但那也是標記出錯最容易藏身的地方，值得回頭看。
    def yes_n(grp):
        return sum(1 for r in grp if (r["ans"] or "").strip().upper().startswith("A"))
    no_yes = [gb for gb in order
              if all(re.fullmatch(r"[AB]", (r["ans"] or "").strip()) for r in gb[0])
              and yes_n(gb[0]) == 0]
    if no_yes:
        print("\n注意 2：有 %d 組**整組都標 No**（沒有任何一個解法被標成可行）。"
              % len(no_yes))
        print("        樣板允許這種情況，但也最容易藏標記錯誤，收錄時值得回頭確認：")
        for grp, _ in no_yes:
            print("        %s（%s）"
                  % (", ".join(r["label"] for r in sorted(grp, key=lambda r: (sec_rank(r["sec"]), r["no"]))),
                     topic(grp[0]["scen"], 44)))


def main():
    rows = []
    for f in FILES:
        rs, _ = scan(f)
        tag = (os.path.basename(f).replace("NEW-AZ-104-", "")
               .replace("NewQuestion-AZ-104-", "").replace(".pdf", ""))[:12]
        for r in rs:
            r["tag"] = tag
            r["scen"], r["sol"] = split_q(r["text"], r["sec"].startswith("T"))
            rows.append(r)

    print("三份檔案原始題數合計 %d" % len(rows))
    for f in FILES:
        tag = (os.path.basename(f).replace("NEW-AZ-104-", "")
               .replace("NewQuestion-AZ-104-", "").replace(".pdf", ""))[:12]
        print("   %-14s %3d 題" % (tag, sum(1 for r in rows if r["tag"] == tag)))
    print()

    # 情境相近就先分到同一群（0.92：容得下轉錄雜訊，又不會把不同題黏在一起）
    long_rows = [r for r in rows if len(r["scen"]) > 80]
    print("納入比對 %d 題（情境 >80 字元；太短的殼題判不了，另外列）" % len(long_rows))

    used, clusters = set(), []
    for i, a in enumerate(long_rows):
        if i in used:
            continue
        grp = [a]
        used.add(i)
        for j in range(i + 1, len(long_rows)):
            if j in used:
                continue
            if jac(a["scen"], long_rows[j]["scen"]) >= 0.92:
                grp.append(long_rows[j])
                used.add(j)
        if len(grp) > 1:
            clusters.append(grp)

    真重複, 系列題 = [], []
    for grp in clusters:
        # 群內再依「解法」細分：解法一樣才算重複
        buckets = []
        for r in grp:
            for b in buckets:
                if jac(r["sol"], b[0]["sol"]) >= 0.92 or (not r["sol"] and not b[0]["sol"]):
                    b.append(r)
                    break
            else:
                buckets.append([r])
        for b in buckets:
            if len(b) > 1:
                真重複.append(b)
        if len(buckets) > 1:
            系列題.append((grp, buckets))

    dup_extra = sum(len(b) - 1 for b in 真重複)
    print()
    print("真重複（情境與解法都相同）      %3d 組，多出來 %3d 題" % (len(真重複), dup_extra))
    print("系列題（同情境、不同解法）      %3d 組，共 %3d 題 ← 這些是不同的題，不能砍"
          % (len(系列題), sum(len(g) for g, _ in 系列題)))
    print()
    print("所以「AZ-104 有幾題」有三個答案：")
    print("   原始題數合計          %3d" % len(rows))
    print("   只看 470Q 那一份      %3d" % sum(1 for r in rows if r["tag"].startswith("470")))
    print("   扣掉真重複的唯一題數  %3d" % (len(rows) - dup_extra))

    cross = [b for b in 真重複 if len({r["tag"] for r in b}) > 1]
    print()
    print("真重複裡有 %d 組是跨檔案的（增題其實已經在 470Q 裡）" % len(cross))
    conflict = [b for b in 真重複 if len({(r["ans"] or "").strip()[:20] for r in b if r["ans"]}) > 1]
    print("真重複裡有 %d 組**標的答案互相矛盾**，轉錄到那幾題要人工裁決" % len(conflict))

    if "--series" in sys.argv:
        print_series(系列題)
        return

    if "--list" not in sys.argv:
        print("\n（加 --list 看每一組，--series 只看系列題）")
        return

    print("\n=== 真重複 · 標的答案矛盾 ===")
    for b in conflict:
        ans = sorted({(r["ans"] or "—").strip()[:22] for r in b})
        print("  %-58s ans=%s" % (" | ".join(short(r) for r in b), " / ".join(ans)))
    print("\n=== 真重複 · 答案一致（留一題就好）===")
    for b in 真重複:
        if b in conflict:
            continue
        print("  %-58s ans=%s" % (" | ".join(short(r) for r in b),
                                  (b[0]["ans"] or "—")[:22]))
    print("\n=== 系列題（同情境、不同解法，全部都要收）===")
    for grp, buckets in 系列題:
        print("  %d 題 / %d 種解法：%s"
              % (len(grp), len(buckets), " | ".join(short(r) for r in grp)))


if __name__ == "__main__":
    main()
