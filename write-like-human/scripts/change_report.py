#!/usr/bin/env python3
"""Make a Word file that shows every change between two versions of a text.

  python change_report.py before.txt after.txt -o letter-changes.docx
  python change_report.py report.docx report-humanized.docx

BEFORE and AFTER can each be .txt, .md, or .docx. Paragraphs are matched
in order and compared word by word. Removed words are shown in red with a
line through them. Added words are shown in green and underlined. Text
that did not change is shown normally. A short note at the top explains
what the file is.

The default output name is <after-name>-changes.docx. The script refuses
to write over either input file.

Only uses python-docx and the standard library.
"""

import argparse
import difflib
import os
import re
import sys

try:
    from docx import Document
    from docx.shared import RGBColor, Pt
    from docx.enum.text import WD_UNDERLINE
except ImportError:  # pragma: no cover
    sys.exit("python-docx is not installed. Show the changes side by side in the chat instead.")

TOKEN_RE = re.compile(r"\s+|[^\s]+")
RED = RGBColor(0xC0, 0x00, 0x00)
GREEN = RGBColor(0x00, 0x80, 0x00)


def read_paragraphs(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".docx":
        doc = Document(path)
        paras = [p.text for p in doc.paragraphs]
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    paras.extend(p.text for p in cell.paragraphs)
        return [p for p in paras if p.strip()]
    with open(path, encoding="utf-8-sig") as fh:
        text = fh.read().replace("\r\n", "\n")
    # Word files cannot hold control characters. A form feed (a page break
    # in text saved from a PDF) starts a new paragraph, a vertical tab is a
    # line break, and the rest are dropped.
    text = text.replace("\f", "\n\n").replace("\v", "\n")
    text = re.sub(r"[\x00-\x08\x0e-\x1f]", "", text)
    return [p.strip("\n") for p in re.split(r"\n\s*\n", text) if p.strip()]


def add(paragraph, text, kind):
    run = paragraph.add_run(text)
    if kind == "del":
        run.font.strike = True
        run.font.color.rgb = RED
    elif kind == "ins":
        run.font.underline = WD_UNDERLINE.SINGLE
        run.font.color.rgb = GREEN
    return run


def diff_words(paragraph, old, new):
    a, b = TOKEN_RE.findall(old), TOKEN_RE.findall(new)
    changed = False
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            add(paragraph, "".join(a[i1:i2]), None)
            continue
        changed = True
        if op in ("delete", "replace"):
            add(paragraph, "".join(a[i1:i2]), "del")
            if op == "replace":
                add(paragraph, " ", None)
        if op in ("insert", "replace"):
            add(paragraph, "".join(b[j1:j2]), "ins")
    return changed


def build(before, after, out_path, title):
    doc = Document()
    doc.add_heading("Changes: %s" % title, level=1)
    note = doc.add_paragraph()
    note.add_run("This file shows what changed. ")
    add(note, "Red with a line through it", "del")
    note.add_run(" was removed. ")
    add(note, "Green and underlined", "ins")
    note.add_run(" was added. Everything else is the same as before. "
                 "This is a report to read, not the finished document.")
    for r in note.runs:
        r.font.size = Pt(9)

    changed = 0
    matcher = difflib.SequenceMatcher(None, before, after, autojunk=False)
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == "equal":
            for p in before[i1:i2]:
                doc.add_paragraph(p)
        elif op == "delete":
            for p in before[i1:i2]:
                add(doc.add_paragraph(), p, "del")
                changed += 1
        elif op == "insert":
            for p in after[j1:j2]:
                add(doc.add_paragraph(), p, "ins")
                changed += 1
        else:
            olds, news = before[i1:i2], after[j1:j2]
            for k in range(max(len(olds), len(news))):
                old = olds[k] if k < len(olds) else ""
                new = news[k] if k < len(news) else ""
                para = doc.add_paragraph()
                if not old:
                    add(para, new, "ins")
                    changed += 1
                elif not new:
                    add(para, old, "del")
                    changed += 1
                elif diff_words(para, old, new):
                    changed += 1
    doc.save(out_path)
    return changed


def main():
    parser = argparse.ArgumentParser(description="Word file showing every change between two texts.")
    parser.add_argument("before", help="original .txt, .md, or .docx")
    parser.add_argument("after", help="rewritten .txt, .md, or .docx")
    parser.add_argument("-o", "--output", help="output path (default: <after-name>-changes.docx)")
    args = parser.parse_args()

    out_path = args.output or os.path.splitext(args.after)[0] + "-changes.docx"
    out_abs = os.path.abspath(out_path)
    if out_abs in (os.path.abspath(args.before), os.path.abspath(args.after)):
        sys.exit("Refusing to overwrite an input file. Pick another output name.")
    before, after = read_paragraphs(args.before), read_paragraphs(args.after)
    title = os.path.basename(args.before)
    changed = build(before, after, out_path, title)
    print("Saved %s (%d paragraphs with changes)" % (out_path, changed))


if __name__ == "__main__":
    main()
