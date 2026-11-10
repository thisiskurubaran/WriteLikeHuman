# Installing WriteLikeHuman

This guide is for people who have never installed anything in Claude before. It takes about two minutes. You only do it once.

## What you need

- A Claude account. Skills work on the Free, Pro, Max, Ultra, Team, and Enterprise plans.
- A computer for the first step. You upload the skill on the Claude website or the desktop app. After that you can use it on your phone too.
- The file `WriteLikeHuman.zip`. You get it from the [Releases page](https://github.com/thisiskurubaran/WriteLikeHuman/releases).

A skill is a small set of instructions that Claude reads when it needs them. WriteLikeHuman is one skill. You install one zip and everything is included.

## Step 1: Download the zip

1. Open the [Releases page](https://github.com/thisiskurubaran/WriteLikeHuman/releases).
2. Find the newest release at the top.
3. Under **Assets**, click `WriteLikeHuman.zip`.
4. Leave the file as it is. Do not unzip it.

## Step 2: Turn on file creation in Claude

Skills need Claude's "code execution" setting. This is the setting that lets Claude create and edit files for you.

1. Go to [claude.ai](https://claude.ai) or open the Claude desktop app.
2. Click your name or initials in the bottom left corner.
3. Click **Settings**.
4. Click **Capabilities**.
5. Find **Code execution and file creation**. In newer versions it may be called **Create and edit files**.
6. Turn it on.

On a Team or Enterprise plan, your organization's owner may need to turn this on for everyone first. If you cannot find the setting, ask them.

## Step 3: Upload the skill

1. In Claude, go to **Customize**, then **Skills**.
2. Click the **+** button.
3. Click **+ Create skill**.
4. Click **Upload a skill**.
5. Choose the `WriteLikeHuman.zip` file you downloaded.
6. Wait for it to finish. WriteLikeHuman now shows up in your skills list.
7. Make sure the switch next to it is on.

That is it. Start a new chat and try it.

## Using it on your phone

1. Upload the skill on the website or desktop app first (steps 1 to 3 above).
2. Open the Claude app on your phone and sign in with the same account.
3. Start a new chat and ask for something, like "Make this message sound less robotic".

Your skills belong to your account, so the phone app uses the same ones. If it does not seem to work on your phone, check that you are signed in to the same account, then try again on the website.

## Using it in Claude Code

This part is only for people who use Claude Code, the version of Claude that runs in a terminal. Most people can skip it.

The easiest way is to install it as a plugin. In Claude Code, type these two commands:

```text
/plugin marketplace add thisiskurubaran/WriteLikeHuman
/plugin install write-like-human@writelikehuman
```

The skill loads on its own when your request matches, or you can call it with `/write-like-human:write-like-human`. To get new versions later, run `/plugin marketplace update writelikehuman`.

If you'd rather not use plugins, copy the folder by hand:

1. Download and unzip `WriteLikeHuman.zip`.
2. Copy the `write-like-human` folder into `~/.claude/skills/` (create the folder if it is not there).
3. Start Claude Code. The skill loads on its own.

You should end up with `~/.claude/skills/write-like-human/SKILL.md`.

## How to use it

Just ask in your own words. You do not need special commands. Some things to try:

- "Make this email sound less robotic"
- "Humanize this Word file" (then attach the file)
- "Does this sound like AI?"
- "Write a farewell speech for my manager"
- "Reply to this WhatsApp from my landlord"
- "Make this simpler for my dad"
- "Show me each change so I can approve it"

You get your text back first, then a short list of what changed and why. When you send a file, you get a new copy back named with `-humanized` at the end. Your original file stays as it was.

## Something not working?

**The upload fails.**
This usually means the zip was opened and zipped again by hand. The zip must hold the `write-like-human` folder, not the loose files inside it. Download a fresh copy from the [Releases page](https://github.com/thisiskurubaran/WriteLikeHuman/releases) and upload it without unzipping. If you built the zip yourself, zip the folder itself, not its contents.

**The upload button is missing.**
Check step 2. Code execution and file creation must be turned on. On a work account, your organization may have skills turned off. Ask your admin.

**Claude does not use the skill.**
Say its name in your message, for example: "Use WriteLikeHuman to make this sound more natural." Also check that the switch next to it in **Customize > Skills** is on.

**It still behaves like an older version.**
After uploading a new zip, check that **Customize > Skills** shows only one WriteLikeHuman and that it's switched on. Then start a new chat, since an open chat keeps the skill it started with. In Claude Code, run `/plugin marketplace update writelikehuman` and restart Claude Code.

**It gave me a short menu instead of doing anything.**
That happens when the message doesn't say what you want, like "help with this" and some text. Pick a number, or say it in your own words: "rewrite it", "reply to it", "check it before I send". A clear request skips the menu.

**It answered in English when I wrote in Hindi, Tamil, or another language.**
The rewrite stays in your language and script. The short "What I changed" list follows the language you asked in, so if you asked in English, the list is in English. To get everything in your language, ask in that language, or add "reply in Tamil".

**It asked me whether something really happened.**
That's on purpose. It won't add an experience, achievement, or qualification to a form, resume, or letter until you confirm it's true. Answer yes with the details, or leave it out.

**It asked which date I meant.**
Also on purpose. A date like 03/04 can mean 3 April or 4 March, so it keeps the date as you wrote it, or asks before writing the month out.

**Your file is too big.**
Very large files can fail to upload or take a long time. Try sending one chapter or a few pages at a time, or paste the text straight into the chat.

**It changed something it should not have.**
Please tell us by opening an issue on GitHub. Describe what happened using made up text. Do not attach your real personal files.
