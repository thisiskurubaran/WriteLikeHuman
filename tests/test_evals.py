"""Checks that the eval file is well formed and points at real modules.

The evals themselves are run by hand in Claude (see tests/evals/README.md).
This test only makes sure the list stays usable: every case has the
fields it needs and every module it names exists in the skill.

Run from the repo root:  python -m unittest discover -s tests -v
"""

import json
import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFERENCES = os.path.join(ROOT, "write-like-human", "references")
EVALS = os.path.join(ROOT, "tests", "evals", "evals.json")


class EvalFileTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(EVALS, encoding="utf-8") as f:
            cls.data = json.load(f)
        cls.cases = cls.data["cases"]

    def test_has_cases(self):
        self.assertGreater(len(self.cases), 0)

    def test_ids_are_unique(self):
        ids = [c["id"] for c in self.cases]
        self.assertEqual(len(ids), len(set(ids)))

    def test_cases_have_required_fields(self):
        for case in self.cases:
            with self.subTest(case=case.get("id")):
                for key in ("id", "prompt", "should_load", "must", "must_not"):
                    self.assertIn(key, case)
                self.assertTrue(case["prompt"].strip())
                self.assertIsInstance(case["should_load"], list)
                self.assertTrue(case["must"], "every case needs at least one 'must'")

    def test_named_modules_exist(self):
        for case in self.cases:
            for module in case["should_load"]:
                with self.subTest(case=case["id"], module=module):
                    self.assertTrue(
                        os.path.isfile(os.path.join(REFERENCES, module)),
                        "%s names a module that does not exist: %s" % (case["id"], module),
                    )

    def test_includes_cases_that_should_not_trigger(self):
        self.assertTrue(any(not c["should_load"] for c in self.cases))


if __name__ == "__main__":
    unittest.main()
