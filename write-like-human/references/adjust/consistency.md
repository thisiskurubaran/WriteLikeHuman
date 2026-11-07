# Consistency check

Check that a long document uses the same words, spellings, and styles all the way through. Long documents written over weeks, or by several people, drift: "e-mail" on page 2, "email" on page 9.

## When this applies

- "Check this report for consistency", "make the terms consistent", "is my thesis consistent?"
- A long document (a report, thesis, manual, policy, handbook) where the user wants it to read as one piece.
- After merging sections written by different people.

For short messages this is rarely worth doing. Use it for documents of a few pages or more.

## What stays the same

- Quotes and citations, exactly as they are, even if their spelling differs from the rest. A quote from an American source keeps "color" in a British English report.
- Names, numbers, dates, amounts, legal terms, and product names.
- Terms the user has protected (see `adjust/protected-words.md`).
- The document's layout. Follow the matching file module when editing a file.

## What to look for

- The same thing called two names: "client" and "customer", "the app" and "the platform", "Phase 2" and "Stage 2". Ask which one the user wants unless one is clearly a slip.
- One spelling style: British or American (colour/color, organise/organize), and the same choice for words with two common forms (email/e-mail, online/on-line, okay/OK).
- Number style: "10 percent" vs "10%", "five" vs "5" for small numbers, "1,00,000" vs "100,000", "Rs" vs "₹" vs "INR".
- Date style: "12 March 2026" vs "March 12, 2026" vs "12/03/2026".
- Heading capitals: Sentence case vs Title Case, and the same choice at each heading level.
- List punctuation: full stops at the end of bullets or not, capital letter at the start or not, within the same kind of list.
- Abbreviations: spelled out on first use, then used the same way after. "Annual General Meeting (AGM)", then "AGM", not "A.G.M.".
- Small things that show: "Figure 3" vs "fig. 3", "Section 2.1" vs "section 2.1".

## Steps

1. Read the whole document before reporting anything. Note each style choice and how often each version appears.
2. For each inconsistency, work out which version is used most. That is the likely default, but the user decides.
3. Report first. Group by type, show the versions found, how many times, and where (page, section, or heading).
4. Wait for the user to choose. Accept short answers: "use the most common one everywhere", "client, not customer", "keep the numbers as they are".
5. Apply only what they approved. Skip quotes, citations, and protected terms.
6. Return the file as `<original-name>-humanized.<ext>` with a short summary of what was made consistent.

## Output

First round, a report like this:

```
Consistency check

Terms
- "client" (14 times) and "customer" (5 times: sections 3 and 6)

Spelling
- Mostly British: "organise" (8). American "organize" appears twice (pages 4, 11).

Numbers
- "per cent" (6) and "%" (9). Section 5 uses "%" throughout.

Headings
- Level 2 headings are sentence case except "Next Steps And Timeline" (page 12).

Which should I use? You can say "most common everywhere".
```

Second round: the updated file and one line per change type, such as "Changed 5 'customer' to 'client'. Left the two quotes in section 6 as they were."

## Example

Before (from three pages of a report):

> The e-mail survey reached 1,200 customers. ... Most clients replied by email within 2 days. ... Next Steps And Timeline ... We will organize a follow-up in three days.

After (user chose "client", "email", sentence case, and British spelling):

> The email survey reached 1,200 clients. ... Most clients replied by email within 2 days. ... Next steps and timeline ... We will organise a follow-up in three days.

(Made up figures. "2 days" and "three days" were left as they were because the user chose to keep number style unchanged.)
