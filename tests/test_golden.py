"""Golden-file tests: everything the user didn't ask to change stays exactly the same.

For each Office script, the test builds a small made-up file, changes one
piece of text, and then compares the output with the input:

- Every part of the file other than the one holding the changed text must
  be byte for byte identical (styles, images, headers, settings, and so on).
- Inside the changed part, every other paragraph, cell, or shape must be
  identical too: same text, same formatting XML, same formulas.

This catches quiet formatting damage that a text-only check would miss.

Run from the repo root:  python -m unittest discover -s tests -v
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "write-like-human", "scripts")

try:
    import docx  # noqa: F401
    from docx.shared import Pt, RGBColor
    HAVE_DOCX = True
except ImportError:
    HAVE_DOCX = False
try:
    import openpyxl
    from openpyxl.comments import Comment
    from openpyxl.styles import Font
    HAVE_XLSX = True
except ImportError:
    HAVE_XLSX = False
try:
    import pptx  # noqa: F401
    from pptx.util import Inches, Pt as PPt
    HAVE_PPTX = True
except ImportError:
    HAVE_PPTX = False

# Parts that only hold timestamps or app info and may be rewritten on save.
METADATA = {"docProps/core.xml", "docProps/app.xml"}


def run(script, *args):
    out = subprocess.run([sys.executable, os.path.join(SCRIPTS, script)] + list(args),
                         capture_output=True, text=True)
    if out.returncode != 0:
        raise AssertionError("%s failed: %s %s" % (script, out.stdout, out.stderr))
    return out.stdout


def differing_parts(a_path, b_path):
    a, b = zipfile.ZipFile(a_path), zipfile.ZipFile(b_path)
    if set(a.namelist()) != set(b.namelist()):
        return {"<part list changed>": sorted(set(a.namelist()) ^ set(b.namelist()))}
    return {n for n in a.namelist() if n not in METADATA and a.read(n) != b.read(n)}


@unittest.skipUnless(HAVE_DOCX, "python-docx not installed")
class _WordBase(unittest.TestCase):
    """Builds the sample report. Holds no tests itself."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.src = os.path.join(self.tmp, "report.docx")
        d = docx.Document()
        d.sections[0].header.paragraphs[0].text = "Northbay Traders, Quarterly report"
        d.add_heading("Quarterly report", 1)
        p = d.add_paragraph("Sales grew in March. ")
        r = p.add_run("Mumbai led with Rs 4,20,000.")
        r.bold = True
        r.font.color.rgb = RGBColor(0xC2, 0x41, 0x0C)
        p2 = d.add_paragraph("It is important to note that the team worked tirelessly.")
        p2.runs[0].italic = True
        p2.runs[0].font.size = Pt(13)
        d.add_paragraph("A list item stays put.", style="List Bullet")
        t = d.add_table(rows=2, cols=2)
        t.cell(0, 0).text, t.cell(0, 1).text = "Region", "Amount"
        t.cell(1, 0).text, t.cell(1, 1).text = "Pune", "Rs 1,10,000"
        d.add_page_break()
        d.add_paragraph("Last page note.")
        d.save(self.src)

    def _apply(self, target_text, new_text, *extra):
        segs = json.loads(run("docx_rewrite.py", "extract", self.src))["segments"]
        target = next(s["id"] for s in segs if s["text"] == target_text)
        changes = os.path.join(self.tmp, "changes.json")
        with open(changes, "w", encoding="utf-8") as f:
            json.dump({target: new_text}, f)
        out = os.path.join(self.tmp, "out.docx")
        run("docx_rewrite.py", "apply", self.src, changes, "-o", out, *extra)
        return target, out


class WordGoldenTest(_WordBase):
    def test_only_the_document_part_changes(self):
        _, out = self._apply("It is important to note that the team worked tirelessly.",
                             "The team worked hard.")
        self.assertEqual(differing_parts(self.src, out), {"word/document.xml"})

    def test_other_paragraphs_are_byte_identical(self):
        from lxml import etree
        _, out = self._apply("It is important to note that the team worked tirelessly.",
                             "The team worked hard.")
        before = [etree.tostring(p._p) for p in docx.Document(self.src).paragraphs]
        after_doc = docx.Document(out)
        after = [etree.tostring(p._p) for p in after_doc.paragraphs]
        self.assertEqual(len(before), len(after))
        changed = [i for i, (x, y) in enumerate(zip(before, after)) if x != y]
        self.assertEqual(len(changed), 1, "exactly one paragraph should change")
        para = after_doc.paragraphs[changed[0]]
        self.assertEqual(para.text, "The team worked hard.")
        self.assertTrue(para.runs[0].italic, "the changed paragraph keeps its italics")
        self.assertEqual(para.runs[0].font.size, Pt(13), "and its font size")
        tb = docx.Document(self.src).tables[0]._tbl
        ta = after_doc.tables[0]._tbl
        self.assertEqual(etree.tostring(tb), etree.tostring(ta), "the table is untouched")

    def test_tracked_changes_leave_other_parts_alone(self):
        _, out = self._apply("Last page note.", "Final note.", "--track-changes")
        self.assertEqual(differing_parts(self.src, out), {"word/document.xml"})


@unittest.skipUnless(HAVE_XLSX, "openpyxl not installed")
class ExcelGoldenTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.src = os.path.join(self.tmp, "budget.xlsx")
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Budget"
        ws.append(["Item", "Amount", "Date", "Remarks"])
        ws.append(["Hotel", 6400, None, "Customer has expressed significant dissatisfaction."])
        ws.append(["Train", 2150, None, "Booked early."])
        ws["C2"] = "2026-03-15"
        ws["B4"] = "=SUM(B2:B3)"
        ws["B2"].number_format = "#,##0"
        ws["A1"].font = Font(bold=True, color="C2410C")
        ws["D3"].comment = Comment("Check with Ravi", "Asha")
        ws.column_dimensions["D"].width = 42
        notes = wb.create_sheet("Notes")
        notes["A1"] = "Second sheet stays exactly the same."
        wb.save(self.src)

    def test_only_the_changed_cell_differs(self):
        changes = os.path.join(self.tmp, "changes.json")
        with open(changes, "w", encoding="utf-8") as f:
            json.dump({"Budget!D2": "Customer unhappy."}, f)
        out = os.path.join(self.tmp, "out.xlsx")
        run("xlsx_text_cells.py", "apply", self.src, changes, "-o", out)

        a, b = openpyxl.load_workbook(self.src), openpyxl.load_workbook(out)
        self.assertEqual(a.sheetnames, b.sheetnames)
        for name in a.sheetnames:
            for row in a[name].iter_rows():
                for cell in row:
                    other = b[name][cell.coordinate]
                    if name == "Budget" and cell.coordinate == "D2":
                        self.assertEqual(other.value, "Customer unhappy.")
                        continue
                    with self.subTest(cell="%s!%s" % (name, cell.coordinate)):
                        self.assertEqual(cell.value, other.value)
                        self.assertEqual(cell.number_format, other.number_format)
                        self.assertEqual(cell.font.b, other.font.b)
                        self.assertEqual(cell.font.color and cell.font.color.rgb,
                                         other.font.color and other.font.color.rgb)
        self.assertEqual(b["Budget"]["B4"].value, "=SUM(B2:B3)", "the formula survives")
        self.assertEqual(b["Budget"]["D3"].comment.text, "Check with Ravi")
        self.assertEqual(b["Budget"].column_dimensions["D"].width, 42)
        parts = differing_parts(self.src, out)
        self.assertNotIn("xl/worksheets/sheet2.xml", parts, "the second sheet is untouched")


@unittest.skipUnless(HAVE_PPTX, "python-pptx not installed")
class SlidesGoldenTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.src = os.path.join(self.tmp, "deck.pptx")
        prs = pptx.Presentation()
        s1 = prs.slides.add_slide(prs.slide_layouts[1])
        s1.shapes.title.text = "Quarterly update"
        s1.placeholders[1].text = "We are excited to harness our synergies going forward."
        s1.notes_slide.notes_text_frame.text = "Speak slowly here."
        s2 = prs.slides.add_slide(prs.slide_layouts[5])
        s2.shapes.title.text = "Slide two stays the same"
        box = s2.shapes.add_textbox(Inches(1), Inches(2), Inches(5), Inches(1))
        box.text_frame.text = "Rs 4,20,000 in March"
        box.text_frame.paragraphs[0].runs[0].font.size = PPt(28)
        prs.save(self.src)

    def test_other_slides_and_parts_are_untouched(self):
        segs = json.loads(run("pptx_rewrite.py", "extract", self.src))["segments"]
        target = next(s["id"] for s in segs if s["text"].startswith("We are excited"))
        changes = os.path.join(self.tmp, "changes.json")
        with open(changes, "w", encoding="utf-8") as f:
            json.dump({target: "We will work together on this."}, f)
        out = os.path.join(self.tmp, "out.pptx")
        run("pptx_rewrite.py", "apply", self.src, changes, "-o", out)
        self.assertEqual(differing_parts(self.src, out), {"ppt/slides/slide1.xml"})


@unittest.skipUnless(HAVE_DOCX, "python-docx not installed")
class WordCommentsGoldenTest(_WordBase):
    """--comments may add the comments part, its relationship, and its content
    type, and edit document.xml. Every other part stays identical."""

    ALLOWED = {"word/document.xml", "word/comments.xml", "word/_rels/document.xml.rels", "[Content_Types].xml"}

    def _changed_parts(self, out):
        a, b = zipfile.ZipFile(self.src), zipfile.ZipFile(out)
        added = set(b.namelist()) - set(a.namelist())
        removed = set(a.namelist()) - set(b.namelist())
        self.assertEqual(removed, set(), "no part may disappear")
        changed = {n for n in a.namelist() if n not in METADATA and a.read(n) != b.read(n)}
        return changed | added

    def test_comments_touch_only_their_parts(self):
        _, out = self._apply("It is important to note that the team worked tirelessly.",
                             "The team worked hard.", "--comments")
        self.assertLessEqual(self._changed_parts(out), self.ALLOWED)
        self.assertIn("word/comments.xml", zipfile.ZipFile(out).namelist())

    def test_comments_with_tracked_changes(self):
        _, out = self._apply("Last page note.", "Final note.", "--comments", "--track-changes")
        self.assertLessEqual(self._changed_parts(out), self.ALLOWED)

    def test_comment_text_and_other_paragraphs(self):
        from lxml import etree
        segs = json.loads(run("docx_rewrite.py", "extract", self.src))["segments"]
        target = next(s["id"] for s in segs if s["text"] == "Last page note.")
        changes = os.path.join(self.tmp, "c.json")
        with open(changes, "w", encoding="utf-8") as f:
            json.dump({target: {"text": "Final note.", "why": "Shorter."}}, f)
        out = os.path.join(self.tmp, "c.docx")
        run("docx_rewrite.py", "apply", self.src, changes, "-o", out, "--comments")
        doc = docx.Document(out)
        if hasattr(doc, "comments"):
            self.assertEqual([c.text for c in doc.comments], ["Shorter."])
        before = [etree.tostring(p._p) for p in docx.Document(self.src).paragraphs]
        after = [etree.tostring(p._p) for p in doc.paragraphs]
        self.assertEqual(sum(1 for x, y in zip(before, after) if x != y), 1)


try:
    import pypdf  # noqa: F401
    from reportlab.pdfgen import canvas as _canvas  # noqa: F401
    HAVE_FORMS = True
except ImportError:
    HAVE_FORMS = False


@unittest.skipUnless(HAVE_FORMS, "pypdf or reportlab not installed")
class FormGoldenTest(unittest.TestCase):
    def setUp(self):
        from reportlab.pdfgen import canvas
        self.tmp = tempfile.mkdtemp()
        self.src = os.path.join(self.tmp, "form.pdf")
        c = canvas.Canvas(self.src)
        c.drawString(72, 760, "Page one: applicant")
        c.acroForm.textfield(name="full_name", x=160, y=750, width=200, height=20)
        c.acroForm.textfield(name="city", x=160, y=720, width=200, height=20)
        c.acroForm.checkbox(name="agree", x=160, y=690, size=16)
        c.showPage()
        c.drawString(72, 760, "Page two: notes stay the same")
        c.acroForm.textfield(name="notes", x=160, y=750, width=200, height=20, value="Existing note")
        c.save()

    def test_only_filled_fields_change(self):
        from pypdf import PdfReader
        values = os.path.join(self.tmp, "v.json")
        with open(values, "w", encoding="utf-8") as f:
            json.dump({"full_name": "Asha Verma"}, f)
        out = os.path.join(self.tmp, "out.pdf")
        run("form_fill.py", "fill", self.src, values, "-o", out)
        a, b = PdfReader(self.src), PdfReader(out)
        self.assertEqual(len(a.pages), len(b.pages))
        for i, (pa, pb) in enumerate(zip(a.pages, b.pages)):
            self.assertEqual(pa.extract_text(), pb.extract_text(), "page %d text" % (i + 1))
        fa, fb = a.get_fields(), b.get_fields()
        self.assertEqual(set(fa), set(fb))
        for name in fa:
            if name == "full_name":
                self.assertEqual(fb[name].get("/V"), "Asha Verma")
            else:
                self.assertEqual(fa[name].get("/V"), fb[name].get("/V"), name)


HTML_PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Rani's Bakery</title>
<meta name="description" content="We harness tradition to bake bread daily.">
<style>p { color: #333; }</style>
<script>var x = "keep me";</script></head>
<body>
<h1 class='big'>Welcome to Rani's Bakery</h1>
<p>We are thrilled to offer fresh bread &amp; cakes from Rs 450.</p>
<img src="bread.jpg" alt="A delightful image of bread" width=300>
<pre>  code   stays  </pre>
<p title="Hours">Open 7 am to 9 pm.</p>
</body></html>
"""


class HtmlGoldenTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.src = os.path.join(self.tmp, "page.html")
        with open(self.src, "w", encoding="utf-8", newline="") as f:
            f.write(HTML_PAGE)

    def _apply(self, mapping, *extract_flags):
        nodes = json.loads(run("html_rewrite.py", "extract", self.src, *extract_flags))["nodes"]
        ids = {n["text"]: n["id"] for n in nodes}
        changes = os.path.join(self.tmp, "c.json")
        with open(changes, "w", encoding="utf-8") as f:
            json.dump({ids[k]: v for k, v in mapping.items()}, f)
        out = os.path.join(self.tmp, "out.html")
        run("html_rewrite.py", "apply", self.src, changes, "-o", out)
        with open(out, encoding="utf-8", newline="") as f:
            return f.read()

    def test_text_only_bytes_outside_change_identical(self):
        result = self._apply({"Welcome to Rani's Bakery": "Fresh bread at Rani's"})
        self.assertEqual(result, HTML_PAGE.replace("Welcome to Rani's Bakery", "Fresh bread at Rani's"))

    def test_attributes_bytes_outside_change_identical(self):
        result = self._apply({"A delightful image of bread": "Loaves of bread on a counter",
                              "We harness tradition to bake bread daily.": "We bake bread every day."},
                             "--attributes")
        expected = (HTML_PAGE.replace("A delightful image of bread", "Loaves of bread on a counter")
                    .replace("We harness tradition to bake bread daily.", "We bake bread every day."))
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
