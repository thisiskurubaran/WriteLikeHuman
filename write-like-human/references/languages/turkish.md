# Turkish

Rewrite Turkish so it sounds like a person wrote it, with the right level of formality.

## When this applies

- The text is in Turkish.
- The user asks for a translation into Turkish (also load `translate-humanize.md`). Ask whether the reader is "sen" or "siz" if it is not clear.

## What stays the same

- Language. Turkish stays Turkish. Never translate unless asked.
- Sen or siz. Keep the form the user chose and keep the verb endings consistent with it.
- Titles of address: "Ahmet Bey", "Ayşe Hanım", "Hocam". Keep them as the user wrote them.
- Names, numbers, dates, amounts, and places. Turkish writes dates as 07.11.2026 and uses a comma for decimals. Keep the user's format.
- Turkish letters (ç, ğ, ı, İ, ö, ş, ü). Never replace them with plain Latin letters.

## AI tells in Turkish

- Long formal chains in a casual message: "gerçekleştirilmesi sağlanmıştır" where "yapıldı" says it.
- English calques: "mantık yapmak" for "mantıklı olmak" (to make sense), "günün sonunda" for "sonuçta" (at the end of the day).
- Translated openers: "Umarım bu e-posta seni iyi bulur".
- Overuse of "ve" to join clauses, where Turkish uses verb forms like -ip, -arak, or -ince.
- Repeating "ben" and "siz" in every sentence, where the verb ending already shows who it is.
- Mixing sen and siz forms.
- Sentences ordered like English with the verb in the middle, when Turkish normally puts it at the end.

## Steps

1. Identify the reader and keep sen or siz.
2. Shorten long formal verb chains in casual writing.
3. Replace calques and translated openers with natural Turkish ("Merhaba Ahmet Bey,").
4. Join clauses with Turkish verb forms instead of a string of "ve".
5. Drop pronouns the verb ending already shows.
6. Check names, numbers, dates, and Turkish letters are unchanged.

## Output

The rewritten Turkish text, then a short **What I changed** list in the language the user is using with you.

## Example

Before: "Umarım bu e-posta sizi iyi bulur. Toplantının pazartesi gününe ertelenmesi kararı alınmış olduğunu bildirmek isterim."

After: "Merhaba Ayşe Hanım, toplantıyı pazartesiye erteledik."

Gloss: "Hello Ms. Ayşe, we've moved the meeting to Monday." The first uses a translated English opener and a long passive chain. The rewrite keeps the respectful "Hanım" and says it directly.

## Help wanted

This file has not yet been reviewed by a native speaker. If you speak Turkish, corrections are welcome. See CONTRIBUTING.md.
