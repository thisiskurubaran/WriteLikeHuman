"""Size budgets, so the skill stays quick as it grows.

Claude reads SKILL.md and the pattern catalog on every request, and one or
two guides after that. Every extra word costs time and tokens for every
user, so each file has a budget. If a test here fails, trim the file or
split it, rather than raising the limit.

Run from the repo root:  python -m unittest discover -s tests -v
"""

import glob
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_DIR = os.path.join(ROOT, "write-like-human")
REFS = os.path.join(SKILL_DIR, "references")

SKILL_MAX_LINES = 200
SKILL_MAX_WORDS = 2600
DESCRIPTION_MAX_CHARS = 1024
CATALOG_MAX_WORDS = 3500      # references/ai-patterns.md, read on every request
GUIDE_MAX_WORDS = 1500        # every other guide, read only when it applies
ALWAYS_MAX_WORDS = 6000       # SKILL.md + ai-patterns.md, read on every request
REQUEST_MAX_WORDS = 11000     # everything read for one common request

# Files read for some common requests, as the router sends them.
COMMON_REQUESTS = {
    "email rewrite": ["modes/rewrite.md", "writing/index.md", "writing/email.md"],
    "resume in Word": ["modes/rewrite.md", "files/word.md", "writing/index.md",
                       "writing/resume.md", "lists/buzzwords.md"],
    "PDF report": ["modes/rewrite.md", "files/pdf.md", "writing/index.md", "writing/report.md"],
    "README in a repo": ["modes/rewrite.md", "developer/readme.md", "lists/buzzwords.md",
                         "developer/repo-files.md"],
    "Hindi translation": ["modes/rewrite.md", "languages/translate-humanize.md", "languages/hindi.md"],
    "voice profile from WhatsApp": ["modes/rewrite.md", "voice/voice-profile.md", "voice/chat-export.md"],
}


def words(path):
    with open(path, encoding="utf-8") as f:
        return len(f.read().split())


class SizeBudgetTest(unittest.TestCase):
    def test_skill_file(self):
        path = os.path.join(SKILL_DIR, "SKILL.md")
        with open(path, encoding="utf-8") as f:
            text = f.read()
        lines = text.count("\n") + 1
        self.assertLessEqual(lines, SKILL_MAX_LINES,
                             "SKILL.md has %d lines (budget %d)" % (lines, SKILL_MAX_LINES))
        self.assertLessEqual(len(text.split()), SKILL_MAX_WORDS,
                             "SKILL.md has %d words (budget %d)" % (len(text.split()), SKILL_MAX_WORDS))
        desc = re.search(r"(?m)^description: (.*)$", text).group(1)
        self.assertLessEqual(len(desc), DESCRIPTION_MAX_CHARS,
                             "description is %d characters (limit %d)" % (len(desc), DESCRIPTION_MAX_CHARS))

    def test_pattern_catalog(self):
        n = words(os.path.join(REFS, "ai-patterns.md"))
        self.assertLessEqual(n, CATALOG_MAX_WORDS,
                             "ai-patterns.md has %d words (budget %d)" % (n, CATALOG_MAX_WORDS))

    def test_always_read(self):
        n = words(os.path.join(SKILL_DIR, "SKILL.md")) + words(os.path.join(REFS, "ai-patterns.md"))
        self.assertLessEqual(n, ALWAYS_MAX_WORDS,
                             "SKILL.md + ai-patterns.md is %d words (budget %d)" % (n, ALWAYS_MAX_WORDS))

    def test_common_requests(self):
        always = words(os.path.join(SKILL_DIR, "SKILL.md")) + words(os.path.join(REFS, "ai-patterns.md"))
        for name, files in COMMON_REQUESTS.items():
            with self.subTest(request=name):
                n = always + sum(words(os.path.join(REFS, f)) for f in files)
                self.assertLessEqual(n, REQUEST_MAX_WORDS,
                                     "%s reads %d words (budget %d)" % (name, n, REQUEST_MAX_WORDS))

    def test_each_guide(self):
        for path in sorted(glob.glob(os.path.join(REFS, "**", "*.md"), recursive=True)):
            rel = os.path.relpath(path, REFS)
            if rel == "ai-patterns.md":
                continue
            with self.subTest(guide=rel):
                n = words(path)
                self.assertLessEqual(n, GUIDE_MAX_WORDS,
                                     "%s has %d words (budget %d)" % (rel, n, GUIDE_MAX_WORDS))


if __name__ == "__main__":
    unittest.main()
