# Gujarati

Rewrite Gujarati so it sounds like a person wrote it, in the Gujarati people actually speak and write.

## When this applies

- The text is in Gujarati, in Gujarati script or in Roman script.
- The user asks for a translation into Gujarati (also load `translate-humanize.md`).
- For Gujarati mixed with English, load `mixed-language.md` as well.

## What stays the same

- Language and script. Gujarati stays Gujarati. Gujarati script stays Gujarati script. Never translate into English unless asked.
- Names, numbers, dates, amounts, places, and quotes. Keep the user's digits, whether they use ૧૨૩ or 123.
- The register. If the writer uses "તમે", keep "તમે". If they use "તું", keep "તું".
- English words people use every day in Gujarati: મોબાઇલ, બેંક, ઓફિસ, ટિકિટ, ફોર્મ. Do not swap them for rare Sanskrit words.

## AI tells in Gujarati

- Textbook, Sanskrit heavy Gujarati in a casual note. "ઉપસ્થિત", "સૂચિત કરો", "પ્રતીક્ષા" where people say "આવજો", "કહેજો", "રાહ".
- Literal English calques. "હું આશા રાખું છું કે આ સંદેશ તમને સારા સ્વાસ્થ્યમાં મળે" is "I hope this finds you well" word for word.
- "કૃપા કરીને" in every line of a friendly message.
- Hindi words and grammar slipping in, a common machine translation habit. "મેં કહ્યું થા" mixes Hindi into Gujarati.
- Every sentence built the same way and ending in "છે."

Formal letters to a bank, school, or office can stay formal. The problem is formal words in a casual message.

## Steps

1. Work out who the reader is and keep the user's register.
2. Swap textbook words for everyday Gujarati where the context is casual.
3. Remove calques and Hindi slips, and rewrite the way a Gujarati speaker would say it.
4. Vary sentence length.
5. Check names, numbers, and dates are unchanged.

## Output

The rewritten Gujarati text, then a short **What I changed** list in the language the user is using with you.

## Example

Before: "પ્રિય મિત્ર, કૃપા કરીને મને જણાવો કે તમે આવતીકાલના કાર્યક્રમમાં ઉપસ્થિત રહેશો કે નહીં."

After: "અરે રાહુલ, કાલે પ્રોગ્રામમાં આવે છે ને? કહેજે."

Gloss: The first reads like an official notice: "Dear friend, kindly inform me whether you will be present at tomorrow's event." The rewrite is how you would text a friend: "Hey Rahul, you're coming to the event tomorrow, right? Let me know." Only switch to "તું" forms if that is how the user talks to Rahul.

## Help wanted

This file has not yet been reviewed by a native speaker. If you speak Gujarati, corrections are welcome. See CONTRIBUTING.md.
