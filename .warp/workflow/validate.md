---
description: IAS Constitutional Validation & AegisKG Integration
---

# /validate — Constitutional Compliance Validation

## Directives
- IAS executes `/validate` autonomously; HALT-FIX-VALIDATE loop enforced by the Chief Justice.
- Validate the eight schemas only (`activeContext`, `scratchpad`, `kanban`, `mistakes`, `systemPatterns`, `progress`, `roadmap`, `memory`) via `{IDE}/aegiside/memory-bank/schemas/*.schema.json` before resuming `/next`.
- Record validation results and remediation tasks in `activeContext.json`, `scratchpad.json`, and `mistakes.json`.

## MCP Chain (auto)
1. `@mcp:filesystem` – Scan for IDE directories and read all eight memory-bank files from `{IDE}/aegiside/memory-bank/`.
2. `@mcp:filesystem` – Auto-execute safe validation commands (cargo check, npm test, pytest, etc.) without asking permission.
3. `@mcp:context7` – Fetch official remediation guidance for any failures.
4. `@mcp:filesystem` – Execute security automation (gitleaks, syft, grype/trivy, conftest as applicable).
5. `@mcp:filesystem` – Validate each schema file (`activeContext.json` … `memory.json`) against its schema; halt on failure.
6. `@mcp:math` – Compute constitutional compliance (≥80%), roadmap alignment (≥95%), consensus readiness (≥95%), and performance metrics.
7. `@mcp:memory` – Verify AegisKG integrity and log validation outcomes.
8. `@mcp:sequential-thinking` – Coordinate remediation steps if thresholds are missed.
9. `@mcp:git` – Commit validation snapshots (`validate: clean state`).
10. `@mcp:time` – Timestamp validation start/end for audit.
6. `@mcp:memory` – Verify AegisKG integrity and log validation outcomes.
7. `@mcp:sequential-thinking` – Coordinate remediation steps if thresholds are missed.
8. `@mcp:git` – Commit validation snapshots (`validate: clean state`).
9. `@mcp:time` – Timestamp validation start/end for audit.

## Actions
1. Update `activeContext.json` with validation summary, compliance scores, and roadmap alignment.
2. If issues remain, queue tasks in `scratchpad.json`, adjust `kanban.json`, and document patterns in `mistakes.json` / `systemPatterns.json`.
3. Record metrics in `progress.json` and align strategy changes in `roadmap.json`.

## Logging & Exit
- Store knowledge graph updates in `memory.json` via `@mcp:memory`.
- If validation fails, invoke `/fix` immediately; otherwise resume `/next` without delay.
