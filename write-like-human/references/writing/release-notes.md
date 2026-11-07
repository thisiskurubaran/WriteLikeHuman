# Release notes and app updates

Help small developers and makers write changelogs, GitHub release notes, and the "What's new" text for app stores (Google Play, the App Store) or a product update email.

Good release notes tell users what changed for them, in plain words. They are not marketing copy.

## When this applies

- "Write the What's new text for version 2.4."
- "Turn these commit messages into release notes."
- "Make this changelog readable for users."
- The user pastes notes full of hype ("Exciting new update!", "We've supercharged your experience").

## What stays the same

- Version numbers, build numbers, and dates exactly as given.
- Feature names, screen names, setting names, and button labels as they appear in the app.
- Issue or ticket numbers (#142, JIRA-881) and links, where the user includes them.
- What actually changed. Do not add features, fixes, or speed claims the user did not mention. "Faster" only if they said so, and numbers only if they gave them.

## Steps

1. Sort the changes into groups that make sense for the reader: New, Improved, Fixed. Add "Removed" or "Changed" if something users rely on is going away or behaving differently. Skip empty groups.
2. Write each item from the user's side: what they can now do, or what no longer goes wrong. "You can now export reports as PDF" beats "Implemented PDF export functionality".
3. Translate developer wording for app store text: "Fixed a crash when opening a photo from the gallery" rather than "Fixed NPE in GalleryActivity". Keep technical detail in developer changelogs if the audience is developers.
4. Put breaking changes or anything users must do first, clearly: "After updating, sign in again."
5. Keep app store text short. Stores have character limits (Google Play's "What's new" is about 500 characters, and limits change, so tell the user to check). Lead with the most noticeable change.
6. Remove hype: "exciting", "supercharged", "game-changing", "we're thrilled", rocket emoji. A simple thanks to users who reported bugs is fine.
7. Check every version number, name, and issue number against the original.

## Formats

App store "What's new":

```
- New: export any report as a PDF from the Share menu.
- Fixed: the app no longer closes when you open a photo from the gallery.
- Fixed: reminders now ring at the right time after a phone restart.
```

Developer changelog (Keep a Changelog style):

```
## [2.4.0] - 2025-09-12

### Added
- PDF export for reports (#142)

### Fixed
- Crash when opening a gallery photo on Android 14 (#151)
```

## Output

The notes in the format the user needs, ready to paste, then a short **What I changed** list. Add the approximate character count for app store text.

## Example

Before:

> 🚀 Version 3.1 is HERE! We're thrilled to unveil an exciting update that supercharges your experience! We've squashed pesky bugs and added amazing new features you'll love. Update now!

Commit notes the user gave: "added dark mode toggle in Settings > Display", "fix: sync failing on slow networks (#88)", "fix: typo on login screen".

After:

> Version 3.1
> - New: turn on dark mode in Settings > Display.
> - Fixed: syncing now works on slow connections.
> - Fixed: a typo on the login screen.

(About 120 characters.)

What I changed
- Replaced the announcement with what actually changed, taken from your commit notes.
- Kept "Settings > Display" exactly, so users can find it.
- Removed the rocket emoji and "supercharges".
