#!/usr/bin/env python3
"""List and update the text cells of a spreadsheet, and nothing else.

Works on .xlsx and .csv files. Numbers, formulas, dates, true/false values,
and text that has no letters in it (phone numbers, IDs, codes like
"12-04") are never listed and never changed. Cell comments (notes) in
.xlsx files are listed too.

Two steps:

  1. extract: list text cells as JSON.

       python xlsx_text_cells.py extract budget.xlsx -o cells.json
       python xlsx_text_cells.py extract feedback.csv --min-words 4

     Ids look like "Sheet1!C7" for a cell and "Sheet1!C7#comment" for its
     comment. In a CSV the sheet name is "csv". Each item has "words" so
     you can skip short labels like "Total" or "Name". Row 1 is marked
     "header": true; leave headers alone unless the user asks, since other
     sheets or tools may look them up by name.

  2. apply: give back new text for the ids you changed.

       python xlsx_text_cells.py apply budget.xlsx changes.json

     changes.json can be {"Sheet1!C7": "new text", ...} or the edited
     output of extract. Saved as budget-humanized.xlsx (or .csv). The
     original is never overwritten. An id that points at a number,
     formula, or date is refused.

Warning for .xlsx: openpyxl, the library this uses, drops charts, images,
and some advanced features when it saves. If the workbook has any, apply
stops and says so. Use --force only after telling the user, or use the
fallback in files/spreadsheet.md instead.

Only uses openpyxl and the standard library.
"""

import argparse
import csv
import datetime
import io
import json
import os
import re
import sys
import zipfile

LETTER_RE = re.compile(r"[^\W\d_]", re.UNICODE)
NUMBER_RE = re.compile(r"\d+(?:[,.:/]\d+)*")
RISKY_PARTS = ("xl/drawings/", "xl/charts/", "xl/media/", "xl/pivotTables/", "xl/slicers/")


def humanized_path(path):
    root, ext = os.path.splitext(path)
    return "%s-humanized%s" % (root, ext)


def is_editable_text(value):
    """True only for real text: not a number, formula, date, or bare code."""
    if not isinstance(value, str):
        return False
    stripped = value.strip()
    if not stripped or stripped.startswith("="):
        return False
    return bool(LETTER_RE.search(stripped))


def word_count(text):
    return len([w for w in text.split() if any(c.isalnum() for c in w)])


def numbers_in(text):
    return sorted(NUMBER_RE.findall(text or ""))


def load_changes(path):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if isinstance(data, dict) and "cells" in data:
        return {c["id"]: c["text"] for c in data["cells"]}
    if isinstance(data, list):
        return {c["id"]: c["text"] for c in data}
    return data


def emit(args, items, label):
    out = {"file": os.path.basename(args.file), "cells": items}
    payload = json.dumps(out, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(payload)
        print("Wrote %d %s to %s" % (len(items), label, args.output))
    else:
        print(payload)


# ---------------------------------------------------------------- xlsx

def risky_parts(path):
    with zipfile.ZipFile(path) as z:
        # Comments live in legacy .vml drawing files, which openpyxl keeps.
        names = [n for n in z.namelist()
                 if not (n.startswith("xl/drawings/") and n.endswith(".vml"))]
    return sorted({p.rstrip("/") for p in RISKY_PARTS if any(n.startswith(p) for n in names)})


def xlsx_extract(args):
    from openpyxl import load_workbook
    wb = load_workbook(args.file)
    items = []
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for cell in row:
                ref = "%s!%s" % (ws.title, cell.coordinate)
                if cell.data_type == "s" and is_editable_text(cell.value):
                    words = word_count(cell.value)
                    if words >= args.min_words:
                        items.append({"id": ref, "text": cell.value, "words": words,
                                      "header": cell.row == 1})
                if cell.comment is not None and cell.comment.text.strip():
                    items.append({"id": ref + "#comment", "text": cell.comment.text,
                                  "words": word_count(cell.comment.text), "header": False})
    risky = risky_parts(args.file)
    if risky:
        sys.stderr.write("NOTE: this workbook has %s. Saving with this script would drop them.\n"
                         % ", ".join(risky))
    emit(args, items, "text cells")


def split_ref(ref):
    sheet, _, coord = ref.rpartition("!")
    return sheet, coord


def xlsx_apply(args, out_path):
    from openpyxl import load_workbook
    from openpyxl.comments import Comment
    risky = risky_parts(args.file)
    if risky and not args.force:
        sys.exit("Stopped: this workbook has %s, which would be lost on save. "
                 "Tell the user, then rerun with --force, or use the fallback."
                 % ", ".join(risky))
    changes = load_changes(args.changes)
    wb = load_workbook(args.file, keep_vba=False)
    changed, refused, warnings = 0, [], []
    for ref, new in changes.items():
        is_comment = ref.endswith("#comment")
        sheet, coord = split_ref(ref[:-len("#comment")] if is_comment else ref)
        if sheet not in wb.sheetnames:
            refused.append(ref + " (no such sheet)")
            continue
        cell = wb[sheet][coord]
        if is_comment:
            if cell.comment is None:
                refused.append(ref + " (no comment there)")
                continue
            old = cell.comment.text
            if new != old:
                author = cell.comment.author
                cell.comment = Comment(new, author, cell.comment.height, cell.comment.width)
                changed += 1
        else:
            if cell.data_type != "s" or not is_editable_text(cell.value):
                refused.append(ref + " (not a text cell)")
                continue
            old = cell.value
            if new != old:
                cell.value = new
                changed += 1
        if numbers_in(old) != numbers_in(new):
            warnings.append("%s: numbers differ (%s -> %s)" % (ref, numbers_in(old), numbers_in(new)))
    wb.save(out_path)
    report(out_path, changed, refused, warnings)


# ---------------------------------------------------------------- csv

def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as fh:
        raw = fh.read()
    try:
        dialect = csv.Sniffer().sniff(raw[:4096], delimiters=",;\t|")
    except csv.Error:
        dialect = csv.excel
    rows = list(csv.reader(io.StringIO(raw), dialect))
    dialect.newline = "\r\n" if "\r\n" in raw else "\n"
    return rows, dialect


def col_letter(index):
    letters = ""
    index += 1
    while index:
        index, rem = divmod(index - 1, 26)
        letters = chr(65 + rem) + letters
    return letters


def looks_like_date(text):
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y", "%d %b %Y", "%d %B %Y"):
        try:
            datetime.datetime.strptime(text.strip(), fmt)
            return True
        except ValueError:
            pass
    return False


def csv_cells(rows):
    for r, row in enumerate(rows, start=1):
        for c, value in enumerate(row):
            if is_editable_text(value) and not looks_like_date(value):
                yield "csv!%s%d" % (col_letter(c), r), r - 1, c, value


def csv_extract(args):
    rows, _ = read_csv(args.file)
    items = []
    for ref, r, _, value in csv_cells(rows):
        words = word_count(value)
        if words >= args.min_words:
            items.append({"id": ref, "text": value, "words": words, "header": r == 0})
    emit(args, items, "text cells")


def csv_apply(args, out_path):
    rows, dialect = read_csv(args.file)
    lookup = {ref: (r, c) for ref, r, c, _ in csv_cells(rows)}
    changes = load_changes(args.changes)
    changed, refused, warnings = 0, [], []
    for ref, new in changes.items():
        if ref not in lookup:
            refused.append(ref + " (not a text cell)")
            continue
        r, c = lookup[ref]
        old = rows[r][c]
        if new != old:
            rows[r][c] = new
            changed += 1
        if numbers_in(old) != numbers_in(new):
            warnings.append("%s: numbers differ (%s -> %s)" % (ref, numbers_in(old), numbers_in(new)))
    with open(out_path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, delimiter=dialect.delimiter, quotechar=dialect.quotechar or '"',
                            lineterminator=getattr(dialect, "newline", "\r\n"))
        writer.writerows(rows)
    report(out_path, changed, refused, warnings)


# ---------------------------------------------------------------- shared

def report(out_path, changed, refused, warnings):
    print("Saved %s (%d cells changed)" % (out_path, changed))
    for w in warnings:
        print("CHECK: " + w)
    for r in refused:
        print("Skipped: " + r)


def is_csv(path):
    return path.lower().endswith((".csv", ".tsv", ".txt"))


def cmd_extract(args):
    (csv_extract if is_csv(args.file) else xlsx_extract)(args)


def cmd_apply(args):
    out_path = args.output or humanized_path(args.file)
    if os.path.abspath(out_path) == os.path.abspath(args.file):
        sys.exit("Refusing to overwrite the original file. Pick another output name.")
    if is_csv(args.file):
        csv_apply(args, out_path)
    else:
        xlsx_apply(args, out_path)


def main():
    parser = argparse.ArgumentParser(description="Rewrite text cells only. Numbers and formulas are left alone.")
    sub = parser.add_subparsers(dest="command", required=True)

    ex = sub.add_parser("extract", help="list text cells and comments as JSON")
    ex.add_argument("file")
    ex.add_argument("-o", "--output", help="write JSON here instead of printing it")
    ex.add_argument("--min-words", type=int, default=1,
                    help="only list cells with at least this many words (default 1)")
    ex.set_defaults(func=cmd_extract)

    ap = sub.add_parser("apply", help="write new text into a copy of the file")
    ap.add_argument("file")
    ap.add_argument("changes", help="JSON file mapping cell id to new text")
    ap.add_argument("-o", "--output", help="output path (default: <name>-humanized.<ext>)")
    ap.add_argument("--force", action="store_true",
                    help="save even if charts or images would be dropped")
    ap.set_defaults(func=cmd_apply)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
