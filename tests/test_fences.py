import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

from checks import fences


class MermaidFencesTest(unittest.TestCase):
    def test_no_fences_yields_nothing(self):
        self.assertEqual(fences.mermaid_fences(["# Chapter", "", "text"]), [])

    def test_non_mermaid_fence_is_ignored(self):
        lines = ["```python", "x = 1", "```"]
        self.assertEqual(fences.mermaid_fences(lines), [])

    def test_closed_fence_yields_body_and_start_line(self):
        lines = ["# Chapter", "```mermaid", "flowchart TD", "  A --> B", "```"]
        found = fences.mermaid_fences(lines)
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].start_line, 2)
        self.assertEqual(found[0].body, ["flowchart TD", "  A --> B"])

    def test_unterminated_fence_yields_none_body(self):
        found = fences.mermaid_fences(["```mermaid", "flowchart TD"])
        self.assertEqual(len(found), 1)
        self.assertIsNone(found[0].body)

    def test_two_fences_are_both_returned(self):
        lines = ["```mermaid", "flowchart TD", "```", "text", "```mermaid", "erDiagram", "```"]
        found = fences.mermaid_fences(lines)
        self.assertEqual([f.start_line for f in found], [1, 5])


if __name__ == "__main__":
    unittest.main()
