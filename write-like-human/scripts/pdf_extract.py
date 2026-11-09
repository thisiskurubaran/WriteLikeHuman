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

  3. images: save the pictures inside chosen pages, so a scanned page
     can be read from its image. Prints one saved path per line.

       python pdf_extract.py images letter.pdf --pages 2,3 --out page-images

     If a page has no picture inside it, the script says so. Ask the
     user for a photo or screenshot of that page instead.

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


BULLET = re.compile(r"^([-*\u2022\u25aa\u25cf]|\(?\d{1,3}[.)]|\(?[a-zA-Z][.)])\s")
SALUTATION = re.compile(
    r"^(dear|respected|hi|hello|to|sir|madam|yours\s+(sincerely|faithfully|truly)|"
    r"regards|warm regards|best regards|thanks|thank you|sincerely)\b.{0,60}[,:]?$",
    re.IGNORECASE)
SENTENCE_END = re.compile(r"[.!?:;\u0964][\"')\]]*$")


def _median(values):
    values = sorted(values)
    if not values:
        return 0
    mid = len(values) // 2
    return values[mid] if len(values) % 2 else (values[mid - 1] + values[mid]) / 2.0


def page_lines(page):
    """Lines of a page with their height on the page and font size.

    Uses pypdf's text visitor when it works. Returns a list of dicts
    {"text", "y", "size"}; y and size are None when positions are not
    available, and the caller falls back to text-only rules.
    """
    frags = []

    def visit(text, cm, tm, font, size):
        if not text:
            return
        try:
            y = tm[4] * cm[1] + tm[5] * cm[3] + cm[5]
            scale = abs(tm[3] * cm[3]) or 1.0
            frags.append((text, round(y, 1), (size or 0) * scale))
        except Exception:
            frags.append((text, None, None))

    try:
        raw = page.extract_text(visitor_text=visit) or ""
    except Exception:
        raw, frags = "", []
    lines, cur, cur_y, cur_size = [], "", None, None

    def push():
        if cur.strip() or cur == "":
            lines.append({"text": cur.strip(), "y": cur_y, "size": cur_size})

    for text, y, size in frags:
        parts = text.split("\n")
        for i, part in enumerate(parts):
            if i > 0:
                push()
                cur, cur_y, cur_size = "", None, None
            if part == "":
                continue
            if cur and y is not None and cur_y is not None and abs(y - cur_y) > 2:
                push()
                cur, cur_y, cur_size = "", None, None
            cur = cur + part if cur else part
            if cur_y is None:
                cur_y, cur_size = y, size
    push()
    # Drop empty duplicates created by explicit newlines; keep real blank lines
    # only when they separate text.
    cleaned = []
    for ln in lines:
        if not ln["text"] and (not cleaned or not cleaned[-1]["text"]):
            continue
        cleaned.append(ln)
    if not any(ln["text"] for ln in cleaned):
        return [{"text": t.strip(), "y": None, "size": None} for t in raw.split("\n")]
    return cleaned


def join_lines(lines):
    """Join PDF lines into paragraphs and keep real paragraph breaks.

    A new paragraph starts at a blank line, a bullet or numbered item, the
    line after a greeting or sign-off ("Dear Mr Sharma,"), the line after a
    short line, a bigger vertical gap than usual, or a change of font size.
    Words split with a hyphen at a line end are joined back together.
    """
    texts = [ln["text"] for ln in lines if ln["text"]]
    if not texts:
        return ""
    typical = _median([len(t) for t in texts]) or 1
    gaps = []
    prev = None
    for ln in lines:
        if ln["text"] and ln.get("y") is not None:
            if prev is not None and prev["y"] is not None and prev["y"] > ln["y"]:
                gaps.append(prev["y"] - ln["y"])
            prev = ln
    usual_gap = _median(gaps)

    paragraphs, buf, last = [], "", None
    blank_before = False

    def new_para(line):
        if not buf or last is None:
            return False
        if blank_before or BULLET.match(line["text"]) or BULLET.match(last["text"]):
            return True
        if SALUTATION.match(last["text"]) and len(last["text"]) < 0.8 * typical:
            return True
        if len(last["text"]) < 0.6 * typical:
            return True
        if usual_gap and last.get("y") is not None and line.get("y") is not None:
            gap = last["y"] - line["y"]
            if gap > 1.5 * usual_gap:
                return True
            if SENTENCE_END.search(last["text"]) and line["text"][:1].isupper() and gap > 1.15 * usual_gap:
                return True
        if last.get("size") and line.get("size"):
            big, small = max(last["size"], line["size"]), min(last["size"], line["size"])
            if small and big / small > 1.15:
                return True
        return False

    for line in lines:
        text = line["text"]
        if not text:
            blank_before = True
            continue
        if new_para(line):
            paragraphs.append(buf)
            buf = text
        elif buf and re.search(r"[A-Za-z]-$", buf) and text[:1].islower():
            buf = buf[:-1] + text
        else:
            buf = (buf + " " + text) if buf else text
        last, blank_before = line, False
    if buf:
        paragraphs.append(buf)

    out = []
    for i, para in enumerate(paragraphs):
        if i and BULLET.match(para) and BULLET.match(paragraphs[i - 1]):
            out.append("\n" + para)
        else:
            out.append(("\n\n" if i else "") + para)
    return "".join(out)


def tidy(text):
    """Join lines broken by the PDF layout back into paragraphs (text only)."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return join_lines([{"text": ln.strip(), "y": None, "size": None} for ln in text.split("\n")])


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
        if args.raw:
            try:
                text = page.extract_text() or ""
            except Exception:
                text = ""
        else:
            text = join_lines(page_lines(page))
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
        print("Wrote %d %s to %s" % (len(pages), "page" if len(pages) == 1 else "pages", args.output))
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


def parse_pages(spec, total):
    pages = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            pages.extend(range(int(a), int(b) + 1))
        else:
            pages.append(int(part))
    bad = [n for n in pages if n < 1 or n > total]
    if bad:
        sys.exit("Page %s is out of range. This PDF has %d pages." % (bad[0], total))
    return pages


def cmd_images(args):
    try:
        from pypdf import PdfReader
    except ImportError:
        sys.exit("pypdf is not installed. Look at the PDF pages directly, or ask for a photo of the page.")
    reader = PdfReader(args.file)
    total = len(reader.pages)
    pages = parse_pages(args.pages, total) if args.pages else list(range(1, total + 1))
    os.makedirs(args.out, exist_ok=True)
    base = os.path.splitext(os.path.basename(args.file))[0]
    saved = 0
    for n in pages:
        try:
            images = list(reader.pages[n - 1].images)
        except Exception as exc:  # pypdf can fail on unusual image filters
            print("PAGE %d: could not read its images (%s). Ask for a photo or screenshot of this page." % (n, exc))
            continue
        if not images:
            print("PAGE %d: no picture inside this page. Ask for a photo or screenshot of it." % n)
            continue
        for i, img in enumerate(images, start=1):
            ext = os.path.splitext(img.name)[1].lower() or ".png"
            if ext not in (".png", ".jpg", ".jpeg", ".jp2", ".tif", ".tiff", ".gif", ".bmp"):
                ext = ".png"
            path = os.path.join(args.out, "%s-page%d-%d%s" % (base, n, i, ext))
            with open(path, "wb") as fh:
                fh.write(img.data)
            print(path)
            saved += 1
    if not saved:
        sys.exit(1)


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

    im = sub.add_parser("images", help="save the pictures inside chosen pages, to read scanned pages")
    im.add_argument("file")
    im.add_argument("--pages", help="page numbers like 2,3 or 2-4 (default: all pages)")
    im.add_argument("--out", default="page-images", help="folder to save images in (default: page-images)")
    im.set_defaults(func=cmd_images)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
