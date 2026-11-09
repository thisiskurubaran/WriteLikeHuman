"""Keep the website in sync with the repo.

The English landing page (docs/index.html) is the source. This script:

1. Updates every number marked with data-stat on the English page (how many
   guides, writing types, languages, and test cases) from the repo.
2. Rebuilds the Hindi and Tamil landing pages (docs/hi/, docs/ta/) from it.
3. Rebuilds the examples page (docs/examples.html) from
   write-like-human/examples/before-after.md.
4. Rebuilds the guide (docs/guide.html) from the tasks in gen_guide.py.

Run from the repo root:
    python3 docs/_build/sync_site.py           write any pages that changed
    python3 docs/_build/sync_site.py --check   change nothing, exit 1 if any page is out of date

Standard library only.
"""

import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

import gen_examples  # noqa: E402
import gen_guide  # noqa: E402
import gen_lang  # noqa: E402


def load_counts():
    """Recompute the site numbers with the same code the tests use."""
    path = os.path.join(ROOT, "tests", "test_site.py")
    spec = importlib.util.spec_from_file_location("test_site", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.actual_counts()


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def expected_pages():
    """Return {repo-relative path: expected content} for every generated page."""
    counts = load_counts()
    index = read("docs/index.html")

    def fix(m):
        name = m.group(1)
        if name not in counts:
            sys.exit("Unknown data-stat name on docs/index.html: %s" % name)
        return 'data-stat="%s">%d<' % (name, counts[name])

    index = re.sub(r'data-stat="(\w+)">(\d+)<', fix, index)
    pages = {"docs/index.html": index}
    for lang, html in gen_lang.build(index).items():
        pages["docs/%s/index.html" % lang] = html
    examples, _cards = gen_examples.build(index, read("write-like-human/examples/before-after.md"))
    pages["docs/examples.html"] = examples
    pages["docs/guide.html"] = gen_guide.build(index)
    return pages, counts


def main():
    check = "--check" in sys.argv[1:]
    try:
        pages, counts = expected_pages()
    except gen_lang.NotFound as err:
        sys.exit("Could not build the translated pages: %s" % err)

    stale = []
    for rel, content in pages.items():
        path = os.path.join(ROOT, rel)
        current = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if current == content:
            continue
        stale.append(rel)
        if not check:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

    numbers = ", ".join("%s %d" % (k, v) for k, v in sorted(counts.items()))
    if check:
        if stale:
            print("These pages are out of date: %s" % ", ".join(stale))
            print("Run: python3 docs/_build/sync_site.py   (then commit the changed pages)")
            sys.exit(1)
        print("All generated pages are up to date (%s)." % numbers)
    else:
        print("Updated: %s" % (", ".join(stale) if stale else "nothing, already up to date"))
        print("Numbers: %s" % numbers)


if __name__ == "__main__":
    main()
