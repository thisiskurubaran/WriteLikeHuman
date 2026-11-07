# Japanese

Rewrite Japanese so it sounds like a person wrote it, at the politeness level the user chose.

## When this applies

- The text is in Japanese.
- The user asks for a translation into Japanese (also load `translate-humanize.md`). Ask who the reader is if it is not clear, because the politeness level depends on it.

## What stays the same

- Language. Japanese stays Japanese. Never translate unless asked.
- Politeness level. Plain form (だ, である) stays plain. Polite form (です, ます) stays polite. Keigo (いたします, おります, ございます) stays keigo for clients and customers. Do not mix levels in one text.
- Name suffixes. Keep 様, さん, くん, or 先生 as the user wrote them.
- Names, numbers, dates, amounts, and places. Keep the user's date style (2026年11月7日 or 2026/11/7) and number style.

## AI tells in Japanese

- Translated English openers: "このメールがあなたを元気に見つけることを願っています". Japanese business email opens with set phrases like "お世話になっております" or "お疲れさまです".
- Overuse of あなた. Japanese usually uses the person's name or leaves the subject out.
- 私は at the start of every sentence.
- Too much katakana English where a Japanese word is normal: アジェンダ for 議題, ソリューション for 解決策. Some katakana is normal in business, so keep what the user uses.
- Mixing です and ます with plain forms in one message.
- "〜することができます" where "〜できます" is enough.
- English punctuation and many exclamation marks. Japanese uses "、" and "。".

## Steps

1. Identify the reader and the politeness level, and keep it.
2. Replace translated openers with natural Japanese set phrases, at the same politeness.
3. Cut あなた and repeated 私は.
4. Make the verb forms consistent.
5. Check names, numbers, and dates are unchanged.

## Output

The rewritten Japanese text, then a short **What I changed** list in the language the user is using with you.

## Example

Before: "田中様、このメールがあなたを元気に見つけることを願っています。会議が月曜日に移動されたことをお知らせしたいと思います。"

After: "田中様、お世話になっております。会議の日程を月曜日に変更いたしました。"

Gloss: "Mr. or Ms. Tanaka, thank you as always. We have moved the meeting to Monday." The first is a word for word translation of an English opener and uses あなた. The rewrite keeps the formal 様 and keigo, because the user was writing formally.

## Help wanted

This file has not yet been reviewed by a native speaker. If you speak Japanese, corrections are welcome. See CONTRIBUTING.md.
