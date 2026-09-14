import contextlib
import io
import os
import pathlib
import signal
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

import verify


class _Timeout(Exception):
    pass


@contextlib.contextmanager
def _deadline(seconds):
    def _raise(signum, frame):
        raise _Timeout(f"blocked for more than {seconds}s")

    previous = signal.signal(signal.SIGALRM, _raise)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous)


class VerifyTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)
        self.docs_dir = self.root / "docs" / "architecture"
        self.docs_dir.mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def run_main(self, extra=None):
        argv = [str(self.docs_dir), "--repo-root", str(self.root)] + (extra or [])
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = verify.main(argv)
        return code, out.getvalue()

    def test_clean_documentation_returns_zero(self):
        (self.docs_dir / "05.md").write_text(
            "# Building Blocks\n\n"
            "<!-- arc-steward:generated:components -->\n"
            "```mermaid\nflowchart TD\n  A[API] --> B[DB]\n```\n"
            "<!-- /arc-steward:generated -->\n"
        )
        code, output = self.run_main()
        self.assertEqual(code, 0)
        self.assertIn("5 checks", output)

    def test_findings_return_one_and_are_printed(self):
        (self.docs_dir / "05.md").write_text("<!-- arc-steward:generated:broken -->\nbody\n")
        code, output = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("05.md", output)
        self.assertIn("[markers]", output)
        self.assertIn("broken", output)

    def test_all_four_checks_report(self):
        (self.docs_dir / "05.md").write_text(
            "<!-- arc-steward:refs\nnot/here\n-->\n"
            "```mermaid\nbogusType\n  A --> B\n```\n"
            "[gone](nope.md)\n"
            "<!-- /arc-steward:generated -->\n"
        )
        code, output = self.run_main()
        self.assertEqual(code, 1)
        for name in ("markers", "mermaid", "references", "links"):
            self.assertIn(f"[{name}]", output)

    def test_missing_docs_directory_returns_two(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = verify.main([str(self.root / "absent"), "--repo-root", str(self.root)])
        self.assertEqual(code, 2)

    def test_nested_documents_are_checked(self):
        nested = self.docs_dir / "08-data-model"
        nested.mkdir()
        (nested / "users.md").write_text("<!-- /arc-steward:generated -->\n")
        code, output = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("users.md", output)

    def test_schema_glob_is_passed_to_reference_check(self):
        migrations = self.root / "db"
        migrations.mkdir()
        (migrations / "001.sql").write_text("CREATE TABLE users (id uuid);\n")
        (self.docs_dir / "08.md").write_text(
            "```mermaid\nerDiagram\n  ghosts {\n    uuid id PK\n  }\n```\n"
        )
        code, output = self.run_main(["--schema-glob", "db/*.sql"])
        self.assertEqual(code, 1)
        self.assertIn("ghosts", output)

    def test_empty_documentation_tree_is_a_finding(self):
        code, output = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn(str(self.docs_dir), output)

    def test_success_line_reports_document_count(self):
        (self.docs_dir / "05.md").write_text("# Building Blocks\n")
        (self.docs_dir / "06.md").write_text("# Runtime View\n")
        code, output = self.run_main()
        self.assertEqual(code, 0)
        self.assertIn("2 document", output)

    def test_missing_schema_glob_is_reported_as_disabled(self):
        (self.docs_dir / "05.md").write_text("# Building Blocks\n")
        code, output = self.run_main()
        self.assertEqual(code, 0)
        self.assertIn("no --schema-glob given", output)
        self.assertIn("disabled", output)

    def test_schema_globs_report_match_counts(self):
        migrations = self.root / "db"
        migrations.mkdir()
        (migrations / "001.sql").write_text("CREATE TABLE users (id uuid);\n")
        (migrations / "002.sql").write_text("CREATE TABLE signals (id uuid);\n")
        (self.docs_dir / "05.md").write_text("# Building Blocks\n")
        code, output = self.run_main(["--schema-glob", "db/*.sql"])
        self.assertEqual(code, 0)
        self.assertIn("db/*.sql", output)
        self.assertIn("matched 2 file(s)", output)

    def test_schema_glob_matching_nothing_reports_zero(self):
        (self.docs_dir / "05.md").write_text("# Building Blocks\n")
        code, output = self.run_main(["--schema-glob", "db/*.sql"])
        self.assertEqual(code, 0)
        self.assertIn("matched 0 file(s)", output)

    def test_missing_routing_file_is_reported_as_unchecked(self):
        (self.docs_dir / "05.md").write_text("# Building Blocks\n")
        code, output = self.run_main()
        self.assertEqual(code, 0)
        self.assertIn("no arc-steward.routing.md found", output)

    def test_routing_findings_are_collected(self):
        (self.docs_dir / "05-building-block-view.md").write_text("# Building Blocks\n")
        (self.docs_dir / "arc-steward.routing.md").write_text(
            "## Documents\n\n- `05` — Building Block View\n\n"
            "## Path routing\n\n"
            "| Path pattern | Artifacts |\n|---|---|\n"
            "| `src/**` | 07 deployment |\n"
        )
        code, output = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("[routing]", output)
        self.assertIn("arc-steward.routing.md", output)


class NonRegularFileTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)
        self.docs_dir = self.root / "docs" / "architecture"
        self.docs_dir.mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def run_main(self, extra=None):
        argv = [str(self.docs_dir), "--repo-root", str(self.root)] + (extra or [])
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = verify.main(argv)
        return code, out.getvalue()

    def test_symlinked_document_content_is_not_read(self):
        outside = self.root / "outside.txt"
        outside.write_text("OUTSIDE_ONLY_CONTENT\n")
        (self.docs_dir / "leak.md").symlink_to(outside)
        (self.docs_dir / "05.md").write_text("# Building Blocks\n")
        code, output = self.run_main()
        self.assertNotIn("OUTSIDE_ONLY_CONTENT", output)
        self.assertEqual(code, 1)
        self.assertIn("leak.md", output)

    def test_symlinked_document_is_not_counted_as_scanned(self):
        outside = self.root / "outside.txt"
        outside.write_text("data\n")
        (self.docs_dir / "leak.md").symlink_to(outside)
        (self.docs_dir / "05.md").write_text("# Building Blocks\n")
        code, output = self.run_main()
        self.assertIn("1 document", output)

    def test_document_in_symlinked_directory_is_not_followed(self):
        outside = self.root / "outside"
        outside.mkdir()
        (outside / "05.md").write_text("<!-- /arc-steward:generated -->\n")
        (self.docs_dir / "linked").symlink_to(outside, target_is_directory=True)
        (self.docs_dir / "05.md").write_text("# Building Blocks\n")
        code, output = self.run_main()
        self.assertEqual(code, 0, output)
        self.assertIn("1 document", output)

    def test_fifo_document_does_not_hang(self):
        os.mkfifo(self.docs_dir / "hang.md")
        (self.docs_dir / "05.md").write_text("# Building Blocks\n")
        with _deadline(10):
            code, output = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("hang.md", output)

    def test_fifo_link_target_does_not_hang(self):
        os.mkfifo(self.root / "pipe")
        (self.docs_dir / "05.md").write_text("# Building Blocks\n[x](../../pipe#anchor)\n")
        with _deadline(10):
            code, _ = self.run_main()
        self.assertEqual(code, 1)

    def test_fifo_schema_source_does_not_hang(self):
        os.mkfifo(self.root / "schema.sql")
        (self.docs_dir / "08.md").write_text(
            "```mermaid\nerDiagram\n  users {\n    uuid id PK\n  }\n```\n"
        )
        with _deadline(10):
            self.run_main(["--schema-glob", "schema.sql"])


class SchemaGlobContainmentTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = pathlib.Path(self.tmp.name)
        self.repo = self.base / "repo"
        self.docs_dir = self.repo / "docs" / "architecture"
        self.docs_dir.mkdir(parents=True)
        self.outside = self.base / "outside"
        self.outside.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def run_main(self, extra=None):
        argv = [str(self.docs_dir), "--repo-root", str(self.repo)] + (extra or [])
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = verify.main(argv)
        return code, out.getvalue()

    def _er_document(self):
        (self.docs_dir / "08.md").write_text(
            "```mermaid\nerDiagram\n  ghosts {\n    uuid id PK\n  }\n```\n"
        )

    def test_glob_inside_repo_still_resolves_entities(self):
        db = self.repo / "db"
        db.mkdir()
        (db / "001.sql").write_text("CREATE TABLE ghosts (id uuid);\n")
        self._er_document()
        code, output = self.run_main(["--schema-glob", "db/*.sql"])
        self.assertEqual(code, 0, output)
        self.assertIn("matched 1 file(s)", output)

    def test_traversal_glob_matches_nothing_and_is_not_read(self):
        (self.outside / "schema.sql").write_text("CREATE TABLE ghosts (id uuid);\n")
        self._er_document()
        code, output = self.run_main(["--schema-glob", "../outside/*.sql"])
        self.assertIn("matched 0 file(s)", output)
        self.assertEqual(code, 1)
        self.assertIn("ghosts", output)

    def test_absolute_glob_does_not_crash(self):
        (self.docs_dir / "05.md").write_text("# Building Blocks\n")
        code, output = self.run_main(["--schema-glob", "/etc/pass*"])
        self.assertEqual(code, 0, output)
        self.assertIn("matched 0 file(s)", output)

    def test_symlinked_schema_source_is_excluded(self):
        target = self.outside / "schema.sql"
        target.write_text("CREATE TABLE ghosts (id uuid);\n")
        db = self.repo / "db"
        db.mkdir()
        (db / "link.sql").symlink_to(target)
        self._er_document()
        code, output = self.run_main(["--schema-glob", "db/*.sql"])
        self.assertIn("matched 0 file(s)", output)
        self.assertEqual(code, 1)
        self.assertIn("ghosts", output)


if __name__ == "__main__":
    unittest.main()
