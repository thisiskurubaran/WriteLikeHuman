# Check mode

Point out what makes the text read like AI, without rewriting it.

## When this applies

- "Does this sound like AI?", "check this", "is this robotic?", "what gives it away?", "be honest, does this sound like ChatGPT?"
- The user wants feedback, not a new version.

## What stays the same

Everything. You do not change the text in this mode. If the user wants changes after seeing the findings, switch to rewrite or side by side mode.

## What this is not

This is a reading of the writing, not a verdict on who wrote it. You cannot know whether AI wrote something, and neither can anyone else from the text alone. Never give a score, a percentage, or a "likely AI" label. Never say the text will or will not be flagged by any tool. Talk only about how it reads.

## Steps

1. Read the whole text.
2. Go through `ai-patterns.md` and note what you find, with short quotes as evidence.
3. Group the findings in plain words. Put the most noticeable first. Usually that is the opening, the closing, stock words, dashes, and formatting.
4. Pick out what already sounds natural and say so. People want to know what to keep.
5. Give an overall read in one or two sentences, in normal language: "It reads mostly natural. The opening and the last line are the parts that sound generated."
6. Offer to fix it, in one line.

## Output

Use this shape:

```
Overall: <one or two sentences>

What stands out
- <plain description>: "<short quote>"
- <plain description>: "<short quote>"
- ...

What already sounds natural
- <one or two points>

Want me to fix these? I can also show each change so you can pick.
```

Keep quotes short, under about ten words each. Do not paste the whole text back. Three to seven findings is plenty. If there is almost nothing to flag, say so honestly and stop.

## Example

Text:

> In today's digital age, effective communication is more crucial than ever. Our team has been working tirelessly to streamline our processes. Moreover, we have implemented a powerful new system that empowers employees. Ultimately, this is not just about efficiency, it's about people.

Check:

```
Overall: This reads like generated text. Almost every sentence has
a common chatbot habit, and it never says anything specific.

What stands out
- Warm-up opening that says nothing: "In today's digital age"
- Several words chatbots overuse: "crucial", "streamline",
  "powerful", "empowers"
- "Moreover" and "Ultimately" starting sentences
- A "not just X, it's Y" line at the end: "not just about efficiency"
- No details: which system, which team, what changed?

What already sounds natural
- The sentences are short and easy to follow.

Want me to fix these? I can also show each change so you can pick.
```
