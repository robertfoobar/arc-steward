import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

from checks import markers


CLEAN = """# Chapter

Hand-written intro.

<!-- arc-steward:generated:context-diagram -->
Generated body.
<!-- /arc-steward:generated -->

Hand-written outro.
"""


class CheckMarkersTest(unittest.TestCase):
    def test_clean_document_yields_no_findings(self):
        self.assertEqual(markers.check_markers(CLEAN, "03.md"), [])

    def test_unclosed_block_is_reported(self):
        text = "<!-- arc-steward:generated:abc -->\nbody\n"
        found = markers.check_markers(text, "03.md")
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].line, 1)
        self.assertIn("abc", found[0].message)
        self.assertEqual(found[0].check, "markers")

    def test_closing_without_opening_is_reported(self):
        text = "body\n<!-- /arc-steward:generated -->\n"
        found = markers.check_markers(text, "03.md")
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].line, 2)

    def test_nested_block_is_reported(self):
        text = (
            "<!-- arc-steward:generated:outer -->\n"
            "<!-- arc-steward:generated:inner -->\n"
            "<!-- /arc-steward:generated -->\n"
            "<!-- /arc-steward:generated -->\n"
        )
        found = markers.check_markers(text, "03.md")
        self.assertTrue(any("nested" in f.message.lower() for f in found))

    def test_duplicate_id_in_same_file_is_reported(self):
        text = (
            "<!-- arc-steward:generated:dup -->\n"
            "<!-- /arc-steward:generated -->\n"
            "<!-- arc-steward:generated:dup -->\n"
            "<!-- /arc-steward:generated -->\n"
        )
        found = markers.check_markers(text, "03.md")
        self.assertTrue(any("dup" in f.message for f in found))

    def test_invalid_id_is_reported(self):
        text = "<!-- arc-steward:generated:Not_Valid -->\n<!-- /arc-steward:generated -->\n"
        found = markers.check_markers(text, "03.md")
        self.assertEqual(len(found), 1)


if __name__ == "__main__":
    unittest.main()
