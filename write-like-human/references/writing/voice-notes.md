# Voice notes

Turn speech-to-text transcripts into writing people can read. Voice notes, dictated messages, call transcripts, and recorded thoughts.

## When this applies

- The user pastes text from a voice note, dictation app, or call transcript.
- The text has fillers ("um", "like", "you know", "basically", "na", "matlab"), repeats, run-on sentences, or odd words where the software misheard.
- They ask to "clean this up", "make this readable", or "turn this into a message".

## What stays the same

- What the person said and meant. Clean the form, not the content.
- Names, numbers, dates, times, amounts, and addresses.
- The speaker's way of talking. A casual voice note becomes a casual message, not a formal letter.
- Mixed language. If they switch between Hindi and English, keep the switch (see `languages/mixed-language.md`).

## Fixing mishearings

Speech-to-text often gets words wrong. Fix a word only when the right one is obvious from context:

- "We'll meet at the cafe near the bus stand at for" becomes "at four".
- "Send me the in voice" becomes "invoice".

When you are not sure, do not guess. Mark it as `[unclear]` or `[unclear: "Ravi" or "Ravish"?]` and mention it in the change summary. A wrong guess on a name, number, or address can cause real trouble.

## Steps

1. Remove fillers, false starts, and repeated words ("I was, I was going to").
2. Split run-on speech into sentences. Add punctuation and paragraphs.
3. Fix obvious mishearings. Mark unclear ones.
4. Keep corrections the speaker made: "Tuesday, no sorry, Wednesday" becomes "Wednesday".
5. Ask what the output is for if it matters: a message to send, notes for themselves, or minutes. For meetings, also read `writing/meeting-notes.md`.
6. Do not add points the speaker did not make or tidy away ones they did.

## Output

The cleaned text, then a short change summary. List every `[unclear]` spot so the user can check it.

## Example

Before:

> hi bhaiya so um I was calling about the the flat basically the tap in the kitchen is leaking since like Monday and um the plumber you sent he came but he said part is not there so can you uh can you send someone again maybe Saturday morning before eleven thanks

After:

> Hi bhaiya, the kitchen tap in the flat has been leaking since Monday. The plumber you sent came, but he said the part wasn't available. Can you send someone again, maybe Saturday morning before 11? Thanks.
