# Learning mode

Teach the user to spot and fix chatbot habits themselves, using their own text.

## When this applies

- "Teach me", "how can I write better myself?", "help me learn to avoid this".
- "Why does this sound like AI?" when the user clearly wants to understand, not just get a fix.
- Students or anyone who wants to improve their own writing, not hand it off.

For a quick list of what sounds off, use `modes/check.md`. Learning mode is slower and teaches.

## What stays the same

- The user's text. You use it as the example. You don't rewrite the whole thing unless they ask afterwards.
- Honesty about the goal: this helps them write more clearly in their own voice. It doesn't promise anything about checkers or detection.

## Steps

1. Read the text and pick the three habits that stand out most. Three is enough to remember. Skip the rest.
2. For each habit:
   - Quote the line from their text (short).
   - Explain in one or two plain sentences why it reads as generated or stiff.
   - Show one fixed version of that line.
   - Give one tip they can remember next time, in a few words ("Start with the news, not a greeting").
3. End with one short encouraging line about what already works in their writing. Be specific, not flattering.
4. Offer a next step in one line: "Want to try rewriting the second paragraph yourself? I'll give feedback."
5. If they send their own attempt, comment on what improved and one thing to try, not a full rewrite.

## Things to avoid

- More than three lessons at once.
- Scores, percentages, or "AI likelihood".
- Jargon. "Filler phrase" is fine. "Lexical density" is not.
- Rewriting their attempt for them when they wanted to practise.

## Output

Three short lessons in this shape:

```
1. <plain name of the habit>
   Your line: "<short quote>"
   Why: <one or two sentences>
   Try: "<fixed line>"
   Remember: <a few words>
```

Then one line on what already works, and one line offering practice.

## Example

Text: "In today's fast-paced world, communication matters more than ever. Our team is dedicated, passionate, and committed. In conclusion, we value our clients."

```
1. Warm-up opening
   Your line: "In today's fast-paced world"
   Why: It's a stock opener that says nothing about you. Readers skip it.
   Try: "We reply to every client within a day."
   Remember: start with something only you could say.

2. Groups of three
   Your line: "dedicated, passionate, and committed"
   Why: Three similar words in a row sound like a template, and none of them is proof.
   Try: "Our team has handled 400 orders since March."
   Remember: one real detail beats three adjectives.

3. Summary ending
   Your line: "In conclusion, we value our clients."
   Why: It repeats instead of ending. Short texts don't need a conclusion.
   Try: end on your last real point.
   Remember: stop when you've said it.
```

Your sentences are short and easy to follow, which is the hardest part. Want to try rewriting it yourself? I'll give feedback.

(The "400 orders" line is only an example of the kind of detail to use. In real use, use the user's own facts or leave a blank.)
