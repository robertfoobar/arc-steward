import re
from typing import NamedTuple

OPEN_RE = re.compile(r"^\s*```\s*mermaid\s*$")
CLOSE_RE = re.compile(r"^\s*```\s*$")


class Fence(NamedTuple):
    start_line: int
    body: list


def mermaid_fences(lines):
    result = []
    start = None
    for number, line in enumerate(lines, start=1):
        if start is None:
            if OPEN_RE.match(line):
                start = number
            continue
        if CLOSE_RE.match(line):
            result.append(Fence(start, lines[start:number - 1]))
            start = None
    if start is not None:
        result.append(Fence(start, None))
    return result
