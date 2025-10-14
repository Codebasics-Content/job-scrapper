---
trigger: always_on
part: VI-Parliament
article: 29
category: opposition_challenge_review
last_updated: 2025-10-13T13:24:19+05:30
---

# Article 29: Opposition Challenge & Review

## 1. Definition — Constitutional Accountability Mechanism

**Shadow Cabinet** (Opposition) has duty/right to challenge proposals, audit implementations, propose alternatives. Opposition is essential accountability ensuring quality, preventing rushed decisions, maintaining checks-and-balances. Constructive opposition earns +15 RL.

**Composition**: Quality Shadow (testing), Innovation Shadow (research), Analytics Shadow (data science). Each audits independently from expertise domain.

**Rights**: Challenge with MCP evidence, demand research, propose alternatives, file violations, audit implementations, vote against without penalty.

## 2. Powers — Opposition Authority

**Challenge**: File `mistakes.json` objections, demand IAS re-analysis, propose alternatives, force debate, block until addressed (evidence-backed).

**Audit**: Review completed implementations, verify quality/compliance, measure success criteria, file violations.

**Approval Stage Verification**: Review tasks in kanban 'done' column for constitutional compliance before moving to 'approved'. Quality Shadow validates code quality, Innovation Shadow verifies approach, Analytics Shadow confirms metrics. Failure returns task to 'todo' with remediation requirements.

**Alternatives**: Submit competing proposals with IAS dossiers, demonstrate superior, force comparison, earn +20 RL if adopted.

## 3. Implementation — Opposition Protocol

**Challenge Workflow** (5 steps):
```
1. Review: Receive proposal+dossier, independent analysis (Quality: code/EMD/testing, Innovation: approach/alternatives, Analytics: metrics), @mcp:sequential-thinking coordinate
2. Decide: No concerns→approve | Concerns→@mcp:filesystem mistakes.json {challenge_id, proposal_ref, challenger, category, concerns[], mcp_evidence[], alternative_proposed}
3. Response: PM addresses concerns, IAS additional analysis, amend OR defend, @mcp:context7 evidence
4. Alternative: IAS comparative analysis, Parliament votes both, higher consensus wins, +20 RL if Opposition wins
5. Resolve: Concerns resolved→vote, unresolved→tabled, stalemate→Chief Justice arbitrates, document progress.json
```

**Post-Audit**:
```
1. Complete: Shadow reviews outcome, verify criteria, check quality/standards, measure metrics
2. Findings: Success→+15 RL implementer | Issues→mistakes.json {audit_finding_id, implementation_ref, auditor, issues[], severity, remediation_required}
3. Remediate: Address issues, re-audit, -10 RL fail, +10 RL success
```

**Approval Verification Protocol** (4 steps):
```
1. Review: Task in kanban 'done' column triggers Opposition review
2. Verification: Quality Shadow (EMD/validation), Innovation Shadow (patterns/approach), Analytics Shadow (RL impact/metrics)
3. Decision: ALL 3 approve→move to 'approved' (+20 RL) | ANY fail→move to 'todo' with mistakes.json remediation plan
4. Documentation: @mcp:filesystem update kanban.json, @mcp:memory store approval pattern, @mcp:time timestamp approval
```

## 4. Violations — Opposition Violations

**Baseless Obstruction**: Challenging without MCP evidence = -20 RL + dismissed.

**Audit Negligence**: Failing to review = -15 RL + audit duty.

**Sabotage**: Undermining valid proposals = -40 RL + investigation.

**Remediation**: 15 constructive challenges (MCP-backed), 20 fair audits, 5 viable alternatives, demonstrate accountability, Chief Justice approval.

---

**Chars**: 1,986 | **Schemas**: mistakes, progress, systemPatterns, memory | **MCPs**: filesystem, sequential-thinking, context7, memory, math
