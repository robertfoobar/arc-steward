import contextlib
import io
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

import verify

FIXTURES = pathlib.Path(__file__).resolve().parent / "fixtures"


def run(root, extra=None):
    argv = [str(root / "docs" / "architecture"), "--repo-root", str(root)] + (extra or [])
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = verify.main(argv)
    return code, out.getvalue()


class SmokeTest(unittest.TestCase):
    def test_good_fixture_passes(self):
        code, output = run(
            FIXTURES / "good",
            ["--schema-glob", "backend/src/db/migrations/*.sql"],
        )
        self.assertEqual(code, 0, output)

    def test_bad_fixture_reports_every_check(self):
        code, output = run(FIXTURES / "bad")
        self.assertEqual(code, 1)
        for name in ("markers", "mermaid", "references", "links"):
            self.assertIn(f"[{name}]", output)


if __name__ == "__main__":
    unittest.main()
