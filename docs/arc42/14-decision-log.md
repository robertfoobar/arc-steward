# 14 Decision Log

The repository has no ADR directory, so the decisions are logged here. The reasons are taken from
the README, `conventions.md` and the message of the commit named in each entry — squash-merged
pull requests, so the commit message carries the pull request description.

| # | Date | Decision | Why | Consequence | Commit |
|---|---|---|---|---|---|
| 1 | 2026-09-04 | Diagrams are Mermaid only | GitHub renders Mermaid in the pull request diff, where the review happens; PlantUML needs a render step, and a public PlantUML or Kroki server would receive the schema | No render pipeline; ER diagrams cannot show indexes or check constraints, which stay in the schema sources | `d28f2e2` |
| 2 | 2026-09-04 | Generated content lives inside `arc42:generated` provenance markers | Hand-written prose must survive every refresh structurally, not because a prompt asked politely | Refresh is confined to marked blocks; hand-written chapters are never refreshed at all | `d28f2e2` |
| 3 | 2026-09-04 | Missing evidence becomes `⚠️ TODO(human)`, never a guess | A plausible invented statement is worse than a visible gap, because nobody knows to question it | Bootstrap output contains open questions by design | `d28f2e2` |
| 4 | 2026-09-04 | The trigger is a workflow step before the pull request, not a CI gate or a hook | That is the one point where closing the gap is cheap, while the diff that changed the architecture is still in front of the author | Drift is only prevented where the workflow step is actually run | `d28f2e2` |
| 5 | 2026-09-04 | A standard-library Python harness verifies what can be checked mechanically, with structural rather than full Mermaid checks | A diagram naming something that no longer exists is worse than no diagram; real Mermaid parsing would drag in Node and a headless browser | The harness runs with bare `python3`, but sanity-checks Mermaid rather than parsing it | `d28f2e2` |
| 6 | 2026-09-04 | One routing file per target repository carries language, paths, bounded contexts and flows | One skill has to serve different stacks without code changes; the flow list is curated so the runtime view does not grow a diagram per endpoint | Refresh quality depends on the routing table, hence decision 7 | `d28f2e2` |
| 7 | 2026-09-04 | The routing configuration is checked, not trusted | A routing table targeting an absent chapter makes every refresh report "nothing mapped", indistinguishable from a real no-op | `routing.py` mirrors the chapter canons of `conventions.md` | `d28f2e2` |
| 8 | 2026-09-04 | Technical ER diagrams are split one file per bounded context | A single ER diagram of 20+ tables is unreadable in any notation | Cross-context foreign keys reference entities by name only | `d28f2e2` |
| 9 | 2026-09-10 | Renamed from arc42-refresh to arc-steward; installation via `~/.agents/skills/`, no hard-coded skill path | The skill covers arc42 and the Software Guidebook, so the arc42-only name no longer fit; the harness path must work wherever the skill was loaded from | The directory `docs/arc42/` and the `arc42:` marker prefix were not renamed, so Guidebook sets live under an arc42 name | `3575958` |
| 10 | 2026-09-10 | CI runs a SkillSpector scan, pinned to one scanner version, against a reviewed baseline | The first scan found a real issue — the missing `allowed-tools` declaration; pinning keeps the scan from changing behaviour on upstream pushes | Each accepted false positive is recorded with a specific reason in `.skillspector-baseline.yaml` | `3575958`, `07c41d0`, `1768f34` |
| 11 | 2026-09-10 | The P2 findings on this documentation set are suppressed by a path-scoped rule, backed by a test that allows no HTML comment in `docs/arc42/` other than the skill's own marker syntax | Every refresh rewrites the generated blocks, which would invalidate exact fingerprints each time; a rule alone would hide a real hidden instruction next to a marker | `tests/test_own_docs.py` is the actual guard; the suppression rule only keeps the report readable | this change |

⚠️ TODO(human): Should future decisions keep being logged in this table, or move to one ADR file per
decision once the table outgrows a screen?
