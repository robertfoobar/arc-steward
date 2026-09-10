import pathlib
import re
import sys
import unittest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from checks import routing

CONVENTIONS = REPO_ROOT / "conventions.md"
ROW_RE = re.compile(r"^\|\s*(\d{2})\s*\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|\s*$")


def _section(lines, heading_prefix):
    start = next((i for i, line in enumerate(lines) if line.startswith(heading_prefix)), None)
    if start is None:
        return None
    body = []
    for line in lines[start + 1:]:
        if line.startswith("#"):
            break
        body.append(line)
    return body


def _documented_rows(heading_prefix):
    lines = CONVENTIONS.read_text(encoding="utf-8").splitlines()
    section = _section(lines, heading_prefix)
    if section is None:
        return None
    return [row.groups() for row in map(ROW_RE.match, section) if row]


def _code_rows(chapters):
    return [(number, names["en"], names["de"]) for number, names in chapters.items()]


class CanonSyncTest(unittest.TestCase):
    def assert_in_sync(self, heading_prefix, chapters):
        documented = _documented_rows(heading_prefix)
        self.assertIsNotNone(documented, f"heading '{heading_prefix}' not found in conventions.md")
        self.assertEqual(documented, _code_rows(chapters))

    def test_arc42_table_matches_conventions(self):
        self.assert_in_sync("### 1.1 ", routing.ARC42_CHAPTERS)

    def test_guidebook_table_matches_conventions(self):
        self.assert_in_sync("### 1.2 ", routing.GUIDEBOOK_CHAPTERS)


if __name__ == "__main__":
    unittest.main()
