#!/usr/bin/env python3
"""Check that weekdays written next to dates are right.

Finds dates that have a weekday beside them, such as "Monday 14 March",
"Mon, 14/03/2026", "March 14, 2026 (Saturday)" or "14 March 2026, Tue",
and reports any where the weekday does not match the date.

  python date_check.py invite.txt
  python date_check.py --text "See you on Monday 14 March 2026."
  python date_check.py notice.txt --us          # read 03/04 as March 4
  python date_check.py notice.txt --year 2027   # dates with no year
  python date_check.py notice.txt --json
  cat draft.txt | python date_check.py

Numeric dates like 03/04 are read as day/month (the Indian and British
way) unless you pass --us. When a date has no year, the script uses the
next time that date comes round (today counts), or the year from --year,
and says which year it assumed. --today YYYY-MM-DD sets "today" for that
guess.

Exit code: 1 when any weekday is wrong or a date does not exist (like
30 February), 0 when everything matches or no dates were found.

Only uses the standard library.
"""

import argparse
import datetime
import json
import re
import sys

WEEKDAYS = {
    "monday": 0, "mon": 0,
    "tuesday": 1, "tues": 1, "tue": 1,
    "wednesday": 2, "wed": 2,
    "thursday": 3, "thurs": 3, "thur": 3, "thu": 3,
    "friday": 4, "fri": 4,
    "saturday": 5, "sat": 5,
    "sunday": 6, "sun": 6,
}
DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTHS = {
    "january": 1, "jan": 1, "february": 2, "feb": 2, "march": 3, "mar": 3,
    "april": 4, "apr": 4, "may": 5, "june": 6, "jun": 6, "july": 7, "jul": 7,
    "august": 8, "aug": 8, "september": 9, "sept": 9, "sep": 9,
    "october": 10, "oct": 10, "november": 11, "nov": 11, "december": 12, "dec": 12,
}

WD = r"(?P<wd>%s)" % "|".join(sorted(WEEKDAYS, key=len, reverse=True))
MON = r"(?P<mon>%s)" % "|".join(sorted(MONTHS, key=len, reverse=True))
DAY = r"(?P<day>[0-3]?\d)(?:st|nd|rd|th)?"
YEAR = r"(?P<year>\d{4}|'\d{2})"

DATE_FORMS = [
    # 14 March 2026, 14th of March, 14 Mar
    r"%s\s+(?:of\s+)?%s\.?(?:,?\s+%s)?" % (DAY, MON, YEAR),
    # March 14, 2026 or March 14th
    r"%s\.?\s+%s(?:,?\s+%s)?" % (MON, DAY, YEAR),
    # 14/03/2026, 14-03-26, 14.03, 14/03
    r"(?P<n1>[0-3]?\d)[/.\-](?P<n2>[01]?\d)(?:[/.\-](?P<nyear>\d{4}|\d{2}))?",
]
DATE_RE = [re.compile(r"(?<![\w/.\-])" + f + r"(?![\w/]|[.\-]\d)", re.IGNORECASE) for f in DATE_FORMS]
BEFORE_RE = re.compile(WD + r"\.?,?\s+(?:the\s+)?$", re.IGNORECASE)
AFTER_RE = re.compile(r"^\s*,?\s*[(\[]?\s*" + WD + r"\b\.?(?:\s*[)\]])?", re.IGNORECASE)


def find_dates(text):
    """Yield (start, end, groups) for each date, longest form first, no overlaps."""
    taken = []
    found = []
    for rx in DATE_RE:
        for m in rx.finditer(text):
            if any(m.start() < e and s < m.end() for s, e in taken):
                continue
            taken.append((m.start(), m.end()))
            found.append(m)
    found.sort(key=lambda m: m.start())
    return found


def resolve(m, us, year_opt, today):
    g = m.groupdict()
    if g.get("mon"):
        month = MONTHS[g["mon"].lower()]
        day = int(g["day"])
        year_text = g.get("year")
    else:
        a, b = int(g["n1"]), int(g["n2"])
        day, month = (b, a) if us else (a, b)
        year_text = g.get("nyear")
    assumed = None
    if year_text:
        year_text = year_text.lstrip("'")
        year = int(year_text)
        if year < 100:
            year += 2000
    elif year_opt:
        year = year_opt
        assumed = year
    else:
        year = today.year
        try:
            if datetime.date(year, month, day) < today:
                year += 1
        except ValueError:
            pass
        assumed = year
    return day, month, year, assumed


def impossible_date(m, us, year_opt, today):
    """An item for a date with no weekday that cannot exist, else None."""
    g = m.groupdict()
    named = bool(g.get("mon"))
    has_year = bool(g.get("year") or g.get("nyear"))
    if not named and not has_year:
        return None        # "14.03" may be a version number or a score
    day, month, year, assumed = resolve(m, us, year_opt, today)
    if not (1 <= month <= 12 and 1 <= day <= 31):
        return None        # not a date at all, for example "45/80/2024"
    if month == 2 and day == 29 and not has_year:
        return None        # fine in a leap year, and no year was given
    try:
        datetime.date(year, month, day)
        return None
    except ValueError:
        pass
    text = m.string
    return {"text": m.group(0).strip().rstrip("."), "line": text.count("\n", 0, m.start()) + 1,
            "stated_weekday": None, "year_assumed": assumed, "date": None, "actual_weekday": None,
            "ok": False, "problem": "%d/%d/%d is not a real date" % (day, month, year)}


def check(text, us=False, year_opt=None, today=None):
    today = today or datetime.date.today()
    results = []
    for m in find_dates(text):
        before = BEFORE_RE.search(text[max(0, m.start() - 20):m.start()])
        after = AFTER_RE.match(text[m.end():m.end() + 20])
        wd_match = before or after
        if not wd_match:
            # No weekday to compare, but a date that can't exist ("31 April",
            # "29 Feb 2023") is still worth flagging.
            impossible = impossible_date(m, us, year_opt, today)
            if impossible:
                results.append(impossible)
            continue
        stated = WEEKDAYS[wd_match.group("wd").lower()]
        if before:
            start = m.start() - (len(before.group(0)))
            end = m.end()
        else:
            start = m.start()
            end = m.end() + after.end()
        day, month, year, assumed = resolve(m, us, year_opt, today)
        line = text.count("\n", 0, start) + 1
        item = {"text": text[start:end].strip().rstrip("."), "line": line,
                "stated_weekday": DAY_NAMES[stated], "year_assumed": assumed}
        try:
            date = datetime.date(year, month, day)
        except ValueError:
            item.update({"date": None, "actual_weekday": None, "ok": False,
                         "problem": "%d/%d/%d is not a real date" % (day, month, year)})
            results.append(item)
            continue
        item.update({"date": date.isoformat(), "actual_weekday": DAY_NAMES[date.weekday()],
                     "ok": date.weekday() == stated})
        results.append(item)
    return results


def describe(results):
    if not results:
        return "No dates with a weekday, and no impossible dates, found."
    lines = []
    for r in results:
        note = " (year assumed: %d)" % r["year_assumed"] if r["year_assumed"] else ""
        if r.get("problem"):
            lines.append('Line %d: "%s": %s.%s' % (r["line"], r["text"], r["problem"], note))
        elif r["ok"]:
            lines.append('Line %d: "%s": OK%s' % (r["line"], r["text"], note))
        else:
            d = datetime.date.fromisoformat(r["date"])
            lines.append('Line %d: "%s": MISMATCH, %s is a %s, not %s.%s'
                         % (r["line"], r["text"], d.strftime("%d %B %Y").lstrip("0"),
                            r["actual_weekday"], r["stated_weekday"], note))
    bad = sum(1 for r in results if not r["ok"])
    lines.append("Checked %d date%s, %d to fix." % (len(results), "" if len(results) == 1 else "s", bad))
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Check weekdays written next to dates.")
    parser.add_argument("file", nargs="?", help="text file (default: read from stdin)")
    parser.add_argument("--text", help="check this text instead of a file")
    parser.add_argument("--us", action="store_true", help="read numeric dates as month/day")
    parser.add_argument("--year", type=int, help="year to use for dates written without one")
    parser.add_argument("--today", help="treat this date (YYYY-MM-DD) as today when guessing a year")
    parser.add_argument("--json", action="store_true", help="print JSON")
    args = parser.parse_args()

    if args.text is not None:
        text = args.text
    elif args.file:
        with open(args.file, encoding="utf-8-sig") as fh:
            text = fh.read()
    else:
        text = sys.stdin.read()
    today = datetime.date.fromisoformat(args.today) if args.today else None

    results = check(text, args.us, args.year, today)
    bad = sum(1 for r in results if not r["ok"])
    if args.json:
        print(json.dumps({"dates": results, "to_fix": bad}, ensure_ascii=False, indent=2))
    else:
        print(describe(results))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
