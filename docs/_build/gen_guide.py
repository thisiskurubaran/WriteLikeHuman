"""Builds docs/guide.html, the "How do I..." guide.

The page reuses the styles, icons, theme script, nav, and footer of
docs/index.html. The tasks live in TASKS below: edit them here, then run
sync_site.py. Each task has an id (used as the link anchor), a group, a
title, an example prompt, 3 to 5 plain steps, and an optional note.
"""
import html

GROUPS = [
    ("everyday", "Everyday writing"),
    ("files", "Files"),
    ("voice", "Your voice"),
    ("business", "Small business"),
    ("languages", "Languages and access"),
    ("developers", "For developers"),
    ("code", "Claude Code"),
]

TASKS = [
    ("humanize-email", "everyday", "Make an email sound less robotic",
     "Make this email sound less robotic",
     ["Paste the email into a chat with Claude.",
      "Say what you want in your own words, like the example.",
      "Read the new version, then the short \"What I changed\" list under it.",
      "Want a different tone? Say \"a bit warmer\" or \"more formal\"."],
     "Names, dates, and amounts stay exactly as you wrote them."),
    ("before-send", "everyday", "Check a message before sending it",
     "Check this before I send it",
     ["Paste the message, plus the one you're replying to if there is one.",
      "Ask for a check before you send.",
      "You get a short list: a missing attachment, a weekday that doesn't match the date, an unanswered question, a leftover [name].",
      "Say \"fix these\" if you want them fixed."],
     None),
    ("tricky-reply", "everyday", "Reply to a tricky message",
     "Reply to my landlord about the deposit without sounding rude",
     ["Paste the message you got and say what you want to say back.",
      "You get one reply, calm and clear.",
      "If you want it firmer or softer, say so. You can also ask for exactly two versions to compare."],
     None),
    ("work-chat", "everyday", "Write a Slack, Teams, or Google Chat message",
     "Write a Slack message telling my team the release moves to Thursday",
     ["Say what you want to tell or ask, and who it's for: a channel, your lead, or a thread.",
      "Or paste your draft, plus the thread you're replying to.",
      "You get a short message with the point in the first line, ready to paste.",
      "Email habits like \"Hope you're doing well\" and \"Kind regards\" are left out. Ask for it more casual or more polite if you like."],
     "Names, @mentions, ticket numbers, and dates stay as you gave them. It won't add promises you didn't make."),
    ("read", "everyday", "Understand how a message sounds",
     "How does this message from my boss sound?",
     ["Paste the message you got.",
      "Ask how it sounds, like the example.",
      "You get a calm reading of the tone, based only on the words. It won't guess what the person secretly means.",
      "Say \"help me reply\" if you want a reply next."],
     None),
    ("negotiation", "everyday", "Ask for a better salary, price, or rent",
     "Help me ask for a higher salary, the offer is 9 lakh and I was hoping for 11",
     ["Give the offer, the number you want, and your real reasons.",
      "You get a short, polite message you can send or say.",
      "Ask for it firmer or softer if you like."],
     "It uses only the numbers and reasons you give. It won't invent other offers or achievements."),
    ("quick-options", "everyday", "Get quick choices when you're not sure what to ask",
     "help with this",
     ["Paste the text or attach the file, with a short message like the example, or none at all.",
      "You get 2 to 4 short numbered choices, like \"Write a reply\" or \"Check it before you send\". In Claude Code you can tap one.",
      "Reply with a number, or say what you want in your own words.",
      "Nothing changes until you pick."],
     "Clear requests, like \"make this friendlier\", skip the options and go straight to the work."),
    ("word-file", "files", "Fix a Word file, with the reasons in comments",
     "Humanize this Word file and explain each change in a comment",
     ["Attach the .docx file.",
      "Ask for the fix, like the example. Leave out the comment part if you don't need it.",
      "You get a new copy ending in -humanized. Fonts, tables, and lists stay the same.",
      "Each change has a short note in the margin saying why. Ask for tracked changes instead if you prefer."],
     "Your original file is never overwritten."),
    ("form", "files", "Fill in a form",
     "Fill this visa form with my details",
     ["Attach the fillable PDF or the Word form.",
      "Give your details in the chat, in any order.",
      "You get a filled copy, plus a list of anything it couldn't fill.",
      "Check every field and sign it yourself."],
     "It never guesses ID numbers, dates of birth, or addresses, and never ticks a declaration for you."),
    ("template", "files", "Fill a template",
     "Fill my company letterhead with this letter",
     ["Attach your Word or PowerPoint template.",
      "Paste or describe what should go in it.",
      "You get a filled copy with your template's look kept.",
      "Anything you didn't give stays as a clear [blank] to fill in."],
     None),
    ("slides", "files", "Make slides from notes",
     "Make 5 slides for my team meeting from these notes",
     ["Paste your notes, with any numbers you want to use.",
      "Say how many slides, or let Claude pick.",
      "You get a .pptx with short slide text and fuller speaker notes.",
      "Ask for changes slide by slide: \"shorter title on slide 3\"."],
     "It never adds figures, charts, or results you didn't give."),
    ("spreadsheet", "files", "Make a spreadsheet",
     "Put these expenses in a sheet with a notes column",
     ["Paste your list: items, amounts, dates.",
      "Say which columns you want.",
      "You get an .xlsx with your numbers exactly as given, and totals as formulas so they stay right."],
     None),
    ("google", "files", "Edit a Google Sheet or Slides deck",
     "Make the Remarks column in my Google Sheet sound natural",
     ["Connect Claude to your Google account (Settings, then Connectors), if you haven't already.",
      "Share the link to the Sheet or Slides deck in the chat.",
      "The text is fixed right there. Numbers, formulas, and layout are left alone.",
      "No connector? Download it as .xlsx or .pptx, attach it, and you get a new copy back."],
     None),
    ("long-document", "files", "Fix a long thesis, manual, or report",
     "Fix the wording in my 120 page thesis, keep the terms consistent",
     ["Attach the file. Word, PDF, or LaTeX (.tex) all work.",
      "Claude works through it section by section and keeps a list of names and terms so they stay the same.",
      "You get a new copy ending in -humanized, plus a short note of anything it wasn't sure about.",
      "For LaTeX, only the prose changes. Commands, maths, and citations stay exactly as they were."],
     None),
    ("voice", "voice", "Build my voice profile",
     "Make a quick voice profile from these 3 messages",
     ["For a quick start, paste 3 short messages you wrote yourself.",
      "You get a short profile: how long your sentences run, words you like, how you sign off.",
      "Save it as a note or file and attach it next time: \"use my voice profile\".",
      "Add more of your writing later to make it better, or keep a \"work me\" and a \"personal me\"."],
     "Only your own writing. It won't copy anyone else's voice."),
    ("style-guide", "voice", "Set up a team style guide",
     "Help me make a style guide for my bakery's messages",
     ["Ask for a style guide, or attach one you already have.",
      "Fill in the blanks: product names, words to use and avoid, how you sign off.",
      "Save it and attach it whenever you write for the team.",
      "Every message then follows it, and product names stay spelled exactly."],
     None),
    ("payment-reminder", "business", "Send a payment reminder",
     "Write a polite reminder for invoice 1043, Rs 18,500, due on 5 March",
     ["Give the invoice number, the amount, and the due date.",
      "Say whether it's the first reminder or a follow-up.",
      "You get a short, polite message for email or WhatsApp, firmer for later reminders.",
      "Amounts, dates, and invoice numbers stay exactly as you gave them."],
     None),
    ("support-reply", "business", "Reply to a customer",
     "Reply to this customer whose order arrived late",
     ["Paste the customer's message and the facts: order number, what went wrong, what you'll do.",
      "You get a reply that says sorry once, explains the fix, and says what happens next.",
      "It only promises what you said you'll do."],
     None),
    ("out-of-office", "business", "Set an out-of-office reply",
     "Write an out-of-office reply, I'm away 10 to 14 March, contact Ravi",
     ["Give the dates and who to contact instead.",
      "Say where it's for: email, WhatsApp Business away message, or both.",
      "You get a short reply you can paste in. Ask for an email signature too if you need one."],
     None),
    ("personalised", "business", "Send personal messages to a list of people",
     "Make one Diwali message per row in this sheet, using each person's name",
     ["Attach a spreadsheet with names, and any detail you want used, like an order or a city.",
      "Write or describe the message once.",
      "You get a file with one draft per row. Nothing is sent.",
      "Copy each draft into WhatsApp or email yourself."],
     "Only for people you already know, like customers or family. It won't write bulk marketing or spam."),
    ("script", "languages", "Write in Hindi or Tamil script",
     "Write this in Hindi script: kal subah 10 baje milte hain",
     ["Paste your Hinglish or Tanglish written in English letters.",
      "Ask for it in Hindi (Devanagari) or Tamil script.",
      "You get the same words in that script. Nothing is translated.",
      "Check names and English words, since some can be spelled more than one way."],
     "Works for Hindi and Tamil, plus Telugu, Kannada, Malayalam, Bengali, Marathi, and Gujarati."),
    ("alt-text", "languages", "Write alt text for images",
     "Write alt text for these 3 product photos",
     ["Attach the images.",
      "Say where they'll go: an Instagram post, a website, or slides.",
      "You get a short, plain description for each one.",
      "It describes only what's visible and never guesses who people are."],
     None),
    ("easy-read", "languages", "Make something Easy Read or dyslexia friendly",
     "Make this Word file dyslexia friendly",
     ["Attach the file or paste the text.",
      "Ask for Easy Read for short, simple lines with picture suggestions, or dyslexia friendly for a clearer layout.",
      "Dyslexia friendly keeps every word and changes only the font, spacing, and alignment. You get a new copy ending in -readable.",
      "Easy Read rewrites in simpler words, so check that nothing important was left out."],
     None),
    ("readme", "developers", "Write or fix a README",
     "Write a README for this project",
     ["In Claude Code, ask with the project open. Elsewhere, paste your README and say what the project does.",
      "You get a short opening that says what it is and who it's for, then install, quick start, and usage.",
      "Install steps use the real commands from your repo. If one is missing, you get a clear TODO instead of a guess.",
      "Emoji on every heading, walls of badges, and sales words are cut."],
     "Commands, code blocks, paths, and version numbers stay exactly as written. It never adds a feature the project doesn't have."),
    ("commit-message", "developers", "Write a commit message or PR description",
     "Write a commit message for my staged changes",
     ["In Claude Code, just ask: it reads your staged changes. Elsewhere, paste the diff or a list of what changed.",
      "You get a summary line under about 72 characters, plus a line or two on why if it helps.",
      "For a PR, you get what changed, why, and how to check it, following your repo's PR template if there is one.",
      "It follows your repo's style, like fix(login): or a ticket prefix, and doesn't commit unless you ask."],
     "It describes only what's in the diff. It won't say tests were added or passed unless they were."),
    ("architecture", "developers", "Explain the architecture or folder structure",
     "Explain our folder structure for a new teammate",
     ["In Claude Code, ask with the project open. Elsewhere, paste the folder tree (tree -L 2) or a screenshot of it.",
      "For a folder structure, you get the tree plus one line per folder: what lives there and when you'd edit it.",
      "For an architecture doc, you get the main parts, what each one talks to, and one real request followed from start to finish.",
      "For a decision record (ADR), give the choice and your reasons. You get short Context, Decision, and Consequences sections."],
     "It uses the real names of folders and services and never invents parts your code doesn't have. It never moves or creates code files."),
    ("code-comments", "developers", "Clean up code comments without touching the code",
     "Clean up the comments in billing.py, leave the code alone",
     ["Attach or paste the file, or ask in Claude Code with the project open.",
      "Only comments and docstrings are rewritten, mostly to explain why the code does something.",
      "A script puts each comment back in its place and refuses to save if any code would change.",
      "You get a new copy ending in -humanized (in a git repo, the file is edited in place), plus a list of comments worth deleting."],
     "Licence headers, tool directives like noqa, commented-out code, TODOs, and @param names are left as they are."),
    ("error-messages", "developers", "Write clearer error messages and app text",
     "Make these error messages friendlier",
     ["Paste the messages, button labels, or translation file (like en.json), and say what the code does if it isn't clear.",
      "Each error message says what happened and what the person can do now.",
      "Buttons say what they do, and empty screens say what to do next.",
      "In a translation file, only the English values change. Keys and placeholders like {name} stay exactly."],
     "API docs work too: paste the endpoint and you get a plain description, a parameter table, and an example with your real field names."),
    ("claude-code", "code", "Use it in Claude Code",
     "/plugin marketplace add thisiskurubaran/WriteLikeHuman",
     ["In Claude Code, run the command above.",
      "Then run /plugin install write-like-human@writelikehuman.",
      "Ask in your own words as usual. To update later, run /plugin marketplace update writelikehuman."],
     None),
]

ARROW = '<svg class="icon" aria-hidden="true"><use href="#i-arrow"/></svg>'

EXTRA_CSS = '''
/* ---------- Guide ---------- */
.g-hero { padding: 40px 0 8px; }
@media (min-width: 640px) { .g-hero { padding: 56px 0 12px; } }
.g-hero h1 { font-size: clamp(2.2rem, 1.4rem + 4vw, 3.8rem); }
.g-hero .lede { margin-bottom: 0; }
.g-layout { display: grid; grid-template-columns: minmax(0, 1fr); gap: 24px; padding-top: 28px; }
@media (min-width: 1024px) { .g-layout { grid-template-columns: 250px minmax(0, 1fr); gap: 40px; align-items: start; } }
.g-toc { display: none; }
@media (min-width: 1024px) { .g-toc { display: block; position: sticky; top: 100px; max-height: calc(100vh - 120px); overflow-y: auto; } .g-jump { display: none; } }
.g-toc h2 { font: 600 12.5px var(--mono); letter-spacing: .08em; text-transform: uppercase; color: var(--muted); margin: 0 0 10px; }
.g-toc h3 { font-size: 13px; color: var(--muted); margin: 14px 0 4px; font-weight: 600; }
.g-toc ul, .g-jump ul { list-style: none; margin: 0; padding: 0; }
.g-toc a { display: block; padding: 6px 10px; border-radius: 10px; font-size: 14px; color: var(--ink-2); text-decoration: none; }
.g-toc a:hover { background: var(--panel-2); color: var(--ink); }
.g-toc a[aria-current="true"] { background: var(--accent-soft); color: var(--accent); font-weight: 600; }
.g-jump { margin-bottom: 28px; border: 1px solid var(--line); border-radius: var(--r-lg); background: var(--panel); }
.g-jump summary { list-style: none; cursor: pointer; display: flex; align-items: center; justify-content: space-between; gap: 12px; min-height: 52px; padding: 0 18px; font-weight: 600; }
.g-jump summary::-webkit-details-marker { display: none; }
.g-jump summary .icon { transition: rotate .2s; rotate: 90deg; }
.g-jump[open] summary .icon { rotate: 270deg; }
.g-jump ul { padding: 0 8px 10px; display: grid; grid-template-columns: minmax(0, 1fr); }
.g-jump a { display: flex; align-items: center; min-height: 44px; padding: 0 10px; border-radius: 10px; color: var(--ink-2); text-decoration: none; font-size: 15px; }
.g-jump a:hover { background: var(--panel-2); }
.g-group { margin-bottom: 32px; }
.g-group > h2 { font-size: clamp(1.4rem, 1.1rem + 1.2vw, 1.9rem); margin: 0 0 14px; }
.g-tasks { display: grid; grid-template-columns: minmax(0, 1fr); gap: 14px; }
@media (min-width: 760px) and (max-width: 1023px) { .g-tasks { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (min-width: 1280px) { .g-tasks { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
.task { scroll-margin-top: 100px; background: var(--panel); border: 1px solid var(--line); border-radius: var(--r-lg); padding: var(--tile-pad); min-width: 0; box-shadow: var(--shadow-sm); }
.task h3 { font-size: 1.1rem; letter-spacing: -0.015em; margin: 0 0 12px; }
.task .say { display: block; margin: 0 0 14px; font-size: 14.5px; color: var(--ink-2); background: var(--panel-2); border: 1px solid var(--line); border-radius: 12px; padding: 10px 12px; overflow-wrap: anywhere; }
.task .say b { display: block; font: 600 11.5px var(--mono); letter-spacing: .06em; text-transform: uppercase; color: var(--muted); margin-bottom: 3px; }
.task ol { margin: 0; padding: 0; list-style: none; counter-reset: step; display: grid; gap: 8px; }
.task li { counter-increment: step; display: grid; grid-template-columns: 26px minmax(0, 1fr); gap: 10px; font-size: 14.5px; color: var(--ink-2); }
.task li::before { content: counter(step); width: 26px; height: 26px; border-radius: 8px; background: var(--ink); color: var(--bg); display: grid; place-items: center; font-size: 12.5px; font-weight: 700; }
.task .note { margin: 14px 0 0; padding-top: 12px; border-top: 1px dashed var(--line); font-size: 13.5px; color: var(--muted); }
.g-cta { margin-top: 8px; }
'''


def esc(text):
    return html.escape(text, quote=False)


EN_UI = {
    "title": "Guide | WriteLikeHuman",
    "desc": "How to use WriteLikeHuman: fix an email, fill a form, make slides, build your voice profile, payment reminders, and more, in short steps.",
    "eyebrow": "Guide", "h1": "How do I...",
    "lede": "Short steps for the things people ask WriteLikeHuman most. Every example is something you can type, in your own words, in Claude on the web, desktop, or phone.",
    "toc": "On this page", "jump": "Jump to a task", "say": "Say something like", "run": "Run",
    "cta_h": "Not installed yet?", "cta_p": "It takes two minutes: download the zip, then upload it in Claude.",
    "cta_dl": "Download the skill", "cta_how": "How to install", "note": None,
    "home": "Home", "files": "Files", "features": "Features", "examples": "Examples", "guide": "Guide",
    "install": "Install", "download": "Download", "top": "Top",
    "foot_note": "Free and open source under the MIT license.",
    "contribute": "Contribute", "feedback": "Share feedback", "privacy": "Privacy",
    "foot_small": "An independent project. Claude is made by Anthropic. All names and numbers in this guide are made up.",
    "skip": "Skip to content", "lang": "Language", "theme": "Switch theme", "menu": "Open menu",
}

# Where links point from each version of the guide.
PATHS = {
    "en": {"home": "./", "examples": "examples.html", "privacy": "privacy.html",
           "en": "guide.html", "hi": "hi/guide.html", "ta": "ta/guide.html", "url": "guide.html"},
    "hi": {"home": "./", "examples": "../examples.html", "privacy": "../privacy.html",
           "en": "../guide.html", "hi": "guide.html", "ta": "../ta/guide.html", "url": "hi/guide.html"},
    "ta": {"home": "./", "examples": "../examples.html", "privacy": "../privacy.html",
           "en": "../guide.html", "hi": "../hi/guide.html", "ta": "guide.html", "url": "ta/guide.html"},
}

TR_CSS = """
/* ---------- Translated page ---------- */
.tr-note { margin: 14px 0 0; padding: 10px 14px; border: 1px dashed var(--line-strong); border-radius: 14px; background: var(--panel); font-size: 13.5px; color: var(--muted); }
.tr-note a { color: var(--accent); }
"""

THEME_LABEL = {
    "hi": "dark ? 'Light theme पर जाएँ' : 'Dark theme पर जाएँ'",
    "ta": "dark ? 'Light theme-க்கு மாறு' : 'Dark theme-க்கு மாறு'",
}

GUIDE_JS = """  /* Guide: close the jump list after a pick, and mark the task in view */
  var jump = document.querySelector('.g-jump');
  if (jump) jump.addEventListener('click', function (e) { if (e.target.closest('a')) jump.open = false; });
  var links = {};
  document.querySelectorAll('.g-toc a').forEach(function (a) { links[a.getAttribute('href').slice(1)] = a; });
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        Object.keys(links).forEach(function (k) { links[k].removeAttribute('aria-current'); });
        var a = links[en.target.id]; if (a) a.setAttribute('aria-current', 'true');
      });
    }, { rootMargin: '-30% 0px -60% 0px' });
    document.querySelectorAll('.task').forEach(function (t) { io.observe(t); });
  }
})();
</script>"""

CARD = """        <article class="task" id="{id}" aria-labelledby="{id}-h">
          <h3 id="{id}-h">{title}</h3>
          <p class="say"><b>{label}</b>{prompt}</p>
          <ol>{steps}</ol>
          {note}
        </article>"""

GROUP = """      <section class="g-group" aria-labelledby="g-{id}" style="padding-top:0">
        <h2 id="g-{id}">{name}</h2>
        <div class="g-tasks">
{cards}
        </div>
      </section>"""


def build(idx, lang="en"):
    """Return the guide page HTML for lang ('en', 'hi', or 'ta'), built on top of the landing page."""
    if lang == "en":
        ui, groups, text = EN_UI, dict(GROUPS), esc
        tasks = {t[0]: t[2:] for t in TASKS}
    else:
        import gen_guide_i18n as i18n
        ui, groups, text = i18n.UI[lang], i18n.GROUPS[lang], (lambda s: s)
        tasks = i18n.TASKS[lang]
        missing = [t[0] for t in TASKS if t[0] not in tasks]
        if missing:
            raise KeyError("gen_guide_i18n.py has no %s text for: %s" % (lang, ", ".join(missing)))
    P = PATHS[lang]
    h = P["home"]

    head_top = idx[:idx.index('<script>')]
    theme_script = idx[idx.index('<script>'):idx.index('</script>') + 9]
    css = idx[idx.index('<style>') + 7:idx.index('</style>')]
    sprite = idx[idx.index('<!-- Reused icons -->'):idx.index('</svg>\n\n<nav') + 6]
    script_all = idx[idx.rindex('<script>'):idx.rindex('</script>') + 9]

    head = head_top.replace('<html lang="en">', '<html lang="%s">' % lang, 1)
    head = head.replace('<title>WriteLikeHuman</title>', '<title>%s</title>' % ui["title"], 1)
    head = head.replace(
        'content="A free Claude skill that makes everyday writing sound like a person wrote it. Emails, WhatsApp replies, letters, resumes, posts, and the files you already use."',
        'content="%s"' % ui["desc"], 1)
    head = head.replace('<meta property="og:title" content="WriteLikeHuman">',
                        '<meta property="og:title" content="%s">' % ui["title"], 1)
    head = head.replace('<meta property="og:url" content="https://thisiskurubaran.github.io/WriteLikeHuman/">',
                        '<meta property="og:url" content="https://thisiskurubaran.github.io/WriteLikeHuman/%s">' % P["url"], 1)

    def langs(extra_class=""):
        cur = {l: (' aria-current="page"' if l == lang else '') for l in ("en", "hi", "ta")}
        return ('<div class="lang-switch%s" role="group" aria-label="%s">'
                '<a href="%s" lang="en"%s>English</a><a href="%s" lang="hi"%s>हिंदी</a>'
                '<a href="%s" lang="ta"%s>தமிழ்</a></div>'
                % (extra_class, ui["lang"], P["en"], cur["en"], P["hi"], cur["hi"], P["ta"], cur["ta"]))

    arrow = ' ' + ARROW
    nav = "\n".join([
        '<nav class="topnav" aria-label="Main">',
        '  <div class="wrap bar">',
        '    <a class="brand" href="%s" aria-label="WriteLikeHuman home">' % h,
        '      <svg class="logo" aria-hidden="true" focusable="false"><use href="#logo"/></svg>',
        '      WriteLikeHuman',
        '    </a>',
        '    <div class="links">',
        '      <a href="%s#files">%s</a>' % (h, ui["files"]),
        '      <a href="%s#features">%s</a>' % (h, ui["features"]),
        '      <a href="%s">%s</a>' % (P["examples"], ui["examples"]),
        '      <a href="guide.html" aria-current="page">%s</a>' % ui["guide"],
        '      <a href="%s#install">%s</a>' % (h, ui["install"]),
        '      <a href="https://github.com/thisiskurubaran/WriteLikeHuman">GitHub</a>',
        '    </div>',
        '    <div class="nav-end">',
        '      <button class="icon-btn theme-btn" id="theme-btn" type="button" aria-label="%s">' % ui["theme"],
        '        <svg class="icon moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/></svg>',
        '        <svg class="icon sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
        '      </button>',
        '      <button class="icon-btn menu-btn" id="menu-btn" type="button" popovertarget="menu" aria-label="%s" aria-controls="menu">' % ui["menu"],
        '        <svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
        '      </button>',
        '      <a class="nav-cta" href="https://github.com/thisiskurubaran/WriteLikeHuman/releases/latest">%s</a>' % ui["download"],
        '    </div>',
        '  </div>',
        '</nav>',
        '',
        '<div class="menu" id="menu" popover>',
        '  <a href="%s">%s%s</a>' % (h, ui["home"], arrow),
        '  <a href="%s#files">%s%s</a>' % (h, ui["files"], arrow),
        '  <a href="%s#features">%s%s</a>' % (h, ui["features"], arrow),
        '  <a href="%s">%s%s</a>' % (P["examples"], ui["examples"], arrow),
        '  <a href="%s#install">%s%s</a>' % (h, ui["install"], arrow),
        '  <a href="https://github.com/thisiskurubaran/WriteLikeHuman">GitHub%s</a>' % arrow,
        '  <a href="https://github.com/thisiskurubaran/WriteLikeHuman/releases/latest">%s <svg class="icon" aria-hidden="true"><use href="#i-down"/></svg></a>' % ui["download"],
        '  ' + langs(),
        '</div>',
        '',
    ])

    footer = "\n".join([
        '<footer>',
        '  <div class="wrap foot">',
        '    <div class="foot-top">',
        '      <a class="brand" href="#top" aria-label="WriteLikeHuman, back to top"><svg class="logo" aria-hidden="true" focusable="false"><use href="#logo"/></svg>WriteLikeHuman</a>',
        '      <a class="to-top" href="#top">%s <svg class="icon" aria-hidden="true"><use href="#i-down"/></svg></a>' % ui["top"],
        '    </div>',
        '    <p class="foot-note">%s</p>' % ui["foot_note"],
        '    <nav class="flinks" aria-label="Footer">',
        '      <a href="https://github.com/thisiskurubaran/WriteLikeHuman">GitHub</a>',
        '      <a href="https://github.com/thisiskurubaran/WriteLikeHuman/blob/main/CHANGELOG.md">Changelog</a>',
        '      <a href="https://github.com/thisiskurubaran/WriteLikeHuman/blob/main/CONTRIBUTING.md">%s</a>' % ui["contribute"],
        '      <a href="%s">%s</a>' % (h, ui["home"]),
        '      <a href="%s">%s</a>' % (P["examples"], ui["examples"]),
        '      <a href="https://github.com/thisiskurubaran/WriteLikeHuman/issues/new?template=feedback.md">%s</a>' % ui["feedback"],
        '      <a href="%s">%s</a>' % (P["privacy"], ui["privacy"]),
        '    </nav>',
        '    ' + langs(" foot-langs"),
        '    <p class="foot-small">%s</p>' % ui["foot_small"],
        '  </div>',
        '</footer>',
        '',
    ])

    # Table of contents (desktop) and jump list (phones)
    toc_parts, jump_items, groups_html = [], [], []
    for gid, _gname in GROUPS:
        ids = [t[0] for t in TASKS if t[1] == gid]
        if not ids:
            continue
        gname = text(groups[gid])
        toc_parts.append('<h3>%s</h3><ul>%s</ul>' % (gname, ''.join(
            '<li><a href="#%s">%s</a></li>' % (tid, text(tasks[tid][0])) for tid in ids)))
        jump_items.extend('<li><a href="#%s">%s</a></li>' % (tid, text(tasks[tid][0])) for tid in ids)
        cards = []
        for tid in ids:
            title, prompt, steps, note = tasks[tid]
            cards.append(CARD.format(
                id=tid, title=text(title), prompt=text(prompt),
                label=ui["run"] if tid == 'claude-code' else ui["say"],
                steps=''.join('<li><span>%s</span></li>' % text(st) for st in steps),
                note='<p class="note">%s</p>' % text(note) if note else ''))
        groups_html.append(GROUP.format(id=gid, name=gname, cards='\n'.join(cards)))

    script = script_all[:script_all.index('  /* Before and after demo */')] + GUIDE_JS
    if lang != "en":
        script = script.replace("dark ? 'Switch to light theme' : 'Switch to dark theme'", THEME_LABEL[lang])

    note = ('<div class="wrap"><p class="tr-note" role="note">%s</p></div>\n\n' % ui["note"]) if ui.get("note") else ''
    extra = EXTRA_CSS + (TR_CSS if lang != "en" else '')

    body = "\n".join([
        '<main id="main">',
        '<header class="g-hero" id="top">',
        '  <div class="wrap">',
        '    <p class="eyebrow">%s</p>' % ui["eyebrow"],
        '    <h1>%s</h1>' % ui["h1"],
        '    <p class="lede">%s</p>' % ui["lede"],
        '  </div>',
        '</header>',
        '',
        '<div class="wrap g-layout">',
        '  <aside class="g-toc" aria-label="%s">' % ui["toc"],
        '    <h2>%s</h2>' % ui["toc"],
        '    ' + ''.join(toc_parts),
        '  </aside>',
        '  <div>',
        '    <details class="g-jump">',
        '      <summary>%s%s</summary>' % (ui["jump"], arrow),
        '      <ul>%s</ul>' % ''.join(jump_items),
        '    </details>',
        '\n'.join(groups_html),
        '    <div class="cta-band g-cta">',
        '      <svg class="squiggle sq1" viewBox="0 0 400 60" aria-hidden="true"><path d="M10 40c30-30 50-30 70 0s40 30 70 0 50-30 70 0 40 30 70 0 50-30 70 0"/></svg>',
        '      <svg class="squiggle sq2" viewBox="0 0 400 60" aria-hidden="true"><path d="M10 40c30-30 50-30 70 0s40 30 70 0 50-30 70 0 40 30 70 0 50-30 70 0"/></svg>',
        '      <h2>%s</h2>' % ui["cta_h"],
        '      <p>%s</p>' % ui["cta_p"],
        '      <div class="actions">',
        '        <a class="btn btn-primary" href="https://github.com/thisiskurubaran/WriteLikeHuman/releases/latest"><svg class="icon" aria-hidden="true"><use href="#i-down"/></svg>%s</a>' % ui["cta_dl"],
        '        <a class="btn btn-secondary" href="%s#install">%s</a>' % (h, ui["cta_how"]),
        '      </div>',
        '    </div>',
        '  </div>',
        '</div>',
        '</main>',
        '',
    ])

    return (head + theme_script + '\n<style>' + css + extra + '</style>\n</head>\n<body>\n'
            '<a class="skip" href="#main">' + ui["skip"] + '</a>\n\n' + sprite + '\n\n' + nav + '\n' + note
            + body + '\n' + footer + '\n' + script + '\n</body>\n</html>\n')
