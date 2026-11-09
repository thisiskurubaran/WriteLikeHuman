# Website build scripts

The English landing page, `docs/index.html`, is the source for the whole site. These scripts keep the other pages in step with it. They use only the Python standard library. GitHub Pages doesn't publish this folder, because its name starts with an underscore.

| Script | What it does |
|---|---|
| `sync_site.py` | Runs everything below. Updates the numbers on the English page (guides, writing types, languages, test cases) from the repo, then rebuilds the Hindi, Tamil, examples, and guide pages. |
| `gen_lang.py` | Builds `docs/hi/index.html` and `docs/ta/index.html` from the English page, using the translation table `T` at the top of the file. |
| `gen_guide.py` | Builds `docs/guide.html`, the "How do I..." guide. The tasks are listed in `TASKS` at the top: edit them there. |
| `gen_examples.py` | Builds `docs/examples.html` from `write-like-human/examples/before-after.md`, reusing the landing page's styles, icons, nav, and footer. |

## Everyday use

Run from the repo root after you change `docs/index.html`, add a guide, add a test case, or add a sample to `before-after.md`:

```bash
python3 docs/_build/sync_site.py
```

Then commit the pages it changed. To check without changing anything (this also runs on every pull request):

```bash
python3 docs/_build/sync_site.py --check
```

## Changing a translation

Never edit `docs/hi/index.html` or `docs/ta/index.html` by hand, because the next build overwrites them. Instead, find the row in `T` in `gen_lang.py`. Each row is:

```python
("English text exactly as on the page", "Hindi text", "Tamil text", replace_all)
```

Edit the Hindi or Tamil part and run `sync_site.py`. If you change English text on the landing page, update the first part of its row too, or the build stops with a message naming the text it couldn't find. Native speakers are welcome to improve any row (see the "Help wanted" section in `CONTRIBUTING.md`).

## Adding an example

Add the sample to `write-like-human/examples/before-after.md`, then add its heading to a category in `CATS` in `gen_examples.py` so it gets the right filter tag, and run `sync_site.py`.

## Added in v0.6.0

- `gen_guide_i18n.py` holds the Hindi and Tamil text for the guide (`docs/hi/guide.html`, `docs/ta/guide.html`). Add a task to `gen_guide.py` and you must add it here too, or the build stops and names the missing task.
- `gen_privacy.py` builds `docs/privacy.html` from its `SECTIONS` list, using the guide's page frame.
- If `tests/evals/results/` holds a saved score (from `tests/run_evals.py --save`), `sync_site.py` shows the newest one by version under the stats on the English, Hindi, and Tamil landing pages. With no saved score, nothing is shown.
