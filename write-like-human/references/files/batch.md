# Several files at once

## When this applies

The user sends more than one file and wants them all done: "fix all 5 cover letters", "humanize these three reports", "clean up the speaker notes in both decks". The files can be the same type or mixed.

Load the file module for each type (for example `files/word.md` and `files/pdf.md`) and the writing module for the kind of writing.

## What stays the same

- Each file's own facts. Details never move from one file to another. The company name in cover letter 2 must not appear in cover letter 4. The dates in report A must not end up in report B. This is the main risk with batches, so check for it.
- Each file's own tone and formality, unless the user asks for one tone across all of them.
- Everything the single-file modules protect: layout, formulas, timings, and the protected content in the core rules.
- The originals. Every file gets its own new copy.

## Steps

1. List the files back to the user in one short line if there are more than five, or if it is not clear which ones they mean: "I'll do these 7: cover-letter-acme.docx, cover-letter-brightlane.docx, ... OK?" For five or fewer clear files, just start.
2. Ask once about anything that applies to all of them (for example, the same tone), not file by file.
3. Do one file at a time, start to finish, following its own module. Do not hold several files' text in mind and rewrite them together.
4. After each file, check its names, numbers, and dates against its own original only.
5. When the files are similar (several cover letters), avoid giving them all the same new sentences. Each should still read as written for its own reader.
6. After the last file, do a quick pass across all the outputs for details that leaked between files.

## Output

- One new file per input, each named `<original-name>-humanized.<ext>`.
- A short summary per file, two or three bullets each, under the file name.
- One overall line at the end, such as "Did all 5. The Brightlane letter needed the most work, the others were small fixes."
- If one file failed, say which and why in one line, and still return the others.

Example layout:

```
cover-letter-acme-humanized.docx
- Cut the opening line about being "thrilled to apply".
- Swapped "results-driven team player" for the project you described.

cover-letter-brightlane-humanized.docx
- Shortened the second paragraph, which repeated your resume.

Did both. Names, dates, and company details stayed with their own letters.
```

## Example

Before, from two cover letters in the same batch:

> Letter 1 (Acme Foods): "I am excited to harness my skills to drive impactful outcomes at your esteemed organization."
>
> Letter 2 (Brightlane): "I am excited to harness my skills to drive impactful outcomes at your esteemed organization."

After:

> Letter 1: "I'd like to bring my four years of food safety audits to Acme's quality team."
>
> Letter 2: "Your delivery app is something I use every week, and I'd like to help design it."

Each sentence uses only details from its own letter or from what the user said about that job. If a letter has no details to work with, ask, rather than borrowing from another one.

## If something goes wrong

- **Too many files for one reply**: do them in groups, say how many are left, and keep going when the user says so.
- **One file will not open**: return the others and explain the one that failed.
- **Files are near copies of each other**: ask whether they want the same changes in all, which is faster and keeps them consistent.
- **The user says "same as before" for a new batch**: reuse the tone and choices from the earlier batch, and say so in one line.
