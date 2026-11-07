# Italian

Rewrite Italian so it sounds like a person wrote it, with the right level of formality.

## When this applies

- The text is in Italian.
- The user asks for a translation into Italian (also load `translate-humanize.md`). Ask whether the reader is someone they would address as "tu" or "Lei" if it is not clear.

## What stays the same

- Language. Italian stays Italian. Never translate unless asked.
- Tu or Lei. Keep the form the user chose, and keep every verb, pronoun, and possessive consistent with it (Lei, La, Suo).
- Names, numbers, dates, amounts, and places. Italian writes dates as 7/11/2026 and uses a comma for decimals (12,50 euro). Keep the user's format.
- Formal letter conventions when the user is writing formally ("Gentile...", "Cordiali saluti").

## AI tells in Italian

- English calques: "fare senso" for "avere senso", "realizzare" for "rendersi conto", "supportare" for "sostenere", "applicare per un lavoro" for "candidarsi".
- Too many anglicisms where Italian has a normal word: "meeting" and "call" are common in offices, but "deadline", "task", "feedback", "performare" in every line sounds like a translation.
- Mixing tu and Lei in one message.
- Translated openers: "Spero che questa email ti trovi bene".
- Overlong sentences full of "che" clauses, and "il quale" where "che" is enough.
- Possessives everywhere ("la mia macchina, il mio telefono") where Italian usually drops them.
- English punctuation: Title Case in headings, or many exclamation marks.

## Steps

1. Identify the reader and keep tu or Lei consistently.
2. Replace calques and unneeded anglicisms with normal Italian. Keep office anglicisms the user clearly uses.
3. Swap translated openers for natural ones ("Ciao Marco," or "Gentile dottoressa Ricci,").
4. Shorten long sentences and cut extra possessives.
5. Check names, numbers, and dates are unchanged.

## Output

The rewritten Italian text, then a short **What I changed** list in the language the user is using with you.

## Example

Before: "Spero che questa email ti trovi bene. Volevo realizzare se hai avuto il tempo di dare un feedback sul task che ti ho mandato."

After: "Ciao Luca, hai avuto modo di guardare il lavoro che ti ho mandato? Fammi sapere cosa ne pensi."

Gloss: "Hi Luca, did you get a chance to look at the work I sent you? Let me know what you think." The first uses a translated opener, "realizzare" in the English sense, and two anglicisms in one sentence.

## Help wanted

This file has not yet been reviewed by a native speaker. If you speak Italian, corrections are welcome. See CONTRIBUTING.md.
