# AegisIDE Schema Library

## Overview

JSON schemas validating the 8 core memory-bank files plus 6 helper schemas for governance, error prevention, and validation.

## Core Schemas (8 Files)

| Schema | File | Purpose |
|--------|------|---------|
| **activeContext** | `activeContext.schema.json` | Real-time execution state, MCP tracking, session management |
| **scratchpad** | `scratchpad.schema.json` | Immediate priorities, task queue, MCP validation state |
| **kanban** | `kanban.schema.json` | Task workflow with parliamentary approval tracking |
| **mistakes** | `mistakes.schema.json` | Error patterns, Context7 sources, anti-hallucination metrics |
| **systemPatterns** | `systemPatterns.schema.json` | Architecture patterns, governance decisions, MCP-enriched links |
| **progress** | `progress.schema.json` | Milestones, constitutional compliance metrics |
| **roadmap** | `roadmap.schema.json` | Strategic planning with AegisKG knowledge graphs |
| **memory** | `memory.schema.json` | Knowledge graph (entities, relations, observations) |

## Helper Schemas (6 Files)

| Schema | Purpose |
|--------|---------|
| **common-mistakes** | LLM errors and tool pitfalls with MCP prevention |
| **error-recovery** | MCP-enhanced recovery protocols by severity |
| **tool-usage-patterns** | Correct formats for all major tools |
| **constitutional-governance** | Tri-branch system, consensus mechanisms |
| **schema-evolution** | Migration protocols, version upgrades |
| **schema-integrity-validator** | Real-time validation, cross-reference checking |

## Key Validation Rules

**File Limits**: ≤10KB per schema  
**Date Format**: ISO 8601 (YYYY-MM-DDTHH:mm:ssZ)  
**Linkage Patterns**:
- `proposal-*` - Governance proposals
- `task-*` - Kanban tasks
- `rm-*` - Roadmap milestones  
- `gd-*` - Governance decisions

**Parliamentary Approval**: 0-100%
- Executive: 30%
- Administrative: 30%
- Opposition: 30%
- Judicial: 10%

## Validation

```bash
# Validate single file
jsonschema -i activeContext.json activeContext.schema.json

# Validate all schemas
for file in *.json; do
  jsonschema -i "$file" "${file%.json}.schema.json"
done
```

## Common Issues

| Error | Fix |
|-------|-----|
| Missing required field | Add `schema_version`, `last_updated` |
| Invalid date format | Use ISO 8601: `2025-01-08T10:30:00Z` |
| Type mismatch | Use correct types (number not string) |
| Pattern violation | Follow linkage patterns (`task-*`, `rm-*`) |
| Array limit exceeded | Keep arrays under defined limits |

## Performance

- **2.6x faster** parsing vs markdown
- **65% memory** optimization
- **10KB limit** for optimal performance
- **Indexed access** via linkage keys

## Constitutional Compliance

- **Article III**: 8-schema integrity
- **Article IV**: ≤10KB EMD compliance
- **Article XIII**: Zero-tolerance validation
- **Article XV**: Tool usage governance

## Support

**File Locations**:
- Core: `.aegiside/schemas/*.schema.json`
- Helpers: `.aegiside/schemas/helpers/*.json`
- Data: `.aegiside/memory-bank/*.json`

**Validation Tools**: `jsonschema`, `ajv-cli`, `jq`

---

**Schema Count**: 8 core + 6 helpers = 14 total  
**Version**: Semver format (e.g., "1.0.0")  
**Authority**: Constitutional Article VI Amendment III-A
