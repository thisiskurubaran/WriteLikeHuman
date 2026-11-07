"""Optional eval runner: sends tests/evals/evals.json through the Claude API.

This is NOT part of the normal tests and never runs on GitHub. Each run
calls the API and costs money on your own account, so run it by hand
before a release if you want an automatic first pass. Trying the cases
in the Claude app (see tests/evals/README.md) is still the real test.

How it works, for each case:
  1. Claude gets SKILL.md as its instructions and a read_reference tool
     that returns files from write-like-human/references/. The runner
     records which files it reads.
  2. Claude answers the case prompt.
  3. A second call grades the answer against the case's "must" and
     "must_not" lists and returns pass or fail with reasons.
  4. The files Claude read are compared with "should_load".

Cases that need an attached or pasted file are skipped.

Setup:
  pip install anthropic
  export ANTHROPIC_API_KEY=...        (or sign in with `ant auth login`)

Usage, from the repo root:
  python tests/run_evals.py                   # every case
  python tests/run_evals.py --case check-paragraph --case us-to-uk
  python tests/run_evals.py --model claude-sonnet-5-5 --json results.json
"""

import argparse
import json
import os
import sys

try:
    import anthropic
    from anthropic import beta_tool
except ImportError:
    sys.exit("This runner needs the Anthropic SDK: pip install anthropic")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_DIR = os.path.join(ROOT, "write-like-human")
REFERENCES = os.path.join(SKILL_DIR, "references")
EVALS = os.path.join(ROOT, "tests", "evals", "evals.json")

FALLBACK_BETA = "server-side-fallback-2026-07-01"

JUDGE_SCHEMA = {
    "type": "object",
    "properties": {
        "passed": {"type": "boolean"},
        "must": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "rule": {"type": "string"},
                    "met": {"type": "boolean"},
                    "reason": {"type": "string"},
                },
                "required": ["rule", "met", "reason"],
                "additionalProperties": False,
            },
        },
        "must_not": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "rule": {"type": "string"},
                    "happened": {"type": "boolean"},
                    "reason": {"type": "string"},
                },
                "required": ["rule", "happened", "reason"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["passed", "must", "must_not"],
    "additionalProperties": False,
}


def needs_attachment(case):
    prompt = case["prompt"].lower()
    return "(attach" in prompt or "(paste" in prompt


def skill_system_prompt():
    with open(os.path.join(SKILL_DIR, "SKILL.md"), encoding="utf-8") as f:
        skill = f.read()
    return (
        "You are Claude with the WriteLikeHuman skill installed. Its SKILL.md is below. "
        "When it tells you to read a file under references/, call the read_reference tool "
        "with the path relative to references/ (for example modes/rewrite.md). "
        "If the skill does not apply to the request, ignore it and answer normally.\n\n"
        + skill
    )


def run_case(client, model, case):
    loaded = []

    @beta_tool
    def read_reference(path: str) -> str:
        """Read a WriteLikeHuman reference file.

        Args:
            path: Path relative to references/, for example modes/rewrite.md.
        """
        clean = path.strip().lstrip("/")
        if clean.startswith("references/"):
            clean = clean[len("references/"):]
        full = os.path.realpath(os.path.join(REFERENCES, clean))
        if not full.startswith(os.path.realpath(REFERENCES) + os.sep) or not os.path.isfile(full):
            return "No such reference file: %s" % path
        loaded.append(clean)
        with open(full, encoding="utf-8") as f:
            return f.read()

    runner = client.beta.messages.tool_runner(
        model=model,
        max_tokens=16000,
        system=skill_system_prompt(),
        tools=[read_reference],
        messages=[{"role": "user", "content": case["prompt"]}],
        output_config={"effort": "medium"},
        betas=[FALLBACK_BETA],
        fallbacks="default",
    )
    final = runner.until_done()
    if final.stop_reason == "refusal":
        return "", loaded, "refused"
    answer = "".join(b.text for b in final.content if b.type == "text")
    return answer, loaded, final.stop_reason


def judge(client, model, case, answer):
    rubric = {
        "prompt": case["prompt"],
        "must": case["must"],
        "must_not": case["must_not"],
        "answer": answer,
    }
    response = client.beta.messages.create(
        model=model,
        max_tokens=4000,
        system=(
            "You grade replies from a writing assistant. For each 'must' rule, say whether "
            "the answer meets it. For each 'must_not' rule, say whether it happened. "
            "'the skill does not load' is met when the answer is a normal reply with no "
            "humanizing, change summary, or rewrite. passed is true only if every must is "
            "met and no must_not happened. Be strict and brief."
        ),
        messages=[{"role": "user", "content": json.dumps(rubric, ensure_ascii=False)}],
        output_config={"effort": "low", "format": {"type": "json_schema", "schema": JUDGE_SCHEMA}},
        betas=[FALLBACK_BETA],
        fallbacks="default",
    )
    if response.stop_reason == "refusal":
        return {"passed": False, "must": [], "must_not": [], "error": "judge refused"}
    text = next(b.text for b in response.content if b.type == "text")
    return json.loads(text)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--case", action="append", help="Run only this case id (repeatable)")
    parser.add_argument("--model", default="claude-opus-5-5", help="Model for the skill (default: claude-opus-5-5)")
    parser.add_argument("--judge-model", default="claude-opus-5-5", help="Model for grading (default: claude-opus-5-5)")
    parser.add_argument("--json", metavar="FILE", help="Also write full results to this JSON file")
    args = parser.parse_args()

    with open(EVALS, encoding="utf-8") as f:
        cases = json.load(f)["cases"]
    if args.case:
        wanted = set(args.case)
        unknown = wanted - {c["id"] for c in cases}
        if unknown:
            sys.exit("Unknown case id: %s" % ", ".join(sorted(unknown)))
        cases = [c for c in cases if c["id"] in wanted]

    client = anthropic.Anthropic()
    results, passed, failed, skipped = [], 0, 0, 0

    for case in cases:
        if needs_attachment(case):
            print("SKIP  %s (needs a file, try it in the Claude app)" % case["id"])
            skipped += 1
            continue
        try:
            answer, loaded, stop = run_case(client, args.model, case)
            grade = judge(client, args.judge_model, case, answer) if answer else {
                "passed": False, "must": [], "must_not": [], "error": "no answer (%s)" % stop}
        except anthropic.APIStatusError as e:
            print("ERROR %s: API returned %s" % (case["id"], e.status_code))
            failed += 1
            continue
        except anthropic.APIConnectionError:
            sys.exit("Could not reach the Claude API. Check your network and try again.")

        expected = set(case["should_load"])
        missing = sorted(expected - set(loaded))
        loads_ok = not missing if expected else not loaded
        ok = grade.get("passed", False) and loads_ok
        passed += ok
        failed += not ok
        print("%s  %s" % ("PASS" if ok else "FAIL", case["id"]))
        if missing:
            print("      did not read: %s" % ", ".join(missing))
        if not expected and loaded:
            print("      read skill files when it should not have: %s" % ", ".join(loaded))
        for item in grade.get("must", []):
            if not item["met"]:
                print("      missed: %s (%s)" % (item["rule"], item["reason"]))
        for item in grade.get("must_not", []):
            if item["happened"]:
                print("      did: %s (%s)" % (item["rule"], item["reason"]))
        if grade.get("error"):
            print("      %s" % grade["error"])
        results.append({"id": case["id"], "passed": ok, "loaded": loaded, "answer": answer, "grade": grade})

    print("\n%d passed, %d failed, %d skipped" % (passed, failed, skipped))
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print("Full results written to %s" % args.json)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
