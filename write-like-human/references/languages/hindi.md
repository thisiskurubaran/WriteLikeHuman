# Hindi

Rewrite Hindi so it sounds like a person wrote it, in the Hindi people actually speak and write.

## When this applies

- The text is in Hindi, in Devanagari or in Roman script.
- The user asks for a translation into Hindi (also load `translate-humanize.md`).
- For Hindi mixed with English, load `mixed-language.md` instead or as well.

## What stays the same

- Language and script. Hindi stays Hindi. Devanagari stays Devanagari. Never translate into English unless asked.
- Names, numbers, dates, amounts, places, and quotes.
- The register. If the writer uses "aap", keep "aap". If they use "tum", keep "tum".
- English words people use every day in Hindi: मोबाइल, बैंक, फ़ॉर्म, ऑफ़िस, टिकट. Do not swap them for rare Sanskrit words.

## AI tells in Hindi

- Textbook Sanskritized Hindi. Words like "दूरभाष" for phone, "संगणक" for computer, "प्रतीक्षा" in a casual note. People use "फ़ोन", "कंप्यूटर", "इंतज़ार".
- Literal English calques. "मैं आशा करता हूँ कि यह संदेश आपको अच्छे स्वास्थ्य में पाता है" is "I hope this finds you well" word for word. Nobody writes this.
- Overuse of formal forms. "कृपया", "अवश्य", "सादर" in every line of a casual message.
- Passive government style where it does not belong: "आपको सूचित किया जाता है कि..." in a note to a friend.
- Same sentence shape repeated, each ending in "है।"
- Wrong gender agreement or stiff word order copied from English.

Formal letters to a bank or office can be formal. The problem is formal words in a casual message.

## Steps

1. Work out who the reader is and keep the user's register.
2. Swap textbook words for everyday Hindustani where the context is casual.
3. Remove calques and rewrite them the way a Hindi speaker would say them.
4. Vary sentence length. Check gender and number agreement.
5. Check names, numbers, and dates are unchanged.

## Output

The rewritten Hindi text, then a short **What I changed** list. Write the summary in the language the user is using with you. If they wrote to you in English, the summary can be in English.

## Example

Before: "प्रिय मित्र, मैं आशा करता हूँ कि आप स्वस्थ होंगे। कृपया मुझे सूचित करें कि आप कल के कार्यक्रम में उपस्थित होंगे अथवा नहीं।"

After: "अरे अमित, कैसे हो? कल के प्रोग्राम में आ रहे हो ना? बता देना।"

Gloss: The first version reads like a government letter: "Dear friend, I hope you are healthy. Kindly inform me whether you will be present at tomorrow's event." The rewrite is how you would text a friend: "Hey Amit, how are you? You're coming to tomorrow's event, right? Let me know."
