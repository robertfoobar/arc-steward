# Conventions

This is the detailed reference `SKILL.md` defers to. It exists so the skill's output stays
stable — across runs, across projects, across the two documentation standards and the two
documentation languages it supports. Read it before generating or refreshing any artifact.

## 1. Chapter names

Two documentation standards are supported. The routing file's **Documentation standard** section
selects one; an absent section means `arc42`. The two canons do not correspond chapter by
chapter, so moving an existing set from one to the other is a fresh bootstrap into an empty
directory, never a rename.

Chapter file names are fixed per standard and language. Never translate a chapter name ad hoc,
and never invent a file name that is not in these tables — always take it from here.

> `scripts/checks/routing.py` carries a machine-readable copy of both tables so the harness can
> verify the selection against what is on disk. Editing one without the other makes the check
> disagree with this document; they move together, and `tests/test_canon_sync.py` fails when
> they do not.

### 1.1 arc42 v9 — `arc42`

| # | English | German |
|---|---|---|
| 01 | `01-introduction-and-goals.md` | `01-einfuehrung-und-ziele.md` |
| 02 | `02-constraints.md` | `02-randbedingungen.md` |
| 03 | `03-context-and-scope.md` | `03-kontextabgrenzung.md` |
| 04 | `04-solution-strategy.md` | `04-loesungsstrategie.md` |
| 05 | `05-building-block-view.md` | `05-bausteinsicht.md` |
| 06 | `06-runtime-view.md` | `06-laufzeitsicht.md` |
| 07 | `07-deployment-view.md` | `07-verteilungssicht.md` |
| 08 | `08-crosscutting-concepts.md` | `08-querschnittliche-konzepte.md` |
| 09 | `09-architecture-decisions.md` | `09-architekturentscheidungen.md` |
| 10 | `10-quality-requirements.md` | `10-qualitaetsanforderungen.md` |
| 11 | `11-risks-and-technical-debt.md` | `11-risiken-und-technische-schulden.md` |
| 12 | `12-glossary.md` | `12-glossar.md` |

### 1.2 Software Guidebook — `guidebook`

Simon Brown's Software Guidebook, from *Software Architecture for Developers*.

| # | English | German |
|---|---|---|
| 01 | `01-context.md` | `01-kontext.md` |
| 02 | `02-functional-overview.md` | `02-funktionaler-ueberblick.md` |
| 03 | `03-quality-attributes.md` | `03-qualitaetsmerkmale.md` |
| 04 | `04-constraints.md` | `04-randbedingungen.md` |
| 05 | `05-principles.md` | `05-prinzipien.md` |
| 06 | `06-software-architecture.md` | `06-softwarearchitektur.md` |
| 07 | `07-external-interfaces.md` | `07-externe-schnittstellen.md` |
| 08 | `08-code.md` | `08-code.md` |
| 09 | `09-data.md` | `09-daten.md` |
| 10 | `10-infrastructure-architecture.md` | `10-infrastrukturarchitektur.md` |
| 11 | `11-deployment.md` | `11-deployment.md` |
| 12 | `12-operation-and-support.md` | `12-betrieb-und-support.md` |
| 13 | `13-development-environment.md` | `13-entwicklungsumgebung.md` |
| 14 | `14-decision-log.md` | `14-entscheidungslog.md` |

Unlike arc42, which originates in German and carries an authoritative German chapter set, the
Software Guidebook is published in English only. The German column above is this skill's own
translation, chosen so that a German documentation set is not half English. It follows the same
spelling rules as the arc42 column — lower case, hyphenated, umlauts transliterated as `ae`,
`oe`, `ue` — and `08-code.md` and `11-deployment.md` are identical in both columns because the
German technical term is the English word.

Treat these names as fixed from here on. They are not authoritative in the way the arc42 names
are, but a rename after the fact breaks every link in every set already generated, so a better
translation is not worth the churn.

### 1.3 The data-model subdirectory

The chapter carrying the data model additionally has a subdirectory, because the technical ER
diagrams are split one file per bounded context and do not fit inside a single chapter file:

| Standard | Language | Directory | Fixed files |
|---|---|---|---|
| `arc42` | English | `08-data-model/` | `domain.md`, `overview.md` |
| `arc42` | German | `08-datenmodell/` | `fachlich.md`, `uebersicht.md` |
| `guidebook` | English | `09-data/` | `domain.md`, `overview.md` |
| `guidebook` | German | `09-daten/` | `fachlich.md`, `uebersicht.md` |

Bounded-context file names inside that subdirectory are not fixed — they are derived from the
routing file's bounded-context list — but the fixed files above are exact and must not be
renamed.

### 1.4 Selecting a subset of chapters

The routing file's **Documents** section selects which chapters the set contains. `all` is the
default and the right answer for most projects: a chapter with nothing to say costs a paragraph,
not a page, because §5 and §6 keep it short by themselves. A list is for projects small enough
that whole chapters would stay genuinely empty.

Two rules hold whatever the selection, and the harness enforces both:

1. Every selected chapter exists as a file.
2. Every chapter the path routing table targets is selected.

Rule 2 is the load-bearing one. The routing table names artifacts by chapter number, and refresh
resolves that number to a file through the tables above. A number that resolves to a file the set
does not contain makes refresh find nothing and report "nothing mapped" — which `SKILL.md`
declares a valid outcome, so the failure is silent and permanent.

Never omit a chapter to save effort. Omit it only when the project genuinely has no such content,
and say so where a reader would look for it.

## 2. Provenance markers

Generated content lives inside a fenced block:

```
<!-- arc-steward:generated:<block-id> -->
...generated content...
<!-- /arc-steward:generated -->
```

The checker (`scripts/checks/markers.py`) enforces four rules:

1. **Balanced.** Every opening marker has a matching closing marker before the file ends. An
   opening marker with no closing marker is reported as an unclosed block.
2. **Not nested.** A new opening marker may not appear while a block is already open in the
   same file.
3. **Unique id per file.** `<block-id>` must not repeat within a document.
4. **Id pattern.** `<block-id>` matches `[a-z0-9-]+` — lowercase letters, digits and hyphens
   only.

Refresh mode never edits anything outside a marked block. Hand-written prose that lives
between blocks, or in a file with no blocks at all, is untouched by definition — it is not
protected by instruction, it is structurally outside the region the refresh is allowed to
rewrite.

## 3. Reference annotations

Directly below a generated diagram, inside the same generated block, list every repo-relative
path the diagram depicts:

```
<!-- arc-steward:refs
path/to/file/one
path/to/file/two
-->
```

A generated table derived from the code carries the same annotation below it, listing the paths
it was derived from, so a reviewer can see which paths the routing table must send to that block.

The opening line is exactly `<!-- arc-steward:refs` with nothing after it on that line, one path per
line, and a closing line containing only `-->`. The checker
(`scripts/checks/references.py`) confirms every listed path exists in the repo. When the
diagram is an `erDiagram`, the checker additionally resolves every entity name it finds against
the project's schema sources — configured via `--schema-glob` — so entity names must match the
schema, not a paraphrase of it.

## 4. Diagram conventions

Every diagram is Mermaid, fenced with ```` ```mermaid ````, using one of the types
`scripts/checks/mermaid.py` accepts: `flowchart`, `graph`, `sequenceDiagram`, `erDiagram`,
`classDiagram`, `stateDiagram-v2`, `C4Context`. The artifact canon below only uses a subset of
those.

### Context diagram

`flowchart TD`. The system under documentation is a single node. External actors and systems
surround it. No internal structure — that belongs to the component diagram, not here.

### Component diagram

`flowchart TD`. One `subgraph` per deployable unit. Nodes inside a subgraph are that
deployable's components. Edges are labelled with the interaction they represent, not left bare.

### Sequence diagram

`sequenceDiagram`, one diagram per entry in the routing file's flow list. The initiating actor
is the first participant. No more than seven participants in one diagram.

### Deployment diagram

`flowchart TD`. One `subgraph` per host or container runtime.

### Domain ER diagram

`erDiagram`. Domain entities and their relationships only — no columns, no technical join
tables. This is the business-readable model, the `domain.md` / `fachlich.md` of the data-model
subdirectory in §1.3.

### Technical ER diagram

`erDiagram`, one file per bounded context. Every entity carries all of its columns, each with
its type and a `PK`, `FK` or `UK` marker where it applies. A foreign key that points out of the
current bounded context references the target entity by name without redefining it — the
entity's full column list lives only in its own bounded context's file.

## 5. Evidence rule

Never write a plausible guess. Where the code does not support a statement the document is
about to make, write:

```
⚠️ TODO(human): <specific question>
```

A flagged gap is a successful outcome of a run, not a failure of it — it means the skill found
the limit of what the evidence supports and said so, instead of inventing the rest.

## 6. Chapters with an authoritative source

Some chapters are commonly maintained elsewhere in a repo already — dependency manifests and CI
policy for constraints, an ADR directory for decisions, a backlog or issue tracker and security
findings for risks and technical debt:

| Standard | Chapters with a likely source elsewhere |
|---|---|
| `arc42` | 02 constraints, 04 solution strategy, 09 architecture decisions, 11 risks and technical debt |
| `guidebook` | 04 constraints, 05 principles, 14 decision log |

Where such a source exists, write a short orientation paragraph and link to it. Never copy
content that is maintained elsewhere — a copy drifts from its source the first time either one
changes, which is the exact failure mode this skill exists to prevent.

Where no such source exists in the repository, the evidence rule from section 5 applies: flag
the gap with `⚠️ TODO(human): <specific question>` instead of writing the orientation paragraph
anyway. Every link to a source must be relative and resolvable within the repository — the link
checker (`scripts/checks/links.py`) fails the run on a link target that does not exist.
