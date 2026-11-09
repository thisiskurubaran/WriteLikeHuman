#!/usr/bin/env python3
"""List and fill the fields of a fillable PDF form.

A fillable PDF (an "AcroForm") has named boxes you can type into. This
script lists those boxes and fills them with values you give it. It
never guesses a value: fields you leave out stay as they were.

  1. fields: list every field with its name, type, current value, and
     the choices for drop-downs, checkboxes, and radio buttons.

       python form_fill.py fields form.pdf
       python form_fill.py fields form.pdf -o fields.json

     JSON shape:
       {"file": "form.pdf", "fields": [
          {"name": "full_name", "type": "text", "value": "", "page": 1},
          {"name": "agree", "type": "checkbox", "value": "/Off",
           "options": ["/Yes", "/Off"], "page": 1}]}

  2. fill: write values into a copy of the form. Give a JSON object of
     field name to value. Checkboxes take one of their listed options,
     such as "/Yes" or "/Off".

       python form_fill.py fill form.pdf values.json

     Saved as form-filled.pdf. The original form is never overwritten.
     Field names that don't exist in the form are reported and skipped.

Only uses pypdf and the standard library.
"""

import argparse
import json
import os
import sys


def need_pypdf():
    try:
        import pypdf  # noqa: F401
    except ImportError:
        sys.exit("This script needs pypdf (pip install pypdf). "
                 "Fallback: list the form's questions as text and give the answers to type in.")


def filled_path(path):
    base, _ = os.path.splitext(path)
    return base + "-filled.pdf"


def field_type(ft):
    return {"/Tx": "text", "/Btn": "button", "/Ch": "choice", "/Sig": "signature"}.get(ft, str(ft))


def button_options(annot):
    ap = annot.get("/AP")
    if ap is None:
        return []
    ap = ap.get_object()
    normal = ap.get("/N")
    if normal is None:
        return []
    try:
        return sorted(str(k) for k in normal.get_object().keys())
    except AttributeError:
        return []


def collect_fields(reader):
    """Return field info keyed by name, with page numbers from widgets."""
    pages_by_name = {}
    options_by_name = {}
    for page_no, page in enumerate(reader.pages, start=1):
        for ref in page.get("/Annots") or []:
            annot = ref.get_object()
            if annot.get("/Subtype") != "/Widget":
                continue
            node = annot
            name = node.get("/T")
            if name is None and node.get("/Parent") is not None:
                node = node["/Parent"].get_object()
                name = node.get("/T")
            if name is None:
                continue
            name = str(name)
            pages_by_name.setdefault(name, page_no)
            opts = button_options(annot)
            if opts:
                merged = set(options_by_name.get(name, [])) | set(opts)
                options_by_name[name] = sorted(merged)

    out = []
    for name, field in (reader.get_fields() or {}).items():
        ftype = field_type(field.get("/FT"))
        flags = int(field.get("/Ff", 0) or 0)
        if ftype == "button":
            if flags & (1 << 16):
                ftype = "pushbutton"
            elif flags & (1 << 15):
                ftype = "radio"
            else:
                ftype = "checkbox"
        value = field.get("/V")
        info = {
            "name": name,
            "type": ftype,
            "value": "" if value is None else str(value),
            "page": pages_by_name.get(name),
        }
        if ftype in ("checkbox", "radio"):
            info["options"] = options_by_name.get(name, [])
        elif ftype == "choice":
            raw = field.get("/Opt") or []
            opts = []
            for o in raw:
                o = o.get_object() if hasattr(o, "get_object") else o
                opts.append(str(o[-1]) if isinstance(o, list) else str(o))
            info["options"] = opts
        if field.get("/TU"):
            info["label"] = str(field.get("/TU"))
        out.append(info)
    return out


def cmd_fields(args):
    need_pypdf()
    from pypdf import PdfReader
    reader = PdfReader(args.file)
    fields = collect_fields(reader)
    if not fields:
        print("No fillable fields found. This PDF is probably a flat form: "
              "list its questions as text instead and give the answers to type in.",
              file=sys.stderr)
    data = {"file": os.path.basename(args.file), "fields": fields}
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        print("Wrote %d %s to %s" % (len(fields), "field" if len(fields) == 1 else "fields", args.output))
    else:
        print(text)


def cmd_fill(args):
    need_pypdf()
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import BooleanObject, NameObject

    out_path = args.output or filled_path(args.file)
    if os.path.abspath(out_path) == os.path.abspath(args.file):
        sys.exit("Refusing to overwrite the original form. Choose a different output name.")

    with open(args.values, encoding="utf-8") as fh:
        values = json.load(fh)
    if not isinstance(values, dict):
        sys.exit("values JSON must be an object of field name to value.")

    reader = PdfReader(args.file)
    known = {f["name"]: f for f in collect_fields(reader)}
    unknown = [k for k in values if k not in known]
    for k in unknown:
        print("SKIP: no field called %r in this form" % k)
    for k, v in values.items():
        f = known.get(k)
        if f and f["type"] in ("checkbox", "radio") and f.get("options") and str(v) not in f["options"]:
            sys.exit("Field %r takes one of %s, not %r." % (k, ", ".join(f["options"]), v))
        if f and f["type"] == "signature":
            sys.exit("Field %r is a signature box. Leave it for the user to sign." % k)

    to_fill = {k: ("" if v is None else str(v)) for k, v in values.items() if k in known}

    writer = PdfWriter()
    writer.append(reader)
    for page in writer.pages:
        names_here = set()
        for ref in page.get("/Annots") or []:
            annot = ref.get_object()
            name = annot.get("/T")
            if name is None and annot.get("/Parent") is not None:
                name = annot["/Parent"].get_object().get("/T")
            if name is not None:
                names_here.add(str(name))
        page_values = {k: v for k, v in to_fill.items() if k in names_here}
        if page_values:
            writer.update_page_form_field_values(page, page_values, auto_regenerate=False)

    if "/AcroForm" in writer._root_object:
        writer._root_object["/AcroForm"][NameObject("/NeedAppearances")] = BooleanObject(True)

    with open(out_path, "wb") as fh:
        writer.write(fh)

    blank = [n for n, f in known.items() if f["type"] in ("text", "choice") and n not in to_fill and not f["value"]]
    print("Saved %s (%d fields filled)" % (out_path, len(to_fill)))
    if blank:
        print("STILL BLANK: " + ", ".join(blank))


def main():
    parser = argparse.ArgumentParser(description="List and fill the fields of a fillable PDF form.")
    sub = parser.add_subparsers(dest="command", required=True)

    f = sub.add_parser("fields", help="list the form's fields as JSON")
    f.add_argument("file")
    f.add_argument("-o", "--output", help="write here instead of printing")
    f.set_defaults(func=cmd_fields)

    fl = sub.add_parser("fill", help="write values into a copy of the form")
    fl.add_argument("file", help="the original PDF form")
    fl.add_argument("values", help="JSON object of field name to value")
    fl.add_argument("-o", "--output", help="output path (default: <name>-filled.pdf)")
    fl.set_defaults(func=cmd_fill)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
