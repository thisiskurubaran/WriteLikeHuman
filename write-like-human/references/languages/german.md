# German

Rewrite German so it sounds like a person wrote it, for the right reader and region.

## When this applies

- The text is in German.
- The user asks for a translation into German (also load `translate-humanize.md`).

## What stays the same

- Language. German stays German. Never translate unless asked.
- Regional variety. Germany, Austria, and Switzerland differ. Keep the user's words ("Jänner" in Austria) and spelling (Swiss German writing uses "ss" instead of "ß").
- Names, numbers, dates, amounts, and places. Keep German number format (1.500,50 €) and dates (07.11.2026).
- The register. "Sie" stays "Sie". "Du" stays "du".

## AI tells in German

- Nominalstil. Piles of nouns ending in "-ung", "-heit", "-keit" where a verb works better. "Die Durchführung der Überprüfung erfolgt durch uns" instead of "Wir prüfen das."
- Overlong noun chains. Long compound nouns or chains of genitives that a person would break up.
- English calques. "Das macht Sinn" (common now, but "Das ergibt Sinn" or "Das ist sinnvoll" reads better in formal writing), "in 2026" (use "2026" or "im Jahr 2026"), "Ich erinnere das" (use "Ich erinnere mich daran"), "einmal mehr" overused.
- Wrong Sie or du. Many workplaces use "du", many do not. Keep what the user uses.
- Stock openers like "Ich hoffe, diese E-Mail findet Sie gut", which is a calque. Use "Ich hoffe, es geht Ihnen gut" or start with the point.
- English comma habits. German needs a comma before subordinate clauses ("dass", "weil", "wenn").

## Steps

1. Identify the reader, region, and register, and keep them.
2. Turn noun piles into verbs.
3. Break up long noun chains.
4. Replace calques and fix commas.
5. Check names, numbers, and dates are unchanged.

## Output

The rewritten German text, then a short **What I changed** list in the language the user is using with you. Describe the changes in plain words, without word-by-word English glosses of the rewritten text.

## Example

Before: "Sehr geehrter Herr Becker, ich hoffe, diese E-Mail findet Sie gut. Die Durchführung der Reparatur erfolgt nach Erhalt der Bestätigung Ihrerseits."

After: "Sehr geehrter Herr Becker, sobald Sie uns bestätigen, reparieren wir das Gerät."

Gloss: "Dear Mr Becker, as soon as you confirm, we will repair the device." The first used a translated English opener and a pile of nouns ("Durchführung", "Erhalt", "Bestätigung") where one verb does the job.

## Help wanted

This file has not yet been reviewed by a native speaker. If you speak German, corrections are welcome. See CONTRIBUTING.md.
