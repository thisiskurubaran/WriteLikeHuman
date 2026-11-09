# Script conversion

Write the same words in a different script. Roman letters to Hindi script, Tamil letters to Roman, and so on. This is not translation: the language and the words stay exactly the same, only the alphabet changes.

## When this applies

Only when the user asks, in words like:

- "Write this in Hindi script", "put this in Devanagari"
- "Type this in Tamil letters", "convert to Telugu script"
- "Write this in English letters", "convert to Roman", "I can't read the script, write it in ABC"

Scripts covered:

- Roman (Latin letters) to and from Devanagari, for Hindi, Marathi, Nepali, and Konkani
- Roman to and from Tamil, Telugu, Kannada, Malayalam, Bengali, Gujarati, and Gurmukhi (Punjabi)
- Roman to and from Urdu in Nastaliq, which runs right to left

If the user only wants the message to sound more natural, this is not the module. Use the language file or `mixed-language.md` and keep their script. Never change someone's script without being asked.

## What stays the same

- The language and the words. Hinglish stays Hinglish, just written in Devanagari. Nothing is translated, added, or reworded.
- Numbers, amounts, dates, and times, written as digits the way the user wrote them (10 baje stays 10 बजे, not दस बजे).
- Names of products, brands, and apps, emails, links, phone numbers, and codes such as PNR or order numbers. These stay in Roman letters.
- People's names are converted, since that is what people do in WhatsApp, unless the user says to keep them in Roman.
- Line breaks, emoji, and punctuation.

## Steps

1. Confirm the target script from the request. If the user says "Hindi script" for Marathi text, use Devanagari with Marathi spelling.
2. Convert word by word, keeping the user's word order.
3. Roman input is often ambiguous. People write "kal" for both yesterday and tomorrow (it is the same word in Hindi, कल), "d" for both द and ड, "t" for both त and ट, and rarely mark long vowels ("dil" or "deel"). Pick the common everyday spelling for each word.
4. English words inside Hinglish or Tanglish: by default, write them in the target script the way people do in chats (meeting becomes मीटिंग, office becomes ऑफ़िस). If the user prefers English words left in Roman, follow that. Ask once at most, not for every message.
5. Keep the protected items above unchanged.
6. For Urdu, write in Nastaliq, right to left, and keep digits as the user wrote them. In a Word file, set the paragraph direction to right to left (see `urdu.md`).
7. List any word that could reasonably be spelled two ways, so the user can check it. Keep the list short: only real doubts, not every word.

## Output

The converted text first, ready to copy. Then, if needed, one short line: "Check these: कल (could mean yesterday or tomorrow, I kept it as written), डेट or देट?" No change summary, since nothing was rewritten.

## Example

Roman to Devanagari. User: "Write this in Hindi script: Kal meeting 10 baje hai, office time pe aa jana."

> कल मीटिंग 10 बजे है, ऑफ़िस टाइम पे आ जाना।

Gloss: "The meeting is at 10 tomorrow, come to the office on time." Same words, same order. Only the script changed. "Meeting" and "office" are written in Devanagari the way people type them in WhatsApp.

Tamil to Roman. User: "I can't read Tamil script, write this in English letters: நாளை காலை 9 மணிக்கு வருகிறேன்."

> Naalai kaalai 9 manikku varugiren.

Gloss: "I will come at 9 tomorrow morning." Still Tamil, now in Roman letters. The 9 stays a digit.

## Help wanted

This file has not yet been reviewed by native speakers. If you write any of these scripts every day, corrections to the spellings and examples are welcome. See CONTRIBUTING.md.
