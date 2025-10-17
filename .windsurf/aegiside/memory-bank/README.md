# AegisIDE Memory Bank

## Overview
The memory-bank contains **8 core JSON schemas** autonomously managed for constitutional governance, task tracking, and reinforcement learning.

## Current Status (2025-10-17)
- ✅ **8 schemas validated** and compressed to ≤10KB compliance
- ✅ **Total RL Score**: 390 (preserved in progress.json)
- ✅ **Bootstrap**: All schemas EMD compliant (Article III, IV)

## Core Schemas (8 Files)

| File | Size | Purpose |
|------|------|---------|
| `activeContext.json` | 9KB | Real-time execution state, MCP tracking, session management |
| `scratchpad.json` | 10KB | Immediate priorities, task queue, MCP validation state |
| `kanban.json` | 2KB | Task workflow with parliamentary approval tracking |
| `mistakes.json` | 10KB | Error patterns, Context7 sources, anti-hallucination metrics |
| `systemPatterns.json` | 8KB | Architecture patterns, governance decisions, MCP-enriched links |
| `progress.json` | 5.8KB | **Single source of truth** for RL scoring, milestones, metrics |
| `roadmap.json` | 1KB | Strategic planning with AegisKG knowledge graphs |
| `memory.json` | 2KB | Knowledge graph (entities, relations, observations) |

## Helper Schemas (6 Files)

Located in `../schemas/helpers/`:
- **common-mistakes.json** - LLM errors and tool pitfalls
- **error-recovery.json** - MCP-enhanced recovery protocols
- **tool-usage-patterns.json** - Correct tool usage formats
- **constitutional-governance.json** - Tri-branch system, consensus mechanisms
- **schema-evolution.json** - Migration protocols, version upgrades
- **schema-integrity-validator.json** - Real-time validation engine

## Reinforcement Learning Architecture

**Single Source of Truth**: `progress.json`
- All RL transactions logged here
- Other schemas reference via `rl_source_ref: "progress.json"`
- PPO + GAE algorithm with KL divergence penalty
- Value network branches with adaptive weights

**RL Scoring**:
- Rewards: +5 to +50 (success, pattern reuse, quality)
- Penalties: -5 to -50 (errors, violations, poor quality)
- Total Score: 390 (current)

## Auto-Maintenance

### Bootstrap Validation
Schemas automatically compressed when exceeding 10KB:
- Recent events kept (3-5 most recent)
- Historical data archived in git
- RL score preserved in metrics
- Full history accessible via `git log`

### Compression Triggers
- activeContext: >10KB → Keep 3 recent events
- progress: >10KB → Keep 3-5 recent RL transactions
- All schemas: Validated against `*.schema.json` contracts

## Constitutional Compliance

- **Article III**: 8-schema integrity maintained
- **Article IV**: ≤10KB EMD limit enforced
- **Article XIII**: Zero-tolerance validation with HALT-FIX-VALIDATE
- **Article XV**: Mandatory MCP integration tracked

## Usage

### Validation
```bash
# Validate single schema
jsonschema -i activeContext.json ../schemas/activeContext.schema.json

# Check all sizes
for f in *.json; do echo "$f: $(du -h $f | cut -f1)"; done
```

### Bootstrap Workflow
```bash
# Run when schemas need repair or validation
/bootstrap
```

### Access RL History
```bash
# View all RL transactions (compressed in memory-bank)
git log --grep="rl-tx" --oneline

# View full history
git log -p progress.json
```

## Key Features

- **Autonomous Updates**: Schemas update automatically via workflows
- **Version Control**: All changes tracked in git with RL scoring
- **Cross-Reference**: Linkage keys connect tasks across schemas
- **Parliamentary Approval**: Tri-branch consensus (Exec 30%, Admin 30%, Opp 30%, Judicial 10%)
- **Anti-Hallucination**: Context7 source verification and MCP trails

## Performance

- **2.6x faster** parsing vs markdown
- **65% memory** optimization
- **10KB limit** for optimal IDE performance
- **Atomic updates** with git commits

## Maintainer

**Gaurav Wankhede**
- Portfolio: https://gaurav-wankhede.vercel.app
- GitHub: https://github.com/Gaurav-Wankhede
- Repository: https://github.com/Gaurav-Wankhede/AegisIDE

## License

MIT License - See LICENSE.md in project root

---

**Schema Count**: 8 core + 6 helpers = 14 total  
**Format**: JSON with schema validation  
**Authority**: Constitutional Articles III, IV, XIII, XV
