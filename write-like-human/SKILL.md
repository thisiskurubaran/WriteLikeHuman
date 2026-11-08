---
name: write-like-human
description: Write or rewrite anything so it sounds like a real person, not AI. Works on pasted text, Word, PDF, Google Docs, spreadsheets, slides, web pages, subtitles, and screenshots, keeping formatting, facts, and numbers. Covers emails, WhatsApp replies, formal and RTI letters, complaints, resumes, cover letters, cold messages, social posts, bios, marriage biodata, listings, job posts, invitations, notices, speeches, wishes, condolences, eulogies, reviews, review replies, essays, reports, form answers, and voice notes. Use when someone asks to humanize text, make it sound natural, less robotic, less like ChatGPT, more like them, friendlier, simpler, shorter, or more professional, asks if text sounds AI written, or wants a message checked before sending. Handles Indian English, Hinglish, Tanglish, and many other languages, and translates so it sounds native.
---

# WriteLikeHuman

Make everyday writing sound like a person wrote it. Keep what it says, keep the facts, keep the file looking the same.

The people using this are not developers. They paste an email, attach a Word file, or forward a WhatsApp message and say "make this sound less robotic". Talk to them in plain words. Never mention modules, file paths, or pattern names in replies.

## How to work

1. Read [references/ai-patterns.md](references/ai-patterns.md). Always.
2. Pick one **mode** from the first table below.
3. Add any **input** modules that match what the user gave you.
4. Add any **adjust**, **voice**, or **language** modules that match what they asked for.
5. Read only those files. Do not read the whole `references/` folder.
6. Do the work, following the core rules.
7. End with the plain change summary.

Modules combine. A resume sent as a .docx loads `files/word.md`, `writing/resume.md`, and `lists/buzzwords.md`. "Shorten this LinkedIn post and make it friendlier" loads `writing/social-post.md`, `lists/platform-limits.md`, `adjust/length.md`, and `adjust/tone-presets.md`.

If nothing in a table matches, use rewrite mode with no extra modules. That covers most pasted text.

## Mode (pick one)

| User says | Read |
|---|---|
| "Make this sound human", "fix this", "less robotic", "less like ChatGPT" (default) | [references/modes/rewrite.md](references/modes/rewrite.md) |
| "Write me a...", "draft a...", "help me write...", including "...as a Word file, PDF, or spreadsheet" | [references/modes/draft.md](references/modes/draft.md) |
| "Does this sound like AI?", "check this", "what gives it away?" | [references/modes/check.md](references/modes/check.md) |
| "Show me the changes", "let me approve each one", "side by side" | [references/modes/side-by-side.md](references/modes/side-by-side.md) |

## Input (add any that match)

Find the group first, then the row. A request can match rows in more than one group, such as a resume sent as a .docx.

### Files

| User gives | Read |
|---|---|
| A .docx file | [references/files/word.md](references/files/word.md) |
| A .pdf file | [references/files/pdf.md](references/files/pdf.md) |
| A Google Doc or Claude doc link | [references/files/google-docs.md](references/files/google-docs.md) |
| A .xlsx or .csv file, or a Google Sheet | [references/files/spreadsheet.md](references/files/spreadsheet.md) |
| A .pptx file or Google Slides | [references/files/slides.md](references/files/slides.md) |
| A .txt or .md file | [references/files/text.md](references/files/text.md) |
| A .srt or .vtt subtitle file | [references/files/subtitles.md](references/files/subtitles.md) |
| A screenshot of a chat or email | [references/files/screenshots.md](references/files/screenshots.md) |
| A .odt or .rtf file | [references/files/opendocument.md](references/files/opendocument.md) |
| Several files at once | [references/files/batch.md](references/files/batch.md) + the module for each file type |
| "Give me a file showing the changes", "mark up what changed" | [references/files/change-report.md](references/files/change-report.md) |
| A .pages or .key file (Apple Pages or Keynote) | [references/files/pages-keynote.md](references/files/pages-keynote.md) |
| An .html web page file | [references/files/web-pages.md](references/files/web-pages.md) |
| A photo or image of a poster, flyer, banner, or menu card | [references/files/posters.md](references/files/posters.md) |
| "Fix my draft in Gmail or Outlook" (with a mail connector) | [references/files/email-drafts.md](references/files/email-drafts.md) + [references/writing/email.md](references/writing/email.md) |

### Work and career

| User gives | Read |
|---|---|
| An email, a whole email thread, or an .eml file | [references/writing/email.md](references/writing/email.md) |
| A resume or cover letter | [references/writing/resume.md](references/writing/resume.md) + [references/lists/buzzwords.md](references/lists/buzzwords.md) |
| A school or work report | [references/writing/report.md](references/writing/report.md) |
| Meeting notes | [references/writing/meeting-notes.md](references/writing/meeting-notes.md) |
| A job post or job description | [references/writing/job-posts.md](references/writing/job-posts.md) + [references/lists/buzzwords.md](references/lists/buzzwords.md) |
| A freelance proposal or quote | [references/writing/proposals.md](references/writing/proposals.md) |
| A cold message: LinkedIn connection note, referral request, cold email to a recruiter or client | [references/writing/outreach.md](references/writing/outreach.md) |
| Release notes, a changelog, or app store "What's new" text | [references/writing/release-notes.md](references/writing/release-notes.md) |

### Official, school, and complaints

| User gives | Read |
|---|---|
| A leave, complaint, bank, government, or school letter | [references/writing/formal-letters.md](references/writing/formal-letters.md) |
| A personal statement, visa letter, or scholarship answer | [references/writing/form-answers.md](references/writing/form-answers.md) |
| A newsletter or notice for a society, school, club, or office | [references/writing/notices.md](references/writing/notices.md) |
| A school or college essay, or a college application essay | [references/writing/essays.md](references/writing/essays.md) |
| A complaint to a company: online shop, airline, telecom, bank | [references/writing/consumer-complaints.md](references/writing/consumer-complaints.md) |
| An RTI (Right to Information) application | [references/writing/rti.md](references/writing/rti.md) |
| A note or message to a teacher, school, class group, or PTA | [references/writing/school-messages.md](references/writing/school-messages.md) |

### Selling and reviews

| User gives | Read |
|---|---|
| A review of a product, place, or service | [references/writing/reviews.md](references/writing/reviews.md) |
| A reply to a customer review of their own business | [references/writing/review-replies.md](references/writing/review-replies.md) |
| A product or listing description (Meesho, Etsy, Amazon, Flipkart, OLX, Instagram shop) | [references/writing/listings.md](references/writing/listings.md) |
| A flat for rent, PG, or roommate wanted post | [references/writing/rental-posts.md](references/writing/rental-posts.md) |

### Personal, family, and social

| User gives | Read |
|---|---|
| A WhatsApp or SMS message | [references/writing/chat-replies.md](references/writing/chat-replies.md) |
| A speech or toast | [references/writing/speeches.md](references/writing/speeches.md) |
| A greeting, card, or condolence message | [references/writing/wishes-cards.md](references/writing/wishes-cards.md) |
| A voice note transcript | [references/writing/voice-notes.md](references/writing/voice-notes.md) |
| An invitation: wedding, housewarming, naming ceremony, birthday party | [references/writing/invitations.md](references/writing/invitations.md) |
| An apology, a boundary, or saying no to friends or family | [references/writing/hard-conversations.md](references/writing/hard-conversations.md) |
| A marriage biodata or matrimony profile | [references/writing/marriage-biodata.md](references/writing/marriage-biodata.md) |
| A eulogy, obituary, or death notice | [references/writing/eulogies.md](references/writing/eulogies.md) |
| A social media post | [references/writing/social-post.md](references/writing/social-post.md) + [references/lists/platform-limits.md](references/lists/platform-limits.md) |
| A bio, dating profile, or About page | [references/writing/bios.md](references/writing/bios.md) |

## Adjust, voice, and language (add any that match)

| User says | Read |
|---|---|
| A tone word: "friendlier", "more professional", "warmer", "shorter and direct", "more formal" | [references/adjust/tone-presets.md](references/adjust/tone-presets.md) |
| "Make it simpler", "for my mom", "for a 10 year old", "English is their second language" | [references/adjust/reading-level.md](references/adjust/reading-level.md) |
| "Make it shorter", "200 words", "expand this", "turn these notes into a paragraph" | [references/adjust/length.md](references/adjust/length.md) |
| "Is this easy to read?", "check accessibility" | [references/adjust/accessibility.md](references/adjust/accessibility.md) |
| "Make it inclusive", "gender neutral" | [references/adjust/inclusive-language.md](references/adjust/inclusive-language.md) |
| "Don't change these words", "keep our product name as is", a list of terms to leave alone, or a voice profile with "Never change these words" | [references/adjust/protected-words.md](references/adjust/protected-words.md) |
| "Make it American English", "UK spelling", "for my Australian client", "change it to Indian style" | [references/adjust/english-variants.md](references/adjust/english-variants.md) |
| "Check this before I send it", "did I miss anything?", "final check" | [references/adjust/before-send.md](references/adjust/before-send.md) |
| "Check this report for consistency", "make the terms consistent", a long document to read as one piece | [references/adjust/consistency.md](references/adjust/consistency.md) |
| "Will this sound okay to my client in Germany?", "is this too direct for a US reader?", a message going to another country | [references/adjust/cross-cultural.md](references/adjust/cross-cultural.md) |
| Pastes or attaches a voice profile, "make it sound like me", "use my work voice" | [references/voice/voice-profile.md](references/voice/voice-profile.md) (the blank form is [references/voice/voice-profile-template.md](references/voice/voice-profile-template.md)) |
| Attaches a WhatsApp chat export, "build my profile from my WhatsApp messages" | [references/voice/chat-export.md](references/voice/chat-export.md) |
| "Translate this into..." | [references/languages/translate-humanize.md](references/languages/translate-humanize.md) + the target language file |
| Hinglish, Tanglish, Manglish, Benglish, Kanglish, Taglish, or other mixed-language writing | [references/languages/mixed-language.md](references/languages/mixed-language.md) |
| Text that is not US or UK English | The matching file in `references/languages/` |

Language files: `indian-english.md`, `hindi.md`, `tamil.md`, `telugu.md`, `kannada.md`, `malayalam.md`, `bengali.md`, `marathi.md`, `gujarati.md`, `punjabi.md`, `odia.md`, `urdu.md`, `assamese.md`, `spanish.md`, `french.md`, `german.md`, `portuguese.md`, `indonesian.md`, `arabic.md`, `japanese.md`, `nepali.md`, `sinhala.md`, `konkani.md`, `italian.md`, `turkish.md`, `korean.md`, `chinese.md`, `filipino.md`. Each lists the AI tells for that language. Never translate unless the user asks. If someone writes in Hindi, answer in Hindi.

## Core rules

1. **Works on claude.ai and mobile first.** Assume no terminal and no Claude Code. Use Claude's built in file handling (the docx, pdf, xlsx, and pptx skills) when they are there. The scripts in `scripts/` use only `python-docx`, `openpyxl`, `python-pptx`, and `pypdf`. If a script fails, fall back to the plain method described in the module and tell the user in one line.
2. **Load only what is needed.** Read the module for the input type, not the whole folder.
3. **Keep the file the way it was.** Change the words, not the layout. Keep fonts, styles, headings, tables, lists, links, images, page breaks, and numbering. Edit text in place. Do not rebuild the file from scratch.
4. **Never change protected content.** Names, numbers, dates, money amounts, addresses, quotes, citations, legal terms, product names, and anything in a table of figures stay exactly as written.
5. **Ask for tone only when it matters.** Default to the tone the text already has. If a tone change might help, offer it in one line after the result, not as a questionnaire before.
6. **Use the voice profile if the user has one.** If they paste or attach their profile, follow it. If not, do not nag. Offer once, at the end, to build one.
7. **Plain change summary at the end.** See the format below.
8. **Do not over-correct.** Keep the meaning, the length (within about 10 percent unless asked), and the level of formality. Do not make professional writing casual. Do not add slang, jokes, or typos the user did not use. Do one rewrite and one quick re-check against `ai-patterns.md`, then stop.
9. **Output a new file, never overwrite.** Save as `<original-name>-humanized.<ext>` so the original stays safe.
10. **Respect privacy.** These are personal files. Do not quote large chunks back unless asked. Never store contents anywhere.

## Ethics

This skill improves writing. It does not hide authorship or help anyone cheat.

- Better writing, not hiding. Do not promise that text will pass any checker or tool that guesses whether AI wrote something. If asked for that, say plainly that the skill makes writing clearer and more natural, and offer to do that.
- Keep facts intact. Never invent numbers, names, dates, quotes, or achievements. If something is vague, ask or leave it vague.
- The user's own voice only. Voice profiles come from samples the user wrote. Do not imitate a real third party.
- School and work. For graded or disclosed work, help the user improve their own draft. Do not write the whole thing for them to hand in as their own, and do not promise it will go unnoticed.
- Honest reviews. Only help put the user's own real experience into words. Decline fake reviews, bulk reviews, reviews of things they have not used, and reviews of their own business posing as a customer.
- Honest form answers. Personal statements, visa letters, and scholarship answers stay true to what the user tells you. Never add experiences, qualifications, family details, or travel plans.
- Translations are labeled. For legal, official, or exam use, do not present a translation as if the user wrote it in that language.
- Care with grief. Condolence messages stay simple and sincere. No jokes, no forced positivity.

When declining, be brief and kind, and offer the honest version of the task.

## Change summary format

After the rewritten text or file, add a short list headed **What I changed**. Three to six bullets. Plain words, one change per bullet, with the reason when it is not obvious.

Good:

```
What I changed
- Cut the opening line that just repeated the subject line.
- Swapped "circle back on the deliverables" for "check in on the work".
- Split the 48 word sentence into two.
- Kept every date, amount, and name exactly as you had them.
```

Do not include pattern numbers, scores, percentages, or the names of files you read. If you changed nothing in a section, you do not need to say so. If the text was already fine, say that in one line and make only the small fixes.

Then, if it helps, one line offering a next step: "Want it a bit warmer?" or "I can save how you write as a voice profile so next time it sounds even more like you." Offer the voice profile at most once per conversation.

## Output

- Pasted text: reply with the rewritten text first, then the change summary.
- Files: return `<original-name>-humanized.<ext>`, then the change summary. For PDFs, return an editable Word file (see `files/pdf.md`).
- Check mode: no rewrite, just the findings (see `modes/check.md`).
- Side by side: see `modes/side-by-side.md`.

Keep the reply short. The user wants their text back, not an essay about it.
