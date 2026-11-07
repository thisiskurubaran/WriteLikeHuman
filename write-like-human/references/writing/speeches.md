# Speeches and toasts

Wedding speeches, birthday toasts, farewell speeches, retirement send-offs, and short words at family functions. These are written to be heard, not read.

## When this applies

- The user asks you to write, fix, or shorten a speech or toast.
- They paste a draft that sounds stiff or "like a greeting card".
- They mention an event: wedding, sangeet, reception, birthday, anniversary, farewell, retirement, school function.

## What stays the same

- Every name, relationship, date, and place.
- The stories the user tells you. Keep their details. Do not make a story bigger or funnier than it was.
- The user's language mix. If they wrote "Mausi" or "Appa", keep it.
- Inside jokes, unless the user asks if they will land with the whole room.

Never invent anecdotes, memories, quotes, or qualities. A made up story in a speech is worse than no story, because people in the room know the truth.

## Ask for the real material

If the user only gives the occasion and a name, ask two or three short questions before drafting:

- "Who is the speech for, and how do you know them?"
- "One small story or moment you remember with them?"
- "How long should it be? Most toasts are 1 to 3 minutes."

If they say "just write something", write a short version with clear gaps like `[a moment when she helped you]` and tell them to fill those in.

## Writing for the ear

- Short sentences. One idea each. People cannot reread a sentence they heard.
- Use names often. "Rohan" is easier to follow than "he" after a pause.
- Put a natural pause after a story or a laugh line. Mark it with a line break.
- Avoid lists of adjectives ("kind, generous, and loyal"). Tell one story that shows one of them.
- Avoid quotes from famous people unless the user picked one.
- No big openers like "Ladies and gentlemen, we are gathered here today". Start with who you are or with the story.
- End by asking people to raise a glass, clap, or wish the person well. Keep it to one line, not a dramatic finish.

## Timing

People speak at about 130 words per minute when they are a little nervous. Use that to set length:

| Length | Words |
|---|---|
| 1 minute | about 130 |
| 2 minutes | about 260 |
| 3 minutes | about 390 |
| 5 minutes | about 650 |

Tell the user the rough speaking time in the change summary. Use `scripts/word_count.py` for an exact count when it is available.

## Timing and pauses

To see how long each part takes to say, run:

```
python scripts/word_count.py speech.txt --speech
```

It prints the total speaking time and the time for each section (sections are split on blank lines), at about 130 words per minute. Add `--wpm 110` for a slow, emotional speech or `--wpm 150` for a confident speaker. If the script fails, count the words and divide by 130.

Use the per-section times to spot a section that runs long ("the story about the trip takes 90 seconds of a 3 minute toast"), and say so in one line.

Only if the user asks for a reading copy, mark pauses so the speech is easier to deliver:

- a single `/` for a short breath
- `(pause)` before a punchline or after an emotional line, where the room needs a moment

Keep pause marks out of the normal version. They are for the copy the speaker holds, not for sharing.

Example reading copy:

> I met Kiran on our first day at work. / She was the only one who knew where the canteen was. (pause) / Nine years later, she still knows where everything is.

## Steps

1. Collect the real material (see above).
2. Pick a simple shape: who I am, one or two stories, what they mean to me, the toast.
3. Write it in the user's register. A best man at a casual wedding sounds different from a manager at a retirement lunch.
4. Read it in your head at speaking pace. Break any sentence you would run out of breath on.
5. Check it against `ai-patterns.md`. Greeting card phrases and forced triads are common here.

## Output

The speech with a blank line between spoken chunks, so it is easy to read from a phone. Then the change summary with the speaking time.

## Example

Before:

> Good evening everyone. Today we celebrate the remarkable journey of Meena, a colleague who embodies dedication, compassion, and excellence. Her unwavering commitment has been a beacon for us all.

After:

> Hi everyone. I'm Kavya, and I've sat next to Meena for six years.
>
> On my first day I couldn't log in to anything. Meena didn't send me to IT. She pulled up a chair and sat with me until it worked. That took two hours.
>
> That's Meena. She makes time.
>
> Meena, we'll miss you. Everyone, please raise a glass to Meena.

The story came from the user. The rewrite cut the three-word praise list and let the story show it.
