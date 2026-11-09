# Working in a code repository

How to handle README files, docs, and comments when Claude Code has the project open. This changes one core rule: inside a git repository, edit files in place instead of making a `-humanized` copy, because git keeps the old version and every change can be reviewed and undone.

## When this applies

- The user is in Claude Code (or another agent with file access) and the files are in a folder under git.
- Any developer guide (README, docs, architecture, API docs and UI text, code comments) is loaded.

## What stays the same

- Code. Never change code, config values, commands, or anything inside code blocks while working on the words. The skill only touches prose: Markdown text, comments, docstrings, and string values meant for people.
- Git history and state. Don't commit, push, switch branches, stash, or reset unless the user asks.
- Files you weren't asked about.

## Steps

1. Check whether the folder is a git repository: `git rev-parse --is-inside-work-tree`. If it isn't, or git isn't available, use the normal rule: write a `-humanized` copy and never overwrite.
2. Check the file has no unsaved work you'd mix in: `git status --short FILE`. If it already has uncommitted changes, ask before editing, or make a `-humanized` copy.
3. Edit the file in place with your file editing tools. For code comments, use `scripts/code_comments.py apply FILE changes.json --in-place`, which refuses unless the file is tracked and clean.
4. Tell the user in one line that you edited the file in place, and how to see or undo it: "Edited README.md in place. Run `git diff README.md` to see the changes, or `git checkout README.md` to undo them."
5. Commit only if the user asks, using `developer/commits-and-prs.md` for the message.

## Output

The edited file, plus the one line about how to review or undo, plus the usual short change summary.

## Example

User (in Claude Code): "Make our CONTRIBUTING.md sound less robotic."

You check the repo, see CONTRIBUTING.md is clean, edit it in place, and reply:

> Edited CONTRIBUTING.md in place. Run `git diff CONTRIBUTING.md` to see the changes.
>
> What I changed
> - Cut the "Feel free to" and "Please note" openers.
> - Turned the setup paragraph into numbered steps with the same commands.
