# Filipino

Rewrite Filipino (Tagalog) so it sounds like a person wrote it, with the right level of politeness.

## When this applies

- The text is in Filipino or Tagalog.
- The user asks for a translation into Filipino (also load `translate-humanize.md`).
- Most everyday Filipino writing mixes in English (Taglish). For that, also load `mixed-language.md` and keep the mix.

## What stays the same

- Language. Filipino stays Filipino. Never translate unless asked.
- Politeness markers. "Po" and "opo" show respect to older people, customers, and bosses. Keep them where the user used them. Do not add them to a message between friends, and do not remove them from a message to a parent or a client.
- Forms of address: Ate, Kuya, Tita, Tito, Ma'am, Sir. Keep them as the user wrote them.
- The amount of English. If the user writes Taglish, keep it Taglish.
- Names, numbers, dates, amounts, and places. Keep the user's style for money (₱1,500 or PHP 1,500) and dates.

## AI tells in Filipino

- Deep, formal Tagalog in a casual message: "Mangyaring ipaalam sa akin" where people write "Pakisabi na lang" or "Paki-update ako".
- Translated English openers: "Umaasa ako na ang mensaheng ito ay makakarating sa iyo nang maayos".
- Pure Tagalog replacing English words that everyone uses in daily life: "salumpuwit" for "upuan" or "chair", or forced translations of "meeting", "deadline", "load".
- Missing or misplaced "po", or "po" on every single word.
- "Ikaw" and "ako" in every sentence, where Filipino often leaves them out.
- Stiff word order copied from English.

## Steps

1. Identify the reader and keep the level of respect, including po and opo.
2. Keep the user's mix of English. Do not purify it.
3. Replace deep or translated phrases with how people actually say them.
4. Check names, numbers, and dates are unchanged.

## Output

The rewritten Filipino text, then a short **What I changed** list in the language the user is using with you.

## Example

Before (to a client): "Umaasa ako na ang mensaheng ito ay makakarating sa iyo nang maayos. Mangyaring ipaalam sa akin kung natanggap mo ang bayad."

After: "Hi Ma'am Liza, natanggap n'yo na po ba ang bayad? Pakisabi na lang po."

Gloss: "Hi Ma'am Liza, did you receive the payment? Please let me know." The first is a translated English opener in deep, formal Tagalog. The rewrite is polite, with "po" and "Ma'am", the way people write to a client.

## Help wanted

This file has not yet been reviewed by a native speaker. If you speak Filipino, corrections are welcome. See CONTRIBUTING.md.
