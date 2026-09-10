# 06 Software Architecture

arc-steward has two kinds of building blocks. The instruction documents are loaded into the
agent's context and steer its judgement: what to write, where, and when to stop and ask. The
verification harness is ordinary deterministic code the agent runs afterwards, so that every rule
it covers does not rest on the agent having followed an instruction. Both ship together as one
directory — the only deployable unit.

## Components

<!-- arc-steward:generated:components -->
```mermaid
flowchart TD
  subgraph SkillDir["arc-steward skill directory, a release checkout installed by symlink"]
    subgraph Instructions["Agent instructions, loaded into the agent context"]
      Skill["SKILL.md: mode selection and procedures"]
      Conventions["conventions.md: canons, markers, diagram rules"]
      Template["templates/arc-steward.routing.template.md"]
    end
    subgraph Harness["Verification harness, one python3 process"]
      Verify["scripts/verify.py: CLI, report, exit code"]
      Markers["checks/markers.py"]
      Mermaid["checks/mermaid.py"]
      References["checks/references.py"]
      Links["checks/links.py"]
      Routing["checks/routing.py"]
      Fences["checks/fences.py"]
    end
  end
  Target[("Target repository")]
  Skill -->|defers binding rules to| Conventions
  Skill -->|takes the routing file structure from| Template
  Skill -->|runs before finishing| Verify
  Skill -->|has the agent write generated blocks in| Target
  Verify -->|reads docs and schema sources of| Target
  Verify -->|per document| Markers
  Verify -->|per document| Mermaid
  Verify -->|per document| References
  Verify -->|per document| Links
  Verify -->|format version first, then once per documentation set| Routing
  Mermaid -->|extracts mermaid fences via| Fences
  References -->|extracts mermaid fences via| Fences
  Routing -.->|mirrors the chapter tables of| Conventions
```

<!-- arc-steward:refs
SKILL.md
conventions.md
templates/arc-steward.routing.template.md
scripts/verify.py
scripts/checks/markers.py
scripts/checks/mermaid.py
scripts/checks/references.py
scripts/checks/links.py
scripts/checks/routing.py
scripts/checks/fences.py
-->
<!-- /arc-steward:generated -->

## Checks

<!-- arc-steward:generated:checks -->
| Check | Scope | Fails the run when |
|---|---|---|
| `markers` | Every document | A provenance marker is unclosed, nested, duplicated within the file, closes without an opening, or its id does not match `[a-z0-9-]+` |
| `mermaid` | Every document | A mermaid fence is unterminated or empty, has an unknown diagram type, unbalanced brackets, or a `subgraph` without `end` |
| `references` | Every document | A path in a reference annotation does not exist, or — when schema globs are given — an `erDiagram` entity is missing from the schema sources |
| `links` | Every document | A relative link target or an anchor does not resolve |
| `routing` | The documentation set | Checked first: the format version is unparseable or differs from the supported one — that finding alone is reported and nothing else runs. Then: the standard or language is unknown or carries more than its value, a section heading appears twice, a selected chapter has no file, the path routing table targets a chapter the set does not contain, or a template placeholder marked `EXAMPLE` is left in the routing file |

`scripts/verify.py` exits 0 when clean, 1 on findings or when it scanned zero documents, and 2 on
a wrong invocation. The exact command is in [Verification](../../SKILL.md#verification).
`routing.py` carries its own copy of the chapter tables from `conventions.md`;
`tests/test_canon_sync.py` fails when the two copies disagree, and
`tests/test_format_version.py` when the supported format version differs between code,
`conventions.md`, the template and this repository's own routing file.

<!-- arc-steward:refs
scripts/verify.py
scripts/checks
tests/test_canon_sync.py
tests/test_format_version.py
-->
<!-- /arc-steward:generated -->

## Runtime flows

### Bootstrap

<!-- arc-steward:generated:flow-bootstrap -->
```mermaid
sequenceDiagram
  actor Developer
  participant Agent as Coding agent
  participant Skill as SKILL.md and conventions.md
  participant Repo as Target repository
  participant Verify as scripts/verify.py
  Developer->>Agent: Set up the architecture documentation
  Agent->>Skill: load procedure and conventions
  Agent->>Repo: look for docs/architecture/arc-steward.routing.md
  Repo-->>Agent: missing, so bootstrap
  alt docs/architecture holds foreign content
    Agent-->>Developer: ask to move that content elsewhere or abort
  else directory empty or absent
    Agent->>Repo: gather routing values from the repository layout, write nothing yet
    Agent->>Developer: propose language, standard and documents, ask for the business flows
    Developer-->>Agent: confirm
    Agent->>Repo: write arc-steward.routing.md in one go, structured like the template
    Agent->>Repo: write index.md and every selected chapter, TODO(human) where evidence is missing
  end
  loop until the run is clean
    Agent->>Verify: python3 verify.py docs/architecture with one schema glob per schema source
    Verify-->>Agent: exit code and findings
    Agent->>Repo: fix findings
  end
  Agent-->>Developer: report standard, selection, generated chapters, stubs and open TODOs
```

<!-- arc-steward:refs
SKILL.md
conventions.md
templates/arc-steward.routing.template.md
scripts/verify.py
-->
<!-- /arc-steward:generated -->

### Refresh

<!-- arc-steward:generated:flow-refresh -->
```mermaid
sequenceDiagram
  actor Developer
  participant Agent as Coding agent
  participant Routing as arc-steward.routing.md
  participant Git as git
  participant Docs as Chapter files
  participant Verify as scripts/verify.py
  Developer->>Agent: Feature complete, refresh the docs before the pull request
  Agent->>Routing: read format version, standard, documents and path routing
  alt format version differs from the supported one
    Agent-->>Developer: report both versions and stop, write nothing
  end
  Agent->>Git: probe origin/HEAD, then origin/main, origin/master, main, master
  alt no default branch found
    Agent-->>Developer: ask which branch to compare against
  else base found
    Agent->>Git: diff merge-base to HEAD, names only
    Git-->>Agent: changed paths
    Agent->>Routing: map changed paths to chapter artifacts
    alt nothing maps
      Agent-->>Developer: report that no artifact is affected
    else artifacts affected
      Agent->>Docs: patch only inside the affected generated blocks
      loop until the run is clean
        Agent->>Verify: python3 verify.py docs/architecture
        Verify-->>Agent: exit code and findings
        Agent->>Docs: fix findings
      end
      Agent-->>Developer: report what changed and what was left alone
    end
  end
```

<!-- arc-steward:refs
SKILL.md
scripts/verify.py
-->
<!-- /arc-steward:generated -->
