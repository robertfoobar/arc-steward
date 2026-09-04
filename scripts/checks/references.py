import re

from checks import fences
from checks.finding import Finding

CHECK = "references"
REFS_OPEN_RE = re.compile(r"^<!--\s*arc42:refs\s*$")
REFS_CLOSE_RE = re.compile(r"^\s*-->\s*$")
ENTITY_BLOCK_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*\{\s*$")
ENTITY_REL_RE = re.compile(
    r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*[|}o][|}o\-.]*[|{o]\s*([A-Za-z_][A-Za-z0-9_]*)\s*:"
)
COMMENT_RE = re.compile(r"--[^\n]*|#[^\n]*|/\*.*?\*/", re.DOTALL)


def _annotated_paths(lines):
    result = []
    inside = False
    for number, line in enumerate(lines, start=1):
        if not inside:
            if REFS_OPEN_RE.match(line):
                inside = True
            continue
        if REFS_CLOSE_RE.match(line):
            inside = False
            continue
        candidate = line.strip()
        if candidate:
            result.append((number, candidate))
    return result


def _er_entities(lines):
    result = {}
    for fence in fences.mermaid_fences(lines):
        if not fence.body:
            continue
        content = [line for line in fence.body if line.strip()]
        if not content or not content[0].strip().startswith("erDiagram"):
            continue
        for offset, line in enumerate(fence.body):
            number = fence.start_line + 1 + offset
            block = ENTITY_BLOCK_RE.match(line)
            if block:
                result.setdefault(block.group(1), number)
                continue
            relation = ENTITY_REL_RE.match(line)
            if relation:
                result.setdefault(relation.group(1), number)
                result.setdefault(relation.group(2), number)
    return result


def _schema_text(repo_root, schema_globs):
    chunks = []
    for pattern in schema_globs:
        for candidate in sorted(repo_root.glob(pattern)):
            if candidate.is_file():
                chunks.append(candidate.read_text(encoding="utf-8", errors="replace"))
    return COMMENT_RE.sub(" ", "\n".join(chunks))


def check_references(text, path, repo_root, schema_globs):
    lines = text.splitlines()
    findings = []
    for number, candidate in _annotated_paths(lines):
        if not (repo_root / candidate).exists():
            findings.append(
                Finding(path, number, CHECK, f"referenced path does not exist: {candidate}")
            )
    entities = _er_entities(lines)
    if entities and schema_globs:
        haystack = _schema_text(repo_root, schema_globs)
        for entity, number in sorted(entities.items()):
            if not re.search(rf"\b{re.escape(entity)}\b", haystack):
                findings.append(
                    Finding(path, number, CHECK, f"entity not found in schema sources: {entity}")
                )
    return findings
