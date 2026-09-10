import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from checks import links, markers, mermaid, references, routing

CHECK_COUNT = 5


def _parse(argv):
    parser = argparse.ArgumentParser(prog="verify.py")
    parser.add_argument("docs_dir")
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--schema-glob", action="append", default=[])
    return parser.parse_args(argv)


def _collect(docs_dir, repo_root, schema_globs):
    documents = sorted(docs_dir.rglob("*.md"))
    findings = []
    for document in documents:
        text = document.read_text(encoding="utf-8", errors="replace")
        relative = str(document.relative_to(docs_dir))
        findings.extend(markers.check_markers(text, relative))
        findings.extend(mermaid.check_mermaid(text, relative))
        findings.extend(references.check_references(text, relative, repo_root, schema_globs))
        findings.extend(links.check_links(text, relative, document))
    findings.extend(routing.check_routing(docs_dir))
    return findings, len(documents)


def _report_schema_globs(repo_root, schema_globs):
    if not schema_globs:
        print(
            "arc-steward: no --schema-glob given, ER entity resolution against schema "
            "sources is disabled"
        )
        return
    for pattern in schema_globs:
        matched = sum(1 for candidate in repo_root.glob(pattern) if candidate.is_file())
        print(f"arc-steward: schema glob '{pattern}' matched {matched} file(s)")


def _report_routing(docs_dir):
    if routing.routing_path(docs_dir).is_file():
        return
    print(
        f"arc-steward: no {routing.ROUTING_FILENAME} found, so the configured standard, "
        "the selected documents and the path routing are not checked"
    )


def main(argv):
    args = _parse(argv)
    docs_dir = pathlib.Path(args.docs_dir)
    repo_root = pathlib.Path(args.repo_root)
    if not docs_dir.is_dir():
        print(f"error: documentation directory not found: {docs_dir}")
        return 2
    _report_schema_globs(repo_root, args.schema_glob)
    _report_routing(docs_dir)
    findings, document_count = _collect(docs_dir, repo_root, args.schema_glob)
    if document_count == 0:
        print(f"arc-steward: no documentation files found under {docs_dir}")
        return 1
    if not findings:
        print(f"arc-steward: {CHECK_COUNT} checks passed across {document_count} document(s)")
        return 0
    for item in sorted(findings, key=lambda f: (f.path, f.line, f.check)):
        print(f"{item.path}:{item.line}: [{item.check}] {item.message}")
    print(
        f"arc-steward: {len(findings)} finding(s) across {CHECK_COUNT} checks "
        f"in {document_count} document(s)"
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
