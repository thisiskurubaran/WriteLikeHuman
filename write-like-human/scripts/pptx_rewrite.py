#!/usr/bin/env python3
"""Rewrite slide text and speaker notes in a PowerPoint (.pptx) file.

Two steps:

  1. extract: list every paragraph of text on every slide, including text
     inside tables and grouped shapes, plus the speaker notes.

       python pptx_rewrite.py extract deck.pptx -o segments.json

     Each segment has an id like "s3-2-1" (slide 3, shape 2, paragraph 1)
     or "s3-notes-1" for notes. Slide text segments also show "chars", the
     current length, so you can keep new text about the same size and stop
     it spilling out of its box.

  2. apply: give back new text for the ids you changed.

       python pptx_rewrite.py apply deck.pptx changes.json

     changes.json can be {"s3-2-1": "new text", ...} or the edited output
     of extract. The result is saved as deck-humanized.pptx. The original
     is never overwritten.

Formatting is kept the same way as in docx_rewrite.py: unchanged words stay
in their original run (font, size, colour, bold), new words take the
formatting of the word they replace. Layout, pictures, charts, and
animations are not touched.

Only uses python-pptx and the standard library.
"""

import argparse
import difflib
import json
import os
import re
import sys

try:
    from pptx import Presentation
    from pptx.enum.shapes import MSO_SHAPE_TYPE
except ImportError:  # pragma: no cover
    sys.exit("python-pptx is not installed. Use the plain fallback in files/slides.md.")

A_NS = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
TOKEN_RE = re.compile(r"\s+|\w+|[^\w\s]", re.UNICODE)
NUMBER_RE = re.compile(r"\d+(?:[,.:/]\d+)*")
LONGER_WARNING = 1.15


def humanized_path(path):
    root, ext = os.path.splitext(path)
    return "%s-humanized%s" % (root, ext)


# ---------------------------------------------------------------- reading

def text_runs(p_el):
    return [r for r in p_el.findall(A_NS + "r") if r.find(A_NS + "t") is not None]


def run_text(r):
    return "".join(t.text or "" for t in r.findall(A_NS + "t"))


def para_text(p_el):
    return "".join(run_text(r) for r in text_runs(p_el))


def walk_shapes(shapes, prefix):
    """Yield (shape_id_path, shape) for every shape, opening groups."""
    for i, shape in enumerate(shapes, start=1):
        path = "%s%d" % (prefix, i)
        if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
            for item in walk_shapes(shape.shapes, path + "."):
                yield item
        else:
            yield path, shape


def shape_paragraphs(shape):
    """Yield (suffix, paragraph element) for a shape's text and tables."""
    if shape.has_text_frame:
        for k, p in enumerate(shape.text_frame.paragraphs, start=1):
            yield "%d" % k, p._p
    if getattr(shape, "has_table", False) and shape.has_table:
        for ri, row in enumerate(shape.table.rows, start=1):
            for ci, cell in enumerate(row.cells, start=1):
                for k, p in enumerate(cell.text_frame.paragraphs, start=1):
                    yield "r%dc%d-%d" % (ri, ci, k), p._p


def collect_paragraphs(prs):
    """Yield (id, where, paragraph element) in a stable order."""
    for s, slide in enumerate(prs.slides, start=1):
        for path, shape in walk_shapes(slide.shapes, ""):
            for suffix, p in shape_paragraphs(shape):
                yield "s%d-%s-%s" % (s, path, suffix), "slide", p
        if slide.has_notes_slide:
            frame = slide.notes_slide.notes_text_frame
            if frame is not None:
                for k, p in enumerate(frame.paragraphs, start=1):
                    yield "s%d-notes-%d" % (s, k), "notes", p._p


# ---------------------------------------------------------------- editing

def apply_plain(p_el, new_text):
    runs = text_runs(p_el)
    if not runs:
        return False
    old_tokens, owners = [], []
    for i, r in enumerate(runs):
        for tok in TOKEN_RE.findall(run_text(r)):
            old_tokens.append(tok)
            owners.append(i)
    new_tokens = TOKEN_RE.findall(new_text)
    buckets = [""] * len(runs)
    last_owner = 0
    matcher = difflib.SequenceMatcher(None, old_tokens, new_tokens, autojunk=False)
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == "equal":
            for k in range(i1, i2):
                buckets[owners[k]] += old_tokens[k]
                last_owner = owners[k]
        elif op == "delete":
            last_owner = owners[i2 - 1]
        else:
            owner = owners[i1] if op == "replace" else last_owner
            buckets[owner] += "".join(new_tokens[j1:j2])
            last_owner = owner
    for r, text in zip(runs, buckets):
        ts = r.findall(A_NS + "t")
        ts[0].text = text
        for t in ts[1:]:
            r.remove(t)
    return True


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
    prs = Presentation(args.file)
    segments = []
    for pid, where, p in collect_paragraphs(prs):
        text = para_text(p)
        if text.strip():
            seg = {"id": pid, "where": where, "text": text}
            if where == "slide":
                seg["chars"] = len(text)
            segments.append(seg)
    out = {"file": os.path.basename(args.file), "slides": len(prs.slides), "segments": segments}
    payload = json.dumps(out, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(payload)
        print("Wrote %d %s from %d %s to %s" % (len(segments), "paragraph" if len(segments) == 1 else "paragraphs", len(prs.slides), "slide" if len(prs.slides) == 1 else "slides", args.output))
    else:
        print(payload)


def cmd_apply(args):
    out_path = args.output or humanized_path(args.file)
    if os.path.abspath(out_path) == os.path.abspath(args.file):
        sys.exit("Refusing to overwrite the original file. Pick another output name.")
    changes = load_changes(args.changes)
    prs = Presentation(args.file)
    changed, skipped, warnings, seen = 0, 0, [], set()
    for pid, where, p in collect_paragraphs(prs):
        if pid not in changes:
            continue
        seen.add(pid)
        old, new = para_text(p), changes[pid]
        if new == old:
            skipped += 1
            continue
        if numbers_in(old) != numbers_in(new):
            warnings.append("%s: numbers differ (%s -> %s)" % (pid, numbers_in(old), numbers_in(new)))
        if where == "slide" and len(new) > len(old) * LONGER_WARNING and len(new) - len(old) > 5:
            warnings.append("%s: new text is %d chars, was %d. It may not fit its box."
                            % (pid, len(new), len(old)))
        if apply_plain(p, new):
            changed += 1
    prs.save(out_path)
    print("Saved %s (%d %s changed, %d unchanged)" % (out_path, changed, "paragraph" if changed == 1 else "paragraphs", skipped))
    for w in warnings:
        print("CHECK: " + w)
    missing = sorted(set(changes) - seen)
    if missing:
        print("Unknown ids ignored: " + ", ".join(missing))


def main():
    parser = argparse.ArgumentParser(description="Rewrite slide text and notes, keep the layout.")
    sub = parser.add_subparsers(dest="command", required=True)

    ex = sub.add_parser("extract", help="list slide and notes paragraphs as JSON")
    ex.add_argument("file")
    ex.add_argument("-o", "--output", help="write JSON here instead of printing it")
    ex.set_defaults(func=cmd_extract)

    ap = sub.add_parser("apply", help="write new text into a copy of the deck")
    ap.add_argument("file")
    ap.add_argument("changes", help="JSON file mapping paragraph id to new text")
    ap.add_argument("-o", "--output", help="output path (default: <name>-humanized.pptx)")
    ap.set_defaults(func=cmd_apply)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
