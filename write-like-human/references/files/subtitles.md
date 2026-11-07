# Subtitle files (.srt, .vtt)

## When this applies

The user attaches a subtitle file: captions for a YouTube video, a reel, a course lesson, a wedding film, or a company talk. Usually `.srt`, sometimes `.vtt`. Common requests: "these auto captions sound weird", "clean up my subtitles", "make the captions read naturally".

Load `writing/voice-notes.md` too when the captions came from automatic speech recognition, since they share the same problems (fillers, mishearings, no punctuation).

## What stays the same

- Every timing line (`00:00:01,000 --> 00:00:03,500`), exactly. Timings line the words up with the video. Changing them puts captions out of sync.
- Cue numbers and their order.
- The number of captions. Do not merge or split cues, because each one is tied to its own moment in the video.
- What the speaker said. Captions show speech, so keep the speaker's meaning and their way of talking. Clean it up, do not rewrite it into an essay.
- Names, numbers, dates, product names, and any words in another language the speaker used on purpose.
- Speaker labels (`[Asha]`, `- `), sound notes (`[music]`, `[laughs]`), and styling tags (`<i>`).

## Steps

1. Get the captions with ids:
   ```
   python scripts/srt_rewrite.py extract <file>.srt -o cues.json
   ```
   Each caption has an id, its timing, its text, how many seconds it shows on screen, and its longest line.
2. Rewrite only the text. Fix punctuation, obvious mishearings (only when the meaning is clear from context), stray fillers, and stiff wording. Keep it spoken: contractions, short phrases, and the speaker's own words.
3. Keep captions easy to read:
   - About 42 characters per line at most
   - Two lines per caption at most
   - Roughly the same length as before, so people have time to read it before it disappears (about 21 characters per second is the upper limit)
4. Write only changed captions to a JSON file, `{"12": "new text", ...}`. Use `\n` for a line break inside a caption.
5. Apply:
   ```
   python scripts/srt_rewrite.py apply <file>.srt changes.json
   ```
6. Read the `CHECK:` lines. They flag captions that are too long or too fast. Shorten those and apply again.
7. If something is unclear in the audio and you cannot tell from context, leave it as it was or mark it `[unclear]`. Do not guess a name or number.

## Output

- Return `<original-name>-humanized.srt` (or `.vtt`). Timings are copied from the original, and the script refuses to run if any timing changed.
- Then the plain change summary from `SKILL.md`, plus one line confirming the timings were not changed.
- Do not paste the whole file back into the chat.

## Example

Before:

```
7
00:01:12,400 --> 00:01:15,900
so um basically what we did was we we
leveraged the the new oven

8
00:01:16,000 --> 00:01:18,200
and uh the cakes came out way better
```

After:

```
7
00:01:12,400 --> 00:01:15,900
So what we did was
switch to the new oven,

8
00:01:16,000 --> 00:01:18,200
and the cakes came out way better.
```

The timings and cue numbers are identical. "Way better" stays because that is how the speaker talks.

## If something goes wrong

- **The script will not run**: edit the file by hand in the same way. Copy every number and timing line exactly, change only the text lines, and keep a blank line between captions. Tell the user you did it by hand.
- **The file has formatting the script does not know** (advanced `.vtt` with positioning, `.ass` or `.ssa` files): do not risk breaking it. Give the user a list of caption number and new text to paste in their subtitle editor.
- **Captions are burned into the video**: they are part of the picture and cannot be edited as a file. Tell the user they need the subtitle file from whoever made the video, or offer to clean up a transcript instead.
- **The captions are in another language**: load the matching file from `languages/`. Never translate unless asked.
