# Assamese

Rewrite Assamese so it sounds like a person wrote it, in the Assamese people actually speak and write.

## When this applies

- The text is in Assamese, in Assamese script or in Roman script.
- The user asks for a translation into Assamese (also load `translate-humanize.md`).
- For Assamese mixed with English, load `mixed-language.md` as well.

## What stays the same

- Language and script. Assamese stays Assamese. Never translate unless asked.
- Assamese letters. Assamese uses ৰ and ৱ, not the Bengali র and ব for those sounds. Keep them.
- Names, numbers, dates, amounts, places, and quotes.
- The register. "আপুনি" stays "আপুনি". "তুমি" stays "তুমি". "তই" stays "তই".

## AI tells in Assamese

- Bengali spelling or words. Machine translation often writes Bengali and calls it Assamese: র instead of ৰ, or Bengali verb forms like "করছি" where Assamese says "কৰি আছোঁ".
- Bookish words in a casual note: "অনুগ্ৰহ কৰি", "উপস্থিত থাকিব", "জনাব" in every line.
- Literal English calques like "মই আশা কৰোঁ এই বাৰ্তাই আপোনাক ভাল স্বাস্থ্যত পায়".
- Every sentence built the same way.

## Steps

1. Work out the reader and keep the user's register.
2. Fix Bengali letters and verb forms.
3. Swap bookish words for everyday Assamese in casual text.
4. Remove calques.
5. Check names, numbers, and dates are unchanged.

## Output

The rewritten Assamese text, then a short **What I changed** list in the language the user is using with you.

## Example

Before: "প্ৰিয় বন্ধু, অনুগ্ৰহ কৰি মোক জনাব যে আপুনি কাইলৈৰ অনুষ্ঠানত উপস্থিত থাকিব নে নাই।"

After: "অ' ৰাহুল, কাইলৈ প্ৰ'গ্ৰামলৈ আহিবি নে? কৈ দিবি।"

Gloss: The first reads like an official notice: "Dear friend, kindly let me know whether you will be present at tomorrow's function." The rewrite is a text to a close friend: "Hey Rahul, are you coming to the event tomorrow? Let me know." Use the "তই" forms only if that is how the user talks to Rahul.

## Help wanted

This file has not yet been reviewed by a native speaker. If you speak Assamese, corrections are welcome. See CONTRIBUTING.md.
