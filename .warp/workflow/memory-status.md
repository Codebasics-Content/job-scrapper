---
description: Audit the health of `memory.json` and record follow-up actions.
---

# /memory-status — Knowledge Graph Audit

## Directives
- Execute immediately when `/memory-status` is invoked; IAS logs the outcome in `activeContext.json`.
- Validate `memory.json` against `.windsurf/memory-bank/schemas/memory.schema.json` before saving any remediation.
- Record anomalies and required fixes in `mistakes.json` and queue work in `scratchpad.json`.

## MCP Chain (auto)
1. `@mcp:context7` – Confirm schema contract and constitutional expectations (Articles I, XI, XVI).
2. `@mcp:filesystem` – Read `.windsurf/memory-bank/memory.json` and load schema.
3. `@mcp:memory` – Retrieve metadata (entity count, relations, observations) for comparison.
4. `@mcp:time` – Timestamp the audit start.
5. `@mcp:math` – Compute health metrics (density, growth delta, compliance score).
6. `@mcp:sequential-thinking` – Plan remediation for orphaned nodes or conflicting observations.
7. `@mcp:fetch` – Pull external ontology updates if schema drift is detected.
8. `@mcp:filesystem` – Validate against `.windsurf/memory-bank/schemas/memory.schema.json`; halt on failure.
9. `@mcp:git` – Snapshot the audit report if files are modified.
10. `@mcp:memory` – Persist audit summary and follow-up tasks to the knowledge graph.

## Actions
1. Document audit metrics and issues in `activeContext.json` (include timestamp and compliance score).
2. If remediation is required, add tasks to `scratchpad.json` and classify severity in `mistakes.json`.
3. Update `progress.json` with audit frequency, health score, and pending remediation count.

## Logging & Exit
- Store optimization or ontology adjustments in `systemPatterns.json`.
- Commit with message `memory-status: knowledge graph audit` if changes were made.
- Proceed directly to `/next` or `/fix` (if remediation required).
