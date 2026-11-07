# Form answers

Personal statements, statements of purpose, visa purpose letters, scholarship and fellowship answers, and "tell us about yourself" boxes on applications.

## When this applies

- The user pastes a draft answer, the question, or both.
- They mention a university application, SOP, scholarship, visa, job portal question, or grant form.
- They have notes about themselves and want them turned into an answer.

## What stays the same

- Every fact about the user: grades, test scores, dates, jobs, projects, awards, family details, money, travel dates, addresses, and sponsor details.
- The reason they give for applying or travelling.
- Names of schools, employers, programs, and places.

Never invent experiences, qualifications, family details, hardships, travel plans, ties to home, or future plans. An invented detail on a visa or scholarship form can get the user rejected or worse. If the answer is thin, ask for more real detail. Do not fill the gap.

## Point out when the form needs their own words

Many forms ask the applicant to confirm they wrote the answer, or say that tools may only be used for light editing. When the form or the user mentions this:

- Say so in one line: "This application asks that the statement be your own writing, so I'll suggest edits to your draft rather than rewrite it."
- Work in side by side style. Suggest changes sentence by sentence and let the user pick. See `modes/side-by-side.md`.
- Focus on clarity, grammar, and cutting filler. Keep their structure and phrasing where it works.

If the user asks you to write the whole answer from nothing for such a form, offer to ask them questions and help shape their own answers instead.

## Visa letters

- Keep it factual and calm: who is travelling, why, dates, where they will stay, who is paying, and when they will return.
- Use the exact dates, amounts, and names the user gives.
- No emotional appeals or promises the user has not made.
- Remind the user to check the embassy's own checklist, since requirements change.

## Word and character limits

- Ask for the limit if it is not given and the form usually has one.
- Use `scripts/word_count.py` for an exact count when available. Many portals count characters with spaces, so check which the form uses.
- When cutting, drop filler and repeated points first, then the weakest example. Never cut a fact the question directly asks for.

## Steps

1. Read the question. Answer what it asks, not a general essay about the user.
2. Find the one or two real examples that best answer it.
3. Open with something specific, not "Since my childhood I have always been passionate about".
4. Replace claims with what happened. "I am a strong leader" becomes what they led and what came of it, using only facts they gave.
5. Check the limit. Check against `ai-patterns.md`. Statement-of-purpose clichés are common.

## Output

The answer with its word or character count, then a brief change summary. If you had to leave gaps, list the questions that would fill them.

## Example

Before:

> From a young age, I have always been passionate about technology. I am a hardworking, dedicated, and innovative individual who thrives in challenging environments. This scholarship will help me achieve my dreams.

After:

> In my second year I built a small app that lets my college canteen take orders by WhatsApp. About 300 students used it in the first month. That project is why I want to study software engineering. This scholarship would cover the tuition my family cannot.

The app, the 300 students, and the family situation all came from the user's notes. Without them, the right move is to ask, not to invent.
