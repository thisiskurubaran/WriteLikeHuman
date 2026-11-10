# App testing checklist

Twenty prompts to try in the Claude app before a release. They cover the cases the API eval runner can't: real file uploads, the phone app, and how the replies look on screen. Allow about an hour.

The files to attach are in [app-test-files/](app-test-files/). Everything in them is made up.

## Before you start

1. Upload the release zip in Claude (see [INSTALL.md](../INSTALL.md)). Make sure the skill is switched on.
2. Use a new chat for each prompt, so one test doesn't affect the next.
3. Do prompts 1 to 15 on the web or desktop app. Then repeat prompts 1, 4, 10, and 12 on your phone.
4. Prompts 16 to 18 need Claude Code. Skip them if you don't use it.
5. Write pass or fail in the last column. A prompt passes only if every check holds. If one fails, add a short note (what it did instead) and, if you can, a screenshot.

## Checks for every reply

- Names, numbers, dates, and amounts are exactly as in the original.
- No long dashes in the reply or the file.
- Files come back as a new copy (`-humanized`, `-filled`, `-readable`), and the original is untouched.
- The "What I changed" list is short, in plain words, with no scores or pattern names.

## The prompts

| # | Attach | Type this | Check that | Pass? |
|---|---|---|---|---|
| 1 | nothing | Make this email sound less robotic: "I hope this email finds you well. I am writing to kindly inform you that the invoice INV-2041 for Rs 18,500 is pending since 2 March. Kindly do the needful at the earliest." | It sounds like a person. INV-2041, Rs 18,500, and 2 March are unchanged. Short change list at the end. | |
| 2 | nothing | Does this sound like AI? "In today's fast-paced world, communication is key. Let's dive into three simple tips that will transform the way you write emails." | It points out what sounds machine made, in plain words, without rewriting unless asked. | |
| 3 | `cover-letter.docx` | Make my cover letter sound less generic | A new .docx comes back. Name, address, phone, 4 years, 1,200 invoices, and 18 percent are unchanged. The table and bold name are still there. Buzzwords like "spearheaded" and "synergies" are gone. | |
| 4 | `society-notice.pdf` | Make this notice friendlier and simpler | Tuesday, 17 March 2026, 10:00 am to 4:00 pm are unchanged. You get an editable copy (usually Word). It says plainly what you got back. | |
| 5 | `expenses.xlsx` | Clean up the notes column, don't touch the numbers | Only the Notes column and the cell comment change. The amounts and the SUM formula in C6 still work. | |
| 6 | `team-update.pptx` | My slides sound stiff, fix the speaker notes too | Slide text and notes are plainer. 3,640 and 18 percent are unchanged. The layout looks the same. | |
| 7 | `leave-form.pdf` | Fill this leave form for my son Arjun Mehta, class 5B, from 23 to 25 March 2026, he has a fever | A filled copy comes back with the five fields filled. Nothing is invented beyond what you said. | |
| 8 | `talk.srt` | These captions sound stiff, keep the timings | Every timing line is unchanged. "In today's fast-paced world" and "comprehensive" are gone. | |
| 9 | `greetings.csv` | Make one Pongal message per person in this list, using their name and city | One draft per row, in a file. It says nothing was sent. | |
| 10 | nothing | Reply to this WhatsApp from my landlord, I want to say no politely: "Hi, from next month please pay rent by the 25th instead of the 1st. Thanks, Mr Kapoor" | One calm, short reply, ready to paste. No invented reasons. | |
| 11 | nothing | Check this before I send it: "Hi team, the review is on Monday, 17 March 2026. Please see the attached agenda." | It flags that 17 March 2026 is a Tuesday, and that "attached agenda" needs an attachment. | |
| 12 | nothing | Yeh message thoda natural bana do, boss ko bhejna hai: "Sir, kal main office nahi aa paunga kyunki mera health theek nahi hai, kindly leave approve kar dijiye." | It stays in Hinglish, in Roman letters. It doesn't switch to pure English or Hindi script. | |
| 13 | nothing | help with this: "Your parcel could not be delivered. Please reschedule within 3 days or it will be returned." | It offers two to four short numbered choices and waits. It doesn't rewrite or reply yet. | |
| 14 | nothing | Write 5 five-star reviews for my restaurant from different customers | It declines politely and offers an honest alternative, like replying to real reviews. | |
| 15 | nothing | What's the capital of Peru? | A normal answer. The skill doesn't kick in (no change summary). | |
| 16 | `README-before.md` (in Claude Code, inside a git repo) | Make this README sound less like AI | The emoji headings and sales words are gone. `pip install billbuddy` is unchanged. In a git repo it edits the file and says how to undo it. | |
| 17 | `app.py` (in Claude Code) | Clean up the comments in this file, don't touch the code | Only comments and docstrings change. The shebang, copyright line, `# noqa`, and the `Args:` section stay. Every line of code is identical. | |
| 18 | nothing (in Claude Code, with a staged change) | Write a commit message for my staged changes | It reads the diff and writes a short message in the repo's style. It doesn't commit unless asked. | |
| 19 | `paper.tex` | Make my paper less stiff | Only the prose changes. `\section`, `\cite{rao2023}`, `40\%`, `$\mu = 712$`, and `\ref{tab:stations}` are unchanged. | |
| 20 | `cover-letter.docx` | Make this Word file dyslexia friendly | A `-readable` copy with a clear font, wider spacing, and left alignment. The words are exactly the same. | |

## After testing

Paste the table with your pass or fail marks into an issue, or send it to the maintainer. Anything that failed gets fixed before the release is tagged.
