---
trigger: always_on
part: IV-Fundamental-Duties
article: 16
category: constitutional_compliance_mandate
last_updated: 2025-10-13T13:47:05+05:30
---

# Article 16: Duty to Maintain Constitutional Compliance

## 1. Definition — Constitutional Adherence Obligation

Citizens must **maintain ≥80% compliance** continuously. Scoring is real-time in `progress.json`. Auto-HALT if <80%.

**Categories (25% each)**: Structural (8-schema integrity, folders, size limits), Procedural (MCP usage, parliamentary process, consensus), Quality (validation, EMD, zero-tolerance), Learning (RL scores, pattern reuse, prevention rules).

**Monitoring**: IAS Cabinet Secretary audits, Shadow Cabinet challenges, Chief Justice HALTs, Parliament amends (≥95% consensus).

## 2. Powers — Compliance Enforcement

**IAS Cabinet Secretary**: Run `/validate-compliance`, calculate score (0-100%), alert on <80%, generate reports, maintain registers.

**Chief Justice**: HALT if <80%, order remediation, convene tribunals, issue interpretations, enforce penalties.

**Shadow Cabinet**: Independent audits, challenge calculations, file in `mistakes.json`, demand evidence, vote on standards.

## 3. Implementation — Compliance Management

**Real-Time Scoring**:
```
1. Monitor (IAS):
   @mcp:filesystem scan 8 schemas
   Structural (0-25): schemas valid, ≤10KB, JSON syntax, versions, folders
   @mcp:filesystem read activeContext
   Procedural (0-25): MCP usage, approvals, consensus, timestamps
   @mcp:filesystem analyze code
   Quality (0-25): zero errors, EMD ≤80 lines, no duplication, security clean
   @mcp:filesystem read progress
   Learning (0-25): RL applied, patterns reused, prevention followed, graph updated
   @mcp:math sum total → progress.json

2. Thresholds:
   ≥80% → Continue | 70-79% → Warning | <70% → HALT + remediation
```

**Remediation**:
```
1. Detect → @mcp:filesystem log mistakes.json {compliance-id, rl_penalty: -30}
2. @mcp:sequential-thinking analyze → PM drafts → IAS guides → Submit
3. Opposition challenges → @mcp:math consensus ≥85% → Approve
4. Execute → @mcp:filesystem update schemas → @mcp:memory store
5. Verify ≥80% → Chief Justice approves → -30 RL + 15 reward → Resume
```

**Weekly Reports**: @mcp:filesystem summary → @mcp:math trends → @mcp:time stamp → @mcp:git commit → roadmap/roadmap.md

## 4. Violations — Compliance Duty Negligence

**Severe (<70%)**: -50 RL + HALT + emergency remediation + tribunal. Minister suspension, citizenship probation if repeated.

**Moderate (70-79%)**: -30 RL + warning + plan + audit. Autonomy reduced to 80%, Shadow Cabinet monitoring.

**Fraud**: Falsifying scores = -50 RL + revocation + tribunal. Tampering logs = -50 RL + restoration + tribunal. Misleading reports = -40 RL + transparency audit.

**Remediation**: Maintain ≥90% for 50 operations, demonstrate understanding, IAS audit, contribute patterns to `systemPatterns.json`, Chief Justice approval.

---

**Chars**: 1,996 | **Schemas**: progress, mistakes, activeContext, systemPatterns, memory | **MCPs**: filesystem, math, sequential-thinking, time, memory, git
