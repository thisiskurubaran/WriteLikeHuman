# Slides (.pptx, Google Slides)

## When this applies

The user attaches a PowerPoint file (`.pptx`) or shares Google Slides and wants the slide text, the speaker notes, or both to sound more natural. Typical cases: a team update deck, a class presentation, a pitch to a client, a wedding slideshow with captions.

If the user is going to read the notes aloud, also load `writing/speeches.md`, since spoken text needs shorter sentences.

## What stays the same

- Layout, positions, sizes of text boxes and shapes
- Fonts, colours, bold, bullet styles, slide themes
- Pictures, charts, diagrams, videos, animations, transitions
- Slide order and the number of slides
- Tables of figures and chart labels
- Slide numbers, dates, logos in the master slide
- Protected content from the core rules: names, numbers, dates, money, quotes, product names

Only the words in text boxes, table cells, and speaker notes change.

## Steps

1. **Ask what to cover** only if it is unclear: "Slide text, speaker notes, or both?" If the user said nothing, do both.
2. **List the text:**
   ```
   python scripts/pptx_rewrite.py extract <file>.pptx -o segments.json
   ```
   Each paragraph has an id like `s3-2-1` (slide 3, shape 2, paragraph 1), `s3-2.1-1` for a shape inside a group, `s3-4-r2c3-1` for a table cell, and `s3-notes-1` for speaker notes. Slide text also shows `chars`, its current length.
3. **Rewrite slide text with length in mind.** A text box is a fixed size. Longer text spills out of the box or shrinks to an unreadable size.
   - Keep each new line at or under the old length. A little shorter is better.
   - Bullets stay as short fragments, not full sentences. "Sales up 12% in Q3" is fine on a slide.
   - Do not turn one bullet into two or merge bullets. Each paragraph id maps to one line.
   - Titles: cut AI filler ("Harnessing Synergies for Tomorrow"), keep them short and plain ("Next year's plan").
4. **Rewrite speaker notes** more freely. Notes are not limited by a box. Write them the way a person talks: short sentences, "we", contractions where the speaker would use them. Keep any figures exactly.
5. **Keep the deck consistent.** The same term should be used the same way on every slide.
6. **Write changes as JSON** (id to new text) and apply:
   ```
   python scripts/pptx_rewrite.py apply <file>.pptx changes.json
   ```
7. **Read the CHECK lines.** `may not fit its box` means the new text is noticeably longer than the old. Shorten it. `numbers differ` means a figure changed. Fix it.
8. **Quick re-check** against `ai-patterns.md`. Then stop.

## With a Google connector

When the user links a Google Slides deck and a Google Drive or Slides connector is attached, edit the deck itself instead of asking for a download.

1. Make a copy first, named `<title> (humanized)`, and edit the copy. Edit the original only if the user clearly says to.
2. Change only the text in text boxes, tables, and speaker notes, by the same rules as above. Leave layouts, images, charts, and the figures in them alone.
3. Keep each text box about as long as before, so nothing spills off the slide.
4. Tell the user where the copy is and give the change summary.

Without a connector, ask the user to download it (**File > Download > Microsoft PowerPoint (.pptx)**) and attach it, or paste the slide text and notes. If they paste, give it back slide by slide with "Slide 1", "Slide 2" labels so they know where each line goes.

## Creating a new deck

When the user wants new slides ("make 5 slides for my team meeting from these notes"), this is draft mode. Write the content first, then build the `.pptx` with Claude's built in pptx skill.

1. Ask how many slides only if it matters and the user didn't say. Otherwise pick a number that fits the notes, usually 5 to 8.
2. Start with a title slide: the topic, and the speaker's name or team if the user gave it.
3. One idea per slide. A plain title that says what the slide is about ("What we shipped in March"), not a slogan.
4. Slide text stays short: three to five bullets, each a few words. No full paragraphs on a slide.
5. Put the explanation in the speaker notes, written the way the person talks, with figures exactly as the user gave them.
6. Use only the user's facts. Never invent numbers, charts, quotes, customer names, or results to make a slide look fuller. If a slide would be empty, say so or drop it.
7. Plain layout: the default theme or the user's own template (see `files/templates.md`). No decorative effects the user didn't ask for.
8. Name the file after what it is, like `team-update.pptx`, and say in one line how many slides it has.

## Output

- Return `<original-name>-humanized.pptx`. The original is never overwritten.
- Then the change summary. Mention if you only did notes or only slide text, and flag any slide where text might be tight:
  > - Shortened the title on slide 4 so it fits on one line.
  > - Rewrote the speaker notes on all 8 slides so they're easier to say out loud.

## Example

Slide 2 of `q3-review.pptx`.

Slide text, before:
> Frictionless Onboarding Journey for 40 New Clients

Slide text, after:
> Onboarded 40 new clients

Speaker notes, before:
> Let's take a moment to dive into how our team harnessed innovative strategies to drive a transformative onboarding experience for our 40 valued clients.

Speaker notes, after:
> This quarter we brought on 40 new clients. Most of them were set up within a week, which is faster than last year.

Wrong: "faster than last year" is only allowed if the original notes or the user said so. If they didn't, leave it out:
> This quarter we brought on 40 new clients. Here's how the setup went.

## If something goes wrong

- **The script fails or python-pptx is missing:** use Claude's built in pptx skill if it is there, with the same rules. If not, give the new text slide by slide ("Slide 3, title: ...", "Slide 3, notes: ...") so the user can paste it in.
- **Text is inside a picture** (a screenshot of a slide, a poster image): the script cannot see it. Tell the user which slides have text in images and offer to rewrite it if they paste the words.
- **Charts and SmartArt:** labels inside charts and diagrams are not changed. Mention it if they contain wording the user might want fixed.
- **The file is .ppt (old format) or .key (Keynote):** ask them to save or export as .pptx, or paste the text.
- **A slide looks crowded after the change:** go back and cut words. Never shrink fonts or move boxes yourself.
