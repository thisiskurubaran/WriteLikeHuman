"""Builds docs/privacy.html, a plain-words privacy page.

It reuses the page frame of the guide (head, nav, footer, theme script)
so every page looks and behaves the same, and swaps in the content
below. Edit SECTIONS here, then run sync_site.py.
"""
import gen_guide

SECTIONS = [
    ("your-text", "What happens to your text", [
        "Your text and files are used only inside your own chat with Claude. That's where WriteLikeHuman runs.",
        "WriteLikeHuman is a set of instructions and small helper scripts that Claude reads. It has no server, no account, and no database of its own.",
        "It doesn't store your writing, and it doesn't send it anywhere. There's nothing to sign up for and nothing that tracks you.",
    ]),
    ("files", "Files you attach", [
        "When you attach a Word, Excel, PowerPoint, or PDF file, the helper scripts run inside Claude's own sandbox, the same place Claude works on any file you give it.",
        "They read your file and write one new file next to it, ending in <b>-humanized</b> (or <b>-filled</b> for forms and templates). Your original is never changed.",
        "The scripts don't connect to the internet, and they don't keep a copy of anything after the chat.",
    ]),
    ("anthropic", "What Anthropic's policies cover", [
        "Claude is made by Anthropic, so how your chats are stored and used is covered by Anthropic's own policies and your account settings, not by WriteLikeHuman.",
        'Read them here: <a href="https://www.anthropic.com/legal/privacy">Anthropic privacy policy</a>. Your chat history and data controls are in Claude under <b>Settings</b>.',
    ]),
    ("connectors", "Google and email connectors", [
        "Some features, like editing a Google Doc or a Gmail draft in place, only work if you connect Claude to that account yourself.",
        "WriteLikeHuman only works on the file or draft you point it to, works on a copy unless you say otherwise, and never sends an email or message for you.",
    ]),
    ("tips", "A few tips", [
        "When you report a problem or share an example, use made-up text instead of real names, numbers, or documents.",
        "Build voice profiles only from your own writing. Don't paste other people's messages or personal details into a profile.",
        "Personalised messages from a spreadsheet are only for people you already know, and they're saved as drafts for you to send yourself.",
    ]),
    ("report", "Report a privacy problem", [
        'If you think WriteLikeHuman could leak, store, or send text it shouldn\'t, please tell us privately. The steps are in the <a href="https://github.com/thisiskurubaran/WriteLikeHuman/blob/main/SECURITY.md">security policy</a>. Please don\'t open a public issue for it.',
    ]),
]

CSS = """
/* ---------- Privacy ---------- */
.p-hero { padding: 40px 0 8px; }
@media (min-width: 640px) { .p-hero { padding: 56px 0 12px; } }
.p-hero h1 { font-size: clamp(2.2rem, 1.4rem + 4vw, 3.8rem); }
.p-body { max-width: 760px; padding-top: 20px; }
.p-card { background: var(--panel); border: 1px solid var(--line); border-radius: var(--r-lg); padding: var(--tile-pad); margin-bottom: 14px; box-shadow: var(--shadow-sm); }
.p-card h2 { font-size: clamp(1.2rem, 1rem + .8vw, 1.5rem); margin: 0 0 10px; }
.p-card p { margin: 0 0 10px; color: var(--ink-2); }
.p-card p:last-child { margin-bottom: 0; }
.p-card a { color: var(--accent); }
.p-updated { color: var(--muted); font-size: 14px; margin: 18px 0 0; }
"""


def build(idx):
    page = gen_guide.build(idx, "en", current=None)
    page = page.replace('<title>Guide | WriteLikeHuman</title>', '<title>Privacy | WriteLikeHuman</title>', 1)
    page = page.replace('<meta property="og:title" content="Guide | WriteLikeHuman">',
                        '<meta property="og:title" content="Privacy | WriteLikeHuman">', 1)
    page = page.replace('content="%s"' % gen_guide.EN_UI["desc"],
                        'content="What happens to your text with WriteLikeHuman: it stays in your own chat with Claude. Nothing is stored or sent."', 1)
    page = page.replace('WriteLikeHuman/guide.html">', 'WriteLikeHuman/privacy.html">', 1)
    page = page.replace('<a href="privacy.html">Privacy</a>', '<a href="privacy.html" aria-current="page">Privacy</a>', 1)
    page = page.replace('<a href="guide.html" lang="en" aria-current="page">English</a>', '<a href="./" lang="en">English</a>', 1)
    page = page.replace('<a href="hi/guide.html" lang="hi">', '<a href="hi/" lang="hi">', 1)
    page = page.replace('<a href="ta/guide.html" lang="ta">', '<a href="ta/" lang="ta">', 1)
    page = page.replace('<a href="guide.html" lang="en" aria-current="page">English</a>', '<a href="./" lang="en">English</a>', 1)
    page = page.replace('<a href="hi/guide.html" lang="hi">', '<a href="hi/" lang="hi">', 1)
    page = page.replace('<a href="ta/guide.html" lang="ta">', '<a href="ta/" lang="ta">', 1)
    page = page.replace('All names and numbers in this guide are made up.', 'This page describes the skill as published on GitHub.', 1)
    page = page.replace('</style>', CSS + '</style>', 1)

    cards = []
    for sid, title, paras in SECTIONS:
        cards.append('    <section class="p-card" id="%s" aria-labelledby="%s-h">\n      <h2 id="%s-h">%s</h2>\n%s\n    </section>'
                     % (sid, sid, sid, title, "\n".join("      <p>%s</p>" % p for p in paras)))
    main = "\n".join([
        '<main id="main">',
        '<header class="p-hero" id="top">',
        '  <div class="wrap">',
        '    <p class="eyebrow">Privacy</p>',
        '    <h1>Your writing stays yours</h1>',
        '    <p class="lede">WriteLikeHuman runs inside your own chat with Claude. It has no server, stores nothing, and sends nothing. Here is what that means in plain words.</p>',
        '  </div>',
        '</header>',
        '',
        '<div class="wrap">',
        '  <div class="p-body">',
        "\n".join(cards),
        '    <p class="p-updated">Questions? <a href="https://github.com/thisiskurubaran/WriteLikeHuman/issues/new?template=feedback.md">Ask on GitHub</a>, using made-up text only.</p>',
        '  </div>',
        '</div>',
        '</main>',
    ])
    a = page.index('<main id="main">')
    b = page.index('</main>') + len('</main>')
    return page[:a] + main + page[b:]
