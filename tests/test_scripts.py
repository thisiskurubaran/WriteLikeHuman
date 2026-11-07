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


if __name__ == "__main__":
    unittest.main()
