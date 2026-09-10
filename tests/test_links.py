import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

from checks import links


class LinksTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)
        docs_dir = self.root / "docs" / "architecture"
        docs_dir.mkdir(parents=True)
        self.doc = docs_dir / "05-building-block-view.md"
        (docs_dir / "03-context-and-scope.md").write_text(
            "# Context and Scope\n\n## External Interfaces\n\ntext\n"
        )
        (self.root / "docs" / "adr").mkdir()
        (self.root / "docs" / "adr" / "0001-x.md").write_text("# One\n")

    def tearDown(self):
        self.tmp.cleanup()

    def check(self, text):
        return links.check_links(text, "05-building-block-view.md", self.doc)

    def test_document_without_links_is_clean(self):
        self.assertEqual(self.check("# Chapter\n\ntext\n"), [])

    def test_external_links_are_skipped(self):
        self.assertEqual(self.check("[arc42](https://arc42.org)\n"), [])

    def test_valid_sibling_link_is_clean(self):
        self.assertEqual(self.check("[context](03-context-and-scope.md)\n"), [])

    def test_valid_link_into_another_directory_is_clean(self):
        self.assertEqual(self.check("[adr](../adr/0001-x.md)\n"), [])

    def test_missing_target_is_reported(self):
        found = self.check("[gone](99-nowhere.md)\n")
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].check, "links")
        self.assertIn("99-nowhere.md", found[0].message)
        self.assertEqual(found[0].line, 1)

    def test_valid_anchor_is_clean(self):
        self.assertEqual(
            self.check("[iface](03-context-and-scope.md#external-interfaces)\n"), []
        )

    def test_missing_anchor_is_reported(self):
        found = self.check("[iface](03-context-and-scope.md#nope)\n")
        self.assertEqual(len(found), 1)
        self.assertIn("nope", found[0].message)

    def test_same_document_anchor_is_resolved(self):
        text = "# Building Block View\n\n[top](#building-block-view)\n"
        self.assertEqual(self.check(text), [])

    def test_punctuation_heading_keeps_github_double_hyphen(self):
        text = "# Stakeholder & Rollen\n\n[top](#stakeholder--rollen)\n"
        self.assertEqual(self.check(text), [])

    def test_underscore_in_heading_is_preserved(self):
        text = "# check_links\n\n[top](#check_links)\n"
        self.assertEqual(self.check(text), [])

    def test_unreadable_target_is_reported_not_raised(self):
        found = self.check("[dir](../adr#anything)\n")
        self.assertEqual(len(found), 1)
        self.assertIn("not readable", found[0].message)


if __name__ == "__main__":
    unittest.main()
