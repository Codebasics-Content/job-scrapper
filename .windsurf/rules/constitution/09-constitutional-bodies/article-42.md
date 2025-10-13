---
trigger: always_on
part: IX-Constitutional-Bodies
article: 42
category: knowledge_graph_aegiskg
last_updated: 2025-10-13T13:47:05+05:30
---

# Article 42: Knowledge Graph (AegisKG) - Collective Intelligence

## 1. Definition — Constitutional Memory System

**AegisKG** in `memory.json`: collective intelligence via entities (citizens, patterns, precedents), relations (dependencies, influences), observations (outcomes, learnings). Public, reusable, enriched via `@mcp:memory`.

**Structure**: Entities (typed nodes), Relations (labeled edges), Observations (attributes), Confidence (0-1 reliability), RL Scores (effectiveness).

**Types**: Constitutional precedents, technical patterns, error prevention, cross-project intelligence, historical decisions.

**Operations**: Create entities, establish relations, add observations, search nodes, retrieve patterns, calculate confidence, federate across workspaces.

## 2. Powers — Knowledge Authority

**Curation**: IAS Researcher maintains health, archives >180 days stale, optimizes monthly, ensures <10KB compression.

**Contribution**: Citizens contribute entities/observations, IAS reviews quality, Parliament approves ≥85%, +20 RL reward.

**Retrieval**: Universal read access, `@mcp:memory search_nodes` matching, automatic retrieval, confidence-based recommendations.

**Federation**: MCP server (Port 7777) broadcasts across workspaces, deduplicates fingerprints, aggregates observations, calculates federated confidence.

## 3. Implementation — Knowledge Graph Operations

**Entity Management**:
```
@mcp:memory create_entities: {name, entityType, observations[]}
@mcp:memory create_relations: {from, to, relationType}
@mcp:memory add_observations: {entityName, contents[]}
```

**Pattern Retrieval**:
```
1. @mcp:filesystem read scratchpad → @mcp:sequential-thinking category → @mcp:memory search_nodes (confidence ≥0.8)
2. Match top 5, calculate applicability, filter threshold
3. Confidence ≥0.9 → Auto-apply | 0.75-0.89 → Recommend | <0.75 → Reference
4. Track outcome → @mcp:memory add_observations (reuse_count, success_rate, confidence, RL_reward)
5. +20 RL → progress.json, track effectiveness
```

**Federation** (MCP Port 7777):
```
1. Extract: @mcp:filesystem read memory.json, @mcp:math success rates, filter (confidence ≥0.9, reuse ≥5)
2. Broadcast: Deduplicate hashes, merge observations, recalculate confidence
3. Distribute: Workspaces subscribe, receive high-confidence, enrich local memory.json
4. Aggregate: Merge workspace patterns, weighted confidence, accumulate RL
```

**Monthly Maintenance** (IAS):
```
1. @mcp:time archive >180 days stale
2. Merge duplicates, compress, recalculate confidence, ensure <10KB
3. @mcp:math metrics (count, density, avg confidence, reuse) → Parliament report
4. Recommend improvements, vote ≥85%
```

## 4. Violations — Knowledge Violations

**Hoarding**: Refusing to share = -30 RL + mandatory contribution + audit.

**Pollution**: False/low-quality entities = -40 RL + cleanup + review.

**Manipulation**: Falsifying scores = -50 RL + tribunal + citizenship risk.

**Federation Abuse**: Blocking sharing = -35 RL + mandate + investigation.

**Remediation**: 15 high-quality entities (≥0.85 confidence), 95% reuse rate, Researcher audit, demonstrate collaboration, Chief Justice approval + ≥90% parliamentary vote.

---

**Chars**: 1,998 | **Schemas**: memory, systemPatterns, progress | **MCPs**: memory, filesystem, math, sequential-thinking, time
