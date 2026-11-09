# Changelog

All notable changes to this project are written down here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Size budgets for SKILL.md, the pattern catalog, and every guide, checked on every pull request, so the skill stays quick.
- Hindi, Tamil, and Hinglish eval cases for payment reminders, support replies, and personalised messages.
- "How does this sound?" mode: a calm reading of a message someone else sent, with no invented intent, then help replying.
- Negotiation messages for salary, prices, and rent, using only your real numbers and reasons.
- Recommendation and reference letters written from what the recommender actually saw.
- Scripts and descriptions for YouTube videos, Reels, and Shorts, written to be spoken.
- Easy Read: a simple accessible format with one idea per line and picture suggestions.
- Keeping your voice profile or house style in a Claude Project so it applies without attaching it each time.
- Long documents: theses, manuals, and long reports handled section by section, with names and terms kept consistent and nothing dropped.
- Dyslexia-friendly layout for Word files: clear font, wider spacing, left alignment, and no long italics. The words don't change.
- Voice profiles from Telegram and Signal chat exports, as well as WhatsApp.
- LaTeX files: prose rewritten while commands, maths, and citations stay exactly as they were.
- Eval cases and test prompts for every v0.6.0 guide (146 cases in all).

### Changed

- The router links every v0.6.0 guide.

## [0.5.0] - 2026-11-09

### Added

- A GitHub workflow you start by hand that runs the evals with your API key and attaches the score. It never runs on its own.
- Script conversion: write the same words in Hindi, Tamil, or another Indian script, or back into Roman letters, without translating.
- Payment reminders and invoice notes, with amounts, invoice numbers, and due dates kept exactly as given.
- Customer support replies for small businesses, with no refunds or dates promised that the owner didn't approve.
- Out-of-office and away messages, WhatsApp Business greetings, and email signatures.
- Alt text for images: describes what is visible and never guesses who people are.
- A quick starter voice profile from just three messages, which can grow later.
- Personalised messages from a spreadsheet: one draft per person using their name, saved to a file. Nothing is sent, and it's only for people you already know.
- Explanations as Word comments: each change can come with a short margin note saying why.
- Google Sheets and Google Slides edited in place when a Google connector is attached, on a copy unless you say otherwise.
- Golden-file tests for form filling, web pages, and Word comments, and tests for the new message script.
- Eval cases and test prompts for every v0.5.0 guide, including a decline case for bulk messages to a bought list (131 cases in all).
- The scripts that build the Hindi, Tamil, examples, and guide pages are in the repo, and a check fails if those pages fall out of date with the English page.
- A How do I guide on the website with short steps for every common task, and a What's new section on the home page.

### Changed

- Python cache folders and Node packages are ignored, so test runs no longer leave untracked files.
- GitHub Actions in the workflows are pinned to exact versions, and Dependabot keeps those pins up to date.
- The router links the new writing types, alt text, and script conversion.
- A tighter skill description that leads with the most common requests and leaves room for future features.
- The README lists every v0.5.0 feature.
- Hindi and Tamil README brought up to date with v0.5.0.

## [0.4.0] - 2026-11-09

### Added

- The eval runner can save a score summary per release (--save v0.4.0), so pass rates can be compared over time.
- Golden-file tests that prove everything you didn't ask to change in a Word, Excel, or PowerPoint file stays byte for byte the same.
- Sindhi, Maithili, Vietnamese, Thai, and Swahili language guides, and a section on formal and official Hindi.
- Singapore, Nigerian, Kenyan, Philippine, and South African English, kept as the user writes them.
- Reply options for tricky messages: one reply plus a single tone offer, never a pile of versions.
- Voice profiles can be built from Word, PDF, or text files the user wrote.
- Team style guides: a shared house style for a small business or team, with a fill-in template.
- Explain mode: ask why any single change was made and get a plain answer, with an offer to undo it.
- Learning mode: a short lesson on the three most noticeable habits in your own text, so you can write better yourself.
- Six more kinds of writing: event announcements, rental agreements in plain words, product FAQs, school circulars, grievance letters to an employer, and insurance claims.
- Create PowerPoint decks from notes: short slide text, fuller speaker notes, and no invented figures.
- Fill a Word or PowerPoint template, such as a letterhead or a resume layout, keeping its look.
- Fill in forms: fillable PDFs and Word forms, with personal details never guessed and missing answers listed.
- Scanned PDF pages are read from their images, and names and numbers read that way are confirmed with the user.
- Photos of handwritten notes, whiteboards, and letters turned into typed text, with unclear words marked instead of guessed.
- A router check that every guide can be reached and every link and example points at a real guide.
- Eval cases and test prompts for every new v0.4.0 guide (124 cases in all).
- An examples page on the website: every before and after sample, searchable and filterable by kind of writing.
- Hindi and Tamil versions of the website, labeled as translations of the English page.
- A feedback form for saying what worked and what didn't, without sharing personal text.

### Changed

- The skill description names the new abilities (forms, templates, scanned PDFs, handwriting, and creating files) so those requests trigger it.
- The Claude Code plugin now installs only the skill folder (about 670 KB), not the website, tests, and translations.
- SKILL.md is about a fifth shorter. The kinds-of-writing tables moved to a lookup file that is read only when needed, so every request costs fewer tokens.
- The README lists every v0.4.0 feature and links the new examples page.

## [0.3.2] - 2026-11-08

### Added

- Draft mode can hand back a new Word file, PDF, or spreadsheet when asked. The skill writes the words and Claude builds the file.
- Eleven more chatbot habits in the pattern catalog, including template letter phrases, biodata and listing cliches, and engagement-bait endings.
- Eval cases for every language guide and the pattern catalog, so all 94 guides are covered (103 cases).
- Before and after samples for creating a Word file and a spreadsheet.
- A social preview image, so links to the website show a picture on WhatsApp, LinkedIn, and X.
- A check on every pull request that loads the website at phone, tablet, and desktop sizes in Chromium and WebKit and fails if it doesn't fit the screen.

### Changed

- The website has its own icon, a speech bubble with a hand-drawn line, in the header and the browser tab.
- A simpler, more modern website with a bento grid of interactive examples, a typing prompt bar, and a language marquee.
- The website has a new section on creating and editing Word, PDF, and Excel files, and larger tap targets on phones.
- The README shows how to create new Word, PDF, and Excel files, not only edit existing ones.

### Fixed

- The website now lays out at the phone's real width. A chat mock-up in the hero was forcing every phone to 444 pixels wide and zooming the page out.
- On phones, the website's "New" badge stays on one line, the footer has full-width buttons, and page content no longer shows above the floating menu bar.
- The website's numbers were typed by hand and had gone stale (81 test cases instead of 103). A test now checks them against the repo.

## [0.3.1] - 2026-11-07

### Added

- Checks that every module has the standard sections, that the newest changelog section has entries, and that the plugin version matches the changelog.
- Eval cases for every writing, file, adjust, voice, and mode module (81 cases in all).
- Ten more before and after samples covering the v0.2.0 and v0.3.0 modules.
- Web pages: image descriptions (alt text) and meta descriptions can be rewritten too, when asked.

### Changed

- The router's input table is split into groups (files, work, official, selling, personal) so the right module is easier to find.
- Hindi and Tamil README and install guide brought up to date, including the plugin install.
- Spreadsheets with charts: a plainer warning, and the option to get only the rewritten text cells back.
- A redesigned project website, with an interactive before and after, the plugin install, and every language.

### Fixed

- The skill description now names the newer writing types and files, so requests for them trigger the skill.
- Four modules now use the standard section headings, and the tone presets module has an Output section.
- PDF text keeps its paragraph breaks, including greeting lines and numbered lists.

## [0.3.0] - 2026-11-07

### Added

- Marriage biodata and matrimony profiles, warm and factual.
- Cold messages: LinkedIn notes, referral requests, and cold emails.
- Complaints to companies, with order numbers kept exact and an escalation path.
- RTI applications in the standard Indian format.
- Flat for rent, PG, and roommate posts with fair wording.
- Notes and messages to teachers, schools, and class groups.
- Eulogies and obituary notices, written with care.
- Release notes and app store "What's new" text.
- Interview thank-you notes as an email preset.
- A consistency check for long documents: terms, spelling, numbers, and headings.
- A cross-cultural check that notes what might read badly to a reader in another country.
- Two lengths at once, only when asked.
- Nepali, Sinhala, Konkani, Italian, Turkish, Korean, Chinese, and Filipino language guides, and Taglish in the mixed language guide.
- A before-you-send check: missing attachments, weekdays that don't match dates, unanswered questions, leftover placeholders.
- Speech timing per section, with optional pause marks in a reading copy.
- Apple Pages and Keynote files.
- Web pages: visible text rewritten, tags, links, and code left exactly as they were.
- Posters and flyers: a cleaner version of the text to retype.
- Gmail and Outlook drafts edited in place when a mail connector is attached. Nothing is ever sent.
- An optional eval runner that sends the evals through the Claude API with your own key.
- Releases build and attach WriteLikeHuman.zip automatically.
- A language review issue form for native speakers.
- Claude Code plugin: install with two commands instead of copying the folder.
- A simple project website in docs/, ready for GitHub Pages.

## [0.2.0] - 2026-11-07

### Added

- Replies to customer reviews for small business owners, written as themselves.
- Product and listing descriptions, with every fact taken from the seller.
- Invitations for weddings, housewarmings, naming ceremonies, and birthdays.
- Apologies, boundaries, and saying no to friends and family.
- Plain, inclusive job posts and job descriptions.
- Newsletters and community notices for societies, schools, clubs, and offices.
- Freelance proposals and quotes, with no invented clients or credentials.
- School and college essays, improved in the student's own words.
- Email threads: read the whole thread before drafting the reply.
- Protected words: a list of terms that must never change, kept on its own or inside a voice profile.
- Switching between US, UK, Australian, and Indian English.
- Ready-to-paste formatting for each social platform.
- Gujarati, Punjabi, Odia, Urdu, and Assamese language guides.
- Portuguese, Indonesian, Arabic, and Japanese language guides, with right-to-left notes for Urdu and Arabic files.
- Manglish, Benglish, and Kanglish examples in the mixed language guide.
- Plain text and Markdown files.
- Subtitle files (.srt, .vtt): only caption text changes, never the timings.
- Drafting replies from screenshots of chats and emails.
- OpenDocument and RTF files, returned as Word files when they can't be edited directly.
- Several files at once, with each file's facts kept separate.
- A Word file that marks every change, for any input.
- Building a voice profile from the user's own WhatsApp messages, with other people's messages dropped and contact details hidden.
- An optional reading age in the accessibility check, only when asked.
- Tests for every helper script, using sample files made at run time.
- Skill evals: prompts with expected behavior to run before each release.
- Automatic style, structure, and script checks on every pull request.
- Hindi and Tamil translations of the README and install guide, labeled as translations.

### Changed

- Language files and the contributing guide now ask native speakers to review them, and the guide asks for install screenshots.

### Fixed

- The dash check in the contributing guide now runs under a UTF-8 locale, so it no longer passes silently.

## [0.1.0] - 2026-11-07

### Added

- The WriteLikeHuman skill, shipped as one folder (`write-like-human/`) with a router that loads only the parts each request needs.
- A catalog of common AI writing habits, each with a plain explanation and a before and after.
- Four ways to work: rewrite, draft new text, check without changing, and side by side approval of each change.
- File support for Word, PDF (returned as an editable Word file), Google Docs and Claude docs, spreadsheets, and slides, with helper scripts that keep formatting and never touch numbers or formulas.
- Writing guides for emails, WhatsApp and SMS replies, Indian format letters, resumes and cover letters, social posts, bios, reports, meeting notes, speeches, wishes and cards, honest reviews, form answers, and voice note transcripts.
- Adjustments for tone, reading level, length (with an exact word count script), accessibility, and optional inclusive wording.
- Personal voice profiles, including more than one per person, with a fill-in template.
- Language guides for translation, Hinglish and other mixed writing, Indian English, Hindi, Tamil, Telugu, Kannada, Malayalam, Bengali, Marathi, Spanish, French, and German.
- Before and after samples and a list of test prompts.
- MIT license and a generic `.gitignore`.
- Install guide for claude.ai, the desktop app, the mobile app, and Claude Code.
- Contributing guide and Code of Conduct (Contributor Covenant 2.1).
- Security policy with private reporting.
- Issue templates for bugs and feature requests, and a pull request checklist.

[Unreleased]: https://github.com/thisiskurubaran/WriteLikeHuman/compare/v0.5.0...HEAD
[0.5.0]: https://github.com/thisiskurubaran/WriteLikeHuman/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/thisiskurubaran/WriteLikeHuman/compare/v0.3.2...v0.4.0
[0.3.2]: https://github.com/thisiskurubaran/WriteLikeHuman/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/thisiskurubaran/WriteLikeHuman/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/thisiskurubaran/WriteLikeHuman/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/thisiskurubaran/WriteLikeHuman/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/thisiskurubaran/WriteLikeHuman/releases/tag/v0.1.0
