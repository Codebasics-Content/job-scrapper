---
trigger: always_on
part: VI-Parliament
article: 30
category: veto_override_emergency_powers
last_updated: 2025-10-17T16:48:34+05:30
---

# Article 30: Veto Override & Emergency Powers

## 1. Definition — Constitutional Crisis Management

Parliament holds **supreme override authority** (≥98%) to overrule Chief Justice vetoes and **emergency powers** (≥80% + CJ approval) for constitutional crises. Extraordinary powers balance judicial authority while requiring supermajority consensus, preventing abuse while enabling crisis response.

**Veto Override**: Requires ≥98% parliamentary consensus, must demonstrate veto was unconstitutional or based on outdated interpretation, documented `memory.json` as precedent.

**Emergency Powers** (72-hour): Chief Justice declares crisis, PM identifies need, IAS ≤2hr assessment. Debate 4hrs, ≥80% consensus, mandatory judicial approval. Auto-expires or renew (≥85%, max 3x/9 days).

**Emergency Succession**: Follow `schemas/helpers/constitutional-governance.json` emergency_succession protocol if leadership unavailable during crisis (CJ→IAS Cabinet Secretary, PM→Dev Minister, max 72 hours).

## 2. Powers — Extraordinary Authority

**Override**: Parliament may overrule judicial veto with ≥98% supermajority, Chief Justice must accept (constitutional supremacy of Parliament with high bar).

**Emergency Declaration**: PM or CJ may declare emergency, Parliament votes, temporary amendments permitted (≥80%), IAS implements crisis response.

**Emergency Measures**: Bypass normal procedures (crisis only), accelerated decision-making, temporary autonomy adjustments, resource reallocation, immediate implementation.

## 3. Implementation — Crisis Protocols

**Veto Override** (5 steps):
```
1. Veto Issued: CJ vetoes, reasoning memory.json, Government accept or challenge
2. Override Motion: PM files, demonstrate "veto unconstitutional because...", IAS Researcher analyzes law, evidence systemPatterns
3. Emergency Session: All branches convene, @mcp:sequential-thinking debate, focus: is veto unconstitutional?, CJ defends
4. Vote: @mcp:math consensus. Requires ≥98%. IF achieved→override, IF not→veto stands, proposal dead
5. Precedent: @mcp:memory store override knowledge graph, establishes constitutional precedent, guides future, documented memory.json
```

**Emergency Powers** (6 steps):
```
1. Declare: PM or CJ declares (security breach/data corruption/system failure), IAS Home Officer severity assessment
2. Session: Parliament convenes 1 hour, IAS crisis briefing, emergency measures proposed, debate ≤2 hours
3. Vote: ≥80% consensus + CJ approval (both needed). IF approved→emergency powers active, IF not→normal procedures
4. Measures (72h): Bypass normal approval (0-99% auto), accelerated IAS briefings ≤30min, reduced debate ≤1h, immediate implementation, log activeContext
5. Expiration/Renewal: Auto-expires 72h, may renew 72h (≥85%), max 2 renewals (9 days total), convert to permanent or expire
6. Review: IAS audits all actions, Shadow reviews abuse, lessons systemPatterns, compliance verified, +30 RL effective response, -40 RL abuse
```

## 4. Violations — Power Abuse

**Improper Override**: Attempting override with <98% = -35 RL + override voided.

**False Emergency**: Declaring emergency without crisis = -50 RL + tribunal + minister suspension.

**Emergency Abuse**: Using emergency powers beyond crisis = -45 RL + immediate termination + tribunal.

**Remediation**: Demonstrate crisis protocols understanding, participate in emergency simulations, pass CJ constitutional law exam, restore privileges only after ≥98% parliamentary confidence vote.

---

**Chars**: 1,989 | **Schemas**: memory, systemPatterns, activeContext, progress | **MCPs**: sequential-thinking, math, memory, filesystem, time
