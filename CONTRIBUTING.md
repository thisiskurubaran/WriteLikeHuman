# Contributing to WriteLikeHuman

Thanks for helping. This project makes everyday writing sound like a person wrote it, so the bar for our own files is the same: plain, clear, and human.

You do not need to be a developer to help. Many of the most useful contributions are a single new example or one AI habit we missed.

## Ways to help

### Suggest a new AI tell

An AI tell is a habit that makes writing sound machine made, like opening every email with "I hope this email finds you well" or ending every post with a one-line moral.

1. Open an issue using the **Feature request** template, or edit `write-like-human/references/ai-patterns.md` directly.
2. Give it a plain name.
3. Say in one or two sentences why it reads as AI.
4. Add a short before and after, using made up text.

### Suggest a new file type or writing type

Open a **Feature request** issue. Tell us what people would give the skill (a file, a kind of message) and what they would expect back. If you want to write the module yourself, see the module format below.

### Suggest or improve a language

Each language has its own file in `write-like-human/references/languages/`. The most helpful thing a native speaker can add is a list of phrases that sound machine translated or stiff, with natural versions next to them. Never add a rule that makes the skill translate when the user did not ask.

### Help wanted

Two things we can't do well without you:

- Screenshots for the install guide. If you have the skill installed, take a screenshot of each upload step in [INSTALL.md](INSTALL.md) (Settings, Capabilities, Customize, Skills, Upload a skill). Crop out your name, email, and chat history, then attach them to an issue or a pull request.
- Native speaker review. None of the language files have been checked by a native speaker yet. If you speak one of the languages in `write-like-human/references/languages/`, read its file and fix anything that sounds wrong. Each file ends with a "Help wanted" note until someone has reviewed it. Remove that note in your pull request once you have.

## How the skill is organized

The skill lives in the `write-like-human/` folder. That folder is what gets zipped and uploaded.

```
write-like-human/
├── SKILL.md          the router: reads the request and picks modules
├── references/
│   ├── ai-patterns.md   the catalog of AI tells, always loaded
│   ├── modes/           rewrite, draft, check, side by side
│   ├── files/           Word, PDF, Google Docs, spreadsheets, slides
│   ├── writing/         email, letters, resumes, posts, speeches, and more
│   ├── adjust/          tone, reading level, length, accessibility, inclusive wording
│   ├── voice/           personal voice profiles
│   ├── lists/           buzzwords and platform limits
│   └── languages/       one file per language, plus translation and mixed language
├── scripts/          small Python helpers for Office files and word counts
└── examples/         before and after samples and test prompts
```

`SKILL.md` stays short. It holds the routing tables, the core rules, and the change summary format. Everything else goes in `references/` so Claude reads only what a request needs.

If you add a module, link it from the right table in `SKILL.md`. A module nobody links to never gets loaded.

## Module format

Every module uses the same sections, in this order:

1. **When this applies**: what the user gives or says that loads this module.
2. **What stays the same**: the things this module must never change.
3. **Steps**: what Claude does, in order.
4. **Output**: what the user gets back.
5. **Example**: one short before and after in everyday language.

Scripts must use only `python-docx`, `openpyxl`, `python-pptx`, and `pypdf`, since those are what claude.ai has. Every script needs a plain fallback written into its module, in case it fails. Scripts write a new file and never overwrite the original.

## Style rules

These apply to every file in the repo.

- No em dashes or en dashes. Use a comma, colon, period, parentheses, or a plain hyphen. When a file needs to talk about them, write the words "em dash" or "en dash" instead of the character.
- Write like a person. Avoid filler openers ("In today's fast-paced world", "Let's dive in", "Whether you're a..."), "not just X, but Y" contrasts, forced groups of three, one-line dramatic closers, and sales language.
- Avoid stock words: delve, leverage, robust, seamless, elevate, unlock, empower, game-changer, cutting-edge, comprehensive, crucial, tapestry, realm, testament. The pattern catalog and buzzword list may name them on purpose.
- No emoji in headings. No bold label on every bullet.
- Plain English for a general audience. If a technical word cannot be avoided, explain it in the same sentence.
- Short sentences. Concrete examples over abstract claims.
- No real personal data. Use made up names, companies, numbers, and addresses.

## Ethics rules

The skill improves writing. It does not hide who wrote something or help anyone cheat. Pull requests that break these will not be merged.

- No features aimed at fooling tools that guess whether AI wrote a text. Do not name such tools as a goal, and do not add tricks meant to beat them.
- No impersonation. Voice profiles learn the user's own voice from samples they wrote, never a real third party.
- Honest school and work use. The skill helps people improve their own drafts. It does not promise that anything will go unnoticed.
- Keep facts intact. Never invent numbers, names, dates, quotes, or achievements.
- Honest reviews only. No fake reviews, bulk reviews, reviews of things the user has not used, or reviews of the user's own business posing as a customer.
- Honest form answers. Personal statements, visa letters, and scholarship answers stay true to what the user says.
- Translations are labeled honestly where disclosure matters (legal, official, or exam use).
- Care with grief. Condolence messages stay simple and sincere.

## Commit messages

We use [Conventional Commits](https://www.conventionalcommits.org/).

- Format: `type(scope): short summary`
- Types: `feat`, `fix`, `docs`, `refactor`, `chore`, `test`
- Scope is the module or area, like `feat(pdf): handle scanned pages`
- Summary in the imperative, lowercase, no period at the end, under 72 characters
- Add a body when the reason is not obvious. Wrap it at 72 characters.
- One logical change per commit.

Example:

```
feat(spreadsheet): skip cells that hold numbers or formulas

Only text cells, notes, and comments get rewritten. Touching a
formula cell could silently break someone's budget.
```

## Checks before you open a pull request

Run these from the repo root and fix anything they find:

```bash
# Use a UTF-8 locale, or the dash check below fails quietly and finds nothing
export LC_ALL=C.UTF-8

EX="--exclude-dir=.git --exclude=CONTRIBUTING.md --exclude=ai-patterns.md --exclude=buzzwords.md"

# Em and en dashes
grep -rnP '\x{2014}|\x{2013}' --exclude-dir=.git . && echo "FIX: dashes found"

# Stock words outside the lists that name them on purpose
grep -rniwE "delve|leverage|seamless|robust|elevate|unlock|empower|tapestry|game-changer|cutting-edge|testament" $EX .

# Language about fooling AI checkers
# (the brackets keep this file from matching its own search)
grep -rniE "gpt[z]ero|turn[i]tin|undetect[a]ble|by[p]ass|100% hu[m]an|ai detec[t]or" --exclude-dir=.git . && echo "FIX: checker language found"

# Skill name matches the folder
grep -q "^name: write-like-human$" write-like-human/SKILL.md || echo "FIX: name mismatch"

# Every module is linked from SKILL.md (language files are linked as a group)
for f in $(cd write-like-human/references && find . -name '*.md' | sed 's|^\./||'); do
  case "$f" in languages/*) continue;; esac
  grep -q "$f" write-like-human/SKILL.md || echo "FIX: $f not linked from SKILL.md"
done
```

Then test your change: zip the `write-like-human/` folder, upload it to Claude, and try two prompts a normal person would type, plus one that should not use the skill. Add those prompts to `write-like-human/examples/test-prompts.md`.

## Code of conduct

By taking part you agree to follow our [Code of Conduct](CODE_OF_CONDUCT.md).
