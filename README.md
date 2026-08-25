# arc42-refresh

An [Agent Skill](https://agentskills.io) that keeps a fixed canon of architecture
documentation artifacts up to date **after every feature**, rolled up into a complete
[arc42](https://arc42.org) documentation set.

> **Status: in development.** The design is settled; the skill itself is not implemented yet.

## Why another arc42 skill

The existing ones — [arc42-toolkit](https://github.com/MSiccDev/arc42-toolkit),
[generating-arc42](https://github.com/alicommit-malp/generating-arc42),
[enterprise-architecture-skill](https://github.com/gauravs19/enterprise-architecture-skill) —
are *first-creation* tools: analyse the repo, interview the architect, emit twelve chapters.
They solve the blank page.

They do not solve the harder problem: the documentation is stale two weeks later.

`arc42-refresh` is built for the steady state. It reads the feature diff, decides which
artifacts the change actually touches, and patches only those — surgically, leaving
hand-written prose intact.

## The artifact canon

| Artifact | arc42 chapter |
|---|---|
| Context diagram | 03 Context and scope |
| Component diagram | 05 Building block view |
| Runtime sequence diagrams | 06 Runtime view |
| Deployment diagram | 07 Deployment view |
| Domain-level ER diagram | 08 Crosscutting concepts |
| Technical ER diagrams, one per bounded context | 08 Crosscutting concepts |

All twelve arc42 chapters exist. Chapters with an authoritative source elsewhere in the repo
link to it generously rather than duplicating it.

## Design principles

- **Mermaid only.** GitHub renders it natively, so every diagram is readable in the PR diff
  where the review happens. No render step, and no shipping your schema to a public
  PlantUML or Kroki server.
- **Provenance markers.** Generated content lives inside `<!-- arc42:generated:id -->`
  fences. The refresh touches nothing outside them, so your prose is structurally safe —
  not merely protected by a polite prompt.
- **Evidence or a gap.** Where the code does not support a statement, the skill writes an
  explicit `TODO(human)` instead of inventing one.
- **Verify before finishing.** Mermaid parses, every named component and table resolves in
  the code, markers are balanced, links resolve.
- **Split by bounded context.** A single ER diagram of 20+ tables is unreadable in any
  notation. The file split does the grouping that layout directives cannot.

## Installation

Not yet available.

## License

[MIT](LICENSE) for the skill. The arc42 template itself is by Dr. Gernot Starke and
Dr. Peter Hruschka, licensed CC BY-SA 4.0.
