# Security policy

WriteLikeHuman works on personal files: emails, resumes, letters, bank forms. If something could put the contents of those files at risk, we want to hear about it quickly and privately.

## Supported versions

Only the latest release gets fixes. If you are on an older zip, download the newest one from the [Releases page](https://github.com/thisiskurubaran/WriteLikeHuman/releases) and check whether the problem is still there.

## What to report

Please report anything like this privately:

- A way the skill could leak, store, or send the contents of a user's file or text anywhere.
- A script that writes outside its output file, deletes or overwrites the original, or reads files it was not given.
- A prompt or file that tricks the skill into saving personal data, sending it somewhere, or showing it to someone else.
- Real personal data that ended up in the repo by mistake (names, phone numbers, addresses, documents).

Problems with writing quality, like a rewrite that changed a date, are bugs, not security issues. Use the normal bug report for those.

## How to report

1. Go to the **Security** tab of this repository on GitHub.
2. Click **Report a vulnerability**.
3. Describe the problem and how to make it happen again.

Please do not open a public issue for security problems.

Never attach real personal files to a report. Recreate the problem with made up text, names, and numbers.

## What happens next

We aim to reply within 7 days. We will tell you whether we can reproduce it and when a fix is likely. Once it is fixed and released, we are happy to credit you in the changelog if you want.
