# Accessibility check

Check whether a piece of writing is easy for everyone to read, including people using screen readers, people with dyslexia, people reading on small phones, and people reading in a second language.

## When this applies

- "Is this easy to read?", "check accessibility", "is this clear?", "will people with screen readers be okay with this?"
- The user is preparing a notice, newsletter, form, website page, slide deck, or document for the public or a large group.

## What stays the same

This is a check first. Do not rewrite until the user asks. When they do, keep facts, names, numbers, dates, and legal wording unchanged.

## What to look for

Long sentences
- Flag sentences over about 25 words. Quote the first few words so the user can find them.

Walls of text
- Paragraphs over about 5 lines on a phone. Suggest a break or a list.

Jargon and abbreviations
- Words the intended reader may not know. Abbreviations not spelled out the first time ("SOP", "EOD", "KYC").

Unclear link text
- "Click here", "this link", "read more", or bare URLs. Screen readers often read links on their own, so the text should say where it goes ("Download the fee form").

Missing alt text
- In Word files and slides, images without a description. Suggest short alt text based on what the image shows, and ask the user to confirm, since you may not know why it is there.

Headings
- Long documents with no headings, or headings that skip levels. Screen reader users jump between headings.

Meaning carried by colour or position alone
- "Items in red are overdue" or "see the box on the right". Suggest adding a word ("marked Overdue").

Hard to scan formatting
- Text in all capitals, lots of italics, or underlined text that is not a link.

Instructions
- Several steps in one sentence. Suggest a numbered list.

## Steps

1. Ask who will read it only if it is not clear.
2. Go through the list above. Note each problem with where it is.
3. Group findings by type. Lead with the ones that will affect the most readers.
4. Offer to fix them. If the user says yes, use `modes/rewrite.md` with the findings as the focus.

For Word, PDF, and slide files, also read the matching file module so you can check images and headings.

## Reading age (only if asked)

If the user asks how hard the text is to read ("what reading level is this?", "would a 12 year old get this?"), you can give a rough reading age. Never add it by default.

1. Run `python scripts/word_count.py FILE --readability` (or pipe the text in). This works for English text only.
2. Report it in plain words as a rough guide: "This reads at about the level of a 13 year old." Add the one or two things pushing it up, such as long sentences or long words.
3. Do not put the number in the change summary, and do not present it as a score or a grade the text passed or failed.
4. If the script fails, or the text is not in English, describe it in words instead: "Most sentences are short and the words are everyday ones, so most adults will find it easy."

## Output

```
Accessibility check

Mostly clear. A few things to fix:

- 4 sentences are over 25 words (the first starts "As per the circular...").
- 2 links say "click here". Better: "Download the form" and "See the bus timings".
- The chart on slide 3 has no description for screen readers.
- "PTM" is never spelled out.

Want me to fix these?
```

Keep it to the real problems. If the text is fine, say so in one line.

## Example

Before:

> For the fee structure click here. Students who have not paid the second instalment (highlighted in red in the attached list) by the 15th will not be permitted to sit the term exam as per the school's policy which was communicated earlier.

Findings: "click here" link text, meaning shown only in red, one 32 word sentence.

After (if asked to fix):

> See the fee structure for 2025 to 26. Students who have not paid the second instalment by the 15th cannot sit the term exam. Their names are marked "Unpaid" in the attached list.
