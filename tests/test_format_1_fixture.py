import contextlib
import io
import pathlib
import shutil
import sys
import tempfile
import unittest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import verify
from checks import routing

FIXTURE = REPO_ROOT / "tests" / "fixtures" / "format-1"


class FormatOneFixtureTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name) / "repo"
        shutil.copytree(FIXTURE, self.root)
        self.docs = self.root / "docs" / "architecture"

    def tearDown(self):
        self.tmp.cleanup()

    def edit(self, name, old, new):
        path = self.docs / name
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def run_verify(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = verify.main([str(self.docs), "--repo-root", str(self.root)])
        return code, out.getvalue()

    def test_format_1_is_still_the_current_format(self):
        self.assertEqual(routing.FORMAT_VERSION, 1)

    def test_the_frozen_set_passes(self):
        self.assertEqual(self.run_verify()[0], 0)

    def test_its_generated_markers_are_still_recognized(self):
        self.edit("01-context.md", "<!-- /arc-steward:generated -->\n", "")
        code, output = self.run_verify()
        self.assertEqual(code, 1)
        self.assertIn("[markers]", output)

    def test_its_reference_annotations_are_still_recognized(self):
        self.edit("01-context.md", "src/app.py", "src/gone.py")
        code, output = self.run_verify()
        self.assertEqual(code, 1)
        self.assertIn("[references]", output)

    def test_its_routing_file_and_format_section_are_still_read(self):
        self.edit(routing.ROUTING_FILENAME, "`1`", "`2`")
        code, output = self.run_verify()
        self.assertEqual(code, 1)
        self.assertIn("format version 2", output)

    def test_its_chapter_file_names_are_still_the_canon(self):
        (self.docs / "01-context.md").rename(self.docs / "01-kontext-renamed.md")
        code, output = self.run_verify()
        self.assertEqual(code, 1)
        self.assertIn("01-context.md", output)


if __name__ == "__main__":
    unittest.main()
