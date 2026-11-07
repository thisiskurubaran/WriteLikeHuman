# Spanish

Rewrite Spanish so it sounds like a person wrote it, for the right region and reader.

## When this applies

- The text is in Spanish.
- The user asks for a translation into Spanish (also load `translate-humanize.md`).

## What stays the same

- Language. Spanish stays Spanish. Never translate unless asked.
- Regional variety. Spain, Mexico, Argentina, and other countries differ. Keep the user's variety: "vosotros" in Spain, "ustedes" in Latin America, "vos" in Argentina and Uruguay if the user uses it. Keep local words ("coche" or "carro", "ordenador" or "computadora").
- Names, numbers, dates, amounts, and places. Keep the user's number format (1.500,50 or 1,500.50).
- The register. "Usted" stays "usted". "Tú" stays "tú".

## AI tells in Spanish

- Too many gerunds. "Le escribo informándole que..." or a chain of "-ando" and "-iendo" clauses. Use a plain verb: "Le escribo para avisarle que...".
- English calques. "Jugar un rol" (use "desempeñar un papel" or just "influir"), "aplicar a un trabajo" (use "solicitar" or "postularse" by region), "en orden a" (use "para"), "hacer sentido" (use "tener sentido").
- Wrong tú or usted for the reader. Usted with a close friend, or tú with a bank, unless that is normal in the user's region.
- Capitalized titles and days copied from English. In Spanish, months and days are lowercase: "lunes", "noviembre".
- Overuse of the passive with "ser", where Spanish prefers "se": "fue aprobado por el equipo" instead of "el equipo lo aprobó".
- Stock openers like "Espero que este correo le encuentre bien".
- English punctuation. Missing opening "¿" and "¡".

## Steps

1. Identify the region and the register, and keep both.
2. Cut gerund chains and passives.
3. Replace calques with natural Spanish.
4. Fix punctuation, capitalization, and accents.
5. Check names, numbers, and dates are unchanged.

## Output

The rewritten Spanish text, then a short **What I changed** list in the language the user is using with you.

## Example

Before: "Estimado Carlos, espero que este correo le encuentre bien. Le escribo informándole que la reunión ha sido movida al Lunes."

After: "Hola Carlos: te escribo para avisarte que pasamos la reunión al lunes."

Gloss: "Hi Carlos, just letting you know we moved the meeting to Monday." The first uses a translated English opener, a gerund, a passive, a capital on "Lunes", and "usted" with a colleague the user normally calls "tú". Only switch to "tú" if that matches how the user addresses Carlos.
