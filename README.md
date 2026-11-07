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

### Ways to work

| You want to | Say something like |
|---|---|
| Fix text you already have | "Make this sound natural" |
| Write something new that sounds right the first time | "Write a thank you note to my teacher" |
| Find out what sounds off, without changes | "Does this sound like AI?" |
| Approve or reject each change | "Show me the changes one by one" |

### Files

| File | What happens |
|---|---|
| Word (.docx) | Rewrites the text and keeps fonts, styles, tables, and lists. Can show changes as tracked changes. |
| PDF | Reads the text page by page and gives you back an editable Word file. Tells you if a page is a scanned image. |
| Google Docs and Claude docs | Edits in place if Claude is connected to your Google account, otherwise gives you a clean copy to paste back. |
| Spreadsheets (.xlsx, .csv, Google Sheets) | Rewrites only text cells, notes, and comments. Never touches numbers or formulas. |
| Slides (.pptx, Google Slides) | Rewrites slide text and speaker notes and keeps the layout. |

### Kinds of writing

| Writing | Notes |
|---|---|
| Emails | Quick replies, saying no politely, follow-ups, thank yous, apologies, asking for something |
| WhatsApp and SMS replies | To family, landlords, delivery people, building groups |
| Formal letters | Leave, complaint, bank, government, and school letters in Indian formats |
| Resumes and cover letters | Swaps buzzwords for plain words, never invents achievements |
| Social posts | LinkedIn, Instagram, X, WhatsApp, Facebook, within each platform's limits |
| Bios | Instagram bio, dating profile, website About page |
| Reports | School and work reports, made clearer in your own words |
| Meeting notes | Rough notes into readable minutes and summaries |
| Speeches and toasts | Wedding, birthday, farewell, written to be read out loud |
| Wishes and cards | Festival greetings, congratulations, and condolences written with care |
| Reviews | Your own real experience with a product, place, or service, in your words |
| Form answers | Personal statements, visa purpose letters, scholarship answers, kept true |
| Voice notes | Speech-to-text transcripts turned into readable text |

### Adjustments

| Adjustment | Say something like |
|---|---|
| Tone | "Friendlier", "more professional", "warmer", "short and direct", "more formal" |
| Reading level | "Simpler for my mom", "for a 10 year old", "English is their second language" |
| Length | "Cut this to 200 words", "turn these notes into a paragraph" |
| Easy to read | "Is this easy to read?" flags long sentences, jargon, and unclear links |
| Inclusive wording | "Make it gender neutral" (only when you ask) |

### Your own voice

Give it a few things you wrote yourself and it builds a short voice profile: how long your sentences are, words you use, how you sign off. You keep the profile as a note or file and attach it next time. You can have more than one, like "work me" and "personal me".

### Languages

| Language | What it does |
|---|---|
| Indian English | Keeps lakh, crore, Indian dates, and natural Indian phrasing. No forced American style. |
| Hinglish, Tanglish, and other mixes | Keeps your mix of languages and your script. Does not "correct" it into pure English. |
| Hindi, Tamil, Telugu, Kannada, Malayalam, Bengali, Marathi | Fixes stiff, textbook, or machine-translated wording in that language |
| Spanish, French, German | The same, with each language's own common slips |
| Translation | "Translate this into Hindi" gives a version that sounds native, not machine translated |

It never translates unless you ask. If you write in Tamil, it answers in Tamil.

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
