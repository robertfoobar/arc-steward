---
name: arc-steward
description: Use when a feature is complete and about to become a pull request, to bring the architecture documentation back in sync - refreshes context, component, deployment, sequence and ER diagrams from the feature diff. Also use to bootstrap architecture documentation in a repository that has none, following arc42 or Simon Brown's Software Guidebook, with all chapters or a selected subset.
allowed-tools: Read Write Edit Bash(git:*) Bash(python3:*)
---

# arc-steward

Keeps a fixed canon of architecture documentation current. Two modes, selected automatically:
`docs/arc42/index.md` missing means **bootstrap**, otherwise **refresh**. An explicit mode in the
request overrides the detection.

The documentation set is described by two values in the routing file, both read before anything
is written:

- **Documentation standard** — `arc42` (default) or `guidebook` for Simon Brown's Software
  Guidebook. Picks the chapter canon.
- **Documents** — `all` (default) or a list of chapter numbers. Picks a subset of that canon, for
  projects small enough that whole chapters would stay empty.

Read `conventions.md` before writing anything. It pins both chapter canons, the subset rules,
marker syntax and one diagram convention per artifact.

## Bootstrap

1. Read `docs/arc42/arc42.routing.md`. If absent, create `docs/arc42/` and copy
   `templates/arc42.routing.template.md` to `docs/arc42/arc42.routing.md`, then fill in **all
   seven** of its sections from the repository: detect the documentation language from existing
   docs and propose it for confirmation, detect schema sources, propose bounded contexts, and
   derive the path routing table from the repository's actual layout. Every example value in the
   template is a placeholder from a hypothetical project — replace all of them, do not edit
   around them. Ask the human to confirm the essential business flows — never invent that list.
   Leaving the path routing table unfilled, or leaving it matching the template's example paths,
   makes every later refresh find nothing and silently no-op, so it is not optional. As a sanity
   check on the finished table, confirm every path pattern in it matches at least one path in
   `git ls-files` — a pattern matching nothing is a wrong entry, not a placeholder for the future.
2. Settle the standard and the document selection before writing any chapter, because both are
   expensive to change afterwards. Propose `arc42` and `all` unless the repository argues
   otherwise, and have the human confirm. Deviating from `all` needs a reason from the
   repository, not a preference for less work — see `conventions.md` §1.4. Whatever is agreed
   goes into the routing file's **Documentation standard** and **Documents** sections; the
   harness reads them back, so an unrecorded choice is a broken one.
3. Create `docs/arc42/index.md` (entry point and chapter overview) plus every selected chapter,
   using the names from the conventions table for the configured standard and language. Without
   `index.md` the next invocation would detect "missing" again and re-run bootstrap instead of
   switching to refresh. If the selection is a subset, say in `index.md` which chapters are
   deliberately absent and why, so a reader can tell "not applicable" from "not written".
4. Generate what the code supports. Everything else gets `⚠️ TODO(human): <specific question>`.
5. Run the verification command below. Fix findings. Do not finish with findings outstanding.
6. Report the standard and selection used, which chapters are generated, which are stubs, and
   every open TODO.

## Refresh

1. Read `docs/arc42/arc42.routing.md`, including the documentation standard and the document
   selection — the routing table names artifacts by chapter number, and that number only
   resolves to a file through the canon in `conventions.md` §1. If the file does not exist, run
   bootstrap steps 1 and 2 first to create and fill it in, then continue here.
2. Determine the feature diff, without hard-coding a default branch name or remote. Probe
   for a comparison point rather than assuming one — `refs/remotes/origin/HEAD` is frequently
   unset (a single-branch clone, a shallow CI checkout, a remote added without
   `git remote set-head`), so a bare fallback to `origin/main` still breaks on a master-default
   repository:
   ```bash
   base=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null)
   if [ -z "$base" ]; then
     for candidate in origin/main origin/master main master; do
       git rev-parse --verify --quiet "$candidate" >/dev/null && base=$candidate && break
     done
   fi
   if [ -z "$base" ]; then
     echo "no recognizable default branch found" >&2
   else
     git diff "$(git merge-base "$base" HEAD)...HEAD" --name-only
   fi
   ```
   If `base` is still empty after the loop, stop and ask the human which branch to compare
   against — never guess a ref or silently diff against nothing.
3. Map the changed paths through the routing table to the affected artifacts. If nothing maps,
   report that and stop — no change is a valid outcome, not a failure.
4. For each affected artifact, edit only inside its `<!-- arc42:generated:id -->` block. Never
   touch a line outside a marked block.
5. If the set has a glossary chapter, any new domain entity gets an entry there.
6. Run the verification command below. Fix findings.
7. Report what changed, and what was deliberately left alone and why.

## Verification

Run from the repository root, with one `--schema-glob` per entry in the routing file's schema
sources. `<skill-dir>` is the directory this SKILL.md was loaded from — e.g.
`~/.claude/skills/arc-steward`, `~/.agents/skills/arc-steward`, or a project-local
`.agents/skills/arc-steward` — never hard-code one location, since it varies by harness and
install:

```bash
python3 <skill-dir>/scripts/verify.py docs/arc42 \
  --repo-root . \
  --schema-glob 'backend/src/db/migrations/*.sql'
```

The command reports which schema globs ran and how many files each matched, and says plainly
when none were given that ER entity resolution against schema sources is disabled — an unfilled
schema-sources section in the routing file is otherwise indistinguishable from a genuinely
database-free project. It says the same when the routing file itself is absent, in which case
the standard, the document selection and the path routing go unchecked. It also reports how many
documents it scanned; scanning zero documents is always a failure, never a clean run — check the
directory argument if that happens.

The routing check is what makes a subset selection safe: it fails the run when a selected chapter
has no file, and when the path routing table targets a chapter the set does not contain. Without
it that second case is invisible, because refresh would simply map nothing and report success.

Exit code 0 means clean. Exit code 1 lists findings as `file:line: [check] message`, or reports
zero documents scanned. Exit code 2 means the invocation was wrong — usually a mistyped
documentation directory. Never claim the documentation is updated without a clean run.

## Rules

`conventions.md` is binding for everything this procedure does not spell out: the two chapter
canons and their file names per language, the data-model subdirectory, the subset rules, the
provenance marker rules, the reference annotation syntax, one diagram convention per artifact,
the evidence rule, and how to treat chapters whose authoritative source lives elsewhere. Do not
restate its rules here — read it.
