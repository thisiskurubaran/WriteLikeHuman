#!/usr/bin/env python3
"""Rewrite the text of a Word (.docx) file without touching its layout.

Two steps:

  1. extract: list every paragraph that has text, each with a stable id.

       python docx_rewrite.py extract report.docx -o segments.json

  2. apply: give back the new text for the ids you changed. Only those
     paragraphs are edited. Fonts, bold, italics, styles, tables, lists,
     images, links, headers, and footers stay as they were.

       python docx_rewrite.py apply report.docx changes.json
       python docx_rewrite.py apply report.docx changes.json --track-changes

     changes.json can be a plain mapping {"p3": "new text", ...} or the
     same shape extract produced, with edited "text" values. The result is
     saved as report-humanized.docx next to the original. The original is
     never overwritten.

How formatting is kept: the old and new text are compared word by word.
Words that did not change keep the exact run (and so the exact font, bold,
italic, colour) they were in. New words take the formatting of the word
they replaced, or of the word just before them.

With --track-changes the edits are written as Word revisions (shown as
tracked changes by author "WriteLikeHuman"), so the user can accept or
reject each one in Word.

Only uses python-docx and the standard library.
"""

import argparse
import copy
import datetime
import difflib
import json
import os
import re
import sys

try:
    from docx import Document
    from docx.oxml.ns import qn
except ImportError:  # pragma: no cover
    sys.exit("python-docx is not installed. Use the plain fallback in files/word.md.")

TOKEN_RE = re.compile(r"\s+|\w+|[^\w\s]", re.UNICODE)
NUMBER_RE = re.compile(r"\d+(?:[,.:/]\d+)*")
AUTHOR = "WriteLikeHuman"
XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"
FALLBACK_TAG = "{http://schemas.openxmlformats.org/markup-compatibility/2006}Fallback"


# ---------------------------------------------------------------- reading

def humanized_path(path, ext=None):
    root, old_ext = os.path.splitext(path)
    return "%s-humanized%s" % (root, ext or old_ext)


def text_runs(p_el):
    """All w:r elements in a paragraph that carry visible text, in order.

    Includes runs inside hyperlinks and earlier insertions. Skips deleted
    text, field codes, and runs that hold only images or breaks.
    """
    runs = []
    for r in p_el.iter(qn("w:r")):
        parent = r.getparent()
        if parent is not None and parent.tag == qn("w:del"):
            continue
        if r.find(qn("w:t")) is not None:
            runs.append(r)
    return runs


def run_text(r):
    return "".join(t.text or "" for t in r.findall(qn("w:t")))


def para_text(p_el):
    return "".join(run_text(r) for r in text_runs(p_el))


def in_fallback(el):
    parent = el.getparent()
    while parent is not None:
        if parent.tag == FALLBACK_TAG:
            return True
        parent = parent.getparent()
    return False


def in_table(el):
    parent = el.getparent()
    while parent is not None:
        if parent.tag == qn("w:tbl"):
            return True
        parent = parent.getparent()
    return False


def header_footer_parts(doc):
    """Header and footer parts in a stable order: (kind, part)."""
    found = []
    for rel_id, rel in doc.part.rels.items():
        if rel.reltype.endswith("/header"):
            found.append(("header", rel_id, rel.target_part))
        elif rel.reltype.endswith("/footer"):
            found.append(("footer", rel_id, rel.target_part))

    def rid_num(item):
        digits = re.sub(r"\D", "", item[1])
        return (item[0], int(digits) if digits else 0)

    found.sort(key=rid_num)
    return [(kind, part) for kind, _, part in found]


def collect_paragraphs(doc):
    """Yield (id, where, paragraph element) in a stable order."""
    n = 0
    for p in doc.element.body.iter(qn("w:p")):
        if in_fallback(p):
            continue
        n += 1
        yield "p%d" % n, ("table" if in_table(p) else "body"), p
    counters = {"header": 0, "footer": 0}
    for kind, part in header_footer_parts(doc):
        counters[kind] += 1
        prefix = "h" if kind == "header" else "f"
        m = 0
        for p in part.element.iter(qn("w:p")):
            if in_fallback(p):
                continue
            m += 1
            yield "%s%d-%d" % (prefix, counters[kind], m), kind, p


# ---------------------------------------------------------------- diffing

def run_tokens(runs):
    """Split each run's text into tokens, remembering which run each came from."""
    tokens, owners = [], []
    for i, r in enumerate(runs):
        for tok in TOKEN_RE.findall(run_text(r)):
            tokens.append(tok)
            owners.append(i)
    return tokens, owners


def plan_edit(runs, new_text):
    """Return a list of (kind, text, run_index) where kind is equal/insert/delete."""
    old_tokens, owners = run_tokens(runs)
    new_tokens = TOKEN_RE.findall(new_text)
    matcher = difflib.SequenceMatcher(None, old_tokens, new_tokens, autojunk=False)
    plan = []
    last_owner = 0
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == "equal":
            for k in range(i1, i2):
                plan.append(("equal", old_tokens[k], owners[k]))
                last_owner = owners[k]
            continue
        if op in ("replace", "delete"):
            for k in range(i1, i2):
                plan.append(("delete", old_tokens[k], owners[k]))
        if op in ("replace", "insert"):
            owner = owners[i1] if op == "replace" else last_owner
            for k in range(j1, j2):
                plan.append(("insert", new_tokens[k], owner))
            last_owner = owner
        elif op == "delete" and i2 > i1:
            last_owner = owners[i2 - 1]
    return plan


def set_run_text(r, text):
    ts = r.findall(qn("w:t"))
    first = ts[0]
    first.text = text
    first.set(XML_SPACE, "preserve")
    for t in ts[1:]:
        r.remove(t)


def apply_plain(p_el, new_text):
    runs = text_runs(p_el)
    if not runs:
        return False
    buckets = [""] * len(runs)
    for kind, tok, owner in plan_edit(runs, new_text):
        if kind != "delete":
            buckets[owner] += tok
    for r, text in zip(runs, buckets):
        set_run_text(r, text)
    return True


# ---------------------------------------------------------- tracked changes

class RevisionIds:
    def __init__(self, start=9000):
        self.next = start

    def take(self):
        self.next += 1
        return str(self.next)


def make_run(template, text, deleted=False):
    r = copy.deepcopy(template)
    for child in list(r):
        if child.tag != qn("w:rPr"):
            r.remove(child)
    t = r.makeelement(qn("w:delText") if deleted else qn("w:t"), {})
    t.text = text
    t.set(XML_SPACE, "preserve")
    r.append(t)
    return r


def wrap(tag, run, ids, when):
    el = run.makeelement(qn(tag), {
        qn("w:id"): ids.take(),
        qn("w:author"): AUTHOR,
        qn("w:date"): when,
    })
    el.append(run)
    return el


def apply_tracked(p_el, new_text, ids, when):
    runs = text_runs(p_el)
    if not runs:
        return False
    # Tracked changes are only rebuilt when every text run sits directly in
    # the paragraph. Runs inside links or earlier revisions get a plain edit.
    if any(r.getparent() is not p_el for r in runs):
        return apply_plain(p_el, new_text)

    plan = plan_edit(runs, new_text)
    # Group neighbouring tokens with the same kind and run into one piece.
    pieces = []
    for kind, tok, owner in plan:
        if pieces and pieces[-1][0] == kind and pieces[-1][2] == owner:
            pieces[-1][1] += tok
        else:
            pieces.append([kind, tok, owner])

    new_elements = []
    for kind, text, owner in pieces:
        template = runs[owner]
        if kind == "equal":
            new_elements.append(make_run(template, text))
        elif kind == "delete":
            new_elements.append(wrap("w:del", make_run(template, text, deleted=True), ids, when))
        else:
            new_elements.append(wrap("w:ins", make_run(template, text), ids, when))

    # Runs that also hold other things (tabs, breaks, images) are kept but
    # lose their text; plain text runs are replaced by the new elements.
    anchor = runs[0]
    index = list(p_el).index(anchor)
    for r in runs:
        others = [c for c in r if c.tag not in (qn("w:rPr"), qn("w:t"))]
        if others:
            for t in r.findall(qn("w:t")):
                r.remove(t)
        else:
            p_el.remove(r)
    for offset, el in enumerate(new_elements):
        p_el.insert(index + offset, el)
    return True


# ---------------------------------------------------------------- commands

def numbers_in(text):
    return sorted(NUMBER_RE.findall(text))


def load_changes(path):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if isinstance(data, dict) and "segments" in data:
        return {s["id"]: s["text"] for s in data["segments"]}
    if isinstance(data, list):
        return {s["id"]: s["text"] for s in data}
    return data


def cmd_extract(args):
    doc = Document(args.file)
    segments = []
    for pid, where, p in collect_paragraphs(doc):
        text = para_text(p)
        if text.strip():
            segments.append({"id": pid, "where": where, "text": text})
    out = {"file": os.path.basename(args.file), "segments": segments}
    payload = json.dumps(out, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(payload)
        print("Wrote %d paragraphs to %s" % (len(segments), args.output))
    else:
        print(payload)


def cmd_apply(args):
    out_path = args.output or humanized_path(args.file)
    if os.path.abspath(out_path) == os.path.abspath(args.file):
        sys.exit("Refusing to overwrite the original file. Pick another output name.")
    changes = load_changes(args.changes)
    doc = Document(args.file)
    existing = [int(v) for el in doc.element.body.iter()
                for v in [el.get(qn("w:id"))] if v and v.isdigit()]
    ids = RevisionIds(max(existing + [9000]))
    when = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    changed, skipped, warnings = 0, 0, []
    seen = set()
    for pid, _, p in collect_paragraphs(doc):
        if pid not in changes:
            continue
        seen.add(pid)
        old, new = para_text(p), changes[pid]
        if new == old:
            skipped += 1
            continue
        if numbers_in(old) != numbers_in(new):
            warnings.append("%s: numbers differ (%s -> %s)" % (pid, numbers_in(old), numbers_in(new)))
        done = apply_tracked(p, new, ids, when) if args.track_changes else apply_plain(p, new)
        if done:
            changed += 1
    missing = sorted(set(changes) - seen)
    doc.save(out_path)
    print("Saved %s (%d paragraphs changed, %d unchanged)" % (out_path, changed, skipped))
    for w in warnings:
        print("CHECK: " + w)
    if missing:
        print("Unknown ids ignored: " + ", ".join(missing))


def main():
    parser = argparse.ArgumentParser(description="Rewrite Word text, keep the layout.")
    sub = parser.add_subparsers(dest="command", required=True)

    ex = sub.add_parser("extract", help="list paragraphs with text as JSON")
    ex.add_argument("file")
    ex.add_argument("-o", "--output", help="write JSON here instead of printing it")
    ex.set_defaults(func=cmd_extract)

    ap = sub.add_parser("apply", help="write new text into a copy of the file")
    ap.add_argument("file")
    ap.add_argument("changes", help="JSON file mapping paragraph id to new text")
    ap.add_argument("-o", "--output", help="output path (default: <name>-humanized.docx)")
    ap.add_argument("--track-changes", action="store_true",
                    help="write edits as Word tracked changes")
    ap.set_defaults(func=cmd_apply)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
