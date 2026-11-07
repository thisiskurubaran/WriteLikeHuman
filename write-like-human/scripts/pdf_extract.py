#!/usr/bin/env python3
"""Pull text out of a PDF page by page, and turn rewritten text into Word.

A PDF cannot be edited in place in any reliable way, so the result of a
rewrite is always a new, editable Word file.

  1. extract: get the text of each page and flag pages that look scanned
     (a photo of a page, with little or no real text in it).

       python pdf_extract.py extract letter.pdf -o pages.json
       python pdf_extract.py extract letter.pdf --markdown

     JSON shape:
       {"file": "letter.pdf", "pages": [
          {"page": 1, "text": "...", "words": 312, "scanned": false},
          {"page": 2, "text": "", "words": 0, "scanned": true}],
        "scanned_pages": [2]}

  2. to-docx: after rewriting, write the text into a Word file. Give it
     the same JSON with the "text" of each page replaced. Blank lines
     separate paragraphs. Lines that start with "# " or "## " become
     headings, lines that start with "- " become bullet points. Each PDF
     page starts on a new Word page unless --no-page-breaks is given.

       python pdf_extract.py to-docx letter.pdf pages-rewritten.json

     Saved as letter-humanized.docx. The PDF itself is not changed.

Only uses pypdf, python-docx, and the standard library.
"""

import argparse
import json
import os
import re
import sys

SCANNED_MIN_CHARS = 30


def humanized_docx_path(path):
    root, _ = os.path.splitext(path)
    return root + "-humanized.docx"


def word_count(text):
    return len([w for w in text.split() if any(c.isalnum() for c in w)])


def page_has_images(page):
    try:
        resources = page.get("/Resources") or {}
        xobjects = resources.get("/XObject") if hasattr(resources, "get") else None
        if not xobjects:
            return False
        xobjects = xobjects.get_object()
        for name in xobjects:
            obj = xobjects[name].get_object()
            if obj.get("/Subtype") == "/Image":
                return True
    except Exception:
        return False
    return False


def tidy(text):
    """Join lines broken by the PDF layout back into paragraphs."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Words split across lines with a hyphen: "exam-\nple" -> "example".
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
    paragraphs = re.split(r"\n\s*\n", text)
    cleaned = []
    for para in paragraphs:
        lines = [ln.strip() for ln in para.split("\n") if ln.strip()]
        if not lines:
            continue
        # Keep bullet-like lines on their own, join the rest.
        out, buf = [], []
        for ln in lines:
            if re.match(r"^([-*•]|\d+[.)])\s", ln):
                if buf:
                    out.append(" ".join(buf))
                    buf = []
                out.append(ln)
            else:
                buf.append(ln)
        if buf:
            out.append(" ".join(buf))
        cleaned.append("\n".join(out))
    return "\n\n".join(cleaned)


def cmd_extract(args):
    try:
        from pypdf import PdfReader
    except ImportError:
        sys.exit("pypdf is not installed. Read the PDF with Claude's own PDF handling instead.")
    reader = PdfReader(args.file)
    if reader.is_encrypted:
        try:
            reader.decrypt("")
        except Exception:
            sys.exit("This PDF is password protected. Ask the user for an unlocked copy.")
    pages = []
    for i, page in enumerate(reader.pages, start=1):
        try:
            raw = page.extract_text() or ""
        except Exception:
            raw = ""
        text = raw if args.raw else tidy(raw)
        visible = len(re.sub(r"\s", "", text))
        scanned = visible < SCANNED_MIN_CHARS and (page_has_images(page) or visible == 0)
        pages.append({"page": i, "text": text, "words": word_count(text), "scanned": scanned})
    scanned_pages = [p["page"] for p in pages if p["scanned"]]

    if args.markdown:
        parts = []
        for p in pages:
            note = " (looks scanned, no text found)" if p["scanned"] else ""
            parts.append("## Page %d%s\n\n%s" % (p["page"], note, p["text"]))
        payload = "\n\n".join(parts) + "\n"
    else:
        payload = json.dumps({"file": os.path.basename(args.file), "pages": pages,
                              "scanned_pages": scanned_pages}, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(payload)
        print("Wrote %d pages to %s" % (len(pages), args.output))
    else:
        print(payload)
    if scanned_pages:
        sys.stderr.write("NOTE: pages %s look scanned. Their text needs reading from the image.\n"
                         % ", ".join(str(n) for n in scanned_pages))


def add_block(doc, block):
    for line in block.split("\n"):
        line = line.rstrip()
        if not line:
            continue
        if line.startswith("## "):
            doc.add_heading(line[3:], level=2)
        elif line.startswith("# "):
            doc.add_heading(line[2:], level=1)
        elif re.match(r"^[-*•]\s", line):
            doc.add_paragraph(line[2:].strip(), style="List Bullet")
        elif re.match(r"^\d+[.)]\s", line):
            doc.add_paragraph(re.sub(r"^\d+[.)]\s+", "", line), style="List Number")
        else:
            doc.add_paragraph(line)


def cmd_to_docx(args):
    try:
        from docx import Document
        from docx.enum.text import WD_BREAK
    except ImportError:
        sys.exit("python-docx is not installed. Give the user the rewritten text to paste instead.")
    out_path = args.output or humanized_docx_path(args.file)
    if os.path.abspath(out_path) == os.path.abspath(args.file):
        sys.exit("Refusing to overwrite the original file.")
    with open(args.pages, encoding="utf-8") as fh:
        data = json.load(fh)
    pages = data["pages"] if isinstance(data, dict) else data
    doc = Document()
    for n, page in enumerate(pages):
        if n and not args.no_page_breaks:
            doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        for block in re.split(r"\n\s*\n", page.get("text", "")):
            add_block(doc, block)
    doc.save(out_path)
    print("Saved %s (%d pages of text)" % (out_path, len(pages)))


def main():
    parser = argparse.ArgumentParser(description="Get text out of a PDF, and put rewritten text into Word.")
    sub = parser.add_subparsers(dest="command", required=True)

    ex = sub.add_parser("extract", help="text per page, with scanned pages flagged")
    ex.add_argument("file")
    ex.add_argument("-o", "--output", help="write here instead of printing")
    ex.add_argument("--markdown", action="store_true", help="output Markdown instead of JSON")
    ex.add_argument("--raw", action="store_true", help="keep the PDF's own line breaks")
    ex.set_defaults(func=cmd_extract)

    td = sub.add_parser("to-docx", help="write rewritten page text into a new Word file")
    td.add_argument("file", help="the original PDF (used for the output name)")
    td.add_argument("pages", help="JSON with rewritten page text")
    td.add_argument("-o", "--output", help="output path (default: <name>-humanized.docx)")
    td.add_argument("--no-page-breaks", action="store_true", help="run pages together")
    td.set_defaults(func=cmd_to_docx)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
