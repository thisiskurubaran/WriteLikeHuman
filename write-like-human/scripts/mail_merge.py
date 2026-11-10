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

Dates and numbers in a .xlsx are written the way the sheet shows them
(20/11/2026, 1,200, 15%), without currency signs. Excel's default short
date depends on the computer's settings, so those dates are written as
2026-11-20. Row numbers in the report are the rows in the sheet. If the
message uses a heading that two columns share, the script stops.

To put real braces in a message, double them: {{SAVE10}} comes out as
{SAVE10}, and is never treated as a placeholder.

Only uses openpyxl, python-docx (for .docx output), and the standard library.
"""

import argparse
import csv
import datetime
import os
import re
import sys

# "{{" and "}}" are literal braces; "{Name}" is a placeholder.
PLACEHOLDER = re.compile(r"\{\{|\}\}|\{([^{}]+)\}")


def placeholders(template):
    return [m.group(1) for m in PLACEHOLDER.finditer(template) if m.group(1) is not None]


DATE_TOKEN = re.compile(
    r'\[[^\]]*\]|"[^"]*"|\\.|yyyy|yy|mmmmm|mmmm|mmm|mm|m|dddd|ddd|dd|d|hh|h|ss|s'
    r'|am/pm|a/p|.', re.IGNORECASE)
NUMBER_PART = re.compile(r"[#0,]*0(?:\.0+)?%?")


def date_text(value, fmt):
    """A date or time as the sheet shows it, for plain date formats.

    Excel's built-in short date (shown here as "mm-dd-yy") follows the
    computer's settings, so it and anything unusual come out as 2026-03-14,
    which can't be misread. A time of midnight on a date is left off.
    """
    calendar = isinstance(value, datetime.date)
    clock = isinstance(value, (datetime.time, datetime.datetime))
    has_time = isinstance(value, datetime.time) or (
        isinstance(value, datetime.datetime) and value.time() != datetime.time(0))
    tokens = DATE_TOKEN.findall(fmt or "")
    plain = bool(fmt) and fmt.lower() not in ("general", "mm-dd-yy") and not any(
        t in ("0", "#", "@", ";", "?") for t in tokens)
    out = []
    ampm = any(t.lower() in ("am/pm", "a/p") for t in tokens)
    for i, t in enumerate(tokens if plain else []):
        low = t.lower()
        minute = low in ("m", "mm") and (
            any(x.lower() in ("h", "hh") for x in tokens[max(0, i - 2):i])
            or any(x.lower() in ("s", "ss") for x in tokens[i + 1:i + 3]))
        if low in ("yyyy", "yy", "mmmm", "mmm", "dddd", "ddd", "dd", "d") or (
                low in ("mm", "m") and not minute):
            if not calendar:
                plain = False
                break
            out.append({"yyyy": "%04d" % value.year, "yy": "%02d" % (value.year % 100),
                        "mmmm": value.strftime("%B"), "mmm": value.strftime("%b"),
                        "mm": "%02d" % value.month, "m": "%d" % value.month,
                        "dddd": value.strftime("%A"), "ddd": value.strftime("%a"),
                        "dd": "%02d" % value.day, "d": "%d" % value.day}[low])
        elif minute or low in ("hh", "h", "ss", "s", "am/pm", "a/p"):
            if not clock:
                plain = False
                break
            hour = (value.hour % 12 or 12) if ampm else value.hour
            out.append({"mm": "%02d" % value.minute, "m": "%d" % value.minute,
                        "hh": "%02d" % hour, "h": "%d" % hour,
                        "ss": "%02d" % value.second, "s": "%d" % value.second,
                        "am/pm": "AM" if value.hour < 12 else "PM",
                        "a/p": "A" if value.hour < 12 else "P"}[low])
        elif t.startswith("["):
            continue
        elif t.startswith('"'):
            out.append(t[1:-1])
        elif t.startswith("\\"):
            out.append(t[1:])
        elif len(t) == 1 and not t.isalpha():
            out.append(t)
        else:
            plain = False
            break
    if plain:
        return "".join(out).strip()
    if isinstance(value, datetime.datetime):
        return value.strftime("%Y-%m-%d %H:%M" if has_time else "%Y-%m-%d")
    if calendar:
        return value.strftime("%Y-%m-%d")
    return value.strftime("%H:%M" if not value.second else "%H:%M:%S")


def number_text(value, fmt):
    """A number roughly as the sheet shows it: whole numbers without ".0",
    percentages as percentages, and the decimals and thousands commas the
    cell's format asks for. Currency signs and other symbols are left off."""
    first = re.sub(r'\[[^\]]*\]|"[^"]*"|\\.', "", (fmt or "General").split(";")[0])
    m = NUMBER_PART.search(first) if first.lower() != "general" else None
    if not m:
        if float(value).is_integer() and abs(value) < 1e15:
            return str(int(value))
        return "%.15g" % value
    part = m.group(0)
    if part.endswith("%"):
        value = value * 100
    decimals = len(part.split(".")[1].rstrip("%")) if "." in part else 0
    text = (("{:,.%df}" if "," in part else "{:.%df}") % decimals).format(value)
    digits = part.split(".")[0].rstrip("%").count("0")
    if "," not in part and digits > 1:  # "00000" keeps leading zeros, as in a PIN or ZIP code
        sign = "-" if text.startswith("-") else ""
        whole, _, rest = text.lstrip("-").partition(".")
        text = sign + whole.zfill(digits) + ("." + rest if rest else "")
    return text + ("%" if part.endswith("%") else "")


def cell_text(value, fmt):
    if value is None:
        return ""
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (datetime.date, datetime.time)):
        return date_text(value, fmt)
    if isinstance(value, (int, float)):
        return number_text(value, fmt)
    return str(value)


def read_rows(path):
    """Return (headings, rows). headings has one entry per column, blank for
    a column with no heading. Each row is (row number in the sheet, values)."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        try:
            with open(path, newline="", encoding="utf-8-sig") as fh:
                table = list(enumerate(csv.reader(fh), start=1))
        except UnicodeDecodeError:
            sys.exit("This CSV file is not saved as UTF-8. In Excel, use Save As and pick "
                     "'CSV UTF-8', or send the .xlsx file instead.")
    elif ext in (".xlsx", ".xlsm"):
        try:
            import openpyxl
        except ImportError:
            sys.exit("openpyxl is not installed. Use the plain fallback in files/personalised-messages.md.")
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        ws = wb.worksheets[0]
        table = [(n, [cell_text(c.value, getattr(c, "number_format", None)) for c in row])
                 for n, row in enumerate(ws.iter_rows(), start=ws.min_row or 1)]
    else:
        sys.exit("Use a .xlsx or .csv file. For Google Sheets, download as .xlsx or .csv first.")
    table = [(n, row) for n, row in table if any(str(c).strip() for c in row)]
    if not table:
        sys.exit("The sheet is empty.")
    headings = [str(h).strip() for h in table[0][1]]
    rows = []
    for n, raw in table[1:]:
        raw = [str(v).strip() for v in raw] + [""] * (len(headings) - len(raw))
        rows.append((n, raw[:len(headings)]))
    return headings, rows


def lookup_for(headings, raw):
    """Map lower-case heading to value. The first column with a heading wins."""
    lookup = {}
    for h, v in zip(headings, raw):
        if h:
            lookup.setdefault(h.lower(), v)
    return lookup


def fill(template, row):
    """Return (message, missing_placeholders) for one row.

    row maps lower-case heading to value (see lookup_for)."""
    lookup = row
    missing = []

    def sub(match):
        if match.group(1) is None:
            return match.group(0)[0]      # "{{" becomes "{", "}}" becomes "}"
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
    print("Columns: " + ", ".join(h for h in headings if h))
    print("Rows: %d" % len(rows))


def cmd_merge(args):
    headings, rows = read_rows(args.file)
    named = [h for h in headings if h]
    with open(args.template, encoding="utf-8-sig") as fh:
        template = fh.read().strip("\n")
    used = {m.strip().lower() for m in placeholders(template)}
    unknown = sorted(u for u in used if u not in {h.lower() for h in named})
    if unknown:
        sys.exit("These placeholders have no matching column: %s. Columns are: %s"
                 % (", ".join("{%s}" % u for u in unknown), ", ".join(named)))
    twice = sorted(u for u in used if [h.lower() for h in named].count(u) > 1)
    if twice:
        sys.exit("More than one column is called %s, so the script can't tell which one to use. "
                 "Rename one of them in the sheet and run it again."
                 % ", ".join("{%s}" % u for u in twice))

    out = args.out or os.path.splitext(args.file)[0] + "-messages.txt"
    refuse_overwrite(out, args.file, args.template)
    ext = os.path.splitext(out)[1].lower()

    messages, gaps = [], []
    for n, raw in rows:
        text, missing = fill(template, lookup_for(headings, raw))
        messages.append(text)
        if missing:
            gaps.append("row %d (%s): no value for %s" % (
                n, raw[0] or "blank", ", ".join("{%s}" % m for m in missing)))

    if ext == ".csv":
        with open(out, "w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow(headings + ["Message"])
            for (_, raw), text in zip(rows, messages):
                writer.writerow(raw + [text])
    elif ext == ".docx":
        try:
            from docx import Document
        except ImportError:
            sys.exit("python-docx is not installed. Save as .txt or .csv instead.")
        doc = Document()
        for (_, raw), text in zip(rows, messages):
            doc.add_heading(raw[0] or "(no name)", level=2)
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
