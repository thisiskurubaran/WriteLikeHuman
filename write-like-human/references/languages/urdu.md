# Urdu

Rewrite Urdu so it sounds like a person wrote it, in the Urdu people actually speak and write.

## When this applies

- The text is in Urdu, in Urdu script (Nastaliq) or in Roman Urdu.
- The user asks for a translation into Urdu (also load `translate-humanize.md`).
- For Urdu mixed with English, load `mixed-language.md` as well.

## What stays the same

- Language and script. Urdu script stays Urdu script, Roman Urdu stays Roman Urdu. Never switch to Devanagari or translate unless asked.
- Urdu vocabulary. Urdu and Hindi share grammar but differ in words. Keep the user's Urdu choices: "شکریہ" not "dhanyavaad", "انتظار" not "pratiksha", "اطلاع" not "suchna".
- Names, numbers, dates, amounts, places, and quotes. Keep the user's digits, whether ۱۲۳ or 123.
- The register. "آپ" stays "آپ". "تم" stays "تم".

## AI tells in Urdu

- Hindi words in Urdu script. Machine translation sometimes writes Sanskrit based Hindi words in Urdu letters.
- Heavy Persian and Arabic words in a casual message: "براہِ کرم مطلع فرمائیں", "تشریف آوری" to a friend. Formal letters can keep them.
- Literal English calques like "مجھے امید ہے کہ یہ پیغام آپ کو اچھی صحت میں پائے".
- English punctuation. Urdu uses "،" for a comma and "؟" for a question mark.
- Every sentence ending in "ہے۔" with the same shape.

## Right to left text in files

Urdu is written right to left. When you edit a Word file in place, keep each paragraph's existing settings so the direction stays right. If you create new paragraphs (for example when turning a PDF into a Word file), they need right to left set: in python-docx this means adding `w:bidi` to the paragraph properties and `w:rtl` to the runs. If you cannot do that, tell the user to select the text in Word and click the right to left button.

## Steps

1. Note the script and the register, and keep both.
2. Replace Hindi slips with the user's Urdu words.
3. Swap heavy formal words for everyday ones in casual text.
4. Remove calques and fix punctuation.
5. Check names, numbers, and dates are unchanged.

## Output

The rewritten Urdu text, then a short **What I changed** list in the language the user is using with you.

## Example

Before: "محترم دوست، براہِ کرم مجھے مطلع فرمائیں کہ آیا آپ کل کی تقریب میں تشریف لائیں گے یا نہیں۔"

After: "یار عمران، کل پروگرام میں آ رہے ہو نا؟ بتا دینا۔"

Gloss: The first reads like a formal invitation reply: "Respected friend, kindly inform me whether you will grace tomorrow's function." The rewrite is a text to a friend: "Imran, you're coming to the event tomorrow, right? Let me know."

## Help wanted

This file has not yet been reviewed by a native speaker. If you speak Urdu, corrections are welcome. See CONTRIBUTING.md.
