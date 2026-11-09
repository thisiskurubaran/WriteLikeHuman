#!/usr/bin/env python3
"""Pull one person's own messages out of a WhatsApp, Telegram, or Signal chat export.

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

Reads these exports (the format is detected unless --format is given):
  WhatsApp, Android and iPhone .txt:
    12/03/24, 9:15 pm - Asha: text
    [12/03/24, 9:15:02 PM] Asha: text
  Telegram Desktop, "Export chat history" as JSON: the result.json file.
  Signal, plain text from common backup tools:
    [2026-03-12 09:15] Asha: text
Messages that run over several lines are kept together. The detected
format is printed to the error stream, so it never mixes with the output.

Only uses the standard library.
"""

import argparse
import collections
import json
import re
import sys

LINE_RE = re.compile(
    r"^‎?\[?"
    r"(?P<date>\d{1,4}[./-]\d{1,2}[./-]\d{1,4}),?\s+"
    r"(?P<time>\d{1,2}[:.]\d{2}(?:[:.]\d{2})?(?:\s?[  ]?[AaPp]\.?\s?[Mm]\.?)?)"
    r"\]?\s*(?:-\s*)?"
    r"(?P<rest>.*)$"
)
SIGNAL_LINE_RE = re.compile(
    r"^\[(?P<date>\d{4}-\d{2}-\d{2})[ T](?P<time>\d{1,2}:\d{2}(?::\d{2})?)\]\s*(?P<rest>.*)$"
)
SIGNAL_MEDIA = re.compile(r"^\s*\[(attachment|sticker|image|video|voice message|audio|file)[^\]]*\]\s*$", re.I)
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


def parse(lines, line_re=LINE_RE):
    """Yield (sender, text) for every message. System lines have sender None."""
    sender, buf = None, None
    for raw in lines:
        line = raw.rstrip("\n").rstrip("\r")
        m = line_re.match(line)
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


def telegram_text(value):
    """Telegram stores text as a string or a list of strings and parts."""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        out = []
        for part in value:
            if isinstance(part, str):
                out.append(part)
            elif isinstance(part, dict):
                out.append(str(part.get("text", "")))
        return "".join(out)
    return ""


def parse_telegram(raw):
    """Yield (sender, text) from a Telegram Desktop result.json."""
    data = json.loads(raw)
    messages = data.get("messages", []) if isinstance(data, dict) else []
    for msg in messages:
        if not isinstance(msg, dict):
            continue
        if msg.get("type") != "message":
            yield None, ""
            continue
        sender = msg.get("from") or msg.get("actor")
        yield (str(sender).strip() if sender else None), telegram_text(msg.get("text", ""))


def detect_format(raw):
    stripped = raw.lstrip()
    if stripped.startswith("{"):
        try:
            data = json.loads(stripped)
            if isinstance(data, dict) and isinstance(data.get("messages"), list):
                return "telegram"
        except ValueError:
            pass
    first = [l for l in raw.splitlines() if l.strip()][:20]
    if first and sum(1 for l in first if SIGNAL_LINE_RE.match(l)) >= max(1, len(first) // 2):
        return "signal"
    return "whatsapp"


def read_messages(raw, fmt):
    if fmt == "telegram":
        return list(parse_telegram(raw))
    if fmt == "signal":
        return list(parse(raw.splitlines(), SIGNAL_LINE_RE))
    return list(parse(raw.splitlines()))


def redact(text):
    text = URL.sub("[link]", text)
    text = EMAIL.sub("[email]", text)
    text = PHONE.sub(lambda m: "[phone]" if sum(c.isdigit() for c in m.group()) >= 9 else m.group(), text)
    return text


def clean(text):
    text = EDITED_TAG.sub("", text).strip()
    if not text or MEDIA.match(text) or DELETED.match(text) or SIGNAL_MEDIA.match(text):
        return None
    return redact(text)


def main():
    parser = argparse.ArgumentParser(description="Keep only one sender's messages from a WhatsApp, Telegram, or Signal export.")
    parser.add_argument("file", help="the exported chat (.txt, or result.json for Telegram)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list-senders", action="store_true", help="list senders with message counts")
    group.add_argument("--sender", help="the user's own name as it appears in the export")
    parser.add_argument("-o", "--output", help="write messages here instead of printing them")
    parser.add_argument("--max", type=int, help="keep only the most recent N messages")
    parser.add_argument("--format", choices=["auto", "whatsapp", "telegram", "signal"], default="auto",
                        help="export format (default: detect it)")
    args = parser.parse_args()

    with open(args.file, encoding="utf-8-sig") as fh:
        raw = fh.read()
    fmt = detect_format(raw) if args.format == "auto" else args.format
    try:
        messages = read_messages(raw, fmt)
    except ValueError:
        sys.exit("This doesn't look like a Telegram result.json. Try --format whatsapp or --format signal.")
    names = {"whatsapp": "WhatsApp", "telegram": "Telegram", "signal": "Signal"}
    sys.stderr.write("Reading this as a %s export.\n" % names[fmt])

    if args.list_senders:
        counts = collections.Counter(s for s, _ in messages if s)
        if not counts:
            sys.exit("No messages found. Is this a WhatsApp, Telegram, or Signal chat export?")
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
