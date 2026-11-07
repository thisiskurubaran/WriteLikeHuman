# Skill evals

`evals.json` is a list of prompts to try in Claude before each release. Each case says which parts of the skill should load, what the reply must do, and what it must not do.

## How to run them

1. Zip the `write-like-human/` folder and upload it to Claude (see [INSTALL.md](../../INSTALL.md)).
2. Start a new chat for each case and paste the `prompt`. Where a case says "attach a file", use a small made-up file. Never use real personal files.
3. Compare the reply with `must` and `must_not`. A case passes only if every `must` holds and no `must_not` happens.
4. For `should_load`, ask Claude at the end of the chat which reference files it read, or check its tool calls if your app shows them.
5. Write down any failures in the release pull request, and fix the module or the router table in `SKILL.md` before tagging.

## Adding a case

Add an object to `cases` with a unique `id`. Keep prompts in the words a normal person would type. If you add a module, add at least one case that should load it, and one prompt for something close to it that should not.

`tests/test_evals.py` checks that the file is valid and that every module it names exists, so a renamed module can't quietly break the list.
