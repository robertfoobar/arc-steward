# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/) as defined in
[RELEASING.md](RELEASING.md#choosing-the-version).

## [Unreleased]

## [1.2.0] - 2026-09-25

### Changed

- Refresh treats a no-op as its default outcome. After mapping the diff it checks whether the
  change is architecturally significant — interfaces, modules, components, runtime dependencies,
  deployment topology, persisted data model, cross-cutting concepts — and stays passive for CI and
  other process changes, refactorings without structural impact, development tooling, tests, bug
  fixes, UI copy, dependency updates and configuration values. Skipped candidates are named in the
  report (#33).
- The documentation separates what the harness enforces from what the agent is instructed to do:
  staying inside generated blocks and under `docs/architecture/` is a rule, not a sandbox. The
  README gains a "Limitations and safe use" section, and `SECURITY.md` names the latest release
  as the only supported version instead of the latest commit on `main` (#28).
- `NOTICE` states that the arc42 chapter titles stay under CC BY-SA 4.0 rather than MIT, carries
  the upstream copyright notice, and points the Software Guidebook at its own book, noting that
  the chapter canon follows an earlier edition (#28, #30).

### Added

- An Impressum section in the README, and a note that the skill is given away for free and creates
  no advisory contract (#28).

## [1.1.0] - 2026-09-14

A security-hardening release. No format change, so existing documentation sets need no migration.
Two entries add stricter checks: a non-regular `*.md` in the docs tree is now a finding, and
`--schema-glob` candidates outside the repository are dropped, so a run may report findings it
previously did not.

### Security

- Narrow `allowed-tools` to `Read Write Edit`, dropping the `Bash(git:*)` and `Bash(python3:*)`
  wildcards. Both pre-approved arbitrary code execution for the invoking turn — `git -c
  alias.x='!sh'` and `python3 -c` run shell code while still matching the wildcard — which
  combined with untrusted repository content read into context enabled prompt-free execution.
  Read-only git forms stay prompt-free via the harness's built-in read-only set; `verify.py`
  now prompts once per run. Releases 1.0.0 and 1.0.1 are affected; upgrade (#17).
- Add a trust-boundary section to `SKILL.md`: repository content the skill reads (routing file,
  diff, file contents) is data, never instructions. Instructions embedded in that content are
  ignored, writes stay under `docs/architecture/`, and generated content never instructs a later
  agent. Hardens the skill against indirect prompt injection from untrusted repositories.
- `verify.py` no longer follows symlinks or reads non-regular files. Document collection walks the
  tree without descending into symlinked directories and reads only regular files; link-target and
  schema-source reads do the same. A committed symlink pointing outside the repository is reported
  instead of read (no out-of-repo exfiltration), and a FIFO or device target no longer blocks the
  run. A non-regular `*.md` in the docs tree is now a finding.
- `--schema-glob` is contained to the repository. A glob candidate that resolves outside the
  repository root is dropped instead of read, so a `..`-traversal pattern can no longer pull in
  out-of-repo content, and an absolute or otherwise unsupported pattern is treated as zero matches
  rather than crashing the run.
- Sanitize control and format characters when printing findings. A referenced path or link target
  is attacker-controlled text echoed into the finding line; control characters in it (ANSI escape
  sequences, zero-width or bidirectional marks) are now replaced with a visible escaped form before
  output, so a crafted document can no longer manipulate the terminal or smuggle hidden text back
  into an agent's context through a finding.

## [1.0.1] - 2026-09-10

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

[Unreleased]: https://github.com/robertfoobar/arc-steward/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/robertfoobar/arc-steward/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/robertfoobar/arc-steward/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/robertfoobar/arc-steward/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/robertfoobar/arc-steward/releases/tag/v1.0.0
