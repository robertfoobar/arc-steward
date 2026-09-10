# Security Policy

## Reporting a vulnerability

Report security issues privately via GitHub Security Advisories: open the **Security** tab on
this repository and select **Report a vulnerability**. Do not open a public issue for anything
that could be exploited before a fix ships.

If the Security tab has no "Report a vulnerability" option, private vulnerability reporting
hasn't been enabled yet on this repo — in that case, open a regular issue asking for a private
channel to be set up, without including exploit details.

## Scope

This skill reads files in the repository it runs against and writes only under
`docs/architecture/`: bootstrap creates the routing file, `index.md` and the chapter files there,
and refresh edits only inside `<!-- arc-steward:generated:id -->` blocks of those files.
`scripts/verify.py` reads files under the given docs directory and any paths matched by
`--schema-glob`. Relevant reports include anything that would make the skill read, write, or
execute outside of what `SKILL.md` and `conventions.md` describe.

## Supported versions

This is a single-branch project; only the latest commit on `main` is supported. There are no
maintained release branches to backport fixes to.
