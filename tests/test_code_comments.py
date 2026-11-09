"""Tests for write-like-human/scripts/code_comments.py.

Every sample file is made up and built in a temporary folder while the
tests run.

Run from the repository root:

    python -m unittest discover -s tests -v
"""

import ast
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "write-like-human", "scripts")
SCRIPT = "code_comments.py"


def run(script, *args, expect=0, cwd=None):
    proc = subprocess.run(
        [sys.executable, os.path.join(SCRIPTS, script)] + [str(a) for a in args],
        capture_output=True, text=True, encoding="utf-8", cwd=cwd,
    )
    if expect is not None and proc.returncode != expect:
        raise AssertionError("%s %s exited %d\nstdout: %s\nstderr: %s"
                             % (script, args, proc.returncode, proc.stdout, proc.stderr))
    return proc


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False)
    return path


class TempDirCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = self._tmp.name

    def tearDown(self):
        self._tmp.cleanup()

    def path(self, name):
        return os.path.join(self.dir, name)

    def write(self, name, text, newline="\n", bom=False):
        path = self.path(name)
        with open(path, "w", encoding="utf-8-sig" if bom else "utf-8", newline=newline) as fh:
            fh.write(text)
        return path

    def read(self, path):
        with open(path, encoding="utf-8", newline="") as fh:
            return fh.read()

    def extract(self, path):
        return json.loads(run(SCRIPT, "extract", path).stdout)

    def by_text(self, data, fragment):
        for c in data["comments"]:
            if fragment in c["text"]:
                return c
        raise AssertionError("no comment containing %r in %r" % (fragment, data["comments"]))


PY_SAMPLE = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tools for the Brindle shop ledger.

This module basically just adds up the totals.
"""
import os  # noqa: F401

# This function is used in order to
# add the two numbers together.
def add(a, b):
    """Add two numbers.

    Args:
        a: the first number
        b: the second number

    Returns:
        The sum of both.
    """
    # total = a + b
    note = "# this is a string, not a comment"
    return a + b  # gives back the total amount


class Ledger:
    """Keeps track of the shop entries."""

    def size(self):
        return 0
'''


def strip_py_comments(src):
    """Code with comments and docstrings removed, for comparing in tests."""
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and node.body:
            first = node.body[0]
            if isinstance(first, ast.Expr) and isinstance(getattr(first, "value", None), ast.Constant) \
                    and isinstance(first.value.value, str):
                node.body = node.body[1:]
    return ast.dump(tree)


class PythonTest(TempDirCase):
    def test_extract_lists_comments_and_docstrings(self):
        path = self.write("ledger.py", PY_SAMPLE)
        data = self.extract(path)
        self.assertEqual(data["language"], "python")
        kinds = [c["kind"] for c in data["comments"]]
        self.assertEqual(kinds.count("docstring"), 3)
        merged = self.by_text(data, "in order to")
        self.assertEqual(merged["text"], "This function is used in order to\nadd the two numbers together.")
        self.assertEqual(merged["kind"], "line")
        self.assertEqual(self.by_text(data, "/usr/bin/env")["skip"], "shebang line")
        self.assertEqual(self.by_text(data, "coding")["skip"], "encoding line")
        self.assertEqual(self.by_text(data, "noqa")["skip"], "tool directive")
        self.assertIn("commented-out code", self.by_text(data, "total = a + b")["skip"])
        self.assertNotIn("skip", self.by_text(data, "gives back the total"))
        self.assertFalse(any("this is a string" in c["text"] for c in data["comments"]))
        mod = self.by_text(data, "Brindle")
        self.assertEqual(mod["text"], "Tools for the Brindle shop ledger.\n\nThis module basically just adds up the totals.")

    def test_apply_rewrites_and_keeps_code(self):
        path = self.write("ledger.py", PY_SAMPLE)
        data = self.extract(path)
        ids = {c["text"].split("\n")[0]: c["id"] for c in data["comments"]}
        changes = {
            ids["Tools for the Brindle shop ledger."]: "Totals for the Brindle shop ledger.\n\nIt adds up the money.",
            ids["This function is used in order to"]: "Add two numbers.\nKept short on purpose.\nThird line.",
            ids["Add two numbers."]: ("Add a and b.\n\nArgs:\n    a: the first number\n    b: the second number"
                                      "\n\nReturns:\n    The sum of both."),
            ids["gives back the total amount"]: "the total",
            ids["Keeps track of the shop entries."]: "Holds the shop entries.",
        }
        proc = run(SCRIPT, "apply", path, write_json(self.path("c.json"), changes))
        self.assertIn("5 changed comments", proc.stdout)
        out = self.read(self.path("ledger-humanized.py"))
        self.assertIn('"""Totals for the Brindle shop ledger.\n\nIt adds up the money.\n"""', out)
        self.assertIn("# Add two numbers.\n# Kept short on purpose.\n# Third line.\ndef add", out)
        self.assertIn('    """Add a and b.\n\n    Args:\n        a: the first number\n', out)
        self.assertIn("    return a + b  # the total\n", out)
        self.assertIn('    """Holds the shop entries."""\n', out)
        self.assertEqual(strip_py_comments(PY_SAMPLE), strip_py_comments(out))
        # The original is untouched.
        self.assertEqual(self.read(path), PY_SAMPLE)

    def test_docstring_quotes_and_tags(self):
        path = self.write("ledger.py", PY_SAMPLE)
        data = self.extract(path)
        doc = self.by_text(data, "Add two numbers.")
        cls = self.by_text(data, "Keeps track")
        changes = {doc["id"]: "Add them.\n\nReturns:\n    The sum.", cls["id"]: 'Says """hi"""'}
        proc = run(SCRIPT, "apply", path, write_json(self.path("c.json"), changes), expect=2)
        self.assertIn("SKIPPED %s: a tag or section line" % doc["id"], proc.stdout)
        self.assertIn("SKIPPED %s: the new text contains \"\"\"" % cls["id"], proc.stdout)
        self.assertEqual(self.read(self.path("ledger-humanized.py")), PY_SAMPLE)

    def test_skipped_comment_refused(self):
        path = self.write("ledger.py", PY_SAMPLE)
        data = self.extract(path)
        noqa = self.by_text(data, "noqa")
        proc = run(SCRIPT, "apply", path, write_json(self.path("c.json"), {noqa["id"]: "fine"}), expect=2)
        self.assertIn("SKIPPED %s: tool directive" % noqa["id"], proc.stdout)

    def test_type_ignore_and_license(self):
        src = ("# Copyright 2024 Fenwick Labs\n# SPDX-License-Identifier: MIT\n\n"
               "x = int('3')  # type: ignore\n# pylint: disable=invalid-name\ny = 2\n")
        data = self.extract(self.write("m.py", src))
        self.assertEqual(self.by_text(data, "Copyright")["skip"], "license or copyright notice")
        self.assertEqual(self.by_text(data, "type: ignore")["skip"], "tool directive")
        self.assertEqual(self.by_text(data, "pylint")["skip"], "tool directive")


JS_SAMPLE = r'''// @ts-nocheck
/* eslint-disable no-console */
const site = "https://example.com/a//b"; // the main address
const quote = 'it is // not a comment';
const tpl = `value ${ pick("/* x */") } // still text ${`inner // ${1}`}`;
const slashes = /\/\/+/g; // squash repeated slashes
/**
 * Fetch the member record from the server.
 * Returns null when it is missing.
 *
 * @param {string} id the member id
 * @returns {Promise<Member>}
 */
function load(id) {
  // console.log(id);
  return fetch(site + id); /* short note */
}
'''


class JavaScriptTest(TempDirCase):
    def test_strings_are_not_comments(self):
        data = self.extract(self.write("app.js", JS_SAMPLE))
        self.assertEqual(data["language"], "javascript")
        texts = [c["text"] for c in data["comments"]]
        self.assertFalse(any("example.com" in t or "not a comment" in t or "still text" in t
                             or "inner" in t or "x" == t.strip() for t in texts), texts)
        self.assertIn("the main address", texts)
        self.assertIn("squash repeated slashes", texts)
        self.assertEqual(self.by_text(data, "@ts-nocheck")["skip"], "tool directive")
        self.assertEqual(self.by_text(data, "eslint-disable")["skip"], "tool directive")
        self.assertIn("commented-out code", self.by_text(data, "console.log")["skip"])
        doc = self.by_text(data, "Fetch the member")
        self.assertEqual(doc["kind"], "block")
        self.assertEqual(doc["text"], "Fetch the member record from the server.\nReturns null when it is missing."
                                      "\n\n@param {string} id the member id\n@returns {Promise<Member>}")

    def test_block_rerendered_with_stars(self):
        path = self.write("app.js", JS_SAMPLE)
        data = self.extract(path)
        doc = self.by_text(data, "Fetch the member")
        note = self.by_text(data, "short note")
        addr = self.by_text(data, "main address")
        changes = {
            doc["id"]: ("Get the member record from the server.\nGives back null if there is none.\n"
                        "\n@param {string} id the member id\n@returns {Promise<Member>}"),
            note["id"]: "a quick note",
            addr["id"]: "home page",
        }
        run(SCRIPT, "apply", path, write_json(self.path("c.json"), changes))
        out = self.read(self.path("app-humanized.js"))
        expected = JS_SAMPLE.replace(
            " * Fetch the member record from the server.\n * Returns null when it is missing.\n",
            " * Get the member record from the server.\n * Gives back null if there is none.\n",
        ).replace("/* short note */", "/* a quick note */").replace("// the main address", "// home page")
        self.assertEqual(out, expected)

    def test_tag_change_skipped(self):
        path = self.write("app.js", JS_SAMPLE)
        doc = self.by_text(self.extract(path), "Fetch the member")
        changes = {doc["id"]: "Get the record.\n@param {string} id which member\n@returns {Promise<Member>}"}
        proc = run(SCRIPT, "apply", path, write_json(self.path("c.json"), changes), expect=2)
        self.assertIn("SKIPPED %s: a tag or section line" % doc["id"], proc.stdout)
        self.assertEqual(self.read(self.path("app-humanized.js")), JS_SAMPLE)

    def test_block_end_marker_skipped(self):
        path = self.write("app.js", JS_SAMPLE)
        note = self.by_text(self.extract(path), "short note")
        proc = run(SCRIPT, "apply", path, write_json(self.path("c.json"), {note["id"]: "stop */ here"}), expect=2)
        self.assertIn("*/", proc.stdout)

    def test_trailing_comment_newline_skipped(self):
        path = self.write("app.js", JS_SAMPLE)
        addr = self.by_text(self.extract(path), "main address")
        proc = run(SCRIPT, "apply", path, write_json(self.path("c.json"), {addr["id"]: "two\nlines"}), expect=2)
        self.assertIn("SKIPPED %s: this comment shares its line with code" % addr["id"], proc.stdout)
        self.assertTrue(os.path.exists(self.path("app-humanized.js")))

    def test_merged_line_comments(self):
        src = "function f() {\n    // First we check the list\n    // and then we sort it.\n    return 1;\n}\n"
        path = self.write("sort.ts", src)
        data = self.extract(path)
        self.assertEqual(len(data["comments"]), 1)
        c = data["comments"][0]
        self.assertEqual(c["text"], "First we check the list\nand then we sort it.")
        run(SCRIPT, "apply", path, write_json(self.path("c.json"), {c["id"]: "Check the list, then sort it."}))
        self.assertEqual(self.read(self.path("sort-humanized.ts")),
                         "function f() {\n    // Check the list, then sort it.\n    return 1;\n}\n")


class RoundTripTest(TempDirCase):
    def test_crlf_and_bom_unchanged(self):
        src = "// Sets up the Larkspur widget.\r\nint main() {\r\n\treturn 0; /* done */   \r\n}\r\n"
        path = self.write("main.c", src, newline="", bom=True)
        run(SCRIPT, "apply", path, write_json(self.path("c.json"), {}))
        with open(path, "rb") as a, open(self.path("main-humanized.c"), "rb") as b:
            self.assertEqual(a.read(), b.read())

    def test_extract_output_as_changes_is_identical(self):
        path = self.write("ledger.py", PY_SAMPLE.replace("\n", "\r\n"), newline="", bom=True)
        run(SCRIPT, "extract", path, "-o", self.path("c.json"))
        run(SCRIPT, "apply", path, self.path("c.json"))
        with open(path, "rb") as a, open(self.path("ledger-humanized.py"), "rb") as b:
            self.assertEqual(a.read(), b.read())

    def test_crlf_change_keeps_crlf(self):
        src = "// Sets up the\r\n// Larkspur widget.\r\nint main() {\r\n  return 0;\r\n}\r\n"
        path = self.write("main.c", src, newline="", bom=True)
        data = self.extract(path)
        run(SCRIPT, "apply", path, write_json(self.path("c.json"), {data["comments"][0]["id"]: "Starts\nthe widget."}))
        with open(self.path("main-humanized.c"), "rb") as fh:
            out = fh.read()
        self.assertEqual(out, b"\xef\xbb\xbf// Starts\r\n// the widget.\r\nint main() {\r\n  return 0;\r\n}\r\n")


class OutputTest(TempDirCase):
    def test_refuses_same_output(self):
        path = self.write("ledger.py", PY_SAMPLE)
        proc = run(SCRIPT, "apply", path, write_json(self.path("c.json"), {}), "-o", path, expect=1)
        self.assertIn("Refusing to overwrite the original", proc.stderr)

    def test_unsupported_extension(self):
        path = self.write("notes.txt", "# hello\n")
        proc = run(SCRIPT, "extract", path, expect=1)
        self.assertIn("not a supported file type", proc.stderr)
        self.assertIn(".py", proc.stderr)
        self.assertIn(".rs", proc.stderr)

    def test_extract_to_file_message(self):
        path = self.write("one.go", "package main\n\n// Says hello to Orla.\nfunc main() {}\n")
        proc = run(SCRIPT, "extract", path, "-o", self.path("out.json"))
        self.assertIn("Wrote 1 comment to", proc.stdout)

    def test_in_place_refused_outside_git(self):
        path = self.write("ledger.py", PY_SAMPLE)
        proc = run(SCRIPT, "apply", path, write_json(self.path("c.json"), {}), "--in-place", expect=1)
        self.assertIn("Run without --in-place", proc.stderr)
        self.assertEqual(self.read(path), PY_SAMPLE)

    @unittest.skipUnless(shutil.which("git"), "git is not installed")
    def test_in_place_in_git_repo(self):
        repo = self.path("repo")
        os.mkdir(repo)
        path = os.path.join(repo, "ledger.py")
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(PY_SAMPLE)

        def git(*args):
            subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@example.com"] + list(args),
                           cwd=repo, check=True, capture_output=True)

        git("init", "-q")
        git("add", "ledger.py")
        git("commit", "-q", "-m", "start")
        data = self.extract(path)
        cls = self.by_text(data, "Keeps track")
        changes = write_json(self.path("c.json"), {cls["id"]: "Holds the shop entries."})
        run(SCRIPT, "apply", path, changes, "--in-place")
        self.assertIn('"""Holds the shop entries."""', self.read(path))
        # Now the file has uncommitted changes, so a second run is refused.
        proc = run(SCRIPT, "apply", path, changes, "--in-place", expect=1)
        self.assertIn("uncommitted changes", proc.stderr)


class OtherLanguagesTest(TempDirCase):
    def test_go_basics(self):
        src = ('//go:build linux\n\npackage main\n\nimport "fmt"\n\n'
               '// main prints a greeting\n// for the Tamsin team.\nfunc main() {\n'
               '\tfmt.Println("see http://example.com // here") // print it\n'
               '\tpath := `C:\\raw // text`\n\t_ = path\n}\n')
        path = self.write("main.go", src)
        data = self.extract(path)
        self.assertEqual(data["language"], "go")
        self.assertEqual(self.by_text(data, "go:build")["skip"], "tool directive")
        texts = [c["text"] for c in data["comments"]]
        self.assertFalse(any("example.com" in t or "raw" in t for t in texts), texts)
        greet = self.by_text(data, "greeting")
        self.assertEqual(greet["text"], "main prints a greeting\nfor the Tamsin team.")
        run(SCRIPT, "apply", path, write_json(self.path("c.json"), {greet["id"]: "main greets the Tamsin team."}))
        out = self.read(self.path("main-humanized.go"))
        self.assertEqual(out, src.replace("// main prints a greeting\n// for the Tamsin team.",
                                          "// main greets the Tamsin team."))

    def test_shell_basics(self):
        src = ("#!/bin/bash\n# shellcheck disable=SC2086\n\n# Copy the files over\n# to the backup folder.\n"
               "echo \"a # b\" 'c # d' ${#items[@]} # count them\n"
               "cat <<EOF\n# not a comment inside the heredoc\nEOF\n"
               "# cp -r src dst;\n")
        path = self.write("backup.sh", src)
        data = self.extract(path)
        self.assertEqual(data["language"], "shell")
        self.assertEqual(self.by_text(data, "/bin/bash")["skip"], "shebang line")
        self.assertEqual(self.by_text(data, "shellcheck")["skip"], "tool directive")
        self.assertIn("commented-out code", self.by_text(data, "cp -r")["skip"])
        texts = [c["text"] for c in data["comments"]]
        self.assertFalse(any(t in ("b\" 'c", "d' ${#items[@]}") or "heredoc" in t or t.startswith("b") for t in texts),
                         texts)
        self.assertIn("count them", texts)
        copy = self.by_text(data, "Copy the files")
        run(SCRIPT, "apply", path, write_json(self.path("c.json"), {copy["id"]: "Back up the files."}))
        out = self.read(self.path("backup-humanized.sh"))
        self.assertEqual(out, src.replace("# Copy the files over\n# to the backup folder.", "# Back up the files."))

    def test_yaml_block_scalar(self):
        src = ("title: Don't stop # plain note\nquote: 'it''s # no'\n"
               "steps:\n  - run: |\n      echo hi # not a comment\n  # Build the site\n  - run: make\n")
        data = self.extract(self.write("ci.yml", src))
        texts = [c["text"] for c in data["comments"]]
        self.assertEqual(texts, ["plain note", "Build the site"])

    def test_rust_raw_string_and_nesting(self):
        src = ('fn main() {\n    let s = r#"a // b "quoted" /* c */"#;\n'
               "    let c = '\"'; // a quote char\n    /* outer /* inner */ still outer */\n"
               "    let _x: &'static str = \"y\"; // static text\n}\n")
        data = self.extract(self.write("main.rs", src))
        texts = [c["text"] for c in data["comments"]]
        self.assertEqual(texts, ["a quote char", "outer /* inner */ still outer", "static text"])


if __name__ == "__main__":
    unittest.main()
