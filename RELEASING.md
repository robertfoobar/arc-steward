# Releasing

For the maintainer. Contributing doesn't require any of this — see
[CONTRIBUTING.md](CONTRIBUTING.md).

## Choosing the version

Read the `[Unreleased]` entries in `CHANGELOG.md`:

- **MAJOR** if any entry is marked breaking. Every format-version bump is a major release.
- **MINOR** if any entry adds a capability, including a new or stricter check.
- **PATCH** otherwise: fixes that change neither the format nor the checks.

## Steps

1. Move the `[Unreleased]` entries under a new `## [X.Y.Z] - YYYY-MM-DD` heading, update the link
   references at the bottom of `CHANGELOG.md`, and merge that through a PR.
2. Right after that merge, tag the merge commit on `main` — never a local branch commit, and only
   with green CI. Until the first tag exists the install command in the README fails:
   `git fetch origin && git tag -a vX.Y.Z -m vX.Y.Z origin/main && git push origin vX.Y.Z`
3. Publish the release with that changelog section as notes:
   `gh release create vX.Y.Z --verify-tag --title vX.Y.Z --notes-file <file with the section>`
4. For a major release, check that the notes carry the migration instructions and point to the
   migration script, if there is one.
