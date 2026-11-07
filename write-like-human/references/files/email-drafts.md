# Email drafts in Gmail or Outlook

## When this applies

The user asks you to fix an email that is sitting in their drafts: "fix my draft to the landlord", "make the draft in my Gmail less stiff", "clean up the Outlook draft I just wrote".

This module covers drafts reached through a mail connector (a Gmail or Outlook connection set up in Claude). If the user pastes the email into the chat instead, use `writing/email.md` on the pasted text and skip this module.

## What stays the same

- The recipients (To, Cc, Bcc), the subject unless asked, and every attachment.
- Names, dates, amounts, addresses, order numbers, and links in the email.
- The quoted earlier messages below the draft, if it is a reply.
- Every other email in the mailbox. You only look at and change the one draft the user means.

Hard limits:

- Never send anything. Only edit the draft. The user presses Send themselves.
- Never create a new draft to a new recipient, or add a recipient, without asking first.
- Never delete a draft or move emails.

## Steps

1. Check whether a mail connector is available. If not, go to "If something goes wrong" below.
2. Find the draft the user means. If more than one draft could match ("the draft to Ravi" and there are two), list them by subject and date and ask which one.
3. Read the draft and, if it is a reply, the message it replies to, so the tone fits. Follow `writing/email.md` for the kind of email it is.
4. Rewrite the body following `ai-patterns.md` and the mode module. Keep the greeting and sign-off the user normally uses.
5. Show the user the new version in the chat first. If they are happy, or if they already said "just update it", save it to the same draft.
6. Confirm in one line that the draft is updated and not sent.

## Output

- The updated draft, saved in place in their drafts folder.
- In the chat: the new text, one line saying "Updated your draft. It hasn't been sent.", then the plain change summary from `SKILL.md`.

## Example

Draft in Gmail, to the building manager, before:

> Dear Sir, I am writing to bring to your kind attention that the lift in B wing has been non-functional since 3 days. Kindly do the needful at the earliest.

After:

> Dear Mr. Joshi, the lift in B wing has not been working for three days. Could you please get it repaired soon? Several elderly residents on the upper floors are finding it hard to manage. Thanks, Anil (B-503)

Only add the line about elderly residents if the user mentioned it. The recipient and subject are unchanged, and the draft is saved, not sent.

## If something goes wrong

- **No mail connector is attached**: ask the user to copy the draft into the chat. Give back a clean version to paste over the old text. Mention in one line that if they connect Gmail or Outlook in Claude's settings, you can update drafts directly next time.
- **The connector can read but not edit drafts**: give the clean version in the chat to paste back.
- **You can't find the draft**: ask for the subject line or the recipient's name.
- **Saving the draft would change the formatting** (signatures with images, tables): show the new text and ask the user to paste it in themselves, so their signature stays intact.
