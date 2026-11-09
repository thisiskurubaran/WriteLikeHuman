# Word documents (.docx)

## When this applies

The user attaches a `.docx` file: a report, a letter, a resume, an essay, a policy, meeting minutes. Load this module together with the writing module for the kind of document (a resume as a Word file also loads `writing/resume.md`).

If they only paste text copied out of Word, you do not need this module. Work on the pasted text.

## What stays the same

- Fonts, sizes, colours, bold, italics, underline, highlights
- Paragraph styles, headings, and the heading levels
- Tables, including the rows, columns, and cell shading
- Bullet and numbered lists, and their numbering
- Links, images, charts, text boxes, page breaks, section breaks
- Headers, footers, page numbers, footnotes
- Comments and tracked changes that are already in the file
- Everything in the core rules list of protected content: names, numbers, dates, money, addresses, quotes, citations, legal terms, product names, tables of figures

Only the words inside paragraphs change. You never rebuild the document from scratch.

## Steps

1. **Tell the user what you are about to do** in one line if the file is long ("This is 14 pages, I'll go through it section by section"). Skip this for short files.
2. **Read the text with ids.** Run:
   ```
   python scripts/docx_rewrite.py extract <file>.docx -o segments.json
   ```
   Each paragraph comes back with an id (`p12`, `h1-1` for a header, `f1-1` for a footer) and where it sits (`body`, `table`, `header`, `footer`).
3. **Decide what to touch.** Rewrite body paragraphs and text in table cells that holds sentences. Leave alone:
   - Headings, unless they are clearly AI filler ("Harnessing the Power of Our Q3 Results")
   - Short labels in tables ("Region", "Total", "Q3")
   - Cells holding figures, and anything that looks like a table of numbers
   - Signatures, addresses, reference numbers, legal clauses
4. **Rewrite** following `ai-patterns.md`, the mode module, and any writing or adjust modules. Keep each paragraph as one paragraph. Do not merge or split paragraphs, because the ids map one to one. If a paragraph really should be cut, give it back with the smallest version that still makes sense, and mention it in the summary.
5. **Write only what changed** into a JSON file mapping id to new text, for example `{"p4": "...", "p9": "..."}`.
6. **Apply:**
   ```
   python scripts/docx_rewrite.py apply <file>.docx changes.json
   ```
   Add `--track-changes` if the user wants to see each edit in Word, or asked to approve changes (side by side mode). Word then shows every edit as a tracked change they can accept or reject.
7. **Read the script's CHECK lines.** A line like `p7: numbers differ` means a number moved or vanished. Go back and fix that paragraph unless the user asked for the change.
8. **Quick re-check.** Extract the new file and skim it once against `ai-patterns.md`. Then stop.

### Tracked changes on request

Offer tracked changes in one line when the document is going to someone else for review, such as a manager or a teacher: "Want me to show the edits as tracked changes so you can accept or reject each one in Word?"

### Explanations in the margin

When the user wants to know why each change was made ("explain each change in the margin", "add a note for every edit"), or the file goes to someone who will ask "why did you change this?", add `--comments`. Give each change a short reason in the changes file:

```json
{"p3": {"text": "The team worked hard.", "why": "Cut the filler opening."}}
```

Each changed paragraph then gets a margin comment by "WriteLikeHuman" with that reason, in plain words and without pattern numbers. Without a reason it says "Reworded for clarity." This works on its own or together with `--track-changes`. Offer it in one line for documents going to a reviewer, the same way as tracked changes.

### Comments in the file

If the document has reviewer comments, leave them. Do not rewrite comment text unless the user asks.

## Output

- Return `<original-name>-humanized.docx`. The script names it this way and refuses to overwrite the original.
- Then the plain change summary from `SKILL.md`. Mention anything you left alone on purpose that the user might expect you to change ("I left the table of sales figures exactly as it was").
- Do not paste the whole document back into the chat.

## Example

A paragraph in a work update, `team-update.docx`:

Before:
> In today's fast-paced business landscape, our team has **harnessed** state-of-the-art tools to deliver Rs 4,50,000 in sales by 12 March 2025, showcasing our unwavering commitment to excellence.

After:
> Our team used new tools to bring in Rs 4,50,000 in sales by 12 March 2025.

The bold stays on the word that replaced "harnessed". The amount and date are untouched. The file comes back as `team-update-humanized.docx`.

Summary line the user sees:
> - Cut the "fast-paced business landscape" opener and the line about commitment to excellence. They didn't add any information.

## If something goes wrong

- **The script will not run** (no Python, library missing, error): use Claude's built in docx skill if it is there, and edit paragraph by paragraph the same way. If neither works, give the user the rewritten text section by section, under the same headings, so they can paste it into their file. Say so in one line: "I couldn't edit the file directly, so here's the new text to paste in."
- **A paragraph comes out with odd formatting** (a whole sentence turned bold, for example): the new wording replaced a formatted word with a longer phrase. Rephrase so the formatted word stays, or keep the original wording for that part.
- **The file is a .doc (old Word format)** or a .odt: ask the user to save it as .docx and send it again, or work from pasted text.
- **The file is password protected**: ask for an unlocked copy. Do not try to get around the password.
- **The file is very long** (over about 30 pages): work through it in parts and tell the user which part you are on. Keep the same tone across parts.
