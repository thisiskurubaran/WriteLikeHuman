"""Checks that the numbers on the website match the repository.

The landing pages (docs/index.html and the Hindi and Tamil versions in
docs/hi/ and docs/ta/) show counts such as how many writing
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
SITES = [os.path.join(ROOT, "docs", *p.split("/")) for p in ("index.html", "hi/index.html", "ta/index.html")]
EVALS = os.path.join(ROOT, "tests", "evals", "evals.json")

NOT_A_LANGUAGE = {"translate-humanize.md", "mixed-language.md", "indian-english.md", "script-conversion.md"}


def actual_counts():
    guides = [p for p in glob.glob(os.path.join(REFS, "**", "*.md"), recursive=True)
              if os.path.basename(p) != "index.md"]
    languages = [p for p in glob.glob(os.path.join(REFS, "languages", "*.md"))
                 if os.path.basename(p) not in NOT_A_LANGUAGE]
    with open(EVALS, encoding="utf-8") as f:
        evals = json.load(f)["cases"]
    return {
        "guides": len(guides),
        "writing": len([p for p in glob.glob(os.path.join(REFS, "writing", "*.md"))
                        if os.path.basename(p) != "index.md"]),
        "languages": len(languages),
        "evals": len(evals),
    }


class SiteNumbersTest(unittest.TestCase):
    def test_numbers_match_the_repo(self):
        expected = actual_counts()
        for site in SITES:
            rel = os.path.relpath(site, ROOT)
            with open(site, encoding="utf-8") as f:
                html = f.read()
            shown = re.findall(r'data-stat="(\w+)">(\d+)<', html)
            self.assertTrue(shown, "no data-stat numbers found in %s" % rel)
            for name, value in shown:
                with self.subTest(page=rel, stat=name):
                    self.assertIn(name, expected, "unknown data-stat name: %s" % name)
                    self.assertEqual(
                        int(value), expected[name],
                        "%s shows %s for %s, but the repo has %s"
                        % (rel, value, name, expected[name]),
                    )

    def test_translations_show_the_same_numbers(self):
        def stats(path):
            with open(path, encoding="utf-8") as f:
                return sorted(re.findall(r'data-stat="(\w+)">(\d+)<', f.read()))
        english = stats(SITES[0])
        for site in SITES[1:]:
            with self.subTest(page=os.path.relpath(site, ROOT)):
                self.assertEqual(stats(site), english)


if __name__ == "__main__":
    unittest.main()
