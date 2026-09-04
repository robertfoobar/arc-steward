from typing import NamedTuple


class Finding(NamedTuple):
    path: str
    line: int
    check: str
    message: str
