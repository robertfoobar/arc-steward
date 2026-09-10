import re

from checks.finding import Finding

CHECK = "markers"
OPEN_RE = re.compile(r"^<!--\s*arc-steward:generated:(\S+)\s*-->\s*$")
CLOSE_RE = re.compile(r"^<!--\s*/arc-steward:generated\s*-->\s*$")
ID_RE = re.compile(r"^[a-z0-9-]+$")


def _scan(text):
    lines = text.splitlines()
    findings = []
    seen_ids = set()
    open_at = None
    open_id = None
    open_invalid = False
    for number, line in enumerate(lines, start=1):
        opening = OPEN_RE.match(line)
        if opening:
            block_id = opening.group(1)
            if open_at is not None:
                findings.append(
                    Finding("", number, CHECK, f"nested generated block '{block_id}'")
                )
                continue
            if not ID_RE.match(block_id):
                findings.append(
                    Finding("", number, CHECK, f"invalid block id '{block_id}'")
                )
                open_invalid = True
                open_at = number
                open_id = block_id
                continue
            if block_id in seen_ids:
                findings.append(
                    Finding("", number, CHECK, f"duplicate block id '{block_id}'")
                )
                continue
            seen_ids.add(block_id)
            open_invalid = False
            open_at = number
            open_id = block_id
            continue
        if CLOSE_RE.match(line):
            if open_at is None:
                findings.append(
                    Finding("", number, CHECK, "closing marker without opening marker")
                )
                continue
            open_at = None
            open_id = None
            open_invalid = False
    if open_at is not None:
        findings.append(
            Finding("", open_at, CHECK, f"unclosed generated block '{open_id}'")
        )
    return findings


def check_markers(text, path):
    findings = _scan(text)
    return [f._replace(path=path) for f in findings]
