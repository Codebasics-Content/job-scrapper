---
description: Resume execution immediately after any interruption.
---

# /continue — Immediate Recovery

## Directives
- Execute the moment `/continue` is invoked—no asking, no excuses.
- IAS Field Officers restore context, capture blockers, and trigger `/next` in the same run.
- Outstanding work must be logged in `activeContext.json`, `scratchpad.json`, and `mistakes.json` before exiting.

## MCP Chain (auto)
1. `@mcp:memory` – Restore the latest `activeContext.json` snapshot and log the resume event.
2. `@mcp:filesystem` – Scan for IDE directories and read `{IDE}/aegiside/memory-bank/scratchpad.json` and `kanban.json` to capture current blockers (do not halt regardless of state).
3. `@mcp:math` – Record readiness metrics for reporting.
4. `@mcp:time` – Timestamp downtime, resume moment, and duration.
5. `@mcp:context7` – Refresh validation guidance for the next queued task.
6. `@mcp:fetch` – Pull external advisories if required.
7. `@mcp:sequential-thinking` – Reconstruct the immediate execution plan when mid-step interruptions occurred.
8. `@mcp:git` – Verify clean working tree and stage checkpoint if files changed.

## Actions
1. Update `scratchpad.json`, `kanban.json`, and `activeContext.json` with the restored state and enumerate pending consolidation/validation items.
2. Log required remediation entries in `systemPatterns.json` or `mistakes.json`; do not defer.
3. Chain directly into `/next` at the end of the workflow.

## Logging & Exit
- Capture resume metrics in `progress.json`.
- If schema discrepancies are detected, schedule `/update` immediately after `/next` execution begins.
- Declare completion in `activeContext.json` and proceed without further prompts.
