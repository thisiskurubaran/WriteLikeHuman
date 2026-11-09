# Personalised messages from a spreadsheet

One message, filled in for each person on a list the user already has: festival greetings to family and friends, a thank you to every guest, a reminder to each parent in a class group, a note to existing customers who asked to hear from the shop.

## When this applies

- "Send this Diwali wish to everyone in my sheet, using each name."
- "Make a thank you message for each guest in this list."
- The user gives a message and a .xlsx or .csv with columns such as Name, Relation, City, or Amount.

This is for people the user already knows: family, friends, colleagues, guests, students' parents, or customers who chose to hear from them. Decline bulk marketing to strangers, bought or scraped lists, and messages meant to look personal to people who never asked to be contacted. Say why in one line, and offer to help with a message for people who did opt in.

## What stays the same

- Every name, amount, date, and detail comes from the sheet, exactly as written. Never invent a detail to make a message feel more personal ("hope the new house is lovely" when the sheet says nothing about a house).
- The message is the same for everyone except the placeholders, unless the user asks for differences (for example a warmer line for family).
- Nothing is ever sent. The result is a file of drafts the user copies or sends themselves.
- The original sheet is never changed.

## Steps

1. Get the message right first. If the user's draft sounds stiff, rewrite it once using the right writing guide (for a festival wish, `writing/wishes-cards.md`), then show it with the placeholders in place: "Happy Diwali, {Name}! Wishing you and the family in {City} a bright year." If the message needs real curly braces, like a coupon code `{SAVE10}`, write them doubled in the template (`{{SAVE10}}`) so the script doesn't read them as a column.
2. Check the columns:
   ```
   python scripts/mail_merge.py columns contacts.xlsx
   ```
   Make sure every placeholder matches a column heading. Upper or lower case doesn't matter.
3. Save the message to a text file and fill it for every row:
   ```
   python scripts/mail_merge.py merge contacts.xlsx message.txt --out diwali-messages.csv
   ```
   Use `.csv` to keep the sheet's columns with a new Message column, `.txt` for a plain list to copy from, or `.docx` for one block per person.
4. Read the CHECK lines. A row with a missing value keeps its placeholder, such as `{City}`. Tell the user which rows need a value, or offer a version of the message without that placeholder. Do not fill the gap yourself.
5. Show the first two or three messages in the chat so the user can see how they read, then give the file.

## Output

- A new file, `<sheet-name>-messages.csv` (or `.txt` or `.docx`), with one message per row.
- One line saying nothing was sent and how many messages are in the file.
- The rows with missing values, if any.

## Example

User: "Make a Pongal wish for everyone in this sheet. Columns are Name and Relation."

Message:

> Happy Pongal, {Name}! Hope the pongal boils over and the year is sweet. Lots of love.

Sheet rows: Lakshmi (Aunt), Karthik (Cousin), a row with no name.

Result (`pongal-messages.txt`):

> Happy Pongal, Lakshmi! Hope the pongal boils over and the year is sweet. Lots of love.
>
> Happy Pongal, Karthik! Hope the pongal boils over and the year is sweet. Lots of love.
>
> Happy Pongal, {Name}! Hope the pongal boils over and the year is sweet. Lots of love.

"Saved 3 messages. Nothing was sent. Row 4 has no name, so I left {Name} there. Add the name or delete that row."

## If something goes wrong

If the script can't run, do it by hand: read the sheet, fill the message for each row in the chat, and list rows with missing values instead of guessing. For long lists (more than about 50 rows), suggest the user download the result as a file rather than scrolling through the chat. If the sheet is a Google Sheet without a connector, ask the user to download it as .xlsx or .csv first.
