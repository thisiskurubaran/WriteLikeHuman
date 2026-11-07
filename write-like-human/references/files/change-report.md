# Change report (a Word file showing every change)

## When this applies

- The user wants to see exactly what changed, in a file they can keep, print, or send: "give me a file that shows the changes", "mark up what you changed", "I need to show my manager what was edited".
- The input was anything: pasted text, a PDF, a Google Doc, a Markdown file. For Word files, real tracked changes (see `files/word.md`) are usually better, because the user can accept or reject each edit in Word. Offer that first for Word files.
- Side by side mode, when the user would rather review on paper or in Word than in the chat.

## What stays the same

- Nothing in the user's text changes because of this module. The report only shows the difference between the original and the rewritten version.
- The rewritten version follows all the usual rules: protected content, length, tone.

## Steps

1. Do the rewrite first, following the mode and the file or writing module.
2. Save the original text and the new text as files. Plain `.txt` is fine. Use blank lines between paragraphs. If the original was a Word file, you can use the `.docx` files directly.
3. Make the report:
   ```
   python scripts/change_report.py before.txt after.txt -o <name>-changes.docx
   ```
   Removed words show in red with a line through them. Added words show in green and underlined. Unchanged text is plain. A short note at the top explains the colours.
4. Open nothing else and change nothing else. The script refuses to write over either input.

## Output

- `<original-name>-changes.docx`, the report.
- Usually also the clean rewritten version (`<original-name>-humanized.<ext>`), so the user has both: one to read the changes, one to use.
- One line telling them which file is which: "The -changes file shows every edit in colour. The -humanized file is the clean version to use."
- The plain change summary from `SKILL.md`.

## Example

Original paragraph:

> We utilized a comprehensive approach to ensure smooth delivery of all 240 orders.

Rewritten:

> We changed how we packed and tracked orders, and all 240 went out on time.

In `orders-changes.docx`, "utilized a comprehensive approach to ensure smooth delivery of" appears in red with a line through it, "changed how we packed and tracked orders, and" and "went out on time" appear in green and underlined, and "We", "all 240", and the full stop stay plain. The number 240 is unchanged.

## If something goes wrong

- **The script will not run**: give the changes in the chat as a numbered before and after list (as in `modes/side-by-side.md`), and say you could not make the file.
- **Paragraphs were split or merged in the rewrite**: the report still works, but it shows whole paragraphs as removed and added. That is fine, and you can mention it.
- **The user wants accept or reject buttons**: that needs a Word file with tracked changes. Use `files/word.md` with `--track-changes`, starting from the original as a .docx.
- **The document is very long**: the report can be long too. Offer it section by section if that is easier to review.
