# Security Policy

## Reporting a vulnerability

Report security issues privately via GitHub Security Advisories: open the **Security** tab on
this repository and select **Report a vulnerability**. Do not open a public issue for anything
that could be exploited before a fix ships.

## Scope

This skill reads files in the repository it runs against. It is written to change files only
under `docs/architecture/`: bootstrap creates the routing file, `index.md` and the chapter files
there, and refresh edits only inside `<!-- arc-steward:generated:id -->` blocks of those files.
These are instructions to the agent running the skill, not a sandbox — `allowed-tools`
pre-approves `Read Write Edit` for any path and restricts nothing. `scripts/verify.py` reads files
under the given docs directory and any paths matched by `--schema-glob`. Relevant reports include
anything that would make the skill read, write, or execute outside of what `SKILL.md` and
`conventions.md` describe, including repository content that steers the agent into doing so.

## Supported versions

Only the latest release is supported. Fixes land on `main` and ship with the next release; there
are no maintained release branches to backport them to.
