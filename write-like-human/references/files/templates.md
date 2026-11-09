# Templates (.docx, .pptx)

## When this applies

The user gives you a Word or PowerPoint file to use as a template, plus the content to put in it. Typical requests:

- "Write my leave letter on our company letterhead" (with a `.docx` letterhead)
- "Put my details into this resume layout"
- "Fill this certificate template for Priya Nair"
- "Use our team's slide template for these notes"

The template decides the look. You decide the words, using only the facts the user gives you. Load the writing module for the kind of document too (for example `writing/formal-letters.md` or `writing/resume.md`).

If the user wants a brand new file with no template, use draft mode instead (`modes/draft.md`, "When the user wants a file").

## What stays the same

- Everything about the template's look: fonts, colours, logos, headers and footers, margins, table layout, slide masters, bullet styles
- Fixed text that belongs to the template, such as the company address in the letterhead or a legal footer
- The order of sections, unless the user asks to change it
- Protected content from the core rules: names, numbers, dates, money, addresses, quotes, product names

Only placeholder text and the sections meant for content change.

## Steps

1. **Find the placeholders.** List the template's text:
   ```
   python scripts/docx_rewrite.py extract <template>.docx -o segments.json
   python scripts/pptx_rewrite.py extract <template>.pptx -o segments.json
   ```
   Placeholders usually look like `[Name]`, `{{date}}`, `<Company>`, `XXXX`, `Lorem ipsum`, or sample text such as "John Doe, Marketing Manager".
2. **Match the user's facts to the placeholders.** Name to name, date to date. If the user didn't give a fact a placeholder asks for, leave a clear blank like `[your employee ID]`. Never fill it with a guess or sample data.
3. **Write the body text** in the template's sections, following `ai-patterns.md`, the mode module, and the writing module. Keep each section about the length the template expects, so the layout holds.
4. **Leave sample content out** if the user gave nothing for it. A resume template's sample "Volunteer work" section is removed or left as a clear placeholder, never filled with invented experience.
5. **Write the changes as JSON** (id to new text) and apply them, so styles stay as they were:
   ```
   python scripts/docx_rewrite.py apply <template>.docx changes.json -o <template-name>-filled.docx
   python scripts/pptx_rewrite.py apply <template>.pptx changes.json -o <template-name>-filled.pptx
   ```
6. **Read the CHECK lines** for changed numbers and slide text that may not fit its box. Fix anything they flag.
7. **Check every fact** in the filled file against what the user told you.

## Output

- A new file named `<template-name>-filled.docx` (or `.pptx`). The template is never overwritten, so the user can use it again.
- A short summary: which placeholders you filled, and a one-line list of anything still blank.
  > Filled your name, today's date, and the leave dates. Still blank: your employee ID, which wasn't in your message.

## Example

Template `letterhead.docx`, before:

> [Date]
>
> To,
> [Recipient name]
> [Recipient title]
>
> Subject: [Subject]
>
> [Body of the letter]

The user says: "Leave letter to Mr. Suresh Rao, HR Manager, for 3 to 5 March, my daughter's school annual day. I'm Kavya Iyer."

After (`letterhead-filled.docx`, same fonts and logo):

> [Date]
>
> To,
> Mr. Suresh Rao
> HR Manager
>
> Subject: Leave from 3 to 5 March
>
> I request leave from 3 to 5 March to attend my daughter's school annual day. I will make sure my pending work is handed over before I leave.
>
> Kavya Iyer

The date stays `[Date]` because the user didn't give one. "Handed over" is only right if the user mentioned it. If not, leave that sentence out.

## If something goes wrong

- **The script fails or python-docx or python-pptx is missing:** use Claude's built in docx or pptx skill to edit the copy, with the same rules. If neither works, give the filled text section by section ("Recipient: ...", "Body: ...") so the user can paste it into the template.
- **Placeholders are in text boxes, headers, or footers the script didn't list:** say which ones, and give the text to paste there.
- **The template is a PDF:** a PDF can't be filled like a Word file. If it has fillable boxes, use `files/forms.md`. If not, ask for the Word version, or build a new Word file that copies its layout and say so.
- **The template is a .dotx or .potx:** ask the user to open it and save it as `.docx` or `.pptx` first, or treat it as a normal file if the script reads it.
- **Text overflows a box or a page:** shorten the words. Never change fonts, sizes, or margins to make it fit.
