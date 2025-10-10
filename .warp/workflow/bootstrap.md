---
description: Ensure mandatory memory-bank schemas exist and pass strict validation.
---

# /bootstrap — Memory Bank Regeneration

## Directives
- Execute immediately when `/bootstrap` is invoked; no questions, no delays.
- IAS Field Officers run the action autonomously and log every step in `activeContext.json`.
- Reference schemas live in `{IDE}/aegiside/memory-bank/schemas/*.schema.json`; validation is mandatory before saving.

## MCP Chain (auto)
1. `@mcp:filesystem` – Scan for IDE directories (`.windsurf/`, `.cursor/`, `.vscode/`, `.cline/`, `.qoder/`, `.trae/`, `.idle/`, `.zed/`, `.jetbrains/`, `.replit/`, `.pycharm/`) and locate `aegiside/memory-bank/` within the active IDE directory.
2. `@mcp:sequential-thinking` – Compare the directory contents with the canonical list of eight schemas.
3. `@mcp:math` – Count files and compute completion percentage.
4. `@mcp:context7` – Re-confirm schema contracts for any missing files.
5. `@mcp:filesystem` – Create missing files with minimal valid payloads.
6. `@mcp:time` – Timestamp scan, creation, and verification events.
7. `@mcp:filesystem` – Validate each file against its schema (`activeContext`, `scratchpad`, `kanban`, `mistakes`, `systemPatterns`, `progress`, `roadmap`, `memory`).
8. `@mcp:git` – Stage the regeneration changes for auditability.
9. `@mcp:memory` – Persist the regeneration summary to the knowledge graph.

## Actions
1. Regenerate missing files under `{IDE}/aegiside/memory-bank/` only; never touch the canonical source directory.
2. Re-run schema validation after each creation; halt immediately if a schema error appears.
3. Update `activeContext.json` with the regeneration event and list remaining discrepancies (if any).

## Logging & Exit
- Record remediation details in `mistakes.json` when files were missing or malformed.
- Append bootstrap success metrics to `progress.json`.
- Commit with message `bootstrap: memory bank regenerated` and proceed directly to `/update` or `/next` as required.
