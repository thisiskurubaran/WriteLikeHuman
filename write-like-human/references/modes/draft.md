# Draft mode

Write new text that sounds like a person from the first draft, so there is nothing to fix later.

## When this applies

- "Write me a...", "draft a...", "help me write...", "can you write a reply to this".
- The user gives notes, bullet points, or a situation and wants finished text.

## What stays the same

There is no original text, so "the same" means the facts the user gave you:

- Every name, number, date, place, and amount they mention goes in exactly as given.
- Nothing gets added that they did not tell you. No made up achievements, anecdotes, reasons, or quotes.
- If they wrote to you in a certain style (casual, Hinglish, short), that is a strong hint for the draft's style.

## Steps

1. Work out three things: who will read it, what the user wants to happen after they read it, and how formal the setting is.
2. Check you have the facts you need. If something essential is missing (the date of the leave, who the speech is about), ask one short question. Ask about at most two things. If it is not essential, write the draft and leave a clear blank like `[your manager's name]`.
3. If the user gave a voice profile, follow it.
4. Load the writing module for the type (email, speech, letter, and so on) and follow its format.
5. Write the draft. Start with the point. Use plain words. Vary sentence length. Use the specifics the user gave you instead of general statements.
6. Read it against `ai-patterns.md`. Fix any patterns before showing it.
7. Check every fact against what the user told you.

## Things to avoid

- Writing a long draft when a short one would do. A thank you message is three lines, not three paragraphs.
- Filling gaps with plausible details. A blank in brackets is better than a made up fact.
- Opening with "I hope this email finds you well" or any line from the openers list in `ai-patterns.md`, unless the setting truly calls for a formula (some formal Indian letters do, see `writing/formal-letters.md`).
- Offering three versions unless asked. Give one good one.

## When the user wants a file

Sometimes the user wants the result as a file: "write my leave letter as a Word file", "make this notice a PDF I can print", "put these expenses in a spreadsheet with a notes column".

1. Write the content first, following the steps above. The words are your job. Building the file is a separate step.
2. Build the file with Claude's built in file tools (the docx, pdf, or xlsx skills) when they are available. If file creation is turned off, give the text and tell the user in one line how to turn on **Code execution and file creation** in Settings.
3. Keep the layout plain and familiar: a clear heading, normal paragraphs, the format the writing module asks for (for example the Indian letter format in `writing/formal-letters.md`). No decorative styling the user did not ask for.
4. Spreadsheets: put in only the numbers, dates, and names the user gave you, exactly as given. You write the headings, labels, and notes. Never invent figures to fill a row. If you add a total, use a formula so it stays correct, and say so.
5. Name the file after what it is, in lowercase with hyphens, like `leave-letter.docx` or `trip-expenses.xlsx`.
6. Check the facts in the file against what the user told you, the same as for text.

To change a file the user already has, this is not draft mode. Use rewrite mode with the matching file module (`files/word.md`, `files/pdf.md`, `files/spreadsheet.md`).

## Output

- The draft first, ready to copy.
- If you left blanks, list them after the draft in one line: "Fill in: your manager's name, the last working day."
- A change summary is not needed for drafts. Instead, if you made a choice the user might want to change (formal vs friendly, long vs short), say so in one line.

## Example

User: "write a msg to my building secretary that the water tank cleaning date clashes with my mom's surgery on 14th, can they move it"

Draft:

> Hi Mr. Kulkarni, the tank cleaning is set for the 14th, but my mother has surgery that day and we'll need water at home before and after. Would it be possible to move it by a day or two? Happy to help inform the other flats if it changes. Thanks, Neha (B-402)

Note: I kept it polite but direct. Tell me if you want it more formal.

(Made up names. "B-402" is a placeholder for the user's flat number; in real use, leave `[flat number]` if they did not give one.)
