# Changelog

All notable changes to this project are written down here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Draft mode can hand back a new Word file, PDF, or spreadsheet when asked. The skill writes the words and Claude builds the file.

### Changed

- The website has its own icon, a speech bubble with a hand-drawn line, in the header and the browser tab.
- A simpler, more modern website with a bento grid of interactive examples, a typing prompt bar, and a language marquee.
- The website has a new section on creating and editing Word, PDF, and Excel files, and larger tap targets on phones.

### Fixed

- The website now lays out at the phone's real width. A chat mock-up in the hero was forcing every phone to 444 pixels wide and zooming the page out.
- On phones, the website's "New" badge stays on one line, the footer has full-width buttons, and page content no longer shows above the floating menu bar.

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

[Unreleased]: https://github.com/thisiskurubaran/WriteLikeHuman/compare/v0.3.1...HEAD
[0.3.1]: https://github.com/thisiskurubaran/WriteLikeHuman/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/thisiskurubaran/WriteLikeHuman/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/thisiskurubaran/WriteLikeHuman/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/thisiskurubaran/WriteLikeHuman/releases/tag/v0.1.0
