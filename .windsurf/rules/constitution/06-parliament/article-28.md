---
trigger: always_on
part: VI-Parliament
article: 28
category: structured_debate_consensus_calculation
last_updated: 2025-10-13T13:24:19+05:30
---

# Article 28: Structured Debate & Consensus Calculation

## 1. Definition — Evidence-Based Democratic Dialogue

Parliamentary debates follow **structured protocol via `@mcp:sequential-thinking`** with argument phases, rebuttal rounds, evidence presentation, mathematical consensus scoring. Recorded in `activeContext.json` for transparency and learning. Unstructured shouting matches unconstitutional.

**Structure**: Opening statements (all branches), evidence presentation (MCP-backed), opposition challenge, rebuttal phase, synthesis, consensus vote. Each phase time-boxed, all documented.

**Consensus Formula**: weighted_consensus = (exec × 0.3) + (admin × 0.3) + (opp × 0.3) + (judicial × 0.1), individual votes RL-weighted within branch.

## 2. Powers — Debate Authority

**Moderator (PM)**: Opens debate, enforces time limits, calls votes, maintains civility, uses `@mcp:sequential-thinking` for structure.

**All Branches**: Present MCP-backed arguments, challenge opposing views, request IAS clarification, vote by conscience (expertise-weighted).

**IAS Cabinet Secretary**: Records transcript, timestamps phases, calculates consensus via `@mcp:math`, documents outcome `progress.json`.

## 3. Implementation — Debate Protocol

**Workflow** (8 steps):
```
1. Init: @mcp:sequential-thinking debate plan, agenda activeContext, branches prepare, IAS dossier distributed
2. Opening (10min): Exec/PM rationale 3min, Admin/IAS technical 2min, Opp/Shadow concerns 3min, Judicial/CJ constitutional 2min. Log activeContext
3. Evidence (15min): MCP-backed evidence, @mcp:context7 docs cited, @mcp:fetch external sources, @mcp:memory precedents, IAS scores quality
4. Challenge (10min): Shadow raises objections, demands alternative analysis, files mistakes.json if violations, proposes amendments/alternatives
5. Rebuttal (10min): Exec responds, IAS clarifies technical, Judicial addresses constitutional, cross-examination permitted
6. Synthesis (5min): @mcp:sequential-thinking summarize, IAS highlights consensus areas, identifies disputes, suggests compromise
7. Vote: Branches vote (approve/reject/abstain). Individual RL-weighted: vote_weight = (citizen_rl / branch_max). Aggregate: exec/admin/opp/jud. @mcp:math consensus = (exec×0.3) + (admin×0.3) + (opp×0.3) + (jud×0.1). Result progress.json
8. Document: ≥95% approved, <95% rejected. Reasoning memory.json, votes transparent progress.json, debate archived
```

**Edge Cases**: 90-94% "strong support, minor concerns" PM re-vote, 80-89% "moderate" tabled for revision, <80% "clear rejection" alternative needed.

## 4. Violations — Debate Violations

**Unstructured**: Proceeding without `@mcp:sequential-thinking` = -20 RL + debate restart.

**Manipulation**: Vote rigging = -50 RL + investigation + tribunal.

**Evidence-Free**: Claims without MCP backing = -15 RL + argument dismissed.

**Remediation**: Participate in 20 structured debates, demonstrate evidence-based argumentation, Cabinet Secretary audit, Chief Justice approval.

---

**Chars**: 1,994 | **Schemas**: activeContext, progress, mistakes, memory | **MCPs**: sequential-thinking, math, context7, fetch, memory, filesystem, time
