"""Checks that the numbers on the website match the repository.

The landing page (docs/index.html) shows counts such as how many writing
guides and test cases there are. Each number is marked with a data-stat
attribute, and this test recomputes it from the repo, so the page can't
quietly go out of date.

Run from the repo root:  python -m unittest discover -s tests -v
"""

import glob
import json
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFS = os.path.join(ROOT, "write-like-human", "references")
SITE = os.path.join(ROOT, "docs", "index.html")
EVALS = os.path.join(ROOT, "tests", "evals", "evals.json")

NOT_A_LANGUAGE = {"translate-humanize.md", "mixed-language.md", "indian-english.md"}


def actual_counts():
    guides = glob.glob(os.path.join(REFS, "**", "*.md"), recursive=True)
    languages = [p for p in glob.glob(os.path.join(REFS, "languages", "*.md"))
                 if os.path.basename(p) not in NOT_A_LANGUAGE]
    with open(EVALS, encoding="utf-8") as f:
        evals = json.load(f)["cases"]
    return {
        "guides": len(guides),
        "writing": len(glob.glob(os.path.join(REFS, "writing", "*.md"))),
        "languages": len(languages),
        "evals": len(evals),
    }


class SiteNumbersTest(unittest.TestCase):
    def test_numbers_match_the_repo(self):
        with open(SITE, encoding="utf-8") as f:
            html = f.read()
        shown = re.findall(r'data-stat="(\w+)">(\d+)<', html)
        self.assertTrue(shown, "no data-stat numbers found on the site")
        expected = actual_counts()
        for name, value in shown:
            with self.subTest(stat=name):
                self.assertIn(name, expected, "unknown data-stat name: %s" % name)
                self.assertEqual(
                    int(value), expected[name],
                    "docs/index.html shows %s for %s, but the repo has %s"
                    % (value, name, expected[name]),
                )


if __name__ == "__main__":
    unittest.main()
