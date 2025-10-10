---
description: Identify, approve, and apply optimizations without manual prompting.
---

# /optimize — Performance Upgrade Loop

## Directives
- IAS Researcher owns `/optimize`; execute immediately when invoked.
- Optimizations must be backed by MCP research, benchmarked, and recorded in the memory bank.
- Validate every modified memory-bank file against `.windsurf/memory-bank/schemas/*.schema.json` before saving.

## MCP Chain (auto)
1. `@mcp:context7` – Retrieve official optimization guidance and constitutional constraints.
2. `@mcp:fetch` – Gather industry benchmarks and best-practice references.
3. `@mcp:memory` – Load historical optimization patterns.
4. `@mcp:math` – Capture baseline metrics (latency, throughput, resource usage).
5. `@mcp:sequential-thinking` – Plan optimization steps and consensus requirements.
6. `@mcp:filesystem` – Apply changes (code + config) while keeping files ≤80 lines and ≤10 KB.
7. `@mcp:time` – Timestamp pre/post benchmark runs.
8. `@mcp:filesystem` – Run benchmarks/tests; halt if regressions appear.
9. `@mcp:filesystem` – Update the eight schemas plus supporting files; validate via `.windsurf/memory-bank/schemas/*.schema.json`.
10. `@mcp:git` – Stage/commit with message `optimize: <summary>`.
11. `@mcp:memory` – Persist new optimization pattern, benchmarks, and decisions.

## Actions
1. Record optimization summary in `systemPatterns.json`, including before/after metrics and applicable contexts.
2. Update `mistakes.json` if the change resolves recurring inefficiencies; log velocity impact in `progress.json`.
3. Link roadmap objectives impacted by the optimization in `roadmap.json` to maintain strategic alignment.

## Logging & Exit
- Store knowledge graph deltas in `memory.json` and timestamp events in `activeContext.json`.
- Queue follow-up tasks in `scratchpad.json` if additional optimization passes are required.
- Resume `/next` automatically after completion.
