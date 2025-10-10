---
description: Load constitution, validate memory bank, and launch autonomous execution without delay.
---

# /init — Session Spin-Up

## Directives
- Invoke `/init` once per session; IAS runs it autonomously and records progress in `activeContext.json`.
- Constitution files and memory-bank schemas must load without prompts. Missing assets trigger `/bootstrap` automatically.
- Schema validation uses `{IDE}/aegiside/memory-bank/schemas/*.schema.json` every time a file is read or regenerated.

## MCP Chain (auto)
1. `@mcp:filesystem` – Scan for IDE directories (`.windsurf/`, `.cursor/`, `.vscode/`, `.cline/`, `.qoder/`, `.trae/`, `.idle/`, `.zed/`, `.jetbrains/`, `.replit/`, `.pycharm/`) and locate `aegiside/memory-bank/` for the eight essential files.
2. `@mcp:sequential-thinking` – Determine if `/bootstrap` or `/blueprint create …` must run before continuing.
3. `@mcp:filesystem` – Load the eight schema files (`activeContext.json`, `scratchpad.json`, `kanban.json`, `mistakes.json`, `systemPatterns.json`, `progress.json`, `roadmap.json`, `memory.json`) plus helper schemas (`helpers/common-mistakes.json`, `helpers/error-recovery.json`, `helpers/tool-usage-patterns.json`) and `core/schemas/README.md` for reference.
4. `@mcp:math` – Compute readiness score (schema count, size compliance ≤10 KB).
5. `@mcp:context7` – Verify schemas for each of the eight files.
6. `@mcp:filesystem` – Validate each file against its schema; halt on any violation.
7. `@mcp:memory` – Restore knowledge graph snapshot and log the initialization event.
8. `@mcp:time` – Timestamp session start and schema validation completion.
9. `@mcp:git` – Stage initialization snapshot if files changed.

## Actions
1. Load applicable technology laws by scanning for project manifest files (e.g., `package.json`, `Cargo.toml`) via `@mcp:filesystem` and pulling matching rules.
2. Update `activeContext.json` with constitution versions, schema compliance score, and outstanding remediation tasks, if any.
3. If schemas fail validation, queue remediation steps in `scratchpad.json` and invoke `/fix` immediately.

## Logging & Exit
- Record readiness metrics in `progress.json` and document context assembly patterns in `systemPatterns.json`.
- Commit with message `init: session ready` when regeneration occurred.
- Announce readiness in `activeContext.json` and call `/next` to begin autonomous execution.