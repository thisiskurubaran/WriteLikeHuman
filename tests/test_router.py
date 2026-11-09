"""Router checks: Claude can reach every guide, and every link goes somewhere.

SKILL.md is the router. Some of its rows point at small index files
(for example references/writing/index.md) that list related guides. These
tests follow both levels and check that:

- every link in the router and its index files points at a real file,
- every guide in references/ can be reached from the router,
- every guide named in the evals and in examples/test-prompts.md exists
  and is routed, so a renamed or unlinked guide can't slip through.

Run from the repo root:  python -m unittest discover -s tests -v
"""

import glob
import json
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_DIR = os.path.join(ROOT, "write-like-human")
REFS = os.path.join(SKILL_DIR, "references")
LINK = re.compile(r"\]\(([^)#\s]+\.md)\)")
CODE = re.compile(r"`([a-z0-9-]+\.md)`")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def router_files():
    """SKILL.md plus every index.md it links to, as absolute paths."""
    files = [os.path.join(SKILL_DIR, "SKILL.md")]
    for target in LINK.findall(read(files[0])):
        if target.endswith("index.md"):
            files.append(os.path.normpath(os.path.join(SKILL_DIR, target)))
    return files


def routed_guides():
    """Every references/ file the router reaches, relative to references/."""
    reached = set()
    for path in router_files():
        base = os.path.dirname(path)
        text = read(path)
        for target in LINK.findall(text):
            full = os.path.normpath(os.path.join(base, target))
            if full.startswith(REFS + os.sep):
                reached.add(os.path.relpath(full, REFS).replace(os.sep, "/"))
        # Language files are listed by name in backticks.
        for name in CODE.findall(text):
            if os.path.exists(os.path.join(REFS, "languages", name)):
                reached.add("languages/" + name)
    return reached


def all_guides():
    return {os.path.relpath(p, REFS).replace(os.sep, "/")
            for p in glob.glob(os.path.join(REFS, "**", "*.md"), recursive=True)}


class RouterLinksTest(unittest.TestCase):
    def test_every_link_points_at_a_real_file(self):
        for path in router_files():
            base = os.path.dirname(path)
            for target in LINK.findall(read(path)):
                with self.subTest(router=os.path.relpath(path, ROOT), link=target):
                    self.assertTrue(os.path.isfile(os.path.normpath(os.path.join(base, target))),
                                    "%s links to a missing file: %s" % (os.path.relpath(path, ROOT), target))

    def test_every_guide_is_reachable(self):
        missing = sorted(g for g in all_guides() - routed_guides() if not g.endswith("index.md"))
        self.assertEqual(missing, [], "not reachable from SKILL.md or its index files: %s" % missing)


class RoutedExamplesTest(unittest.TestCase):
    def test_eval_modules_are_routed(self):
        cases = json.loads(read(os.path.join(ROOT, "tests", "evals", "evals.json")))["cases"]
        reached = routed_guides()
        for case in cases:
            for module in case["should_load"]:
                with self.subTest(case=case["id"], module=module):
                    self.assertIn(module, reached)

    def test_test_prompt_modules_exist(self):
        """Short names in the 'Should load' column must match a real guide."""
        names = {os.path.basename(g)[:-3] for g in all_guides()}
        text = read(os.path.join(SKILL_DIR, "examples", "test-prompts.md"))
        unknown = set()
        in_load_table = False
        for line in text.splitlines():
            if not line.startswith("|"):
                in_load_table = False
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            if "Should load" in line:
                in_load_table = True
                continue
            if not in_load_table or set(line) <= set("|- ") or len(cells) < 2:
                continue
            for word in re.findall(r"[a-z][a-z-]+", cells[1].split("(")[0]):
                if word in ("or", "and", "the", "builds", "claude"):
                    continue
                if word not in names and not any(n.startswith(word) for n in names):
                    unknown.add(word)
        self.assertEqual(sorted(unknown), [], "test-prompts.md names guides that don't exist: %s" % sorted(unknown))


if __name__ == "__main__":
    unittest.main()
