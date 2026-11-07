# Posters and flyers (images)

## When this applies

The user sends a picture of a poster, flyer, banner, menu card, or social media graphic, and wants the words to sound better: a society Diwali event poster, a tuition class flyer, a shop sale banner, an Instagram post image.

## What stays the same

- The order of the information: headline first, then details, then contact or call to action, the way it appears on the poster.
- Every date, time, price, phone number, address, website, name, and offer detail, exactly as on the image.
- Roughly the same amount of text. Posters have little space, so a rewrite should be as short or shorter.

Be plain about what you can do. You can read the text in the image, but you cannot edit the image itself. You give back clean text that the user can retype in Canva, Photoshop, PowerPoint, or whatever they made it in.

## Steps

1. Read all the text in the image, top to bottom. Note what is the headline, what is the detail, and what is small print.
2. If any part is blurry, cut off, or hard to read, list it and ask the user, rather than guessing. A wrong phone number on a poster is worse than a stiff sentence.
3. Rewrite following `ai-patterns.md`. Poster text should be short and direct: a clear headline, the key facts, and one line telling people what to do. Remove filler like "We are pleased to announce" and stacked exclamation marks.
4. Keep any slogan or brand line the user seems attached to, unless they asked for it to change.
5. Lay out the new text in the same blocks as the poster, labeled so the user knows where each line goes.

## Output

Give the text in blocks matching the poster, for example:

```
Headline:   Diwali Mela at Green Park Society
Details:    Sat 1 Nov, 5 pm to 9 pm
            Food stalls, games, and a rangoli contest
            Clubhouse lawn
Call to action: Register your stall by 25 Oct
Contact:    Meera, 98765 43210
```

Then one line: "I can't edit the image itself, but you can paste these lines into Canva or wherever you made the poster." Then the plain change summary from `SKILL.md`.

If the user only wants the headline or one line improved, give just that.

## Example

Text read from the poster, before:

> GRAND OPENING!!! We are extremely delighted to inform you that our state-of-the-art tuition centre is now open for admissions! Bring out the best in your child! Classes 6 to 10. Call 91234 56780.

After:

```
Headline:   Now open: tuition for Classes 6 to 10
Details:    Admissions open now
Contact:    Call 91234 56780
```

The class range and phone number are unchanged. "State-of-the-art" and "bring out the best in your child" are gone because they say nothing a parent can check.

## If something goes wrong

- **The image is too small or blurry to read**: ask for a clearer photo, or for the user to type the text.
- **The poster is mostly in another language**: follow the matching file in `languages/` and answer in that language.
- **There is a lot of tiny print** (terms and conditions): rewrite only the main text unless asked. Keep the small print exactly as it is, since it may have legal meaning.
- **The user asks you to make a new image**: say you can only give the text, and suggest they paste it into Canva or a similar tool.
