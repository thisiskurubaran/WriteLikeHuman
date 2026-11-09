# Saving your voice in Claude

Explain how to keep a voice profile or a team style guide inside a Claude Project, so it applies automatically instead of being attached to every chat.

The skill itself never stores anything. This module tells the user how to store their own profile in their own Claude account, if they want to.

## When this applies

- "Can you remember my voice?", "I don't want to paste my profile every time", "how do I make this always use our house style?"
- After building a voice profile or a style guide, when the user asks how to reuse it.
- Offer this at most once per conversation, after a profile or style guide is made.

## What stays the same

- The profile is the user's own. You explain where to put it; you don't save it anywhere yourself.
- The profile's content. Don't rewrite it while explaining how to save it.

## Steps

Explain it in plain words, one action per step:

1. On the Claude website or desktop app, open **Projects** and create a new project, for example "My writing" or "Northbay team".
2. Add the profile in one of two ways:
   - Paste it into the project's **instructions**, with one line before it such as "Use this voice profile when I ask you to write or rewrite anything."
   - Or save it as a file (for example `voice-profile.md`) and add it to the project's files.
3. Start chats inside that project when you want writing in that voice. WriteLikeHuman will use the profile it finds there.
4. Projects made on the web or desktop show up in the Claude phone app too, under the same account.
5. To change the profile later, edit the project instructions or replace the file. New chats in the project use the new version.

Several profiles ("work me" and "personal me") can live in separate projects, or in one project with a line saying which to use when.

## Privacy

- Keep the profile about how the user writes: sentence length, words they like, greetings, sign-offs.
- Don't put other people's personal details in it: phone numbers, addresses, health information, or private messages from friends and family.
- For a team style guide in a shared project, remember that everyone with access to the project can read it.

## Output

The short steps above, adapted to what the user has (a personal voice profile or a team style guide), in plain words. Mention that if they'd rather not use Projects, attaching the profile at the start of a chat works just as well.

## Example

User: "This profile is great. Do I have to paste it every time?"

Reply:

> You don't have to. You can keep it in a Claude Project:
>
> 1. Open Projects on the Claude website and create one called "My writing".
> 2. Paste your profile into the project's instructions, starting with: "Use this voice profile when I ask you to write or rewrite anything."
> 3. Start your chats inside that project. It works in the phone app too.
>
> To change the profile later, just edit the instructions. Keep it about how you write, not about other people.
