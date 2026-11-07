# Odia

Rewrite Odia so it sounds like a person wrote it, in the Odia people actually speak and write.

## When this applies

- The text is in Odia, in Odia script or in Roman script.
- The user asks for a translation into Odia (also load `translate-humanize.md`).
- For Odia mixed with English, load `mixed-language.md` as well.

## What stays the same

- Language and script. Odia stays Odia. Never translate into English unless asked.
- Names, numbers, dates, amounts, places, and quotes. Keep the user's digits, whether ୧୨୩ or 123.
- The register. "ଆପଣ" stays "ଆପଣ". "ତୁମେ" stays "ତୁମେ". "ତୁ" stays "ତୁ".
- Everyday English words used in Odia: ମୋବାଇଲ, ବ୍ୟାଙ୍କ, ଅଫିସ, ଟିକେଟ.

## AI tells in Odia

- Bookish, Sanskrit heavy Odia in a casual note: "ଉପସ୍ଥିତ ରହିବେ", "ସୂଚିତ କରନ୍ତୁ", "ଦୟାକରି" in every line.
- Literal English calques like "ମୁଁ ଆଶା କରୁଛି ଏହି ବାର୍ତ୍ତା ଆପଣଙ୍କୁ ଭଲ ସ୍ୱାସ୍ଥ୍ୟରେ ପାଏ".
- Bengali or Hindi words slipping in, a common machine translation habit.
- Every sentence built the same way.

Formal letters can stay formal. The problem is formal words where the user wanted something casual.

## Steps

1. Work out the reader and keep the user's register.
2. Swap bookish words for everyday Odia in casual text.
3. Remove calques and words from other languages.
4. Vary sentence length.
5. Check names, numbers, and dates are unchanged.

## Output

The rewritten Odia text, then a short **What I changed** list in the language the user is using with you.

## Example

Before: "ପ୍ରିୟ ବନ୍ଧୁ, ଦୟାକରି ମୋତେ ସୂଚିତ କରନ୍ତୁ ଯେ ଆପଣ ଆସନ୍ତାକାଲି କାର୍ଯ୍ୟକ୍ରମରେ ଉପସ୍ଥିତ ରହିବେ କି ନାହିଁ।"

After: "ଆରେ ସୁମିତ, କାଲି ପ୍ରୋଗ୍ରାମକୁ ଆସୁଛୁ ତ? କହିଦେବୁ।"

Gloss: The first reads like a formal notice: "Dear friend, kindly inform me whether you will be present at tomorrow's event." The rewrite is a text to a close friend: "Hey Sumit, you're coming to the event tomorrow, right? Let me know." Use the "ତୁ" forms only if that is how the user talks to Sumit.

## Help wanted

This file has not yet been reviewed by a native speaker. If you speak Odia, corrections are welcome. See CONTRIBUTING.md.
