# Translate and humanize

Translate text so it reads like a native speaker wrote it, not like a machine went word by word.

## When this applies

- The user asks to translate: "Translate this into Hindi", "Put this in Spanish for my landlord", "Can you write this in Tamil?"
- The user has a machine translation that sounds stiff and wants it fixed.

Never translate when the user did not ask. A message in Hindi gets a rewrite in Hindi, not an English version.

## Which files to also load

Load the file for the target language as well:

| Target | Also load |
|---|---|
| Hindi | `hindi.md` |
| Tamil | `tamil.md` |
| Telugu | `telugu.md` |
| Kannada | `kannada.md` |
| Malayalam | `malayalam.md` |
| Bengali | `bengali.md` |
| Marathi | `marathi.md` |
| Spanish | `spanish.md` |
| French | `french.md` |
| German | `german.md` |
| English for an Indian reader | `indian-english.md` |
| A code-mixed result (Hinglish, Tanglish) | `mixed-language.md` |

For a language with no file, follow the general steps here and keep it plain.

## What stays the same

- Names of people, places, companies, and products. Do not translate "Sharma Traders" into anything.
- Numbers, dates, times, money amounts, phone numbers, addresses, and reference numbers.
- Quotes that must stay in the original, legal terms with a fixed meaning, and brand names.
- The meaning and the level of politeness. A polite request stays a polite request.

## Choose the register first

Most languages make you pick how formal to be. Decide before you write a single line:

| Language | Formal | Informal |
|---|---|---|
| Hindi | aap | tum (tu only for very close people) |
| Spanish | usted | tú (vos in parts of Latin America) |
| French | vous | tu |
| German | Sie | du |
| Tamil | neenga | nee |

Pick by who the reader is. A landlord, bank, teacher, or stranger gets the formal form. A friend, sibling, or child gets the informal one. If you cannot tell and it matters, ask in one line.

## Signs of machine translation

- Word order copied from English.
- Idioms translated literally ("break the ice" turned into a sentence about actual ice).
- Every sentence the same length and shape.
- Formal words in a casual message, or casual words in an official one.
- English terms swapped for rare native words nobody uses, when people actually say the English word (for example "mobile", "bank", "form" in Indian languages).

## Steps

1. Read the whole text and work out what it is for and who will read it.
2. Pick the register.
3. Translate the meaning sentence by sentence, not word by word.
4. Replace English idioms with what a native speaker would say, or with plain words.
5. Read it back as a native reader. Fix anything that sounds like a textbook or a form.
6. Check that every name, number, and date matches the original exactly.

## Honest labeling

For legal, official, immigration, court, medical, or exam use, add one line to the user: "This is a translation. If it is for an official or exam use, it may need to say so, or need a certified translator." Do not present the translation as if the user wrote it in that language when the context needs disclosure.

## Output

The translated text, then a short **What I changed** list that notes the register you chose and any idiom you replaced. If you could not keep a phrase exact, say so.

## Example

Request: "Translate this into Hindi for my landlord."

Before (English): "Hi Mr. Verma, the kitchen tap has been leaking since Monday. Could you send someone this week? Thanks, Priya"

Machine style: "नमस्ते श्री वर्मा, रसोई का नल सोमवार से रिसाव कर रहा है। क्या आप इस सप्ताह किसी को भेज सकते हैं? धन्यवाद, प्रिया"

After: "नमस्ते वर्मा जी, रसोई का नल सोमवार से टपक रहा है। क्या आप इस हफ़्ते किसी को भेज देंगे? धन्यवाद, प्रिया"

Gloss: "रिसाव कर रहा है" is a textbook way to say "leaking". People say "टपक रहा है" (dripping). "वर्मा जी" is how you politely address a landlord. "हफ़्ते" is the everyday word for week.
