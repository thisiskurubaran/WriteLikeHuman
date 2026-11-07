# OpenDocument and RTF files (.odt, .rtf)

## When this applies

The user attaches an `.odt` file (from LibreOffice Writer, OpenOffice, or some school and government computers) or an `.rtf` file (from WordPad or older software). Load the writing module for the kind of document too.

For `.docx` files, use `files/word.md` instead.

## What stays the same

- The words that are protected by the core rules: names, numbers, dates, money, addresses, quotes, citations, legal terms, product names, tables of figures.
- As much of the layout as the route below allows: headings, paragraphs, lists, tables, bold and italics.

Be honest about the format. These files cannot always be edited directly here, so the user may get a Word file back. Say which format they are getting before or with the result, never after they find out.

## Steps

1. Check whether LibreOffice is available (it is in some environments, not all):
   ```
   soffice --version
   ```
2. **If LibreOffice is there**, convert to Word, edit, and convert back:
   ```
   soffice --headless --convert-to docx --outdir work <file>.odt
   python scripts/docx_rewrite.py extract work/<file>.docx -o segments.json
   python scripts/docx_rewrite.py apply work/<file>.docx changes.json
   soffice --headless --convert-to odt --outdir out work/<file>-humanized.docx
   ```
   Follow the steps in `files/word.md` for what to rewrite and what to leave alone. Return `<file>-humanized.odt`. For an `.rtf` file, convert back with `--convert-to rtf` the same way. Mention in one line that the file went through a conversion, so the user should glance at the layout.
3. **If LibreOffice is not there**:
   - For `.odt`: the file is a zip with the text in `content.xml`. Read the paragraphs (the `text:p` and `text:h` elements) to get the text.
   - For `.rtf`: strip the control words to get plain text. A short Python script with the standard library is enough: remove `{\*...}` groups, drop control words like `\par` (turn `\par` into a line break) and `\b`, and decode `\'xx` and `\uN` characters.
   - Rewrite the text, then write it into a new Word file with `python-docx`, keeping headings and paragraphs in order.
   - Return `<file>-humanized.docx` and tell the user plainly: "I couldn't edit the .odt directly here, so this is a Word file with the new text. LibreOffice opens it fine, and you can save it as .odt from there."
4. Check protected content against the original.

## Output

- `<original-name>-humanized.odt` or `.rtf` when LibreOffice was available, otherwise `<original-name>-humanized.docx`.
- One line saying which format they got and why, then the plain change summary from `SKILL.md`.
- Never overwrite the original.

## Example

A paragraph in `society-notice.odt`, before:

> It is hereby brought to the kind notice of all esteemed residents that the water supply shall remain suspended on 9 June from 10 am to 2 pm owing to essential maintenance activities.

After:

> Water supply will be off on 9 June from 10 am to 2 pm for maintenance.

The date and times are unchanged. If LibreOffice was not available, the user gets `society-notice-humanized.docx` with a one line note explaining why.

## If something goes wrong

- **The conversion fails or the layout comes back broken**: fall back to step 3 and return a Word file, or give the rewritten text section by section for the user to paste into their own file.
- **The file is password protected**: ask for an unlocked copy.
- **The .rtf is mostly images or tables of figures**: rewrite only the sentences, and tell the user which parts you left alone.
- **The user needs the exact original format for an office or portal**: suggest they open the Word file in LibreOffice and use Save As, which keeps the format they need.
