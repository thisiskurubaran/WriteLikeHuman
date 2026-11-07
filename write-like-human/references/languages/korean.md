# Korean

Rewrite Korean so it sounds like a person wrote it, at the speech level the user chose.

## When this applies

- The text is in Korean.
- The user asks for a translation into Korean (also load `translate-humanize.md`). Ask who the reader is if it is not clear, because the speech level depends on it.

## What stays the same

- Language. Korean stays Korean. Never translate unless asked.
- Speech level. Formal polite (합니다, 습니다) stays formal. Everyday polite (해요, 어요) stays everyday polite. Casual speech (반말: 해, 야) stays casual. Do not mix levels in one text.
- Titles and suffixes: 님, 씨, 선생님, 팀장님. Keep them as the user wrote them.
- Names, numbers, dates, amounts, and places. Keep the user's date style (2026년 11월 7일 or 2026.11.7).

## AI tells in Korean

- Translated English openers: "이 이메일이 당신을 잘 찾기를 바랍니다".
- Overuse of 당신. Koreans almost never use 당신 for "you" in everyday writing. They use the person's name and title, or leave "you" out.
- 저는 or 나는 at the start of every sentence.
- Stiff Sino-Korean words where a simpler native word is normal: 진행하다 for everything, 이용하다 where 쓰다 fits.
- Passive forms copied from English: "결정되어졌습니다" (double passive) for "결정했습니다".
- Mixing 합니다 and 해요 endings in one message.
- Too many exclamation marks and English-style lists in a short message.

## Steps

1. Identify the reader and keep the speech level.
2. Replace translated openers with natural Korean ("안녕하세요, 김민수 팀장님.").
3. Remove 당신 and repeated 저는.
4. Use simpler words where the Sino-Korean ones sound stiff, unless the setting is formal.
5. Fix double passives and make the endings consistent.
6. Check names, numbers, and dates are unchanged.

## Output

The rewritten Korean text, then a short **What I changed** list in the language the user is using with you.

## Example

Before: "이 이메일이 당신을 잘 찾기를 바랍니다. 회의가 월요일로 변경되어졌음을 알려드리고자 합니다."

After: "안녕하세요, 팀장님. 회의를 월요일로 옮겼습니다."

Gloss: "Hello, manager. We've moved the meeting to Monday." The first is a word for word translation of an English opener, uses 당신, and has a double passive. The rewrite keeps the formal polite level.

## Help wanted

This file has not yet been reviewed by a native speaker. If you speak Korean, corrections are welcome. See CONTRIBUTING.md.
