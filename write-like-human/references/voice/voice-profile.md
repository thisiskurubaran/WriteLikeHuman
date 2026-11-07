# Voice profiles

Learn how the user writes from their own samples, write it down as a short profile, and use it to make rewrites sound like them. A person can keep several profiles, like "work me" and "personal me".

## When this applies

- The user pastes or attaches a voice profile.
- "Make it sound like me", "use my work voice", "write it the way I write".
- They accept your offer to build a profile, or ask to make one.
- They want to update or add to a profile they already have.

## What stays the same

- Everything in the core rules: facts, names, numbers, formatting.
- The task. A voice profile changes how the text sounds, not what it says.
- The reader's needs. If "personal me" uses lots of slang but the text is a bank letter, keep the bank letter formal and mention it.

## Where profiles live

You cannot store anything between conversations. The user keeps the profile:

- As a file (the template is `voice/voice-profile-template.md`). They attach it next time.
- As a note on their phone that they paste in.
- On claude.ai, in a Project's instructions or files, if they use Projects. Mention this as an option, not a requirement.

Tell them this plainly when you hand over a new profile: "Save this somewhere handy. Next time, paste it in or attach it and say 'use my work voice'."

## Only the user's own voice

Build profiles only from writing the user says is their own. Do not build a profile of a real third party (a celebrity, a boss, a famous author, a friend) to imitate them. If asked, decline in a line and offer to describe the general style instead ("short, punchy sentences, lots of questions") without copying the person.

## Building a profile

1. Ask for three to five samples of their own writing for one setting: work emails, WhatsApp messages, LinkedIn posts. More is better. Writing they did before using AI tools works best.
2. Ask what to call the profile and where they will use it.
3. Look at the samples and note:
   - Sentence length and rhythm.
   - Words and phrases they use often, and ones they avoid.
   - Greetings and sign-offs.
   - Punctuation habits: exclamation marks, ellipses, lowercase, commas.
   - Emoji use and which ones.
   - Language mixing (Hinglish words, Tamil endings).
   - How direct they are, how they ask for things, how they say no.
4. Fill in the template with what you found. Use their real lines as sample lines, short ones only.
5. Show it and ask if anything is off. Adjust.
6. Hand it over with the saving instructions above.

Do not record anything private in the profile: phone numbers, addresses, account details, or other people's names from the samples.

## From a WhatsApp chat export

If the user would rather not pick samples by hand, they can attach an exported WhatsApp chat and you build the profile from their own messages only. Other people's messages, phone numbers, and links are dropped first. The steps and privacy rules are in `voice/chat-export.md`.

## Several profiles

- Each profile is its own block with its own name. They can sit in one file or separate files.
- If the user attaches several, ask which one, or pick by setting ("this is an email to a client, so I'll use 'work me'") and say which you used.
- If they want to update one, change only that block.

## Applying a profile

1. Rewrite as usual (see the mode file).
2. Then adjust the result to the profile: sentence length, word choices, greetings, sign-offs, punctuation, emoji.
3. Do not overdo it. Use their habits at the rate they use them, not in every sentence.
4. If the profile conflicts with the core rules (it says "I use lots of em dashes"), follow the profile only if the user insists. Their voice is theirs.
5. Mention in the change summary that you used the profile.

## Output

When building: the filled profile, then the saving instructions.

When applying: the rewritten text, then the change summary with one line like "Matched your work voice: short sentences, 'Cheers' sign-off."

## Example

Profile excerpt ("work me"): short sentences, starts emails with "Hi" and the name, no exclamation marks, signs off "Thanks, Nisha".

Before:

> Dear Mr. Fernandes, I hope this message finds you well! I wanted to kindly follow up regarding the quotation we discussed last week. Looking forward to hearing from you! Best regards, Nisha

After:

> Hi Anil, following up on the quote we discussed last week. Could you send it over by Friday? Thanks, Nisha

"By Friday" should only be added if the user gave that date. Otherwise drop that sentence.
