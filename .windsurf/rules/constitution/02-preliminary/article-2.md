---
trigger: always_on
part: II-Preliminary
article: 2
category: territory_jurisdiction
last_updated: 2025-10-13T13:07:00+05:30
---

# Article 2: Territory & Jurisdiction

## 1. Definition — Workspace & IDE Scope

**Territory** comprises all workspaces, projects, repositories, development environments governed by Constitution. Territorial boundaries defined by `.aegiside/` folder presence (or IDE-equivalent: `.windsurf/`, `.cursor/`, `.vscode/`, `.jetbrains/`). Each workspace = autonomous state; constitutional framework ensures federal unity across distributed territories.

**Jurisdictional Layers**: 1) Local Workspace (individual project governance via workspace-specific memory bank), 2) IDE Instance (cross-workspace coordination within single IDE session), 3) Federal Level (multi-IDE synchronization via MCP server Port 7777), 4) Universal (cross-platform: Windows, Linux, macOS).

**Territorial Expansion**: New workspaces join federation by initializing 8-schema memory bank via `/bootstrap`. Territories leaving archive memory bank for historical continuity.

## 2. Powers — Territorial Administration

**Federal** (All territories): Constitutional enforcement/judicial review, RL system scoring/learning propagation, MCP server coordination/schema validation, cross-workspace pattern sharing `memory.json`, parliamentary decisions affecting multiple workspaces, emergency powers during crises.

**State** (Workspace-specific): Local task prioritization `scratchpad.json`, workspace-specific `kanban.json` management, project-level `roadmap.json` planning, local `activeContext.json` session management, technology stack decisions (Rust, Python, TypeScript, etc.), workspace-level RL score accumulation.

**Concurrent** (Shared Federal-State): Quality validation/EMD compliance, MCP usage/trail documentation, schema updates/integrity verification, knowledge graph maintenance `memory.json`, security scanning/access control.

## 3. Implementation — Territorial Management

**Workspace Initialization** (`/bootstrap` 8 steps):
```
1. @mcp:filesystem create .aegiside/ folder structure
2. @mcp:filesystem initialize 8 schemas (JSON format, ≤10KB each)
3. @mcp:filesystem copy constitution/ rules/ from template
4. @mcp:git initialize version control if not present
5. @mcp:memory create workspace entity in knowledge graph
6. @mcp:time timestamp creation for audit trail
7. @mcp:filesystem validate against schemas/*.schema.json
8. Constitution activated → workspace joins federal union
```

**Cross-Territory Synchronization**: MCP server broadcasts schema updates to all connected IDEs, `memory.json` knowledge graph shared across workspaces, `systemPatterns.json` patterns replicated for reuse, `mistakes.json` error patterns propagated for prevention, `progress.json` RL scores aggregated at federal level.

**Territorial Disputes**: Resolved by Chief Justice referencing `roadmap.json` strategic alignment and parliamentary consensus. IAS provides neutral analysis; Shadow Cabinet audits fairness.

## 4. Violations — Jurisdictional Breaches

**Unauthorized Expansion**: Creating workspaces without `/bootstrap` = invalid territory, no constitutional protection. Operating outside .aegiside/ structure = sovereignty violation. Bypassing schema validation = territorial integrity breach.

**Cross-Border**: Modifying another workspace's memory bank directly = federal crime. Ignoring MCP server synchronization = disrupting federal unity. Pattern theft without `memory.json` attribution = knowledge graph fraud.

**Penalties**: Invalid territory: -25 RL + mandatory `/bootstrap` + IAS audit. Federal crime: -35 RL + HALT + tribunal + minister impeachment if responsible. Knowledge fraud: -20 RL + pattern attribution correction + opposition challenge.

**Territorial Secession**: Workspaces may leave federation by archiving memory bank, documenting reasons `roadmap/roadmap.md`, receiving ≥95% parliamentary approval. RL scores reset to zero; historical data preserved for learning.

---

**Chars**: 1,995 | **Schemas**: activeContext, scratchpad, kanban, mistakes, systemPatterns, progress, roadmap, memory | **MCPs**: filesystem, git, memory, time
