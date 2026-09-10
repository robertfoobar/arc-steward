# arc-steward — Architecture Documentation

This is the architecture documentation of arc-steward itself, following Simon Brown's
[Software Guidebook](https://leanpub.com/software-architecture-for-developers), in English. It is
maintained by arc-steward: before each pull request, the refresh step that
[`CONTRIBUTING.md`](../../CONTRIBUTING.md#before-opening-a-pr) asks for updates the generated
blocks from the feature diff through [`arc-steward.routing.md`](arc-steward.routing.md). The directory and marker names are tool conventions, independent of the standard — see
decision 11 in the [decision log](14-decision-log.md).

## Chapters

| # | Chapter | Content |
|---|---|---|
| 01 | [Context](01-context.md) | Who and what arc-steward interacts with — context diagram |
| 02 | [Functional overview](02-functional-overview.md) | Modes, verification and the configurable capabilities |
| 03 | [Quality attributes](03-quality-attributes.md) | What the design optimizes for, and the limits of each mechanism |
| 04 | [Constraints](04-constraints.md) | Pointers to where each constraint is defined |
| 05 | [Principles](05-principles.md) | Pointer to the design principles, plus the two that shape the skill itself |
| 06 | [Software architecture](06-software-architecture.md) | Component diagram, the checks, bootstrap and refresh sequences |
| 14 | [Decision log](14-decision-log.md) | Architecturally significant decisions and their reasons |

## Deliberately absent chapters

This is a subset of the Guidebook. The chapters below are not missing: the project either has no
such content, or the content is maintained elsewhere and linked here.

| # | Chapter | Why it is absent |
|---|---|---|
| 07 | External interfaces | The interfaces are the `SKILL.md` frontmatter the harness reads, the `verify.py` command line, the routing file format, and the marker and reference syntax target repositories carry. They are specified in [`SKILL.md`](../../SKILL.md#verification), the [routing template](../../templates/arc-steward.routing.template.md) and [`conventions.md`](../../conventions.md#2-provenance-markers), and summarized in [chapter 06](06-software-architecture.md#checks) |
| 08 | Code | A few hundred lines of standard-library Python in small single-purpose modules; the component diagram in [chapter 06](06-software-architecture.md#components) covers them at the level a reader needs |
| 09 | Data | No database and no persisted state beyond the Markdown files the skill writes |
| 10 | Infrastructure architecture | No infrastructure of its own — the skill runs inside the developer's agent harness; CI runs on GitHub-hosted runners, defined in [`ci.yml`](../../.github/workflows/ci.yml) |
| 11 | Deployment | Installation is a `git clone` plus a symlink, described under [Installation](../../README.md#installation) |
| 12 | Operation and support | No running system to operate; vulnerability reporting is in [`SECURITY.md`](../../SECURITY.md) |
| 13 | Development environment | Maintained in [`CONTRIBUTING.md`](../../CONTRIBUTING.md) |

## Verifying this set

```bash
python3 scripts/verify.py docs/architecture --repo-root .
```

No `--schema-glob` is passed, because the project has no schema sources. The unit test suite runs
the same verification in CI, so a renamed file or heading that breaks this set fails the build.
