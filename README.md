# arc42-refresh

An [Agent Skill](https://agentskills.io) that keeps a fixed canon of architecture
documentation artifacts up to date **after every feature**, rolled up into a complete
[arc42](https://arc42.org) or [Software Guidebook](https://leanpub.com/software-architecture-for-developers)
documentation set.

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
- **Provenance markers.** Generated content lives inside `<!-- arc42:generated:id -->`
  fences. The refresh touches nothing outside them, so your prose is structurally safe —
  not merely protected by a polite prompt.
- **Evidence or a gap.** Where the code does not support a statement, the skill writes an
  explicit `TODO(human)` instead of inventing one.
- **Verify before finishing.** The harness checks what it can check mechanically: diagram
  type is recognized and brackets, `subgraph`/`end` pairs and provenance markers balance;
  `erDiagram` entity names resolve against the configured schema sources; internal links and
  anchors resolve; the routing configuration agrees with what is on disk. It does not parse
  Mermaid, and component names in `flowchart` diagrams are not checked against the code — see
  `conventions.md` for the exact rules.
- **Configuration is checked, not trusted.** A routing table pointing at a chapter that does not
  exist is the one failure that cannot be noticed by reading the output, because "nothing to
  update" and "nothing found" look identical. The harness fails the run instead.
- **Split by bounded context.** A single ER diagram of 20+ tables is unreadable in any
  notation. The file split does the grouping that layout directives cannot.

## Installation

Clone the repository and symlink it into your skills directory:

```bash
git clone git@github.com:robertfoobar/arc42-refresh.git ~/projects/arc42-refresh
ln -s ~/projects/arc42-refresh ~/.claude/skills/arc42-refresh
```

Then ask your agent to bootstrap: *"Set up the architecture documentation for this repo."* Add
*"use the Software Guidebook"* or *"only chapters 1, 3, 5 and 9"* if you want something other
than a full arc42 set; the agent will confirm both before writing anything.

The verification harness needs nothing but `python3` — no pip install, no Node.

## License

[MIT](LICENSE) for the skill. The arc42 template itself is by Dr. Gernot Starke and
Dr. Peter Hruschka, licensed CC BY-SA 4.0. The Software Guidebook structure is by Simon Brown,
from *Software Architecture for Developers*.
