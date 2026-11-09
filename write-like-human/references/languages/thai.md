# Thai

Rewrite Thai so it sounds like a person wrote it, at the politeness level the user chose.

## When this applies

- The text is in Thai.
- The user asks for a translation into Thai (also load `translate-humanize.md`). Ask whether the writer is a man or a woman if polite particles are needed and it is not clear.

## What stays the same

- Language. Thai stays Thai. Never translate unless asked.
- Spacing. Thai does not put spaces between words. Spaces mark the end of a phrase or sentence. Never add spaces between words as if it were English.
- Polite particles. Keep ครับ (male speaker) and ค่ะ or คะ (female speaker) exactly as the user uses them. Do not add them to a casual chat that had none, and do not remove them from a polite message.
- Pronouns. Keep the user's choice (ผม, ฉัน, ดิฉัน, เรา, or a nickname).
- Names, numbers, dates, amounts, and places. Keep Buddhist Era years (2569) if the user uses them, and Western years if they use those.

## AI tells in Thai

- Spaces between words, copied from English layout.
- Literal English openers: "ฉันหวังว่าอีเมลนี้จะพบคุณในสุขภาพที่ดี".
- คุณ used in every sentence where Thai would use a name, a title (พี่, น้อง), or leave the subject out.
- Polite particles missing in a message to a boss, or piled onto a casual chat.
- Very formal written words (ดำเนินการ, กระทำ) in everyday messages.

## Steps

1. Note the politeness level, the speaker's particle, and the pronoun, and keep them.
2. Fix spacing so it follows Thai rules.
3. Replace translated openers and cut repeated คุณ.
4. Use everyday words in casual writing.
5. Check names, numbers, and dates are unchanged.

## Output

The rewritten Thai text, then a short **What I changed** list in the language the user is using with you.

## Example

Before: "ฉันหวังว่าอีเมลนี้จะพบคุณในสุขภาพที่ดี การประชุมถูกเลื่อนไปวันจันทร์"

After: "พี่ต้นคะ ประชุมเลื่อนไปวันจันทร์นะคะ"

Gloss: The first version translates "I hope this email finds you in good health. The meeting has been moved to Monday." The rewrite speaks to Ton as พี่ (an older colleague), keeps the writer's female particle คะ, and keeps Monday.

## Help wanted

This file has not yet been reviewed by a native speaker. If you speak Thai, corrections are welcome. See CONTRIBUTING.md.
