# -*- coding: utf-8 -*-
"""核對原文（mg:true 那 40 題）用的共用小工具。

用法：在批次腳本裡 import，然後對每一題呼叫 patch()。
會做三件事：
  1. 依 line_edits 換掉整行欄位（tgt / items / sent / dd / a / q …）
  2. 依 text_subs 換掉題目區塊裡的片段（主要用來同步解析裡的【…】小標）
  3. 補上 vf:true 與 v0（原文對照），v0 插在 e: 之前

每筆資料在 bank_doc.current.js 裡都是「一行 {n:NNN, 開頭」到「下一筆 {n: 開頭」之間，
所以用行首當錨點就夠了，不需要真的 parse JS。
"""
import io, os

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "bank_doc.current.js")


def js(s):
    """轉成 JS 字串字面值，換行寫成 \\n，與檔案裡既有的寫法一致。"""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def arr(items):
    return "[" + ",".join(js(x) for x in items) + "]"


def arr2(groups):
    return "[" + ",".join(arr(g) for g in groups) + "]"


def load():
    with io.open(SRC, encoding="utf-8") as f:
        return f.readlines()


def save(lines):
    with io.open(SRC, "w", encoding="utf-8") as f:
        f.writelines(lines)


def _span(lines, n):
    head = "{n:%d," % n
    start = next((i for i, L in enumerate(lines) if L.startswith(head)), None)
    if start is None:
        raise KeyError("找不到 #%d" % n)
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("{n:")), len(lines))
    return start, end


def patch(lines, n, v0, line_edits=(), text_subs=()):
    """line_edits: [(行首字串, 新的整行內容不含換行)]；每個行首在該題必須剛好命中一行。
       text_subs : [(舊片段, 新片段)]；每個舊片段在該題必須至少出現一次。"""
    start, end = _span(lines, n)
    blk = lines[start:end]

    for prefix, newline in line_edits:
        hit = [i for i, L in enumerate(blk) if L.startswith(prefix)]
        if len(hit) != 1:
            raise ValueError("#%d 行首 %r 命中 %d 行" % (n, prefix, len(hit)))
        blk[hit[0]] = newline + "\n"

    text = "".join(blk)
    for old, new in text_subs:
        if old not in text:
            raise ValueError("#%d 找不到片段 %r" % (n, old[:40]))
        text = text.replace(old, new)

    if "vf:true" not in text:
        if "mg:true," not in text:
            raise ValueError("#%d 沒有 mg:true" % n)
        text = text.replace("mg:true,", "mg:true, vf:true,", 1)

    blk = text.splitlines(True)
    if v0 is not None and not any(L.startswith(" v0:") for L in blk):
        ei = next(i for i, L in enumerate(blk) if L.startswith(" e:"))
        blk.insert(ei, " v0:" + js(v0) + ",\n")

    lines[start:end] = blk
    return lines
