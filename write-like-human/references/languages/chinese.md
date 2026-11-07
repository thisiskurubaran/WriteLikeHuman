# Chinese

Rewrite Chinese so it sounds like a person wrote it, in the user's own script and regional style.

## When this applies

- The text is in Chinese (Mandarin written Chinese), in simplified or traditional characters.
- The user asks for a translation into Chinese (also load `translate-humanize.md`). Ask which script and region the reader is in if it is not clear: mainland China, Taiwan, Hong Kong, Singapore, or Malaysia.
- Written Cantonese is different from standard written Chinese. If the user writes in Cantonese, keep it Cantonese and make fewer changes.

## What stays the same

- Language. Chinese stays Chinese. Never translate unless asked.
- The script. Simplified (简体) stays simplified. Traditional (繁體) stays traditional. Never convert unless asked.
- Regional words. Mainland, Taiwan, and Hong Kong use different words for the same thing: 软件 / 軟體 (software), 视频 / 影片 (video), 打印 / 列印 (print). Keep the user's region.
- Politeness. 您 stays 您, 你 stays 你.
- Names, numbers, dates, amounts, and places. Keep the user's date style (2026年11月7日) and number style.
- Chinese punctuation (，。？！：) in Chinese text.

## AI tells in Chinese

- Translated English openers: "我希望这封邮件找到你一切安好".
- Empty verbs: 进行 and 作为 everywhere. "对方案进行了讨论" where "讨论了方案" says it. "作为一个学生，我..." at the start of everything.
- Too many 的 strung together, and too many 被 passives copied from English.
- Pronouns in every sentence (我, 你, 他们), where Chinese often leaves them out.
- Stock phrases: 总而言之, 值得注意的是, 在当今社会 at the start or end.
- English punctuation (, . ?) in Chinese text, and spaces between characters.
- Mixing simplified and traditional characters, or mainland and Taiwan words, in one text.

## Steps

1. Note the script and the region, and keep both.
2. Replace translated openers with natural Chinese (for example "王经理您好，").
3. Cut empty 进行 and 作为 constructions and extra 的.
4. Turn unneeded 被 passives into active sentences.
5. Drop pronouns the context already makes clear.
6. Fix punctuation to Chinese punctuation.
7. Check names, numbers, and dates are unchanged.

## Output

The rewritten Chinese text, then a short **What I changed** list in the language the user is using with you.

## Example

Before (simplified): "我希望这封邮件找到你一切安好。我们对会议时间进行了调整，会议被改到了星期一。"

After: "王经理您好，会议改到星期一了。"

Gloss: "Hello Manager Wang, the meeting has moved to Monday." The first is a translated English opener, uses 进行 and a 被 passive, and says the same thing twice. The rewrite keeps simplified characters and the polite 您.

## Help wanted

This file has not yet been reviewed by a native speaker. If you read and write Chinese, corrections are welcome, especially for Taiwan and Hong Kong usage. See CONTRIBUTING.md.
