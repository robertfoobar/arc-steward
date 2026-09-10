import contextlib
import io
import pathlib
import re
import sys
import tempfile
import unittest
from unittest import mock

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import verify
from checks import routing

UNPARSEABLE = "unparseable format version"


def _section_value(path, heading):
    lines = path.read_text(encoding="utf-8").splitlines()
    start = lines.index(f"## {heading}")
    for line in lines[start + 1 :]:
        if line.strip():
            return line.strip()
    return None


class FormatVersionTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.docs = pathlib.Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def check(self, body):
        (self.docs / routing.ROUTING_FILENAME).write_text(body)
        return routing.check_format(self.docs)

    def with_version(self, value):
        return self.check(f"## Format version\n\n{value}\n\n## Documents\n\n`all`\n")

    def assert_unparseable(self, value):
        finding = self.with_version(value)
        self.assertIsNotNone(finding, value)
        self.assertIn(UNPARSEABLE, finding.message)

    def test_absent_routing_file_is_not_checked(self):
        self.assertIsNone(routing.check_format(self.docs))

    def test_absent_section_means_the_current_version(self):
        self.assertIsNone(self.check("## Documents\n\n`all`\n"))

    def test_current_version_passes(self):
        self.assertIsNone(self.with_version("`1`"))

    def test_value_without_backticks_passes(self):
        self.assertIsNone(self.with_version("1"))

    def test_prose_after_the_value_is_allowed(self):
        self.assertIsNone(self.with_version("`1`\n\nWhich version of the persisted format."))

    def test_newer_version_names_both_versions(self):
        finding = self.with_version("`2`")
        self.assertIn("newer", finding.message)
        self.assertIn("format version 2", finding.message)
        self.assertIn("supports 1", finding.message)
        self.assertEqual(finding.line, 3)

    def test_older_version_points_at_the_release_notes(self):
        with mock.patch.object(routing, "FORMAT_VERSION", 2):
            finding = self.with_version("`1`")
        self.assertIn("older", finding.message)
        self.assertIn("release notes", finding.message)

    def test_zero_is_unparseable(self):
        self.assert_unparseable("`0`")

    def test_negative_is_unparseable(self):
        self.assert_unparseable("`-1`")

    def test_leading_zero_is_unparseable(self):
        self.assert_unparseable("`01`")

    def test_decimal_is_unparseable(self):
        self.assert_unparseable("`1.0`")

    def test_trailing_text_on_the_value_line_is_unparseable(self):
        self.assert_unparseable("`1` (current)")

    def test_digit_separator_is_unparseable(self):
        self.assert_unparseable("`1_0`")

    def test_four_digits_are_unparseable(self):
        self.assert_unparseable("`1000`")

    def test_empty_section_is_unparseable(self):
        finding = self.check("## Format version\n\n## Documents\n\n`all`\n")
        self.assertIn(UNPARSEABLE, finding.message)

    def test_duplicated_section_is_a_finding(self):
        finding = self.check("## Format version\n\n`1`\n\n## Format version\n\n`1`\n")
        self.assertIn("appears more than once", finding.message)


class FormatMismatchStopsVerifyTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)
        self.docs = self.root / "docs" / "architecture"
        self.docs.mkdir(parents=True)
        (self.docs / "05.md").write_text("<!-- arc-steward:generated:broken -->\nbody\n")

    def tearDown(self):
        self.tmp.cleanup()

    def run_main(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = verify.main([str(self.docs), "--repo-root", str(self.root)])
        return code, out.getvalue()

    def test_mismatch_reports_only_the_format_finding(self):
        (self.docs / routing.ROUTING_FILENAME).write_text("## Format version\n\n`2`\n")
        code, output = self.run_main()
        finding_lines = [line for line in output.splitlines() if ": [" in line]
        self.assertEqual(code, 1)
        self.assertEqual(len(finding_lines), 1)
        self.assertIn("format version 2", finding_lines[0])
        self.assertNotIn("05.md", output)

    def test_unparseable_version_also_stops(self):
        (self.docs / routing.ROUTING_FILENAME).write_text("## Format version\n\n`1.0`\n")
        code, output = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn(UNPARSEABLE, output)
        self.assertNotIn("05.md", output)

    def test_matching_version_runs_all_checks(self):
        (self.docs / routing.ROUTING_FILENAME).write_text("## Format version\n\n`1`\n")
        code, output = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("05.md", output)


class FormatVersionDriftTest(unittest.TestCase):
    def test_conventions_state_the_supported_version(self):
        text = (REPO_ROOT / "conventions.md").read_text(encoding="utf-8")
        stated = re.findall(r"current format version is `(\d+)`", text)
        self.assertEqual(stated, [str(routing.FORMAT_VERSION)])

    def test_template_carries_the_supported_version(self):
        template = REPO_ROOT / "templates" / "arc-steward.routing.template.md"
        self.assertEqual(
            _section_value(template, "Format version"), f"`{routing.FORMAT_VERSION}`"
        )

    def test_own_routing_file_carries_the_supported_version(self):
        own = REPO_ROOT / "docs" / "architecture" / routing.ROUTING_FILENAME
        self.assertEqual(_section_value(own, "Format version"), f"`{routing.FORMAT_VERSION}`")

    def test_the_anchor_path_is_pinned(self):
        text = (REPO_ROOT / "conventions.md").read_text(encoding="utf-8")
        self.assertIn(f"`docs/architecture/{routing.ROUTING_FILENAME}`", text)


if __name__ == "__main__":
    unittest.main()
