# Google Docs and Claude docs

## When this applies

The user shares a Google Docs link (`docs.google.com/document/...`), names a Google Doc in their Drive, or shares a Claude doc (a doc made inside Claude). Load the writing module for the kind of document too.

For Google Sheets use `files/spreadsheet.md`. For Google Slides use `files/slides.md`.

## What stays the same

- Headings, styles, fonts, bold, italics, links
- Tables, lists, numbering, images, page breaks
- Comments and suggestions other people left in the doc
- Who the doc is shared with, its title, and where it lives in Drive
- Everything protected by the core rules: names, numbers, dates, money, addresses, quotes, citations, legal terms, product names, tables of figures

## Steps

### 1. Check what you can reach

- **A Google Drive or Google Docs connector is available** (you can read and edit the user's Google files): you can work on the doc itself. Read the Google Workspace guidance or skill before your first edit, if it is there.
- **The doc is a Claude doc** and you have the docs tools: you can edit it directly.
- **Neither:** you cannot open the link. Ask the user to paste the text, or to download the doc as a Word file (**File > Download > Microsoft Word**) and attach it. Then use `files/word.md` for the Word file.

Never pretend you opened a link you could not open.

### 2. Never overwrite the user's doc without asking

Core rule 9 says the original stays safe. With a connector, the safe choices are, in order of preference:

1. **Make a copy** named `<original title> (humanized)` and edit the copy. This is the default.
2. **Suggest edits in the original** as suggestions, if the connector supports suggesting mode, so the user can accept or reject each one in Google Docs.
3. **Edit the original in place** only when the user clearly asks for it ("just fix it in my doc"). Mention that Google Docs keeps the old version under **File > Version history**, so they can go back.

Ask in one line if it is not clear which they want: "Should I make a copy, or edit your doc directly?"

### 3. Read and rewrite

1. Read the doc's text, section by section for long docs.
2. Rewrite following `ai-patterns.md`, the mode module, and any writing or adjust modules.
3. Change text paragraph by paragraph, replacing only the words. Do not delete and re-create whole sections, because that loses formatting, comments, and links.
4. Skip headings that are fine, short table labels, tables of figures, and anything protected.
5. Quick re-check once against `ai-patterns.md`. Then stop.

### 4. Without a connector: a clean copy to paste back

When the user pasted the text instead:

1. Rewrite it.
2. Give it back with the same headings and lists, in plain formatting that pastes cleanly into Google Docs (simple headings, bullets, no tables drawn with characters).
3. Tell them how to paste it in one line: "Select the old text in your doc and paste this over it. Your headings will carry over."

If only part of a long doc needs work, return only the changed paragraphs, each under the heading it belongs to, so the user knows where it goes.

## Output

- **With a connector:** a link to the edited copy (or a note that the suggestions are in the original), then the change summary.
- **Without a connector:** the rewritten text ready to paste, then the change summary.
- Do not paste the whole doc back into the chat if you edited it directly.

## Example

A paragraph from a shared Google Doc, "Team offsite plan":

Before:
> We are thrilled to announce that this year's offsite will be a transformative journey that fosters collaboration, creativity, and connection. The offsite will take place on 18 and 19 April at Green Valley Resort, Lonavala.

After (in "Team offsite plan (humanized)"):
> This year's offsite is on 18 and 19 April at Green Valley Resort, Lonavala. The plan is to get everyone out of the office for two days and spend real time together.

Change summary:
> - Made a copy called "Team offsite plan (humanized)" so your original is untouched.
> - Moved the dates and place to the first line, since that's what people look for.
> - Cut "transformative journey" and the list of three buzzwords.

## If something goes wrong

- **The connector can read but not edit:** give the user a clean copy to paste back, as in step 4.
- **The link needs permission you don't have** ("You need access"): ask the user to paste the text or download it as Word. Do not ask them to make the doc public.
- **An edit messes up formatting** (a heading turns into normal text): undo that one edit if the tool allows it, and tell the user. Otherwise point them to **File > Version history**.
- **The doc is very long:** ask which section to start with, or work through it in parts and say which part you are on.
