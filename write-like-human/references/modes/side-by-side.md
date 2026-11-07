# Side by side mode

Show each change as a before and after pair, so the user can accept or reject them one by one.

## When this applies

- "Show me the changes", "let me approve each one", "side by side", "what would you change?", "I want to see what you changed".
- The user is careful about their text: a resume, a statement of purpose, a speech, a legal or official letter.
- For files where the user wants tracked changes in Word, also read `files/word.md` (it can produce real tracked changes).

## What stays the same

- The same rules as rewrite mode: meaning, protected content, length, formality, language, and the user's habits.
- Nothing is final until the user says so. Do not apply changes they have not accepted.

## Steps

1. Work out the changes the same way as in `modes/rewrite.md`.
2. Split them into small, separate changes. One change per sentence or phrase, so accepting one does not force another.
3. Number them. For each, show the original, the new version, and a reason in a few plain words.
4. Ask the user which to keep. Accept answers like "all", "all except 3", "1, 2 and 5", "none", or "change 4 to something shorter".
5. Apply only what they accepted. If they ask for a different version of one change, give it and ask again for just that one.
6. Return the final text or file with only the accepted changes.

## Output

First round:

```
1. "I am writing to inform you that I will be unable to attend"
   -> "I can't make it to"
   Why: shorter and less stiff

2. "at your earliest convenience"
   -> "by Friday"
   Why: you mentioned Friday earlier, this makes the ask clear

3. ...

Which ones should I keep? You can say "all", "all except 2", or pick numbers.
```

Keep the list to the changes that matter. If there are more than about 12, group the small ones ("4 to 9: removed long dashes") so the list stays readable. For long documents, go section by section and ask after each one.

Final round: the finished text or the `<original-name>-humanized.<ext>` file, and one line saying how many changes were applied, for example "Applied 6 of 8 changes."

## Example

Before:

> I am reaching out to express my sincere gratitude for your invaluable support during this challenging period. Your guidance has been instrumental in helping me navigate the transition.

Side by side:

```
1. "I am reaching out to express my sincere gratitude for"
   -> "Thank you for"
   Why: says the same thing in three words

2. "invaluable support during this challenging period"
   -> "your support over the last few months"
   Why: plainer, and less like a template

3. "has been instrumental in helping me navigate the transition"
   -> "made the move to the new team much easier"
   Why: "instrumental" and "navigate" are stock phrases; this says what helped

Which ones should I keep?
```

(For change 3, "the move to the new team" is only fine if the user's text or message mentioned it. If not, ask what the transition was instead of guessing.)
