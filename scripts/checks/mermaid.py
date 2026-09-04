import re

from checks import fences
from checks.finding import Finding

CHECK = "mermaid"
KNOWN_TYPES = (
    "flowchart",
    "graph",
    "sequenceDiagram",
    "erDiagram",
    "classDiagram",
    "stateDiagram-v2",
    "C4Context",
)
PAIRS = {"[": "]", "(": ")", "{": "}"}
CLOSERS = {v: k for k, v in PAIRS.items()}
CARDINALITY_RE = re.compile(r"[|}{o]+[-.]{2}[|}{o]+")


def _bracket_findings(fence_line, body, path, is_er):
    stack = []
    for line in body:
        stripped = re.sub(r'"[^"]*"', "", line)
        if is_er:
            stripped = CARDINALITY_RE.sub("", stripped)
        for char in stripped:
            if char in PAIRS:
                stack.append(char)
            elif char in CLOSERS:
                if not stack or stack[-1] != CLOSERS[char]:
                    return [Finding(path, fence_line, CHECK, f"unbalanced bracket '{char}'")]
                stack.pop()
    if stack:
        return [Finding(path, fence_line, CHECK, f"unbalanced bracket '{stack[-1]}'")]
    return []


def _subgraph_findings(fence_line, body, path):
    open_count = sum(1 for line in body if re.match(r"^\s*subgraph\b", line))
    end_count = sum(1 for line in body if re.match(r"^\s*end\s*$", line))
    if open_count > end_count:
        return [Finding(path, fence_line, CHECK, "subgraph without a matching end")]
    return []


def check_mermaid(text, path):
    lines = text.splitlines()
    findings = []
    for fence in fences.mermaid_fences(lines):
        fence_line = fence.start_line
        if fence.body is None:
            findings.append(Finding(path, fence_line, CHECK, "unterminated mermaid fence"))
            continue
        content = [line for line in fence.body if line.strip()]
        if not content:
            findings.append(Finding(path, fence_line, CHECK, "empty mermaid block"))
            continue
        header = content[0].strip()
        if not any(header.startswith(known) for known in KNOWN_TYPES):
            findings.append(
                Finding(path, fence_line, CHECK, f"unknown diagram type '{header.split()[0]}'")
            )
            continue
        findings.extend(
            _bracket_findings(fence_line, content, path, header.startswith("erDiagram"))
        )
        findings.extend(_subgraph_findings(fence_line, content, path))
    return findings
