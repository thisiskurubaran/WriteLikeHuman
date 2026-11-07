# Platform limits and style norms

Use this with `writing/social-post.md` and `writing/bios.md`. The numbers are approximate and platforms change them. If an exact limit matters, tell the user to check in the app before posting.

## Character limits

| Platform | What | Limit (approximate) | Cut-off point to know |
|---|---|---|---|
| LinkedIn | Post | About 3,000 characters | Shows about 200 characters (two or three lines) before "see more" |
| LinkedIn | Headline | About 220 characters | |
| LinkedIn | About section | About 2,600 characters | Shows about the first 300 before "see more" |
| X (Twitter) | Post, free account | 280 characters | Links count as about 23 characters |
| X (Twitter) | Post, paid account | Much longer | Followers see the first 280 or so before "show more" |
| X (Twitter) | Bio | 160 characters | |
| Instagram | Caption | 2,200 characters | Shows about the first 125 before "more" |
| Instagram | Bio | 150 characters | |
| Instagram | Hashtags | Up to 30 per post | |
| Facebook | Post | Very long (over 60,000) | Shows a few lines before "see more" |
| WhatsApp | Status text | About 700 characters | People read it in a few seconds |
| WhatsApp | About line | About 139 characters | |
| YouTube | Video description | 5,000 characters | Shows about the first 100 to 150 |
| Threads | Post | 500 characters | |

Counting tip: emoji can count as two characters on some platforms. Leave a little room.

## Style norms

**LinkedIn.** Professional, first person, short paragraphs. Put the point in the first two lines. Three to five hashtags is normal, more looks like spam. Tagging people is fine when they were involved. Avoid one-sentence-per-line formatting through the whole post.

**X.** One idea per post. Plain and direct. One or two hashtags at most, often none. Threads: number them only if the user wants, and make each post readable alone.

**Instagram.** The photo or video does most of the work. Captions can be short. Line breaks are fine. Hashtags often go at the end or in the first comment. Five to fifteen relevant tags is common, thirty looks desperate.

**Facebook.** Written for friends, family, and local groups. Conversational. Longer personal posts are normal. Hashtags are rare.

**WhatsApp status and groups.** Very short and casual. In groups, many people read it, so stay neutral and polite.

**Threads.** Casual, conversational, like X but friendlier. Few or no hashtags.

**YouTube.** Put what the video is about in the first line or two. Links and timestamps below.

## How to use this file

- Count characters when the user's text is close to a limit. Use `scripts/word_count.py` with the characters option if available, or count carefully.
- Tell the user the count when it matters ("142 of 150 characters").
- If the text is over the limit, say so and offer a shorter version. Do not cut silently.
