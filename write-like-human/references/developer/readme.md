# README files

Write or rewrite a project README so a stranger understands what the project does and can get it running, in plain words.

## When this applies

- "Write a README for this project", "make my README less AI sounding", "clean up the README".
- A README.md, README.rst, or project page pasted in or open in Claude Code.
- A GitHub profile README or a package description (npm, PyPI) counts too.

Load `lists/buzzwords.md` (the developer section) with this guide. In Claude Code inside a git repo, also load `developer/repo-files.md`.

## What stays the same

- Every command, code block, file path, version number, URL, flag, environment variable, and config key, exactly as written. Never change text inside backticks or code fences.
- Badges that point somewhere real, the licence, and credits.
- What the project actually does. Never add a feature, platform, benchmark, or integration the user or the code doesn't show.
- The heading structure the user chose, unless they ask for a new one.

## Steps

1. Find out what the project is. Use the code, package files (package.json, pyproject.toml, go.mod, Cargo.toml), and what the user says. If you can't tell what something does, ask instead of guessing.
2. Open with one or two sentences: what it is and who it's for. "A command line tool that renames photos by the date they were taken." No "Welcome to", no slogan.
3. Use the sections a reader needs, in this order, and skip any that don't apply: what it does, install, quick start (the shortest working example), usage or configuration, contributing, licence.
4. Make every install and usage step something a person can copy and run. Use the real commands from the repo (scripts in package.json, a Makefile, the docs). If a step is missing, leave a clear `TODO` for the user instead of inventing one.
5. Cut the tells in the developer list: emoji on every heading, a wall of badges, "powerful", "seamlessly", "simply run", "Happy coding!".
6. Keep it short. A small project often needs under 300 words. Link to longer docs instead of pasting them in.

## Output

The README in Markdown, ready to save, then a short change summary. In Claude Code inside a git repo, edit README.md in place (see `developer/repo-files.md`). Elsewhere, give the text or save `README-humanized.md`.

## Example

Before:

> # 🚀 PhotoDate ✨
> PhotoDate is a powerful, next-generation solution that seamlessly leverages EXIF metadata to revolutionise how you organise your memories! 📸
> ## ⚡ Installation
> Simply run `pip install photodate` and you're good to go! 🎉

After:

> # PhotoDate
> A command line tool that renames photos by the date they were taken, using the date stored in each file.
> ## Install
> ```
> pip install photodate
> ```

What I changed
- Said what the tool does in one plain sentence.
- Removed the emoji and the sales words.
- Kept the install command exactly as it was.
