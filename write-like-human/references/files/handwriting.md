# Handwriting (photos of notes, whiteboards, letters)

## When this applies

The user sends a photo of handwriting and wants it as typed text or a Word file. Typical cases:

- Notes from a class or a meeting, written in a notebook
- A whiteboard after a planning session
- A diary page, a recipe card, or an old family letter
- A handwritten draft of a speech, essay, or application

Claude reads the photo directly. No script is needed to read it. If the user wants a Word file, build it with Claude's built in docx skill.

If the user also wants the writing improved, load the matching writing module and treat the typed text like any pasted text, after they have checked it.

## What stays the same

- The writer's own words. Typing up handwriting is copying, not rewriting.
- Every name, number, date, amount, and address exactly as written
- The order of the notes, and any structure on the page: headings, lists, arrows, numbered points
- Spelling, grammar, and dialect, unless the user asks you to tidy them
- In personal letters and diaries, the content, the tone, and the feelings. Never "improve" them.

## Steps

1. **Read the whole page first.** Work out the layout: is it a list, paragraphs, a table, a mind map with arrows?
2. **Type it out in the same order**, keeping headings, bullets, and numbering. For a whiteboard or mind map, turn arrows into a simple list or "A leads to B" lines, and say that you did.
3. **Mark anything you can't read.** Never guess silently. Write `[unclear: Mehta?]` with your best guess and a question mark, or `[unclear]` if you have no guess. Numbers and names you aren't sure of are always marked.
4. **Leave crossed-out words out**, unless the user wants them kept. If a crossed-out word changes the meaning, mention it.
5. **Tidy only what the user asked for.** "Type this up" means copy it as written. "Type this up and fix the spelling" means fix obvious spelling only. Rewording is a separate request.
6. **List the unclear bits** at the end so the user can check them against the original.
7. If they want a Word file, build it with plain headings and lists and name it after what it is, like `meeting-notes-12-march.docx`.

## Output

- The typed text, or a Word file, with the page's structure kept.
- A short list of unclear words for the user to check:
  > Three words I couldn't read for sure: the surname on line 2 (Mehta?), the amount next to "rent" (4,500 or 4,800?), and one word in the last line.
- If the user asked for a rewrite as well, do it only after they've confirmed the typed text.

## Example

Photo of a notebook page, as written:

> Team mtg 12/3
> - launch moved to 28th (Priya)
> - need 3 more testers, ask Ravi
> - budget ~ 45k?? check w/ finance
> - next mtg Fri

Typed up:

> Team meeting, 12/3
> - Launch moved to the 28th (Priya)
> - Need 3 more testers, ask Ravi
> - Budget around 45k?? Check with finance
> - Next meeting Friday

Unclear: none. I expanded "mtg" and "w/" since you asked for it tidied. The "??" is in the original, so I kept it.

If the user had said only "type this up", the abbreviations would stay as written.

## If something goes wrong

- **The photo is blurry, dark, or cut off:** say which part you can't read and ask for a clearer photo of just that part. Don't fill gaps with guesses.
- **Most of the page is unreadable:** type what you can, mark the rest `[unclear]`, and say plainly that the photo is hard to read rather than presenting a half guess as the text.
- **The handwriting is in another language or script:** type it in that language and script. Don't translate unless asked. Load the matching `languages/` file for the user's language.
- **The page has drawings, diagrams, or a table:** describe drawings in one line in brackets, and turn a table into a typed table.
- **It's a signed letter or a legal document:** type the text, and note that a typed copy is not the same as the signed original.
