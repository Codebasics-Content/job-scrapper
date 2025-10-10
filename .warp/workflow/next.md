---
description: Continuous autonomous execution loop.
---

# /next — Continuous Task Execution

## Directives
- Drain the backlog without prompts; `/next` never pauses for permission.
- Update all eight memory-bank schemas after each task and validate against `.windsurf/memory-bank/schemas/*.schema.json` before moving on.
- Maintain detailed state in `activeContext.json`, `scratchpad.json`, and `kanban.json` at every iteration.

## MCP Chain (per task)
1. `@mcp:filesystem` – Scan for IDE directories and read `{IDE}/aegiside/memory-bank/scratchpad.json` (primary) or `kanban.json` (fallback) to identify the next task.t-priority work item.
2. `@mcp:math` – Rank tasks (P0 → P3) and compute attention budget.
3. `@mcp:sequential-thinking` – Build the execution plan or resume mid-task state.
4. `@mcp:filesystem` – Load supporting files (code + relevant schemas).
5. `@mcp:context7` – Pull references or official docs for the targeted change.
6. `@mcp:filesystem` – Apply edits; keep files ≤80 lines and ≤10 KB.
7. `@mcp:git` – Stage atomic diff.
8. `@mcp:time` – Timestamp execution start/end.
9. `@mcp:filesystem` – Run validations (`/validate` workflow); halt and invoke `/fix` on error.
10. `@mcp:filesystem` – Update the eight schemas (scratchpad, activeContext, kanban, mistakes, systemPatterns, progress, roadmap, memory) and validate each against its schema.
11. `@mcp:memory` – Record knowledge graph deltas.
12. `@mcp:git` – Commit schema updates (`next: update memory bank`).

## Actions
1. Remove completed tasks from `scratchpad.json`, advance cards in `kanban.json`, and note session metrics in `activeContext.json`.
2. Add error patterns to `mistakes.json`, architecture wins to `systemPatterns.json`, velocity data to `progress.json`, roadmap alignment notes to `roadmap.json`, and knowledge entities to `memory.json`.
3. If the backlog remains, loop immediately to the next task; otherwise, signal completion in `activeContext.json`.

## Logging & Exit
- Record throughput, validation success rate, and attention efficiency in `progress.json`.
- Keep `mistakes.json` and `systemPatterns.json` synchronized with new patterns each iteration.
- `/next` terminates only when `scratchpad.json` has no actionable items or autonomy escalates to 100%; otherwise it repeats automatically.
