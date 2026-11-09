# Code comments and docstrings

Rewrite comments and docstrings so they say what a reader needs, usually why, in plain words. The code never changes.

## When this applies

- "Clean up the comments in this file", "make these docstrings clearer", "the comments sound like AI wrote them".
- A code file pasted in or open in Claude Code, where the user wants only the comments improved.
- Not for writing or changing code. If the user wants code changes, that's ordinary coding help, not this skill.

Load `lists/buzzwords.md` (the developer section) with this guide. In Claude Code inside a git repo, also load `developer/repo-files.md`.

## What stays the same

- Every character of code. Only comment and docstring text changes.
- Licence and copyright headers, shebangs, encoding lines, and tool directives (`noqa`, `type: ignore`, `eslint-disable`, `@ts-ignore`, `//go:build`, `prettier-ignore`).
- Commented-out code. Leave it, even if it looks messy. Removing it is the user's call.
- Doc tags and sections: `@param`, `@returns`, `:param x:`, `Args:`, `Returns:`, `Raises:`, and the names and types in them. Change only the prose after them.
- TODO, FIXME, and ticket references, word for word.

## Steps

1. Run `python scripts/code_comments.py extract FILE`. It lists each comment and docstring with an id (c1, c2, ...), its line, and its text without the comment markers. Entries marked `"skip"` are licences, directives, or commented-out code: leave them alone.
2. Rewrite only the comments that need it. Good comments say why the code does something, warn about a trap, or explain a non-obvious rule. Comments that only repeat the code (`# loop over the items`) are better deleted. The script never removes comments, so list them for the user to delete.
3. Keep each comment about as long as it was, or shorter. Keep the same language (if comments are in Spanish, write Spanish).
4. Save the changes as JSON (`{"c3": "new text", ...}`) and run `python scripts/code_comments.py apply FILE changes.json`. It writes `<name>-humanized.<ext>`, puts each comment back in its original style and indentation, and refuses to write anything if the code would change. In Claude Code inside a git repo, add `--in-place` (see `developer/repo-files.md`).
5. A `SKIPPED` line means a change would have broken the comment (for example `*/` inside a block comment). Fix it or leave that comment.

## Output

The new file (or the in-place edit), then a short change summary with how many comments changed, and a list of comments you'd suggest deleting.

## If the script fails

Rewrite the comments by hand, changing only the text after the comment markers. Then compare the old and new code with the comments removed, line by line, before giving it back. Tell the user in one line that you did it by hand.

## Example

Before:

```python
# This function is responsible for robustly handling the calculation of the total
def total(items):
    # Loop through each item
    return sum(i.price * i.qty for i in items)  # Note that prices are in paise so no rounding is needed
```

After:

```python
# Adds up the order total.
def total(items):
    # Loop through each item
    return sum(i.price * i.qty for i in items)  # Prices are in paise, so no rounding is needed.
```

(The comment "Loop through each item" is listed for the user to delete, since it repeats the code.)

What I changed
- Said what the function does in four words.
- Kept the fact about paise, without "Note that".
- Suggested deleting one comment that repeats the code.
