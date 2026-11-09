# PDFs (.pdf)

## When this applies

The user attaches a `.pdf`: a letter, a report, a resume someone exported, a school assignment, a form. Load the writing module for the kind of document as well.

A PDF is a print-ready file. It cannot be reliably edited in place, so you never claim to have edited the PDF. You read the text, rewrite it, and hand back an **editable Word file** (or a Google Doc or Claude doc if that is what the user works in). Say this plainly at the start, in one line:

> PDFs can't be edited directly, so I'll give you the improved text as a Word file you can edit and save as PDF again.

## What stays the same

- The order of sections and paragraphs
- Headings and their levels, bullet lists and numbered lists
- Every protected item from the core rules: names, numbers, dates, money, addresses, quotes, citations, legal terms, product names
- Tables of figures: copy them across exactly, or leave them out with a note if they can't be rebuilt cleanly

What cannot be kept: the exact page layout, fonts, colours, logos, and images of the original PDF. Tell the user that in the change summary, so they are not surprised. If the look matters (a designed brochure, a certificate), suggest they edit the original source file if they have it, such as the Word or Canva file the PDF came from.

## Steps

1. **Read the text page by page:**
   ```
   python scripts/pdf_extract.py extract <file>.pdf -o pages.json
   ```
   Each page comes back with its text, a word count, and `"scanned": true` if the page looks like a photo or scan with no real text.
2. **Handle scanned pages.** If `scanned_pages` is not empty:
   - Get the picture of each scanned page:
     ```
     python scripts/pdf_extract.py images <file>.pdf --pages 2,3 --out page-images
     ```
     It saves the image inside each page and prints the paths. Open those images and read them yourself, then type out the text carefully. If you can already see the PDF pages directly, you can read them without the script.
   - If the script says a page has no picture inside it, ask the user for a photo or screenshot of that page.
   - Tell the user which pages were scanned and that you read them from the image. Before the final file, list the names, numbers, and dates you read from those pages and ask the user to confirm them.
   - If the image is too blurry to read with confidence, say which page and ask for a clearer copy or the text itself. Never guess at a name, number, or date.
3. **Fix the layout breaks.** PDF text often comes out with lines broken mid-sentence, words split by hyphens, page numbers and running headers mixed in. The script joins broken lines, rejoins hyphenated words, and keeps greetings, sign-offs, list items, and real paragraph breaks on their own. Remove repeated headers, footers, and page numbers, then check the paragraph breaks against the original and fix any it missed.
4. **Mark structure** in the page text so the Word file comes out right: `# ` for a main heading, `## ` for a subheading, `- ` for a bullet, a blank line between paragraphs.
5. **Rewrite** following `ai-patterns.md`, the mode module, and any writing or adjust modules.
6. **Build the Word file** from the edited JSON:
   ```
   python scripts/pdf_extract.py to-docx <file>.pdf pages-rewritten.json
   ```
   This saves `<file>-humanized.docx` with each PDF page starting on a new page. Add `--no-page-breaks` for letters and short documents, where page breaks would look odd.
7. **Quick re-check** of the result against `ai-patterns.md`. Then stop.

If the user works in Google Docs or Claude docs, offer to put the text there instead of a Word file (see `files/google-docs.md`).

### Forms

If the PDF is a form to fill in (a visa form, an application), do not fill fields with made up answers. Help the user word the answers they give you, following `writing/form-answers.md`, and tell them to type the final answers into the form themselves.

## Output

- Return `<original-name>-humanized.docx`. Never say the PDF was changed.
- Then the plain change summary. Always include one line about the format:
  > - Gave it back as a Word file so you can edit it. The original PDF's fonts and layout aren't copied over.
- Mention any scanned pages you read from the image.

## Example

A page from `refund-request.pdf`, as it comes out of the PDF:

Before:
> Dear Mr Sharma, I am writing to bring to your kind attention the matter of my refund of Rs 2,499 for order 55821, placed on 3 Feb-
> ruary 2025. I would be most grateful if you could kindly look into this matter at your earliest convenience.

After (in `refund-request-humanized.docx`):
> Dear Mr Sharma,
>
> I'm writing about my refund of Rs 2,499 for order 55821, placed on 3 February 2025. Could you please look into it and let me know when I can expect it?

The amount, order number, and date are unchanged. The broken word "Feb-ruary" is joined.

## If something goes wrong

- **The script fails or pypdf is missing:** use Claude's built in PDF reading or the pdf skill to get the text, then do the same rewrite. To make the Word file, use the docx skill. If there is no way to make a file, give the rewritten text in the chat under the same headings, ready to paste.
- **Every page is flagged as scanned:** the whole PDF is a scan. Read it from the images if you can. If not, ask the user to send a photo of each page or the text itself.
- **The PDF is password protected:** ask for an unlocked copy. Do not try to get around the password.
- **The text comes out jumbled** (columns mixed together, often in newsletters or two column papers): rebuild the reading order by meaning, and tell the user to check the order in the result. If it is too mixed up to rebuild safely, ask for the original file.
- **The PDF is huge** (over about 40 pages): ask which part they want first, or work through it in parts and say which part you are on.
