# Spreadsheets (.xlsx, .csv, Google Sheets)

## When this applies

The user attaches an Excel file (`.xlsx`) or a `.csv`, or shares a Google Sheet, and wants the writing in it to sound better. Typical cases: a notes or comments column in a budget, customer feedback replies, product descriptions in a catalogue, a project tracker with status updates, survey answers.

## What stays the same

Almost everything. A spreadsheet is mostly numbers and formulas, and one wrong edit can quietly break someone's budget.

Never touch:

- Numbers, money amounts, percentages
- Formulas (anything starting with `=`), and the results they show
- Dates and times
- True/false values, checkboxes, dropdown choices
- Codes and IDs, even when stored as text: phone numbers, PIN codes, invoice numbers, SKUs
- Column headers (other sheets, filters, and formulas may look them up by name)
- Text on hidden sheets, rows, or columns (marked `"hidden": true`), unless the user asks. Mention in one line that you left them alone.
- Sheet names, cell formatting, colours, column widths, filters, frozen rows
- Names, addresses, and the other protected content in the core rules

You may change:

- Text cells that hold sentences: notes, comments, descriptions, replies, status updates
- Cell comments (notes attached to a cell), if the user wants those done too

Short labels like "Done", "Pending", "North", "Total" are left alone. A rough rule: only rewrite cells with four or more words.

## Steps

1. **List the text cells:**
   ```
   python scripts/xlsx_text_cells.py extract <file>.xlsx --min-words 4 -o cells.json
   ```
   This works for `.csv` too. It only ever lists text. Numbers, formulas, dates, and codes are never in the list. Ids look like `Budget!E7` and `Budget!E7#comment`.
2. **Check the note on stderr.** If it says the workbook has charts, images, or pivot tables, stop and read "If something goes wrong" below before going further.
3. **Rewrite** each cell following `ai-patterns.md` and the mode module. Keep cells short. A note that was one line stays about one line. Keep the same tone across a column, so 200 replies don't each sound different.
4. **Keep it consistent.** If the same phrase repeats down a column ("Holistic end-to-end solution"), fix it the same way every time unless variety was the point.
5. **Write the changes** as JSON, id to new text, and apply:
   ```
   python scripts/xlsx_text_cells.py apply <file>.xlsx changes.json
   ```
   The script refuses any id that points at a number, formula, or date, so even a mistake cannot break the maths.
6. **Read the CHECK lines.** `numbers differ` means a number inside a sentence changed. Fix it.
7. **Quick re-check.** Formulas still there, totals unchanged, only the notes changed. Then stop.

### CSV files

A CSV has no formatting and no formulas, just text. The script keeps the separator (comma, semicolon, tab) and line endings as they were. Dates and numbers are still left alone. Keep commas and quotes inside cells safe by letting the script write the file, never by hand.

## With a Google connector

When the user links a Google Sheet and a Google Drive or Sheets connector is attached, edit the sheet itself instead of asking for a download.

1. Make a copy first, named `<title> (humanized)`, and edit the copy. Edit the original only if the user clearly says to.
2. Read the cells through the connector. Change only text cells, notes, and comments, by the same rules as above.
3. Never touch numbers, dates, formulas, or anything a formula refers to. If a cell shows text but holds a formula, leave it.
4. Write back only the cells you changed, one by one, so nothing else in the sheet moves.
5. Tell the user where the copy is and give the change summary.

Without a connector, ask the user to download it (**File > Download > Microsoft Excel (.xlsx)** or **Comma separated values (.csv)**), or to paste the column they want fixed. If they paste a column, give it back in the same order, one line per cell, so they can paste it straight back.

## Output

- Return `<original-name>-humanized.xlsx` (or `.csv`). The original is never overwritten.
- Then the change summary. Say which column or sheet you worked on, and confirm the numbers were left alone:
  > - Rewrote the 18 notes in the "Comments" column. Didn't touch any numbers, dates, or formulas.

## Example

A cell in the Notes column of `office-budget.xlsx`, next to a formula `=B2*C2` and an amount of 15000:

Before:
> This strategic investment will enable our team to foster collaboration and drive synergies.

Wrong rewrite (adds a fact that was never there):
> Pays for the shared meeting room so the team can work in one place.

Right rewrite:
> This spend should help the team work together better.

The formula and the 15000 stay exactly as they were.

## If something goes wrong

- **The script stops and asks for `--force`:** the workbook has charts, images, or pivot tables. The library the script uses (openpyxl) can quietly drop those when it saves, so the script won't save without your say-so. Tell the user plainly, for example: "Your sheet has charts. Saving it with my tool could remove them, so I've stopped before changing anything." Then offer a choice:
  1. Get only the rewritten text cells back as a list with cell references ("E2: ...", "E3: ...") or as a small CSV, to paste into their own file. Nothing in their workbook can break this way, so suggest it first.
  2. Use Claude's built in xlsx skill if it is there, which may keep the charts.
  3. Run with `--force` only if the user says the charts and images don't matter, and say again that they may be lost in the new copy (the original stays safe either way).
- **The script fails to run:** give the rewritten text as a list of cell references and new text, ready to paste. Never rebuild the spreadsheet from scratch.
- **The file is .xls (old Excel) or .ods:** ask the user to save it as .xlsx, or paste the column.
- **The file has macros (.xlsm):** do not edit it with the script. Give the new text as a list with cell references instead.
- **A cell mixes text and a number** ("Paid 4,500 on 2 May, balance pending"): you may reword it, but the number and date must come through exactly.
