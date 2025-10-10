---
description: Tri-branch oversight ensuring constitutional compliance and democratic governance.
---

# /oversight-checks-and-balances — Parliamentary Review

## Directives
- Triggered whenever a proposal needs tri-branch approval; run without manual delays.
- Every decision must include constitutional citations, MCP trails, and memory-bank updates.
- Consensus ≥95% is required; failure defaults to rejection and remediation logging.

## MCP Chain (auto)
1. `@mcp:filesystem` – Read proposal details from `systemPatterns.json`, supporting evidence, and impacted memory-bank files.
2. `@mcp:context7` – Load relevant constitutional articles and laws.
3. `@mcp:fetch` – Gather external advisories or precedent cases if required.
4. `@mcp:memory` – Retrieve historical decisions and store debate outcomes.
5. `@mcp:sequential-thinking` – Orchestrate debate order and ensure every branch is heard.
6. `@mcp:math` – Calculate weighted consensus scores and impact projections.
7. `@mcp:time` – Timestamp submissions, challenges, votes, and rulings.
8. `@mcp:git` – Snapshot debate artifacts and final decisions for the audit trail.

## Actions
1. Log proposal summary, IAS brief, and opposition challenges in `activeContext.json` and `systemPatterns.json`.
2. Record consensus result and judicial ruling in `progress.json`; if consensus <95%, queue remediation tasks in `scratchpad.json`.
3. Update `roadmap.json` when strategic objectives shift; store final verdict in `memory.json`.

## Logging & Exit
- Capture debate patterns and mitigation strategies in `mistakes.json` and `systemPatterns.json`.
- Commit with message `oversight: decision recorded` and direct execution to `/next` or `/fix` based on the ruling.
