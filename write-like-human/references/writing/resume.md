# Resumes and cover letters

## When this applies

The user shares a resume or CV (pasted, .docx, .pdf, or a Google Doc), a cover letter, or a LinkedIn "About" section written like a resume. Always load `lists/buzzwords.md` alongside this file. If it is a file, also load the matching `files/` module.

## What stays the same

- Job titles, company names, dates, locations, degrees, grades, certifications.
- Every number: years of experience, team sizes, percentages, revenue, rupee and dollar amounts.
- Tools, languages, and product names ("Excel", "SAP", "Python", "Tally").
- The layout. Section order, headings, bullet style, columns, fonts. A resume is often tuned to fit one page, so do not let it grow.
- Contact details. Do not rewrite or reformat the email address or phone number.

## The big rule: never invent

Do not add metrics, achievements, responsibilities, titles, or skills the user did not give you. "Managed a team" does not become "Managed a team of 12" unless the user said 12. "Improved sales" does not become "Improved sales by 30%".

If a bullet would be much stronger with a number, ask in the change summary: "If you know roughly how many customers you handled each day, adding it would make this bullet stronger." Leave the bullet as it is until they tell you.

## What to fix

- Buzzwords. Swap them for plain words using `lists/buzzwords.md`. "Spearheaded cross-functional synergies" becomes "Led a project with the sales and support teams" only if that is what the user described.
- Vague bullets. "Responsible for various tasks related to accounts" says nothing. If the resume elsewhere says what those tasks were, use that. If not, flag it.
- Weak openings. Start bullets with a plain past-tense verb: ran, built, fixed, trained, cut, wrote, handled, set up. Present tense for the current job.
- Repeated verbs. Six bullets starting with "Managed" read as filler. Vary them, but keep the meaning.
- The summary paragraph. Many summaries read like "Results-driven, detail-oriented professional with a passion for excellence." Rewrite from the facts in the resume: years, field, what they are good at, what they want next. Two or three lines.
- Length of bullets. One to two lines each. Split or trim long ones.
- "References available on request." Leave it if the user wants it, but mention it can usually go.

Keep the resume plain enough for applicant tracking systems (software many companies use to scan resumes): standard headings like "Experience" and "Education", no text inside images, no tables used for layout unless the user already has them.

## Cover letters

- Open with the role and one real reason the user wants it. Skip "I am writing to express my keen interest in".
- Middle: one or two specific things from their resume that match the job. Use the job ad's wording only where it is true for them.
- Close with a simple line about being glad to talk. No "I am confident I would be a valuable asset".
- Under one page. Three or four short paragraphs.
- Do not claim knowledge of the company the user did not give you.

## Steps

1. Read the whole resume first so you know what facts exist.
2. Rewrite the summary, then each bullet, keeping every fact.
3. Check the length. Same number of pages as before, ideally the same number of lines.
4. Re-check against `ai-patterns.md` and `lists/buzzwords.md`.
5. Write the change summary, including any questions about missing numbers.

## Output

For files, return `<name>-humanized.docx` with the layout unchanged (see `files/word.md` or `files/pdf.md`). For pasted text, return the rewritten text. Then the change summary.

## Example

Before:

```
PROFILE
Highly motivated and results-driven professional with a proven track record
of delivering exceptional customer outcomes in a fast-paced environment.

EXPERIENCE
Customer Support Executive, Brightline Telecom, Pune (2021 to present)
- Spearheaded resolution of customer queries across multiple channels
- Responsible for various tasks related to billing
- Played a key role in onboarding new team members
```

After:

```
PROFILE
Customer support executive with three years at a telecom company. I handle
billing and service queries over phone, chat, and email, and I train new
joiners.

EXPERIENCE
Customer Support Executive, Brightline Telecom, Pune (2021 to present)
- Answer customer queries over phone, chat, and email
- Handle billing questions and correct billing errors
- Train new team members during their first weeks
```

What I changed
- Rewrote the profile from facts in your resume instead of general praise.
- Swapped "spearheaded" and "played a key role" for plain verbs.
- Used the billing details from your skills section to make the vague billing bullet specific.
- Kept the job title, company, city, and dates as written.
- If you know roughly how many queries you handle a day, adding that number would make the first bullet stronger.
