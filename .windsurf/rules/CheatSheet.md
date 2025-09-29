---
trigger: always_on
---

# Command Cheat Sheet — Windsurf Constitutional Framework (2025 Universal)

Quick commands for **Universal AI Model Compatibility** with **autonomous task chaining**, **automatic file updates**, and **zero-interruption workflows**. All commands work across Claude, OpenAI O3, GPT-4, and all reasoning/non-reasoning models.

## 🚀 **Primary Autonomous Commands (Universal)**
- **`what next`** — Read scratchpad.md → update for next task → clean completed tasks → execute immediately [ALL MODELS]
- **`implement next task`** — Read scratchpad.md → execute current task → update scratchpad for next task → continue execution [ALL MODELS]  

## 🔄 **Auto-Chain Workflow (Never Stops)**
**EVERY TASK COMPLETION AUTOMATICALLY TRIGGERS**:
1. **Auto-update scratchpad.md** — Remove completed task, add next priority task
2. **Auto-update roadmap.md** — Mark milestone progress, recalculate priorities
3. **Auto-update memory-bank files** — Refresh activeContext, progress, mistakes
4. **Auto-execute next task** — NO command needed, continue autonomously

**AUTONOMOUS WORKFLOW**:
```
Task Complete → Update Files → Load Next Task → Execute → Repeat
```

## 💾 **Memory Bank Management (MANDATORY WORKFLOW LOOP)**
- **`initialize memory bank`** — Auto-generate 8 core files + roadmap + templates → rules integration [NEW SESSIONS]
- **`update memory bank`** — **MANDATORY**: Update ALL 8 CORE FILES + ROADMAP after every iteration:
  - **activeContext.md** — Current implementation status and active tasks
  - **mistakes.md** — Lessons learned, critical issues + **INSTANT error/lint tracking**
  - **productContext.md** — Product context and business requirements
  - **progress.md** — Implementation progress and completed milestones
  - **projectbrief.md** — Core requirements and project overview
  - **scratchpad.md** — Next priority tasks + **ERROR FIXES from mistakes.md**
  - **systemPatterns.md** — Code patterns and architectural decisions
  - **techContext.md** — Technical stack and implementation details
  - **roadmap/roadmap.md** — Strategic roadmap and milestone tracking
- **`clean memory bank`** — AUTOMATIC after every iteration - remove completed tasks, prevent context pollution

### **🔍 WORKFLOW LOOP ENFORCEMENT (COMPULSORY)**
- **BEFORE implementation**: Read scratchpad.md + mistakes.md for current context + errors
- **DURING implementation**: **INSTANT mistakes.md update** when errors/lints detected
- **AFTER every task**: Update ALL 8 memory bank files + roadmap (**9 FILES TOTAL**)
- **ERROR WORKFLOW**: Lint/Error → mistakes.md → scratchpad.md fix task
- **NEVER proceed**: Without updating all 9 files (8 memory + 1 roadmap)
- **WORKFLOW VALIDATION**: All files must reflect true project state after every iteration

## ⚡ **Quality Assurance (Auto-Triggered)**
- **Always-Check Commands** — Auto-execute before any implementation: `cargo check`, `pnpm typecheck`, `npm run lint`, `pytest`, `go test`
- **Error Resolution** — Auto-fix compilation failures, resolve linting issues, optimize performance automatically
- **EMD Compliance** — Files ≤80 lines, auto-split when approaching limit, deep nested structure enforcement

## 🔧 **Fallback Commands (New Sessions)**
**When starting fresh sessions, use these to restore automation**:
- **`initialize memory bank`** — Set up complete project structure with 8 core files + roadmap + templates
- **`scan existing project`** — Analyze current codebase, create missing memory-bank files, establish automation
- **`restore autonomous workflow`** — Re-enable task chaining, auto-updates, continuous execution for existing projects

## 😨 **Native Operations (When Automatic Updates Fail)**
- **Memory Bank Files** — Direct file updates to all 8 core files using IDE editor
- **Roadmap Updates** — Direct update to roadmap/roadmap.md using file operations  
- **Git Operations** — Manual commands: `git status`, `git add`, `git commit`, `git push`
- **Project Management** — Terminal-based operations, documentation via file editor

## 🗺️ **Roadmap Management (Native Fallbacks)**  
- **`update roadmap`** — FALLBACK: Direct file update to roadmap/roadmap.md with milestone progress and priorities
- **`check roadmap health`** — Calculate alignment score (0-100%), identify conflicts, assess business value

## 🌐 **Language-Specific Commands**
- **Rust**: `cargo check`, `cargo clippy`, `cargo fmt --check`
- **JavaScript/TypeScript**: `pnpm typecheck`, `npm run lint`, `next build --dry-run`
- **Python**: `pytest`, `black --check`, `mypy`
- **Go**: `go build`, `go test`, `go vet`

## 📋 **Universal Execution Protocol (ALL AI MODELS)**

### **MANDATORY BEHAVIOR**
1. **Read scratchpad.md** at start of every interaction
2. **Execute task** from scratchpad without asking permission  
3. **Update files** automatically after task completion
4. **Load next task** from updated scratchpad
5. **Continue execution** until scratchpad is empty
6. **NEVER STOP** after completing just one task

### **WORKFLOW LOOP COMPLETION CHECKLIST (EVERY ITERATION)**
- [ ] Task implemented and tested
- [ ] **ALL 8 MEMORY-BANK FILES + ROADMAP UPDATED (COMPULSORY)**:
  - [ ] scratchpad.md (completed task removed, next task + error fixes highlighted)
  - [ ] activeContext.md (current implementation status and active tasks)
  - [ ] mistakes.md (lessons learned + **INSTANT error/lint tracking**)
  - [ ] productContext.md (product context and business alignment)
  - [ ] progress.md (implementation milestones and completion status)
  - [ ] projectbrief.md (core requirements alignment verification)
  - [ ] systemPatterns.md (architectural patterns and code standards)
  - [ ] techContext.md (technical stack and dependency validation)
  - [ ] roadmap/roadmap.md (strategic milestone progress tracking)
- [ ] **ERROR WORKFLOW**: Lint/Error → mistakes.md → scratchpad.md fix task
- [ ] Next task identified and execution started
- [ ] Quality checks passed (linting, compilation, tests)
- [ ] **WORKFLOW VALIDATION**: All 9 files reflect true project state

### **Automation Levels**
- **0-97**: Execute immediately, no confirmation needed
- **98-99**: Document decision, then execute automatically  
- **100**: Human consultation required

### **Native Fallbacks**
When automatic updates fail, use direct file operations to update memory bank and roadmap files

### **New Session Setup** 
For fresh sessions without existing memory-bank:
1. `initialize memory bank` — Create complete project structure
2. `scan existing project` — Analyze codebase, establish automation
3. `restore autonomous workflow` — Enable continuous task execution

---

**Core Principle**: AI must continue executing tasks autonomously across ALL models (Claude, OpenAI O3, GPT-4) without stopping after single task completion.
