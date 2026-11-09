# Video scripts and descriptions

Help people write scripts for YouTube videos, Instagram Reels, and YouTube Shorts, plus the description that goes under the video. Scripts are written to be spoken, not read.

## When this applies

- "Write a script for my Reel about...", "make this sound natural on camera", "fix my YouTube description".
- A creator, small business, teacher, or coach has notes or a draft and wants something they can say out loud.
- A video description, title, or pinned comment that sounds generic or stuffed with keywords.

## What stays the same

- The facts, prices, product names, dates, offers, and links the user gives.
- The creator's voice and language. Hinglish stays Hinglish, Tamil stays Tamil. Use their voice profile if they have one.
- Any claim the user makes is theirs. Don't add health, money, or results claims ("lose 5 kg in a week", "earn 1 lakh a month") or statistics they didn't give.

## Writing to be spoken

- Short sentences. One idea per breath.
- Words the creator would actually say, with contractions ("you'll", "it's").
- Natural pauses: a line break where they'd breathe. Mark a pause with "(pause)" only if they want a reading copy.
- No tongue twisters or long lists said in one go. Three items at most, and only if there are really three.
- Numbers said the way people say them: "two thousand rupees", "about ten minutes".

## Hooks without clickbait

- Open with the real point or a real question in the first line or two seconds: "Here's how I pack a week of lunches in 20 minutes."
- No fake urgency, "you won't believe", "this will change your life", or a promise the video doesn't keep.

## Steps

1. Find out the platform and length: Reels and Shorts usually run 15 to 60 seconds, YouTube videos longer.
2. Find the one thing the viewer should take away.
3. Write the hook, then the main points in the order they'll be shown, then a short, honest close (a question, a next step, or a "follow for part 2" only if there will be one).
4. Check timing. Video speech runs about 150 words a minute. Run `python scripts/word_count.py FILE --speech --wpm 150` for timing per section. If the script fails, estimate at 150 words a minute and say so.
5. For the description: one or two plain sentences on what the video covers, then links, then hashtags (a few relevant ones, not a wall). Add chapters only if the user gives the timestamps. Never make up timestamps.
6. Check every fact and price against what the user gave.

## Output

The script with simple scene or section labels if useful ("Hook", "Step 1", "Close"), the time estimate, then the description if asked. Then a short change summary.

## Example

User's notes: "reel, 30 sec, my home bakery, new eggless brownies Rs 450 for box of 6, order on WhatsApp, Pune only"

Script (about 30 seconds, roughly 70 words):

> Hook: Eggless brownies that are actually fudgy? Yes, really.
>
> These are new at our home bakery. Six brownies in a box, four hundred and fifty rupees.
>
> No eggs, and you won't miss them. Crackly top, soft middle.
>
> We deliver in Pune only for now.
>
> Close: Order on WhatsApp. The number's in our bio.

Description:

> New eggless brownies, Rs 450 for a box of 6. Delivery in Pune. Order on WhatsApp (link in bio).
>
> #EgglessBrownies #PuneBakery #HomeBaker
