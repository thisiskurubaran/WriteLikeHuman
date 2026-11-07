# WriteLikeHuman

A Claude skill that makes everyday writing sound like a person wrote it.

Paste an email, attach a Word file, or forward a WhatsApp message and say "make this sound less robotic". You get your text back in plain, natural words, with the same facts, numbers, and formatting. Your original file is never overwritten.

It is for people who use Claude day to day. You do not need to know anything about code.

## Before and after

Before:

> I hope this message finds you well! I wanted to reach out regarding the quarterly report. It's important to note that the deadline has been moved to 15 March. Please ensure that all inputs are submitted accordingly. Let me know if you have any questions!

After:

> Hi team, the quarterly report deadline has moved to 15 March. Please send me your inputs by then.

What I changed
- Removed the stock opening and closing lines.
- Cut "It's important to note that", which added nothing.
- Kept the date exactly as it was.

More samples are in [write-like-human/examples/before-after.md](write-like-human/examples/before-after.md).

## Install in two minutes

1. Download `WriteLikeHuman.zip` from the [Releases page](https://github.com/thisiskurubaran/WriteLikeHuman/releases). Do not unzip it.
2. In Claude, turn on **Code execution and file creation** (Settings, then Capabilities).
3. Go to **Customize**, then **Skills**, click **+**, then **Upload a skill**, and pick the zip.
4. Make sure the switch next to WriteLikeHuman is on.

It is one skill. You upload one zip once and everything below is included. Once it is on your account, you can use it in the Claude phone app too.

Full steps, phone use, Claude Code, and fixes for common problems are in [INSTALL.md](INSTALL.md).

## How to use it

Ask in your own words. For example:

- "Make this email sound less robotic"
- "Humanize this Word file"
- "Does this sound like AI?"
- "Write a farewell speech for my manager"
- "Reply to this WhatsApp from my landlord"
- "Make this simpler for my dad"
- "Show me each change so I can approve it"

## What it handles

It works on pasted text, Word files, PDFs, Google Docs, spreadsheets, and slides. It covers emails, WhatsApp replies, letters, resumes, social posts, speeches, wishes, reviews, and more, in Indian English, Hinglish, and several other languages.

## What it will not do

- Change your facts. Names, numbers, dates, amounts, and quotes stay exactly as you wrote them. If something is vague, it asks instead of filling the gap.
- Promise that writing will get past any checker. It makes writing clearer and more natural. That is all.
- Write fake reviews, or reviews of things you have not used.
- Add experiences, qualifications, or plans you do not have to a personal statement or visa letter.
- Imitate a real person other than you.

## Privacy

Your files are used only in your own chat with Claude. The skill does not store or send your text anywhere. If you find a case where it might, please report it privately (see [SECURITY.md](SECURITY.md)).

## Contributing

Ideas for new writing types, languages, or AI habits to catch are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md). Please follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## License

[MIT](LICENSE)
