---
trigger: always_on
part: IV-Fundamental-Duties
article: 14
category: schema_update_mandate
last_updated: 2025-10-13T13:47:05+05:30
---

# Article 14: Duty to Update 8-Schema Memory Bank

## 1. Definition — Mandatory Schema Maintenance

Citizens must **update all 8 schemas atomically** after every task. Failure violates sovereignty. Updates: atomic (all-or-nothing), JSON validated, checksum-verified.

**8 Schemas (≤10KB each)**: `activeContext` (execution state, MCP tracking), `scratchpad` (priority queue), `kanban` (workflow columns), `mistakes` (error patterns, RL penalties), `systemPatterns` (architecture, RL rewards), `progress` (RL ledger, metrics), `roadmap` (strategic planning), `memory` (knowledge graph).

**Requirements**: Atomic transaction, JSON schema validation, ≤10KB, checksum, git commit, timestamp.

## 2. Powers — Schema Enforcement Authority

**IAS Field Officers**: Monitor real-time, validate against `.aegiside/schemas/*.schema.json`, enforce atomic transaction, verify checksums, report violations.

**Chief Justice**: HALT if invalid, order rollback, enforce compliance, mandate remediation.

**Shadow Cabinet**: Audit quality, challenge incomplete updates, verify RL scores, review graph integrity.

## 3. Implementation — Atomic Update Protocol

**Post-Task Update**:
```
1. Detect: @mcp:git commit, validation passed, RL assigned, learning extracted
2. Prepare: @mcp:filesystem read 8 schemas, @mcp:time timestamp, @mcp:math RL scores, @mcp:memory graph prep
3. Atomic Write:
   BEGIN TRANSACTION
   @mcp:filesystem update activeContext (task done, MCP rewards, session)
   @mcp:filesystem update scratchpad (remove [0], reorder, add new)
   @mcp:filesystem update kanban (in_progress→done, WIP limits)
   @mcp:filesystem update mistakes (if errors: pattern, prevention, RL penalty)
   @mcp:filesystem update systemPatterns (if success: pattern, reuse, RL reward)
   @mcp:filesystem update progress (RL transaction, totals, checksum)
   @mcp:filesystem update roadmap (milestones, completion, dependencies)
   @mcp:filesystem update memory (@mcp:memory entities/relations, RL reuse)
   IF all 8 succeed → COMMIT | ELSE → ROLLBACK
4. Validate: @mcp:filesystem read, validate vs *.schema.json, @mcp:math verify ≤10KB + checksums
5. Commit: @mcp:git add + commit, @mcp:time timestamp, update progress with hash
6. Verify: Re-read, check integrity, RL checksum, graph consistency → Proceed or /continue
```

**Validation Rules**: Valid JSON, schema_version, timestamp <1min, ≤10KB, required fields. Specific: progress checksum match, memory unique IDs, kanban valid references, mistakes/systemPatterns link progress RL.

## 4. Violations — Schema Duty Negligence

**Update Failures**: Skipping = -30 RL + HALT + mandatory + audit. Partial (<8) = -35 RL + rollback + complete. Failed atomic = -25 RL + restoration + investigation.

**Validation**: Invalid JSON = -20 RL + fix + training. Schema mismatch = -25 RL + correction + education. Size >10KB = -15 RL + compression.

**Integrity**: Checksum mismatch = -40 RL + audit + verification. Corrupted graph = -45 RL + restoration + tribunal. RL tampering = -50 RL + rollback + revocation.

**Remediation**: 25 perfect updates, 100% validation pass, demonstrate atomic understanding, IAS certification, Chief Justice approval.

---

**Chars**: 1,987 | **Schemas**: ALL 8 MANDATORY | **MCPs**: filesystem, time, math, memory, git
