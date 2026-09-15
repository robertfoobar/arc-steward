# 04 Constraints

The constraints on arc-steward are maintained where they take effect — the skill's frontmatter,
the CI workflow, the contribution guide, the license files. This chapter only points at them, so
that it cannot drift from them.

<!-- arc-steward:generated:constraints -->
| Constraint | Where it is defined |
|---|---|
| Only reading, writing and editing files are declared as pre-approved; `git` and `python3` go through the harness's own permission rules. The field is experimental and does not restrict the agent | `allowed-tools` in the frontmatter of [`SKILL.md`](../../SKILL.md) |
| The harness uses the Python standard library only — no pip install, no Node | [`scripts/verify.py`](../../scripts/verify.py) and [Installation](../../README.md#installation) |
| No harness-specific mechanism; the skill directory is never hard-coded | [Verification](../../SKILL.md#verification) |
| Every diagram is Mermaid, of a type the harness recognizes | [Diagram conventions](../../conventions.md#4-diagram-conventions) |
| The documentation set always lives in `docs/architecture/`, whatever the standard | [`SKILL.md`](../../SKILL.md) |
| Chapter file names come from the fixed canon tables, never from ad-hoc translation | [Chapter names](../../conventions.md#1-chapter-names) |
| CI runs the unit tests, including a verification of this documentation set, and a SkillSpector scan on every push to `main` and every pull request; the scan fails on any finding the reviewed baseline does not cover | [`ci.yml`](../../.github/workflows/ci.yml), [`test_own_docs.py`](../../tests/test_own_docs.py), [`.skillspector-baseline.yaml`](../../.skillspector-baseline.yaml) |
| The skill is MIT-licensed; it takes only the chapter structure and names from arc42 and the Software Guidebook, credits both, and copies none of their explanatory text; the arc42 chapter titles stay under CC BY-SA 4.0; liability under German law is set out separately | [`LICENSE`](../../LICENSE), [`NOTICE`](../../NOTICE), [`HAFTUNG.md`](../../HAFTUNG.md), [Licensing](../../CONTRIBUTING.md#licensing) |
| Releases are SemVer tags; the major version tracks the persisted format, whose version is recorded in the routing file, and `docs/architecture/arc-steward.routing.md` never moves | [Versioning](../../CONTRIBUTING.md#versioning-and-the-changelog), [`RELEASING.md`](../../RELEASING.md), [Format version](../../conventions.md#7-format-version), [`CHANGELOG.md`](../../CHANGELOG.md) |
| Semantic, issue-scoped commits, squash-merged pull requests, no inline code comments | [`CONTRIBUTING.md`](../../CONTRIBUTING.md) |
| Read and write scope that security reports are measured against; only the latest release is supported | [`SECURITY.md`](../../SECURITY.md) |

<!-- arc-steward:refs
SKILL.md
scripts/verify.py
conventions.md
.github/workflows/ci.yml
tests/test_own_docs.py
.skillspector-baseline.yaml
LICENSE
NOTICE
HAFTUNG.md
CONTRIBUTING.md
CHANGELOG.md
RELEASING.md
SECURITY.md
-->
<!-- /arc-steward:generated -->
