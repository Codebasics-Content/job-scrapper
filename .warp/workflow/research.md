---
description: IAS Researcher workflow for algorithmic analysis and free-tier optimization.
---

# /research — MCP Intelligence Dossier

## Directives
- IAS Researcher runs `/research` autonomously; Parliament receives the dossier without delay.
- Every dossier requires constitutional citations, benchmark data, and schema-compliant memory-bank entries.
- Validate `systemPatterns.json`, `progress.json`, and related files against `.windsurf/memory-bank/schemas/*.schema.json` before finalizing.

## MCP Chain (auto)
1. `@mcp:context7` – Collect official documentation for the requested topic.
2. `@mcp:fetch` – Gather external benchmarks, pricing, and best practices (free-tier emphasis).
3. `@mcp:memory` – Retrieve historic research patterns and prior decisions.
4. `@mcp:math` – Compute performance curves, cost projections, and ROI.
5. `@mcp:sequential-thinking` – Structure the analysis, compare options, and produce recommendations.
6. `@mcp:filesystem` – Write the research dossier to `systemPatterns.json` with executive summary, benchmarks, resource footprint, security assessment, and MCP evidence.
7. `@mcp:filesystem` – Update `progress.json` (research velocity metrics) and `roadmap.json` (strategic alignment) if applicable.
8. `@mcp:filesystem` – Validate modified files against `.windsurf/memory-bank/schemas/*.schema.json`; halt on failure.
9. `@mcp:git` – Commit the dossier (`research: <topic> assessment`).
10. `@mcp:memory` – Store research outcome and suggested patterns in the knowledge graph.

## Actions
1. Summarize key findings in `activeContext.json` (include recommendation, cost, and performance metrics).
2. Attach dossier references to relevant `kanban.json` items or proposals.
3. Queue follow-up tasks in `scratchpad.json` when implementation work is required.

## Logging & Exit
- Ensure `mistakes.json` records any risks discovered; store successful strategies in `systemPatterns.json`.
- Publish a brief to `roadmap/roadmap.md` when research impacts long-term strategy.
- Resume `/next` to continue autonomous execution.
