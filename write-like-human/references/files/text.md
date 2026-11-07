# Plain text and Markdown files (.txt, .md)

## When this applies

The user attaches a `.txt` or `.md` file: notes from a phone app, a blog draft, a README for a small project, a letter saved as plain text, an export from Notion, Obsidian, Google Keep, or Apple Notes.

If they paste the text into the chat instead, you do not need this module. Work on the pasted text.

## What stays the same

- The file type. A `.txt` comes back as `.txt`, a `.md` as `.md`.
- Line breaks and blank lines between paragraphs. Some people hard wrap their notes at a fixed width; keep that style if the file uses it.
- In Markdown:
  - Heading markers (`#`, `##`), list markers (`-`, `*`, `1.`), and how lists are nested
  - Links: the link text may change if it is AI filler, but the address in `( )` never changes
  - Images (`![alt](path)`): keep the path, and only touch the alt text if the user asks
  - Code blocks and inline code in backticks: never change anything inside them
  - Tables: keep the pipes and the header row; only rewrite sentences inside cells
  - Front matter at the top between `---` lines: never change it
  - HTML tags, footnote markers, and checkboxes (`- [ ]`, `- [x]`)
- Everything in the core rules list of protected content: names, numbers, dates, money, addresses, quotes, citations, legal terms, product names

## Steps

1. Read the file. For a long file, tell the user in one line that you will go section by section.
2. Mark what not to touch: front matter, code blocks, inline code, link addresses, image paths, and HTML.
3. Rewrite the prose following `ai-patterns.md`, the mode module, and any writing or adjust modules. Work paragraph by paragraph so the structure stays in place.
4. Keep Markdown markers where they were. A bullet stays a bullet. If the original has a bold label on every bullet (`**Speed:** ...`), you may remove the bold labels, since that is a common AI tell, but keep the list.
5. Check protected content and every link address against the original.
6. Save a new file with the same encoding (UTF-8 unless the file is clearly something else) and the same line endings.

## Output

- Return `<original-name>-humanized.txt` or `<original-name>-humanized.md`. Never overwrite the original.
- Then the plain change summary from `SKILL.md`.
- If you can create files, attach the new file. If you cannot (some mobile chats), give the new text in a single code block so it copies cleanly, and say so in one line.

## Example

`trip-notes.md`, before:

```
## Day 2: Munnar

We embarked on a breathtaking journey through the lush tea gardens, immersing ourselves in the rich mosaic of local culture. See [our route](https://example.com/route).
```

After:

```
## Day 2: Munnar

We walked through the tea gardens and stopped at a small shop run by a family who has grown tea there for three generations. See [our route](https://example.com/route).
```

Only use details like the family shop if the user's notes mention them. Without them, the line becomes "We walked through the tea gardens." The heading, the link, and the address stay exactly as they were.

## If something goes wrong

- **The text looks garbled** (odd symbols, broken accents): the file may not be UTF-8. Ask the user to save it again as UTF-8, or to paste the text instead.
- **You cannot create a file**: give the rewritten text in one code block and tell the user to paste it over the old text and save.
- **The file is a .md export with lots of tool syntax** (Notion callouts, Obsidian `[[links]]`, Dataview queries): leave anything you do not recognize exactly as it is.
- **The file is very long**: work in parts and keep the same tone across parts.
