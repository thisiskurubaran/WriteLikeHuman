#!/usr/bin/env python3
"""Split a long document into sections, and list terms to keep consistent.

For theses, long reports, and manuals that are too big to rewrite in one go.

  python doc_sections.py outline thesis.docx
  python doc_sections.py outline report.pdf --json
  python doc_sections.py terms thesis.docx

outline lists the sections in order, each with an id (s1, s2, ...), its
heading, a word count, and where it sits:
  - Word (.docx): sections start at each heading (Heading 1 to 3, Title,
    or any paragraph with an outline level). Each section lists the
    paragraph ids it covers, the same ids docx_rewrite.py uses, so you can
    extract and apply one section at a time.
  - Markdown (.md): sections start at each # heading. Ranges are line
    numbers.
  - Plain text (.txt) without headings and PDF: sections are chunks of
    about --words words (default 2500), split at paragraph or page breaks.
    Ranges are line numbers for text and page numbers for PDF.

terms lists things that must stay the same across sections:
  - names and capitalised terms that appear at least --min times
  - spelling variants found in the same document, such as "colour" and
    "color", or "e-mail" and "email", with how often each appears
Use it to build a short consistency sheet before rewriting.

Only uses the standard library plus python-docx and pypdf.
"""

import argparse
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

WORD = re.compile(r"[^\W\d_][\w'’-]*", re.UNICODE)

# Pairs of spellings that often get mixed in one document.
VARIANT_PAIRS = [
    ("colour", "color"), ("favour", "favor"), ("behaviour", "behavior"), ("honour", "honor"),
    ("labour", "labor"), ("centre", "center"), ("metre", "meter"), ("litre", "liter"),
    ("theatre", "theater"), ("organise", "organize"), ("organisation", "organization"),
    ("realise", "realize"), ("recognise", "recognize"), ("analyse", "analyze"), ("prioritise", "prioritize"),
    ("licence", "license"), ("defence", "defense"), ("programme", "program"), ("catalogue", "catalog"),
    ("travelled", "traveled"), ("cancelled", "canceled"), ("modelling", "modeling"), ("judgement", "judgment"),
    ("e-mail", "email"), ("on-line", "online"), ("web site", "website"), ("data base", "database"),
    ("co-operate", "cooperate"), ("per cent", "percent"), ("towards", "toward"), ("whilst", "while"),
]

COMMON_CAPITALISED = {
    "The", "A", "An", "In", "On", "At", "For", "And", "But", "Or", "If", "When", "This", "That", "These",
    "Those", "It", "We", "I", "You", "They", "He", "She", "Our", "Their", "As", "Of", "To", "By", "With",
    "From", "Is", "Are", "Was", "Were", "Be", "Not", "No", "Yes", "So", "All", "Each", "One", "Two",
    "Table", "Figure", "Chapter", "Section", "Page", "Mr", "Mrs", "Ms", "Dr",
}


def words(text):
    return len(WORD.findall(text))


# ---------------------------------------------------------------- Word

def docx_heading_level(p_el, style_names):
    from docx.oxml.ns import qn
    ppr = p_el.find(qn("w:pPr"))
    if ppr is None:
        return None
    lvl = ppr.find(qn("w:outlineLvl"))
    if lvl is not None and lvl.get(qn("w:val"), "").isdigit():
        n = int(lvl.get(qn("w:val"))) + 1
        return n if n <= 9 else None
    style = ppr.find(qn("w:pStyle"))
    if style is None:
        return None
    name = style_names.get(style.get(qn("w:val")), style.get(qn("w:val")) or "")
    low = name.lower().replace(" ", "")
    if low == "title":
        return 0
    m = re.match(r"heading(\d)$", low)
    if m and int(m.group(1)) <= 3:
        return int(m.group(1))
    return None


def outline_docx(path):
    from docx import Document
    import docx_rewrite
    doc = Document(path)
    style_names = {s.style_id: s.name for s in doc.styles}
    sections = []
    current = None
    for pid, where, p in docx_rewrite.collect_paragraphs(doc):
        if where in ("header", "footer"):
            continue
        text = docx_rewrite.para_text(p)
        level = docx_heading_level(p, style_names) if text.strip() else None
        if level is not None or current is None:
            current = {"heading": text.strip() if level is not None else "(start)",
                       "level": level, "first": pid, "last": pid, "words": 0, "paragraphs": []}
            sections.append(current)
        current["last"] = pid
        if text.strip():
            current["paragraphs"].append(pid)
            current["words"] += words(text)
    out = []
    for i, s in enumerate(sections, 1):
        if not s["paragraphs"]:
            continue
        out.append({"id": "s%d" % i, "heading": s["heading"], "level": s["level"], "words": s["words"],
                    "range": "%s to %s" % (s["paragraphs"][0], s["paragraphs"][-1]),
                    "paragraph_ids": s["paragraphs"]})
    return renumber(out), "paragraph ids"


def docx_text(path):
    from docx import Document
    import docx_rewrite
    doc = Document(path)
    return "\n".join(docx_rewrite.para_text(p) for _, _, p in docx_rewrite.collect_paragraphs(doc))


# ---------------------------------------------------------------- text and PDF

def outline_markdown(lines):
    sections, current = [], None
    in_code = False
    for n, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            in_code = not in_code
        m = None if in_code else re.match(r"^(#{1,3})\s+(.*\S)\s*#*\s*$", line)
        if m or current is None:
            current = {"heading": m.group(2) if m else "(start)", "level": len(m.group(1)) if m else None,
                       "first": n, "last": n, "words": 0}
            sections.append(current)
        current["last"] = n
        current["words"] += words(line)
    out = [{"id": "", "heading": s["heading"], "level": s["level"], "words": s["words"],
            "range": "lines %d to %d" % (s["first"], s["last"])} for s in sections if s["words"]]
    return renumber(out)


def chunk_blocks(blocks, target, unit):
    """blocks: list of (start, end, text). Group into chunks of about target words."""
    out, start, count = [], None, 0
    for i, (first, last_num, text) in enumerate(blocks):
        if start is None:
            start = first
        count += words(text)
        if count >= target or i == len(blocks) - 1:
            out.append({"id": "", "heading": "(part)", "level": None, "words": count,
                        "range": "%s %s to %s" % (unit, start, last_num)})
            start, count = None, 0
    return renumber([o for o in out if o["words"]])


def outline_text(path, target):
    with open(path, encoding="utf-8-sig") as fh:
        lines = fh.read().splitlines()
    if any(re.match(r"^#{1,3}\s+\S", l) for l in lines):
        return outline_markdown(lines), "line numbers"
    blocks, buf, start = [], [], None
    for n, line in enumerate(lines, 1):
        if line.strip():
            if start is None:
                start = n
            buf.append(line)
        elif buf:
            blocks.append((start, n - 1, " ".join(buf)))
            buf, start = [], None
    if buf:
        blocks.append((start, len(lines), " ".join(buf)))
    return chunk_blocks(blocks, target, "lines"), "line numbers"


def outline_pdf(path, target):
    from pypdf import PdfReader
    reader = PdfReader(path)
    pages = [(i, i, page.extract_text() or "") for i, page in enumerate(reader.pages, 1)]
    return chunk_blocks(pages, target, "pages"), "page numbers"


def pdf_text(path):
    from pypdf import PdfReader
    return "\n".join(page.extract_text() or "" for page in PdfReader(path).pages)


def renumber(sections):
    for i, s in enumerate(sections, 1):
        s["id"] = "s%d" % i
    return sections


# ---------------------------------------------------------------- terms

def find_terms(text, min_count):
    counts = collections.Counter()
    for sentence in re.split(r"(?<=[.!?])\s+|\n+", text):
        tokens = re.findall(r"[A-Z][\w’'-]*(?:\s+[A-Z][\w’'-]*)*", sentence)
        for tok in tokens:
            parts = tok.split()
            while parts and parts[0] in COMMON_CAPITALISED:
                parts.pop(0)
            if not parts:
                continue
            counts[" ".join(parts)] += 1
    terms = [{"term": t, "count": n} for t, n in counts.most_common() if n >= min_count]
    lower = text.lower()
    variants = []
    for a, b in VARIANT_PAIRS:
        na = len(re.findall(r"\b%s\w*" % re.escape(a), lower))
        nb = len(re.findall(r"\b%s\w*" % re.escape(b), lower))
        if na and nb:
            variants.append({"spellings": {a: na, b: nb}})
    return terms, variants


# ---------------------------------------------------------------- commands

def load_outline(path, target):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".docx":
        return outline_docx(path)
    if ext == ".pdf":
        return outline_pdf(path, target)
    if ext in (".md", ".markdown", ".txt", ".text"):
        return outline_text(path, target)
    sys.exit("Use a .docx, .pdf, .md, or .txt file.")


def load_text(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".docx":
        return docx_text(path)
    if ext == ".pdf":
        return pdf_text(path)
    with open(path, encoding="utf-8-sig") as fh:
        return fh.read()


def cmd_outline(args):
    sections, unit = load_outline(args.file, args.words)
    total = sum(s["words"] for s in sections)
    if args.json:
        print(json.dumps({"file": os.path.basename(args.file), "unit": unit, "total_words": total,
                          "sections": sections}, ensure_ascii=False, indent=2))
        return
    print("%s: %d sections, about %d words. Ranges are %s." % (os.path.basename(args.file), len(sections), total, unit))
    for s in sections:
        indent = "  " * max((s["level"] or 1) - 1, 0)
        print("%-4s %s%s  (%d words, %s)" % (s["id"], indent, s["heading"], s["words"], s["range"]))


def cmd_terms(args):
    terms, variants = find_terms(load_text(args.file), args.min)
    if args.json:
        print(json.dumps({"terms": terms, "variants": variants}, ensure_ascii=False, indent=2))
        return
    print("Names and terms used %d or more times:" % args.min)
    for t in terms[:60]:
        print("  %4d  %s" % (t["count"], t["term"]))
    if not terms:
        print("  (none)")
    print("Spellings used two ways in this document:")
    for v in variants:
        print("  " + ", ".join("%s x%d" % kv for kv in v["spellings"].items()))
    if not variants:
        print("  (none found)")


def main():
    parser = argparse.ArgumentParser(description="Split a long document into sections and list terms to keep consistent.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    o = sub.add_parser("outline", help="list the sections in order")
    o.add_argument("file")
    o.add_argument("--words", type=int, default=2500, help="target words per chunk when there are no headings")
    o.add_argument("--json", action="store_true")
    o.set_defaults(func=cmd_outline)
    t = sub.add_parser("terms", help="list names, terms, and spelling variants")
    t.add_argument("file")
    t.add_argument("--min", type=int, default=3, help="minimum times a term must appear (default 3)")
    t.add_argument("--json", action="store_true")
    t.set_defaults(func=cmd_terms)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
