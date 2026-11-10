"""Tests for the helper scripts in write-like-human/scripts.

Every sample file is made up and built in a temporary folder while the
tests run, so no real documents are stored in the repository.

Run from the repository root:

    python -m unittest discover -s tests -v
"""

import csv
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
    HAVE_DOCX = True
except ImportError:
    HAVE_DOCX = False
try:
    import openpyxl  # noqa: F401
    HAVE_XLSX = True
except ImportError:
    HAVE_XLSX = False
try:
    import pptx  # noqa: F401
    HAVE_PPTX = True
except ImportError:
    HAVE_PPTX = False
try:
    import pypdf  # noqa: F401
    HAVE_PYPDF = True
except ImportError:
    HAVE_PYPDF = False


def run(script, *args, expect=0):
    proc = subprocess.run(
        [sys.executable, os.path.join(SCRIPTS, script)] + [str(a) for a in args],
        capture_output=True, text=True, encoding="utf-8",
    )
    if expect is not None and proc.returncode != expect:
        raise AssertionError("%s %s exited %d\nstdout: %s\nstderr: %s"
                             % (script, args, proc.returncode, proc.stdout, proc.stderr))
    return proc


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False)
    return path


class TempDirCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = self._tmp.name

    def tearDown(self):
        self._tmp.cleanup()

    def path(self, name):
        return os.path.join(self.dir, name)


@unittest.skipUnless(HAVE_DOCX, "python-docx is not installed")
class DocxRewriteTest(TempDirCase):
    def make_doc(self):
        from docx import Document
        doc = Document()
        doc.add_heading("Team update", level=1)
        p = doc.add_paragraph("We ")
        p.add_run("harnessed").bold = True
        p.add_run(" new tools to reach Rs 4,50,000 in sales.")
        table = doc.add_table(rows=1, cols=2)
        table.cell(0, 0).text = "Region"
        table.cell(0, 1).text = "The north team utilized the new process."
        doc.sections[0].header.paragraphs[0].text = "Northbay Traders"
        path = self.path("update.docx")
        doc.save(path)
        return path

    def segments(self, path):
        out = self.path("seg.json")
        run("docx_rewrite.py", "extract", path, "-o", out)
        with open(out, encoding="utf-8") as fh:
            return {s["text"]: s["id"] for s in json.load(fh)["segments"]}

    def test_comments_explain_each_change(self):
        src = self.make_doc()
        ids = self.segments(src)
        changes = write_json(self.path("c.json"), {
            ids["The north team utilized the new process."]: {
                "text": "The north team used the new process.", "why": "Swapped utilized for used."},
            ids["Team update"]: "Team news",
        })
        out = self.path("commented.docx")
        run("docx_rewrite.py", "apply", src, changes, "-o", out, "--comments")
        with zipfile.ZipFile(out) as z:
            xml = z.read("word/comments.xml").decode("utf-8")
            body = z.read("word/document.xml").decode("utf-8")
        self.assertIn("Swapped utilized for used.", xml)
        self.assertIn("Reworded for clarity.", xml)
        self.assertEqual(body.count("commentReference"), 2)

    def test_formatting_kept(self):
        from docx import Document
        src = self.make_doc()
        ids = self.segments(src)
        body = ids["We harnessed new tools to reach Rs 4,50,000 in sales."]
        cell = ids["The north team utilized the new process."]
        changes = write_json(self.path("c.json"), {
            body: "We used new tools to reach Rs 4,50,000 in sales.",
            cell: "The north team used the new process.",
        })
        run("docx_rewrite.py", "apply", src, changes)
        out = self.path("update-humanized.docx")
        self.assertTrue(os.path.exists(out))
        doc = Document(out)
        para = doc.paragraphs[1]
        self.assertEqual(para.text, "We used new tools to reach Rs 4,50,000 in sales.")
        bold = "".join(r.text for r in para.runs if r.bold)
        self.assertEqual(bold.strip(), "used")
        self.assertEqual(doc.paragraphs[0].style.name, "Heading 1")
        self.assertEqual(doc.tables[0].cell(0, 1).text, "The north team used the new process.")
        self.assertEqual(doc.tables[0].cell(0, 0).text, "Region")
        self.assertEqual(doc.sections[0].header.paragraphs[0].text, "Northbay Traders")

    def test_refuses_overwrite(self):
        src = self.make_doc()
        changes = write_json(self.path("c.json"), {})
        proc = run("docx_rewrite.py", "apply", src, changes, "-o", src, expect=None)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("overwrite", (proc.stdout + proc.stderr).lower())

    def test_track_changes(self):
        src = self.make_doc()
        ids = self.segments(src)
        cell = ids["The north team utilized the new process."]
        changes = write_json(self.path("c.json"), {cell: "The north team used the new process."})
        run("docx_rewrite.py", "apply", src, changes, "--track-changes")
        with zipfile.ZipFile(self.path("update-humanized.docx")) as z:
            xml = z.read("word/document.xml").decode("utf-8")
        self.assertIn("<w:del ", xml)
        self.assertIn("<w:ins ", xml)
        self.assertIn("WriteLikeHuman", xml)

    def test_number_change_flagged(self):
        src = self.make_doc()
        ids = self.segments(src)
        body = ids["We harnessed new tools to reach Rs 4,50,000 in sales."]
        changes = write_json(self.path("c.json"), {body: "We used new tools to reach Rs 5,00,000 in sales."})
        proc = run("docx_rewrite.py", "apply", src, changes)
        self.assertIn("CHECK:", proc.stdout)


@unittest.skipUnless(HAVE_XLSX, "openpyxl is not installed")
class XlsxHiddenCellsTest(TempDirCase):
    def test_hidden_sheet_row_and_column_marked(self):
        from openpyxl import Workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Main"
        ws["A1"] = "Shown text here"
        ws["A2"] = "Hidden row text"
        ws.row_dimensions[2].hidden = True
        ws["C1"] = "Hidden column text"
        ws.column_dimensions["C"].hidden = True
        other = wb.create_sheet("Notes")
        other["A1"] = "Hidden sheet text"
        other.sheet_state = "hidden"
        src = self.path("h.xlsx")
        wb.save(src)
        cells = json.loads(run("xlsx_text_cells.py", "extract", src).stdout)["cells"]
        hidden = {c["id"]: c.get("hidden", False) for c in cells}
        self.assertEqual(hidden, {"Main!A1": False, "Main!C1": True, "Main!A2": True, "Notes!A1": True})


class XlsxTextCellsTest(TempDirCase):
    def make_book(self):
        from openpyxl import Workbook
        from openpyxl.comments import Comment
        wb = Workbook()
        ws = wb.active
        ws.title = "Budget"
        ws.append(["Item", "Qty", "Price", "Total", "Notes"])
        ws.append(["Chairs", 4, 1250, "=B2*C2", "Customer has expressed significant dissatisfaction."])
        ws.append(["Tables", 2, 4800, "=B3*C3", "Delivered on time"])
        ws["D4"] = "=SUM(D2:D3)"
        ws["E2"].comment = Comment("Please utilize the new vendor going forward.", "Ravi")
        path = self.path("budget.xlsx")
        wb.save(path)
        return path

    def test_formulas_and_numbers_untouched(self):
        from openpyxl import load_workbook
        src = self.make_book()
        out = self.path("cells.json")
        run("xlsx_text_cells.py", "extract", src, "-o", out)
        with open(out, encoding="utf-8") as fh:
            data = json.load(fh)
        items = data["cells"] if isinstance(data, dict) and "cells" in data else data
        listed = {c["id"] for c in items}
        self.assertIn("Budget!E2", listed)
        self.assertNotIn("Budget!D2", listed)
        self.assertNotIn("Budget!B2", listed)

        changes = write_json(self.path("c.json"), {
            "Budget!E2": "Customer unhappy.",
            "Budget!E2#comment": "Please use the new vendor from now on.",
        })
        run("xlsx_text_cells.py", "apply", src, changes)
        wb = load_workbook(self.path("budget-humanized.xlsx"))
        ws = wb["Budget"]
        self.assertEqual(ws["E2"].value, "Customer unhappy.")
        self.assertEqual(ws["D2"].value, "=B2*C2")
        self.assertEqual(ws["D4"].value, "=SUM(D2:D3)")
        self.assertEqual(ws["C2"].value, 1250)
        self.assertEqual(ws["E2"].comment.text, "Please use the new vendor from now on.")

    def test_refuses_formula_cell(self):
        src = self.make_book()
        changes = write_json(self.path("c.json"), {"Budget!D2": "oops"})
        proc = run("xlsx_text_cells.py", "apply", src, changes, expect=None)
        from openpyxl import load_workbook
        out = self.path("budget-humanized.xlsx")
        if os.path.exists(out):
            self.assertEqual(load_workbook(out)["Budget"]["D2"].value, "=B2*C2")
        self.assertTrue(proc.returncode != 0 or "refus" in (proc.stdout + proc.stderr).lower()
                        or "skip" in (proc.stdout + proc.stderr).lower())

    def test_csv(self):
        src = self.path("feedback.csv")
        with open(src, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["Date", "Score", "Comment"])
            w.writerow(["2025-03-12", "4", "The service was truly a game changer for our family."])
        run("xlsx_text_cells.py", "extract", src, "-o", self.path("cells.json"))
        with open(self.path("cells.json"), encoding="utf-8") as fh:
            data = json.load(fh)
        items = data["cells"] if isinstance(data, dict) and "cells" in data else data
        target = [c["id"] for c in items if c["text"].startswith("The service")][0]
        run("xlsx_text_cells.py", "apply", src, write_json(self.path("c.json"), {target: "The service helped our family a lot."}))
        with open(self.path("feedback-humanized.csv"), encoding="utf-8") as fh:
            rows = list(csv.reader(fh))
        self.assertEqual(rows[1][0], "2025-03-12")
        self.assertEqual(rows[1][1], "4")
        self.assertEqual(rows[1][2], "The service helped our family a lot.")


@unittest.skipUnless(HAVE_PPTX, "python-pptx is not installed")
class PptxRewriteTest(TempDirCase):
    def test_slide_and_notes(self):
        from pptx import Presentation
        prs = Presentation()
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        slide.shapes.title.text = "Q3 results"
        slide.placeholders[1].text = "We delivered best-in-class growth of 12 percent."
        slide.notes_slide.notes_text_frame.text = "Moving forward, we will utilize this momentum."
        src = self.path("deck.pptx")
        prs.save(src)

        out = self.path("seg.json")
        run("pptx_rewrite.py", "extract", src, "-o", out)
        with open(out, encoding="utf-8") as fh:
            segs = json.load(fh)["segments"]
        body = [s["id"] for s in segs if s["text"].startswith("We delivered")][0]
        notes = [s["id"] for s in segs if "notes" in s["id"]][0]
        run("pptx_rewrite.py", "apply", src, write_json(self.path("c.json"), {
            body: "We grew 12 percent.",
            notes: "Next, we'll build on this.",
        }))
        result = Presentation(self.path("deck-humanized.pptx"))
        s = result.slides[0]
        self.assertEqual(s.shapes.title.text, "Q3 results")
        self.assertEqual(s.placeholders[1].text, "We grew 12 percent.")
        self.assertEqual(s.notes_slide.notes_text_frame.text, "Next, we'll build on this.")


def make_pdf(path):
    """Two-page PDF: page 1 has text, page 2 has none (like a scan)."""
    try:
        from reportlab.pdfgen import canvas
        c = canvas.Canvas(path)
        c.drawString(72, 750, "Dear Mr Sharma, the meeting on 14 February is confirmed.")
        c.drawString(72, 730, "Please bring the signed agreement and two photographs.")
        c.showPage()
        c.showPage()
        c.save()
        return True
    except ImportError:
        pass
    # Build a minimal PDF by hand with the standard library.
    text = b"BT /F1 12 Tf 72 750 Td (Dear Mr Sharma, the meeting on 14 February is confirmed.) Tj ET"
    objs = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R 4 0 R] /Count 2 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 5 0 R /Resources << /Font << /F1 6 0 R >> >> >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>",
        b"<< /Length %d >>\nstream\n" % len(text) + text + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    out = b"%PDF-1.4\n"
    offsets = []
    for i, body in enumerate(objs, 1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % i + body + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    for off in offsets:
        out += b"%010d 00000 n \n" % off
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, xref)
    with open(path, "wb") as fh:
        fh.write(out)
    return True


@unittest.skipUnless(HAVE_PYPDF and HAVE_DOCX, "pypdf or python-docx is not installed")
class PdfExtractTest(TempDirCase):
    def test_extract_and_to_docx(self):
        from docx import Document
        src = self.path("letter.pdf")
        make_pdf(src)
        out = self.path("pages.json")
        run("pdf_extract.py", "extract", src, "-o", out)
        with open(out, encoding="utf-8") as fh:
            data = json.load(fh)
        self.assertEqual(len(data["pages"]), 2)
        self.assertIn("14 February", data["pages"][0]["text"])
        self.assertEqual(data["scanned_pages"], [2])

        data["pages"][0]["text"] = "Dear Mr Sharma,\n\nYour meeting on 14 February is confirmed."
        run("pdf_extract.py", "to-docx", src, write_json(self.path("new.json"), data))
        doc = Document(self.path("letter-humanized.docx"))
        self.assertIn("Your meeting on 14 February is confirmed.", [p.text for p in doc.paragraphs])
        self.assertTrue(os.path.exists(src))


class WordCountTest(TempDirCase):
    def test_counts(self):
        proc = run("word_count.py", "--json", "--text", "Thanks for the update, see you Monday. - ...")
        data = json.loads(proc.stdout)
        self.assertEqual(data["words"], 7)

    def test_target_exit_codes(self):
        run("word_count.py", "--text", "one two three four five six seven eight nine ten", "--target", "10")
        run("word_count.py", "--text", "one two three", "--target", "10", expect=2)

    def test_hindi(self):
        proc = run("word_count.py", "--json", "--text", "मैं कल सुबह आऊँगा।")
        self.assertEqual(json.loads(proc.stdout)["words"], 4)

    def test_readability(self):
        proc = run("word_count.py", "--json", "--readability", "--text",
                   "The cat sat on the mat. It was warm. We went home after lunch.")
        rd = json.loads(proc.stdout)["readability"]
        self.assertTrue(rd["supported"])
        self.assertGreater(rd["flesch_reading_ease"], 80)
        hard = run("word_count.py", "--json", "--readability", "--text",
                   "Notwithstanding the aforementioned considerations, organizational "
                   "transformation necessitates comprehensive institutional realignment.")
        self.assertLess(json.loads(hard.stdout)["readability"]["flesch_reading_ease"], 30)
        other = run("word_count.py", "--json", "--readability", "--text", "मैं कल सुबह आऊँगा।")
        self.assertFalse(json.loads(other.stdout)["readability"]["supported"])


SRT = """1
00:00:01,000 --> 00:00:03,500
Hello everyone, and welcome
to our journey of discovery.

2
00:00:03,600 --> 00:00:06,000
Today we will dive deep into budgets.
"""


class SrtRewriteTest(TempDirCase):
    def test_timings_kept(self):
        src = self.path("talk.srt")
        with open(src, "w", encoding="utf-8") as fh:
            fh.write(SRT)
        out = self.path("cues.json")
        run("srt_rewrite.py", "extract", src, "-o", out)
        with open(out, encoding="utf-8") as fh:
            data = json.load(fh)
        self.assertEqual(len(data["cues"]), 2)
        self.assertEqual(data["cues"][0]["timing"], "00:00:01,000 --> 00:00:03,500")
        run("srt_rewrite.py", "apply", src, write_json(self.path("c.json"), {
            "1": "Hello everyone,\nthanks for coming.",
            "2": "Today we'll look at budgets.",
        }))
        with open(self.path("talk-humanized.srt"), encoding="utf-8") as fh:
            result = fh.read()
        self.assertIn("1\n00:00:01,000 --> 00:00:03,500\nHello everyone,\nthanks for coming.", result)
        self.assertIn("2\n00:00:03,600 --> 00:00:06,000\nToday we'll look at budgets.", result)

    def test_keeps_bom_and_windows_line_endings(self):
        src = self.path("talk.srt")
        with open(src, "wb") as fh:
            fh.write(b"\xef\xbb\xbf" + SRT.replace("\n", "\r\n").encode("utf-8"))
        run("srt_rewrite.py", "apply", src, write_json(self.path("c.json"), {"1": "Hello all."}))
        with open(self.path("talk-humanized.srt"), "rb") as fh:
            raw = fh.read()
        self.assertTrue(raw.startswith(b"\xef\xbb\xbf1\r\n"))
        self.assertIn(b"Hello all.\r\n", raw)
        self.assertNotIn(b"\n", raw.replace(b"\r\n", b""))

    def test_rejects_timing_change(self):
        src = self.path("talk.srt")
        with open(src, "w", encoding="utf-8") as fh:
            fh.write(SRT)
        changes = write_json(self.path("c.json"), {"cues": [
            {"id": "1", "timing": "00:00:02,000 --> 00:00:03,500", "text": "Hi"}]})
        proc = run("srt_rewrite.py", "apply", src, changes, expect=None)
        self.assertNotEqual(proc.returncode, 0)
        self.assertFalse(os.path.exists(self.path("talk-humanized.srt")))

    def test_refuses_overwrite(self):
        src = self.path("talk.srt")
        with open(src, "w", encoding="utf-8") as fh:
            fh.write(SRT)
        proc = run("srt_rewrite.py", "apply", src, write_json(self.path("c.json"), {}), "-o", src, expect=None)
        self.assertNotEqual(proc.returncode, 0)


@unittest.skipUnless(HAVE_DOCX, "python-docx is not installed")
class ChangeReportTest(TempDirCase):
    def test_report(self):
        from docx import Document
        before = self.path("before.txt")
        after = self.path("after.txt")
        with open(before, "w", encoding="utf-8") as fh:
            fh.write("We utilized the new process.\n\nThe office is closed on Monday.\n")
        with open(after, "w", encoding="utf-8") as fh:
            fh.write("We used the new process.\n\nThe office is closed on Monday.\n")
        run("change_report.py", before, after, "-o", self.path("changes.docx"))
        doc = Document(self.path("changes.docx"))
        struck = [r.text for p in doc.paragraphs for r in p.runs if r.font.strike]
        under = [r.text for p in doc.paragraphs for r in p.runs if r.font.underline]
        self.assertIn("utilized", struck)
        self.assertIn("used", under)
        self.assertIn("The office is closed on Monday.", [p.text for p in doc.paragraphs])

    def test_refuses_overwrite(self):
        before = self.path("before.txt")
        with open(before, "w", encoding="utf-8") as fh:
            fh.write("Hello.\n")
        proc = run("change_report.py", before, before, "-o", before, expect=None)
        self.assertNotEqual(proc.returncode, 0)


CHAT_ANDROID = """12/03/24, 9:15 pm - Messages and calls are end-to-end encrypted.
12/03/24, 9:15 pm - Asha: Reached home, will call you tmrw
12/03/24, 9:16 pm - Vikram: ok
12/03/24, 9:17 pm - Asha: <Media omitted>
12/03/24, 9:18 pm - Asha: my new number is +91 98765 43210, mail me at asha@example.com
also check https://example.com/menu
12/03/24, 9:19 pm - Asha: This message was deleted
12/03/24, 9:20 pm - Vikram added Priya
"""

CHAT_IPHONE = """[12/03/24, 9:15:02 PM] Asha: Running 10 min late, sorry!!
[12/03/24, 9:16:10 PM] Vikram: no worries
[12/03/24, 9:17:00 PM] Asha: ‎image omitted
"""


class ChatExportFilterTest(TempDirCase):
    def write(self, name, text):
        path = self.path(name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        return path

    def test_list_senders(self):
        src = self.write("chat.txt", CHAT_ANDROID)
        out = run("chat_export_filter.py", src, "--list-senders").stdout
        self.assertIn("Asha", out)
        self.assertIn("Vikram", out)
        self.assertNotIn("Priya", out)

    def test_android_filter_and_redact(self):
        src = self.write("chat.txt", CHAT_ANDROID)
        out = run("chat_export_filter.py", src, "--sender", "asha").stdout
        self.assertIn("Reached home, will call you tmrw", out)
        self.assertNotIn("ok\n", out.split("tmrw")[0])
        self.assertNotIn("Vikram", out)
        self.assertNotIn("Media omitted", out)
        self.assertNotIn("deleted", out)
        self.assertNotIn("98765", out)
        self.assertNotIn("asha@example.com", out)
        self.assertNotIn("https://", out)
        self.assertIn("[phone]", out)
        self.assertIn("[email]", out)
        self.assertIn("[link]", out)

    def test_iphone_format(self):
        src = self.write("chat.txt", CHAT_IPHONE)
        out = run("chat_export_filter.py", src, "--sender", "Asha").stdout
        self.assertIn("Running 10 min late, sorry!!", out)
        self.assertNotIn("omitted", out)
        self.assertNotIn("no worries", out)

    def test_max(self):
        src = self.write("chat.txt", CHAT_ANDROID)
        out = run("chat_export_filter.py", src, "--sender", "Asha", "--max", "1").stdout
        self.assertNotIn("Reached home", out)
        self.assertIn("[phone]", out)


HTML = """<!DOCTYPE html>
<html><head><title>Sunrise Bakery</title>
<style>p { color: red; }</style>
<script>var s = "<p>Hidden</p>";</script></head>
<body>
  <!-- keep this comment -->
  <h1 class="big">Welcome to our bakery!</h1>
  <p>We are thrilled to offer <a href="/menu?a=1&amp;b=2">our menu</a> &amp; cakes from Rs 450.<br>Call 98765 43210.</p>
  <pre>  spaced   code  </pre><code>x = 1</code>
  <img src="cake.png" alt="cake">
</body></html>
"""


class HtmlRewriteTest(TempDirCase):
    def setUp(self):
        super().setUp()
        self.src = self.path("page.html")
        with open(self.src, "w", encoding="utf-8") as fh:
            fh.write(HTML)

    def nodes(self):
        proc = run("html_rewrite.py", "extract", self.src)
        return {n["text"]: n["id"] for n in json.loads(proc.stdout)["nodes"]}

    def test_skips_script_style_and_code(self):
        texts = self.nodes()
        self.assertIn("Welcome to our bakery!", texts)
        self.assertIn("& cakes from Rs 450.", texts)
        for hidden in ("Hidden", "spaced   code", "x = 1", "p { color: red; }"):
            self.assertFalse(any(hidden in t for t in texts), hidden)

    def test_markup_untouched(self):
        ids = self.nodes()
        changes = write_json(self.path("c.json"), {
            ids["We are thrilled to offer"]: "We bake every morning. See",
        })
        run("html_rewrite.py", "apply", self.src, changes)
        with open(self.path("page-humanized.html"), encoding="utf-8") as fh:
            result = fh.read()
        expected = HTML.replace("We are thrilled to offer", "We bake every morning. See")
        self.assertEqual(result, expected)

    def test_number_change_flagged(self):
        ids = self.nodes()
        changes = write_json(self.path("c.json"), {ids["& cakes from Rs 450."]: "& cakes from Rs 500."})
        proc = run("html_rewrite.py", "apply", self.src, changes)
        self.assertIn("CHECK", proc.stdout)
        with open(self.path("page-humanized.html"), encoding="utf-8") as fh:
            self.assertIn("&amp; cakes from Rs 500.", fh.read())

    def test_refuses_overwrite(self):
        proc = run("html_rewrite.py", "apply", self.src, write_json(self.path("c.json"), {}),
                   "-o", self.src, expect=None)
        self.assertNotEqual(proc.returncode, 0)
        with open(self.src, encoding="utf-8") as fh:
            self.assertEqual(fh.read(), HTML)


ATTR_HTML = (
    '<html><head><meta name="description" content="We harness synergies to bake bread.">'
    "<meta property='og:description' content='Bread &amp; cakes'></head>"
    '<body><img src="a.jpg" alt="A delightful image of bread"><input placeholder=Search>'
    "<p title='Opening hours'>Open daily.</p><code><img alt=\"skip me\"></code></body></html>"
)


class HtmlAttributesTest(TempDirCase):
    def setUp(self):
        super().setUp()
        self.src = self.path("attrs.html")
        with open(self.src, "w", encoding="utf-8") as fh:
            fh.write(ATTR_HTML)

    def test_default_extract_has_no_attributes(self):
        nodes = json.loads(run("html_rewrite.py", "extract", self.src).stdout)["nodes"]
        self.assertEqual([n["id"] for n in nodes], ["t1"])

    def test_attributes_listed_and_code_skipped(self):
        nodes = json.loads(run("html_rewrite.py", "extract", self.src, "--attributes").stdout)["nodes"]
        tags = {n["tag"]: n["text"] for n in nodes if n["id"].startswith("attr-")}
        self.assertEqual(tags["img@alt"], "A delightful image of bread")
        self.assertEqual(tags["input@placeholder"], "Search")
        self.assertEqual(tags["p@title"], "Opening hours")
        self.assertIn("Bread & cakes", [n["text"] for n in nodes])
        self.assertFalse(any(n["text"] == "skip me" for n in nodes))

    def test_attributes_updated_and_quoting_kept(self):
        nodes = json.loads(run("html_rewrite.py", "extract", self.src, "--attributes").stdout)["nodes"]
        ids = {n["text"]: n["id"] for n in nodes}
        changes = write_json(self.path("c.json"), {
            ids["We harness synergies to bake bread."]: "We bake bread every morning.",
            ids["Bread & cakes"]: 'Bread & "fresh" cakes',
            ids["A delightful image of bread"]: "Loaves of bread on a table",
            ids["Search"]: "Search the menu",
            ids["Opening hours"]: "When we're open",
        })
        run("html_rewrite.py", "apply", self.src, changes)
        with open(self.path("attrs-humanized.html"), encoding="utf-8") as fh:
            result = fh.read()
        self.assertIn('content="We bake bread every morning."', result)
        self.assertIn("content='Bread &amp; \"fresh\" cakes'", result)
        self.assertIn('alt="Loaves of bread on a table"', result)
        self.assertIn('placeholder="Search the menu"', result)
        self.assertIn("title='When we&#39;re open'", result)
        self.assertIn('<code><img alt="skip me"></code>', result)
        self.assertIn("<p title=", result)
        self.assertIn(">Open daily.</p>", result)


def make_letter_pdf(path):
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(path)
    y = 760
    for text, gap in [
        ("Dear Mr Sharma,", 28),
        ("Thank you for your letter about the water supply in our build-", 14),
        ("ing. We have checked the tank and the pipes, and it is now fixed.", 28),
        ("Please note:", 16),
        ("1. Keep the main valve open at all times during the day.", 14),
        ("2. Call the office if the water pressure drops again.", 28),
        ("Yours sincerely,", 14),
        ("Anita Rao", 14),
    ]:
        c.drawString(72, y, text)
        y -= gap
    c.save()


try:
    import reportlab  # noqa: F401
    HAVE_REPORTLAB = True
except ImportError:
    HAVE_REPORTLAB = False


@unittest.skipUnless(HAVE_PYPDF and HAVE_REPORTLAB, "pypdf or reportlab is not installed")
class PdfParagraphTest(TempDirCase):
    def paragraphs(self):
        src = self.path("letter.pdf")
        make_letter_pdf(src)
        data = json.loads(run("pdf_extract.py", "extract", src).stdout)
        return data["pages"][0]["text"].split("\n\n")

    def test_salutation_on_its_own(self):
        paras = self.paragraphs()
        self.assertEqual(paras[0], "Dear Mr Sharma,")
        self.assertTrue(paras[1].startswith("Thank you for your letter"))

    def test_hyphen_joined_and_lines_merged(self):
        paras = self.paragraphs()
        self.assertIn("in our building. We have checked", paras[1])

    def test_numbered_items_kept_apart(self):
        text = "\n\n".join(self.paragraphs())
        self.assertIn("1. Keep the main valve open at all times during the day.\n2. Call the office", text)
        self.assertIn("Yours sincerely,", self.paragraphs())


class TidyTextOnlyTest(unittest.TestCase):
    def test_text_only_fallback(self):
        sys.path.insert(0, SCRIPTS)
        try:
            import pdf_extract
        finally:
            sys.path.pop(0)
        text = ("Dear Ms Iyer,\nThe parcel reached us on 3 May and we have sent a\n"
                "replacement today.\n- Order 4471\n- Courier: BlueDart")
        out = pdf_extract.tidy(text)
        self.assertEqual(out.split("\n\n")[0], "Dear Ms Iyer,")
        self.assertIn("we have sent a replacement today.", out)
        self.assertIn("- Order 4471\n- Courier: BlueDart", out)


class DateCheckTest(unittest.TestCase):
    def check(self, text, *args, expect=None):
        proc = run("date_check.py", "--json", "--today", "2026-11-07", "--text", text, *args, expect=expect)
        return proc, json.loads(proc.stdout)

    def test_match(self):
        proc, data = self.check("Party on Saturday 14 March 2026.", expect=0)
        self.assertEqual(data["to_fix"], 0)
        self.assertTrue(data["dates"][0]["ok"])

    def test_impossible_dates_without_weekday(self):
        proc, data = self.check("Due 31 April 2026, or 29 Feb 2027. Version 3.14, Feb 29 is fine.", expect=1)
        self.assertEqual([d["text"] for d in data["dates"]], ["31 April 2026", "29 Feb 2027"])
        self.assertTrue(all(not d["ok"] for d in data["dates"]))

    def test_mismatch(self):
        proc, data = self.check("Meeting: Mon, 14/03/2026 at 10.30.", expect=1)
        item = data["dates"][0]
        self.assertFalse(item["ok"])
        self.assertEqual(item["actual_weekday"], "Saturday")
        self.assertEqual(item["stated_weekday"], "Monday")

    def test_weekday_after_date(self):
        proc, data = self.check("Due 14 March 2026 (Tuesday).", expect=1)
        self.assertEqual(data["dates"][0]["actual_weekday"], "Saturday")

    def test_no_year_assumed(self):
        proc, data = self.check("See you Monday 9 Nov.", expect=0)
        self.assertEqual(data["dates"][0]["year_assumed"], 2026)
        proc, data = self.check("Monday 9 Nov", "--year", "2027", expect=1)
        self.assertEqual(data["dates"][0]["year_assumed"], 2027)
        proc, data = self.check("Friday 6 Nov", expect=None)
        self.assertEqual(data["dates"][0]["year_assumed"], 2027)

    def test_us_order(self):
        self.check("Saturday 03/14/2026", "--us", expect=0)
        proc, data = self.check("Saturday 03/14/2026", expect=1)
        self.assertIn("problem", data["dates"][0])

    def test_no_dates(self):
        proc, data = self.check("Nothing to check here, see you soon.", expect=0)
        self.assertEqual(data["dates"], [])


class WordCountSpeechTest(unittest.TestCase):
    def test_speech_sections(self):
        text = " ".join(["word"] * 95) + "\n\n" + " ".join(["word"] * 200)
        proc = run("word_count.py", "--speech", "--text", text)
        self.assertIn("Section 1: 95 words, about 45 seconds", proc.stdout)
        self.assertIn("Section 2: 200 words, about 1 minute 30 seconds", proc.stdout)
        data = json.loads(run("word_count.py", "--json", "--speech", "--wpm", "100", "--text", text).stdout)
        self.assertEqual(data["speech"]["wpm"], 100)
        self.assertEqual(data["speech"]["total_seconds"], 175)
        self.assertEqual(len(data["speech"]["sections"]), 2)


def make_png(path, w=20, h=10):
    """A tiny solid-colour PNG, written with the standard library only."""
    import struct
    import zlib
    raw = b"".join(b"\x00" + bytes([200, 60, 40]) * w for _ in range(h))

    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    with open(path, "wb") as fh:
        fh.write(b"\x89PNG\r\n\x1a\n"
                 + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
                 + chunk(b"IDAT", zlib.compress(raw))
                 + chunk(b"IEND", b""))
    return path


@unittest.skipUnless(HAVE_PYPDF and HAVE_REPORTLAB, "pypdf or reportlab is not installed")
class FormFillTest(TempDirCase):
    def make_form(self):
        from reportlab.pdfgen import canvas
        path = self.path("form.pdf")
        c = canvas.Canvas(path)
        c.drawString(72, 760, "Full name:")
        c.acroForm.textfield(name="full_name", x=160, y=750, width=200, height=20, tooltip="Full name")
        c.acroForm.textfield(name="city", x=160, y=720, width=200, height=20)
        c.acroForm.checkbox(name="agree", x=160, y=690, size=16)
        c.save()
        return path

    def fields(self, path):
        out = run("form_fill.py", "fields", path).stdout
        return {f["name"]: f for f in json.loads(out)["fields"]}

    def test_lists_fields_with_types_and_options(self):
        fields = self.fields(self.make_form())
        self.assertEqual(fields["full_name"]["type"], "text")
        self.assertEqual(fields["full_name"]["label"], "Full name")
        self.assertEqual(fields["agree"]["type"], "checkbox")
        self.assertIn("/Yes", fields["agree"]["options"])

    def test_fill_writes_a_copy_and_reports_blanks(self):
        src = self.make_form()
        values = write_json(self.path("v.json"), {"full_name": "Asha Verma", "agree": "/Yes", "missing": "x"})
        out = run("form_fill.py", "fill", src, values).stdout
        self.assertIn("SKIP", out)
        self.assertIn("STILL BLANK: city", out)
        filled = self.path("form-filled.pdf")
        self.assertTrue(os.path.exists(filled))
        fields = self.fields(filled)
        self.assertEqual(fields["full_name"]["value"], "Asha Verma")
        self.assertEqual(fields["agree"]["value"], "/Yes")
        self.assertEqual(fields["city"]["value"], "")
        self.assertEqual(self.fields(src)["full_name"]["value"], "")
        from pypdf import PdfReader
        self.assertTrue(PdfReader(filled).trailer["/Root"]["/AcroForm"]["/NeedAppearances"])

    def test_refuses_to_overwrite_and_bad_checkbox_value(self):
        src = self.make_form()
        values = write_json(self.path("v.json"), {"full_name": "Asha"})
        proc = run("form_fill.py", "fill", src, values, "-o", src, expect=None)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("overwrite", proc.stdout + proc.stderr)
        bad = write_json(self.path("bad.json"), {"agree": "maybe"})
        proc = run("form_fill.py", "fill", src, bad, expect=None)
        self.assertNotEqual(proc.returncode, 0)


@unittest.skipUnless(HAVE_PYPDF and HAVE_REPORTLAB, "pypdf or reportlab is not installed")
class PdfImagesTest(TempDirCase):
    def test_saves_images_and_flags_pages_without_one(self):
        from reportlab.pdfgen import canvas
        png = make_png(self.path("p.png"))
        src = self.path("scan.pdf")
        c = canvas.Canvas(src)
        c.drawString(72, 760, "Page one has words only.")
        c.showPage()
        c.drawImage(png, 72, 500, width=200, height=100)
        c.save()
        out_dir = self.path("imgs")
        out = run("pdf_extract.py", "images", src, "--pages", "1,2", "--out", out_dir).stdout
        self.assertIn("PAGE 1: no picture", out)
        saved = os.listdir(out_dir)
        self.assertEqual(len(saved), 1)
        self.assertTrue(saved[0].startswith("scan-page2-"))
        proc = run("pdf_extract.py", "images", src, "--pages", "9", expect=None)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("out of range", proc.stdout + proc.stderr)


class MailMergeTest(TempDirCase):
    def setUp(self):
        super().setUp()
        self.sheet = self.path("guests.csv")
        with open(self.sheet, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["Name", "City"])
            w.writerow(["Lakshmi", "Madurai"])
            w.writerow(["Karthik", ""])
        self.template = self.path("msg.txt")
        with open(self.template, "w", encoding="utf-8") as fh:
            fh.write("Happy Pongal, {name}! Love to everyone in {City}.")

    def test_columns(self):
        out = run("mail_merge.py", "columns", self.sheet).stdout
        self.assertIn("Name, City", out)
        self.assertIn("Rows: 2", out)

    def test_txt_output_and_missing_values_reported(self):
        out = run("mail_merge.py", "merge", self.sheet, self.template).stdout
        self.assertIn("Nothing was sent", out)
        self.assertIn("row 3 (Karthik): no value for {City}", out)
        with open(self.path("guests-messages.txt"), encoding="utf-8") as fh:
            text = fh.read()
        self.assertIn("Happy Pongal, Lakshmi! Love to everyone in Madurai.", text)
        self.assertIn("Happy Pongal, Karthik! Love to everyone in {City}.", text)

    def test_doubled_braces_are_literal(self):
        with open(self.template, "w", encoding="utf-8") as fh:
            fh.write("Hi {Name}, use code {{SAVE10}} at checkout.")
        run("mail_merge.py", "merge", self.sheet, self.template)
        with open(self.path("guests-messages.txt"), encoding="utf-8") as fh:
            text = fh.read()
        self.assertIn("Hi Lakshmi, use code {SAVE10} at checkout.", text)

    def test_csv_output_keeps_columns(self):
        out = self.path("result.csv")
        run("mail_merge.py", "merge", self.sheet, self.template, "--out", out)
        with open(out, newline="", encoding="utf-8") as fh:
            rows = list(csv.reader(fh))
        self.assertEqual(rows[0], ["Name", "City", "Message"])
        self.assertEqual(rows[1][:2], ["Lakshmi", "Madurai"])
        self.assertTrue(rows[1][2].startswith("Happy Pongal, Lakshmi!"))

    @unittest.skipUnless(HAVE_XLSX and HAVE_DOCX, "openpyxl or python-docx is not installed")
    def test_xlsx_in_docx_out(self):
        import openpyxl
        import docx
        book = self.path("guests.xlsx")
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["Name", "City"])
        ws.append(["Lakshmi", "Madurai"])
        wb.save(book)
        out = self.path("result.docx")
        run("mail_merge.py", "merge", book, self.template, "--out", out)
        paras = [p.text for p in docx.Document(out).paragraphs]
        self.assertIn("Lakshmi", paras)
        self.assertIn("Happy Pongal, Lakshmi! Love to everyone in Madurai.", paras)

    def test_unknown_placeholder_and_overwrite_refused(self):
        bad = self.path("bad.txt")
        with open(bad, "w", encoding="utf-8") as fh:
            fh.write("Hi {Nickname}")
        proc = run("mail_merge.py", "merge", self.sheet, bad, expect=None)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("{nickname}", proc.stdout + proc.stderr)
        proc = run("mail_merge.py", "merge", self.sheet, self.template, "--out", self.sheet, expect=None)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("overwrite", proc.stdout + proc.stderr)


@unittest.skipUnless(HAVE_DOCX, "python-docx is not installed")
class DocSectionsTest(TempDirCase):
    def make_docx(self):
        d = docx.Document()
        d.add_heading("Field notes", 0)
        d.add_paragraph("Notes from the Lakeside Survey about colour use.")
        d.add_heading("Chapter 1 Background", 1)
        d.add_paragraph("The Lakeside Survey began in 2019. We study color in signs.")
        d.add_paragraph("The Lakeside Survey team used e-mail and email both.")
        d.add_heading("Chapter 2 Method", 1)
        d.add_paragraph("We visited 40 shops.")
        path = self.path("notes.docx")
        d.save(path)
        return path

    def test_outline_docx_uses_headings_and_paragraph_ids(self):
        out = json.loads(run("doc_sections.py", "outline", self.make_docx(), "--json").stdout)
        heads = [s["heading"] for s in out["sections"]]
        self.assertEqual(heads, ["Field notes", "Chapter 1 Background", "Chapter 2 Method"])
        self.assertEqual(out["unit"], "paragraph ids")
        seg_ids = [s["id"] for s in json.loads(run("docx_rewrite.py", "extract", self.make_docx()).stdout)["segments"]]
        ids = [pid for s in out["sections"] for pid in s["paragraph_ids"]]
        self.assertEqual(ids, seg_ids, "section paragraph ids match docx_rewrite ids")

    def test_outline_markdown_and_plain_text(self):
        md = self.path("a.md")
        with open(md, "w", encoding="utf-8") as fh:
            fh.write("# One\nsome words here\n\n```\n# not a heading\n```\n## Two\nmore words\n")
        out = json.loads(run("doc_sections.py", "outline", md, "--json").stdout)
        self.assertEqual([s["heading"] for s in out["sections"]], ["One", "Two"])
        txt = self.path("b.txt")
        with open(txt, "w", encoding="utf-8") as fh:
            fh.write(("word " * 500 + "\n\n") * 4)
        out = json.loads(run("doc_sections.py", "outline", txt, "--words", "900", "--json").stdout)
        self.assertEqual(len(out["sections"]), 2)
        self.assertEqual(out["sections"][0]["range"], "lines 1 to 3")

    def test_terms_skip_words_only_capitalised_at_sentence_start(self):
        txt = self.path("t.txt")
        with open(txt, "w", encoding="utf-8") as fh:
            fh.write("Final words here. Final checks done. Final notes. "
                     "The Northbay Project began. We met at the Northbay Project. "
                     "Northbay Project ended. We saw Priya. Then Priya left, and then we ate. "
                     "Ask Priya, or ask Ravi.\n")
        out = json.loads(run("doc_sections.py", "terms", txt, "--json").stdout)
        found = {t["term"] for t in out["terms"]}
        self.assertIn("Northbay Project", found)
        self.assertIn("Priya", found)
        self.assertNotIn("Final", found)

    def test_outline_latex(self):
        tex = self.path("thesis.tex")
        with open(tex, "w", encoding="utf-8") as fh:
            fh.write("\\documentclass{report}\n\\title{Preamble words}\n\\begin{document}\n"
                     "\\chapter{Introduction}\nThis chapter sets out the question.\n"
                     "% \\section{Commented out}\n\\section[Short]{Background}\nMore prose here.\n"
                     "\\chapter*{Results}\nThe results were clear.\n\\end{document}\n")
        out = json.loads(run("doc_sections.py", "outline", tex, "--json").stdout)
        self.assertEqual([(s["heading"], s["level"]) for s in out["sections"]],
                         [("Introduction", 1), ("Background", 2), ("Results", 1)])
        self.assertEqual(out["sections"][0]["range"], "lines 4 to 6")

    def test_terms_finds_names_and_spelling_variants(self):
        out = json.loads(run("doc_sections.py", "terms", self.make_docx(), "--min", "2", "--json").stdout)
        terms = {t["term"]: t["count"] for t in out["terms"]}
        self.assertEqual(terms.get("Lakeside Survey"), 3)
        pairs = [set(v["spellings"]) for v in out["variants"]]
        self.assertIn({"colour", "color"}, pairs)
        self.assertIn({"e-mail", "email"}, pairs)


@unittest.skipUnless(HAVE_DOCX, "python-docx is not installed")
class DocxLayoutTest(TempDirCase):
    def make(self):
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from docx.shared import Pt
        d = docx.Document()
        d.add_heading("Notice", 1)
        p = d.add_paragraph("A justified paragraph. ")
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = p.add_run("This italic part has many more than ten words so the italics should go away now.")
        r.italic = True
        r2 = p.add_run(" Short Title")
        r2.italic = True
        small = d.add_paragraph("Small print")
        small.runs[0].font.size = Pt(9)
        path = self.path("lay.docx")
        d.save(path)
        return path

    def test_layout_changes_formatting_not_words(self):
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        src = self.make()
        run("docx_layout.py", src, "--dyslexia")
        out = docx.Document(self.path("lay-readable.docx"))
        self.assertEqual([p.text for p in docx.Document(src).paragraphs], [p.text for p in out.paragraphs])
        body = out.paragraphs[1]
        self.assertEqual(body.alignment, WD_ALIGN_PARAGRAPH.LEFT)
        self.assertEqual(body.paragraph_format.line_spacing, 1.5)
        self.assertEqual([r.font.name for r in body.runs], ["Arial"] * 3)
        self.assertFalse(body.runs[1].italic, "long italics removed")
        self.assertTrue(body.runs[2].italic, "short italics kept")
        self.assertEqual(out.paragraphs[2].runs[0].font.size.pt, 12)
        self.assertEqual(out.paragraphs[0].style.name, "Heading 1")

    def test_refuses_to_overwrite(self):
        src = self.make()
        proc = run("docx_layout.py", src, "--dyslexia", "-o", src, expect=1)
        self.assertIn("overwrite", proc.stdout + proc.stderr)


class ChatExportFormatsTest(TempDirCase):
    def test_telegram_json(self):
        path = self.path("result.json")
        write_json(path, {"name": "Family", "messages": [
            {"id": 1, "type": "service", "actor": "Asha", "text": ""},
            {"id": 2, "type": "message", "from": "Asha", "text": "Reaching by 7, call +91 98765 43210"},
            {"id": 3, "type": "message", "from": "Ravi", "text": "ok"},
            {"id": 4, "type": "message", "from": "Asha", "text": ["See ", {"type": "link", "text": "https://example.com"}, " first"]},
        ]})
        proc = run("chat_export_filter.py", path, "--sender", "asha")
        self.assertIn("Telegram", proc.stderr)
        self.assertEqual(proc.stdout.strip().split("\n\n"), ["Reaching by 7, call [phone]", "See [link] first"])

    def test_signal_text(self):
        path = self.path("signal.txt")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("[2026-03-12 09:15] Asha: Leaving now\n[2026-03-12 09:16] Ravi: ok\n"
                     "[2026-03-12 09:17] Asha: [Attachment: image/jpeg]\n"
                     "[2026-03-12 09:18] Asha: Mail asha@example.com\nsecond line\n")
        proc = run("chat_export_filter.py", path, "--sender", "Asha")
        self.assertIn("Signal", proc.stderr)
        self.assertEqual(proc.stdout.strip().split("\n\n"), ["Leaving now", "Mail [email]\nsecond line"])
        listed = run("chat_export_filter.py", path, "--list-senders").stdout
        self.assertIn("Ravi", listed)

    def test_whatsapp_still_detected(self):
        path = self.path("wa.txt")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("12/03/24, 9:15 pm - Asha: Hello there\n")
        proc = run("chat_export_filter.py", path, "--sender", "Asha")
        self.assertIn("WhatsApp", proc.stderr)
        self.assertEqual(proc.stdout.strip(), "Hello there")


LATEX_SAMPLE = r"""\documentclass{article}
\title{Preamble title stays}
\begin{document}
\section{Introduction}
It is important to note that our method works well. % keep this comment
We show that $E = mc^2$ holds, as in \cite{lee2021} and Table~\ref{tab:one}.
\begin{equation}
  a^2 + b^2 = c^2 \label{eq:p}
\end{equation}
The results are \emph{very promising} and cost 50\% less.
\end{document}
"""


class LineEndingTest(TempDirCase):
    """Text formats keep a byte-order mark and Windows line endings."""

    def check(self, script, name, body, changes):
        src = self.path(name)
        with open(src, "wb") as fh:
            fh.write(b"\xef\xbb\xbf" + body.replace("\n", "\r\n").encode("utf-8"))
        same = self.path("same" + os.path.splitext(name)[1])
        run(script, "apply", src, write_json(self.path("none.json"), {}), "-o", same)
        with open(src, "rb") as a, open(same, "rb") as b:
            self.assertEqual(a.read(), b.read(), "a run with no changes must give the same bytes")
        out = self.path("out" + os.path.splitext(name)[1])
        run(script, "apply", src, write_json(self.path("c.json"), changes), "-o", out)
        with open(out, "rb") as fh:
            raw = fh.read()
        self.assertTrue(raw.startswith(b"\xef\xbb\xbf"))
        self.assertNotIn(b"\n", raw.replace(b"\r\n", b""))

    def test_latex(self):
        self.check("latex_rewrite.py", "w.tex",
                   "\\documentclass{article}\n\\begin{document}\nWe utilise it here.\n\\end{document}\n",
                   {"t1": "We use it here."})

    def test_html(self):
        self.check("html_rewrite.py", "w.html",
                   "<html>\n<body>\n<p>We make use of things.</p>\n</body></html>\n",
                   {"t1": "We use things."})


class LatexRewriteTest(TempDirCase):
    def setUp(self):
        super().setUp()
        self.src = self.path("paper.tex")
        with open(self.src, "w", encoding="utf-8", newline="") as fh:
            fh.write(LATEX_SAMPLE)

    def segments(self):
        return json.loads(run("latex_rewrite.py", "extract", self.src).stdout)["segments"]

    def test_extract_skips_maths_citations_and_preamble(self):
        texts = [s["text"] for s in self.segments()]
        joined = " | ".join(texts)
        self.assertIn("It is important to note that our method works well.", texts)
        self.assertIn("very promising", texts)
        self.assertIn("and cost 50\\% less.", texts)
        for hidden in ("Preamble title", "mc^2", "lee2021", "tab:one", "a^2", "eq:p", "keep this comment"):
            self.assertNotIn(hidden, joined)

    def test_apply_changes_only_prose(self):
        ids = {s["text"]: s["id"] for s in self.segments()}
        changes = write_json(self.path("c.json"), {ids["It is important to note that our method works well."]: "Our method works well."})
        run("latex_rewrite.py", "apply", self.src, changes)
        with open(self.path("paper-humanized.tex"), encoding="utf-8", newline="") as fh:
            out = fh.read()
        self.assertEqual(out, LATEX_SAMPLE.replace("It is important to note that our method works well.", "Our method works well."))

    def test_unsafe_change_is_skipped(self):
        ids = {s["text"]: s["id"] for s in self.segments()}
        changes = write_json(self.path("c.json"), {ids["very promising"]: "very {promising", ids["and cost 50\\% less."]: "and cost 50\\% less overall."})
        proc = run("latex_rewrite.py", "apply", self.src, changes, expect=2)
        self.assertIn("SKIPPED", proc.stdout)
        with open(self.path("paper-humanized.tex"), encoding="utf-8") as fh:
            out = fh.read()
        self.assertIn(r"\emph{very promising}", out)
        self.assertIn(r"and cost 50\% less overall.", out)

    def test_refuses_to_overwrite(self):
        changes = write_json(self.path("c.json"), {})
        proc = run("latex_rewrite.py", "apply", self.src, changes, "-o", self.src, expect=1)
        self.assertIn("overwrite", proc.stdout + proc.stderr)


# ------------------------------------------------- bug sweep: awkward input

W_NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
        'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" '
        'xmlns:v="urn:schemas-microsoft-com:vml" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"')

TEXT_BOX_PARA = (
    '<w:p %s><w:r><w:t xml:space="preserve">Before the box </w:t></w:r>'
    '<w:r><mc:AlternateContent><mc:Choice Requires="wps"><w:drawing><wp:anchor><a:graphic>'
    '<a:graphicData><wps:wsp><wps:txbx><w:txbxContent><w:p><w:r><w:t>Box text here</w:t></w:r>'
    '</w:p></w:txbxContent></wps:txbx></wps:wsp></a:graphicData></a:graphic></wp:anchor>'
    '</w:drawing></mc:Choice><mc:Fallback><w:pict><v:shape><v:textbox><w:txbxContent><w:p>'
    '<w:r><w:t>Box text here</w:t></w:r></w:p></w:txbxContent></v:textbox></v:shape></w:pict>'
    '</mc:Fallback></mc:AlternateContent></w:r>'
    '<w:r><w:t xml:space="preserve">and after it.</w:t></w:r></w:p>' % W_NS)

FIELD_PARA = (
    '<w:p %s><w:r><w:t xml:space="preserve">Updated on </w:t></w:r>'
    '<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText> DATE </w:instrText></w:r>'
    '<w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>10/11/2026</w:t></w:r>'
    '<w:r><w:fldChar w:fldCharType="end"/></w:r>'
    '<w:r><w:t xml:space="preserve"> by the team utilizing data.</w:t></w:r></w:p>' % W_NS)


def run_items(p_el):
    """(kind, text) for the text, tabs, breaks, and field marks of a paragraph."""
    from docx.oxml.ns import qn
    names = {qn("w:t"): "t", qn("w:delText"): "del", qn("w:tab"): "tab", qn("w:br"): "br",
             qn("w:fldChar"): "fld"}
    out = []
    for r in p_el.iter(qn("w:r")):
        for c in r:
            if c.tag in names:
                out.append((names[c.tag], c.text or ""))
            elif c.tag.endswith("}AlternateContent"):
                out.append(("box", ""))
    return out


@unittest.skipUnless(HAVE_DOCX, "python-docx is not installed")
class DocxAwkwardInputTest(TempDirCase):
    def make(self):
        from docx import Document
        from docx.oxml import parse_xml
        doc = Document()
        p = doc.add_paragraph()
        r = p.add_run("Asha Verma")
        r.add_break()
        r.add_text("12 Lake Road")
        r.add_tab()
        r.add_text("Pune 411001 utilized")
        body = doc.element.body
        body.insert(len(body) - 1, parse_xml(TEXT_BOX_PARA))
        body.insert(len(body) - 1, parse_xml(FIELD_PARA))
        path = self.path("odd.docx")
        doc.save(path)
        return path

    def segments(self, path):
        return json.loads(run("docx_rewrite.py", "extract", path).stdout)["segments"]

    def test_tabs_and_line_breaks_are_shown_and_kept(self):
        src = self.make()
        segs = self.segments(src)
        self.assertEqual(segs[0]["text"], "Asha Verma\n12 Lake Road\tPune 411001 utilized")
        changes = write_json(self.path("c.json"), {"p1": "Asha Verma\n12 Lake Road\tPune 411001 used"})
        for extra in ([], ["--track-changes"]):
            out = self.path("out%d.docx" % len(extra))
            run("docx_rewrite.py", "apply", src, changes, "-o", out, *extra)
            import docx as _docx
            p = _docx.Document(out).element.body[0]
            items = [i for i in run_items(p) if i[0] != "del"]
            self.assertEqual(items[:4], [("t", "Asha Verma"), ("br", ""), ("t", "12 Lake Road"), ("tab", "")])
            self.assertEqual("".join(t for _, t in items[4:]), "Pune 411001 used")
            self.assertEqual(self.segments(out)[0]["text"], "Asha Verma\n12 Lake Road\tPune 411001 used")

    def test_text_box_is_its_own_paragraph_and_not_touched(self):
        src = self.make()
        texts = [s["text"] for s in self.segments(src)]
        self.assertIn("Before the box and after it.", texts)
        self.assertEqual(texts.count("Box text here"), 1)
        pid = [s["id"] for s in self.segments(src) if s["text"].startswith("Before")][0]
        changes = write_json(self.path("c.json"), {pid: "Before the box, and then after it."})
        for extra in ([], ["--track-changes"]):
            out = self.path("box%d.docx" % len(extra))
            run("docx_rewrite.py", "apply", src, changes, "-o", out, *extra)
            texts = [s["text"] for s in self.segments(out)]
            self.assertIn("Before the box, and then after it.", texts)
            self.assertIn("Box text here", texts)
            import docx as _docx
            outer = [i for i in run_items(_docx.Document(out).element.body[1]) if i[0] in ("t", "box")]
            self.assertEqual([t for k, t in outer if k == "t"].count("Box text here"), 2,
                             "both copies of the text box keep their text")

    def test_tracked_changes_keep_a_field_in_place(self):
        src = self.make()
        pid = [s["id"] for s in self.segments(src) if s["text"].startswith("Updated")][0]
        changes = write_json(self.path("c.json"), {pid: "Updated on 10/11/2026 by the team using data."})
        out = self.path("fld.docx")
        run("docx_rewrite.py", "apply", src, changes, "-o", out, "--track-changes")
        import docx as _docx
        items = run_items(_docx.Document(out).element.body[2])
        kinds = [k for k, _ in items]
        # The date stays inside the field: begin, separate, the date, end.
        start = kinds.index("fld")
        self.assertEqual(items[start:start + 4], [("fld", ""), ("fld", ""), ("t", "10/11/2026"), ("fld", "")])
        self.assertEqual(items[0], ("t", "Updated on "))


@unittest.skipUnless(HAVE_PPTX, "python-pptx is not installed")
class PptxLineBreakTest(TempDirCase):
    def test_soft_line_break_kept(self):
        from pptx import Presentation
        prs = Presentation()
        slide = prs.slides.add_slide(prs.slide_layouts[0])
        p = slide.shapes.title.text_frame.paragraphs[0]
        p.text = "Quarterly Results"
        p.add_line_break()
        p.add_run().text = "FY 2025 utilized"
        src = self.path("deck.pptx")
        prs.save(src)
        segs = json.loads(run("pptx_rewrite.py", "extract", src).stdout)["segments"]
        self.assertEqual(segs[0]["text"], "Quarterly Results\nFY 2025 utilized")
        sid = segs[0]["id"]
        run("pptx_rewrite.py", "apply", src, write_json(self.path("c.json"), {sid: "Quarterly Results\nFY 2025 in review"}))
        title = Presentation(self.path("deck-humanized.pptx")).slides[0].shapes.title.text_frame
        self.assertEqual(title.paragraphs[0].text, "Quarterly Results\vFY 2025 in review")
        proc = run("pptx_rewrite.py", "apply", src, write_json(self.path("d.json"), {sid: "Quarterly Results FY 2025"}),
                   "-o", self.path("other.pptx"))
        self.assertIn("Left as it was", proc.stdout)
        title = Presentation(self.path("other.pptx")).slides[0].shapes.title.text_frame
        self.assertEqual(title.paragraphs[0].text, "Quarterly Results\vFY 2025 utilized")


@unittest.skipUnless(HAVE_DOCX, "python-docx is not installed")
class DocxLayoutLinksAndNestedTablesTest(TempDirCase):
    def test_link_text_and_nested_table_get_the_font(self):
        from docx.oxml import parse_xml
        from docx.shared import Pt
        d = docx.Document()
        p = d.add_paragraph("See ")
        p._p.append(parse_xml(
            '<w:hyperlink xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
            'w:anchor="top"><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>'
            '<w:sz w:val="18"/></w:rPr><w:t>our page</w:t></w:r></w:hyperlink>'))
        outer = d.add_table(rows=1, cols=1)
        inner = outer.cell(0, 0).add_table(rows=1, cols=1)
        inner.cell(0, 0).paragraphs[0].add_run("Nested cell").font.size = Pt(9)
        src = self.path("links.docx")
        d.save(src)
        run("docx_layout.py", src, "--dyslexia")
        out = docx.Document(self.path("links-readable.docx"))
        link_run = out.paragraphs[0].iter_inner_content()
        runs = []
        for item in link_run:
            runs.extend(item.runs if hasattr(item, "runs") else [item])
        self.assertEqual([r.text for r in runs], ["See ", "our page"])
        self.assertEqual(runs[1].font.name, "Arial")
        self.assertEqual(runs[1].font.size.pt, 12)
        cell_run = out.tables[0].cell(0, 0).tables[0].cell(0, 0).paragraphs[0].runs[0]
        self.assertEqual((cell_run.font.name, cell_run.font.size.pt), ("Arial", 12))


@unittest.skipUnless(HAVE_DOCX, "python-docx is not installed")
class ChangeReportControlCharsTest(TempDirCase):
    def test_form_feed_from_pdf_text(self):
        from docx import Document
        before, after = self.path("a.txt"), self.path("b.txt")
        with open(before, "w", encoding="utf-8") as fh:
            fh.write("End of page one.\n\x0cPage two starts\x0bhere.\x00\n")
        with open(after, "w", encoding="utf-8") as fh:
            fh.write("End of page one.\n\x0cPage two begins here.\n")
        run("change_report.py", before, after, "-o", self.path("r.docx"))
        paras = [p.text for p in Document(self.path("r.docx")).paragraphs]
        self.assertIn("End of page one.", paras)


class WordCountLineEndingTest(unittest.TestCase):
    def test_windows_line_endings_count_the_same_from_stdin(self):
        proc = subprocess.run([sys.executable, os.path.join(SCRIPTS, "word_count.py"), "--json"],
                              input=b"One two.\r\n\r\nThree four five.\r\n", capture_output=True)
        data = json.loads(proc.stdout.decode("utf-8"))
        self.assertEqual(data["characters"], 27)
        self.assertEqual(data["paragraphs"], 2)


class MailMergeAwkwardInputTest(TempDirCase):
    def template(self, text, bom=False):
        path = self.path("msg.txt")
        with open(path, "w", encoding="utf-8-sig" if bom else "utf-8") as fh:
            fh.write(text)
        return path

    @unittest.skipUnless(HAVE_XLSX, "openpyxl is not installed")
    def test_xlsx_dates_and_numbers_as_the_sheet_shows_them(self):
        import datetime
        import openpyxl
        book = self.path("dues.xlsx")
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["Name", "Amount", "Due", "Rate", "Joined", "Pin"])
        ws.append(["Kavya", 1200, datetime.datetime(2026, 11, 20), 0.15, datetime.datetime(2025, 1, 5), 501])
        ws["B2"].number_format = "#,##0"
        ws["C2"].number_format = "dd/mm/yyyy"
        ws["D2"].number_format = "0%"
        ws["E2"].number_format = "mm-dd-yy"  # Excel's default short date
        ws["F2"].number_format = "00000"
        ws.append(["Rohan", 1250.5, datetime.datetime(2026, 12, 1), 0.075, None, None])
        ws["C3"].number_format = "d mmm yyyy"
        ws["D3"].number_format = "0.0%"
        wb.save(book)
        tpl = self.template("{Name}: Rs {Amount} due {Due} ({Rate}), joined {Joined}, pin {Pin}")
        run("mail_merge.py", "merge", book, tpl)
        with open(self.path("dues-messages.txt"), encoding="utf-8") as fh:
            text = fh.read()
        self.assertIn("Kavya: Rs 1,200 due 20/11/2026 (15%), joined 2025-01-05, pin 00501", text)
        self.assertIn("Rohan: Rs 1250.5 due 1 Dec 2026 (7.5%), joined {Joined}, pin {Pin}", text)
        self.assertNotIn("00:00:00", text)

    def test_duplicate_headings_keep_both_columns(self):
        sheet = self.path("people.csv")
        with open(sheet, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["Name", "Phone", "Phone", ""])
            w.writerow(["Meera", "98765 43210", "Office", "note"])
        out = self.path("out.csv")
        run("mail_merge.py", "merge", sheet, self.template("Hi {Name}"), "--out", out)
        with open(out, newline="", encoding="utf-8") as fh:
            rows = list(csv.reader(fh))
        self.assertEqual(rows[0], ["Name", "Phone", "Phone", "", "Message"])
        self.assertEqual(rows[1], ["Meera", "98765 43210", "Office", "note", "Hi Meera"])
        proc = run("mail_merge.py", "merge", sheet, self.template("Call {Phone}"), expect=1)
        self.assertIn("More than one column is called {phone}", proc.stdout + proc.stderr)

    def test_row_numbers_count_blank_rows_and_bom_template(self):
        sheet = self.path("guests.csv")
        with open(sheet, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["Name", "City"])
            w.writerow(["", ""])
            w.writerow(["Karthik", ""])
        out = run("mail_merge.py", "merge", sheet, self.template("Hi {Name} in {City}", bom=True)).stdout
        self.assertIn("row 3 (Karthik)", out)
        with open(self.path("guests-messages.txt"), encoding="utf-8") as fh:
            self.assertTrue(fh.read().startswith("Hi Karthik"))

    def test_csv_not_in_utf8(self):
        sheet = self.path("old.csv")
        with open(sheet, "wb") as fh:
            fh.write("Name\nJos\xe9\n".encode("cp1252"))
        proc = run("mail_merge.py", "merge", sheet, self.template("Hi {Name}"), expect=1)
        self.assertIn("CSV UTF-8", proc.stdout + proc.stderr)
        self.assertNotIn("Traceback", proc.stderr)


class DateCheckAwkwardInputTest(unittest.TestCase):
    def check(self, text, expect):
        proc = run("date_check.py", "--json", "--today", "2026-11-10", "--text", text, expect=expect)
        return json.loads(proc.stdout)["dates"]

    def test_words_ending_in_a_weekday_are_not_weekdays(self):
        self.assertEqual(self.check("The visa was renewed 14 March 2026.", 0), [])
        self.assertEqual(self.check("Call Simon 3 May 2026 about it.", 0), [])

    def test_hours_and_times_are_not_dates(self):
        self.assertEqual(self.check("Open Monday to Friday 9-5.", 0), [])
        self.assertEqual(self.check("See you Monday 9.15 sharp.", 0), [])
        self.assertEqual(len(self.check("Friday 13-11-2026", 0)), 1)

    def test_29_february_without_a_year_uses_the_next_leap_year(self):
        dates = self.check("Tuesday 29 Feb", 0)
        self.assertEqual((dates[0]["date"], dates[0]["year_assumed"]), ("2028-02-29", 2028))


def make_group_form(path):
    """A form with a group "applicant" holding "name" and "city", built by hand."""
    from pypdf import PdfWriter
    from pypdf.generic import ArrayObject, DictionaryObject, FloatObject, NameObject, TextStringObject
    w = PdfWriter()
    page = w.add_blank_page(612, 792)
    parent = DictionaryObject({NameObject("/T"): TextStringObject("applicant")})
    pref = w._add_object(parent)
    kids = ArrayObject()
    for i, name in enumerate(["name", "city"]):
        kid = DictionaryObject({
            NameObject("/Type"): NameObject("/Annot"), NameObject("/Subtype"): NameObject("/Widget"),
            NameObject("/FT"): NameObject("/Tx"), NameObject("/T"): TextStringObject(name),
            NameObject("/Rect"): ArrayObject([FloatObject(v) for v in (50, 700 - 40 * i, 250, 720 - 40 * i)]),
            NameObject("/Parent"): pref, NameObject("/DA"): TextStringObject("/Helv 10 Tf 0 g")})
        kids.append(w._add_object(kid))
    parent[NameObject("/Kids")] = kids
    page[NameObject("/Annots")] = ArrayObject(list(kids))
    font = DictionaryObject({NameObject("/Type"): NameObject("/Font"), NameObject("/Subtype"): NameObject("/Type1"),
                             NameObject("/BaseFont"): NameObject("/Helvetica")})
    w._root_object[NameObject("/AcroForm")] = DictionaryObject({
        NameObject("/Fields"): ArrayObject([pref]), NameObject("/DA"): TextStringObject("/Helv 0 Tf 0 g"),
        NameObject("/DR"): DictionaryObject({NameObject("/Font"): DictionaryObject({NameObject("/Helv"): w._add_object(font)})})})
    w.write(path)
    return path


@unittest.skipUnless(HAVE_PYPDF and HAVE_REPORTLAB, "pypdf or reportlab is not installed")
class FormFillAwkwardInputTest(TempDirCase):
    def fields(self, path):
        return {f["name"]: f for f in json.loads(run("form_fill.py", "fields", path).stdout)["fields"]}

    def test_fields_inside_a_group_are_filled(self):
        src = make_group_form(self.path("group.pdf"))
        fields = self.fields(src)
        self.assertEqual(sorted(fields), ["applicant.city", "applicant.name"])
        self.assertEqual(fields["applicant.name"]["page"], 1)
        values = write_json(self.path("v.json"), {"applicant.name": "Neha Rao", "applicant.city": "Kochi"})
        run("form_fill.py", "fill", src, values)
        fields = self.fields(self.path("group-filled.pdf"))
        self.assertEqual(fields["applicant.name"]["value"], "Neha Rao")
        self.assertEqual(fields["applicant.city"]["value"], "Kochi")

    def test_drop_down_lists_stored_values(self):
        from reportlab.pdfgen import canvas
        src = self.path("drop.pdf")
        c = canvas.Canvas(src)
        c.drawString(50, 600, "State:")
        c.acroForm.choice(name="state", x=50, y=550, width=150, height=20,
                          options=[("Kerala", "KL"), ("Tamil Nadu", "TN")], value="KL")
        c.showPage()
        c.save()
        field = self.fields(src)["state"]
        self.assertEqual(field["value"], "KL")
        self.assertEqual(field["options"], ["KL", "TN"])
        self.assertEqual(field["option_labels"], ["Kerala", "Tamil Nadu"])
        run("form_fill.py", "fill", src, write_json(self.path("v.json"), {"state": "Tamil Nadu"}))
        self.assertEqual(self.fields(self.path("drop-filled.pdf"))["state"]["value"], "TN")

    def test_password_protected_pdf(self):
        from pypdf import PdfWriter
        src = self.path("plain.pdf")
        make_pdf(src)
        locked = self.path("locked.pdf")
        w = PdfWriter(clone_from=src)
        # RC4 needs no extra packages, so this runs where cryptography isn't installed.
        w.encrypt("secret", algorithm="RC4-128")
        w.write(locked)
        for cmd in (["form_fill.py", "fields", locked], ["pdf_extract.py", "extract", locked],
                    ["pdf_extract.py", "images", locked, "--out", self.path("imgs")]):
            proc = run(*cmd, expect=1)
            self.assertIn("password protected", proc.stdout + proc.stderr)
            self.assertNotIn("Traceback", proc.stderr)


@unittest.skipUnless(HAVE_PYPDF and HAVE_DOCX, "pypdf or python-docx is not installed")
class PdfToDocxAwkwardInputTest(TempDirCase):
    def test_numbered_items_keep_their_numbers_and_control_characters_go(self):
        from docx import Document
        src = self.path("terms.pdf")
        make_pdf(src)
        pages = write_json(self.path("p.json"), {"pages": [
            {"page": 1, "text": "1. Payment within 30 days.\n2. Delivery to Pune.\x0c"},
            {"page": 2, "text": "7. Notices go to the office.\x00\n8. Disputes go to Mumbai courts."}]})
        run("pdf_extract.py", "to-docx", src, pages)
        paras = [p.text for p in Document(self.path("terms-humanized.docx")).paragraphs]
        self.assertIn("7. Notices go to the office.", paras)
        self.assertIn("8. Disputes go to Mumbai courts.", paras)
        self.assertIn("1. Payment within 30 days.", paras)

    def test_bad_page_list(self):
        src = self.path("terms.pdf")
        make_pdf(src)
        proc = run("pdf_extract.py", "images", src, "--pages", "2-", "--out", self.path("i"), expect=1)
        self.assertIn("page numbers", proc.stdout + proc.stderr)


if __name__ == "__main__":
    unittest.main()
