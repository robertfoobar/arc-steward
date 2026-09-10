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

The suite includes a verification of the repository's own architecture documentation under
`docs/architecture/`. Keep it current by running the skill in refresh mode on your branch — ask
your agent to *"refresh the architecture documentation"* — and commit the result with the change.

Also run the security scan. CI fails on any finding the baseline doesn't cover:

```bash
uv tool install git+https://github.com/NVIDIA/skillspector.git@v2.11.2
export_dir=$(mktemp -d)
git ls-files -co --exclude-standard | tar -cf - -T - | tar -xf - -C "$export_dir"
(cd "$export_dir" && skillspector scan . --no-llm --baseline .skillspector-baseline.yaml)
```

A new finding that's a genuine false positive (inherent to how this skill works, not a real
issue) gets added to `.skillspector-baseline.yaml` with a specific reason — not a blanket
"reviewed" note. A finding that isn't a false positive gets fixed instead.

Baseline entries are fingerprints of the flagged text, so editing a passage that carries a
baselined finding (the install commands in `README.md`, the top of `SKILL.md`, the marker
section of `conventions.md`) makes the same finding reappear as new. Regenerate with
`skillspector baseline . --no-llm -o .skillspector-baseline.yaml` and carry the existing reasons
over — only if rule and file still match one to one.

## Code style

No inline comments — the existing code has none. If something needs explaining, either make the
name clearer or put the reasoning in `conventions.md`, the commit message, or the PR description.

## Rules and conventions

`conventions.md` is the source of truth for the arc42/Software Guidebook chapter canons, marker
syntax, and everything else the skill enforces. Changing behavior usually means updating
`conventions.md` and the corresponding check under `scripts/checks/` together, with a test.

## Versioning

Releases are tagged `vMAJOR.MINOR.PATCH`. The public contract is what the skill persists in a
user's repository — the documentation directory, the routing file and its sections, the marker
syntax, the chapter file names, the data-model layout (`conventions.md` §7) — plus the
`verify.py` arguments and exit codes. Output wording is not part of it.

- **MAJOR**: an existing documentation set has to be migrated, or the `verify.py` arguments or
  exit codes change incompatibly. The two go together in both directions: a change that requires
  a migration raises the format version, and every format-version bump is a major release. It bumps
  `FORMAT_VERSION` in `scripts/checks/routing.py`, `conventions.md` §7, the template and this
  repo's own routing file together (a test enforces that they agree), and ships migration notes —
  with a migration script where practical.
- **MINOR**: new capability. A new check that can report findings on existing sets is minor,
  and the release notes say so.
- **PATCH**: fixes that change neither the format nor the checks.

The routing file path `docs/architecture/arc-steward.routing.md` never changes — it is how a newer
skill finds a set written by an older one.

`tests/fixtures/format-1/` is a frozen format-1 set, and `tests/test_format_1_fixture.py` checks
that its markers, reference annotations, routing file and chapter names are all still recognized.
A change that breaks one of those tests is a format change: raise the format version, add a
fixture for the new version, and turn the old fixture's tests into a check that it is reported
as older. Never edit a frozen fixture to make it pass.

## Releasing

1. Move the `[Unreleased]` entries in `CHANGELOG.md` under a new `## [X.Y.Z] - YYYY-MM-DD`
   heading, update the link references at the bottom, and merge that through a PR.
2. Right after that merge, tag the merge commit on `main` — never a local branch commit, and
   only with green CI. Until the first tag exists the install command in the README fails:
   `git fetch origin && git tag -a vX.Y.Z -m vX.Y.Z origin/main && git push origin vX.Y.Z`.
3. Publish the release with that section as notes:
   `gh release create vX.Y.Z --verify-tag --title vX.Y.Z --notes-file <file with the section>`.
