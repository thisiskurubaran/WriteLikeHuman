"""Builds docs/examples.html from write-like-human/examples/before-after.md.

The page reuses the styles, icons, nav, and footer of docs/index.html, so
build it after the landing page is final. Run through sync_site.py.
"""
import html
import re


def build(idx, md):
    """Return (examples page HTML, number of cards)."""

    head_top=idx[:idx.index('<script>')]
    theme_script=idx[idx.index('<script>'):idx.index('</script>')+9]
    css=idx[idx.index('<style>')+7:idx.index('</style>')]
    sprite=idx[idx.index('<!-- Reused icons -->'):idx.index('</svg>\n\n<nav')+6]
    script_all=idx[idx.rindex('<script>'):idx.rindex('</script>')+9]

    # --- page head
    head=head_top.replace('<title>WriteLikeHuman</title>','<title>Examples | WriteLikeHuman</title>')
    head=head.replace('content="A free Claude skill that makes everyday writing sound like a person wrote it. Emails, WhatsApp replies, letters, resumes, posts, and the files you already use."',
                      'content="Before and after examples from WriteLikeHuman: emails, WhatsApp replies, letters, resumes, posts, reviews, files, and more."')
    head=head.replace('<meta property="og:title" content="WriteLikeHuman">','<meta property="og:title" content="Examples | WriteLikeHuman">')
    head=head.replace('<meta property="og:url" content="https://thisiskurubaran.github.io/WriteLikeHuman/">','<meta property="og:url" content="https://thisiskurubaran.github.io/WriteLikeHuman/examples.html">')

    CATS={'Email':['Rewrite: a work message','Email: a polite no'],
     'Work':['Resume bullet','LinkedIn post','Reply to a customer review','Product listing'],
     'Personal':['WhatsApp reply to a landlord','Condolence message','Honest review','Voice note cleanup','Invitation','Marriage biodata'],
     'Letters':['Formal letter: leave application (Indian format)','Reading level: simpler for a parent','Essay: helping with the student\'s own draft','Complaint to a company'],
     'Checks':['Check: a short paragraph','Before you send','Message going abroad'],
     'Files':['Spreadsheet','Subtitles','Creating a file: a leave letter as a Word document','Creating a file: trip expenses as a spreadsheet'],
     'Languages':['Hinglish','Tamil message']}
    cat_of={t:c for c,ts in CATS.items() for t in ts}

    def inline(t):
        t=html.escape(t,quote=False)
        t=re.sub(r'`([^`]+)`',r'<code>\1</code>',t)
        return t

    def kind(label):
        l=label.lower()
        if l.startswith('before') or l.startswith('text') or l.startswith('student') or l.startswith('message') or l.startswith('review') or l.startswith('seller') or l.startswith('request') or l.startswith('user'): return 'in'
        return 'out'

    def render(body):
        lines=body.strip('\n').split('\n'); out=[]; i=0
        while i<len(lines):
            ln=lines[i]
            if not ln.strip(): i+=1; continue
            if ln.startswith('```'):
                j=i+1; buf=[]
                while j<len(lines) and not lines[j].startswith('```'): buf.append(lines[j]); j+=1
                out.append('<pre class="ex-pre">'+html.escape('\n'.join(buf),quote=False)+'</pre>'); i=j+1; continue
            if ln.startswith('>'):
                buf=[]
                while i<len(lines) and lines[i].startswith('>'):
                    buf.append(lines[i][1:].lstrip()); i+=1
                paras=[]; cur=[]
                for b in buf:
                    if b=='' : 
                        if cur: paras.append(cur); cur=[]
                    else: cur.append(b)
                if cur: paras.append(cur)
                out.append('<blockquote>'+''.join('<p>'+'<br>'.join(inline(x) for x in p)+'</p>' for p in paras)+'</blockquote>'); continue
            if ln.startswith('|'):
                rows=[]
                while i<len(lines) and lines[i].startswith('|'):
                    cells=[c.strip() for c in lines[i].strip().strip('|').split('|')]
                    if not all(re.fullmatch(r'-+',c) for c in cells if c): rows.append(cells)
                    i+=1
                th=rows[0]; trs=rows[1:]
                out.append('<div class="ex-table" tabindex="0" role="region" aria-label="Table"><table><thead><tr>'+''.join('<th>'+inline(c)+'</th>' for c in th)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+inline(c)+'</td>' for c in r)+'</tr>' for r in trs)+'</tbody></table></div>'); continue
            if ln.strip()=='What I changed':
                items=[]; i+=1
                while i<len(lines) and lines[i].startswith('- '): items.append(lines[i][2:]); i+=1
                out.append('<div class="ex-changes"><p class="ex-label">What I changed</p><ul>'+''.join('<li><svg class="icon" aria-hidden="true"><use href="#i-check"/></svg><span>'+inline(x)+'</span></li>' for x in items)+'</ul></div>'); continue
            m=re.fullmatch(r'([A-Z][^:]{0,60}):\s*(.*)',ln)
            if m and (not m.group(2) or m.group(2).startswith('"')):
                label=m.group(1); rest=m.group(2)
                k=kind(label)
                out.append('<p class="ex-label %s">%s</p>'%(k,inline(label)))
                if rest: out.append('<blockquote class="quote-in"><p>'+inline(rest)+'</p></blockquote>')
                i+=1; continue
            # plain paragraph (notes)
            buf=[]
            while i<len(lines) and lines[i].strip() and not lines[i].startswith(('>','```','|')): buf.append(lines[i]); i+=1
            txt=' '.join(buf)
            cls='ex-note'
            out.append('<p class="%s">%s</p>'%(cls,inline(txt)))
        return '\n'.join(out)

    secs=re.split(r'(?m)^## ',md)[1:]
    cards=[]
    for sec in secs:
        title,body=sec.split('\n',1)
        title=title.strip(); cat=cat_of.get(title,'Personal')
        cards.append((title,cat,render(body)))
    missing=[t for t,c,_ in cards if t not in cat_of]
    assert not missing, missing

    chips=['All']+list(CATS)
    chip_html=''.join('<button type="button" class="fchip" data-filter="%s" aria-pressed="%s">%s<span class="n">%d</span></button>'%(c,'true' if c=='All' else 'false',c,len(cards) if c=='All' else sum(1 for x in cards if x[1]==c)) for c in chips)
    card_html='\n'.join('''      <article class="ex-card" data-cat="%s" id="%s">
        <header class="ex-head"><span class="ex-tag t-%s">%s</span><h2>%s</h2></header>
        <div class="ex-body">
%s
        </div>
      </article>'''%(c,re.sub(r'[^a-z0-9]+','-',t.lower()).strip('-'),c.lower(),c,inline(t),b) for t,c,b in cards)

    extra_css='''
/* ---------- Examples page ---------- */
.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; border: 0; }
.ex-hero { padding: 40px 0 8px; }
@media (min-width: 640px) { .ex-hero { padding: 56px 0 12px; } }
.ex-hero h1 { font-size: clamp(2.2rem, 1.4rem + 4vw, 3.8rem); }
.ex-hero .lede { margin-bottom: 0; }
.ex-tools { margin: 24px 0 20px; padding: 12px; background: var(--panel); border: 1px solid var(--line); border-radius: var(--r-lg); box-shadow: var(--shadow-sm); display: grid; grid-template-columns: minmax(0, 1fr); gap: 10px; min-width: 0; }
.ex-search { min-width: 0; display: flex; align-items: center; gap: 10px; background: var(--panel-2); border: 1px solid var(--line); border-radius: 12px; padding: 0 12px; min-height: 46px; }
.ex-search .icon { width: 18px; height: 18px; color: var(--muted); flex: none; }
.ex-search input { flex: 1; width: 100%; min-width: 0; border: 0; background: transparent; color: var(--ink); font: inherit; font-size: 16px; padding: 10px 0; outline: none; }
.ex-search:focus-within { border-color: var(--accent); }
.fchips { display: flex; gap: 6px; overflow-x: auto; padding-bottom: 2px; scrollbar-width: none; }
.fchips::-webkit-scrollbar { display: none; }
.fchip { flex: none; display: inline-flex; align-items: center; gap: 6px; min-height: 40px; padding: 0 14px; border-radius: 999px; border: 1px solid var(--line); background: var(--panel); color: var(--ink-2); font: inherit; font-size: 14px; font-weight: 600; cursor: pointer; }
.fchip .n { font: 600 12px var(--mono); color: var(--muted); }
.fchip[aria-pressed="true"] { background: var(--ink); color: var(--bg); border-color: var(--ink); }
.fchip[aria-pressed="true"] .n { color: var(--bg); opacity: .7; }
@media (pointer: coarse) { .fchip { min-height: 44px; } }
.ex-count { margin: 0 0 14px; font-size: 14px; color: var(--muted); }
@media (min-width: 900px) { .ex-tools { position: sticky; top: calc(max(12px, env(safe-area-inset-top)) + 76px); z-index: 20; } }
.ex-grid { display: grid; grid-template-columns: minmax(0, 1fr); gap: 14px; }
@media (min-width: 900px) { .ex-grid { grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 16px; align-items: start; } }
.ex-card { background: var(--panel); border: 1px solid var(--line); border-radius: var(--r-lg); padding: var(--tile-pad); min-width: 0; box-shadow: var(--shadow-sm); scroll-margin-top: 180px; }
.ex-card[hidden] { display: none; }
.ex-head { display: flex; flex-direction: column; align-items: flex-start; gap: 8px; margin-bottom: 14px; }
.ex-head h2 { font-size: 1.15rem; line-height: 1.25; letter-spacing: -0.015em; margin: 0; }
.ex-tag { font: 700 12px var(--mono); letter-spacing: .06em; text-transform: uppercase; padding: 4px 10px; border-radius: 999px; background: var(--accent-soft); color: var(--accent); }
.ex-tag.t-files, .ex-tag.t-checks { background: var(--ok-soft); color: var(--ok); }
.ex-body { display: grid; grid-template-columns: minmax(0, 1fr); gap: 10px; min-width: 0; }
.ex-body p { margin: 0; }
.ex-label { font: 700 12px var(--mono); letter-spacing: .06em; text-transform: uppercase; color: var(--muted); margin-top: 4px !important; }
.ex-label.in { color: var(--bad); }
.ex-label.out { color: var(--ok); }
.ex-body blockquote { margin: 0; padding: 12px 14px; border-radius: 12px; background: var(--panel-2); border: 1px solid var(--line); font-size: 15px; color: var(--ink-2); overflow-wrap: anywhere; }
.ex-body blockquote p + p { margin-top: 8px; }
.ex-label.in + blockquote { border-left: 3px solid var(--bad); }
.ex-label.out + blockquote, .ex-label.out + .ex-pre { border-left: 3px solid var(--ok); }
.ex-pre { margin: 0; padding: 12px 14px; border-radius: 12px; background: var(--panel-2); border: 1px solid var(--line); font: 13px/1.6 var(--mono); color: var(--ink-2); white-space: pre-wrap; overflow-wrap: anywhere; }
.ex-note { font-size: 14px; color: var(--muted); }
.ex-body code { font: 13px var(--mono); background: var(--panel-2); border: 1px solid var(--line); border-radius: 6px; padding: 1px 5px; }
.ex-changes { padding: 12px 14px; border-radius: 12px; border: 1px dashed var(--line-strong); }
.ex-changes .ex-label { margin: 0 0 6px !important; }
.ex-changes ul { list-style: none; margin: 0; padding: 0; display: grid; gap: 6px; font-size: 14.5px; color: var(--ink-2); }
.ex-changes li { display: flex; gap: 8px; align-items: flex-start; }
.ex-changes .icon { width: 15px; height: 15px; color: var(--ok); stroke-width: 2.6; margin-top: 4px; flex: none; }
.ex-table:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.ex-table { max-width: 100%; overflow-x: auto; border: 1px solid var(--line); border-radius: 12px; }
.ex-table table { width: 100%; border-collapse: collapse; font-size: 14px; }
.ex-table th, .ex-table td { padding: 8px 10px; border-bottom: 1px solid var(--line); text-align: left; white-space: nowrap; }
.ex-table th { background: var(--panel-2); font-weight: 600; color: var(--muted); }
.ex-table tr:last-child td { border-bottom: 0; }
.ex-empty { padding: 32px 16px; text-align: center; color: var(--muted); border: 1px dashed var(--line-strong); border-radius: var(--r-lg); }
.ex-cta { margin-top: var(--section-space); }
'''
    nav='''<nav class="topnav" aria-label="Main">
  <div class="wrap bar">
    <a class="brand" href="./" aria-label="WriteLikeHuman home">
      <svg class="logo" aria-hidden="true" focusable="false"><use href="#logo"/></svg>
      WriteLikeHuman
    </a>
    <div class="links">
      <a href="./#files">Files</a>
      <a href="./#features">Features</a>
      <a href="examples.html" aria-current="page">Examples</a>
      <a href="guide.html">Guide</a>
      <a href="./#install">Install</a>
      <a href="https://github.com/thisiskurubaran/WriteLikeHuman">GitHub</a>
    </div>
    <div class="nav-end">
      <button class="icon-btn theme-btn" id="theme-btn" type="button" aria-label="Switch theme">
        <svg class="icon moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/></svg>
        <svg class="icon sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
      </button>
      <button class="icon-btn menu-btn" id="menu-btn" type="button" popovertarget="menu" aria-label="Open menu" aria-controls="menu">
        <svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
      </button>
      <a class="nav-cta" href="https://github.com/thisiskurubaran/WriteLikeHuman/releases/latest/download/WriteLikeHuman.zip">Download</a>
    </div>
  </div>
</nav>

<div class="menu" id="menu" popover>
  <a href="./">Home <svg class="icon" aria-hidden="true"><use href="#i-arrow"/></svg></a>
  <a href="./#files">Files <svg class="icon" aria-hidden="true"><use href="#i-arrow"/></svg></a>
  <a href="./#features">Features <svg class="icon" aria-hidden="true"><use href="#i-arrow"/></svg></a>
  <a href="guide.html">Guide <svg class="icon" aria-hidden="true"><use href="#i-arrow"/></svg></a>
  <a href="./#install">Install <svg class="icon" aria-hidden="true"><use href="#i-arrow"/></svg></a>
  <a href="https://github.com/thisiskurubaran/WriteLikeHuman">GitHub <svg class="icon" aria-hidden="true"><use href="#i-arrow"/></svg></a>
  <a href="https://github.com/thisiskurubaran/WriteLikeHuman/releases/latest/download/WriteLikeHuman.zip">Download <svg class="icon" aria-hidden="true"><use href="#i-down"/></svg></a>
  <div class="lang-switch" role="group" aria-label="Language"><a href="./" lang="en">English</a><a href="hi/" lang="hi">हिंदी</a><a href="ta/" lang="ta">தமிழ்</a></div>
</div>
'''
    footer='''<footer>
  <div class="wrap foot">
    <div class="foot-top">
      <a class="brand" href="#top" aria-label="WriteLikeHuman, back to top"><svg class="logo" aria-hidden="true" focusable="false"><use href="#logo"/></svg>WriteLikeHuman</a>
      <a class="to-top" href="#top">Top <svg class="icon" aria-hidden="true"><use href="#i-down"/></svg></a>
    </div>
    <p class="foot-note">Free and open source under the MIT license.</p>
    <nav class="flinks" aria-label="Footer">
      <a href="https://github.com/thisiskurubaran/WriteLikeHuman">GitHub</a>
      <a href="changelog.html">Changelog</a>
      <a href="https://github.com/thisiskurubaran/WriteLikeHuman/blob/main/CONTRIBUTING.md">Contribute</a>
      <a href="./">Home</a>
      <a href="guide.html">Guide</a>
      <a href="https://github.com/thisiskurubaran/WriteLikeHuman/issues/new?template=feedback.md">Share feedback</a>
      <a href="privacy.html">Privacy</a>
    </nav>
    <div class="lang-switch foot-langs" role="group" aria-label="Language"><a href="./" lang="en">English</a><a href="hi/" lang="hi">हिंदी</a><a href="ta/" lang="ta">தமிழ்</a></div>
    <p class="foot-small">An independent project. Claude is made by Anthropic. All names and numbers in these examples are made up.</p>
  </div>
</footer>
'''
    # page script: theme + menu from index, plus filtering
    theme_menu=script_all[:script_all.index('  /* Before and after demo */')]+'''  /* Search and filter */
  var cards = Array.prototype.slice.call(document.querySelectorAll('.ex-card'));
  var search = document.getElementById('ex-q'), count = document.getElementById('ex-count'), empty = document.getElementById('ex-empty');
  var chips = document.querySelectorAll('.fchip'), cat = 'All';
  var texts = cards.map(function (c) { return c.textContent.toLowerCase(); });
  function apply() {
    var q = search.value.trim().toLowerCase(), shown = 0;
    cards.forEach(function (c, i) {
      var ok = (cat === 'All' || c.getAttribute('data-cat') === cat) && (!q || texts[i].indexOf(q) !== -1);
      c.hidden = !ok; if (ok) shown++;
    });
    count.textContent = shown === 1 ? '1 example' : shown + ' examples';
    empty.hidden = shown !== 0;
  }
  chips.forEach(function (b) {
    b.addEventListener('click', function () {
      chips.forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
      b.setAttribute('aria-pressed', 'true'); cat = b.getAttribute('data-filter'); swap(apply);
    });
  });
  search.addEventListener('input', apply);
  document.getElementById('ex-tools').hidden = false;
  apply();
})();
</script>'''

    page=head+theme_script+'\n<style>'+css+extra_css+'</style>\n</head>\n<body>\n<a class="skip" href="#main">Skip to content</a>\n\n'+sprite+'\n\n'+nav+'''
<main id="main">
<header class="ex-hero" id="top">
  <div class="wrap">
    <p class="eyebrow">Examples</p>
    <h1>Before and after</h1>
    <p class="lede">Real kinds of everyday writing, fixed by WriteLikeHuman. Every name, company, and number here is made up. Search, or pick a kind of writing.</p>
  </div>
</header>

<section aria-label="Examples" style="padding-top:0">
  <div class="wrap">
    <div class="ex-tools" id="ex-tools" hidden>
      <label class="ex-search"><svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg><span class="sr-only">Search examples</span><input id="ex-q" type="search" placeholder="Search, for example: WhatsApp, resume, Tamil" autocomplete="off"></label>
      <div class="fchips" role="group" aria-label="Filter by kind of writing">'''+chip_html+'''</div>
    </div>
    <p class="ex-count" id="ex-count" aria-live="polite">'''+str(len(cards))+''' examples</p>
    <div class="ex-grid">
'''+card_html+'''
    </div>
    <p class="ex-empty" id="ex-empty" hidden>No examples match that. Try another word, or pick All.</p>

    <div class="cta-band ex-cta">
      <svg class="squiggle sq1" viewBox="0 0 400 60" aria-hidden="true"><path d="M10 40c30-30 50-30 70 0s40 30 70 0 50-30 70 0 40 30 70 0 50-30 70 0"/></svg>
      <svg class="squiggle sq2" viewBox="0 0 400 60" aria-hidden="true"><path d="M10 40c30-30 50-30 70 0s40 30 70 0 50-30 70 0 40 30 70 0 50-30 70 0"/></svg>
      <h2>Try it on your own writing</h2>
      <p>Download once, upload once, and ask in your own words.</p>
      <div class="actions">
        <a class="btn btn-primary" href="https://github.com/thisiskurubaran/WriteLikeHuman/releases/latest/download/WriteLikeHuman.zip"><svg class="icon" aria-hidden="true"><use href="#i-down"/></svg>Download the skill</a>
        <a class="btn btn-secondary" href="./#install">How to install</a>
      </div>
    </div>
  </div>
</section>
</main>

'''+footer+'\n'+theme_menu+'\n</body>\n</html>\n'
    return page, len(cards)
