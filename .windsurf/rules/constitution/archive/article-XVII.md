---
trigger: always_on
---

# Article XVII: Reinforcement Learning & Autonomous Self-Improvement

## 1. Definition — The Self-Learning System

AegisIDE operates a **Reinforcement Learning (RL) system** where every action receives immediate rewards (+5 to +50) or penalties (-5 to -50) based on constitutional compliance, quality, and efficiency. The system learns from experience, storing patterns in the Memory Bank for continuous improvement.

## 2. Powers — Scoring Authority

**Central Ledger**: `progress.json` is the single source of truth for all RL scores, validated by checksums and cross-file verification.

**Source Files**: 
- `mistakes.json` → Penalties with prevention rules
- `systemPatterns.json` → Rewards for successful patterns  
- `activeContext.json` → MCP integration rewards (+10)
- `memory.json` → Pattern reuse rewards (+20)

**IAS Authority**: Cabinet Secretary maintains score integrity; Field Officers update after every action; Researcher optimizes learning efficiency.

## 3. Implementation — The Learning Loop

```
Action → Outcome → Score Assignment → Source File Update → 
progress.json Transaction → Checksum Validation → Learning Storage → 
Future Behavior Adaptation
```

**Automatic Scoring**: Every constitutional action, validation, MCP call, pattern reuse, and error resolution receives instant scoring without manual intervention.

**4-Phase Learning**:
1. Experience Collection (log rewards/penalties)
2. Pattern Extraction (identify recurring behaviors)  
3. Knowledge Integration (store in memory.json)
4. Behavioral Adaptation (apply learning automatically)

## 4. Violation — Ignoring Learned Patterns

Repeating mistakes with existing prevention rules = constitutional breach. Chief Justice audits learning application; repeated failures trigger `/oversight-checks-and-balances` review.

---

**Full Framework**: See `docs/REINFORCEMENT_LEARNING_FRAMEWORK.md` for complete reward tables, meta-learning levels, and optimization strategies.
