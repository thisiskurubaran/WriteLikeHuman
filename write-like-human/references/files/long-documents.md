# Long documents

## When this applies

The user gives a long document: a thesis, a dissertation, a 100-page report, a manual, a policy handbook, a book chapter, a long PDF. Roughly anything over 30 pages or 10,000 words, or anything that would not fit comfortably in one pass.

Load this together with the file module for the format (`files/word.md`, `files/pdf.md`, `files/latex.md`, `files/text.md`) and the writing module for the kind of document (`writing/report.md`, `writing/essays.md`). For a thesis or graded work, the honest-use rules in `writing/report.md` apply: improve the student's own draft, chapter by chapter.

## What stays the same

- Every section, paragraph, table, figure, and footnote. Nothing is summarised, shortened, or dropped unless the user asks for that.
- The order of sections and the heading structure.
- Names, numbers, dates, citations, quotes, technical terms, and anything in a table of figures.
- One voice from the first page to the last. Section 9 must sound like section 1.
- All the core rules in SKILL.md, for every section.

## Steps

1. **Outline first.** Run `python scripts/doc_sections.py outline FILE`. It lists the sections in order with ids (s1, s2, ...), headings, word counts, and where each one sits: paragraph ids for Word files (the same ids `docx_rewrite.py` uses), line numbers for LaTeX and text, page numbers for PDF. LaTeX sections follow `\chapter`, `\section`, and `\subsection`. Without headings, it splits the file into parts of about 2,500 words at paragraph or page breaks.
2. **Agree the plan** for very long files. Tell the user in two or three lines how many sections there are and how you will go through them, and ask if they want everything or only some chapters. For a shorter long document, just start.
3. **Build a consistency sheet.** Run `python scripts/doc_sections.py terms FILE`. It lists names and capitalised terms that repeat, and spellings used two ways in the same file ("colour" and "color", "e-mail" and "email"). Decide each one with the user's existing choice in mind, using `adjust/consistency.md`. Keep the sheet in your working notes: the names, the terms, the spelling style, the date and number style, how the document refers to itself ("this report", "this study"), and any tone decisions.
4. **Work section by section.** For a Word file, run `docx_rewrite.py extract`, then rewrite only the paragraphs in the current section's id range, and keep the changes for that section. For LaTeX, run `latex_rewrite.py extract` and take the pieces whose line falls in the section's line range. Check each section against the consistency sheet before moving on. Add new decisions to the sheet as they come up.
5. **Report progress** in one short line as you go: "Sections 1 to 4 of 12 done. Same tone and terms kept." Don't paste the rewritten text back unless the user asks.
6. **Apply once.** Combine the changes from every section into one changes file and run `docx_rewrite.py apply` (or `latex_rewrite.py apply`) once, so there is a single final file. For PDF, build one Word file as `files/pdf.md` describes. For text, write one new file.
7. **Final check.** Skim the start of three sections far apart (first, middle, last) for tone, and spot-check the consistency sheet terms across the whole file. Then stop.

## Output

- One file: `<original-name>-humanized.<ext>` (a `.docx` for PDF input). The original is never overwritten.
- A change summary that covers the whole document, not each section: three to six plain bullets, plus one line with the decisions from the consistency sheet ("Kept British spelling throughout, 'Northbay Project' always in full").
- If the user asked for only some chapters, say which ones were done.

## Example

User: "Make my 140-page thesis read more naturally. Same structure please." (attaches thesis.docx)

You run the outline, find 9 chapters, and reply:

> Your thesis has 9 chapters and about 42,000 words. I'll go through them in order and keep your British spelling and terms the same throughout. I'll send one finished file at the end.

Along the way: "Chapters 1 to 3 done." At the end, `thesis-humanized.docx` and:

```
What I changed
- Cut repeated openers like "It is important to note that" across all chapters.
- Split long sentences in the literature review and methods.
- Kept every citation, figure number, and table exactly as it was.
- Used "the Northbay Project" in full everywhere, as in your introduction.
```

## If something goes wrong

- **The outline script fails** or the file has no usable headings: work through it page by page or in chunks of about 2,500 words, and number the parts yourself so you can report progress.
- **You run out of room partway through**: say plainly which section you reached, deliver what is done as a file, and offer to continue from the next section. Never quietly skip sections or summarise to fit.
- **Different sections use different spellings or names on purpose** (quoted sources, a chapter written by a co-author): keep them and mention it in the summary instead of forcing one style.
- **The document is a scanned PDF**: follow the scanned pages steps in `files/pdf.md`, and confirm names and numbers with the user before the final file.
