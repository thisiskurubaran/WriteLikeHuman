#!/usr/bin/env python3
"""Pull one person's own messages out of a WhatsApp chat export.

Use this only with the user's own messages, to build their voice profile.
It never needs anyone else's messages, so it drops them.

  python chat_export_filter.py chat.txt --list-senders
  python chat_export_filter.py chat.txt --sender "Asha" -o asha-samples.txt
  python chat_export_filter.py chat.txt --sender "Asha" --max 200

--list-senders prints each sender name with how many messages they sent,
so the user can say which name is theirs.

--sender prints only that person's messages, one per block, oldest first.
It drops:
  - media placeholders ("<Media omitted>", "image omitted", and the like)
  - deleted messages ("This message was deleted", "You deleted this message")
  - system lines (joined, left, changed the group name, encryption notice)
and it replaces phone numbers, email addresses, and links with
[phone], [email], and [link].

--max N keeps only the last N messages (the most recent ones), which is
usually enough for a voice profile.

Handles the common Android and iPhone export formats, for example:
  12/03/24, 9:15 pm - Asha: text
  [12/03/24, 9:15:02 PM] Asha: text
Messages that run over several lines are kept together.

Only uses the standard library.
"""

import argparse
import collections
import re
import sys

LINE_RE = re.compile(
    r"^‎?\[?"
    r"(?P<date>\d{1,4}[./-]\d{1,2}[./-]\d{1,4}),?\s+"
    r"(?P<time>\d{1,2}[:.]\d{2}(?:[:.]\d{2})?(?:\s?[  ]?[AaPp]\.?\s?[Mm]\.?)?)"
    r"\]?\s*(?:-\s*)?"
    r"(?P<rest>.*)$"
)
SENDER_RE = re.compile(r"^(?P<sender>[^:]{1,60}?):\s(?P<text>.*)$", re.S)

MEDIA = re.compile(
    r"^‎?\s*(<\s*media omitted\s*>|<attached:.*>|(image|video|audio|sticker|gif|document|contact card) omitted"
    r"|.*\.(jpg|jpeg|png|webp|mp4|opus|pdf) \(file attached\))\s*$",
    re.I,
)
DELETED = re.compile(r"^‎?\s*(this message was deleted|you deleted this message)\.?\s*$", re.I)
EDITED_TAG = re.compile(r"\s*<this message was edited>\s*$", re.I)
URL = re.compile(r"(https?://\S+|www\.\S+)", re.I)
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE = re.compile(r"(?<![\w])\+?\d[\d\s().-]{7,}\d(?![\w])")


def parse(lines):
    """Yield (sender, text) for every message. System lines have sender None."""
    sender, buf = None, None
    for raw in lines:
        line = raw.rstrip("\n").rstrip("\r")
        m = LINE_RE.match(line)
        if m:
            if buf is not None:
                yield sender, "\n".join(buf)
            rest = m.group("rest")
            sm = SENDER_RE.match(rest)
            if sm:
                sender, buf = sm.group("sender").strip().lstrip("‎~ ").strip(), [sm.group("text")]
            else:
                sender, buf = None, [rest]
        elif buf is not None:
            buf.append(line)
    if buf is not None:
        yield sender, "\n".join(buf)


def redact(text):
    text = URL.sub("[link]", text)
    text = EMAIL.sub("[email]", text)
    text = PHONE.sub(lambda m: "[phone]" if sum(c.isdigit() for c in m.group()) >= 9 else m.group(), text)
    return text


def clean(text):
    text = EDITED_TAG.sub("", text).strip()
    if not text or MEDIA.match(text) or DELETED.match(text):
        return None
    return redact(text)


def main():
    parser = argparse.ArgumentParser(description="Keep only one sender's messages from a WhatsApp export.")
    parser.add_argument("file", help="the exported chat .txt")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list-senders", action="store_true", help="list senders with message counts")
    group.add_argument("--sender", help="the user's own name as it appears in the export")
    parser.add_argument("-o", "--output", help="write messages here instead of printing them")
    parser.add_argument("--max", type=int, help="keep only the most recent N messages")
    args = parser.parse_args()

    with open(args.file, encoding="utf-8-sig") as fh:
        messages = list(parse(fh))

    if args.list_senders:
        counts = collections.Counter(s for s, _ in messages if s)
        if not counts:
            sys.exit("No messages found. Is this a WhatsApp chat export (.txt)?")
        for name, n in counts.most_common():
            print("%5d  %s" % (n, name))
        return

    wanted = args.sender.strip().casefold()
    kept = []
    for sender, text in messages:
        if sender and sender.casefold() == wanted:
            cleaned = clean(text)
            if cleaned:
                kept.append(cleaned)
    if not kept:
        sys.exit("No messages from %r. Run with --list-senders to see the names." % args.sender)
    if args.max:
        kept = kept[-args.max:]
    out = "\n\n".join(kept) + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(out)
        print("Wrote %d messages from %s to %s" % (len(kept), args.sender, args.output))
    else:
        sys.stdout.write(out)


if __name__ == "__main__":
    main()
