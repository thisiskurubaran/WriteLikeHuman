# Tests

These tests check the helper scripts in `write-like-human/scripts/`: that formatting, formulas, numbers, and subtitle timings survive a rewrite, that originals are never overwritten, and that the chat export filter keeps only one person's messages and hides phone numbers, emails, and links. Every sample file is made up and created in a temporary folder while the tests run, so no real documents are stored here.

To run them, install the four libraries the scripts use with `pip install python-docx openpyxl python-pptx pypdf`, then run `python -m unittest discover -s tests -v` from the top folder of the repository. Tests whose library is missing are skipped with a note instead of failing.
