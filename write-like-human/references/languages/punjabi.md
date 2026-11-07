# Punjabi

Rewrite Punjabi so it sounds like a person wrote it, in the script and style the user already uses.

## When this applies

- The text is in Punjabi, in Gurmukhi (ਪੰਜਾਬੀ), Shahmukhi (پنجابی), or Roman script.
- The user asks for a translation into Punjabi (also load `translate-humanize.md`). Ask which script they want if it is not clear. In India most readers use Gurmukhi. In Pakistan most use Shahmukhi.
- For Punjabi mixed with English or Hindi, load `mixed-language.md` as well.

## What stays the same

- Language and script. Gurmukhi stays Gurmukhi, Shahmukhi stays Shahmukhi, Roman stays Roman. Never switch scripts or translate unless asked.
- Shahmukhi is written right to left, like Urdu. Keep it that way in files (see `urdu.md` for notes on right to left text in Word files).
- Names, numbers, dates, amounts, places, and quotes.
- The register. "ਤੁਸੀਂ" stays "ਤੁਸੀਂ". "ਤੂੰ" stays "ਤੂੰ".
- The user's dialect. Majhi, Doabi, Malwai, and Pakistani Punjabi differ. Keep their words.

## AI tells in Punjabi

- Hindi in Gurmukhi letters. Machine translation often writes Hindi grammar and words in Gurmukhi script: "ਮੈਂ ਜਾ ਰਿਹਾ ਹੂੰ" instead of "ਮੈਂ ਜਾ ਰਿਹਾ ਹਾਂ".
- Over-formal words in a casual message: "ਸੂਚਿਤ ਕਰੋ", "ਹਾਜ਼ਰ ਹੋਵੋਗੇ", "ਕਿਰਪਾ ਕਰਕੇ" in every line.
- Literal English calques like "ਮੈਂ ਆਸ ਕਰਦਾ ਹਾਂ ਕਿ ਇਹ ਸੁਨੇਹਾ ਤੁਹਾਨੂੰ ਚੰਗੀ ਸਿਹਤ ਵਿੱਚ ਮਿਲੇ".
- Mixed up scripts in one message, or Urdu letters in Gurmukhi text.
- Stiff word order copied from English.

## Steps

1. Note the script, dialect, and register, and keep all three.
2. Replace Hindi slips with Punjabi forms.
3. Swap textbook words for everyday ones where the context is casual.
4. Remove calques.
5. Check names, numbers, and dates are unchanged.

## Output

The rewritten Punjabi text in the same script, then a short **What I changed** list in the language the user is using with you.

## Example

Before: "ਪਿਆਰੇ ਦੋਸਤ, ਕਿਰਪਾ ਕਰਕੇ ਮੈਨੂੰ ਸੂਚਿਤ ਕਰੋ ਕਿ ਤੁਸੀਂ ਕੱਲ੍ਹ ਦੇ ਸਮਾਗਮ ਵਿੱਚ ਹਾਜ਼ਰ ਹੋਵੋਗੇ ਜਾਂ ਨਹੀਂ।"

After: "ਓਏ ਗੁਰੀ, ਕੱਲ੍ਹ ਪ੍ਰੋਗਰਾਮ 'ਤੇ ਆ ਰਿਹਾ ਹੈਂ ਨਾ? ਦੱਸ ਦੇਈਂ।"

Gloss: The first reads like a formal notice: "Dear friend, kindly inform me whether you will attend tomorrow's function." The rewrite is a text to a friend: "Hey Guri, you're coming to the event tomorrow, right? Let me know."

## Help wanted

This file has not yet been reviewed by a native speaker. If you speak Punjabi, corrections are welcome, in either script. See CONTRIBUTING.md.
