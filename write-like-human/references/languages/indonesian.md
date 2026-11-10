# Indonesian

Rewrite Indonesian so it sounds like a person wrote it, at the right level of formality.

## When this applies

- The text is in Indonesian (Bahasa Indonesia).
- The user asks for a translation into Indonesian (also load `translate-humanize.md`).

## What stays the same

- Language. Indonesian stays Indonesian. Never translate unless asked.
- Formality. Formal Indonesian (bahasa baku) is right for letters, offices, and official forms. Casual Indonesian is right for chat. Keep the level the user chose.
- Forms of address. "Anda" is formal and can feel cold in chat. "Kamu" is casual. "Bapak" and "Ibu" are polite for elders and work. "Gue" and "lo" are Jakarta slang: use them only if the user already does.
- Names, numbers, dates, amounts, and places. Keep the number format (Rp1.500.000) and date format.

## AI tells in Indonesian

- Formal letter phrases in a chat: "Dengan hormat", "Bersama ini kami sampaikan", "Atas perhatiannya kami ucapkan terima kasih".
- "Anda" in a casual message to a friend or colleague.
- Translated openers: "Saya harap pesan ini menemukan Anda dalam keadaan baik".
- Overuse of "adalah" and "merupakan" where Indonesian leaves them out.
- Stacks of "di-" passives and long nouns ending in "-an": "pelaksanaan pengecekan" instead of "mengecek".
- No particles at all in chat. People soften casual messages with "ya", "sih", "kok", "dong". Use them only as the user does.

## Steps

1. Identify the formality and forms of address, and keep both.
2. Remove letter phrases from casual text, and translated openers from everything.
3. Cut extra "adalah", "merupakan", and passive stacks.
4. Vary sentence length.
5. Check names, numbers, and dates are unchanged.

## Output

The rewritten Indonesian text, then a short **What I changed** list in the language the user is using with you. Describe the changes in plain words, without word-by-word English glosses of the rewritten text.

## Example

Before: "Halo Rina, saya harap pesan ini menemukan Anda dalam keadaan baik. Saya ingin menginformasikan bahwa rapat telah dipindahkan ke hari Senin."

After: "Halo Rina, rapatnya dipindah ke Senin ya."

Gloss: "Hi Rina, the meeting's moved to Monday." The first uses a translated English opener and "Anda" in a chat with a colleague. For a formal email, keep "Anda" or "Ibu" and a fuller sentence.

## Help wanted

This file has not yet been reviewed by a native speaker. If you speak Indonesian, corrections are welcome. See CONTRIBUTING.md.
