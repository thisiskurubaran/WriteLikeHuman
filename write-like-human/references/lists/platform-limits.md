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

## Ready to paste

When the user will paste the result straight into an app, format it for that app. Most apps do not show Markdown, so `**bold**`, `#` headings, and `-` bullets appear as plain symbols. Leave them out unless the app supports them.

LinkedIn. Plain text only. Blank lines between paragraphs survive, so use them. The post is cut after about two lines (roughly 200 characters) with "see more", so the point must sit above that cut. Hashtags go on their own line at the end. Bullets, if the user wants them, are plain characters like a hyphen or a dot at the start of a line.

X. Plain text. If the post is too long, offer to shorten it before offering a thread. For a thread, separate the posts with a blank line and a label like "Post 1" so the user can see where each one ends. Add "1/4" numbering inside the posts only if the user wants it. Hashtags inline or at the end, one or two.

Instagram. Plain text. Line breaks usually survive, but several blank lines in a row may collapse, so keep paragraph breaks simple. Only the first line or two show before "more", so the hook goes there. Hashtags at the end after a blank line, or offer them separately for the first comment.

Facebook. Plain text, line breaks survive. Hashtags rarely needed.

WhatsApp messages and status. WhatsApp has its own formatting: `*bold*`, `_italic_`, `~strikethrough~`, and a hyphen or number at the start of a line for lists. Use these sparingly and only where the user would. Never use Markdown double asterisks, which show up as stars. Keep status updates to a line or two.

Email and plain forms. Plain paragraphs with blank lines between them. No Markdown symbols.

In your reply, put the ready-to-paste text in a plain code block only if the user is copying it on a computer and the formatting matters (threads, WhatsApp symbols). Otherwise give it as normal text, since code blocks are awkward to copy on phones.

## How to use this file

- Count characters when the user's text is close to a limit. Use `scripts/word_count.py` with the characters option if available, or count carefully.
- Tell the user the count when it matters ("142 of 150 characters").
- If the text is over the limit, say so and offer a shorter version. Do not cut silently.
