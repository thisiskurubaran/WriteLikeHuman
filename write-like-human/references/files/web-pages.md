# Web pages (.html)

## When this applies

The user attaches an `.html` file, usually a page from a small business or personal website: a home page, an About page, a services page, a menu. They want the words to sound more natural without breaking the page.

If they paste a few lines of website text into the chat, you do not need this module. Work on the pasted text. If they send a link to a live website, explain that you can rewrite the text if they paste it or send the page file, since you can't change their website yourself.

## What stays the same

- Every tag and attribute: classes, ids, styles, `href` links, image paths, `alt` text and meta descriptions (unless the user asks you to improve them, see below), form fields, and other meta tags.
- Everything inside `<script>`, `<style>`, `<code>`, `<pre>`, `<textarea>`, and `<template>`.
- Comments and the spacing between tags.
- Button and menu labels keep about the same length, so the layout doesn't break.
- Everything in the core rules list of protected content: names, numbers, prices, phone numbers, addresses, opening hours, product names.

## Steps

1. Run the script to list the visible text:

   `python scripts/html_rewrite.py extract <file>.html -o nodes.json`

   Each piece of text gets an id (`t1`, `t2`, ...) and the tag it sits in (`h1`, `p`, `a`, `button`).
2. Read the pieces in order first, so you follow the page. A sentence is often split across several pieces by a link or bold word: `We bake` / `fresh bread` / `every day.` Rewrite them so the sentence still reads well when joined, and keep the link on the same words or close to them.
3. Rewrite following `ai-patterns.md` and the mode module. Website copy is often full of sales language ("unparalleled", "world-class", "take your experience to the next level"); replace it with plain, specific words the owner already gave.
4. Keep headings short, button labels short, and menu items as they are unless asked.
5. Write the changes as JSON, `{"t3": "new text", ...}`, and apply them:

   `python scripts/html_rewrite.py apply <file>.html changes.json`

   It saves `<file>-humanized.html` and never touches the original.
6. Read any `CHECK` lines. They mean a number changed in that piece. Put it back unless the user asked for the change.

## Image descriptions and meta descriptions

Only when the user asks, or as part of an accessibility pass (see `adjust/accessibility.md`), add `--attributes` to extract:

`python scripts/html_rewrite.py extract <file>.html --attributes -o nodes.json`

This also lists `alt`, `title`, `placeholder`, and `aria-label` text, plus the page's meta description (including og:description and twitter:description), with ids like `attr-3`. Their `tag` shows where they sit, for example `img@alt`. apply updates them in place and keeps each value's quotes. Good alt text says what the image shows in a few plain words ("Two loaves of bread on a wooden table"), not "image of" or a sales line. Keep meta descriptions under about 155 characters so search results don't cut them off.

## Output

- `<original-name>-humanized.html`, ready to upload in place of the old page (after the user checks it).
- One line suggesting they open it in a browser to check it before uploading.
- Then the plain change summary from `SKILL.md`.

## Example

Before:

```html
<h1>Welcome to Sunrise Bakery!</h1>
<p>We are thrilled to offer an unparalleled selection of <a href="/menu">artisanal delights</a> crafted with passion.</p>
```

After:

```html
<h1>Welcome to Sunrise Bakery</h1>
<p>We bake bread, cakes, and biscuits every morning. See <a href="/menu">today's menu</a>.</p>
```

Only use details like "every morning" if the owner's page or message says so. The link address, the tags, and the page layout stay exactly as they were.

## If something goes wrong

- **The script fails or the file won't parse**: rewrite the text by hand. Copy the file and change only the words between tags, never anything inside `< >`. Tell the user in one line that you edited it by hand and they should check it in a browser.
- **The page is built by a website builder** (Wix, Squarespace, WordPress page builders): the downloaded file may not be what the site uses. Suggest they paste the text from each section instead, and give it back section by section to paste into the builder.
- **The page is mostly JavaScript and has almost no visible text in the file**: the text is loaded some other way. Ask the user to copy the text from the live page.
- **Text sits in attributes the user wants changed** (like `alt` or `title`): run extract with `--attributes` (see below). For any other attribute, edit by hand, carefully, only if asked.
