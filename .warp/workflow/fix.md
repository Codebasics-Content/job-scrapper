---
description: Resolve errors with the HALT-FIX-VALIDATE loop and resume execution.
---

# /fix — Zero-Tolerance Remediation

## Directives
- HALT immediately on any error/warning; `/fix` executes without debate.
- IAS Field Officers coordinate remediation; Chief Justice confirms readiness before exit.
- Schema validation against `.windsurf/memory-bank/schemas/*.schema.json` is mandatory before saving any memory updates.

## MCP Chain (auto)
1. `@mcp:context7` – Load official remediation guidance and constitutional requirements.
2. `@mcp:filesystem` – Inspect failing files, apply atomic edits, and re-run validations.
3. `@mcp:sequential-thinking` – Decompose root cause, plan corrective steps, and track retry count.
4. `@mcp:fetch` – Pull upstream advisories if local knowledge is insufficient.
5. `@mcp:git` – Stage each iterative fix for complete audit trails.
6. `@mcp:time` – Timestamp HALT start, each attempt, and resolution.
7. `@mcp:math` – Record consensus/impact metrics when multiple options exist.
8. `@mcp:memory` – Log failure patterns, implemented fix, and prevention notes.

## Actions
1. Apply corrections until `/validate` returns 100% clean (HALT-FIX-VALIDATE loop).
2. Update `activeContext.json`, `scratchpad.json`, and `kanban.json` with the remediation state before resuming.
3. Document root cause and resolution in `mistakes.json`; capture reusable patterns in `systemPatterns.json`.

## Logging & Exit
- Append remediation metrics (`time-to-fix`, `attempts`, `consensus`) to `progress.json`.
- Align `roadmap.json` if strategic commitments were impacted.
- Commit with message `fix: resolved blocking issue` and trigger `/continue` or `/next` immediately.
