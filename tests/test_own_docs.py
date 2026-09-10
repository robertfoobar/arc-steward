import contextlib
import fnmatch
import io
import pathlib
import re
import sys
import unicodedata
import unittest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import verify
from checks import routing

DOCS = REPO_ROOT / "docs" / "arc42"
MARKER_LINE_RE = re.compile(r"^<!-- (arc42:generated:[a-z0-9-]+ -->|/arc42:generated -->|arc42:refs)$")
PATTERN_RE = re.compile(r"`([^`]+)`")
INVISIBLE_CATEGORY = "Cf"
GIT_DIR = ".git"


def _documents():
    return sorted(DOCS.rglob("*.md"))


def _repository_files():
    files = (path.relative_to(REPO_ROOT) for path in REPO_ROOT.rglob("*") if path.is_file())
    return [path.as_posix() for path in files if path.parts[0] != GIT_DIR]


def _routing_patterns():
    lines = routing.routing_path(DOCS).read_text(encoding="utf-8").splitlines()
    start = lines.index("## Path routing")
    patterns = []
    for line in lines[start + 1:]:
        if line.startswith("## "):
            break
        if not line.startswith("|"):
            continue
        first_cell = line.strip("|").split("|")[0]
        patterns.extend(PATTERN_RE.findall(first_cell))
    return patterns


class OwnDocsTest(unittest.TestCase):
    def test_verification_passes(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            exit_code = verify.main([str(DOCS), "--repo-root", str(REPO_ROOT)])
        self.assertEqual(exit_code, 0, output.getvalue())

    def test_every_routing_pattern_matches_a_repository_file(self):
        files = _repository_files()
        patterns = _routing_patterns()
        self.assertTrue(patterns)
        for pattern in patterns:
            with self.subTest(pattern=pattern):
                self.assertTrue(fnmatch.filter(files, pattern), f"{pattern} matches nothing")

    def test_html_comments_are_only_marker_syntax(self):
        for document in _documents():
            for number, line in enumerate(document.read_text(encoding="utf-8").splitlines(), 1):
                if "<!--" not in line:
                    continue
                with self.subTest(document=document.name, line=number):
                    self.assertRegex(line, MARKER_LINE_RE)

    def test_no_invisible_format_characters(self):
        for document in _documents():
            text = document.read_text(encoding="utf-8")
            hidden = {hex(ord(char)) for char in text if unicodedata.category(char) == INVISIBLE_CATEGORY}
            with self.subTest(document=document.name):
                self.assertEqual(hidden, set())


if __name__ == "__main__":
    unittest.main()
