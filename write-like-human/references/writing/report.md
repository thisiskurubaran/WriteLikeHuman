# School and work reports

## When this applies

School and college assignments, project reports, lab reports, internship reports, essays, status reports at work, monthly updates, incident reports, and similar documents. If it is a file, also load the matching `files/` module.

## Honest use comes first

Reports are often graded or submitted under the user's name. The rules:

- Help the user improve their own draft. Make it clearer, better organised, and more natural. That is fine and normal, like a friend or teacher reading it over.
- Do not write a whole graded assignment from nothing for the user to hand in as their own. If asked, offer to help them outline it, explain the topic, or improve the draft they write.
- Do not promise the report will pass any checking tool, go unnoticed, or look like it was not edited. If the user asks for that, say plainly that you can make the writing clearer and more natural, and that you cannot promise anything about how it will be checked.
- If their school or employer requires disclosing AI help, remind them once, briefly, without lecturing.
- Never invent sources, citations, data, survey results, quotes, or experiment readings. If the report needs a source it does not have, flag it.

## What stays the same

- Data, results, figures, measurements, units, and anything in a table or chart.
- Citations, references, footnotes, and quoted passages, word for word.
- Technical terms the field uses. "Titration" stays "titration".
- Headings, numbering, figure and table captions, and the reference list format.
- The user's argument and conclusions. You improve how it is said, not what they concluded.
- Word count, within about 10 percent, since many assignments have limits. Use `adjust/length.md` and `scripts/word_count.py` if the user gives a limit.

## What to fix

- Padded introductions. "Since the dawn of time, humans have..." Start with the topic.
- Signposting overload. "In this section, we will explore..." at the start of every section. Once is enough, often zero.
- Inflated words. "Utilise" for "use", "in order to" for "to", "a plethora of" for "many".
- Hedging on everything. "It could perhaps be argued that this may potentially suggest." Hedge once where the evidence really is uncertain.
- Conclusions that repeat the introduction. A conclusion should say what the report found and what it means.
- Long sentences. Split anything over about 30 words if it gets hard to follow.
- Passive voice everywhere. Lab reports often use passive voice on purpose ("The solution was heated"). Keep it there if that is the user's convention. Elsewhere, use active voice where it reads better.

For work reports, put the main point or status at the top ("Project is two weeks behind because the supplier delivery slipped"), then the detail.

## Steps

1. Read the whole report to understand the argument and the facts.
2. Check whether it is graded work. If it is, apply the honest use rules above.
3. Rewrite section by section, keeping every protected item.
4. Check the word count against the original and any limit.
5. Re-check against `ai-patterns.md`.
6. Write the change summary. Flag any missing sources or unclear data instead of fixing them yourself.

## Output

For files, return `<name>-humanized.<ext>` with headings, tables, and references unchanged. For pasted text, return the rewritten text. Then the change summary and the word count if a limit applies.

## Example

Before (school project report, one paragraph):

```
In today's world, water conservation has become a very important and
significant topic. In this report, we will explore the various different
methods of water conservation. Our survey of 40 households in our colony
revealed that a plethora of families are not aware of rainwater harvesting.
```

After:

```
Water shortages are now common in many Indian cities, including ours. This
report looks at ways households can save water. In our survey of 40
households in our colony, most families did not know about rainwater
harvesting.
```

What I changed
- Replaced the general opening with a specific one about the problem.
- Cut "very important and significant" and "various different", which said the same thing twice.
- Swapped "a plethora of" for "most".
- Kept the survey size of 40 households exactly.
- Your survey table does not say how many families knew about rainwater harvesting. If you have that number, adding it would make this sentence stronger.
