# Quick options for unclear requests

When it isn't clear what the user wants done with some text, offer a few short choices instead of guessing or asking an open question.

## When this applies

- The user pastes or attaches text with a vague ask, or none: "help with this", "can you look at this?", "this one", just the text, or a file with no message.
- More than one task is likely. For a pasted message from someone else, they might want a reply, a reading of its tone, or a rewrite.

It does not apply when the request is clear. "Make this friendlier", "reply to this", "check before I send" all go straight to the work. Never show options for a clear request, and never more than once in a conversation for the same text.

## What stays the same

- The user's text. Don't change anything until they pick.
- The rest of the skill: once they choose, load the matching mode and modules as usual.

## Steps

1. Guess the two to four most likely tasks from what they gave you:
   - Their own draft: rewrite it, check it before sending, make it shorter or friendlier.
   - A message someone sent them: reply to it, tell them how it sounds, summarise what they're being asked.
   - A file: fix the wording, check it, or something specific to the file (fill the form, make a change report).
   - Developer text (a README, a diff, comments): rewrite it, write a commit message, explain the structure.
2. If your app has a tool that shows tap-to-pick choices (for example, a question tool in Claude Code), use it: one question, two to four options, each with a short label and one line saying what happens.
3. Otherwise, send a short numbered list and nothing else:

   > What would you like me to do?
   > 1. Rewrite it so it sounds natural
   > 2. Check it before you send
   > 3. Write a reply to it
   >
   > Reply with a number, or tell me in your own words.

4. Keep the labels in the user's language. If they wrote in Hindi, offer the options in Hindi.
5. When they answer ("2", "the second one", "reply"), do that task straight away. If they ignore the options and ask for something else, do that.

## Output

Only the options. No rewrite, no analysis, and no change summary until they choose.

## Example

User: "help with this" (pastes a message from their landlord asking for rent a week early)

You:

> What would you like me to do?
> 1. Write a reply to your landlord
> 2. Tell you how the message sounds
> 3. Help you say no politely
>
> Reply with a number, or tell me in your own words.
