# Commit messages and pull request descriptions

Write commit messages and pull request (PR) descriptions that say what changed and why, in a few plain lines.

## When this applies

- "Write a commit message for this", "write the PR description", "make my PR sound less robotic".
- The user pastes a diff, a list of changes, or a draft message.
- In Claude Code, the user asks for a message for the staged changes.

Load `lists/buzzwords.md` (the developer section) with this guide.

## What stays the same

- What actually changed. Describe only changes that are in the diff or that the user describes. Never claim tests were added, run, or passed unless they were.
- Issue numbers, ticket ids, names of functions, files, and flags, exactly as written.
- The repo's own convention. If recent commits use Conventional Commits (`fix(auth): ...`), a ticket prefix (`ABC-123: ...`), or a sign-off line, follow it. Check with `git log --oneline -15` in Claude Code, or ask.

## Steps

1. Read the diff, or ask for it. In Claude Code, run `git diff --staged` (or `git diff` if nothing is staged). Don't commit anything yourself unless the user asks.
2. Find the one main change and the reason for it. If the reason isn't clear from the diff or the user, ask in one line rather than invent it.
3. Commit message: a summary line under about 72 characters, in the imperative ("Fix", "Add", "Remove"), with no period. Then, only if it helps, a blank line and two to four lines on why, wrapped at about 72 characters.
4. PR description: what changed (two to five bullets), why, and how to check it (the steps or tests the user mentioned). Add "Notes for reviewers" only if there's something risky or unfinished. Follow the repo's PR template if there is one.
5. Cut the tells: "This PR introduces a comprehensive...", "enhances", "various improvements", "Updated code".
6. Split advice: if the diff mixes unrelated changes, say so in one line and offer separate messages.

## Output

The commit message or PR description as plain text in a code block, ready to paste, then one or two lines on what you based it on. No change summary list for a commit message unless the user gave you a draft to fix.

## Example

Before (user's draft):

> This commit introduces comprehensive enhancements to the login flow, robustly addressing various issues and improving the overall user experience.

The diff disables the submit button while the login request is in flight.

After:

> fix(login): stop double submit while signing in
>
> The button stayed active during the request, so a second tap sent
> another login and showed a "session expired" error.

What I changed
- Said exactly what the fix does, from the diff.
- Used the repo's `fix(scope):` style.
