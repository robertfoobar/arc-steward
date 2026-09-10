# 04 Constraints

The constraints on arc-steward are maintained where they take effect — the skill's frontmatter,
the CI workflow, the contribution guide, the license files. This chapter only points at them, so
that it cannot drift from them.

<!-- arc-steward:generated:constraints -->
| Constraint | Where it is defined |
|---|---|
| The tools the skill needs — read, write and edit files, run `git` and `python3` — are declared as pre-approved; the field is experimental and does not restrict the agent | `allowed-tools` in the frontmatter of [`SKILL.md`](../../SKILL.md) |
| The harness uses the Python standard library only — no pip install, no Node | [`scripts/verify.py`](../../scripts/verify.py) and [Installation](../../README.md#installation) |
| No harness-specific mechanism; the skill directory is never hard-coded | [Verification](../../SKILL.md#verification) |
| Every diagram is Mermaid, of a type the harness recognizes | [Diagram conventions](../../conventions.md#4-diagram-conventions) |
| The documentation set always lives in `docs/architecture/`, whatever the standard | [`SKILL.md`](../../SKILL.md) |
| Chapter file names come from the fixed canon tables, never from ad-hoc translation | [Chapter names](../../conventions.md#1-chapter-names) |
| CI runs the unit tests, including a verification of this documentation set, and a SkillSpector scan on every push to `main` and every pull request; the scan fails on any finding the reviewed baseline does not cover | [`ci.yml`](../../.github/workflows/ci.yml), [`test_own_docs.py`](../../tests/test_own_docs.py), [`.skillspector-baseline.yaml`](../../.skillspector-baseline.yaml) |
| The skill is MIT-licensed; the arc42 and Guidebook structures it follows keep their own licenses | [`LICENSE`](../../LICENSE), [`NOTICE`](../../NOTICE) |
| Releases are SemVer tags; the major version tracks the persisted format, whose version is recorded in the routing file, and `docs/architecture/arc-steward.routing.md` never moves | [Versioning](../../CONTRIBUTING.md#versioning-and-the-changelog), [`RELEASING.md`](../../RELEASING.md), [Format version](../../conventions.md#7-format-version), [`CHANGELOG.md`](../../CHANGELOG.md) |
| Semantic, issue-scoped commits, squash-merged pull requests, no inline code comments | [`CONTRIBUTING.md`](../../CONTRIBUTING.md) |
| Read and write scope that security reports are measured against | [`SECURITY.md`](../../SECURITY.md) |

<!-- arc-steward:refs
SKILL.md
scripts/verify.py
conventions.md
.github/workflows/ci.yml
tests/test_own_docs.py
.skillspector-baseline.yaml
LICENSE
NOTICE
CONTRIBUTING.md
CHANGELOG.md
RELEASING.md
SECURITY.md
-->
<!-- /arc-steward:generated -->
