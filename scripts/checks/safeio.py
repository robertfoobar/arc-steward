import os
import pathlib
import stat


def is_regular_file(path):
    try:
        return stat.S_ISREG(os.lstat(path).st_mode)
    except OSError:
        return False


def read_text(path):
    if not is_regular_file(path):
        return None
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def markdown_documents(docs_dir):
    for current, _dirs, files in os.walk(docs_dir, followlinks=False):
        base = pathlib.Path(current)
        for name in files:
            if name.endswith(".md"):
                yield base / name
