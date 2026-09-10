# 06 Software Architecture

arc-steward has two kinds of building blocks. The instruction documents are loaded into the
agent's context and steer its judgement: what to write, where, and when to stop and ask. The
verification harness is ordinary deterministic code the agent runs afterwards, so that every rule
it covers does not rest on the agent having followed an instruction. Both ship together as one
directory — the only deployable unit.

## Components

<!-- arc42:generated:components -->
```mermaid
flowchart TD
  subgraph SkillDir["arc-steward skill directory, installed by git clone and symlink"]
    subgraph Instructions["Agent instructions, loaded into the agent context"]
      Skill["SKILL.md: mode selection and procedures"]
      Conventions["conventions.md: canons, markers, diagram rules"]
      Template["templates/arc42.routing.template.md"]
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
  Skill -->|copies on bootstrap| Template
  Skill -->|runs before finishing| Verify
  Skill -->|has the agent write generated blocks in| Target
  Verify -->|reads docs and schema sources of| Target
  Verify -->|per document| Markers
  Verify -->|per document| Mermaid
  Verify -->|per document| References
  Verify -->|per document| Links
  Verify -->|once per documentation set| Routing
  Mermaid -->|extracts mermaid fences via| Fences
  References -->|extracts mermaid fences via| Fences
  Routing -.->|mirrors the chapter tables of| Conventions
```

<!-- arc42:refs
SKILL.md
conventions.md
templates/arc42.routing.template.md
scripts/verify.py
scripts/checks/markers.py
scripts/checks/mermaid.py
scripts/checks/references.py
scripts/checks/links.py
scripts/checks/routing.py
scripts/checks/fences.py
-->
<!-- /arc42:generated -->

## Checks

<!-- arc42:generated:checks -->
| Check | Scope | Fails the run when |
|---|---|---|
| `markers` | Every document | A provenance marker is unclosed, nested, duplicated within the file, closes without an opening, or its id does not match `[a-z0-9-]+` |
| `mermaid` | Every document | A mermaid fence is unterminated or empty, has an unknown diagram type, unbalanced brackets, or a `subgraph` without `end` |
| `references` | Every document | A path in a reference annotation does not exist, or — when schema globs are given — an `erDiagram` entity is missing from the schema sources |
| `links` | Every document | A relative link target or an anchor does not resolve |
| `routing` | The documentation set | The standard or language is unknown, a selected chapter has no file, or the path routing table targets a chapter the set does not contain |

`scripts/verify.py` exits 0 when clean, 1 on findings or when it scanned zero documents, and 2 on
a wrong invocation. The exact command is in [Verification](../../SKILL.md#verification).
`routing.py` carries its own copy of the chapter tables from `conventions.md`;
`tests/test_canon_sync.py` fails when the two copies disagree.

<!-- arc42:refs
scripts/verify.py
scripts/checks
tests/test_canon_sync.py
-->
<!-- /arc42:generated -->

## Runtime flows

### Bootstrap

<!-- arc42:generated:flow-bootstrap -->
```mermaid
sequenceDiagram
  actor Developer
  participant Agent as Coding agent
  participant Skill as SKILL.md and conventions.md
  participant Repo as Target repository
  participant Verify as scripts/verify.py
  Developer->>Agent: Set up the architecture documentation
  Agent->>Skill: load procedure and conventions
  Agent->>Repo: look for docs/arc42/index.md
  Repo-->>Agent: missing, so bootstrap
  opt arc42.routing.md is missing
    Agent->>Repo: copy the routing template, fill every section from the repository layout
  end
  Agent->>Developer: propose language, standard and documents, ask for the business flows
  Developer-->>Agent: confirm
  Agent->>Repo: record the choices in arc42.routing.md
  Agent->>Repo: write index.md and every selected chapter, TODO(human) where evidence is missing
  loop until the run is clean
    Agent->>Verify: python3 verify.py docs/arc42 with one schema glob per schema source
    Verify-->>Agent: exit code and findings
    Agent->>Repo: fix findings
  end
  Agent-->>Developer: report standard, selection, generated chapters, stubs and open TODOs
```

<!-- arc42:refs
SKILL.md
conventions.md
templates/arc42.routing.template.md
scripts/verify.py
-->
<!-- /arc42:generated -->

### Refresh

<!-- arc42:generated:flow-refresh -->
```mermaid
sequenceDiagram
  actor Developer
  participant Agent as Coding agent
  participant Routing as arc42.routing.md
  participant Git as git
  participant Docs as Chapter files
  participant Verify as scripts/verify.py
  Developer->>Agent: Feature complete, refresh the docs before the pull request
  Agent->>Routing: read standard, documents and path routing
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
        Agent->>Verify: python3 verify.py docs/arc42
        Verify-->>Agent: exit code and findings
        Agent->>Docs: fix findings
      end
      Agent-->>Developer: report what changed and what was left alone
    end
  end
```

<!-- arc42:refs
SKILL.md
scripts/verify.py
-->
<!-- /arc42:generated -->
