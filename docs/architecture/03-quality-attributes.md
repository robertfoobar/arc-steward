# 03 Quality Attributes

The quality attributes below are the ones the repository actually argues for and, where it can,
enforces mechanically. Each names the mechanism that carries it and the limit of that mechanism.

⚠️ TODO(human): Is the order below the intended priority when two attributes conflict — for
example, when a stricter verification check would cost portability or add a dependency?

<!-- arc-steward:generated:quality-attributes -->
| # | Attribute | Scenario | Carried by | Known limit |
|---|---|---|---|---|
| 1 | Trustworthiness of the output | A diagram names a path or ER entity that no longer exists; the run fails instead of shipping the stale name | Reference annotations checked against the repository and the schema sources; the evidence rule | Component names inside `flowchart` diagrams are not checked against the code, and Mermaid is sanity-checked, not parsed |
| 2 | No silent no-op | The routing table points at a chapter the set does not contain; the run fails instead of every later refresh reporting "nothing mapped" | The routing check in `scripts/checks/routing.py` | The harness does not match routing patterns against `git ls-files`; `SKILL.md` asks the agent to do that during bootstrap |
| 3 | Prose safety | A refresh rewrites a diagram; the hand-written paragraphs around it are byte-identical afterwards | Provenance markers — refresh may only edit inside a marked block | The boundary is enforced by the procedure, not by the harness; the harness checks marker balance, not what changed outside the blocks |
| 4 | Output stability | Two runs, or two projects, produce the same chapter file names for the same standard and language | Fixed canons in `conventions.md`, mirrored in `routing.py` and kept equal by `tests/test_canon_sync.py` | — |
| 5 | Portability | The skill runs in any harness that reads `~/.agents/skills/`, with nothing installed but `python3` and `git` | Standard-library-only harness, invoked through the harness's generic shell tool; the skill path is resolved from wherever it was loaded | Only the harnesses listed under Installation in the README are verified |
| 6 | Reviewability | A reviewer sees the documentation change rendered in the pull request diff, next to the code that caused it | Mermaid only, no render step | Mermaid ER diagrams cannot show indexes or check constraints |
| 7 | Confidentiality | No schema is sent to a third-party render service to draw a diagram | Mermaid only — no PlantUML or Kroki server | Code and schema are still visible to GitHub and to the agent's model provider |

<!-- arc-steward:refs
README.md
SKILL.md
conventions.md
scripts/verify.py
scripts/checks/routing.py
tests/test_canon_sync.py
-->
<!-- /arc-steward:generated -->

Sources: [Design principles](../../README.md#design-principles) and
[`conventions.md`](../../conventions.md).
