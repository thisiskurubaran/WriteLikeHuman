#!/usr/bin/env python3
"""Rewrite subtitle text (.srt or simple .vtt) without touching the timings.

Two steps:

  1. extract: list every caption with its id, timing, and text.

       python srt_rewrite.py extract talk.srt -o cues.json

     JSON shape:
       {"file": "talk.srt", "format": "srt", "cues": [
          {"id": "1", "timing": "00:00:01,000 --> 00:00:03,500",
           "text": "Hello everyone,\\nthanks for coming.",
           "seconds": 2.5, "max_line_chars": 18}]}

     Line breaks inside a caption are kept as "\\n" in "text".

  2. apply: give back new text for the ids you changed.

       python srt_rewrite.py apply talk.srt changes.json

     changes.json can be {"1": "new text", ...} or the edited output of
     extract. Only caption text changes. Cue numbers and timings are
     copied from the original file, and if the edited JSON has a
     different "timing" for a cue, apply refuses to run. Saved as
     talk-humanized.srt. The original is never overwritten.

     apply prints a CHECK line for any caption longer than 42 characters
     on a line, with more than two lines, or that reads faster than about
     21 characters per second, so you can shorten it.

Only uses the standard library.
"""

import argparse
import json
import os
import re
import sys

TIMING_RE = re.compile(r"^\s*(\S+)\s*-->\s*(\S+)(.*)$")
MAX_LINE = 42
MAX_LINES = 2
MAX_CPS = 21.0


def humanized_path(path):
    root, ext = os.path.splitext(path)
    return "%s-humanized%s" % (root, ext)


def to_seconds(stamp):
    stamp = stamp.replace(",", ".")
    parts = stamp.split(":")
    try:
        nums = [float(p) for p in parts]
    except ValueError:
        return None
    total = 0.0
    for n in nums:
        total = total * 60 + n
    return total


def parse(text):
    """Return (format, header_lines, cues). Each cue is a dict with
    id, timing, lines."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    blocks = re.split(r"\n\s*\n", text.strip("\n"))
    fmt = "srt"
    header = []
    cues = []
    auto = 0
    for block in blocks:
        lines = block.split("\n")
        if not lines or not lines[0].strip():
            continue
        if lines[0].startswith("WEBVTT"):
            fmt = "vtt"
            header = lines
            continue
        if lines[0].startswith(("NOTE", "STYLE", "REGION")):
            header.append("")
            header.extend(lines)
            continue
        t_index = next((i for i, l in enumerate(lines) if "-->" in l), None)
        if t_index is None or t_index > 1:
            continue
        auto += 1
        cue_id = lines[0].strip() if t_index == 1 else None
        cues.append({
            "id": cue_id or str(auto),
            "has_id_line": t_index == 1,
            "timing": lines[t_index].strip(),
            "lines": lines[t_index + 1:],
        })
    return fmt, header, cues


def render(fmt, header, cues):
    out = []
    if fmt == "vtt":
        out.append("\n".join(header))
    for c in cues:
        block = []
        if fmt == "srt" or c["has_id_line"]:
            block.append(c["id"])
        block.append(c["timing"])
        block.extend(c["lines"])
        out.append("\n".join(block))
    return "\n\n".join(out) + "\n"


def cue_seconds(timing):
    m = TIMING_RE.match(timing)
    if not m:
        return None
    a, b = to_seconds(m.group(1)), to_seconds(m.group(2))
    if a is None or b is None:
        return None
    return round(b - a, 3)


def checks(cue_id, lines, seconds):
    notes = []
    longest = max((len(l) for l in lines), default=0)
    if longest > MAX_LINE:
        notes.append("%s: a line is %d characters (aim for %d or fewer)" % (cue_id, longest, MAX_LINE))
    if len(lines) > MAX_LINES:
        notes.append("%s: %d lines (aim for %d or fewer)" % (cue_id, len(lines), MAX_LINES))
    chars = sum(len(l) for l in lines)
    if seconds and chars / seconds > MAX_CPS:
        notes.append("%s: %.0f characters per second, may be too fast to read" % (cue_id, chars / seconds))
    return notes


def load(path):
    with open(path, encoding="utf-8-sig") as fh:
        return parse(fh.read())


def cmd_extract(args):
    fmt, _, cues = load(args.file)
    items = []
    for c in cues:
        items.append({
            "id": c["id"],
            "timing": c["timing"],
            "text": "\n".join(c["lines"]),
            "seconds": cue_seconds(c["timing"]),
            "max_line_chars": max((len(l) for l in c["lines"]), default=0),
        })
    payload = json.dumps({"file": os.path.basename(args.file), "format": fmt, "cues": items},
                         ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(payload)
        print("Wrote %d captions to %s" % (len(items), args.output))
    else:
        print(payload)


def load_changes(path):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    timings = {}
    if isinstance(data, dict) and "cues" in data:
        data = data["cues"]
    if isinstance(data, list):
        changes = {}
        for item in data:
            changes[str(item["id"])] = item["text"]
            if "timing" in item:
                timings[str(item["id"])] = item["timing"].strip()
        return changes, timings
    return {str(k): v for k, v in data.items()}, timings


def cmd_apply(args):
    out_path = args.output or humanized_path(args.file)
    if os.path.abspath(out_path) == os.path.abspath(args.file):
        sys.exit("Refusing to overwrite the original file. Pick another output name.")
    fmt, header, cues = load(args.file)
    changes, timings = load_changes(args.changes)
    by_id = {c["id"]: c for c in cues}
    moved = [i for i, t in timings.items() if i in by_id and by_id[i]["timing"] != t]
    if moved:
        sys.exit("Timings were changed for captions %s. Only the text may change. "
                 "Nothing was saved." % ", ".join(moved))
    changed, notes = 0, []
    for c in cues:
        if c["id"] not in changes:
            continue
        new_lines = [l.rstrip() for l in changes[c["id"]].replace("\r", "").split("\n")]
        new_lines = [l for l in new_lines if l.strip()]
        if not new_lines:
            notes.append("%s: new text was empty, kept the original" % c["id"])
            continue
        if new_lines != c["lines"]:
            c["lines"] = new_lines
            changed += 1
        notes.extend(checks(c["id"], new_lines, cue_seconds(c["timing"])))
    missing = sorted(set(changes) - set(by_id))
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(render(fmt, header, cues))
    print("Saved %s (%d captions changed, timings untouched)" % (out_path, changed))
    for n in notes:
        print("CHECK: " + n)
    if missing:
        print("Unknown ids ignored: " + ", ".join(missing))


def main():
    parser = argparse.ArgumentParser(description="Rewrite subtitle text, keep the timings.")
    sub = parser.add_subparsers(dest="command", required=True)
    ex = sub.add_parser("extract", help="list captions as JSON")
    ex.add_argument("file")
    ex.add_argument("-o", "--output", help="write JSON here instead of printing it")
    ex.set_defaults(func=cmd_extract)
    ap = sub.add_parser("apply", help="write new caption text into a copy of the file")
    ap.add_argument("file")
    ap.add_argument("changes", help="JSON file mapping caption id to new text")
    ap.add_argument("-o", "--output", help="output path (default: <name>-humanized.srt)")
    ap.set_defaults(func=cmd_apply)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
