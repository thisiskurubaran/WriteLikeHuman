# LaTeX documents (.tex)

## When this applies

The user gives a `.tex` file: a thesis, a paper, a report, a CV, or lecture notes written in LaTeX, and wants the writing to read more naturally. Load the writing module for the kind of document too (`writing/report.md` or `writing/essays.md`, and `files/long-documents.md` for a long thesis).

If they paste only a paragraph of plain text, work on that text instead.

## What stays the same

- Every command, environment, and argument that isn't prose: `\section`, `\cite{...}`, `\ref{...}`, `\label{...}`, `\includegraphics`, `\url`, the link in `\href`, packages, and the whole preamble.
- All maths: `$...$`, `$$...$$`, `\(...\)`, `\[...\]`, and environments such as equation, align, and gather.
- Comments (`% ...`), verbatim and code listings, tikz drawings, and table separators (`&` and `\\`).
- Citations and their keys, figure and table numbers, and cross-references.
- The file's spacing and line breaks outside the text you change.
- For graded or published work, the honest-use rules in `writing/report.md` and `writing/essays.md`: improve the author's own draft.

## Steps

1. Run `python scripts/latex_rewrite.py extract FILE.tex`. It lists the prose pieces with ids (t1, t2, ...) and the line each starts on. Text inside commands like `\emph{...}`, `\section{...}`, `\caption{...}`, and `\footnote{...}` comes out as its own piece.
2. Rewrite only the pieces that need it, following `ai-patterns.md` and the writing module. A piece is often part of a sentence, cut where a citation or maths sits. Rewrite it so the full sentence still reads well with the citation or formula in its place.
3. Never add a backslash, brace, or LaTeX special character (`% $ & # ^ _`) in your new text. Escaped characters already in the text (`\%`, `\&`) may stay. If a change truly needs new LaTeX (an emphasis, a new citation), tell the user instead of adding it.
4. Save the changes as JSON (`{"t2": "new text", ...}`) and run `python scripts/latex_rewrite.py apply FILE.tex changes.json`. It writes `<name>-humanized.tex`, keeps every other byte the same, and skips any change with LaTeX characters, saying which. A `CHECK` line means a number changed: make sure that was intended.
5. Read the changed sentences once in context (the lines around each change) to make sure they still join up with the citations and maths.

## Output

- `<original-name>-humanized.tex`. The original is never overwritten. The user compiles it as usual.
- A short change summary in plain words. Mention that commands, maths, citations, and labels were left exactly as they were.

## Example

Before (in thesis.tex):

```latex
It is important to note that our approach significantly outperforms prior work \cite{lee2021}, as shown in Table~\ref{tab:results}.
```

After:

```latex
Our approach does better than earlier work \cite{lee2021}, as Table~\ref{tab:results} shows.
```

What I changed
- Cut "It is important to note that".
- Replaced "significantly outperforms prior work" with a plainer phrase.
- Left the citation, the table reference, and the non-breaking space exactly as they were.

## If something goes wrong

- **The script fails** or the file uses unusual custom commands: work from the prose pieces by hand. Copy each sentence, change only the words between commands, and give the user the edited lines with their line numbers to paste in.
- **A piece is cut mid-sentence** in an awkward place (around a custom macro): leave that piece alone, or rewrite the whole sentence and give it to the user to place by hand.
- **The document is split across files** (`\input{chapter1}`): ask for the chapter files and process each one, keeping one consistency sheet as in `files/long-documents.md`.
- **The compiled PDF looks wrong afterwards**: the change most likely touched something it shouldn't. Compare with the original using the `CHECK` and `SKIPPED` lines, and undo that change.
