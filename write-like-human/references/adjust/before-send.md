# Before you send

A quick last look at a message or document for the small mistakes that embarrass people after they hit send. This is a check, not a rewrite.

## When this applies

- "Check this before I send it", "anything wrong with this?", "did I miss anything?", "final check".
- The user is replying to a message and pastes both, and asks if the reply covers everything.
- After a rewrite or draft, when the user asks for one last look.

## What stays the same

Everything. You report problems; you do not change the text unless the user asks. When they do, fix only the items they agree to, and follow the core rules for the rest.

## What to look for

- An attachment mentioned but nothing attached: "please find attached", "I've attached", "see the enclosed", "PFA". If the user is writing in chat, you can't see their email client, so ask: "You mention an attachment. Remember to add it."
- A weekday that doesn't match its date: "Monday, 14 March 2027". Run `python scripts/date_check.py FILE` (or pipe the text in, or use `--text "..."`). Add `--us` if the writer uses MM/DD dates, and `--year N` when dates are written without a year. It also flags dates that cannot exist, like "31 April" or "29 Feb 2023". Exit code 1 means something to fix. If the script fails, work the weekday out carefully yourself, and if you're not sure, say so instead of guessing.
- Questions left unanswered. If the user pasted the message they're replying to, list each question or request in it and check the reply answers it. "She asked whether Thursday works. Your reply doesn't say."
- A name spelled two ways in the same message: "Priya" in the greeting, "Pria" in the body.
- The wrong name, or no name, in the greeting. "Hi Rahul" in a reply to Rohan. If the user pasted the original message, compare with how the sender signed off.
- Placeholders left in: `[name]`, `[date]`, `XX`, `TBD`, `<company>`, "Lorem ipsum".
- Amounts that disagree with themselves: "Rs 5,000 (five hundred rupees)", "₹2.5 lakh (2,50,00)". Point it out; never decide which one is right.
- Dates that disagree: "the meeting on 12 June" in one line and "see you on the 13th" in another.
- Something promised but missing: "Here are the three options:" followed by two.

Skip anything that's just style. Tone and AI patterns belong in check mode, not here.

## Steps

1. Read the whole message once. If the user gave the message being replied to, read that first.
2. Go through the list above. Run `date_check.py` if the text has any dates.
3. Collect only real problems. If you're not sure something is wrong, say "check this" rather than "this is wrong".
4. Report them, most important first. Wrong names and wrong dates come before a missing comma.
5. If the user asks you to fix them, fix only those items and return the full text.

## Output

A short list, one problem per line, with the exact bit quoted so the user can find it:

```
Before you send
- You mention "please find attached", so don't forget the file.
- "Monday 14 March": 14 March 2027 is a Sunday.
- Arjun asked if the price includes delivery. Your reply doesn't say.
- "Rs 12,000 (twelve hundred)": the number and the words disagree.

Want me to fix these?
```

If nothing turns up, say so in one line: "Looks good to send." Do not invent small problems to fill the list.

## Example

Message being replied to:

> Hi Neha, can you confirm the venue for Saturday and whether kids are welcome? Thanks, Deepak

User's reply:

> Hi Deepika, the venue is Green Leaf Banquet, Koramangala, on Saturday 9 March. Please find the map attached. See you there!

Check:

```
Before you send
- The greeting says "Deepika", but the message was signed "Deepak".
- Deepak asked whether kids are welcome. Your reply doesn't say.
- "Please find the map attached", so remember to attach it.
- "Saturday 9 March": check the year. 9 March 2025 was a Sunday.

Want me to fix these?
```

(Made up names and venue. The weekday line assumes the user didn't give a year; in real use, run the script with `--year` if the year is known.)
