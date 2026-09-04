import re

from checks.finding import Finding

CHECK = "routing"
ROUTING_FILENAME = "arc42.routing.md"
DEFAULT_STANDARD = "arc42"
DEFAULT_LANGUAGE = "en"
ALL_DOCUMENTS = "all"

ARC42_CHAPTERS = {
    "01": {"en": "01-introduction-and-goals.md", "de": "01-einfuehrung-und-ziele.md"},
    "02": {"en": "02-constraints.md", "de": "02-randbedingungen.md"},
    "03": {"en": "03-context-and-scope.md", "de": "03-kontextabgrenzung.md"},
    "04": {"en": "04-solution-strategy.md", "de": "04-loesungsstrategie.md"},
    "05": {"en": "05-building-block-view.md", "de": "05-bausteinsicht.md"},
    "06": {"en": "06-runtime-view.md", "de": "06-laufzeitsicht.md"},
    "07": {"en": "07-deployment-view.md", "de": "07-verteilungssicht.md"},
    "08": {"en": "08-crosscutting-concepts.md", "de": "08-querschnittliche-konzepte.md"},
    "09": {"en": "09-architecture-decisions.md", "de": "09-architekturentscheidungen.md"},
    "10": {"en": "10-quality-requirements.md", "de": "10-qualitaetsanforderungen.md"},
    "11": {
        "en": "11-risks-and-technical-debt.md",
        "de": "11-risiken-und-technische-schulden.md",
    },
    "12": {"en": "12-glossary.md", "de": "12-glossar.md"},
}

GUIDEBOOK_CHAPTERS = {
    "01": {"en": "01-context.md", "de": "01-kontext.md"},
    "02": {"en": "02-functional-overview.md", "de": "02-funktionaler-ueberblick.md"},
    "03": {"en": "03-quality-attributes.md", "de": "03-qualitaetsmerkmale.md"},
    "04": {"en": "04-constraints.md", "de": "04-randbedingungen.md"},
    "05": {"en": "05-principles.md", "de": "05-prinzipien.md"},
    "06": {"en": "06-software-architecture.md", "de": "06-softwarearchitektur.md"},
    "07": {"en": "07-external-interfaces.md", "de": "07-externe-schnittstellen.md"},
    "08": {"en": "08-code.md", "de": "08-code.md"},
    "09": {"en": "09-data.md", "de": "09-daten.md"},
    "10": {
        "en": "10-infrastructure-architecture.md",
        "de": "10-infrastrukturarchitektur.md",
    },
    "11": {"en": "11-deployment.md", "de": "11-deployment.md"},
    "12": {"en": "12-operation-and-support.md", "de": "12-betrieb-und-support.md"},
    "13": {"en": "13-development-environment.md", "de": "13-entwicklungsumgebung.md"},
    "14": {"en": "14-decision-log.md", "de": "14-entscheidungslog.md"},
}

STANDARDS = {"arc42": ARC42_CHAPTERS, "guidebook": GUIDEBOOK_CHAPTERS}
LANGUAGES = ("en", "de")

_HEADING_RE = re.compile(r"^##\s+(.*?)\s*$")
_TOKEN_RE = re.compile(r"^`?([a-z0-9_-]+)`?$")
_LIST_ITEM_RE = re.compile(r"^\s*[-*]\s+(.*)$")
_LEADING_CHAPTER_RE = re.compile(r"^`?(\d{2})\b")
_CHAPTER_RE = re.compile(r"\b(\d{2})\b")


def _sections(lines):
    result = {}
    current = None
    for number, line in enumerate(lines, start=1):
        heading = _HEADING_RE.match(line)
        if heading:
            current = heading.group(1).strip().lower()
            result[current] = []
            continue
        if current is not None:
            result[current].append((number, line))
    return result


def _first_token(section):
    for number, line in section or []:
        stripped = line.strip()
        if not stripped or stripped.startswith(">"):
            continue
        token = _TOKEN_RE.match(stripped)
        if token:
            return number, token.group(1)
    return None, None


def _document_ids(section):
    ids = []
    for number, line in section or []:
        stripped = line.strip()
        if not stripped or stripped.startswith(">"):
            continue
        if _TOKEN_RE.match(stripped) and stripped.strip("`") == ALL_DOCUMENTS:
            return None
        item = _LIST_ITEM_RE.match(line)
        if not item:
            continue
        chapter = _LEADING_CHAPTER_RE.match(item.group(1).strip())
        if chapter:
            ids.append((number, chapter.group(1)))
    return ids or None


def _routed_chapters(section):
    result = []
    for number, line in section or []:
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 2:
            continue
        if set(cells[-1]) <= set("-: "):
            continue
        if cells[-1].lower() == "artifacts":
            continue
        for chapter in _CHAPTER_RE.findall(cells[-1]):
            result.append((number, chapter))
    return result


def _filename(chapters, chapter, language):
    names = chapters.get(chapter)
    if names is None:
        return None
    return names.get(language) or names[DEFAULT_LANGUAGE]


def routing_path(docs_dir):
    return docs_dir / ROUTING_FILENAME


def check_routing(docs_dir):
    path = routing_path(docs_dir)
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    sections = _sections(text.splitlines())
    findings = []

    standard_line, standard = _first_token(sections.get("documentation standard"))
    if standard is None:
        standard = DEFAULT_STANDARD
    elif standard not in STANDARDS:
        findings.append(
            Finding(
                ROUTING_FILENAME,
                standard_line,
                CHECK,
                f"unknown documentation standard '{standard}', expected one of "
                + ", ".join(sorted(STANDARDS)),
            )
        )
        return findings

    language_line, language = _first_token(sections.get("documentation language"))
    if language is None:
        language = DEFAULT_LANGUAGE
    elif language not in LANGUAGES:
        findings.append(
            Finding(
                ROUTING_FILENAME,
                language_line,
                CHECK,
                f"unknown documentation language '{language}', expected one of "
                + ", ".join(LANGUAGES),
            )
        )
        language = DEFAULT_LANGUAGE

    chapters = STANDARDS[standard]
    selected = _document_ids(sections.get("documents"))
    if selected is None:
        selected_chapters = set(chapters)
    else:
        selected_chapters = set()
        for number, chapter in selected:
            if chapter not in chapters:
                findings.append(
                    Finding(
                        ROUTING_FILENAME,
                        number,
                        CHECK,
                        f"document '{chapter}' is not part of the {standard} canon",
                    )
                )
                continue
            selected_chapters.add(chapter)

    for chapter in sorted(selected_chapters):
        name = _filename(chapters, chapter, language)
        if not (docs_dir / name).is_file():
            findings.append(
                Finding(
                    ROUTING_FILENAME,
                    1,
                    CHECK,
                    f"selected document is missing from the documentation set: {name}",
                )
            )

    for number, chapter in _routed_chapters(sections.get("path routing")):
        if chapter in selected_chapters:
            continue
        if chapter in chapters:
            findings.append(
                Finding(
                    ROUTING_FILENAME,
                    number,
                    CHECK,
                    f"path routing targets chapter {chapter}, which this documentation "
                    "set does not contain, so a refresh would silently skip it",
                )
            )
            continue
        findings.append(
            Finding(
                ROUTING_FILENAME,
                number,
                CHECK,
                f"path routing targets chapter {chapter}, which is not part of the "
                f"{standard} canon",
            )
        )

    return findings
