# French

Rewrite French so it sounds like a person wrote it, for the right reader and region.

## When this applies

- The text is in French.
- The user asks for a translation into French (also load `translate-humanize.md`).

## What stays the same

- Language. French stays French. Never translate unless asked.
- Regional variety. France, Belgium, Switzerland, Quebec, and West Africa differ. Keep the user's words ("courriel" in Quebec, "septante" in Belgium and Switzerland).
- Names, numbers, dates, amounts, and places. Keep French number format (1 500,50 €).
- The register. "Vous" stays "vous". "Tu" stays "tu".

## AI tells in French

- Anglicisms and calques. "Faire du sens" (use "avoir du sens"), "définitivement" for "definitely" (use "vraiment" or "sans aucun doute"), "adresser un problème" (use "traiter" or "régler"), "supporter" for "soutenir", "éventuellement" for "eventually" (use "finalement").
- Wrong tu or vous. Tu with a client or landlord, vous with a close friend.
- English capitalization. Days, months, and languages are lowercase in French: "lundi", "novembre", "français".
- English punctuation. French uses a space before ":", ";", "?", and "!" in France, and « guillemets » for quotes.
- Stock openers like "J'espère que ce message vous trouve bien", which is a calque. Use "J'espère que vous allez bien" or go straight to the point.
- Heavy formal closings in casual mail. "Je vous prie d'agréer..." belongs in a formal letter, not a note to a colleague.

## Steps

1. Identify the reader, the region, and the register, and keep them.
2. Replace anglicisms and calques with natural French.
3. Fix capitalization, spacing, and quotes.
4. Match the closing to the relationship.
5. Check names, numbers, and dates are unchanged.

## Output

The rewritten French text, then a short **What I changed** list in the language the user is using with you. Describe the changes in plain words, without word-by-word English glosses of the rewritten text.

## Example

Before: "Bonjour Julie, j'espère que ce message vous trouve bien. Je voulais adresser le problème de la facture de Novembre. Ça fait du sens de se voir Lundi?"

After: "Bonjour Julie, j'espère que vous allez bien. Je voulais revenir sur la facture de novembre. On peut en parler lundi ?"

Gloss: "Hi Julie, hope you're well. I wanted to follow up on the November invoice. Can we talk about it on Monday?" The first had three calques, two wrong capitals, and no space before the question mark.

## Help wanted

This file has not yet been reviewed by a native speaker. If you speak French, corrections are welcome. See CONTRIBUTING.md.
