#!/usr/bin/env python3
"""Fill one message per row of a spreadsheet, for people the user already knows.

The user writes one message with placeholders like {Name} or {City}, and
gives a .xlsx or .csv with matching column headings. This script writes one
filled message per row into a new file. It never sends anything.

  1. columns: see the column headings and how many rows there are.

       python mail_merge.py columns contacts.xlsx

  2. merge: fill the template for every row.

       python mail_merge.py merge contacts.xlsx template.txt
       python mail_merge.py merge contacts.csv template.txt --out diwali-messages.csv

     The output format follows the --out extension:
       .txt   one message per row, separated by a line of dashes (default)
       .csv   the original columns plus a Message column
       .docx  one block per row, with the first column as a heading

     The default output is <sheet-name>-messages.txt next to the sheet.
     The script refuses to overwrite the sheet or the template.

Placeholders are column headings in curly braces, matched without caring
about upper or lower case: {Name}, {name}, and {NAME} all use the Name
column. If a row has no value for a placeholder, that row is still written
with the placeholder left as it was, and the row is listed in the report,
so nothing gets invented to fill the gap.

Only uses openpyxl, python-docx (for .docx output), and the standard library.
"""

import argparse
import csv
import os
import re
import sys

PLACEHOLDER = re.compile(r"\{([^{}]+)\}")


def read_rows(path):
    """Return (headings, rows) where rows is a list of dicts keyed by heading."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        with open(path, newline="", encoding="utf-8-sig") as fh:
            reader = csv.reader(fh)
            table = [row for row in reader]
    elif ext in (".xlsx", ".xlsm"):
        try:
            import openpyxl
        except ImportError:
            sys.exit("openpyxl is not installed. Use the plain fallback in files/personalised-messages.md.")
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        ws = wb.worksheets[0]
        table = [["" if v is None else str(v) for v in row] for row in ws.iter_rows(values_only=True)]
    else:
        sys.exit("Use a .xlsx or .csv file. For Google Sheets, download as .xlsx or .csv first.")
    table = [row for row in table if any(str(c).strip() for c in row)]
    if not table:
        sys.exit("The sheet is empty.")
    headings = [str(h).strip() for h in table[0]]
    rows = []
    for raw in table[1:]:
        raw = list(raw) + [""] * (len(headings) - len(raw))
        rows.append({h: str(v).strip() for h, v in zip(headings, raw) if h})
    return [h for h in headings if h], rows


def fill(template, row):
    """Return (message, missing_placeholders) for one row."""
    lookup = {k.lower(): v for k, v in row.items()}
    missing = []

    def sub(match):
        key = match.group(1).strip()
        value = lookup.get(key.lower())
        if value:
            return value
        missing.append(key)
        return match.group(0)

    return PLACEHOLDER.sub(sub, template), missing


def refuse_overwrite(out, *inputs):
    for path in inputs:
        if os.path.abspath(out) == os.path.abspath(path):
            sys.exit("Refusing to overwrite %s. Pick another output name." % os.path.basename(path))


def cmd_columns(args):
    headings, rows = read_rows(args.file)
    print("Columns: " + ", ".join(headings))
    print("Rows: %d" % len(rows))


def cmd_merge(args):
    headings, rows = read_rows(args.file)
    with open(args.template, encoding="utf-8") as fh:
        template = fh.read().strip("\n")
    used = {m.strip().lower() for m in PLACEHOLDER.findall(template)}
    unknown = sorted(u for u in used if u not in {h.lower() for h in headings})
    if unknown:
        sys.exit("These placeholders have no matching column: %s. Columns are: %s"
                 % (", ".join("{%s}" % u for u in unknown), ", ".join(headings)))

    out = args.out or os.path.splitext(args.file)[0] + "-messages.txt"
    refuse_overwrite(out, args.file, args.template)
    ext = os.path.splitext(out)[1].lower()

    messages, gaps = [], []
    for n, row in enumerate(rows, start=2):  # row 1 is the headings
        text, missing = fill(template, row)
        messages.append(text)
        if missing:
            gaps.append("row %d (%s): no value for %s" % (
                n, row.get(headings[0], "") or "blank", ", ".join("{%s}" % m for m in missing)))

    if ext == ".csv":
        with open(out, "w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow(headings + ["Message"])
            for row, text in zip(rows, messages):
                writer.writerow([row.get(h, "") for h in headings] + [text])
    elif ext == ".docx":
        try:
            from docx import Document
        except ImportError:
            sys.exit("python-docx is not installed. Save as .txt or .csv instead.")
        doc = Document()
        for row, text in zip(rows, messages):
            doc.add_heading(row.get(headings[0], "") or "(no name)", level=2)
            for para in text.split("\n"):
                doc.add_paragraph(para)
        doc.save(out)
    else:
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(("\n\n" + "-" * 40 + "\n\n").join(messages) + "\n")

    print("Saved %s (%d messages). Nothing was sent." % (out, len(messages)))
    if gaps:
        print("CHECK: %d row(s) have missing values, left as placeholders:" % len(gaps))
        for g in gaps:
            print("  " + g)


def main():
    parser = argparse.ArgumentParser(description="One filled message per spreadsheet row. Never sends anything.")
    sub = parser.add_subparsers(dest="command", required=True)

    c = sub.add_parser("columns", help="list column headings and row count")
    c.add_argument("file")
    c.set_defaults(func=cmd_columns)

    m = sub.add_parser("merge", help="fill the template for every row")
    m.add_argument("file", help=".xlsx or .csv with column headings in the first row")
    m.add_argument("template", help="text file with {Column} placeholders")
    m.add_argument("--out", help="output path ending in .txt, .csv, or .docx")
    m.set_defaults(func=cmd_merge)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
