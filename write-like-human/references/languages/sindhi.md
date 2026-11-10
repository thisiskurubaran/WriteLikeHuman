# Sindhi

Rewrite Sindhi so it sounds like a person wrote it, in the script and register the user chose.

## When this applies

- The text is in Sindhi, in the Arabic-based Sindhi script (common in Pakistan) or in Devanagari (used by many Sindhi speakers in India).
- The user asks for a translation into Sindhi (also load `translate-humanize.md`). Ask which script they want if it is not clear.
- For Sindhi mixed with English, Urdu, or Hindi, also load `mixed-language.md`.

## What stays the same

- Language and script. Sindhi stays Sindhi. Arabic-based script stays in that script, Devanagari stays Devanagari. Never switch scripts and never translate unless asked.
- The extra Sindhi letters. Sindhi has sounds and letters that Urdu and Hindi do not (such as ٻ, ڄ, ڳ, ڏ in the Arabic-based script). Keep them. Do not replace them with the nearest Urdu or Hindi letter.
- Register. Keep "اوهان" (you, polite) where the user uses it, and the familiar form where they use that.
- Names, numbers, dates, amounts, and places. Keep the user's digits (Arabic-Indic or Western).

## AI tells in Sindhi

- Urdu or Hindi words dropped in where everyday Sindhi has its own word. Sindhi is its own language, not a dialect of either.
- Literal English calques, such as a word for word "I hope this message finds you well".
- Very formal, bookish words in a casual message to family or friends.
- The same sentence shape repeated, every sentence ending the same way.
- English punctuation in the Arabic-based script. Use "،" for a comma and "؟" for a question mark there.

## Right to left text in files

The Arabic-based Sindhi script is written right to left. When you edit a Word file in place, keep each paragraph's existing settings so the direction stays right. If you create new paragraphs (for example when turning a PDF into a Word file), they need right to left set: in python-docx this means adding `w:bidi` to the paragraph properties and `w:rtl` to the runs. If you cannot do that, tell the user to select the text in Word and click the right to left button. Devanagari Sindhi is left to right and needs nothing extra.

## Steps

1. Note the script and register, and keep both.
2. Swap borrowed Urdu or Hindi words for the everyday Sindhi word where the context is casual.
3. Rewrite calques the way a Sindhi speaker would say them.
4. Vary sentence length. Fix punctuation for the script.
5. Check names, numbers, and dates are unchanged.

## Output

The rewritten Sindhi text, then a short **What I changed** list in the language the user is using with you. Describe the changes in plain words, without word-by-word English glosses of the rewritten text.

## Example

Before: "مان اميد ڪريان ٿو ته هي پيغام توهان کي سٺي صحت ۾ ملندو. سڀاڻي جي گڏجاڻي ٽي وڳي آهي."

After: "ڪيئن آهيو؟ سڀاڻي جي گڏجاڻي ٽي وڳي آهي."

Gloss: The first version opens with a word for word "I hope this message finds you in good health. Tomorrow's meeting is at three." The rewrite opens the way a person would, "How are you?", and keeps the time exactly.

## Help wanted

This file has not yet been reviewed by a native speaker. If you speak Sindhi, corrections are welcome, in either script. See CONTRIBUTING.md.
