# Contributing

## Workflow

1. Open an issue describing the problem or change before writing code, unless it's a trivial
   fix.
2. Branch from `main`: `feat/<issue-nr>-<short-description>` (letters, digits, `-` only).
3. Commit with [semantic commits](https://www.conventionalcommits.org/), scoped to the issue:
   `feat(#12): add ack toggle`. Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`,
   `chore`.
4. Open a PR against `main`. PRs are squash-merged, so intermediate commits don't need to be
   clean, but the PR title becomes the final commit subject — keep it accurate. Reference the
   issue with `Closes #<nr>` in the PR description.

## Before opening a PR

```bash
python3 -m unittest discover -s tests -v
```

If you changed `SKILL.md`, `conventions.md`, or anything under `scripts/` or `templates/`, also
run the security scan:

```bash
skillspector scan . --no-llm --baseline .skillspector-baseline.yaml
```

A new finding that's a genuine false positive (inherent to how this skill works, not a real
issue) gets added to `.skillspector-baseline.yaml` with a specific reason — not a blanket
"reviewed" note. A finding that isn't a false positive gets fixed instead.

## Code style

No inline comments — the existing code has none. If something needs explaining, either make the
name clearer or put the reasoning in `conventions.md`, the commit message, or the PR description.

## Rules and conventions

`conventions.md` is the source of truth for the arc42/Software Guidebook chapter canons, marker
syntax, and everything else the skill enforces. Changing behavior usually means updating
`conventions.md` and the corresponding check under `scripts/checks/` together, with a test.
