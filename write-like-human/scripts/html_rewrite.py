#!/usr/bin/env python3
"""Rewrite the visible text of a web page (.html) without touching the markup.

Two steps:

  1. extract: list every piece of visible text with a stable id.

       python html_rewrite.py extract about.html -o nodes.json

     JSON shape:
       {"file": "about.html", "nodes": [
          {"id": "t3", "tag": "p", "text": "We are a family bakery in Pune."}]}

     Text inside <script>, <style>, <code>, <pre>, <textarea>, and
     <template> is skipped, and so are pieces that are only whitespace.
     "tag" is the element the text sits in, to help you see where it is.
     Entities such as &amp; are shown decoded ("&").

  2. apply: give back new text for the ids you changed.

       python html_rewrite.py apply about.html changes.json

     With --attributes, extract also lists text that people read or hear
     but that sits inside a tag: alt, title, placeholder, and aria-label
     values, and the content of meta description tags (description,
     og:description, twitter:description). These get ids like "attr-2"
     and "tag" shows the element and attribute, for example "img@alt".
     Without the flag, extract output is exactly as before.

     changes.json can be {"t3": "new text", ...} or the edited output of
     extract (only nodes whose text changed are applied). Saved as
     about-humanized.html, next to the original, which is never
     overwritten. Everything outside the changed text (tags, attributes,
     links, scripts, styles, comments, spacing) stays byte for byte the
     same. The spaces and line breaks around each changed piece are kept.

     apply prints a CHECK line when the numbers in a piece of text
     changed, so you can make sure no price, date, or phone number moved.

Only uses the Python standard library (html.parser).
"""

import argparse
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

SKIP_TAGS = {"script", "style", "code", "pre", "textarea", "template"}
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
             "meta", "param", "source", "track", "wbr"}
NUMBER = re.compile(r"\d(?:[\d,.:/]*\d)?")
TEXT_ATTRS = {"alt", "title", "placeholder", "aria-label"}
META_NAMES = {"description", "og:description", "twitter:description"}
ATTR_RE = re.compile(
    r"""\s([^\s"'>/=]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+)))?""")


class _Spans(HTMLParser):
    """Finds the source ranges between markup, with the element they sit in."""

    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.source = source
        self.line_starts = [0]
        for m in re.finditer(r"\n", source):
            self.line_starts.append(m.end())
        self.stack = []
        self.prev_end = 0
        self.spans = []  # (start, end, tag, skipped)
        self.attrs = []  # (start, end, label, quote) of readable attribute values

    def _offset(self):
        line, col = self.getpos()
        return self.line_starts[line - 1] + col

    def _gap(self, start):
        if start > self.prev_end:
            skipped = any(t in SKIP_TAGS for t in self.stack)
            tag = self.stack[-1] if self.stack else ""
            self.spans.append((self.prev_end, start, tag, skipped))

    def _markup(self, end_finder):
        start = self._offset()
        self._gap(start)
        self.prev_end = end_finder(start)

    def _close_at(self, marker):
        def find(start):
            i = self.source.find(marker, start)
            return len(self.source) if i < 0 else i + len(marker)
        return find

    def _attributes(self, tag, start, text):
        if any(t in SKIP_TAGS for t in self.stack) or tag in SKIP_TAGS:
            return
        found = []
        for m in ATTR_RE.finditer(text):
            name = m.group(1).lower()
            for group, quote in ((2, '"'), (3, "'"), (4, "")):
                if m.group(group) is not None:
                    found.append((name, start + m.start(group), start + m.end(group), quote))
                    break
        names = {f[0]: f for f in found}
        if tag == "meta":
            key = (self.source[names["name"][1]:names["name"][2]] if "name" in names else
                   self.source[names["property"][1]:names["property"][2]] if "property" in names else "")
            if key.strip().lower() in META_NAMES and "content" in names:
                _, a, b, q = names["content"]
                self.attrs.append((a, b, "meta@content", q))
            return
        for name, a, b, q in found:
            if name in TEXT_ATTRS:
                self.attrs.append((a, b, "%s@%s" % (tag, name), q))

    def handle_starttag(self, tag, attrs):
        text = self.get_starttag_text() or ""
        self._attributes(tag, self._offset(), text)
        self._markup(lambda s: s + len(text))
        if tag not in VOID_TAGS:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        text = self.get_starttag_text() or ""
        self._attributes(tag, self._offset(), text)
        self._markup(lambda s: s + len(text))

    def handle_endtag(self, tag):
        self._markup(self._close_at(">"))
        if tag in self.stack:
            while self.stack:
                if self.stack.pop() == tag:
                    break

    def handle_comment(self, data):
        self._markup(self._close_at("-->"))

    def handle_decl(self, decl):
        self._markup(self._close_at(">"))

    def handle_pi(self, data):
        self._markup(self._close_at(">"))

    def unknown_decl(self, data):
        self._markup(self._close_at("]]>"))

    def finish(self):
        self.feed(self.source)
        self.close()
        self._gap(len(self.source))
        return self.spans


def find_nodes(source, attributes=False):
    parser = _Spans(source)
    nodes = []
    n = 0
    for start, end, tag, skipped in parser.finish():
        raw = source[start:end]
        if skipped or not raw.strip():
            continue
        n += 1
        lead = len(raw) - len(raw.lstrip())
        trail = len(raw) - len(raw.rstrip())
        core = raw[lead:len(raw) - trail]
        nodes.append({"id": "t%d" % n, "tag": tag,
                      "text": html.unescape(core),
                      "_start": start + lead, "_end": end - trail})
    if attributes:
        a = 0
        for start, end, label, quote in parser.attrs:
            raw = source[start:end]
            if not raw.strip():
                continue
            a += 1
            nodes.append({"id": "attr-%d" % a, "tag": label, "text": html.unescape(raw),
                          "_start": start, "_end": end, "_quote": quote})
    return nodes


def read(path):
    with open(path, encoding="utf-8-sig") as fh:
        return fh.read()


def cmd_extract(args):
    nodes = find_nodes(read(args.file), attributes=args.attributes)
    out = {"file": os.path.basename(args.file),
           "nodes": [{k: v for k, v in n.items() if not k.startswith("_")} for n in nodes]}
    text = json.dumps(out, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("Wrote %d text pieces to %s" % (len(nodes), args.output))
    else:
        print(text)


def load_changes(path, nodes):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    original = {n["id"]: n["text"] for n in nodes}
    if isinstance(data, dict) and isinstance(data.get("nodes"), list):
        return {n["id"]: n["text"] for n in data["nodes"]
                if "id" in n and "text" in n and original.get(n["id"]) != n["text"]}
    if isinstance(data, dict):
        return {str(k): v for k, v in data.items()}
    raise SystemExit("changes.json must be an object of id to text, or extract output")


def default_output(path):
    base, ext = os.path.splitext(path)
    return base + "-humanized" + (ext or ".html")


def cmd_apply(args):
    source = read(args.file)
    nodes = find_nodes(source, attributes=True)
    changes = load_changes(args.changes, nodes)
    by_id = {n["id"]: n for n in nodes}
    unknown = [k for k in changes if k not in by_id]
    if unknown:
        print("Unknown ids (nothing written): %s" % ", ".join(sorted(unknown)), file=sys.stderr)
        sys.exit(1)

    out_path = args.output or default_output(args.file)
    if os.path.abspath(out_path) == os.path.abspath(args.file):
        print("Refusing to overwrite the original file. Choose another output name.", file=sys.stderr)
        sys.exit(1)

    pieces = []
    pos = 0
    changed = 0
    for node in sorted(nodes, key=lambda n: n["_start"]):
        new = changes.get(node["id"])
        if new is None or new == node["text"]:
            continue
        old_numbers = NUMBER.findall(node["text"])
        new_numbers = NUMBER.findall(new)
        if sorted(old_numbers) != sorted(new_numbers):
            print("CHECK %s: numbers changed from %s to %s"
                  % (node["id"], old_numbers or "none", new_numbers or "none"))
        pieces.append(source[pos:node["_start"]])
        if "_quote" not in node:
            pieces.append(html.escape(new, quote=False))
        elif node["_quote"] == '"':
            pieces.append(html.escape(new, quote=False).replace('"', "&quot;"))
        elif node["_quote"] == "'":
            pieces.append(html.escape(new, quote=False).replace("'", "&#39;"))
        else:
            # Unquoted value: keep it unquoted if it is still one safe word.
            escaped = html.escape(new, quote=False)
            if re.fullmatch(r"[^\s\"'=<>`]+", escaped):
                pieces.append(escaped)
            else:
                pieces.append('"' + escaped.replace('"', "&quot;") + '"')
        pos = node["_end"]
        changed += 1
    pieces.append(source[pos:])

    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("".join(pieces))
    print("Changed %d text pieces. Saved %s" % (changed, out_path))


def main():
    parser = argparse.ArgumentParser(description="Rewrite web page text, keep the markup.")
    sub = parser.add_subparsers(dest="command", required=True)
    ex = sub.add_parser("extract", help="list visible text as JSON")
    ex.add_argument("file")
    ex.add_argument("-o", "--output", help="write JSON here instead of printing it")
    ex.add_argument("--attributes", action="store_true",
                    help="also list alt, title, placeholder, aria-label, and meta description text")
    ex.set_defaults(func=cmd_extract)
    ap = sub.add_parser("apply", help="write new text into a copy of the page")
    ap.add_argument("file")
    ap.add_argument("changes", help="JSON of id to new text")
    ap.add_argument("-o", "--output", help="output path (default <name>-humanized.html)")
    ap.set_defaults(func=cmd_apply)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
