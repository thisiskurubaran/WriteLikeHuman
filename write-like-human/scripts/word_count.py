#!/usr/bin/env python3
"""Count words exactly, and check a text against a target length.

Works for any language that puts spaces between words, including Hindi,
Tamil, and the other Indian languages. A "word" is any run of characters
between spaces that has at least one letter or digit in it, so a lone
"-" or "..." is not counted.

  python word_count.py essay.txt
  python word_count.py essay.txt --target 200
  python word_count.py --target 150 --tolerance 5 < draft.txt
  python word_count.py --text "Thanks for the update, see you Monday."
  python word_count.py essay.txt --json

With --target, it reports how far off the text is and whether it is within
the tolerance (10 percent by default). The exit code is 0 when within
range and 2 when not, so it can be used in a quick check.

Only uses the standard library.
"""

import argparse
import json
import re
import sys

SENTENCE_END = re.compile(r"[.!?।。]+(?=\s|$)")


def count_words(text):
    return len([w for w in text.split() if any(c.isalnum() for c in w)])


def count_sentences(text):
    found = len(SENTENCE_END.findall(text))
    return found or (1 if text.strip() else 0)


def stats(text, target=None, tolerance=10.0):
    words = count_words(text)
    sentences = count_sentences(text)
    result = {
        "words": words,
        "characters": len(text),
        "characters_no_spaces": len(re.sub(r"\s", "", text)),
        "sentences": sentences,
        "paragraphs": len([p for p in re.split(r"\n\s*\n", text) if p.strip()]),
        "average_sentence_words": round(words / sentences, 1) if sentences else 0,
    }
    if target:
        low = target * (1 - tolerance / 100.0)
        high = target * (1 + tolerance / 100.0)
        result.update({
            "target": target,
            "difference": words - target,
            "allowed_range": [int(round(low)), int(round(high))],
            "within_range": low <= words <= high,
        })
    return result


def describe(r):
    lines = ["Words: %d" % r["words"],
             "Sentences: %d (about %s words each)" % (r["sentences"], r["average_sentence_words"]),
             "Characters: %d (%d without spaces)" % (r["characters"], r["characters_no_spaces"])]
    if "target" in r:
        diff = r["difference"]
        if diff == 0:
            where = "exactly on target"
        elif diff > 0:
            where = "%d over" % diff
        else:
            where = "%d under" % -diff
        verdict = "OK" if r["within_range"] else "OUT OF RANGE"
        lines.append("Target: %d, %s, allowed %d to %d: %s"
                     % (r["target"], where, r["allowed_range"][0], r["allowed_range"][1], verdict))
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Exact word counts and target checks.")
    parser.add_argument("file", nargs="?", help="text file (default: read from stdin)")
    parser.add_argument("--text", help="count this text instead of a file")
    parser.add_argument("--target", type=int, help="target word count")
    parser.add_argument("--tolerance", type=float, default=10.0,
                        help="allowed difference in percent (default 10)")
    parser.add_argument("--json", action="store_true", help="print JSON")
    args = parser.parse_args()

    if args.text is not None:
        text = args.text
    elif args.file:
        with open(args.file, encoding="utf-8-sig") as fh:
            text = fh.read()
    else:
        text = sys.stdin.read()

    r = stats(text, args.target, args.tolerance)
    print(json.dumps(r, ensure_ascii=False, indent=2) if args.json else describe(r))
    if args.target and not r["within_range"]:
        sys.exit(2)


if __name__ == "__main__":
    main()
