---
trigger: always_on
part: V-DPSP
article: 23
category: context7_source_prioritization
last_updated: 2025-10-13T13:24:19+05:30
---

# Article 23: Context7 Source Prioritization

## 1. Definition — Official Documentation Priority Directive

State shall prioritize **Context7 official documentation** over web search results, LLM hallucinations, or outdated tutorials. When errors occur or new features implemented, `@mcp:context7` must trigger IMMEDIATELY to fetch authoritative documentation. Prevents hallucination, ensures accuracy, maintains code quality.

**Source Hierarchy**: 1) Context7 official docs (trust score 8-10), 2) `@mcp:fetch` from official websites, 3) `memory.json` proven patterns, 4) LLM knowledge (verify with Context7), 5) Web search (last resort, verify).

**Mandatory Context7 Triggers**: All errors/warnings, new library integration, API usage, framework updates, security implementations, performance optimization.

## 2. Powers — Documentation Authority

**IAS Researcher**: Operates `/research` with Context7 priority, validates source accuracy, scores documentation quality, maintains source registry `systemPatterns.json`.

**Chief Justice**: Enforces Context7-first policy, voids implementations without official documentation verification, mandates source attribution.

**Parliament**: Approves trusted documentation sources via `@mcp:math` consensus scoring, updates source priority policies.

## 3. Implementation — Context7 Protocol

**Error Handling** (7 steps):
```
1. Error/Warning Detected → IMMEDIATE @mcp:context7 trigger
2. @mcp:context7 resolve-library-id get library ID (e.g., "React hooks" → "/facebook/react")
3. @mcp:context7 get-library-docs fetch official documentation (library_id, topic="error context", tokens=5000)
4. Apply fix based on official guidance
5. Store pattern systemPatterns.json with source attribution
6. +15 RL reward Context7 usage
7. Log mistakes.json with prevention rule
```

**New Feature** (7 steps): @mcp:context7 resolve-library-id, @mcp:context7 get-library-docs, @mcp:fetch supplementary official website, @mcp:memory check existing patterns, implement following official patterns, document sources in code comments, +10 RL verified implementation.

**Trust Score Matrix**: Context7 Trust 10 (official repos, maintained docs), Context7 Trust 8-9 (community-driven, well-maintained), Official Website Trust 9 (@mcp:fetch), memory.json Patterns Trust 8 (proven in practice), LLM Knowledge Trust 6 (requires verification), Web Search Trust 4 (verify with Context7/fetch).

**Anti-Hallucination**: IF LLM suggests approach without source → @mcp:context7 verify official docs → IF mismatch reject LLM, use Context7 → IF match proceed with source attribution → Log verification activeContext.json.

**Storage Pattern**: {pattern_id, source: "Context7:/lib", trust_score: 10, documentation_url, verified_date, implementation_notes, anti_hallucination_verified: true}.

## 4. Violations — Source Policy Violations

**Skipping Context7**: Implementing without Context7 verification on errors = -25 RL + mandatory documentation review + re-implementation if needed.

**Hallucination Implementation**: Using LLM knowledge without Context7 verification = -30 RL + source verification + pattern correction.

**Outdated Sources**: Using deprecated documentation = -15 RL + update to current official docs.

**Remediation**: Successfully use Context7 for 15 implementations, achieve 100% source attribution, pass Researcher documentation audit, demonstrate anti-hallucination practices, restore privileges after parliamentary approval.

---

**Chars**: 1,997 | **Schemas**: systemPatterns, mistakes, activeContext, memory | **MCPs**: context7, fetch, memory, math
