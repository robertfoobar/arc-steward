# 02 Functional Overview

arc-steward does one job: it keeps a fixed canon of architecture documentation in sync with the
code, at the moment a feature is about to become a pull request. It is not a CI gate and not a
hook — it runs when the agent is asked to, typically as a step of the development workflow.

<!-- arc42:generated:functions -->
| Function | Trigger | What happens |
|---|---|---|
| Mode selection | Every invocation | `docs/arc42/index.md` missing means bootstrap, otherwise refresh; an explicit mode in the request wins |
| Bootstrap | First run in a repository | Creates and fills the routing file if it is missing, settles standard and document selection with the human, writes `index.md` and every selected chapter |
| Refresh | Feature complete, before the pull request | Diffs the branch against the default branch, maps changed paths through the routing table, patches only the affected generated blocks |
| Verification | End of every bootstrap and refresh | Runs `scripts/verify.py`; the run is not finished until it exits 0 |

Generated content lives only inside provenance markers, and every statement the code does not
support becomes a `⚠️ TODO(human)` instead of a guess — see
[Provenance markers](../../conventions.md#2-provenance-markers) and
[Evidence rule](../../conventions.md#5-evidence-rule).

<!-- arc42:refs
SKILL.md
conventions.md
templates/arc42.routing.template.md
-->
<!-- /arc42:generated -->

The artifact canon, the two standards, the two languages and the chapter subset are described in
the README under [The artifact canon](../../README.md#the-artifact-canon) and
[Choosing a standard and a scope](../../README.md#choosing-a-standard-and-a-scope). The
step-by-step procedures are in [`SKILL.md`](../../SKILL.md); chapter
[06](06-software-architecture.md#runtime-flows) shows them as sequence diagrams.
