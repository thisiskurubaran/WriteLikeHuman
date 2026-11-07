# Length

Shorten text to fit a limit, or expand short notes into full sentences, without changing what it says.

## When this applies

- "Make it shorter", "cut this to 200 words", "under 1,000 characters", "too long", "one paragraph".
- "Expand this", "make it longer", "turn these notes into a paragraph", "I need 500 words".
- A form, platform, or teacher has a limit the user mentions.

Without one of these, core rule 8 applies: keep length within about 10 percent.

## What stays the same

- Facts, names, numbers, dates, and amounts.
- The main point and any direct answer to a question.
- Requests and deadlines in emails and letters.

When expanding, never invent facts, examples, quotes, or results to fill space. Expand with clearer explanation, the reasons the user gave, and the details already in their notes. If there is not enough material to reach the target, say so and ask for more.

## Steps

### Counting

Use `scripts/word_count.py` for exact counts when code execution is available:

```
python scripts/word_count.py FILE --target 200
echo "your text" | python scripts/word_count.py --target 200
```

It reports words and characters. If the script fails or is not available, count carefully by hand and say the count is approximate.

Check what the limit counts. Many forms count characters with spaces. Social platforms count characters. Teachers usually count words.

### Shortening

Cut in this order and stop once the target is met:

1. Filler openers and closers ("I hope this email finds you well", "Thank you for your time and consideration").
2. Repeated points. Keep the clearest version.
3. Hedges and padding ("in order to" becomes "to", "at this point in time" becomes "now").
4. Extra examples. Keep the strongest one.
5. Side points that do not serve the main point.

Do not drop a fact the reader needs to act on.

### Expanding

1. Turn fragments into full sentences.
2. Add the link between points ("because", "so", "which meant").
3. Add context the user gave elsewhere in the conversation.
4. If more is still needed, ask: "Can you tell me one more example or what happened next?"

Do not add generic padding to hit a number.

## Two lengths at once

Only when the user asks for it ("give me a short and a long version", "one for WhatsApp and one for email"), give exactly two versions, labeled with their word counts:

```
Short (38 words)
...

Longer (112 words)
...
```

Both versions follow every rule above: same facts, nothing invented, and the longer one grows only from what the user gave you. Put one change summary after both, not one per version.

Otherwise never offer several versions. One good version is the default, and a menu of options is itself a chatbot habit.

## Output

The new version with its count ("187 words" or "about 190 words"), then a brief change summary saying what was cut or added.

## Example

Before (64 words, target 30):

> I just wanted to reach out and let you know that unfortunately I will not be able to attend the team meeting that is scheduled for Thursday afternoon at 3 pm because I have a doctor's appointment that I booked a while ago. I'll make sure to catch up on the notes afterwards. Sorry for any inconvenience this may cause.

After (28 words):

> I can't make Thursday's 3 pm team meeting because of a doctor's appointment I booked a while ago. I'll catch up on the notes afterwards. Sorry about that.
