#!/usr/bin/env python3
"""Make a Word document easier to read without changing a single word.

  python docx_layout.py letter.docx --dyslexia
  python docx_layout.py letter.docx --dyslexia -o letter-easy.docx

--dyslexia applies a layout many readers with dyslexia find easier:
  - body text in a clear sans-serif font (Arial by default, or --font Verdana)
  - body text at least 12 pt; larger text, such as headings, keeps its size
  - 1.5 line spacing and a little space after each paragraph
  - body paragraphs aligned left (no justified text, which makes uneven gaps)
  - italics removed from long runs (more than 10 words); short italics,
    such as a book title, stay

Headings keep their style and alignment. Tables, images, headers and
footers, and every word stay as they were. The result is saved as
<name>-readable.docx and the original is never overwritten.

Only uses the standard library plus python-docx.
"""

import argparse
import os
import sys

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Pt

MIN_SIZE = Pt(12)


def readable_path(path):
    root, ext = os.path.splitext(path)
    return "%s-readable%s" % (root, ext)


def is_heading(paragraph):
    name = (paragraph.style.name or "").lower() if paragraph.style is not None else ""
    return name.startswith("heading") or name == "title" or name == "subtitle"


def set_font(run, font):
    run.font.name = font
    rpr = run._r.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = rpr.makeelement(qn("w:rFonts"), {})
        rpr.insert(0, rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs"):
        rfonts.set(qn(attr), font)


def effective_size(run, paragraph):
    if run.font.size is not None:
        return run.font.size
    style = paragraph.style
    while style is not None:
        if style.font is not None and style.font.size is not None:
            return style.font.size
        style = style.base_style
    return None


def table_paragraphs(tables):
    for table in tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    yield p
                for p in table_paragraphs(cell.tables):
                    yield p


def body_paragraphs(doc):
    for p in doc.paragraphs:
        yield p
    for p in table_paragraphs(doc.tables):
        yield p


def paragraph_runs(p):
    """The paragraph's runs, including the ones inside links."""
    if not hasattr(p, "iter_inner_content"):  # python-docx before 1.0
        return p.runs
    runs = []
    for item in p.iter_inner_content():
        runs.extend(item.runs if hasattr(item, "runs") else [item])
    return runs


def apply_dyslexia(doc, font):
    changed = 0
    normal = doc.styles["Normal"]
    normal.font.name = font
    if normal.font.size is None or normal.font.size < MIN_SIZE:
        normal.font.size = MIN_SIZE
    seen = set()
    for p in body_paragraphs(doc):
        if id(p._p) in seen:
            continue
        seen.add(id(p._p))
        if not p.text.strip():
            continue
        heading = is_heading(p)
        fmt = p.paragraph_format
        if not heading:
            fmt.line_spacing = 1.5
            fmt.space_after = Pt(8)
            if fmt.alignment in (None, WD_ALIGN_PARAGRAPH.JUSTIFY, WD_ALIGN_PARAGRAPH.DISTRIBUTE):
                fmt.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in paragraph_runs(p):
            if not run.text:
                continue
            if not heading:
                set_font(run, font)
                size = effective_size(run, p)
                if size is None or size < MIN_SIZE:
                    run.font.size = MIN_SIZE
                if run.italic and len(run.text.split()) > 10:
                    run.italic = False
        changed += 1
    return changed


def main():
    parser = argparse.ArgumentParser(description="Make a Word document easier to read without changing its words.")
    parser.add_argument("file")
    parser.add_argument("--dyslexia", action="store_true", help="apply the dyslexia-friendly layout")
    parser.add_argument("--font", default="Arial", choices=["Arial", "Verdana", "Calibri", "Tahoma"],
                        help="clear sans-serif font for body text (default Arial)")
    parser.add_argument("-o", "--output", help="output path (default: <name>-readable.docx)")
    args = parser.parse_args()
    if not args.dyslexia:
        parser.error("choose a layout, for example --dyslexia")
    out = args.output or readable_path(args.file)
    if os.path.abspath(out) == os.path.abspath(args.file):
        sys.exit("Refusing to overwrite the original. Choose a different output name.")
    doc = Document(args.file)
    n = apply_dyslexia(doc, args.font)
    doc.save(out)
    print("Wrote %s. Updated the layout of %d paragraphs. No words were changed." % (out, n))


if __name__ == "__main__":
    main()
