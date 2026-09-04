import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

from checks import routing

ARC42_ALL = [
    "01-introduction-and-goals.md",
    "02-constraints.md",
    "03-context-and-scope.md",
    "04-solution-strategy.md",
    "05-building-block-view.md",
    "06-runtime-view.md",
    "07-deployment-view.md",
    "08-crosscutting-concepts.md",
    "09-architecture-decisions.md",
    "10-quality-requirements.md",
    "11-risks-and-technical-debt.md",
    "12-glossary.md",
]


class RoutingTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.docs = pathlib.Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write_routing(self, body):
        (self.docs / routing.ROUTING_FILENAME).write_text(body)

    def write_documents(self, names):
        for name in names:
            (self.docs / name).write_text("# chapter\n")

    def messages(self):
        return [f.message for f in routing.check_routing(self.docs)]

    def test_absent_routing_file_is_not_a_finding(self):
        self.assertEqual(routing.check_routing(self.docs), [])

    def test_full_arc42_set_passes(self):
        self.write_documents(ARC42_ALL)
        self.write_routing(
            "## Documentation standard\n\n`arc42`\n\n"
            "## Documentation language\n\n`en`\n\n"
            "## Documents\n\n`all`\n\n"
            "## Path routing\n\n"
            "| Path pattern | Artifacts |\n|---|---|\n"
            "| `src/**` | 05 building blocks, 12 glossary |\n"
        )
        self.assertEqual(self.messages(), [])

    def test_absent_standard_section_defaults_to_arc42(self):
        self.write_documents(ARC42_ALL)
        self.write_routing("## Documentation language\n\n`en`\n")
        self.assertEqual(self.messages(), [])

    def test_german_language_expects_german_filenames(self):
        self.write_documents(ARC42_ALL)
        self.write_routing("## Documentation language\n\n`de`\n")
        messages = self.messages()
        self.assertTrue(messages)
        self.assertIn("01-einfuehrung-und-ziele.md", " ".join(messages))

    def test_unknown_standard_is_reported_and_stops(self):
        self.write_routing("## Documentation standard\n\n`c4`\n")
        messages = self.messages()
        self.assertEqual(len(messages), 1)
        self.assertIn("unknown documentation standard 'c4'", messages[0])

    def test_unknown_language_is_reported(self):
        self.write_documents(ARC42_ALL)
        self.write_routing("## Documentation language\n\n`fr`\n")
        self.assertIn(
            "unknown documentation language 'fr'", " ".join(self.messages())
        )

    def test_guidebook_set_passes(self):
        self.write_documents(
            [names["en"] for names in routing.GUIDEBOOK_CHAPTERS.values()]
        )
        self.write_routing(
            "## Documentation standard\n\n`guidebook`\n\n"
            "## Documentation language\n\n`en`\n\n"
            "## Path routing\n\n"
            "| Path pattern | Artifacts |\n|---|---|\n"
            "| `src/**` | 06 software architecture, 14 decision log |\n"
        )
        self.assertEqual(self.messages(), [])

    def test_guidebook_german_set_passes(self):
        self.write_documents(
            [names["de"] for names in routing.GUIDEBOOK_CHAPTERS.values()]
        )
        self.write_routing(
            "## Documentation standard\n\n`guidebook`\n\n"
            "## Documentation language\n\n`de`\n"
        )
        self.assertEqual(self.messages(), [])

    def test_guidebook_german_set_expects_german_filenames(self):
        self.write_documents(
            [names["en"] for names in routing.GUIDEBOOK_CHAPTERS.values()]
        )
        self.write_routing(
            "## Documentation standard\n\n`guidebook`\n\n"
            "## Documentation language\n\n`de`\n"
        )
        self.assertIn("09-daten.md", " ".join(self.messages()))

    def test_both_standards_cover_both_languages(self):
        for name, chapters in routing.STANDARDS.items():
            for number, names in chapters.items():
                for language in routing.LANGUAGES:
                    self.assertIn(language, names, f"{name} {number} lacks {language}")

    def test_subset_only_requires_the_selected_documents(self):
        self.write_documents(["01-introduction-and-goals.md", "05-building-block-view.md"])
        self.write_routing(
            "## Documents\n\n- `01` — Introduction and Goals\n"
            "- `05` — Building Block View\n\n"
            "## Path routing\n\n"
            "| Path pattern | Artifacts |\n|---|---|\n"
            "| `src/**` | 05 building blocks |\n"
        )
        self.assertEqual(self.messages(), [])

    def test_selected_document_without_a_file_is_a_finding(self):
        self.write_documents(["01-introduction-and-goals.md"])
        self.write_routing("## Documents\n\n- `01` — Introduction\n- `05` — Building Blocks\n")
        self.assertIn(
            "selected document is missing from the documentation set: "
            "05-building-block-view.md",
            self.messages(),
        )

    def test_routing_to_an_unselected_chapter_is_a_finding(self):
        self.write_documents(["01-introduction-and-goals.md"])
        self.write_routing(
            "## Documents\n\n- `01` — Introduction\n\n"
            "## Path routing\n\n"
            "| Path pattern | Artifacts |\n|---|---|\n"
            "| `src/**` | 07 deployment |\n"
        )
        joined = " ".join(self.messages())
        self.assertIn("path routing targets chapter 07", joined)
        self.assertIn("silently skip", joined)

    def test_routing_to_a_chapter_outside_the_canon_is_a_finding(self):
        self.write_documents(
            [names["en"] for names in routing.GUIDEBOOK_CHAPTERS.values()]
        )
        self.write_routing(
            "## Documentation standard\n\n`guidebook`\n\n"
            "## Path routing\n\n"
            "| Path pattern | Artifacts |\n|---|---|\n"
            "| `src/**` | 15 nowhere |\n"
        )
        self.assertIn(
            "path routing targets chapter 15, which is not part of the guidebook canon",
            self.messages(),
        )

    def test_selecting_a_chapter_outside_the_canon_is_a_finding(self):
        self.write_routing(
            "## Documentation standard\n\n`arc42`\n\n"
            "## Documents\n\n- `14` — Decision Log\n"
        )
        self.assertIn(
            "document '14' is not part of the arc42 canon", self.messages()
        )

    def test_table_header_and_separator_are_not_read_as_chapters(self):
        self.write_documents(["01-introduction-and-goals.md"])
        self.write_routing(
            "## Documents\n\n- `01` — Introduction\n\n"
            "## Path routing\n\n"
            "| Path pattern | Artifacts |\n|---|---|\n"
        )
        self.assertEqual(self.messages(), [])

    def test_example_list_in_a_blockquote_is_ignored(self):
        self.write_documents(ARC42_ALL)
        self.write_routing(
            "## Documents\n\n`all`\n\n"
            "> - `01` — Introduction and Goals\n"
            "> - `03` — Context and Scope\n"
        )
        self.assertEqual(self.messages(), [])


if __name__ == "__main__":
    unittest.main()
