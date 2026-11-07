# Reading level

Make text easier to read for a particular reader: a child, an older relative, someone reading in their second language, or anyone in a hurry.

## When this applies

- "Make it simpler", "explain it like I'm 10", "for my mom", "for my grandfather", "my dad's English isn't great", "for new staff", "plain English".
- The user names a reader who will find the current text hard.

## What stays the same

- The facts, instructions, numbers, dates, and amounts. Simpler must not mean less accurate.
- Safety and money details. Never drop a warning, deadline, or fee to make it shorter.
- Names, product names, and legal terms. If a legal or medical term must stay, keep it and explain it in plain words right after.

## By reader

### Children

- Short sentences, about 8 to 12 words.
- Everyday words. Explain any new word with something they know.
- Concrete examples ("as heavy as a school bag").
- Talk to them, not down to them. No baby talk.

### Older readers

- Clear and respectful. Simple does not mean childish.
- Larger steps in order, one action per line, for instructions.
- Avoid app and internet slang ("DM", "swipe", "tap the hamburger").
- Spell out what buttons and screens are called, as they appear.
- If the user mentions eyesight, suggest a bigger font in the output file.

### Readers using English as a second language

- Common words, not idioms. "Let's touch base" becomes "Let's talk".
- One idea per sentence. Avoid long chains of "which" and "that".
- Avoid phrasal verbs where a single word works ("find out" can stay, "get across" becomes "explain").
- Keep the same word for the same thing. Do not switch between "invoice", "bill", and "statement" for variety.
- If the reader speaks Hindi, Tamil, or another language and the user asks, offer a translation too (see `languages/translate-humanize.md`).

### General plain English

- Lead with what the reader needs to do or know.
- Sentences under about 20 words on average.
- Active voice ("We will send the card" not "The card will be dispatched").

## Steps

1. Identify the reader. Ask in one line only if it really changes the result.
2. Find the hard parts: long sentences, rare words, jargon, idioms, passive voice.
3. Rewrite those parts. Leave plain parts alone.
4. Break dense paragraphs into short ones or numbered steps.
5. Check that nothing important was lost.

## Output

The simpler version, then a brief change summary. Note any technical word you kept and explained.

## Example

Before:

> Please be advised that your KYC documentation must be updated prior to 31 March, failing which your account may be subject to temporary suspension of debit transactions.

After (for an older parent):

> The bank needs your ID papers again (this is called KYC). Please give them before 31 March. If you don't, you may not be able to take money out of your account for a while.
