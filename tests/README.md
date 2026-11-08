# Tests

These tests check the helper scripts in `write-like-human/scripts/`: that formatting, formulas, numbers, and subtitle timings survive a rewrite, that originals are never overwritten, and that the chat export filter keeps only one person's messages and hides phone numbers, emails, and links. Every sample file is made up and created in a temporary folder while the tests run, so no real documents are stored here.

To run them, install the four libraries the scripts use with `pip install python-docx openpyxl python-pptx pypdf`, then run `python -m unittest discover -s tests -v` from the top folder of the repository. Tests whose library is missing are skipped with a note instead of failing.

`tests/test_site.py` checks that the numbers on the website (how many guides, writing types, languages, and test cases) match the repository. `tests/site_layout.mjs` opens the website at phone, tablet, and desktop sizes in Chromium and WebKit and fails if the page is wider than the screen. It needs Playwright (`npm install --no-save playwright@1.63.0`, then `npx playwright install --with-deps chromium webkit`) and runs with `node tests/site_layout.mjs`. Both run on GitHub for every pull request.
