#!/usr/bin/env python3
"""Rewrite the comments and docstrings in a source file without touching the code.

Works like the other scripts:

  1. extract: list every comment with an id.
       python code_comments.py extract app.py -o comments.json
  2. apply: give back new text for the ids you changed.
       python code_comments.py apply app.py changes.json
     This writes app-humanized.py. The original is never overwritten,
     unless you ask for --in-place (see below).

JSON shape from extract:
  {"file": "app.py", "language": "python", "comments": [
     {"id": "c1", "line": 3, "kind": "line", "text": "Load the config.\\nFall back to defaults."},
     {"id": "c2", "line": 9, "kind": "docstring", "text": "Return the user name."},
     {"id": "c3", "line": 1, "kind": "line", "text": "/usr/bin/env python3", "skip": "shebang line"}]}

"text" is only the prose: the comment markers (#, //, /* */, the " * " at
the start of block lines, and docstring quotes) are left out, and line
breaks inside a comment are kept as "\\n". Full-line comments that sit on
consecutive lines with the same indentation are merged into one entry, so
you can rewrite them as a paragraph. A comment after code on the same line
is its own entry. "kind" is "line", "block" or "docstring".

changes.json can be {"c1": "new text", ...} or the extract output with the
texts edited. Each comment is written back in its original style: the same
markers, the same indentation, the same " * " prefix, the same docstring
quotes. Nothing is wrapped for you: each line of new text becomes one
comment line.

Supported files:
  Python (.py): # comments and docstrings (module, class and function).
  C-style (.js .jsx .mjs .cjs .ts .tsx .java .go .c .h .cpp .hpp .cc .cs
    .kt .swift .rs .php .scala .dart): // and /* */ comments, including
    /** */ doc comments. Strings are skipped, so "http://" in a string is
    not a comment.
  Hash comments (.sh .bash .zsh .rb .yaml .yml .toml .r .pl): # comments.

These are listed with a "skip" reason and never changed: shebangs,
encoding lines, license and copyright notices, tool directives (noqa,
type: ignore, eslint-disable, @ts-ignore, //go:build, rubocop:, and so
on) and comments that look like commented-out code.

In doc comments, lines that start with @word or :word (like @param or
:returns:), section headers such as Args:, Returns: and Raises:, and
doctest lines (>>>) must stay exactly as they were. If one is changed or
removed, that change is skipped.

Safety: the code never changes. After building the new file, the script
removes every comment from both the original and the new file and checks
that what is left is identical, byte for byte. For Python it also checks
that the new file parses and has the same syntax tree. If either check
fails, nothing is written and the script exits with code 1.

A change is skipped, with a message, if it would break the comment: */
inside a block comment, the docstring's own quotes, or a line break in a
comment that shares its line with code. When any change is skipped, the
file is still written but the script exits with code 2.

Everything else stays byte for byte: line endings (CRLF stays CRLF), a
byte-order mark, tabs and trailing spaces. A changes file with no changes
gives an identical copy.

Output:
  default         <name>-humanized<ext>, next to the original
  -o OUT          another name (it can't be the original file)
  --in-place      overwrite the original, but only if git tracks the file
                  and it has no uncommitted changes, so you can review the
                  change with git diff and undo it with git checkout

Known limits: JavaScript regex literals are detected with a simple rule,
and text inside JSX tags is treated as code. Perl quote operators (q, qw,
s///), Ruby %-literals and Ruby regex literals are not parsed. In those
rare spots a comment may be missed or a # inside them may be listed as a
comment, so check the diff.

Only uses the standard library (Python 3.8+).
"""

import argparse
import ast
import bisect
import io
import json
import os
import re
import subprocess
import sys
import textwrap
import tokenize
import warnings
from collections import Counter

C_LANGS = {
    ".js": "javascript", ".jsx": "javascript", ".mjs": "javascript", ".cjs": "javascript",
    ".ts": "typescript", ".tsx": "typescript", ".java": "java", ".go": "go", ".c": "c", ".h": "c",
    ".cpp": "cpp", ".hpp": "cpp", ".cc": "cpp", ".cs": "csharp", ".kt": "kotlin", ".swift": "swift",
    ".rs": "rust", ".php": "php", ".scala": "scala", ".dart": "dart",
}
HASH_LANGS = {
    ".sh": "shell", ".bash": "shell", ".zsh": "shell", ".rb": "ruby", ".yaml": "yaml", ".yml": "yaml",
    ".toml": "toml", ".r": "r", ".pl": "perl",
}
SUPPORTED = [".py"] + list(C_LANGS) + list(HASH_LANGS)

JS = {"javascript", "typescript"}
NESTING = {"rust", "swift", "kotlin", "scala", "dart"}
CHAR_LIT = {"c", "cpp", "java", "go", "csharp", "kotlin", "rust", "scala"}
TRIPLE = {"java", "kotlin", "swift", "scala", "dart", "csharp"}
NO_ESCAPE_TRIPLE = {"kotlin", "scala", "csharp"}
DOLLAR_INTERP = {"kotlin", "scala", "dart"}
MULTILINE_STR = {"rust", "php"}
SQ_STRING = {"javascript", "typescript", "php", "dart"}
SHELL = {"shell"}
REGEX_KEYWORDS = {"return", "typeof", "instanceof", "in", "of", "new", "delete", "void", "throw",
                  "case", "do", "else", "yield", "await"}

CHAR_RE = re.compile(r"'(?:\\[^\n]{1,10}?|[^\\\n])'")
RUST_RAW = re.compile(r'b?r(#*)"')
CPP_RAW = re.compile(r'(?:u8|u|U|L)?R"([^()\\\s]{0,16})\(')
DART_RAW = re.compile(r"r('''|\"\"\"|'|\")")
SWIFT_RAW = re.compile(r'(#+)("""|")')
PHP_HEREDOC = re.compile(r'<<<[ \t]*(["\']?)([A-Za-z_]\w*)\1\r?\n')
HEREDOC = re.compile(r"<<([-~]?)[ \t]*([\"']?)([A-Za-z_]\w*)\2")
WORD = re.compile(r"[\w$]+")
LETTER = re.compile(r"[^\W\d_]", re.UNICODE)

DIRECTIVE_I = re.compile(
    r"\bnoqa\b|type:\s*ignore|\bpylint:|\bpyright:|\bmypy:|\bisort:|\bfmt:\s*(?:off|on|skip)\b|\bpragma:"
    r"|eslint|jshint|jslint|@ts-|prettier-ignore|\bistanbul\b|\b(?:c8|v8)\s+ignore|rubocop:|shellcheck"
    r"|\bnolint\b|nosonar|clang-format|sourcemappingurl|sourceurl=|frozen_string_literal|yamllint"
    r"|swiftlint:|ktlint|\bnosec\b|cspell|spell-checker|codespell|@formatter:|noinspection|warn_indent:",
    re.I)
DIRECTIVE_CS = re.compile(
    r"^go:|^\+build\b|^#?\s*(?:end)?region\b|^<reference\b|@flow\b|@jsx\b|__PURE__|webpack[A-Z]\w*:"
    r"|@vite-ignore|-\*-.*-\*-|\bvim?:|^(?:global|globals|exported)\s+[\w$]+(?:\s*:\s*\w+)?"
    r"(?:\s*,\s*[\w$]+(?:\s*:\s*\w+)?)*\s*$|@(?:license|preserve)\b",
    re.M)
GO_DIRECTIVE = re.compile(r"^//(?:go:|line |export |extern |nolint)")
LICENSE = re.compile(
    r"^\W*copyright\b|copyright\s+(?:\(c\)\s*)?(?:\d{4}|\u00a9)|\(c\)\s*\d{4}|\u00a9|spdx-license"
    r"|all rights reserved|licensed under|permission is hereby granted|@license\b|^\W*license\s*:"
    r"|\b(?:MIT|BSD|Apache|Mozilla Public|GNU (?:Lesser |Affero )?General Public) Licen[cs]e\b", re.I | re.M)
ENCODING = re.compile(r"coding[:=]\s*[-\w.]+")
TAG_LINE = re.compile(
    r"^(?:[@:]\w|>>>|\.\.\.(?:\s|$)|```|[-=~]{3,}$|(?:Args|Arguments|Parameters|Params|Returns?|Raises|"
    r"Yields?|Attributes|Examples?|Notes?|See Also|Keyword Args|Keyword Arguments|Other Parameters|Warns|"
    r"Warnings|References|Todo)\s*:?$)")
INLINE_TAG = re.compile(r"\{@\w+[^}]*\}|</?\w+[^<>]*>")


class ScanError(Exception):
    pass


def plural(n, word):
    return "%d %s%s" % (n, word, "" if n == 1 else "s")


def humanized_path(path):
    root, ext = os.path.splitext(path)
    return "%s-humanized%s" % (root, ext)


def language_for(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".py":
        return "python"
    return C_LANGS.get(ext) or HASH_LANGS.get(ext)


def line_end(s, i):
    """End of the comment that starts at i: before \\r\\n or \\n."""
    j = s.find("\n", i)
    if j == -1:
        j = len(s)
    if j > i and s[j - 1] == "\r":
        j -= 1
    return j


# ---------------------------------------------------------------- C-style


class CScanner:
    def __init__(self, src, lang):
        self.s = src
        self.n = len(src)
        self.lang = lang
        self.tokens = []
        self.nested = 0
        self.prev = None
        self.prev_word = ""

    def run(self):
        self.code(0, None)
        return self.tokens

    def add(self, start, end, kind, **extra):
        tok = {"start": start, "end": end, "kind": kind, "nested": self.nested > 0}
        tok.update(extra)
        self.tokens.append(tok)

    def code(self, i, close):
        s, n, lang = self.s, self.n, self.lang
        opener = {"}": "{", ")": "("}.get(close)
        depth = 0
        number = re.compile(r"\d[\w.']*" if lang in ("c", "cpp") else r"\d[\w.]*")
        while i < n:
            c = s[i]
            nx = s[i + 1] if i + 1 < n else ""
            if c == "/" and nx == "/":
                e = line_end(s, i)
                self.add(i, e, "line")
                i = e
                continue
            if c == "/" and nx == "*":
                i = self.block(i)
                continue
            if c == "#" and lang == "php" and nx != "[":
                e = line_end(s, i)
                self.add(i, e, "line")
                i = e
                continue
            if c in " \t\r\n\f\v":
                i += 1
                continue
            if close:
                if c == opener:
                    depth += 1
                elif c == close:
                    if depth == 0:
                        return i + 1
                    depth -= 1
            j = self.literal(i)
            if j is not None:
                self.prev = '"'
                i = max(j, i + 1)
                continue
            if c.isalpha() or c in "_$":
                m = WORD.match(s, i)
                self.prev, self.prev_word = "a", m.group()
                i = m.end()
                continue
            if c.isdigit():
                self.prev = "0"
                i = number.match(s, i).end()
                continue
            self.prev = c
            i += 1
        return n

    def nested_code(self, i, close):
        saved = (self.prev, self.prev_word)
        self.nested += 1
        self.prev = None
        end = self.code(i, close)
        self.nested -= 1
        self.prev, self.prev_word = saved
        return end

    def block(self, i):
        s, n = self.s, self.n
        j, depth = i + 2, 1
        nest = self.lang in NESTING
        while j < n:
            if s.startswith("*/", j):
                depth -= 1
                j += 2
                if depth == 0:
                    self.add(i, j, "block")
                    return j
                continue
            if nest and s.startswith("/*", j):
                depth += 1
                j += 2
                continue
            j += 1
        self.add(i, n, "block", unterminated=True)
        return n

    def find_end(self, i, closer):
        j = self.s.find(closer, i)
        return self.n if j == -1 else j + len(closer)

    def literal(self, i):
        s, lang = self.s, self.lang
        c = s[i]
        prevc = s[i - 1] if i > 0 else ""
        if not (prevc.isalnum() or prevc == "_"):
            if lang == "rust" and c in "br":
                m = RUST_RAW.match(s, i)
                if m:
                    return self.find_end(m.end(), '"' + m.group(1))
            if lang in ("c", "cpp") and c in "uULR":
                m = CPP_RAW.match(s, i)
                if m:
                    return self.find_end(m.end(), ")" + m.group(1) + '"')
            if lang == "dart" and c == "r":
                m = DART_RAW.match(s, i)
                if m:
                    q = m.group(1)
                    if len(q) == 3:
                        return self.find_end(m.end(), q)
                    j = m.end()
                    while j < self.n and s[j] != q and s[j] != "\n":
                        j += 1
                    return j + 1 if j < self.n and s[j] == q else j
        if lang == "swift" and c == "#":
            m = SWIFT_RAW.match(s, i)
            if m:
                return self.find_end(m.end(), m.group(2) + m.group(1))
        if c == '"':
            if lang == "csharp" and prevc == "@":
                return self.verbatim(i)
            if lang in TRIPLE and s.startswith('"""', i):
                return self.triple(i, '"')
            return self.quoted(i, '"')
        if c == "'":
            if lang in SQ_STRING:
                if lang == "dart" and s.startswith("'''", i):
                    return self.triple(i, "'")
                return self.quoted(i, "'")
            if lang in CHAR_LIT:
                m = CHAR_RE.match(s, i)
                return m.end() if m else None
            return None
        if c == "`":
            if lang in JS:
                return self.template(i)
            if lang == "go":
                return self.find_end(i + 1, "`")
            if lang in ("kotlin", "scala", "swift"):
                j = s.find("`", i + 1)
                nl = s.find("\n", i + 1)
                if j == -1 or (nl != -1 and nl < j):
                    return None
                return j + 1
            return None
        if c == "/" and lang in JS and self.regex_ok():
            return self.regex(i)
        if c == "<" and lang == "php" and s.startswith("<<<", i):
            m = PHP_HEREDOC.match(s, i)
            if m:
                end = re.compile(r"^[ \t]*" + re.escape(m.group(2)) + r"\b", re.M).search(s, m.end())
                return end.end() if end else self.n
        return None

    def quoted(self, i, q):
        s, n, lang = self.s, self.n, self.lang
        j = i + 1
        while j < n:
            ch = s[j]
            if ch == "\\":
                if lang == "swift" and s[j + 1:j + 2] == "(":
                    j = self.nested_code(j + 2, ")")
                    continue
                j += 2
                continue
            if ch == q:
                return j + 1
            if ch == "\n" and lang not in MULTILINE_STR:
                return j
            if ch == "$" and s[j + 1:j + 2] == "{" and lang in DOLLAR_INTERP:
                j = self.nested_code(j + 2, "}")
                continue
            j += 1
        return n

    def triple(self, i, q):
        s, n, lang = self.s, self.n, self.lang
        k = 0
        while i + k < n and s[i + k] == q:
            k += 1
        if lang != "csharp":
            k = 3
        j = i + k
        while j < n:
            ch = s[j]
            if ch == "\\" and lang not in NO_ESCAPE_TRIPLE:
                if lang == "swift" and s[j + 1:j + 2] == "(":
                    j = self.nested_code(j + 2, ")")
                    continue
                j += 2
                continue
            if ch == "$" and s[j + 1:j + 2] == "{" and lang in DOLLAR_INTERP:
                j = self.nested_code(j + 2, "}")
                continue
            if s.startswith(q * k, j):
                j += k
                while j < n and s[j] == q:
                    j += 1
                return j
            j += 1
        return n

    def verbatim(self, i):
        s, n = self.s, self.n
        j = i + 1
        while j < n:
            if s[j] == '"':
                if s[j + 1:j + 2] == '"':
                    j += 2
                    continue
                return j + 1
            j += 1
        return n

    def template(self, i):
        s, n = self.s, self.n
        j = i + 1
        while j < n:
            ch = s[j]
            if ch == "\\":
                j += 2
                continue
            if ch == "`":
                return j + 1
            if ch == "$" and s[j + 1:j + 2] == "{":
                j = self.nested_code(j + 2, "}")
                continue
            j += 1
        return n

    def regex_ok(self):
        if self.prev is None or self.prev in "(,=:[!&|?{};+-*%<>~^":
            return True
        return self.prev == "a" and self.prev_word in REGEX_KEYWORDS

    def regex(self, i):
        s, n = self.s, self.n
        j, in_class = i + 1, False
        while j < n:
            ch = s[j]
            if ch == "\\":
                j += 2
                continue
            if ch == "\n":
                return None
            if in_class:
                if ch == "]":
                    in_class = False
            elif ch == "[":
                in_class = True
            elif ch == "/":
                j += 1
                while j < n and (s[j].isalnum()):
                    j += 1
                return j
            j += 1
        return None


# ------------------------------------------------------------ hash comments


class HashScanner:
    def __init__(self, src, lang):
        self.s = src
        self.n = len(src)
        self.lang = lang
        self.tokens = []
        self.nested = 0
        self.heredocs = []
        self.block_parent = None
        self.done = False

    def run(self):
        self.code(0, None)
        return self.tokens

    def at_line_start(self, i):
        """Skip lines that hold no code at all. Return the new index."""
        s, n, lang = self.s, self.n, self.lang
        while i < n:
            eol = s.find("\n", i)
            nxt = n if eol == -1 else eol + 1
            line = s[i:nxt].rstrip("\r\n")
            if self.heredocs:
                word, indented = self.heredocs[0]
                if (line.strip() if indented else line) == word:
                    self.heredocs.pop(0)
                i = nxt
                continue
            if self.block_parent is not None:
                ind = len(line) - len(line.lstrip(" \t"))
                if not line.strip() or ind > self.block_parent:
                    i = nxt
                    continue
                self.block_parent = None
            if lang in ("ruby", "perl") and line in ("__END__", "__DATA__"):
                self.done = True
                return n
            if (lang == "perl" and re.match(r"=[A-Za-z]", line)) or (lang == "ruby" and line.startswith("=begin")):
                end_word = "=cut" if lang == "perl" else "=end"
                m = re.compile(r"^" + end_word + r"\b.*$", re.M).search(s, nxt)
                i = n if not m else min(n, m.end() + 1)
                continue
            return i
        return i

    def code(self, i, close):
        s, n, lang = self.s, self.n, self.lang
        opener = {"}": "{", ")": "("}.get(close)
        depth = 0
        if i == 0:
            i = self.at_line_start(0)
        while i < n and not self.done:
            c = s[i]
            if c == "\n":
                if lang == "yaml":
                    self.check_block_scalar(i)
                i = self.at_line_start(i + 1)
                continue
            if c == "#":
                prevc = s[i - 1] if i > 0 else "\n"
                if prevc in " \t\r\n":
                    e = line_end(s, i)
                    self.add(i, e)
                    i = e
                    continue
                i += 1
                continue
            if close:
                if c == opener:
                    depth += 1
                elif c == close:
                    if depth == 0:
                        return i + 1
                    depth -= 1
            if c == "\\" and lang in SHELL:
                i += 2
                continue
            if c in "'\"":
                j = self.string(i)
                if j is not None:
                    i = j
                    continue
            if c == "`" and lang in ("shell", "ruby", "perl", "r"):
                i = self.backtick(i)
                continue
            if c == "<" and lang in ("shell", "ruby", "perl") and s.startswith("<<", i) and (i == 0 or s[i - 1] != "<"):
                m = HEREDOC.match(s, i)
                if m:
                    indented = bool(m.group(1))
                    self.heredocs.append((m.group(3), indented))
                    i = m.end()
                    continue
            if c == "$" and lang in SHELL and s[i + 1:i + 2] == "'":
                i = self.simple(i + 1, "'", escapes=True)
                continue
            i += 1
        return n

    def add(self, start, end):
        self.tokens.append({"start": start, "end": end, "kind": "line", "nested": self.nested > 0})

    def check_block_scalar(self, i):
        s = self.s
        ls = s.rfind("\n", 0, i) + 1
        cut = i
        for tok in reversed(self.tokens):
            if tok["start"] < ls:
                break
            cut = min(cut, tok["start"])
        code = s[ls:cut].rstrip(" \t\r")
        if re.search(r"(?:^|\s)[|>][-+1-9]{0,2}$", code):
            line = s[ls:i]
            self.block_parent = len(line) - len(line.lstrip(" \t"))

    def boundary(self, i):
        prevc = self.s[i - 1] if i > 0 else "\n"
        return prevc.isspace() or prevc in "=([{,:;|&!+<>-*%?~'\""

    def nested_code(self, i, close):
        self.nested += 1
        end = self.code(i, close)
        self.nested -= 1
        return end

    def simple(self, i, q, escapes):
        s, n = self.s, self.n
        j = i + 1
        while j < n:
            ch = s[j]
            if escapes and ch == "\\":
                j += 2
                continue
            if ch == q:
                return j + 1
            j += 1
        return n

    def backtick(self, i):
        if self.lang == "r":
            j = self.s.find("`", i + 1)
            nl = self.s.find("\n", i + 1)
            if j == -1 or (nl != -1 and nl < j):
                return i + 1
            return j + 1
        return self.simple(i, "`", escapes=True)

    def string(self, i):
        s, n, lang = self.s, self.n, self.lang
        q = s[i]
        if lang in SHELL:
            if q == "'":
                return self.simple(i, "'", escapes=False)
            j = i + 1
            while j < n:
                ch = s[j]
                if ch == "\\":
                    j += 2
                    continue
                if ch == '"':
                    return j + 1
                if ch == "$" and s[j + 1:j + 2] in ("(", "{"):
                    j = self.nested_code(j + 2, ")" if s[j + 1] == "(" else "}")
                    continue
                if ch == "`":
                    j = self.backtick(j)
                    continue
                j += 1
            return n
        if not self.boundary(i):
            return None
        if lang == "toml":
            if s.startswith(q * 3, i):
                j = i + 3
                while j < n:
                    if q == '"' and s[j] == "\\":
                        j += 2
                        continue
                    if s.startswith(q * 3, j):
                        j += 3
                        while j < n and s[j] == q:
                            j += 1
                        return j
                    j += 1
                return n
            j = i + 1
            while j < n and s[j] != "\n":
                if q == '"' and s[j] == "\\":
                    j += 2
                    continue
                if s[j] == q:
                    return j + 1
                j += 1
            return j
        if lang == "yaml" and q == "'":
            j = i + 1
            while j < n:
                if s[j] == "'":
                    if s[j + 1:j + 2] == "'":
                        j += 2
                        continue
                    return j + 1
                j += 1
            return n
        j = i + 1
        while j < n:
            ch = s[j]
            if ch == "\\":
                j += 2
                continue
            if ch == q:
                return j + 1
            if lang == "ruby" and q == '"' and ch == "#" and s[j + 1:j + 2] == "{":
                j = self.nested_code(j + 2, "}")
                continue
            j += 1
        return n


# ------------------------------------------------------------------ Python


def char_col(line, byte_col):
    return len(line.encode("utf-8")[:byte_col].decode("utf-8", "ignore"))


def doc_owners(tree):
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and node.body:
            first = node.body[0]
            if (isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant)
                    and isinstance(first.value.value, str)):
                yield node, first


def parse_python(src):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return ast.parse(src)


def scan_python(src):
    offs = [0]
    for line in src.split("\n")[:-1]:
        offs.append(offs[-1] + len(line) + 1)

    def pos(rc):
        return offs[rc[0] - 1] + rc[1]

    tokens, strings = [], {}
    try:
        for tok in tokenize.generate_tokens(io.StringIO(src).readline):
            if tok.type == tokenize.COMMENT:
                tokens.append({"start": pos(tok.start), "end": pos(tok.end), "kind": "line", "nested": False})
            elif tok.type == tokenize.STRING:
                strings[tok.start] = tok
        tree = parse_python(src)
    except (tokenize.TokenError, SyntaxError, ValueError) as exc:
        raise ScanError("the Python code could not be read (%s)" % exc)
    lines = src.split("\n")
    for _, expr in doc_owners(tree):
        v = expr.value
        start = (v.lineno, char_col(lines[v.lineno - 1], v.col_offset))
        tok = strings.get(start)
        if tok is None:
            continue
        end = (v.end_lineno, char_col(lines[v.end_lineno - 1], v.end_col_offset))
        if tok.end != end:
            continue  # implicit concatenation such as "a" "b": leave it alone
        tokens.append({"start": pos(tok.start), "end": pos(tok.end), "kind": "doc", "nested": False})
    tokens.sort(key=lambda t: t["start"])
    return tokens


def scan(src, lang):
    if lang == "python":
        return scan_python(src)
    if lang in HASH_LANGS.values():
        return HashScanner(src, lang).run()
    return CScanner(src, lang).run()


def strip_comments(src, tokens):
    """Remove every comment. Full-line comments take their whole line."""
    cuts = []
    for t in tokens:
        a, b = t["start"], t["end"]
        if t["kind"] == "line":
            ls = src.rfind("\n", 0, a) + 1
            if not src[ls:a].strip():
                nl = src.find("\n", b)
                a, b = ls, (len(src) if nl == -1 else nl + 1)
        cuts.append((a, b))
    out, last = [], 0
    for a, b in sorted(cuts):
        if a < last:
            a = last
        out.append(src[last:a])
        last = max(last, b)
    out.append(src[last:])
    return "".join(out)


def ast_without_docstrings(src):
    tree = parse_python(src)
    for node, _ in list(doc_owners(tree)):
        node.body = node.body[1:]
    return ast.dump(tree)


# ------------------------------------------------------------ comment model


def eol_at(src, pos):
    j = src.find("\n", pos)
    if j == -1:
        return "\r\n" if "\r\n" in src else "\n"
    return "\r\n" if j > 0 and src[j - 1] == "\r" else "\n"


def lead_ws(text):
    return text[:len(text) - len(text.lstrip(" \t"))]


PROSE_NODES = (ast.Name, ast.Constant, ast.BoolOp, ast.BinOp, ast.UnaryOp, ast.Compare, ast.Tuple,
               ast.expr_context, ast.boolop, ast.operator, ast.unaryop, ast.cmpop)


def is_trivial_expr(node):
    """Words that happen to parse, like "Options and Arguments" or "-s or --long"."""
    return all(isinstance(n, PROSE_NODES) for n in ast.walk(node))


def python_code(text):
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    for cand in [textwrap.dedent(text)] + lines:
        variants = [cand]
        if cand.rstrip().endswith(":"):
            variants.append(cand.rstrip() + "\n    pass")
        for v in variants:
            try:
                tree = parse_python(v)
            except (SyntaxError, ValueError):
                continue
            for st in tree.body:
                if isinstance(st, ast.Expr) and is_trivial_expr(st.value):
                    continue
                if isinstance(st, ast.AnnAssign) and st.value is None:
                    continue
                return True
    return False


def code_line(line, lang):
    t = line.strip()
    if not t:
        return False
    if t in ("{", "}", "};", "})", "});", ")", "]", "end"):
        return True
    if t[-1] in ";{})" and re.search(r"[=;{}]|\w\(|->|::|\w\.\w|\w\[", t):
        return True
    if lang == "shell" and re.match(r"[A-Za-z_]\w*=\S", t):
        return True
    if lang == "yaml" and re.match(r"-?\s*[\w.-]+:(?:\s+\S+)?$", t):
        return True
    if lang == "toml" and (re.match(r"[\w.-]+\s*=\s*\S", t) or re.match(r"\[\[?[\w.-]+\]\]?$", t)):
        return True
    return False


def looks_like_code(text, lang, doc):
    if lang == "python":
        return python_code(text)
    lines = [l for l in text.split("\n") if l.strip()]
    hits = sum(1 for l in lines if code_line(l, lang))
    if doc:
        return hits * 2 > len(lines)
    return hits > 0


def directive(text):
    return bool(DIRECTIVE_I.search(text) or DIRECTIVE_CS.search(text))


class Comment:
    """One entry in the extract output, and how to write it back."""

    def __init__(self, kind, start, end, text, line):
        self.kind, self.start, self.end, self.text, self.line = kind, start, end, text, line
        self.skip = None
        self.trailing = False
        self.style = {}


def build_comments(src, lang, tokens):
    newlines = [m.start() for m in re.finditer("\n", src)]

    def lineno(pos):
        return bisect.bisect_left(newlines, pos) + 1

    def full_line(pos):
        ls = src.rfind("\n", 0, pos) + 1
        return not src[ls:pos].strip(), src[ls:pos]

    hash_marker = re.compile(r"#+'?" if lang in HASH_LANGS.values() else r"#+")
    comments, group = [], []

    def flush():
        if group:
            comments.append(line_comment(src, lang, list(group), lineno))
            del group[:]

    for t in tokens:
        if t["kind"] != "line":
            flush()
            if t["kind"] == "block":
                comments.append(block_comment(src, lang, t, lineno, full_line))
            else:
                comments.append(docstring(src, t, lineno))
            continue
        raw = src[t["start"]:t["end"]]
        full, before = full_line(t["start"])
        if raw.startswith("//"):
            marker = re.match(r"//[/!]?", raw).group()
        else:
            marker = hash_marker.match(raw).group()
        info = {"tok": t, "raw": raw, "full": full, "indent": before if full else "",
                "marker": marker, "rest": raw[len(marker):], "line": lineno(t["start"])}
        info["solo"] = solo_reason(info, lang)
        if group:
            last = group[-1]
            if (full and not info["solo"] and info["line"] == last["line"] + 1
                    and info["indent"] == last["indent"] and info["marker"] == last["marker"]):
                group.append(info)
                continue
            flush()
        if full and not info["solo"]:
            group.append(info)
        else:
            comments.append(line_comment(src, lang, [info], lineno))
    flush()
    comments = [c for c in comments if LETTER.search(c.text)]
    if lang == "go":
        for c in comments:
            nxt = src[c.end:].lstrip(" \t\r\n")
            if not c.skip and nxt.startswith('import "C"'):
                c.skip = "cgo code that the Go compiler reads"
    return comments


def solo_reason(info, lang):
    raw, text = info["raw"], info["rest"].strip()
    if info["line"] == 1 and raw.startswith("#!"):
        return "shebang line"
    if info["line"] <= 2 and info["marker"].startswith("#") and ENCODING.search(raw):
        return "encoding line"
    if lang == "go" and GO_DIRECTIVE.match(raw):
        return "tool directive"
    if directive(text):
        return "tool directive"
    return None


def common_checks(c, lang, doc=False):
    if c.skip:
        return
    if LICENSE.search(c.text):
        c.skip = "license or copyright notice"
    elif c.kind != "docstring" and directive(c.text):
        c.skip = "tool directive"
    elif c.kind != "docstring" and looks_like_code(c.text, lang, doc):
        c.skip = "looks like commented-out code"


def line_comment(src, lang, infos, lineno):
    first = infos[0]
    space = lead_ws(first["rest"])
    lines = []
    for info in infos:
        rest = info["rest"]
        if rest.startswith(space):
            rest = rest[len(space):]
        else:
            rest = rest.lstrip(" \t")
        lines.append(rest.rstrip())
    c = Comment("line", first["tok"]["start"], infos[-1]["tok"]["end"], "\n".join(lines), first["line"])
    c.trailing = not first["full"]
    c.style = {"indent": first["indent"], "marker": first["marker"], "space": space,
               "eol": eol_at(src, first["tok"]["end"])}
    c.skip = first["solo"]
    if not c.skip and any(t["tok"]["nested"] for t in infos):
        c.skip = "inside a string"
    if not c.skip and lang == "php" and any("?>" in t["raw"] for t in infos):
        c.skip = "contains ?>, which ends the PHP code"
    if not c.skip and any(t["raw"].rstrip().endswith("\\") for t in infos):
        c.skip = "ends with a backslash, which joins it to the next line"
    common_checks(c, lang)
    return c


def strip_blank_edges(lines):
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def block_comment(src, lang, t, lineno, full_line):
    raw = src[t["start"]:t["end"]]
    opener = re.match(r"/\*[*!]?", raw).group()
    unterminated = t.get("unterminated")
    if not unterminated and len(raw) < len(opener) + 2:
        opener = "/*"
    inner = raw[len(opener):] if unterminated else raw[len(opener):-2]
    eol = "\r\n" if "\r\n" in inner else eol_at(src, t["end"])
    lines = [l[:-1] if l.endswith("\r") else l for l in inner.split("\n")]
    full, before = full_line(t["start"])
    indent = before if full else ""
    style = {"opener": opener, "eol": eol, "indent": indent}
    if len(lines) == 1:
        body = lines[0]
        style.update(single=True, lead=lead_ws(body), trail=body[len(body.rstrip()):],
                     cont=indent + (" * " if opener == "/**" else "   "))
        text = body.strip()
    else:
        first, last = lines[0], lines[-1]
        head_blank = not first.strip()
        tail_line = not last.strip()
        middle = lines[1:-1] if tail_line else lines[1:]
        content = [l for l in middle if l.strip()]
        starred = bool(content) and all(re.match(r"[ \t]*\*", l) for l in content)
        if not content:
            starred = opener == "/**"
        if starred:
            prefix = None
            for l in content:
                m = re.match(r"([ \t]*\*)([ \t]?)(.*)", l)
                if m.group(3).strip():
                    prefix = m.group(1) + (m.group(2) or "")
                    break
            if prefix is None:
                prefix = indent + " * "
            mark = re.match(r"[ \t]*\*", prefix).group()
            after = prefix[len(mark):]
            text_lines = []
            for l in middle:
                m = re.match(r"[ \t]*\*", l)
                rest = l[m.end():] if m else l.strip()
                rest = rest[len(after):] if rest.startswith(after) else rest.lstrip(" \t")
                text_lines.append(rest.rstrip())
        else:
            ws = [lead_ws(l) for l in content]
            prefix = os.path.commonprefix(ws) if ws else indent + "   "
            text_lines = [(l[len(prefix):] if l.startswith(prefix) else l.lstrip()).rstrip() for l in middle]
        if not head_blank:
            text_lines.insert(0, first.strip())
        text = "\n".join(strip_blank_edges(text_lines))
        style.update(single=False, head_blank=head_blank, first_raw=first, tail_line=tail_line,
                     last_raw=last, trail=last[len(last.rstrip()):], lead=lead_ws(first), prefix=prefix)
    c = Comment("block", t["start"], t["end"], text, lineno(t["start"]))
    c.trailing = not full or src[t["end"]:line_end(src, t["end"])].strip() != ""
    c.style = style
    if unterminated:
        c.skip = "the comment is never closed"
    elif t["nested"]:
        c.skip = "inside a string"
    common_checks(c, lang, doc=opener == "/**")
    return c


def docstring(src, t, lineno):
    raw = src[t["start"]:t["end"]]
    m = re.match(r"([rRuU]*)('''|\"\"\"|'|\")", raw)
    prefix, quote = m.group(1), m.group(2)
    content = raw[m.end():len(raw) - len(quote)]
    eol = "\r\n" if "\r\n" in content else eol_at(src, t["end"])
    lead = content[:len(content) - len(content.lstrip())]
    rest = content[len(lead):]
    trail = rest[len(rest.rstrip()):]
    body = rest[:len(rest) - len(trail)]
    lines = [l[:-1] if l.endswith("\r") else l for l in body.split("\n")]
    ls = src.rfind("\n", 0, t["start"]) + 1
    indent = lead_ws(src[ls:t["start"]])
    ws = [lead_ws(l) for l in lines[1:] if l.strip()]
    if ws:
        indent = os.path.commonprefix(ws)
    text_lines = [lines[0]] + [(l[len(indent):] if l.startswith(indent) else l.lstrip()).rstrip()
                               for l in lines[1:]]
    c = Comment("docstring", t["start"], t["end"], "\n".join(text_lines).strip(), lineno(t["start"]))
    c.style = {"prefix": prefix, "quote": quote, "lead": lead, "trail": trail, "indent": indent, "eol": eol}
    common_checks(c, "python")
    return c


def render(c, new):
    st = c.style
    lines = new.split("\n")
    if c.kind == "line":
        out = []
        for k, l in enumerate(lines):
            piece = (st["marker"] + st["space"] + l) if l else st["marker"]
            out.append(piece if k == 0 else st["eol"] + st["indent"] + piece)
        return "".join(out)
    if c.kind == "docstring":
        body = st["eol"].join([lines[0]] + [(st["indent"] + l) if l else "" for l in lines[1:]])
        return st["prefix"] + st["quote"] + st["lead"] + body + st["trail"] + st["quote"]
    eol = st["eol"]
    if st["single"]:
        out = st["opener"] + st["lead"] + lines[0]
        out += "".join(eol + (st["cont"] + l if l else st["cont"].rstrip()) for l in lines[1:])
        return out + st["trail"] + "*/"

    def pre(l):
        return st["prefix"] + l if l else st["prefix"].rstrip()

    if st["head_blank"]:
        out = st["opener"] + st["first_raw"] + eol + eol.join(pre(l) for l in lines)
    else:
        out = st["opener"] + st["lead"] + lines[0] + "".join(eol + pre(l) for l in lines[1:])
    if st["tail_line"]:
        return out + eol + st["last_raw"] + "*/"
    return out + st["trail"] + "*/"


def kept_lines(text):
    return Counter(l.strip() for l in text.split("\n") if TAG_LINE.match(l.strip()))


def problem(c, new, lang):
    """Return why this change can't be made, or None."""
    if c.skip:
        return "%s, so it is left alone" % c.skip
    if not new.strip():
        return "the new text is empty. Delete comments by hand if that is what you want"
    if c.trailing and "\n" in new:
        return "this comment shares its line with code, so the new text must be one line"
    if c.kind == "block":
        if "*/" in new:
            return "the new text contains */, which would end the comment early"
        if lang in NESTING and "/*" in new:
            return "the new text contains /*, which would start a comment inside the comment"
    if c.kind == "line":
        if any(l.rstrip().endswith("\\") for l in new.split("\n")):
            return "a line ends with a backslash, which would join it to the next line"
        if lang == "php" and "?>" in new:
            return "the new text contains ?>, which would end the PHP code"
    if c.kind == "docstring":
        q = c.style["quote"]
        if q in new:
            return "the new text contains %s, the quotes around this docstring" % q
        if len(q) == 1 and "\n" in new:
            return "this docstring uses single quotes, so the new text must be one line"
        if not c.style["trail"] and (new.endswith(q[0]) or new.endswith("\\")):
            return "the new text ends with a quote or backslash right before the closing quotes"
    old_tags, new_tags = kept_lines(c.text), kept_lines(new)
    if old_tags - new_tags:
        return ("a tag or section line (like @param, :returns: or Args:) was changed or removed. "
                "Keep those lines exactly as they were")
    if Counter(INLINE_TAG.findall(c.text)) - Counter(INLINE_TAG.findall(new)):
        return "an inline tag such as {@link ...} or <param ...> was changed or removed"
    return None


def snippet_ok(c, rendered, lang):
    """Scan the rendered comment on its own to make sure it is still one comment."""
    if c.kind == "docstring":
        try:
            toks = [t for t in tokenize.generate_tokens(io.StringIO(rendered).readline)
                    if t.type not in (tokenize.NEWLINE, tokenize.NL, tokenize.ENDMARKER)]
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                value = ast.literal_eval(rendered)
        except (tokenize.TokenError, SyntaxError, ValueError):
            return False
        return len(toks) == 1 and toks[0].type == tokenize.STRING and isinstance(value, str)
    toks = scan(rendered, lang)
    if c.kind == "block":
        return len(toks) == 1 and toks[0]["start"] == 0 and toks[0]["end"] == len(rendered) \
            and not toks[0].get("unterminated")
    return (len(toks) == rendered.count("\n") + 1 and all(t["kind"] == "line" for t in toks)
            and toks[0]["start"] == 0)


# ----------------------------------------------------------------- commands


def read_source(path):
    lang = language_for(path)
    if not lang:
        sys.exit("%s is not a supported file type. Supported extensions: %s"
                 % (os.path.basename(path), " ".join(SUPPORTED)))
    try:
        with open(path, encoding="utf-8", newline="") as fh:
            src = fh.read()
    except FileNotFoundError:
        sys.exit("Could not find %s." % path)
    except UnicodeDecodeError:
        sys.exit("%s is not UTF-8 text, so it was not read." % path)
    bom = ""
    if src.startswith("\ufeff"):
        bom, src = "\ufeff", src[1:]
    return lang, bom, src


def analyse(src, lang):
    try:
        tokens = scan(src, lang)
    except ScanError as exc:
        sys.exit("Could not read the file: %s." % exc)
    return tokens, build_comments(src, lang, tokens)


def cmd_extract(args):
    lang, _, src = read_source(args.file)
    _, comments = analyse(src, lang)
    out = []
    for n, c in enumerate(comments, 1):
        item = {"id": "c%d" % n, "line": c.line, "kind": c.kind, "text": c.text}
        if c.skip:
            item["skip"] = c.skip
        out.append(item)
    payload = json.dumps({"file": os.path.basename(args.file), "language": lang, "comments": out},
                         ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(payload)
        print("Wrote %s to %s" % (plural(len(out), "comment"), args.output))
    else:
        print(payload)


def load_changes(path):
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        sys.exit("Could not read the changes file %s: %s" % (path, exc))
    if isinstance(data, dict) and isinstance(data.get("comments"), list):
        data = data["comments"]
    if isinstance(data, list):
        return {str(d["id"]): d.get("text", "") for d in data if isinstance(d, dict) and "id" in d}
    if isinstance(data, dict):
        return {str(k): (v.get("text", "") if isinstance(v, dict) else v) for k, v in data.items()}
    sys.exit("The changes file should map comment ids to new text, like {\"c1\": \"New text.\"}.")


def git_ok(path):
    """Return None if git tracks the file with no uncommitted changes, else the reason."""
    folder = os.path.dirname(os.path.abspath(path)) or "."
    name = os.path.basename(path)

    def git(*cmd):
        try:
            return subprocess.run(["git"] + list(cmd), cwd=folder, capture_output=True).returncode
        except OSError:
            return None

    tracked = git("ls-files", "--error-unmatch", "--", name)
    if tracked is None:
        return "git is not installed"
    if tracked != 0:
        return "the file is not tracked by git"
    if git("diff", "--quiet", "--", name) != 0 or git("diff", "--cached", "--quiet", "--", name) != 0:
        return "the file has uncommitted changes"
    return None


def cmd_apply(args):
    if args.in_place and args.output:
        sys.exit("Use either -o or --in-place, not both.")
    lang, bom, src = read_source(args.file)
    if args.in_place:
        reason = git_ok(args.file)
        if reason:
            sys.exit("Refusing to edit %s in place: %s, so the change could not be reviewed or undone "
                     "with git. Run without --in-place to write a separate copy instead." % (args.file, reason))
        out_path = args.file
    else:
        out_path = args.output or humanized_path(args.file)
        if os.path.abspath(out_path) == os.path.abspath(args.file):
            sys.exit("Refusing to overwrite the original. Choose a different output name.")
    changes = load_changes(args.changes)
    tokens, comments = analyse(src, lang)
    by_id = {"c%d" % n: c for n, c in enumerate(comments, 1)}
    edits, skipped = [], 0
    for cid in changes:
        if cid not in by_id:
            print("SKIPPED %s: no such comment" % cid)
            skipped += 1
    for cid, c in by_id.items():
        if cid not in changes:
            continue
        new = changes[cid]
        if not isinstance(new, str):
            print("SKIPPED %s: the new text is not a string" % cid)
            skipped += 1
            continue
        new = "\n".join(l.rstrip() for l in new.replace("\r\n", "\n").replace("\r", "\n").split("\n")).strip("\n")
        if new == c.text:
            continue
        why = problem(c, new, lang)
        rendered = None
        if not why:
            rendered = render(c, new)
            if not snippet_ok(c, rendered, lang):
                why = "the new text would change where the comment starts or ends"
        if why:
            print("SKIPPED %s: %s." % (cid, why.rstrip(".")))
            skipped += 1
            continue
        edits.append((c.start, c.end, rendered))
    result = src
    for a, b, text in sorted(edits, reverse=True):
        result = result[:a] + text + result[b:]
    if edits:
        try:
            new_tokens = scan(result, lang)
        except ScanError as exc:
            sys.exit("Nothing was written: the new file could not be read back (%s)." % exc)
        if strip_comments(src, tokens) != strip_comments(result, new_tokens):
            sys.exit("Nothing was written: with the comments removed, the new file's code does not match "
                     "the original. This is a safety stop, please report it.")
        if lang == "python":
            try:
                same = ast_without_docstrings(src) == ast_without_docstrings(result)
            except (SyntaxError, ValueError) as exc:
                sys.exit("Nothing was written: the new file is not valid Python (%s)." % exc)
            if not same:
                sys.exit("Nothing was written: the new file's Python code does not match the original. "
                         "This is a safety stop, please report it.")
    with open(out_path, "w", encoding="utf-8", newline="") as fh:
        fh.write(bom + result)
    print("Wrote %s with %d changed %s%s." % (out_path, len(edits), "comment" if len(edits) == 1 else "comments",
                                             (", %d skipped" % skipped) if skipped else ""))
    if skipped:
        # Exit code 2: the file was written, but some changes were left out.
        sys.exit(2)


def main():
    parser = argparse.ArgumentParser(description="Rewrite the comments and docstrings in a source file, "
                                                 "leaving the code alone.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("extract", help="list comments with ids")
    e.add_argument("file")
    e.add_argument("-o", "--output", help="write the JSON here instead of printing it")
    e.set_defaults(func=cmd_extract)
    a = sub.add_parser("apply", help="write a copy of the file with your new comments")
    a.add_argument("file")
    a.add_argument("changes", help="JSON mapping comment id to new text")
    a.add_argument("-o", "--output", help="output path (default: <name>-humanized<ext>)")
    a.add_argument("--in-place", action="store_true",
                   help="overwrite the file, only if git tracks it and it has no uncommitted changes")
    a.set_defaults(func=cmd_apply)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
