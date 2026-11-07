# Bengali

Rewrite Bengali so it sounds like a person wrote it, in the register the situation needs.

## When this applies

- The text is in Bengali, in Bengali script or in Roman script.
- The user asks for a translation into Bengali (also load `translate-humanize.md`).
- For Bengali mixed with English (Benglish), load `mixed-language.md` as well.

## What stays the same

- Language and script. Bengali stays Bengali. Never translate unless asked.
- Names, numbers, dates, amounts, and places.
- The register. "আপনি" (respectful), "তুমি" (familiar), and "তুই" (very close) stay as the user wrote them.
- Everyday English words people use in Bengali (phone, bus, office), unless the user avoids them.

## AI tells in Bengali

- Sadhu bhasha forms in modern text. Old literary verb forms like "করিতেছি", "যাইব" in a modern message. Modern writing uses chalit forms: "করছি", "যাব".
- Heavy Sanskrit-based words in casual text where everyday words fit.
- Literal English calques, such as word for word "I hope this finds you well".
- Wrong level of address for the reader.
- Repeated sentence shape.

Formal letters stay formal, but in modern chalit Bengali unless the user writes otherwise.

## Steps

1. Work out the reader and keep the user's form of address.
2. Replace old literary forms with modern ones.
3. Rewrite calques the way a Bengali speaker would say them.
4. Vary sentence length.
5. Check names, numbers, and dates are unchanged.

## Output

The rewritten Bengali text, then a short **What I changed** list in the language the user is using with you.

## Example

Before (to a friend): "বন্ধু, আমি আগামীকাল আসিব বলিয়া জানাইতেছি।"

After: "কাল আসছি রে।"

Gloss: The first uses old literary forms: "Friend, I am informing you that I shall come tomorrow." The second sounds like a real text: "Coming tomorrow."
