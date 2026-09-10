# arc-steward

[![CI](https://github.com/robertfoobar/arc-steward/actions/workflows/ci.yml/badge.svg)](https://github.com/robertfoobar/arc-steward/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An [Agent Skill](https://agentskills.io) that keeps a fixed canon of architecture
documentation artifacts up to date **after every feature**, rolled up into a complete
[arc42](https://arc42.org) or [Software Guidebook](https://leanpub.com/software-architecture-for-developers)
documentation set.

## Why avoid architecture drift

Architecture documentation rots the moment nobody tends it. Every feature moves a boundary, adds
a dependency, or touches the data model, and the diagrams describing the system keep asserting
what used to be true. That gap between diagram and code is architecture drift — and past a
certain point nobody trusts the diagram enough to open it, so the documentation stops being read
at all.

Drift compounds silently: nothing breaks when a diagram goes stale, so nothing forces a fix.
Closing the gap later means reconstructing weeks or months of decisions from memory, which is
expensive enough that it rarely happens — the documentation just stays wrong.

`arc-steward` closes the gap at the one point where closing it is cheap: right before a feature
becomes a pull request, while the diff that changed the architecture is still in front of you. It
reads that diff, decides which artifacts it actually touches, and patches only those —
surgically, leaving hand-written prose intact — so the documentation never gets the two stale
weeks in the first place.

## The artifact canon

| Artifact | arc42 chapter | Guidebook chapter |
|---|---|---|
| Context diagram | 03 Context and scope | 01 Context |
| Component diagram | 05 Building block view | 06 Software architecture |
| Runtime sequence diagrams | 06 Runtime view | 06 Software architecture |
| Deployment diagram | 07 Deployment view | 11 Deployment |
| Domain-level ER diagram | 08 Crosscutting concepts | 09 Data |
| Technical ER diagrams, one per bounded context | 08 Crosscutting concepts | 09 Data |

Every chapter of the chosen standard exists by default. Chapters with an authoritative source
elsewhere in the repo link to it generously rather than duplicating it, so a chapter with
nothing of its own to say costs a paragraph rather than a page.

## Choosing a standard and a scope

Two values in the routing file, both verified by the harness:

| Setting | Values | Effect |
|---|---|---|
| Documentation standard | `arc42` (default), `guidebook` | Which chapter canon the set follows |
| Documents | `all` (default), or a list of chapter numbers | Which chapters of that canon the set contains |

`Documents` is the escape hatch for small projects, where whole chapters would stay genuinely
empty. It is not a shortcut for writing less: the harness fails the run when the path routing
table targets a chapter the set does not contain, because refresh would otherwise map nothing
and report success forever.

Both standards are available in English and German. arc42 carries an authoritative German chapter
set; the Guidebook is published in English only, so its German chapter names are this skill's own
translation, fixed in `conventions.md` so that every generated set uses the same ones.

Switching standards later is a fresh bootstrap, not a rename — the two canons do not correspond
chapter by chapter.

## Design principles

- **Mermaid only.** GitHub renders it natively, so every diagram is readable in the PR diff
  where the review happens. No render step, and no shipping your schema to a public
  PlantUML or Kroki server.
- **Provenance markers.** Generated content lives inside `<!-- arc-steward:generated:id -->`
  fences. The refresh touches nothing outside them, so your prose is structurally safe —
  not merely protected by a polite prompt.
- **Evidence or a gap.** Where the code does not support a statement, the skill writes an
  explicit `TODO(human)` instead of inventing one.
- **Verify before finishing.** The harness checks what it can check mechanically: diagram
  type is recognized and brackets, `subgraph`/`end` pairs and provenance markers balance;
  `erDiagram` entity names resolve against the configured schema sources; internal links and
  anchors resolve; the routing configuration agrees with what is on disk and carries no leftover
  template placeholder. It does not parse Mermaid, and component names in `flowchart` diagrams
  are not checked against the code — see `conventions.md` for the exact rules.
- **Configuration is checked, not trusted.** A routing table pointing at a chapter that does not
  exist is the one failure that cannot be noticed by reading the output, because "nothing to
  update" and "nothing found" look identical. The harness fails the run instead.
- **Split by bounded context.** A single ER diagram of 20+ tables is unreadable in any
  notation. The file split does the grouping that layout directives cannot.

## Installation

Clone the repository anywhere, then symlink it into `~/.agents/skills/` — the cross-runtime
skills directory:

```bash
git clone https://github.com/robertfoobar/arc-steward.git
git -C arc-steward checkout "$(git -C arc-steward describe --tags --abbrev=0)"
mkdir -p ~/.agents/skills
ln -sf "$PWD/arc-steward" ~/.agents/skills/arc-steward
```

The second line checks out the latest release; `main` is the development branch. Git's
detached-HEAD notice is expected.

Whether that's enough, or you need a second, harness-specific symlink, depends on the harness.
Verified so far:

| Harness | Reads `~/.agents/skills/` | Extra step |
|---|---|---|
| OpenCode | Yes | None |
| Codex CLI | Yes | None |
| GitHub Copilot CLI | Yes | None |
| Gemini CLI | Yes | None |
| Claude Code | No | `mkdir -p ~/.claude/skills && ln -sf "$PWD/arc-steward" ~/.claude/skills/arc-steward` |

Other harnesses (Cursor, Antigravity, Pi, ...) haven't been checked — if `~/.agents/skills/`
doesn't get picked up, look for that harness's own skills directory convention.

Then ask your agent to bootstrap: *"Set up the architecture documentation for this repo."* Add
*"use the Software Guidebook"* or *"only chapters 1, 3, 5 and 9"* if you want something other
than a full arc42 set; the agent will confirm both before writing anything. The set is written to
`docs/architecture/`; if that directory already holds content the skill didn't create, the agent
stops and asks you to move it or abort.

The verification harness needs nothing but `python3` — no pip install, no Node. It runs via
each harness's generic shell tool, so it needs no Claude-Code-specific mechanism.

### Updating

Read the release notes, then check out the latest release. The symlinks point at your clone, so
no re-linking is needed:

```bash
git -C arc-steward fetch --tags
git -C arc-steward checkout "$(git -C arc-steward describe --tags --abbrev=0 origin/main)"
```

To stay on a major version, check out a specific tag such as `v1.4.2` instead.

### Versioning

Releases are tagged `vMAJOR.MINOR.PATCH`, and the version number describes what the skill
persists in your repository. A major release means an existing documentation set has to be
migrated — its release notes explain how, with a migration script where practical. Minor and
patch releases never require changing an existing set, though a new check may report findings,
which the release notes announce. A set records its format version, and the skill refuses to
work on one written in a different format instead of failing silently.

## License

[MIT](LICENSE) for the skill. See [NOTICE](NOTICE) for the licenses covering the documentation
standards its output follows (arc42, the Software Guidebook).
