# Documentation Routing Configuration

Read by the `arc42-refresh` skill. Edit this file, not the skill.

> Every example value below — the schema glob, the bounded contexts, the business flow, and the
> four path-routing rows — is illustrative only, drawn from a hypothetical Python/SQL backend.
> Replace all of them with values specific to this repository. Leaving one in place produces a
> routing table that matches nothing in a different stack, and nothing else will catch that.

## Documentation standard

`arc42`

Which chapter canon this documentation set follows: `arc42`, or `guidebook` for Simon Brown's
Software Guidebook. An absent section means `arc42`. The value is not a rename switch — changing
it later means bootstrapping again into an empty directory, because the chapter files of the two
standards do not correspond one to one.

## Documentation language

`en`

## Documents

`all`

Which chapters of the standard this documentation set actually contains. `all` is the default and
the right answer for most projects: a chapter with nothing to say costs one paragraph, because the
evidence rule and the authoritative-source rule keep it short by themselves.

Replace `all` with a list when a project is small enough that whole chapters would stay empty —
each entry starts with the two-digit chapter number of the configured standard:

> - `01` — Introduction and Goals
> - `03` — Context and Scope
> - `05` — Building Block View
> - `09` — Architecture Decisions

The verification harness enforces two rules here, because getting either wrong turns every later
refresh into a silent no-op:

1. Every chapter selected here exists as a file in this directory.
2. Every chapter the path routing table points at is selected here.

## Schema sources

Glob patterns, relative to the repository root, that define the database schema. Passed to the
verification harness as `--schema-glob`. Leave empty if the project has no database.

- `backend/src/db/migrations/*.sql` — EXAMPLE, replace with this project's own glob(s), or
  remove this line if the project has no database.

## Bounded contexts

One technical ER diagram is generated per entry, in the data-model subdirectory of whichever
chapter carries the data model under the configured standard and language — see `conventions.md`
§1 for the exact directory name.

- `users` — EXAMPLE, replace with this project's actual bounded contexts.
- `signals` — EXAMPLE, replace with this project's actual bounded contexts.

## Essential business flows

One sequence diagram per entry, in the runtime chapter. This list is curated by hand: without it
every new endpoint grows a diagram and the runtime view drowns in trivia. Each entry names the
flow and the entry point that starts it.

| Flow | Entry point |
|---|---|
| EXAMPLE — User sign-in (replace with this project's actual flows) | `backend/src/adapters/http/auth.py` |

## Path routing

Which code paths affect which artifact. A change touching a path triggers a review of every
artifact listed against it. Each artifact begins with the two-digit chapter number, which is what
the verification harness reads. Every path pattern below must match at least one path in
`git ls-files` once filled in — a pattern matching nothing means it was never replaced.

| Path pattern | Artifacts |
|---|---|
| EXAMPLE — `backend/src/domain/**` | 05 building blocks, 08 domain model, 12 glossary |
| EXAMPLE — `backend/src/db/migrations/**` | 08 technical model, 08 overview |
| EXAMPLE — `backend/src/adapters/**` | 03 context, 05 building blocks |
| EXAMPLE — `devops/**`, `docker-compose*.yml`, `Dockerfile` | 07 deployment |
