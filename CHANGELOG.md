# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/) as defined in
[RELEASING.md](RELEASING.md#choosing-the-version).

## [Unreleased]

### Fixed

- The install commands in the README use `ln -sfn`, so re-running them replaces an existing
  link instead of nesting a new one inside the linked directory (#14).

## [1.0.0] - 2026-09-10

First public release.

### Added

- Bootstrap and diff-driven refresh of architecture documentation following arc42 or Simon
  Brown's Software Guidebook, in English or German, with all chapters or a selected subset.
- Mermaid context, component, runtime sequence, deployment and ER diagrams, with generated
  content fenced by `arc-steward:generated` markers so hand-written prose is never touched.
- `scripts/verify.py`: checks markers, Mermaid structure, code and schema references, links and
  anchors, and the routing configuration, including leftover template placeholders.
- Format version 1 of the persisted format, recorded in the routing file and checked before
  anything else, so a set written in another format stops the skill instead of failing silently.

[Unreleased]: https://github.com/robertfoobar/arc-steward/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/robertfoobar/arc-steward/releases/tag/v1.0.0
