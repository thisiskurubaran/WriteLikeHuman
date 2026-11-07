# Arabic

Rewrite Arabic so it sounds like a person wrote it, in the variety the user already writes.

## When this applies

- The text is in Arabic, in Arabic script or in Arabizi (Arabic in Latin letters and numbers, like "7abibi").
- The user asks for a translation into Arabic (also load `translate-humanize.md`). Ask which variety if it matters: Modern Standard Arabic for formal writing, or a dialect such as Egyptian, Gulf, or Levantine for messages.

## What stays the same

- Language, script, and variety. Modern Standard stays Modern Standard. Egyptian stays Egyptian. Arabizi stays Arabizi. Never translate or switch variety unless asked.
- Names, numbers, dates, amounts, places, and quotes. Keep the user's digits, whether Western (123) or Eastern Arabic (١٢٣).
- The register and the forms of address the user chose.

## AI tells in Arabic

- Translated English openers like "أتمنى أن تجدك هذه الرسالة بخير".
- Passive "تم" with a verbal noun everywhere: "تم نقل الاجتماع" where "نقلنا الاجتماع" is more natural.
- "قام بـ" chains: "قام الفريق بمراجعة" instead of "راجع الفريق".
- Random mixing of Modern Standard and dialect in one message.
- Latin punctuation. Arabic uses "،" for a comma, "؛" for a semicolon, and "؟" for a question mark.
- Long sentences chained with "و" with no breaks, copied from English structure.

## Right to left text in files

Arabic is written right to left. When you edit a Word file in place, keep each paragraph's existing settings so the direction stays right. Any new paragraphs you create (for example when turning a PDF into a Word file) need right to left set: in python-docx this means adding `w:bidi` to the paragraph properties and `w:rtl` to the runs. If you cannot do that, tell the user how to fix it in Word with the right to left paragraph button.

## Steps

1. Identify the variety and register, and keep both.
2. Replace "تم" and "قام بـ" chains with direct verbs.
3. Remove translated openers and calques.
4. Fix punctuation.
5. Check names, numbers, and dates are unchanged.

## Output

The rewritten Arabic text, then a short **What I changed** list in the language the user is using with you.

## Example

Before: "عزيزي أحمد، أتمنى أن تجدك هذه الرسالة بخير. أكتب إليك لإعلامك بأنه قد تم نقل الاجتماع إلى يوم الاثنين."

After: "مرحبًا أحمد، نقلنا الاجتماع إلى يوم الاثنين."

Gloss: "Hi Ahmed, we moved the meeting to Monday." The first uses a translated English opener and the passive "تم نقل". Both versions are Modern Standard Arabic, so the variety did not change.

## Help wanted

This file has not yet been reviewed by a native speaker. If you speak Arabic, corrections are welcome, including notes on dialects. See CONTRIBUTING.md.
