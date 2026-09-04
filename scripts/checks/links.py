import re

from checks.finding import Finding

CHECK = "links"
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.*?)\s*$")
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:")


def _slug(heading):
    lowered = heading.strip().lower()
    cleaned = re.sub(r"[^\w\s-]", "", lowered)
    return re.sub(r"\s", "-", cleaned).strip("-")


def _anchors(text):
    return {_slug(match.group(1)) for match in (HEADING_RE.match(line) for line in text.splitlines()) if match}


def check_links(text, path, doc_path):
    findings = []
    for number, line in enumerate(text.splitlines(), start=1):
        for target in LINK_RE.findall(line):
            if target.startswith(EXTERNAL_PREFIXES):
                continue
            file_part, _, anchor = target.partition("#")
            if not file_part:
                if anchor and _slug(anchor) not in _anchors(text):
                    findings.append(
                        Finding(path, number, CHECK, f"anchor not found: #{anchor}")
                    )
                continue
            resolved = (doc_path.parent / file_part).resolve()
            if not resolved.exists():
                findings.append(
                    Finding(path, number, CHECK, f"link target does not exist: {file_part}")
                )
                continue
            if anchor:
                try:
                    target_text = resolved.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    findings.append(
                        Finding(path, number, CHECK, f"link target is not readable: {file_part}")
                    )
                    continue
                if _slug(anchor) not in _anchors(target_text):
                    findings.append(
                        Finding(path, number, CHECK, f"anchor not found in {file_part}: #{anchor}")
                    )
    return findings
