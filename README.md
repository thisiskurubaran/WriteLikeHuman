<div align="center">

# WriteLikeHuman

**Make everyday writing sound like you wrote it.**

A free Claude skill for emails, WhatsApp replies, letters, resumes, posts, and the files you already use.

[![Latest release](https://img.shields.io/github/v/release/thisiskurubaran/WriteLikeHuman?label=release&color=2ea44f)](https://github.com/thisiskurubaran/WriteLikeHuman/releases/latest)
[![License: MIT](https://img.shields.io/github/license/thisiskurubaran/WriteLikeHuman?color=blue)](LICENSE)
[![Claude Skill](https://img.shields.io/badge/Claude-Skill-D97757?logo=claude&logoColor=white)](https://support.claude.com/en/articles/12512180-use-skills-in-claude)
[![Works on](https://img.shields.io/badge/works%20on-web%20%7C%20desktop%20%7C%20mobile-6f42c1)](INSTALL.md)
[![No coding needed](https://img.shields.io/badge/coding-not%20needed-success)](INSTALL.md)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](CONTRIBUTING.md)

[Install](#install-in-two-minutes) · [What you can ask](#what-you-can-ask) · [Features](#features) · [FAQ](#faq) · [Contributing](#contributing)

</div>

---

## Why WriteLikeHuman?

You ask Claude for help with a message and it comes back sounding like a brochure. "I hope this finds you well." "It's important to note." Long dashes everywhere. Nobody talks like that.

WriteLikeHuman fixes it. Paste your text or attach a file, say "make this sound less robotic", and you get it back in plain, natural words. Your facts, numbers, and formatting stay exactly as they were, and your original file is never overwritten.

You don't need to know anything about code. If you can upload a photo, you can install this.

## See the difference

<table>
<tr>
<th width="50%">Before</th>
<th width="50%">After</th>
</tr>
<tr>
<td valign="top">

I hope this message finds you well! I wanted to reach out regarding the quarterly report. It's important to note that the deadline has been moved to 15 March. Please ensure that all inputs are submitted accordingly. Let me know if you have any questions!

</td>
<td valign="top">

Hi team, the quarterly report deadline has moved to 15 March. Please send me your inputs by then.

</td>
</tr>
</table>

Every result ends with a short note in plain words:

> **What I changed**
> - Removed the stock opening and closing lines.
> - Cut "It's important to note that", which added nothing.
> - Kept the date exactly as it was.

More samples: [before-after.md](write-like-human/examples/before-after.md)

## Install in two minutes

| Step | What to do |
|:---:|---|
| 1 | Download **`WriteLikeHuman.zip`** from the [Releases page](https://github.com/thisiskurubaran/WriteLikeHuman/releases). Don't unzip it. |
| 2 | In Claude, open **Settings > Capabilities** and turn on **Code execution and file creation**. |
| 3 | Go to **Customize > Skills**, click **+**, then **Upload a skill**, and pick the zip. |
| 4 | Check the switch next to WriteLikeHuman is on. That's it. |

It's one skill and one upload. Once it's on your account, it works in the Claude phone app too.

Need more help, or use Claude Code? See the full [install guide](INSTALL.md).

## What you can ask

Just talk normally. There are no commands to learn.

```text
Make this email sound less robotic
Humanize this Word file
Does this sound like AI?
Write a farewell speech for my manager
Reply to this WhatsApp from my landlord
Make this simpler for my dad
Show me each change so I can approve it
```

## Features

### Four ways to work

| Mode | Try saying |
|---|---|
| Rewrite text you already have | "Make this sound natural" |
| Draft something new that sounds right first time | "Write a thank you note to my teacher" |
| Check what sounds off, without changing anything | "Does this sound like AI?" |
| Approve or reject each change, one by one | "Show me the changes side by side" |

### Your files, kept intact

| File | What you get back |
|---|---|
| Word (.docx) | Same fonts, styles, tables, and lists. Tracked changes if you want them. |
| PDF | An editable Word copy, with a heads-up if any page is a scanned image. |
| Google Docs and Claude docs | Edited in place when Claude is connected to your Google account, or a clean copy to paste back. |
| Spreadsheets (.xlsx, .csv, Google Sheets) | Only text cells, notes, and comments change. Numbers and formulas are never touched. |
| Slides (.pptx, Google Slides) | Slide text and speaker notes, with the layout left alone. |
| Text and Markdown (.txt, .md) | Markdown, links, and code blocks kept as they were. |
| Subtitles (.srt, .vtt) | Captions reworded, timings untouched, so they stay in sync. |
| OpenDocument and RTF (.odt, .rtf) | Edited as a Word file, and you're told which format you get back. |
| Screenshots of chats and emails | A reply drafted from what's on screen, without repeating anyone's phone number. |
| Several files at once | Each file fixed on its own, with no details mixed between them. |

Every file comes back as a new copy named `yourfile-humanized`, so the original stays safe. Ask for "a file showing what changed" and you also get a Word file with every change marked.

<details>
<summary><b>Kinds of writing it knows (21)</b></summary>

<br>

| Writing | What it pays attention to |
|---|---|
| Emails | Quick replies, polite no's, follow-ups, thank yous, apologies, asking for something, and replies to whole threads |
| WhatsApp and SMS | Replies to family, landlords, delivery people, building groups |
| Formal letters | Leave, complaint, bank, government, and school letters in Indian formats |
| Resumes and cover letters | Plain words instead of buzzwords, and no invented achievements |
| Social posts | LinkedIn, Instagram, X, WhatsApp, and Facebook, within each one's limits |
| Bios | Instagram bio, dating profile, website About page |
| Reports | School and work reports, clearer and still in your words |
| Meeting notes | Rough notes turned into readable minutes |
| Speeches and toasts | Weddings, birthdays, farewells, written to be read out loud |
| Wishes and cards | Festivals, congratulations, and condolences written with care |
| Reviews | Your own real experience, in your own words |
| Form answers | Personal statements, visa letters, scholarship answers, kept true |
| Voice notes | Speech-to-text transcripts turned into readable text |
| Replies to reviews | Business owners answering customer reviews as themselves |
| Listings | Product descriptions for Meesho, Etsy, Amazon, Flipkart, OLX, and Instagram shops, with only the seller's facts |
| Invitations | Weddings, housewarmings, naming ceremonies, birthday parties |
| Hard conversations | Apologies, setting boundaries, saying no to family |
| Job posts | Plain, inclusive job descriptions |
| Notices and newsletters | Housing society, school, club, and office notices |
| Freelance proposals | Upwork, Fiverr, and client quotes, with no invented experience |
| Essays | School and college essays, improved in the student's own words |

</details>

<details>
<summary><b>Adjustments</b></summary>

<br>

| Adjustment | Try saying |
|---|---|
| Tone | "Friendlier", "more professional", "warmer", "short and direct", "more formal" |
| Reading level | "Simpler for my mom", "for a 10 year old", "English is their second language" |
| Length | "Cut this to 200 words", "turn these notes into a paragraph" |
| Easy to read | "Is this easy to read?" flags long sentences, jargon, and unclear links |
| Inclusive wording | "Make it gender neutral" (only when you ask) |
| Words to leave alone | "Never change 'FlexiPlan Pro'" keeps brand names, jargon, and nicknames exactly as written |
| Kind of English | "Make it UK English" switches between US, UK, Australian, and Indian spelling and dates |
| Ready to paste | Line breaks and formatting that work in each app |
| Reading age | "What reading age is this?" gives a rough guide, only when you ask |

</details>

<details>
<summary><b>Your own voice</b></summary>

<br>

Share a few things you wrote yourself and WriteLikeHuman builds a short voice profile: how long your sentences run, the words you like, how you sign off. Keep it as a note or file and attach it next time. You can have more than one, like "work me" and "personal me". You can also build one from your own WhatsApp chat export: only your messages are used, and phone numbers, emails, and links are hidden first.

</details>

<details>
<summary><b>Languages</b></summary>

<br>

| Language | What it does |
|---|---|
| Indian English | Keeps lakh, crore, Indian date formats, and natural Indian phrasing. No forced American style. |
| Hinglish, Tanglish, Manglish, Benglish, Kanglish, and other mixes | Keeps your mix and your script. It won't "correct" you into pure English. |
| Hindi, Tamil, Telugu, Kannada, Malayalam, Bengali, Marathi, Gujarati, Punjabi, Odia, Urdu, Assamese | Fixes stiff, textbook, or machine-translated wording |
| Spanish, French, German, Portuguese, Indonesian, Arabic, Japanese | The same, with each language's own common slips |
| Translation | "Translate this into Hindi" gives you a version that sounds native |

It never translates unless you ask. Write in Tamil and it answers in Tamil.

The language guides haven't been checked by native speakers yet. If you speak one of these languages, [your help is welcome](CONTRIBUTING.md#help-wanted).

</details>

## What it won't do

WriteLikeHuman helps you write better. It doesn't help anyone pretend.

- Change your facts. Names, numbers, dates, amounts, and quotes stay as you wrote them. If something is vague, it asks.
- Make promises about checkers. It makes writing clearer and more natural, and that's all it claims.
- Write fake reviews, or reviews of things you haven't used.
- Invent experiences in a personal statement, visa letter, or scholarship answer.
- Imitate anyone but you.

## FAQ

<details>
<summary><b>Is it free?</b></summary>

<br>

Yes. WriteLikeHuman is free and open source under the MIT license. You need a Claude account with skills available. See the [install guide](INSTALL.md) for details.

</details>

<details>
<summary><b>Does it work on my phone?</b></summary>

<br>

Yes. Upload it once on the Claude website or desktop app, then use it in the Claude app on your phone with the same account.

</details>

<details>
<summary><b>Will it mess up my document?</b></summary>

<br>

It changes words, not layout. Fonts, tables, lists, and formulas stay put, and you always get a new copy, so your original is untouched.

</details>

<details>
<summary><b>It didn't kick in. What now?</b></summary>

<br>

Start your message with "Use WriteLikeHuman to...". If that doesn't help, check the switch is on under **Customize > Skills**. More fixes are in the [install guide](INSTALL.md#something-not-working).

</details>

## Privacy

Your text stays in your own chat with Claude. The skill doesn't save or send your writing anywhere. If you ever spot a case where it might, please [report it privately](SECURITY.md).

## Contributing

Know an AI habit we miss? Want your language or a new kind of writing added? Contributions are welcome. Start with [CONTRIBUTING.md](CONTRIBUTING.md) and please follow the [Code of Conduct](CODE_OF_CONDUCT.md).

Found a bug? [Open an issue](https://github.com/thisiskurubaran/WriteLikeHuman/issues/new/choose), and use made-up text rather than your real files.

## License

Released under the [MIT License](LICENSE). Use it, share it, improve it.
