#!/usr/bin/env python3
"""Rewrite the prose in a LaTeX file without touching commands or maths.

Works like the other scripts:

  1. extract: list every piece of prose with an id.
       python latex_rewrite.py extract thesis.tex > segments.json
  2. apply: give back new text for the ids you changed.
       python latex_rewrite.py apply thesis.tex changes.json
     This writes thesis-humanized.tex. The original is never overwritten.

Only text between \\begin{document} and \\end{document} is offered (the
whole file if there is no \\begin{document}). These are always left alone:
  - the preamble, and comments (% to the end of the line)
  - maths: $...$, $$...$$, \\(...\\), \\[...\\], and environments such as
    equation, align, gather, multline, and their starred forms
  - verbatim, lstlisting, minted, and comment environments
  - command names, and the arguments of commands that hold no prose, such
    as \\cite, \\ref, \\label, \\includegraphics, \\url, \\href (the link),
    \\input, \\begin and \\end names, and lengths
  - table separators (& and \\\\)
The text inside commands like \\emph{...}, \\section{...}, \\caption{...},
and \\footnote{...} is prose, so it is offered as its own segment.

Everything outside the changed segments is kept byte for byte. Each
segment keeps its original leading and trailing spaces and line breaks.

A change is skipped, with a message, if the new text contains a
command (a backslash other than an escaped \\%, \\$, \\&, \\# or \\_), a
brace, or an unescaped %, $, &, #, ^ or _, since those would change the
LaTeX itself. Use --force to apply such changes anyway. When any change
is skipped, the file is still written but the script exits with code 2,
so a skipped change can't go unnoticed.

Only uses the standard library.
"""

import argparse
import json
import os
import re
import sys

NO_PROSE_COMMANDS = {
    "cite", "citep", "citet", "citealp", "citeauthor", "citeyear", "parencite", "textcite", "autocite",
    "footcite", "nocite", "ref", "eqref", "pageref", "autoref", "cref", "Cref", "nameref", "label",
    "includegraphics", "url", "input", "include", "bibliography", "bibliographystyle", "addbibresource",
    "usepackage", "documentclass", "newcommand", "renewcommand", "providecommand", "def", "let",
    "setlength", "addtolength", "setcounter", "addtocounter", "vspace", "hspace", "vskip", "hskip",
    "begin", "end", "pagestyle", "thispagestyle", "pagenumbering", "graphicspath", "hypersetup",
    "geometry", "newenvironment", "renewenvironment", "color", "definecolor", "linewidth", "textwidth",
    "rule", "raisebox", "resizebox", "scalebox", "multicolumn", "multirow", "cline", "hline",
    "toprule", "midrule", "bottomrule", "small", "large", "Large", "footnotesize", "centering",
    "newline", "linebreak", "pagebreak", "newpage", "clearpage", "maketitle", "tableofcontents",
    "listoffigures", "listoftables", "printbibliography", "appendix", "noindent", "par", "item",
}
# Commands whose first argument is a link or key, with later arguments that are prose.
FIRST_ARG_NOT_PROSE = {"href"}
MATH_ENVS = {"equation", "align", "gather", "multline", "flalign", "alignat", "eqnarray", "displaymath",
             "math", "split", "subequations"}
VERBATIM_ENVS = {"verbatim", "Verbatim", "lstlisting", "minted", "comment", "tikzpicture", "filecontents"}
UNSAFE = re.compile(r"\\(?![%$&#_])|[{}]|(?<!\\)[%$&#^_]")
LETTER = re.compile(r"[^\W\d_]{2,}", re.UNICODE)


def humanized_path(path):
    root, ext = os.path.splitext(path)
    return "%s-humanized%s" % (root, ext or ".tex")


def skip_group(src, i, open_ch, close_ch):
    """src[i] == open_ch. Return the index just past the matching close."""
    depth = 0
    n = len(src)
    while i < n:
        c = src[i]
        if c == "\\":
            i += 2
            continue
        if c == open_ch:
            depth += 1
        elif c == close_ch:
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return n


def skip_spaces(src, i):
    while i < len(src) and src[i] in " \t":
        i += 1
    return i


def find_env_end(src, i, name):
    m = re.compile(r"\\end\s*\{\s*%s\s*\}" % re.escape(name)).search(src, i)
    return m.end() if m else len(src)


def segments(src):
    """Return (body_start, body_end, list of (start, end)) for prose spans."""
    begin = re.search(r"\\begin\s*\{\s*document\s*\}", src)
    end = re.search(r"\\end\s*\{\s*document\s*\}", src)
    lo = begin.end() if begin else 0
    hi = end.start() if end and (not begin or end.start() > lo) else len(src)
    spans = []
    text_start = None
    i = lo

    def close_text(at):
        nonlocal text_start
        if text_start is not None and at > text_start:
            spans.append((text_start, at))
        text_start = None

    while i < hi:
        c = src[i]
        # Paragraph breaks end a segment.
        if c == "\n" and src[i + 1:i + 2] == "\n" or (c == "\n" and re.match(r"\n[ \t]*\n", src[i:i + 8])):
            close_text(i)
            i += 1
            continue
        if c == "%":
            close_text(i)
            nl = src.find("\n", i)
            i = hi if nl == -1 or nl > hi else nl
            continue
        if c == "$":
            close_text(i)
            if src[i + 1:i + 2] == "$":
                j = src.find("$$", i + 2)
                i = hi if j == -1 else j + 2
            else:
                j = i + 1
                while j < hi and not (src[j] == "$" and src[j - 1] != "\\"):
                    j += 1
                i = j + 1
            continue
        if c in "{}&~":
            close_text(i)
            i += 1
            continue
        if c == "\\":
            nxt = src[i + 1:i + 2]
            if nxt and nxt in "%$&#_" :
                # Escaped character such as \% or \&: it belongs to the text.
                if text_start is None:
                    text_start = i
                i += 2
                continue
            close_text(i)
            if nxt in ("(", "["):
                closer = "\\)" if nxt == "(" else "\\]"
                j = src.find(closer, i + 2)
                i = hi if j == -1 else j + 2
                continue
            if nxt == "\\":
                i += 2
                if src[i:i + 1] == "[":
                    i = skip_group(src, i, "[", "]")
                continue
            m = re.match(r"\\([A-Za-z@]+)\*?", src[i:])
            if not m:
                i += 2
                continue
            name = m.group(1)
            i += m.end()
            if name == "begin":
                j = skip_spaces(src, i)
                em = re.match(r"\{\s*([A-Za-z*]+)\s*\}", src[j:])
                if em:
                    env = em.group(1).rstrip("*")
                    i = j + em.end()
                    if env in MATH_ENVS or env in VERBATIM_ENVS:
                        i = find_env_end(src, i, em.group(1))
                    else:
                        # Skip optional and required arguments right after \begin{env}.
                        while True:
                            k = skip_spaces(src, i)
                            if src[k:k + 1] == "[":
                                i = skip_group(src, k, "[", "]")
                            elif src[k:k + 1] == "{" and env in ("tabular", "tabularx", "longtable", "array", "minipage", "figure", "table", "wrapfigure"):
                                i = skip_group(src, k, "{", "}")
                            else:
                                break
                continue
            if name in NO_PROSE_COMMANDS:
                while True:
                    k = skip_spaces(src, i)
                    if src[k:k + 1] == "[":
                        i = skip_group(src, k, "[", "]")
                    elif src[k:k + 1] == "{" and name not in ("item", "par", "noindent", "centering", "small",
                                                                "large", "Large", "footnotesize", "newline",
                                                                "linebreak", "pagebreak", "newpage", "clearpage",
                                                                "maketitle", "tableofcontents", "appendix",
                                                                "hline", "toprule", "midrule", "bottomrule",
                                                                "printbibliography", "listoffigures", "listoftables"):
                        i = skip_group(src, k, "{", "}")
                    else:
                        break
                continue
            if name in FIRST_ARG_NOT_PROSE:
                k = skip_spaces(src, i)
                if src[k:k + 1] == "{":
                    i = skip_group(src, k, "{", "}")
                continue
            # Other commands: skip optional arguments; the {text} that follows is prose.
            k = skip_spaces(src, i)
            while src[k:k + 1] == "[":
                i = skip_group(src, k, "[", "]")
                k = skip_spaces(src, i)
            continue
        if text_start is None:
            text_start = i
        i += 1
    close_text(hi)
    return lo, hi, [(a, b) for a, b in spans if LETTER.search(src[a:b])]


def split_ws(text):
    m = re.match(r"^(\s*)(.*?)(\s*)$", text, re.S)
    return m.group(1), m.group(2), m.group(3)


def cmd_extract(args):
    with open(args.file, encoding="utf-8", newline="") as fh:
        src = fh.read()
    _, _, spans = segments(src)
    out = []
    for n, (a, b) in enumerate(spans, 1):
        lead = split_ws(src[a:b])[0]
        line = src.count("\n", 0, a + len(lead)) + 1
        out.append({"id": "t%d" % n, "line": line, "text": split_ws(src[a:b])[1]})
    payload = json.dumps({"file": os.path.basename(args.file), "segments": out}, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(payload)
        print("Wrote %d %s to %s" % (len(out), "segment" if len(out) == 1 else "segments", args.output))
    else:
        print(payload)


def cmd_apply(args):
    with open(args.file, encoding="utf-8", newline="") as fh:
        src = fh.read()
    with open(args.changes, encoding="utf-8") as fh:
        data = json.load(fh)
    if isinstance(data, dict) and isinstance(data.get("segments"), list):
        data = data["segments"]
    if isinstance(data, list):
        changes = {d["id"]: d["text"] for d in data}
    else:
        changes = {k: (v.get("text", "") if isinstance(v, dict) else v) for k, v in data.items()}
    out_path = args.output or humanized_path(args.file)
    if os.path.abspath(out_path) == os.path.abspath(args.file):
        sys.exit("Refusing to overwrite the original. Choose a different output name.")
    _, _, spans = segments(src)
    by_id = {"t%d" % n: span for n, span in enumerate(spans, 1)}
    unknown = sorted(set(changes) - set(by_id))
    for pid in unknown:
        print("SKIPPED %s: no such segment" % pid)
    edits, skipped = [], 0
    for pid, new in changes.items():
        if pid not in by_id:
            continue
        a, b = by_id[pid]
        lead, old, trail = split_ws(src[a:b])
        new = new.strip()
        if new == old:
            continue
        if UNSAFE.search(new) and not args.force:
            print("SKIPPED %s: the new text has a backslash, a brace, or a LaTeX special character. "
                  "Fix it or use --force." % pid)
            skipped += 1
            continue
        if re.findall(r"\d[\d,.]*", old) != re.findall(r"\d[\d,.]*", new):
            print("CHECK %s: the numbers changed. Make sure that was intended." % pid)
        edits.append((a, b, lead + new + trail))
    result = src
    for a, b, text in sorted(edits, reverse=True):
        result = result[:a] + text + result[b:]
    with open(out_path, "w", encoding="utf-8", newline="") as fh:
        fh.write(result)
    print("Wrote %s with %d changed %s%s." % (out_path, len(edits),
                                             "segment" if len(edits) == 1 else "segments",
                                             (", %d skipped" % skipped) if skipped else ""))
    if skipped:
        # Exit code 2: the file was written, but some changes were left out.
        sys.exit(2)


def main():
    parser = argparse.ArgumentParser(description="Rewrite the prose in a LaTeX file, leaving commands and maths alone.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("extract", help="list prose segments with ids")
    e.add_argument("file")
    e.add_argument("-o", "--output", help="write the JSON here instead of printing it")
    e.set_defaults(func=cmd_extract)
    a = sub.add_parser("apply", help="write a new .tex with your changes")
    a.add_argument("file")
    a.add_argument("changes", help="JSON mapping segment id to new text")
    a.add_argument("-o", "--output", help="output path (default: <name>-humanized.tex)")
    a.add_argument("--force", action="store_true", help="apply changes even if they contain LaTeX characters")
    a.set_defaults(func=cmd_apply)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
