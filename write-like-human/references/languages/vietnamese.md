# Vietnamese

Rewrite Vietnamese so it sounds like a person wrote it, with the right pronouns for the relationship.

## When this applies

- The text is in Vietnamese.
- The user asks for a translation into Vietnamese (also load `translate-humanize.md`). Ask who the reader is if it is not clear, because the pronouns depend on age and relationship.

## What stays the same

- Language. Vietnamese stays Vietnamese. Never translate unless asked.
- Diacritics. Every tone mark and vowel mark stays. "ma", "má", "mà", "mả", "mã", "mạ" are different words. Never strip marks or write Vietnamese without them unless the user writes that way.
- Pronouns and kinship terms. Vietnamese uses kinship words as pronouns: anh (older man), chị (older woman), em (younger person), bạn (friend or peer), cô, chú, ông, bà for elders. Keep the pair the user chose. Do not swap them for a neutral "bạn" everywhere.
- Names, numbers, dates, amounts, and places. Keep the user's date style (7/11/2026 is 7 November) and number style (1.500.000 đồng uses dots).

## AI tells in Vietnamese

- "Bạn" used for everyone, including elders and a boss, because it maps to English "you". It sounds cold or rude to an older reader.
- Literal English openers: "Tôi hy vọng email này tìm thấy bạn khỏe mạnh."
- "Tôi" at the start of every sentence in a friendly message where people drop it or use a kinship term.
- Long passive sentences with "được" copied from English.
- Very formal Sino-Vietnamese words in a casual chat.

## Steps

1. Identify the relationship and keep the pronoun pair.
2. Replace translated openers with how a Vietnamese speaker would start.
3. Cut repeated "tôi" and stiff passives.
4. Check every diacritic is still there.
5. Check names, numbers, and dates are unchanged.

## Output

The rewritten Vietnamese text, then a short **What I changed** list in the language the user is using with you.

## Example

Before: "Tôi hy vọng email này tìm thấy bạn khỏe mạnh. Cuộc họp đã được dời sang thứ Hai."

After: "Chào anh Minh, cuộc họp dời sang thứ Hai anh nhé."

Gloss: The first version translates "I hope this email finds you healthy. The meeting has been moved to Monday." The rewrite greets Minh as "anh" (he is older than the writer), drops the passive, and keeps Monday.

## Help wanted

This file has not yet been reviewed by a native speaker. If you speak Vietnamese, corrections are welcome. See CONTRIBUTING.md.
