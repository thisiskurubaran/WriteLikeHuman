# Forms (fillable PDF and Word forms)

## When this applies

The user gives you a form to fill: a fillable PDF (visa application, school admission, bank KYC, insurance claim) or a Word form with labels and blank boxes. They want the answers written in plain words and put in the right boxes.

For long written answers inside a form, such as a statement of purpose or "why do you want this scholarship", also load `writing/form-answers.md`. Its honesty rules apply to every form.

## What stays the same

- The form itself: its layout, wording, logos, and every field you were not asked to fill
- Every fact about the user exactly as they gave it: names, dates, ID numbers, addresses, amounts, phone numbers
- Declarations, consent boxes, and signature boxes, unless the user explicitly tells you what to do with them

## Never guess personal details

A wrong answer on an official form can get the user rejected or worse. So:

- Never invent or guess ID numbers, passport numbers, dates of birth, addresses, income, bank details, family details, or travel dates.
- If the user didn't give a fact a field needs, leave the field blank and list it at the end.
- Never tick a declaration ("I confirm the above is true") or fill a signature box on the user's behalf unless they clearly ask. Even then, remind them to read the declaration first.
- If an answer the user gave seems to contradict another one (two different dates of birth), ask before filling either.

## Steps

### Fillable PDF forms

1. **List the fields:**
   ```
   python scripts/form_fill.py fields <form>.pdf -o fields.json
   ```
   Each field has a `name`, a `type` (text, checkbox, radio, choice, signature), its current `value`, and for checkboxes and drop-downs the `options` it accepts. A drop-down that shows different text from the value it stores also has `option_labels`. Some have a `label` with the question text. A field inside a group has its full name, such as `applicant.name`.
2. **Match the user's facts to the fields.** Field names can be cryptic (`txt_f3`). Use the label, the page number, and the order to work out which is which, and check with the user if you're unsure.
3. **Write the values** as a JSON object of field name to value. Text answers in plain words, short enough for the box. Checkboxes take one of their listed options, such as `/Yes`.
4. **Fill a copy:**
   ```
   python scripts/form_fill.py fill <form>.pdf values.json
   ```
   It saves `<form>-filled.pdf`, skips any field name that doesn't exist, refuses signature boxes, and lists text fields that are still blank.
5. **Check every filled value** against what the user told you.

### Word forms

Word forms are usually tables with a label in one cell and an empty cell next to it, or boxes with grey placeholder text.

1. List the text with `python scripts/docx_rewrite.py extract <form>.docx -o segments.json`. Table cells show up with ids that include their row and column.
2. Fill the empty answer cells and placeholder text, using the same rules as above.
3. Apply with `python scripts/docx_rewrite.py apply <form>.docx changes.json -o <form>-filled.docx`.
4. If a cell is completely empty, the script may not list it. Say which answers go where, so the user can type them in.

## Output

- `<form>-filled.pdf` or `<form>-filled.docx`. The original form is never overwritten.
- A short list of what you filled and what is still blank, in plain words:
  > Filled 14 fields. Still blank: passport number, date of birth, and the signature box. Please add those yourself before you submit.
- A reminder to check the official instructions for that form, since requirements change.

## Example

Form `school-admission.pdf`. The user says: "Fill this for my son Arjun Mehta, Class 3, father's name Rohan Mehta, phone 98XXXXXX10, we live in Pune."

`fields` lists `student_name`, `class`, `dob`, `father_name`, `phone`, `address`, and `declaration` (checkbox).

values.json:
```
{"student_name": "Arjun Mehta", "class": "3", "father_name": "Rohan Mehta", "phone": "98XXXXXX10"}
```

Summary:
> Filled the student name, class, father's name, and phone. Still blank: date of birth and full address (you said Pune, but the form asks for the full address). I left the declaration unticked for you to read and tick yourself.

The city alone was not put in the address box, because a partial address on an admission form can cause trouble later.

## If something goes wrong

- **No fillable fields found:** the PDF is a flat form. List its questions as text, give the answers in the same order, and tell the user they can type them in or print and write them. Do not claim to have filled the PDF.
- **The script fails or pypdf is missing:** give the answers as a plain list of "Question: answer" so the user can copy them in.
- **Values don't show in the filled PDF:** some viewers hide filled values until the form is clicked. Tell the user to open it in a different app (Adobe Reader, or the browser's PDF viewer). The script already asks viewers to redraw the fields.
- **A drop-down doesn't accept the answer:** use one of the listed `options` exactly, and tell the user if none of them fit.
- **The form is a scanned image:** read the questions from the image (see `files/pdf.md`, scanned pages) and give the answers as text to write in by hand.
