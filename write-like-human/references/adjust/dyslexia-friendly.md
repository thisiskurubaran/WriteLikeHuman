# Dyslexia-friendly layout

An optional layout pass that makes a document easier to read for people with dyslexia and other reading differences. It changes how the text looks, not what it says.

## When this applies

- "Make this dyslexia friendly", "easier to read for my dyslexic son", "readable layout", "for a reader with dyslexia".
- School handouts, worksheets, work documents, letters, and notices.
- Only when asked. Never apply this to a document the user didn't ask to reformat.

## What stays the same

- Every word, unless the user also asks for a rewrite (then also use rewrite mode, and `adjust/reading-level.md` or `adjust/easy-read.md` if they ask for simpler words).
- Headings, lists, tables, images, page breaks, and numbering. The structure stays, only its look changes.
- Names, numbers, and dates, of course.

## The layout

- A clear sans-serif font: Arial, Verdana, Calibri, or similar.
- Size 12 to 14 pt for body text, larger for headings.
- Line spacing of 1.5.
- Left aligned, never justified (justified text makes uneven gaps between words).
- No long runs of italics, underlining, or ALL CAPS. Underline only links.
- Bold for emphasis, used sparingly.
- Short paragraphs with space between them.
- Plain backgrounds. If the user wants a tint, a soft cream or pale yellow page is easier for some readers than bright white, but ask first.

## Steps

1. Confirm whether the user wants layout only, or a rewrite too.
2. For a Word file, run `python scripts/docx_layout.py FILE --dyslexia`. It writes `<name>-readable.docx` (or the name given with `-o`) and leaves the original untouched.
3. If the script fails or isn't available, give the user the settings to apply in Word in one short list: Home > Font (Arial, 12 pt), Paragraph > Line spacing 1.5, Align left, and remove italics from long passages.
4. For pasted text, break long paragraphs into shorter ones and use headings or a list where the original was a wall of text. Don't change the words.
5. Check that nothing was lost: same headings, same lists, same tables.

## Output

- Word file: `<name>-readable.docx`, then a short note listing what changed in the layout.
- Pasted text: the same text with shorter paragraphs and clearer breaks, plus the font and spacing settings to use wherever they paste it.

## Example

Before (a school notice in Times New Roman 10 pt, justified, with the whole second paragraph in italics):

> *All students must submit their science project files by Friday 20 November. Late submissions will not be accepted without a note from a parent.*

After (Arial 12 pt, 1.5 spacing, left aligned):

> All students must submit their science project files by **Friday 20 November**.
>
> Late submissions will not be accepted without a note from a parent.

What I changed
- Switched to Arial 12 pt with 1.5 line spacing and left alignment.
- Removed the italics from the whole paragraph and put the deadline in bold instead.
- Split it into two short paragraphs. The words are the same.
