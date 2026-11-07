# Voice profile from a chat export

Build a voice profile from the user's own messages in an exported WhatsApp chat. This is a way to collect writing samples quickly. The profile itself is built the same way as in `voice/voice-profile.md`.

## When this applies

- The user attaches a WhatsApp chat export (a `.txt` file, sometimes inside a `.zip`) and asks to learn how they write.
- They accept your offer to build a voice profile and say "use my WhatsApp messages".

## Privacy first

A chat export holds other people's messages, phone numbers, and private details. Handle it carefully:

- Use only the user's own messages. Drop everyone else's messages before you look at the text. Never quote, summarise, or learn from other people's messages.
- Remove phone numbers, email addresses, and links from the user's messages before using them.
- Do not store the chat or the filtered messages anywhere. Use them for this profile and nothing else.
- Do not put anything private in the profile: no names of other people, no addresses, no account or order details.
- Before starting, suggest the user pick a chat they are comfortable sharing, such as a group where they write a lot about ordinary things. A chat with sensitive health, money, or family matters is a poor choice.

If the user is not sure they want to share a chat, offer the simpler route: they paste 10 to 20 of their own messages.

## What stays the same

- Everything in `voice/voice-profile.md`: the profile describes only the user's own voice, and it changes how text sounds, not what it says.
- The user's language mix. If their messages mix Tamil and English in Roman script, the profile says so.

## Steps

1. Tell the user in one line what will happen: "I'll keep only your messages, remove numbers and links, and build a short profile. Nothing gets saved."
2. Find the sender names in the export:

   ```
   python scripts/chat_export_filter.py EXPORT.txt --list-senders
   ```

3. Ask which name is theirs, if it is not obvious.
4. Pull out only their messages:

   ```
   python scripts/chat_export_filter.py EXPORT.txt --sender "Name" -o my-messages.txt --max 300
   ```

   `--max` limits how many messages are used. 300 is plenty.
5. Read `my-messages.txt` and build the profile following the steps in `voice/voice-profile.md`. Sample lines in the profile must come from the user's messages only, short ones, with nothing private in them.
6. Show the profile, ask if anything is off, and hand it over with the saving instructions from `voice/voice-profile.md`.
7. Mention that chat messages show their casual voice. For a work profile, they need work samples too.

## If something goes wrong

- If the script fails or the export format is unusual, do not read the whole chat to sort it yourself. Ask the user to paste 10 to 20 of their own messages instead, and build the profile from those.
- If the export has media placeholders ("<Media omitted>") or system lines ("Messages are end-to-end encrypted"), the script skips them. If you still see them, ignore them.

## Output

The filled voice profile, then one line on saving it. Do not show the filtered messages back to the user unless they ask.

## Example

The user attaches `WhatsApp Chat with Flat 3B Group.txt` and says "make a personal profile from my messages, I'm Divya".

Result (excerpt):

> Profile name: personal me
>
> Sentence length: very short, often no full stop at the end.
>
> Words and phrases I use: "ok done", "will check", "sorry late reply", "haan".
>
> Emoji: thumbs up and the laughing face, usually one at the end.
>
> Sample lines: "ok done, will bring the keys by 7", "sorry late reply, was driving"

Used 214 of your messages. Other people's messages, numbers, and links were left out.
