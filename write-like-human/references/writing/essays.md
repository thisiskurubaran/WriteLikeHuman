# School and college essays

Help students make their own essays clearer and more natural: school essays, college assignments, and college application essays (Common App, UCAS personal statements, university SOP-style essays).

For visa letters and scholarship answers, use `writing/form-answers.md`. For reports and project write-ups, use `writing/report.md`.

## Honest use comes first

Essays are usually graded or submitted under the student's name. The rules:

- Help the student improve their own draft, the way a teacher or older sibling would read it over. That is fine and normal.
- Do not write a full graded essay or application essay from nothing for the student to submit as their own. If asked, offer to help them brainstorm, outline, or find their own story, then improve the draft they write.
- Never invent experiences, achievements, hardships, family details, awards, or quotes. Admissions essays are about the student's real life. Made up stories can get an application rejected.
- Do not promise anything about how the essay will be checked, or that it will go unnoticed. If asked, say plainly that you can help make their own writing clearer and more natural, and that is all.
- If their school or the application requires disclosing help, remind them once, briefly.

Side by side mode (`modes/side-by-side.md`) works well here. The student sees each change and keeps control of their own essay.

## When this applies

- A student pastes an essay draft and asks to improve it or make it sound less robotic.
- They have notes or a rough draft for a college application essay.
- They ask "does my essay sound like AI?" (also load `modes/check.md`).

## What stays the same

- The student's story, experiences, opinions, and conclusions.
- Facts, dates, names, numbers, and quotations, with citations.
- The prompt they are answering. Keep the essay on topic.
- The word limit. Check it with `scripts/word_count.py` and stay within it.
- Their voice. A 16 year old should sound like a thoughtful 16 year old, not a professor. Keep simple words they chose if they work.

## What to fix

- Grand openings: "Since the dawn of time", "Webster's dictionary defines", "In today's world".
- Big claims with no detail: "This experience changed my life forever." Ask what actually changed.
- Stock essay phrases: "a valuable lesson", "stepped out of my comfort zone", "made me who I am today", "I have always been passionate about".
- Summary endings that repeat the introduction.
- Long, tangled sentences that hide the point.

For application essays, the strongest fix is often a question, not a rewrite: "You mention fixing your grandfather's radio. What did you actually do?" Their answer, in their words, is what makes the essay theirs.

## Steps

1. Read the prompt (ask for it if not given) and the whole draft.
2. Find the one or two moments in the draft that are specific and real. Those are the heart of the essay.
3. Point out vague parts and ask for the real detail instead of filling it in.
4. Make the changes, or show them side by side if the student wants to approve each.
5. Check the word count and every fact.

## Output

The improved essay or the side by side list, then a short change summary. Add any questions for the student about vague parts.

## Example

Before (application essay opening):

> Since childhood, I have always been deeply passionate about technology. Volunteering at the community library was a truly transformative experience that taught me valuable lessons about leadership and helped me step out of my comfort zone.

After:

> Every Saturday for a year, I taught Mrs. Pillai, who is 71, how to video call her grandson in Toronto. It took us six weeks to get past the mute button.

What I changed
- Started with your Saturday sessions at the library instead of a general statement.
- Cut "deeply passionate", "transformative", and "step out of my comfort zone".

(The details about Mrs. Pillai, Toronto, and the mute button are shown as if the student wrote them in their notes. In real use, ask the student for the real moment and use only what they tell you.)
