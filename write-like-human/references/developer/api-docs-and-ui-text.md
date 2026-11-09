# API docs, error messages, and UI text

Write the words developers ship: API reference text, error messages people can act on, and the small text in an app (buttons, labels, empty states, tooltips, confirmations).

## When this applies

- "Write docs for this endpoint", "describe these API parameters", "make the API docs clearer".
- "Make this error message friendlier", "rewrite our error messages", a list of error strings.
- Button labels, empty states ("No invoices yet"), onboarding text, tooltips, confirmation dialogs, notification text.
- A translation file (`en.json`, `messages.po`, `strings.xml`) where only the English values should change.

Load `lists/buzzwords.md` (the developer section) with this guide. In Claude Code inside a git repo, also load `developer/repo-files.md`.

## What stays the same

- Endpoint paths, methods, parameter names, field names, types, status codes, defaults, limits, and example values.
- Keys in translation files, placeholders (`{name}`, `%s`, `{{count}}`, `%1$d`), HTML tags, and markup. Change only the human words in the values.
- What the product actually does. Never document a parameter, error, or behaviour that isn't in the code or the user's notes.
- Length limits. A button stays short, and text that must fit a space stays within it.

## Steps

### API docs

1. One sentence per endpoint: what it does, in plain words. "Creates an invoice for a customer."
2. A parameter table: name, type, required or not, one plain line on what it means and any limits.
3. A short request and response example using the real field names.
4. List the errors the code returns, each with what causes it and what to do.

### Error messages

Each message answers two questions: what happened, and what the person can do now. "Couldn't save your changes. Check your connection and try again." Avoid blaming the user ("Invalid input"), codes with no explanation, "Oops!", and jokes when something went wrong.

### UI text

1. Buttons say what they do, with a verb: "Save draft", "Delete invoice", not "OK" or "Submit" when something clearer fits.
2. Empty states say what's missing and the next step: "No invoices yet. Create your first one."
3. Confirmations name the thing and the result: "Delete 'March report'? This can't be undone."
4. Use the same word for the same thing everywhere (don't mix "project" and "workspace").

## Output

The rewritten text, in the same format it came in (a table, JSON values, a list), then a short change summary. For a translation file, change only the values and say how many strings changed.

## Example

Before:

> Error 0x3F: An unexpected error has occurred. Please try again later or contact your system administrator.

What the code shows: the upload fails when the file is over 10 MB.

After:

> This file is too big to upload. Files can be up to 10 MB.

What I changed
- Said what went wrong and the limit, from the code.
- Removed the code number and "contact your administrator".
