# Tamil

Rewrite Tamil so it sounds like a person wrote it, matching how people really write in the situation.

## When this applies

- The text is in Tamil, in Tamil script or in Roman script.
- The user asks for a translation into Tamil (also load `translate-humanize.md`).
- For Tanglish (Tamil mixed with English), load `mixed-language.md` instead or as well.

## What stays the same

- Language and script. Tamil stays Tamil. Tamil script stays Tamil script. Never translate unless asked.
- Names, numbers, dates, amounts, and places.
- The register. "நீங்க" or "நீங்கள்" stays respectful. "நீ" stays informal.
- English words that people use every day in Tamil (bus, phone, office, ticket), unless the user avoids them.

## AI tells in Tamil

- Literary Tamil (centamil) in casual text. A WhatsApp message to a cousin written like a newspaper editorial. Spoken Tamil forms like "வர்றேன்", "சொல்லு", "இருக்கு" are normal in chat. Written forms like "வருகிறேன்", "இருக்கிறது" fit formal writing.
- Forced pure Tamil words for things people name in English, where the user would not.
- Literal English calques like translating "I hope this finds you well" word by word.
- Mixed registers. Half the message in formal written Tamil, half in spoken Tamil.
- Every sentence the same length, each ending in the same verb form.

Formal letters, school essays, and official mail should stay in standard written Tamil. Fix the stiffness, keep the register.

## Steps

1. Decide if the text is formal written Tamil or everyday spoken Tamil, and keep that.
2. Fix lines that switch register partway.
3. Rewrite calques the way a Tamil speaker would say them.
4. Vary sentence length and endings.
5. Check names, numbers, and dates are unchanged.

## Output

The rewritten Tamil text, then a short **What I changed** list in the language the user is using with you.

## Example

Before (to a friend): "நண்பா, நாளை நான் வருகிறேன் என்பதை உறுதிப்படுத்துகிறேன்."

After: "டேய், நாளைக்கு கண்டிப்பா வர்றேன்."

Gloss: The first reads like a formal notice: "Friend, I confirm that I will come tomorrow." The second is how you would text a friend: "Hey, I'm definitely coming tomorrow."

## Help wanted

This file has not yet been reviewed by a native speaker. If you speak Tamil, corrections are welcome. See CONTRIBUTING.md.
