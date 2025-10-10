---
description: Provides comprehensive summary of memory bank status, tasks, progress, and metrics.
---

# /status — System Status Report

## Directives
- IAS executes `/status` autonomously to deliver a real-time health snapshot to Parliament.
- All metrics must cite constitutional thresholds; schema validation is required before reporting.
- Any variance triggers follow-up tasks added to `scratchpad.json`.

## MCP Chain (auto)
1. `@mcp:context7` – Confirm scoring thresholds (Articles I, III, III-A, XI).
2. `@mcp:filesystem` – Read the eight core schemas, automation files, and roadmap assets.
3. `@mcp:math` – Compute compliance scores (Framework ≥80%, Consensus ≥95%, Roadmap ≥95%), velocity metrics, error rates.
4. `@mcp:sequential-thinking` – Compile remediation recommendations for any failing thresholds.
5. `@mcp:time` – Timestamp the audit and measure data freshness.
6. `@mcp:fetch` – Pull external advisories if anomalies require validation.
7. `@mcp:filesystem` – Validate each updated memory file against `.windsurf/memory-bank/schemas/*.schema.json`.
8. `@mcp:git` – Commit the status dossier (`status: State of the Republic YYYY-MM-DD`).
9. `@mcp:memory` – Store summary metrics and recommended actions in the knowledge graph.

## Actions
1. Write the status summary to `activeContext.json`, including compliance, consensus, roadmap alignment, error counts, and MCP health.
2. Log task distribution and blockers in `scratchpad.json`, update `kanban.json` with any follow-up workflow items.
3. Update `progress.json` with performance metrics; adjust `roadmap.json` if strategic targets shift.

## Logging & Exit
- Record risks and mitigation steps in `mistakes.json`, add proven playbooks to `systemPatterns.json`.
- Publish a condensed stakeholder summary to `roadmap/roadmap.md`.
- Run `/fix`, `/optimize`, or `/update` immediately if any category falls below thresholds; otherwise resume `/next`.
