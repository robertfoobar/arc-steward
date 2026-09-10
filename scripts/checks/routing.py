import re

from checks.finding import Finding

CHECK = "routing"
ROUTING_FILENAME = "arc-steward.routing.md"
FORMAT_VERSION = 1
FORMAT_SECTION = "format version"
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
_PLACEHOLDER_RE = re.compile(r"\bEXAMPLE\b")
_VERSION_RE = re.compile(r"^`?([1-9][0-9]{0,2})`?$")


def _headings(lines):
    for number, line in enumerate(lines, start=1):
        heading = _HEADING_RE.match(line)
        if heading:
            yield number, heading.group(1).strip().lower()


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


def _repeated_headings(lines):
    seen = set()
    for number, name in _headings(lines):
        if name in seen:
            yield number, name
        seen.add(name)


def _first_value_line(section):
    for number, line in section or []:
        stripped = line.strip()
        if stripped and not stripped.startswith(">"):
            return number, stripped
    return None, None


def _single_value(section, label):
    number, text = _first_value_line(section)
    if text is None:
        return None, None, None
    token = _TOKEN_RE.match(text)
    if token:
        return number, token.group(1), None
    finding = Finding(
        ROUTING_FILENAME,
        number,
        CHECK,
        f"{label} must be a single value on the first line of its section, found: {text}",
    )
    return number, None, finding


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


def _placeholder_findings(lines):
    return [
        Finding(
            ROUTING_FILENAME,
            number,
            CHECK,
            "template placeholder left in place, replace it with this repository's own value",
        )
        for number, line in enumerate(lines, start=1)
        if _PLACEHOLDER_RE.search(line)
    ]


def _read_lines(path):
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def _format_finding(line, message):
    return Finding(ROUTING_FILENAME, line, CHECK, message)


def check_format(docs_dir):
    path = routing_path(docs_dir)
    if not path.is_file():
        return None
    lines = _read_lines(path)
    headings = [number for number, name in _headings(lines) if name == FORMAT_SECTION]
    if not headings:
        return None
    if len(headings) > 1:
        return _format_finding(
            headings[1],
            "the format version section appears more than once, so the format version is ambiguous",
        )
    number, text = _first_value_line(_sections(lines)[FORMAT_SECTION])
    match = _VERSION_RE.match(text) if text is not None else None
    if not match:
        return _format_finding(
            number or headings[0],
            f"unparseable format version {text or '(empty section)'}, expected a single positive "
            f"integer such as `{FORMAT_VERSION}`",
        )
    version = int(match.group(1))
    if version > FORMAT_VERSION:
        return _format_finding(
            number,
            f"this set uses format version {version}, newer than this arc-steward, which supports "
            f"{FORMAT_VERSION} — update the skill before running it on this set",
        )
    if version < FORMAT_VERSION:
        return _format_finding(
            number,
            f"this set uses format version {version}, older than this arc-steward, which supports "
            f"{FORMAT_VERSION} — migrate it as described in the release notes of the release that "
            f"introduced format version {FORMAT_VERSION}",
        )
    return None


def _repeated_heading_findings(lines):
    return [
        Finding(
            ROUTING_FILENAME,
            number,
            CHECK,
            f"section '{name}' appears more than once, keep exactly one",
        )
        for number, name in _repeated_headings(lines)
    ]


def check_routing(docs_dir):
    path = routing_path(docs_dir)
    if not path.is_file():
        return []
    lines = _read_lines(path)
    sections = _sections(lines)
    findings = _placeholder_findings(lines) + _repeated_heading_findings(lines)

    standard_line, standard, unparseable = _single_value(
        sections.get("documentation standard"), "documentation standard"
    )
    if unparseable:
        findings.append(unparseable)
        return findings
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

    language_line, language, unparseable = _single_value(
        sections.get("documentation language"), "documentation language"
    )
    if unparseable:
        findings.append(unparseable)
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
