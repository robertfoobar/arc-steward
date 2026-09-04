import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

from checks import references


class ReferencesTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)
        (self.root / "backend" / "src" / "collectors").mkdir(parents=True)
        (self.root / "backend" / "src" / "collectors" / "reddit.py").write_text("x = 1\n")
        migrations = self.root / "backend" / "src" / "db" / "migrations"
        migrations.mkdir(parents=True)
        (migrations / "001_initial.sql").write_text(
            "CREATE TABLE users (id uuid);\nCREATE TABLE raw_signals (id uuid);\n"
        )
        self.globs = ["backend/src/db/migrations/*.sql"]

    def tearDown(self):
        self.tmp.cleanup()


class PathAnnotationTest(ReferencesTestCase):
    def test_existing_path_is_clean(self):
        text = "<!-- arc42:refs\nbackend/src/collectors\n-->\n"
        self.assertEqual(references.check_references(text, "05.md", self.root, []), [])

    def test_missing_path_is_reported(self):
        text = "<!-- arc42:refs\nbackend/src/ghosts\n-->\n"
        found = references.check_references(text, "05.md", self.root, [])
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].check, "references")
        self.assertIn("backend/src/ghosts", found[0].message)
        self.assertEqual(found[0].line, 2)

    def test_document_without_annotations_is_clean(self):
        self.assertEqual(references.check_references("# Chapter\n", "05.md", self.root, []), [])


class EntityVerificationTest(ReferencesTestCase):
    def test_known_entities_are_clean(self):
        text = (
            "```mermaid\n"
            "erDiagram\n"
            "  users {\n"
            "    uuid id PK\n"
            "  }\n"
            '  users ||--o{ raw_signals : "produces"\n'
            "```\n"
        )
        self.assertEqual(references.check_references(text, "08.md", self.root, self.globs), [])

    def test_unknown_entity_is_reported(self):
        text = "```mermaid\nerDiagram\n  bookmarks {\n    uuid id PK\n  }\n```\n"
        found = references.check_references(text, "08.md", self.root, self.globs)
        self.assertEqual(len(found), 1)
        self.assertIn("bookmarks", found[0].message)
        self.assertEqual(found[0].line, 3)

    def test_entity_named_only_in_a_comment_is_reported(self):
        note = self.root / "backend" / "src" / "db" / "migrations" / "002_note.sql"
        note.write_text("-- the bookmarks table was dropped, do not reintroduce it\n")
        text = "```mermaid\nerDiagram\n  bookmarks {\n    uuid id PK\n  }\n```\n"
        found = references.check_references(text, "08.md", self.root, self.globs)
        self.assertEqual(len(found), 1)
        self.assertIn("bookmarks", found[0].message)

    def test_entities_are_not_checked_without_globs(self):
        text = "```mermaid\nerDiagram\n  bookmarks {\n    uuid id PK\n  }\n```\n"
        self.assertEqual(references.check_references(text, "08.md", self.root, []), [])

    def test_non_er_diagrams_are_ignored(self):
        text = "```mermaid\nflowchart TD\n  bookmarks[Bookmarks] --> api[API]\n```\n"
        self.assertEqual(references.check_references(text, "05.md", self.root, self.globs), [])


if __name__ == "__main__":
    unittest.main()
