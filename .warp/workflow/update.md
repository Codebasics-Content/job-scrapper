---
description: Manually synchronize the memory bank when automatic updates fail.
---

# /update — Manual Memory-Bank Sync

## Directives
- IAS Field Officers run `/update` autonomously when real-time updates fall behind.
- Synchronize the eight mandatory schemas and validate each against `.windsurf/memory-bank/schemas/`.
- Record remediation steps in `activeContext.json`, `scratchpad.json`, and `mistakes.json` before resuming `/next`.

## MCP Chain (auto)
1. `@mcp:context7` – Review schema requirements for all memory-bank files.
2. `@mcp:filesystem` – Read the eight schemas: `activeContext.json`, `scratchpad.json`, `kanban.json`, `mistakes.json`, `systemPatterns.json`, `progress.json`, `roadmap.json`, `memory.json`.
3. `@mcp:math` – Compute file sizes, schema compliance score, and attention allocation.
4. `@mcp:sequential-thinking` – Plan remediation for missing schemas, oversized files, or inconsistent linkage keys.
5. `@mcp:filesystem` – Apply updates and cross-file synchronization.
6. `@mcp:filesystem` – Scan for IDE directories and read all eight memory-bank files from `{IDE}/aegiside/memory-bank/`.schemas/*.schema.json`); halt on any failure.
7. `@mcp:time` – Timestamp remediation actions and verify freshness.
8. `@mcp:git` – Commit with message `update: manual memory-bank sync`.
9. `@mcp:memory` – Log the fallback event and store updated patterns.

## Actions
1. Document the sync summary, schema results, and remaining gaps in `activeContext.json`.
2. Queue outstanding tasks in `scratchpad.json` and categorize issues in `mistakes.json`.
3. Update `progress.json` with remediation metrics (files fixed, time spent, compliance score).

## Logging & Exit
- Store cross-file alignment notes in `systemPatterns.json` and update roadmap alignment in `roadmap.json`.
- Publish a short report to `roadmap/roadmap.md` if strategic items were adjusted.
- Resume `/next` immediately after completion.
