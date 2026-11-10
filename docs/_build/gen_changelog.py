"""Builds docs/changelog.html from CHANGELOG.md.

Like the privacy page, it reuses the guide's page frame (head, nav,
footer, theme script) and swaps in its own content. CHANGELOG.md is the
source: edit that, then run sync_site.py.

The Markdown it understands is what Keep a Changelog uses:
"## [1.2.3] - YYYY-MM-DD" version headings, "### Added" style
subheadings, "- " bullets (with indented "- " bullets one level deep),
and inline `code`, **bold**, and [links](url). All text is HTML-escaped.
"""
import html
import re

import gen_guide

REPO = "https://github.com/thisiskurubaran/WriteLikeHuman"
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]

VERSION_RE = re.compile(r"^##\s+\[?([^\]\s]+)\]?(?:\s+-\s+(\S+))?\s*$")
LINKDEF_RE = re.compile(r"^\[([^\]]+)\]:\s*(\S+)\s*$")
BULLET_RE = re.compile(r"^(\s*)[-*]\s+(.*)$")

CSS = """
/* ---------- Changelog ---------- */
.c-hero { padding: 40px 0 8px; }
@media (min-width: 640px) { .c-hero { padding: 56px 0 12px; } }
.c-hero h1 { font-size: clamp(2.2rem, 1.4rem + 4vw, 3.8rem); }
.c-body { max-width: 760px; padding-top: 20px; }
.c-jump { margin: 0 0 22px; }
.c-jump h2 { font: 600 12.5px var(--mono); letter-spacing: .08em; text-transform: uppercase; color: var(--muted); margin: 0 0 10px; }
.c-jump ul { list-style: none; margin: 0; padding: 0; display: flex; flex-wrap: wrap; gap: 8px; }
.c-jump a { display: inline-flex; align-items: center; min-height: 44px; padding: 0 14px; border: 1px solid var(--line); border-radius: 999px; background: var(--panel); color: var(--ink-2); font: 600 13.5px var(--mono); text-decoration: none; }
.c-jump a:hover { border-color: var(--line-strong); color: var(--ink); }
.c-ver { background: var(--panel); border: 1px solid var(--line); border-radius: var(--r-lg); padding: var(--tile-pad); margin-bottom: 14px; box-shadow: var(--shadow-sm); }
.c-ver-head { display: flex; flex-wrap: wrap; align-items: baseline; gap: 4px 14px; }
.c-ver h2 { font-size: clamp(1.4rem, 1.1rem + 1vw, 1.8rem); margin: 0; }
.c-date { margin: 0; color: var(--muted); font-size: 14.5px; }
.c-links { display: flex; flex-wrap: wrap; gap: 0 18px; margin: 4px 0 6px; }
.c-links a { display: inline-flex; align-items: center; min-height: 44px; color: var(--accent); font-weight: 600; font-size: 14.5px; }
.c-ver h3 { font: 600 12.5px var(--mono); letter-spacing: .08em; text-transform: uppercase; color: var(--accent); margin: 18px 0 8px; }
.c-ver ul { margin: 0; padding-left: 1.2em; display: grid; gap: 8px; }
.c-ver ul ul { margin-top: 8px; }
.c-ver li { color: var(--ink-2); font-size: 15px; overflow-wrap: anywhere; }
.c-ver li::marker { color: var(--muted); }
.c-ver p { margin: 0 0 10px; color: var(--ink-2); }
.c-ver li a, .c-ver p a { color: var(--accent); }
.c-ver code { font: 600 .9em var(--mono); background: var(--panel-2); border: 1px solid var(--line); border-radius: 6px; padding: 1px 5px; overflow-wrap: anywhere; }
.c-fold > summary { list-style: none; cursor: pointer; display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 8px 14px; min-height: 44px; border-radius: 12px; }
.c-fold > summary::-webkit-details-marker { display: none; }
.c-fold > summary .c-ver-head { min-width: 0; }
.c-toggle { display: inline-flex; align-items: center; gap: 6px; min-height: 34px; padding: 0 12px; border: 1px solid var(--line); border-radius: 999px; background: var(--panel-2); color: var(--ink-2); font-size: 13.5px; font-weight: 600; white-space: nowrap; }
.c-fold > summary:hover .c-toggle { border-color: var(--line-strong); color: var(--ink); }
.c-toggle .icon { width: 14px; height: 14px; transition: rotate .2s; }
.c-fold[open] .c-toggle .icon { rotate: 180deg; }
.c-fold:not([open]) .c-hide, .c-fold[open] .c-show { display: none; }
.c-fold-body { padding-top: 4px; }
.c-next { background: transparent; border-style: dashed; border-color: var(--line-strong); box-shadow: none; }
.c-next h2 { font-size: clamp(1.15rem, 1rem + .6vw, 1.4rem); }
.c-next-note { display: block; flex-basis: 100%; margin: 4px 0 0; color: var(--muted); font-size: 14px; font-weight: 400; }
.c-jump a.c-jump-next { border-style: dashed; background: transparent; font-family: var(--sans); }
.c-more { margin: 26px 0 0; padding: var(--tile-pad); border: 1px solid var(--line); border-radius: var(--r-lg); background: var(--panel); }
.c-more p { margin: 0 0 12px; font-weight: 600; color: var(--ink); }
.c-more-actions { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 18px; }
.c-all { display: inline-flex; align-items: center; min-height: 44px; color: var(--accent); font-weight: 600; font-size: 14.5px; }
@media (prefers-reduced-motion: reduce) { .c-toggle .icon { transition: none; } }
"""


def inline(text):
    """Escape text and turn `code`, **bold**, and [links](url) into HTML."""
    codes = []

    def keep_code(m):
        codes.append(m.group(1))
        return "\x00%d\x00" % (len(codes) - 1)

    text = re.sub(r"`([^`]+)`", keep_code, text)
    text = html.escape(text, quote=True)
    text = re.sub(r"\[([^\[\]]+)\]\(([^)\s]+)\)", lambda m: '<a href="%s">%s</a>' % (m.group(2), m.group(1)), text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: "<code>%s</code>" % html.escape(codes[int(m.group(1))], quote=True), text)


def parse(md):
    """Return (versions, links). Each version is a dict with name, date, and blocks."""
    versions, links = [], {}
    cur = None
    section = None
    for raw in md.splitlines():
        line = raw.rstrip()
        m = LINKDEF_RE.match(line)
        if m:
            links[m.group(1).lower()] = m.group(2)
            continue
        m = VERSION_RE.match(line)
        if m and not line.startswith("###"):
            cur = {"name": m.group(1), "date": m.group(2), "sections": []}
            section = None
            versions.append(cur)
            continue
        if cur is None or not line.strip():
            continue
        if line.startswith("### "):
            section = {"title": line[4:].strip(), "items": []}
            cur["sections"].append(section)
            continue
        if section is None:
            section = {"title": None, "items": []}
            cur["sections"].append(section)
        m = BULLET_RE.match(line)
        if m:
            if m.group(1) and section["items"] and section["items"][-1][0] == "li":
                section["items"][-1][2].append(m.group(2))
            else:
                section["items"].append(["li", m.group(2), []])
        elif raw[:1].isspace() and section["items"]:
            # A wrapped line belongs to the bullet above it.
            last = section["items"][-1]
            if last[2]:
                last[2][-1] += " " + line.strip()
            else:
                last[1] += " " + line.strip()
        else:
            section["items"].append(["p", line.strip(), []])
    versions = [v for v in versions if any(s["items"] for s in v["sections"])]
    return versions, links


def nice_date(iso):
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", iso or "")
    if not m:
        return html.escape(iso or "")
    y, mo, d = (int(x) for x in m.groups())
    return '<time datetime="%s">%d %s %d</time>' % (iso, d, MONTHS[mo - 1], y)


def render_items(items, indent):
    out, pad = [], " " * indent
    in_list = False
    for kind, text, kids in items:
        if kind == "li":
            if not in_list:
                out.append(pad + "<ul>")
                in_list = True
            sub = ""
            if kids:
                sub = "<ul>%s</ul>" % "".join("<li>%s</li>" % inline(k) for k in kids)
            out.append(pad + "  <li>%s%s</li>" % (inline(text), sub))
        else:
            if in_list:
                out.append(pad + "</ul>")
                in_list = False
            out.append(pad + "<p>%s</p>" % inline(text))
    if in_list:
        out.append(pad + "</ul>")
    return out


NEXT_LABEL = "Coming in the next release"
NEXT_NOTE = "These changes are on the website or the main branch, but not in the downloadable zip yet."
CHEVRON = '<svg class="icon" aria-hidden="true" viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></svg>'

# Older versions start open, so they show with JavaScript off. On phones this
# folds them, and a link to a version (on load, from the jump list, or any
# other #hash) opens it and scrolls to it.
FOLD_JS = """    <script>
    (function () {
      function openFor(hash) {
        if (!hash || hash.length < 2) return null;
        var el = document.getElementById(decodeURIComponent(hash.slice(1)));
        if (!el) return null;
        var d = el.querySelector('.c-fold');
        if (d) d.open = true;
        return el;
      }
      if (window.matchMedia('(max-width: 699px)').matches) {
        document.querySelectorAll('.c-fold').forEach(function (d) { d.open = false; });
      }
      var start = openFor(location.hash);
      if (start) start.scrollIntoView();
      window.addEventListener('hashchange', function () { var t = openFor(location.hash); if (t) t.scrollIntoView(); });
      document.addEventListener('click', function (e) {
        var a = e.target.closest && e.target.closest('a[href^="#"]');
        if (a) openFor(a.getAttribute('href'));
      });
    })();
    </script>"""


def version_id(name):
    """Return (anchor id, label) for a version name like '0.9.0' or 'Unreleased'."""
    if name.lower() == "unreleased":
        return "unreleased", NEXT_LABEL
    vid = "v" + name.lstrip("v")
    return vid, vid


def render_version(v, links, fold):
    """One version as a card. fold=True puts its changes behind a <details> disclosure."""
    name = v["name"]
    unreleased = name.lower() == "unreleased"
    vid, label = version_id(name)
    esc_id = html.escape(vid, quote=True)
    date = nice_date(v["date"]) if v["date"] else ""
    cls = "c-ver c-next" if unreleased else "c-ver"
    lines = ['    <section class="%s" id="%s" aria-labelledby="%s-h">' % (cls, esc_id, esc_id)]
    pad = 6
    if fold:
        pad = 8
        lines += ['      <details class="c-fold" open>',
                  '        <summary>',
                  '          <span class="c-ver-head"><h2 id="%s-h">%s</h2>%s</span>'
                  % (esc_id, html.escape(label), ('<span class="c-date">%s</span>' % date) if date else ''),
                  '          <span class="c-toggle"><span class="c-show">Show changes</span><span class="c-hide">Hide changes</span>%s</span>' % CHEVRON]
        if unreleased:
            lines.append('          <span class="c-next-note">%s</span>' % NEXT_NOTE)
        lines += ['        </summary>', '        <div class="c-fold-body">']
    else:
        lines += ['      <div class="c-ver-head">',
                  '        <h2 id="%s-h">%s</h2>' % (esc_id, html.escape(label))]
        if date:
            lines.append('        <p class="c-date">%s</p>' % date)
        lines.append('      </div>')
        if unreleased:
            lines.append('      <p class="c-next-note">%s</p>' % NEXT_NOTE)

    sp = " " * pad
    actions = []
    if not unreleased:
        actions.append('<a href="%s/releases/tag/%s">%s on GitHub</a>'
                       % (REPO, html.escape(vid, quote=True), html.escape(vid)))
    compare = links.get(name.lower())
    if compare:
        m = re.search(r"/compare/([^./][^/]*?)\.\.\.", compare)
        if m:
            text = "Code changes since %s" % m.group(1)
            actions.append('<a href="%s">%s</a>' % (html.escape(compare, quote=True), html.escape(text)))
    if actions:
        lines.append(sp + '<p class="c-links">%s</p>' % " ".join(actions))

    for s in v["sections"]:
        if not s["items"]:
            continue
        if s["title"]:
            lines.append(sp + '<h3>%s</h3>' % inline(s["title"]))
        lines.extend(render_items(s["items"], pad))
    if fold:
        lines += ['        </div>', '      </details>']
    lines.append('    </section>')
    return "\n".join(lines)


def render_versions(versions, links):
    """Unreleased (if any) and older releases fold; the newest release stays open."""
    out, newest_done = [], False
    for v in versions:
        released = v["name"].lower() != "unreleased"
        fold = not released or newest_done
        out.append(render_version(v, links, fold))
        if released:
            newest_done = True
    return "\n".join(out)


def build(idx, md):
    versions, links = parse(md)
    page = gen_guide.build(idx, "en", current=None)
    page = page.replace('<title>Guide | WriteLikeHuman</title>', '<title>Changelog | WriteLikeHuman</title>', 1)
    page = page.replace('<meta property="og:title" content="Guide | WriteLikeHuman">',
                        '<meta property="og:title" content="Changelog | WriteLikeHuman">', 1)
    page = page.replace('content="%s"' % gen_guide.EN_UI["desc"],
                        'content="Every WriteLikeHuman release, newest first: what was added, changed, and fixed."', 1)
    page = page.replace('WriteLikeHuman/guide.html">', 'WriteLikeHuman/changelog.html">', 1)
    page = page.replace('<a href="changelog.html">Changelog</a>', '<a href="changelog.html" aria-current="page">Changelog</a>', 1)
    # There is no Hindi or Tamil changelog, so the language links go to the landing pages.
    page = page.replace('<a href="guide.html" lang="en" aria-current="page">English</a>', '<a href="./" lang="en">English</a>')
    page = page.replace('<a href="hi/guide.html" lang="hi">', '<a href="hi/" lang="hi">')
    page = page.replace('<a href="ta/guide.html" lang="ta">', '<a href="ta/" lang="ta">')
    page = page.replace('All names and numbers in this guide are made up.',
                        'This page is built from CHANGELOG.md in the repository.', 1)
    page = page.replace('</style>', CSS + '</style>', 1)

    jump = "".join('<li><a href="#%s"%s>%s</a></li>'
                   % (html.escape(vid, quote=True), ' class="c-jump-next"' if vid == "unreleased" else '', html.escape(label))
                   for vid, label in (version_id(v["name"]) for v in versions))
    main = "\n".join([
        '<main id="main">',
        '<header class="c-hero" id="top">',
        '  <div class="wrap">',
        '    <p class="eyebrow">Changelog</p>',
        '    <h1>What changed</h1>',
        '    <p class="lede">Every release, newest first.</p>',
        '  </div>',
        '</header>',
        '',
        '<div class="wrap">',
        '  <div class="c-body">',
        '    <nav class="c-jump" aria-labelledby="c-jump-h">',
        '      <h2 id="c-jump-h">Jump to a version</h2>',
        '      <ul>%s</ul>' % jump,
        '    </nav>',
        render_versions(versions, links),
        FOLD_JS,
        '    <div class="c-more">',
        '      <p>Want the newest version?</p>',
        '      <div class="c-more-actions">',
        '        <a class="btn btn-primary" href="%s/releases/latest/download/WriteLikeHuman.zip"><svg class="icon" aria-hidden="true"><use href="#i-down"/></svg>Download the latest version</a>' % REPO,
        '        <a class="c-all" href="%s/releases">All releases</a>' % REPO,
        '      </div>',
        '    </div>',
        '  </div>',
        '</div>',
        '</main>',
    ])
    a = page.index('<main id="main">')
    b = page.index('</main>') + len('</main>')
    return page[:a] + main + page[b:]
