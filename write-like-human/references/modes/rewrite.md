# Rewrite mode

Fix existing text so it reads like a person wrote it. This is the default mode.

## When this applies

- The user pastes or attaches text and says "make this sound human", "fix this", "less robotic", "less like ChatGPT", "clean this up", or just "humanize".
- The user gives text with no instruction at all and seems to want it improved.
- Any request that is not clearly a new draft, a check, or a side by side review.

## What stays the same

- What the text says. Every claim, request, and decision stays.
- Protected content: names, numbers, dates, money amounts, addresses, quotes, citations, legal terms, product names, and figures in tables.
- Length, within about 10 percent, unless the user asked for shorter or longer.
- Formality. A letter to a bank stays formal. A text to a friend stays casual.
- The language and script. Hindi stays Hindi, Hinglish in Roman script stays Hinglish in Roman script.
- The user's own habits, if the text was mostly theirs and only partly AI. Keep their quirks.
- Formatting: paragraphs, lists, headings, and line breaks, unless the formatting itself is the problem (see `ai-patterns.md`, the formatting section).

## Steps

1. Read the whole text once. Work out who it is for and what it is trying to do.
2. Note the tone it already has. That is the tone you keep unless asked otherwise.
3. If the user gave a voice profile, read it now and follow it over the general advice here.
4. Go through `ai-patterns.md` and mark what you find. Focus on the stack: openers, closers, stock words, dashes, filler, bold labels, and rhythm usually matter most.
5. Rewrite. Start where the real content starts. Use plain words. Mix sentence lengths. Cut repetition. Replace generic claims with the user's own specifics if they are already in the text.
6. Check protected content against the original, item by item. Every name, number, and date must match.
7. Do one quick re-read against `ai-patterns.md`. Fix anything you introduced. Then stop. Do not keep polishing.
8. Write the change summary as described in `SKILL.md`.

## Things to avoid

- Adding facts, examples, or feelings the user did not give you.
- Making it casual when it was professional, or stiff when it was friendly.
- Adding slang, typos, or "um" to fake a human feel.
- Turning every long sentence short. Some long sentences are fine.
- Rewriting text that was already good. If only two lines need work, change two lines and say so.

## If the text is very short

For a single line or a short message, just give the better version and one line of explanation. Skip the bulleted summary if there is only one change.

## Output

- Pasted text: the rewritten text first, then **What I changed**.
- File: a new file named `<original-name>-humanized.<ext>`, then **What I changed**. Follow the matching file module for how to edit the file.
- Optional last line: one offer, such as a tone change or building a voice profile.

## Example

Before:

> Certainly! Here's a message for your team. I'm excited to share that we have successfully completed the migration to our new billing system. This represents a significant milestone in our journey toward operational excellence. Moving forward, all invoices will be generated seamlessly through the new platform, ensuring accuracy and efficiency. Should you have any questions, please don't hesitate to reach out!

After:

> Hi all, we've finished moving to the new billing system. From now on, invoices come out of the new system automatically. If anything looks off, message me.

What I changed
- Removed the opening line meant for you, not your team.
- Cut "significant milestone in our journey toward operational excellence", which says nothing specific.
- Replaced "seamlessly" and "ensuring accuracy and efficiency" with what actually happens.
- Swapped the stock closing for a direct one.

(This example is shorter than the original because the original was mostly filler. In normal use, stay within about 10 percent.)
