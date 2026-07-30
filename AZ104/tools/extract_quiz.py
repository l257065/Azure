import re, json, html, os, sys

# usage: python extract_quiz.py <quiz_html_path> <out_json_path>
# quiz_html_path defaults to source/quiz20.html; question codes are read from the
# file itself (AZ104-Q\d+), so this works for any saved Build School quiz page.
#
# Handles two source layouts seen across the 20 quizzes so far:
#   - data-type="single"/"multiple": real MC questions. Options + which ones are
#     marked correct (class contains "wpProQuiz_answerCorrect") are extracted directly,
#     no need to look at a screenshot.
#   - data-type="free_answer": Quiz20-style. No real options in the HTML, only an
#     answer screenshot (…_ans.png or rIdNN.jpg) shown after "check". Must be read visually.
# Any other data-type is still emitted with raw_type set so it doesn't get silently dropped.

here = os.path.dirname(os.path.abspath(__file__))
path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "..", "source", "quiz20.html")
files_dir_name = os.path.splitext(os.path.basename(path))[0] + "_files"

with open(path, encoding="utf-8") as f:
    content = f.read()

starts = [m.start() for m in re.finditer(r'<li class="wpProQuiz_listItem"', content)]
end_marker = re.search(r'<li class="wpProQuiz_endQuizElement"', content)
end_pos = end_marker.start() if end_marker else len(content)
bounds = starts + [end_pos]
items = [content[bounds[i]:bounds[i+1]] for i in range(len(starts))]

print(f"found {len(items)} items")


def text_lines_of(frag):
    """<div>/<p> 逐行抽成文字，去標籤、去空白、丟掉空行"""
    out = []
    for l in re.findall(r'<(?:div|p)[^>]*>(.*?)</(?:div|p)>', frag, re.S):
        t = re.sub(r'<[^>]+>', '', l).strip()
        t = html.unescape(t)
        if t:
            out.append(t)
    return out


def imgs_of(frag):
    return re.findall(r'<img[^>]+src="\./' + re.escape(files_dir_name) + r'/([^"]+)"', frag)


def balanced_div(s, start):
    """s[start:] 開頭就是某個 <div ...> 的內容起點（開始標籤已經吃掉），
    回傳這個 div 自己的內容（不含它自己的收尾 </div>），用配對計數，不猜固定層數。"""
    depth = 1
    for m in re.finditer(r'<div\b|</div>', s[start:]):
        if m.group(0) == '</div>':
            depth -= 1
            if depth == 0:
                return s[start:start + m.start()]
        else:
            depth += 1
    return s[start:]  # 沒配到就整段吃完，保底


results = []
for it in items:
    m_type = re.search(r'<li class="wpProQuiz_listItem"[^>]*data-type="([a-z_]+)"', it)
    raw_type = m_type.group(1) if m_type else None

    m_code = re.search(r'<strong>(AZ104-Q\d+)</strong>', it) or re.search(r'(AZ104-Q\d+)', it)
    code = m_code.group(1) if m_code else None

    m_qnum = re.search(r'題 <span>(\d+)</span> of <span>(\d+)</span>', it)

    m_cat = re.search(r'類別：<span>([^<]*)</span>', it)
    category = m_cat.group(1).strip() if m_cat else None
    if category in ("", "None"):
        category = None

    m_legend = re.search(r'<legend class="wpProQuiz_question_text">(.*?)</legend>', it, re.S)
    legend_html = m_legend.group(1) if m_legend else ""
    inline_images = imgs_of(legend_html)
    legend_html_stripped = re.sub(r'<div><strong>AZ104-Q\d+</strong></div>', '', legend_html)
    question_text = "\n".join(text_lines_of(legend_html_stripped))

    # ---- options (single/multiple only) ------------------------------------------------
    options = None
    if raw_type in ("single", "multiple"):
        m_list = re.search(r'<div class="wpProQuiz_questionList"[^>]*>(.*?)</fieldset>', it, re.S)
        list_html = m_list.group(1) if m_list else ""
        opt_blocks = re.findall(
            r'<div class="wpProQuiz_questionListItem([^"]*)"[^>]*data-pos="(\d+)">(.*?)</div>\s*(?=<div class="wpProQuiz_questionListItem"|<div class="wpProQuiz_questionListItem |</div>\s*</div>\s*$|$)',
            list_html, re.S
        )
        # 上面的 lookahead 對最後一個 item 不穩定，改用更簡單的切法：先找出所有 data-pos 開頭位置
        pos_starts = [m.start() for m in re.finditer(r'<div class="wpProQuiz_questionListItem[^"]*"[^>]*data-pos="\d+">', list_html)]
        pos_starts.append(len(list_html))
        options = []
        for i in range(len(pos_starts) - 1):
            block = list_html[pos_starts[i]:pos_starts[i+1]]
            m_head = re.match(r'<div class="wpProQuiz_questionListItem([^"]*)"[^>]*data-pos="(\d+)">', block)
            cls = m_head.group(1) if m_head else ""
            correct = "wpProQuiz_answerCorrect" in cls
            # option text: last <span>...</span> inside the <label>, drop the "1. " hidden index span
            m_label = re.search(r'<label>(.*?)</label>', block, re.S)
            label_html = m_label.group(1) if m_label else ""
            m_txt = re.findall(r'<span>(.*?)</span>', label_html, re.S)
            opt_text = ""
            if m_txt:
                opt_text = re.sub(r'<[^>]+>', '', m_txt[-1]).strip()
                opt_text = html.unescape(opt_text)
            options.append({"text": opt_text, "correct": correct})

    # ---- answer image(s) + explanation text (wpProQuiz_incorrect / AnswerMessage) --------
    # "正確"（correct）那個區塊永遠有一個空的 AnswerMessage，"不正確"（incorrect）那個才是真內容，
    # 用 balanced_div 從 incorrect 區塊開始找，不要讓固定層數的 </div> 數量把兩段黏在一起。
    answer_images, explanation = [], ""
    m_incorrect = re.search(r'class="wpProQuiz_incorrect">', it)
    if m_incorrect:
        m_msg = re.search(r'class="wpProQuiz_AnswerMessage">', it[m_incorrect.end():])
        if m_msg:
            msg_start = m_incorrect.end() + m_msg.end()
            msg_html = balanced_div(it, msg_start)
            answer_images = imgs_of(msg_html)
            msg_html = re.sub(r'<img[^>]*>', '', msg_html)
            msg_html = re.sub(r'<strong>Explanation:</strong>', '', msg_html)
            explanation = "\n".join(text_lines_of(msg_html))

    entry = {
        "code": code,
        "qnum": int(m_qnum.group(1)) if m_qnum else None,
        "qtotal": int(m_qnum.group(2)) if m_qnum else None,
        "raw_type": raw_type,
        "category": category,
        "question": question_text,
        "inline_images": inline_images,
        "answer_images": answer_images,
        "explanation": explanation,
    }
    if options is not None:
        entry["options"] = options
    results.append(entry)

out_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "..", "source", "quiz20_questions.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("wrote", out_path)
by_type = {}
for r in results:
    by_type[r["raw_type"]] = by_type.get(r["raw_type"], 0) + 1
print("by raw_type:", by_type)
no_correct = [r["code"] for r in results if r.get("options") is not None and not any(o["correct"] for o in r["options"])]
if no_correct:
    print("WARNING no option marked correct:", no_correct)
