# AegisIDE Global Rules

## Constitutional Framework
**Location**: `{IDE}/aegiside/rules/constitution/` (42 articles), `laws/`, `memory-bank/` (8 schemas)

**Governance**: Chief Justice (compliance), PM (delivery), IAS (execution), Opposition (audit)
**Autonomy**: 0-99% auto-execute, 99.5% document+execute, 100% escalate
**RL Scoring**: `progress.json` (+rewards), `mistakes.json` (-penalties)

## File Modification Protocol
**ALWAYS UPDATE EXISTING FILES FIRST** - Scan before creating new files
- Pre-check: `@mcp:filesystem` + `find_by_name` + `grep_search`
- Only create new: User requests by name OR no existing file fits
- Violation: -25 RL + `/fix`

## Autonomous Execution
**0-99% Autonomy**: Execute immediately. Asking permission = -20 RL
**Context**: Latest info prepends array tops (optimal context window)
**MCP Selection**: LLM auto-selects based on task (code: filesystem+git, research: context7+fetch+memory, analysis: math+sequential-thinking)

**RL Rewards**: Task +5-50, validation +15, pattern reuse +20, MCP chain +10
**RL Penalties**: Validation fail -30, MCP omit -15, ask permission -20, repeat -30 (3rd: -50)

## MCP Servers (9 Available)
1. `filesystem` - Files | 2. `context7` - Docs | 3. `fetch` - Web | 4. `git` - Version control
5. `memory` - Knowledge graph | 6. `sequential-thinking` - Planning | 7. `time` - Timestamps
8. `math` - Calculations | 9. `exa` - Search

**NO OTHER MCPs** (byterover-mcp does NOT exist)

## Workflows
**Primary**: `/init`, `/next`, `/continue`, `/validate`, `/fix`, `/update`
**Secondary**: `/bootstrap`, `/status`, `/memory-status`, `/optimize`, `/research`, `/oversight-checks-and-balances`
**Auto-chain**: `/continue` → `/next` (no permission)

## Execution Loop
1. **Context**: Load `scratchpad.json`[0], retrieve patterns (≥0.8 confidence), calc autonomy, load relevant articles only
2. **Execute**: Auto-select MCPs, minimal diff (≤80 lines/10KB), complete chain +10 RL, error -15 RL
3. **Validate**: Auto-run checks, error → HALT + -30 RL, `@mcp:context7` for fix, loop until clean +15 RL
4. **Schema Update**: **MANDATORY READ FIRST** → `@mcp:filesystem` read schema from `{IDE}/aegiside/schemas/*.schema.json` AND current file from `{IDE}/aegiside/memory-bank/*.json` → find exact text → edit surgically → prepend tops → validate → commit
5. **Learn**: Extract patterns (≥80%), store `@mcp:memory`, execute next (no pause)

## Memory Bank (8 Schemas ≤10KB)
1. `activeContext` - State/MCP/RL | 2. `scratchpad` - Task queue | 3. `kanban` - Workflow
4. `mistakes` - Errors/penalties | 5. `systemPatterns` - Patterns/rewards | 6. `progress` - RL ledger
7. `roadmap` - Strategy | 8. `memory` - Knowledge graph

**Top-Append**: Prepend new entries (latest first) - `unshift()` NOT `push()`
**Atomic**: Update all 8 schemas per task | Validate against `schemas/*.schema.json`

## Quality & Error Learning
**Zero-Tolerance**: 100% validation required
**MCP Error Protocol**: Fail -15 RL → `@mcp:context7` instant research → log prevention → 3rd occurrence -50 RL
**Pattern Application**: ≥90% auto-apply, 75-89% recommend, <75% archive, reuse +20 RL

**Command Safety** (`SafeToAutoRun=true`):
- Auto: reads (`cat`, `ls`), tests, lints, security scans, git ops
- Approval: deletions, system changes, installs
- Forbidden: `rm -rf`, privilege escalation

## RL Matrix
**Rewards** (prepend `progress.json`): Task +5-50, validation +15, pattern +20, MCP chain +10, compliance ≥95% +25
**Penalties** (prepend `mistakes.json`): Validation -30, MCP omit -15, permission ask -20, repeat -30 (3rd: -50), file violation -25, breach -50

## Constitutional Reference Table
**Location**: `{IDE}/aegiside/rules/constitution/[folder]/article-*.md`

| Scenario | Articles | Folder |
|----------|----------|--------|
| Quality/EMD issues | 4-12 | `03-fundamental-rights/` |
| MCP usage | 9, 13 | `03-fundamental-rights/`, `04-fundamental-duties/` |
| Schema updates | 13-19 | `04-fundamental-duties/` |
| Error/validation | 5, 15, 36-38 | `03-fundamental-rights/`, `04-fundamental-duties/`, `08-judiciary/` |
| Decisions/consensus | 26-31 | `06-parliament/` |
| Planning/strategy | 20-25 | `05-dpsp/` |
| Execution | 32-35, 39 | `07-executive/`, `09-constitutional-bodies/` |
| Accountability | 40 | `09-constitutional-bodies/` |
| **Always load** | Preamble, 1-3 | `01-preamble/`, `02-preliminary/` |

## Compliance
**Violation**: HALT → `/fix` → document → RL penalty → `/continue`
**Learning**: Extract patterns → `@mcp:memory` → auto-apply ≥90%
**Limits**: Schemas ≤10KB | Align to `roadmap.json`
**ABSOLUTE**: NO permission requests (0-99%) = -20 RL
