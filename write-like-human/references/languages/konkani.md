# Konkani

Rewrite Konkani so it sounds like a person wrote it, in the user's own script and dialect.

## When this applies

- The text is in Konkani, in any script: Devanagari, Roman (Romi), Kannada, or Malayalam script.
- The user asks for a translation into Konkani (also load `translate-humanize.md`). Ask which script and dialect they want if it is not clear.
- For Konkani mixed with English, also load `mixed-language.md`.

## What stays the same

- Language. Konkani stays Konkani. Never translate unless asked.
- The script. Konkani is written in several scripts, and people feel strongly about theirs. Devanagari stays Devanagari, Romi stays Romi, Kannada script stays Kannada script. Never switch scripts unless asked.
- The dialect. Goan, Mangalorean, and other Konkani differ in words and grammar, and between communities. Keep the user's dialect and their spellings. Do not "standardise" it.
- Forms of address and respect: तुम / tum, तूं / tum, or a title. Keep the user's choice.
- Names, numbers, dates, amounts, and places.

## AI tells in Konkani

- Marathi or Hindi words and grammar slipping in, a common machine translation error, especially in Devanagari.
- Sanskrit-heavy textbook words in a casual message.
- Word for word English openers and closers.
- Switching between dialects or spellings within one text.
- Formal written phrasing in a family chat.

## Steps

1. Note the script, the dialect, and the user's spellings, and keep all three.
2. Replace Marathi, Hindi, or textbook words with everyday Konkani from the user's dialect. If you are not sure a word belongs to their dialect, leave it as they wrote it.
3. Rewrite translated phrases the way a Konkani speaker would say them.
4. Check names, numbers, and dates are unchanged.

Because Konkani varies so much, make fewer changes rather than more. Fix what is clearly stiff and leave the rest.

## Output

The rewritten Konkani text, then a short **What I changed** list in the language the user is using with you.

## Example

Before (Romi Konkani, to family): "Krupaya kollounk di, tumi faleam yetat vo na."

After: "Faleam yetat mhunn sang, hanv vaat polletam."

Gloss: "Tell me if you're coming tomorrow, I'll be waiting." The first sounds like a formal request. The rewrite is how someone would text family, in the same Romi script.

## Help wanted

This file has not yet been reviewed by a native speaker. If you speak Konkani, corrections are welcome, especially for dialects and scripts other than Romi. See CONTRIBUTING.md.
