# Nepali

Rewrite Nepali so it sounds like a person wrote it, at the level of respect the user chose.

## When this applies

- The text is in Nepali, in Devanagari or in Roman script.
- The user asks for a translation into Nepali (also load `translate-humanize.md`).
- For Nepali mixed with English, also load `mixed-language.md`.

## What stays the same

- Language and script. Nepali stays Nepali. Devanagari stays Devanagari, Roman stays Roman. Never translate unless asked.
- The level of respect. Nepali has several: हजुर (very respectful), तपाईं (polite), तिमी (familiar), and त (very close or rough). Keep the one the user chose, and keep the verb endings that go with it.
- English words people use every day in Nepali: फोन, अफिस, बैंक, मिटिङ. Do not replace them with rare Sanskrit words.
- Names, numbers, dates, amounts, and places. Keep the user's calendar too: a date in Bikram Sambat (वि.सं.) stays in Bikram Sambat.

## AI tells in Nepali

- Textbook Sanskrit words where people use plain ones: "प्रतीक्षा" in a chat where people write "पर्खनु", "सूचित गर्नु" for "भन्नु".
- Word for word English openers: "म आशा गर्छु यो सन्देशले तपाईंलाई राम्रो स्वास्थ्यमा भेट्छ".
- Mixing तपाईं and तिमी verb forms in one message.
- Repeating "म" and "तपाईं" in every sentence, where Nepali usually leaves them out.
- Hindi words or Hindi grammar slipping in, a common machine translation error.

## Steps

1. Work out who the reader is and keep the user's level of respect.
2. Replace stiff or Hindi-influenced words with everyday Nepali.
3. Rewrite translated openers the way a Nepali speaker would say them.
4. Make the verb endings match the level of respect throughout.
5. Check names, numbers, and dates are unchanged.

## Output

The rewritten Nepali text, then a short **What I changed** list in the language the user is using with you. Describe the changes in plain words, without word-by-word English glosses of the rewritten text.

## Example

Before: "म आशा गर्छु यो सन्देशले तपाईंलाई राम्रो स्वास्थ्यमा भेट्छ। भोलिको बैठक स्थगित गरिएको छ भनेर सूचित गर्न चाहन्छु।"

After: "नमस्ते, भोलिको मिटिङ सरेको छ।"

Gloss: "Hello, tomorrow's meeting has been moved." The first is a word for word translation of an English email opener with formal government wording. The rewrite keeps the polite tone and says it simply.

## Help wanted

This file has not yet been reviewed by a native speaker. If you speak Nepali, corrections are welcome. See CONTRIBUTING.md.
