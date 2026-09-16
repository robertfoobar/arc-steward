# Documentation Routing Configuration

Read by the `arc-steward` skill. Edit this file, not the skill.

## Format version

`1`

Which version of arc-steward's persisted format this set follows: the directory, this file, the
markers, the chapter file names and the data-model layout. A newer arc-steward reads it to recognize a set written by an
older one. Do not change it by hand, a migration does.

## Documentation standard

`guidebook`

Which chapter canon this documentation set follows: `arc42`, or `guidebook` for Simon Brown's
Software Guidebook. An absent section means `arc42`. The value is not a rename switch — changing
it later means bootstrapping again into an empty directory, because the chapter files of the two
standards do not correspond one to one.

## Documentation language

`en`

## Documents

- `01` — Context
- `02` — Functional overview
- `03` — Quality attributes
- `04` — Constraints
- `05` — Principles
- `06` — Software architecture
- `14` — Decision log

The remaining chapters are deliberately absent; `index.md` gives the reason for each.

The verification harness enforces two rules here, because getting either wrong turns every later
refresh into a silent no-op:

1. Every chapter selected here exists as a file in this directory.
2. Every chapter the path routing table points at is selected here.

## Schema sources

None. This project has no database, so ER entity resolution is disabled on purpose.

## Bounded contexts

None. Without a database there is no technical ER diagram to split.

## Essential business flows

One sequence diagram per entry, in chapter 06. This list is curated by hand: without it every new
code path grows a diagram and the runtime view drowns in trivia. Each entry names the flow and the
entry point that starts it.

| Flow | Entry point |
|---|---|
| Bootstrap | `SKILL.md` |
| Refresh | `SKILL.md` |

## Path routing

Which code paths affect which artifact. A change touching a path triggers a review of every
artifact listed against it. Each artifact begins with the two-digit chapter number, which is what
the verification harness reads. Every path pattern below matches at least one path in
`git ls-files`; `tests/test_own_docs.py` checks each against the files in the repository. Artifacts are named by chapter number
and generated block id. Only generated blocks are routed — a refresh never edits hand-written
prose, so chapters 05 and 14 have nothing to route to.

| Path pattern | Artifacts |
|---|---|
| `SKILL.md` | 01 context, 02 functions, 03 quality-attributes, 04 constraints, 06 components, 06 checks, 06 flow-bootstrap, 06 flow-refresh |
| `conventions.md` | 01 context, 02 functions, 03 quality-attributes, 04 constraints, 06 components, 06 checks, 06 flow-bootstrap |
| `templates/**` | 02 functions, 06 components, 06 flow-bootstrap |
| `scripts/**` | 01 context, 03 quality-attributes, 04 constraints, 06 components, 06 checks, 06 flow-bootstrap, 06 flow-refresh |
| `tests/**` | 03 quality-attributes, 04 constraints, 06 checks |
| `README.md` | 01 context, 03 quality-attributes, 04 constraints |
| `.github/workflows/**`, `.skillspector-baseline.yaml` | 04 constraints |
| `LICENSE`, `NOTICE`, `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md`, `RELEASING.md` | 04 constraints |
