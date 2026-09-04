import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

from checks import mermaid


def fence(body):
    return f"# Chapter\n\n```mermaid\n{body}\n```\n"


class CheckMermaidTest(unittest.TestCase):
    def test_document_without_diagrams_is_clean(self):
        self.assertEqual(mermaid.check_mermaid("# Chapter\n\ntext\n", "05.md"), [])

    def test_valid_flowchart_is_clean(self):
        body = "flowchart TD\n  A[User] --> B[API]"
        self.assertEqual(mermaid.check_mermaid(fence(body), "05.md"), [])

    def test_valid_er_diagram_is_clean(self):
        body = 'erDiagram\n  users {\n    uuid id PK\n  }\n  users ||--o{ sessions : "has"'
        self.assertEqual(mermaid.check_mermaid(fence(body), "08.md"), [])

    def test_valid_sequence_diagram_is_clean(self):
        body = "sequenceDiagram\n  Client->>API: request\n  API-->>Client: response"
        self.assertEqual(mermaid.check_mermaid(fence(body), "06.md"), [])

    def test_unknown_diagram_type_is_reported(self):
        found = mermaid.check_mermaid(fence("pieChartish\n  A --> B"), "05.md")
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].check, "mermaid")
        self.assertIn("pieChartish", found[0].message)

    def test_empty_block_is_reported(self):
        found = mermaid.check_mermaid("```mermaid\n\n```\n", "05.md")
        self.assertEqual(len(found), 1)
        self.assertIn("empty", found[0].message.lower())

    def test_er_cardinality_is_not_a_bracket(self):
        body = 'erDiagram\n  users ||--o{ sessions : "has"\n  sessions }o--|| hosts : "on"'
        self.assertEqual(mermaid.check_mermaid(fence(body), "08.md"), [])

    def test_unbalanced_brace_in_er_entity_is_reported(self):
        body = 'erDiagram\n  users {\n    uuid id PK\n  users ||--o{ sessions : "has"'
        found = mermaid.check_mermaid(fence(body), "08.md")
        self.assertTrue(any("bracket" in f.message.lower() for f in found))

    def test_unbalanced_bracket_is_reported(self):
        found = mermaid.check_mermaid(fence("flowchart TD\n  A[User --> B[API]"), "05.md")
        self.assertTrue(any("bracket" in f.message.lower() for f in found))

    def test_subgraph_without_end_is_reported(self):
        body = "flowchart TD\n  subgraph Backend\n    A[API]"
        found = mermaid.check_mermaid(fence(body), "05.md")
        self.assertTrue(any("subgraph" in f.message.lower() for f in found))

    def test_unterminated_fence_is_reported(self):
        found = mermaid.check_mermaid("```mermaid\nflowchart TD\n  A --> B\n", "05.md")
        self.assertTrue(any("unterminated" in f.message.lower() for f in found))

    def test_line_number_points_at_the_fence(self):
        found = mermaid.check_mermaid(fence("nonsenseType\n  A --> B"), "05.md")
        self.assertEqual(found[0].line, 3)


if __name__ == "__main__":
    unittest.main()
