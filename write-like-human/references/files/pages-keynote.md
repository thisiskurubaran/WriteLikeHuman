# Apple Pages and Keynote files (.pages, .key)

## When this applies

The user attaches a `.pages` document or a `.key` presentation, usually made on a Mac, iPhone, or iPad. Common ones: a school assignment, a club newsletter, a talk for an event, a resume someone made in a Pages template.

## What stays the same

- The words that are not being improved, and everything in the core rules list of protected content: names, numbers, dates, money, addresses, quotes, citations, legal terms, product names.
- Headings, lists, tables, images, and slide layout, as far as the conversion allows.
- The original file. You never change it.

Be honest about the format. Pages and Keynote files are Apple's own format, and you cannot edit them directly. What the user gets back is a Word file (`.docx`) or a PowerPoint file (`.pptx`). Both open in Pages and Keynote again.

## Steps

1. Tell the user in one line: "I can't edit Pages or Keynote files directly, so I'll give you back a Word (or PowerPoint) file. It opens fine in Pages (or Keynote)."
2. Check whether LibreOffice is available by running `soffice --version`.
3. If it is, convert a copy:
   - Pages: `soffice --headless --convert-to docx --outdir <folder> <file>.pages`
   - Keynote: `soffice --headless --convert-to pptx --outdir <folder> <file>.key`
4. Open the converted copy and check it looks right: the text is all there, headings and lists made it, slides have their text boxes. Newer Pages and Keynote files sometimes convert badly or not at all. If the result is empty or garbled, go to step 6.
5. If the conversion worked, follow `files/word.md` for a Word file or `files/slides.md` for a PowerPoint file, including their scripts.
6. If LibreOffice is missing or the conversion failed, ask the user to export the file themselves. Give these steps:
   - On a Mac: open the file, click **File**, then **Export To**, then **Word** (or **PowerPoint** for Keynote). Click **Next**, then **Export**, and send me the new file.
   - On an iPhone or iPad: open the file, tap the **...** (More) button, tap **Export**, choose **Word** (or **PowerPoint**), then share the file here.
7. Once you have a Word or PowerPoint file, continue with step 5.

## Output

- `<original-name>-humanized.docx` for Pages, or `<original-name>-humanized.pptx` for Keynote.
- One line saying the user can open it in Pages or Keynote, and that some special Apple fonts or effects may look a little different.
- Then the plain change summary from `SKILL.md`.

## Example

The user sends `club-update.pages` and says "make this sound less stiff".

You reply: "I can't edit Pages files directly, so here's a Word copy. It opens fine in Pages."

Before (one paragraph inside the file):

> We are delighted to announce that the annual sports day will be held on 18 January. Participation is highly encouraged for all members.

After:

> Sports day is on 18 January this year. We'd love to see everyone there.

The date, the heading above it, and the club logo stay as they were.

## If something goes wrong

- **The converted file is blank or missing text**: newer Pages files often don't convert. Ask the user to export to Word or PowerPoint with the steps above.
- **The user is on a phone and can't find Export**: ask them to copy the text and paste it into the chat. Return the rewritten text to paste back.
- **Fonts or slide animations look different after conversion**: tell the user plainly. The words are what changed; they can reapply a font in Pages or Keynote in a few clicks.
- **The file is very large or has many images**: ask for an export without images, or work section by section on pasted text.
