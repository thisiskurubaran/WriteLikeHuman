"""Optional eval runner: sends tests/evals/evals.json through the Claude API.

This is NOT part of the normal tests and never runs on its own. Each run
calls the API and costs money on your own account, so run it by hand
before a release if you want an automatic first pass. It prints the
tokens used and an estimated cost at the end, and --max-cost stops the
run before the estimate goes over a limit you set. Trying the cases
in the Claude app (see tests/evals/README.md) is still the real test.

How it works, for each case:
  1. Claude gets SKILL.md as its instructions and a read_reference tool
     that returns files from write-like-human/references/. The runner
     records which files it reads.
  2. Claude answers the case prompt.
  3. A second call grades the answer against the case's "must" and
     "must_not" lists and returns pass or fail with reasons.
  4. The files Claude read are compared with "should_load".

Cases that need an attached or pasted file, or Claude Code with a real
repository, are skipped.

Setup:
  pip install anthropic
  export ANTHROPIC_API_KEY=...        (or sign in with `ant auth login`)

Usage, from the repo root:
  python tests/run_evals.py                   # every case
  python tests/run_evals.py --case check-paragraph --case us-to-uk
  python tests/run_evals.py --model claude-sonnet-5-5 --json results.json
  python tests/run_evals.py --save v0.4.0     # keep a score summary for this release
  python tests/run_evals.py --max-cost 5      # stop before spending more than about $5

Saved summaries go to tests/evals/results/<label>.json, with the date,
model, and pass, fail, and skip counts per case, so scores can be
compared from release to release. They hold no answers, only results.
"""

import argparse
import datetime
import json
import os
import re
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

# US dollars per million tokens: input, output, cache write (5 minute), cache read.
# Used only for the cost estimate. Other models get token counts and no estimate.
PRICES = {
    "claude-opus-5-5": (4.00, 20.00, 5.00, 0.20),
    "claude-sonnet-5-5": (2.00, 10.00, 2.50, 0.10),
}


class Spend:
    """Adds up token usage across calls, per model."""

    def __init__(self):
        self.by_model = {}

    def add(self, model, usage):
        if usage is None:
            return
        t = self.by_model.setdefault(model, [0, 0, 0, 0])
        t[0] += getattr(usage, "input_tokens", 0) or 0
        t[1] += getattr(usage, "output_tokens", 0) or 0
        t[2] += getattr(usage, "cache_creation_input_tokens", 0) or 0
        t[3] += getattr(usage, "cache_read_input_tokens", 0) or 0

    def cost(self):
        """Estimated dollars, or None if a model has no known price."""
        total = 0.0
        for model, t in self.by_model.items():
            if model not in PRICES:
                return None
            total += sum(n * price for n, price in zip(t, PRICES[model])) / 1e6
        return total

    def report(self):
        lines = []
        for model, (inp, out, write, read) in self.by_model.items():
            lines.append("%s: %d input, %d output, %d written to cache, %d read from cache"
                         % (model, inp, out, write, read))
        cost = self.cost()
        lines.append("Estimated cost: %s" % ("$%.2f" % cost if cost is not None else "unknown for this model"))
        return "\n".join(lines)

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
    """True for cases the API can't run: an attached file, or Claude Code in a repo."""
    prompt = case["prompt"].lower()
    return "(attach" in prompt or "(paste" in prompt or "(in claude code" in prompt


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


def run_case(client, model, case, spend):
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
        # The skill text is the same for every case, so it is cached once
        # and read back cheaply. The top-level cache_control caches the
        # growing conversation within a case, turn by turn.
        system=[{"type": "text", "text": skill_system_prompt(), "cache_control": {"type": "ephemeral"}}],
        cache_control={"type": "ephemeral"},
        tools=[read_reference],
        messages=[{"role": "user", "content": case["prompt"]}],
        output_config={"effort": "medium"},
        betas=[FALLBACK_BETA],
        fallbacks="default",
    )
    final = None
    for message in runner:
        spend.add(model, message.usage)
        final = message
    if final.stop_reason == "refusal":
        return "", loaded, "refused"
    answer = "".join(b.text for b in final.content if b.type == "text")
    return answer, loaded, final.stop_reason


def judge(client, model, case, answer, spend):
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
    spend.add(model, response.usage)
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
    parser.add_argument("--max-cost", type=float, metavar="DOLLARS",
                        help="Stop before the estimated spend goes over this many US dollars")
    parser.add_argument("--save", metavar="LABEL", help="Save a score summary as tests/evals/results/LABEL.json, for example v0.4.0")
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
    spend = Spend()
    stopped = False

    for case in cases:
        cost = spend.cost()
        done = passed + failed
        if args.max_cost is not None and cost is not None and done:
            # Stop if one more case at the average so far would go over the limit.
            if cost + cost / done > args.max_cost:
                print("STOP  spending limit: about $%.2f used, next case would pass $%.2f" % (cost, args.max_cost))
                stopped = True
                break
        if needs_attachment(case):
            print("SKIP  %s (needs a file or Claude Code, try it in the app)" % case["id"])
            skipped += 1
            continue
        try:
            answer, loaded, stop = run_case(client, args.model, case, spend)
            grade = judge(client, args.judge_model, case, answer, spend) if answer else {
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

    print("\n%d passed, %d failed, %d skipped%s" % (passed, failed, skipped,
                                                 " (stopped early at the spending limit)" if stopped else ""))
    print(spend.report())
    if args.save:
        if not re.fullmatch(r"[A-Za-z0-9._-]+", args.save):
            sys.exit("--save label may only use letters, numbers, dots, dashes, and underscores")
        out_dir = os.path.join(ROOT, "tests", "evals", "results")
        os.makedirs(out_dir, exist_ok=True)
        summary = {
            "label": args.save,
            "date": datetime.date.today().isoformat(),
            "model": args.model,
            "judge_model": args.judge_model,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "pass_rate": round(passed / (passed + failed), 3) if passed + failed else None,
            "estimated_cost_usd": round(spend.cost(), 2) if spend.cost() is not None else None,
            "stopped_early": stopped,
            "cases": {r["id"]: r["passed"] for r in results},
        }
        path = os.path.join(out_dir, args.save + ".json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print("Score summary saved to %s" % os.path.relpath(path, ROOT))
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print("Full results written to %s" % args.json)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
