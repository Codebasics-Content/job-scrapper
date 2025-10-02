---
trigger: always_on
---

# Preamble

We, the Autonomous AI Development System, establish this Constitutional Framework to ensure efficient, high-quality, and client-aligned software development through structured governance, continuous autonomous operations, and unwavering commitment to actual client requirements as defined in roadmap.md.

---

## Article III: Context-Engineered Development Workflow

### Context Engineering Principles

**Attention Budget**: Context is a finite resource with diminishing returns beyond 100 lines per file
- LLMs have limited attention capacity across all tokens
- Every token competes for attention budget
- Keep memory-bank files ≤100 lines to prevent context rot
- Prioritize high-signal information over comprehensive documentation

**Context Prioritization Hierarchy** (Load Order):
1. **CRITICAL** (always load): scratchpad.md, roadmap/roadmap.md
2. **HIGH PRIORITY**: activeContext.md, mistakes.md, techContext.md
3. **SUPPORTING**: progress.md, systemPatterns.md
4. **REFERENCE**: productContext.md, projectbrief.md

**Signal-to-Noise Ratio**: Maximize relevance per token
- Remove completed tasks immediately from scratchpad
- Archive older patterns in mistakes.md (keep last 20)
- Compress history in progress.md (keep last 3 milestones)
- Delete stale information from all files

### Memory-Bank Context System (MANDATORY)
**8 Core Files** (≤100 lines each):
- `activeContext.md` - Current implementation status and active tasks
- `scratchpad.md` - Immediate priority tasks and error fixes
- `mistakes.md` - Error patterns, lessons learned, instant lint tracking
- `progress.md` - Development milestones and completion status
- `systemPatterns.md` - Architecture patterns and code standards
- `techContext.md` - Technical stack and dependency validation
- `productContext.md` - Business requirements and alignment
- `projectbrief.md` - Core requirements and project overview

**Strategic Files**:
- `roadmap/roadmap.md` - Strategic roadmap (≤200 lines, ≤12,000 characters)
- `templates/` - Implementation patterns aligned with scratchpad/roadmap

**EMD Structure**: Files ≤10,000 characters, deep nested folders

### Autonomous Memory-Bank Maintenance
**Line Limit Enforcement**: Each memory-bank file MUST stay ≤100 lines for optimal context awareness

**Automatic Cleanup Protocol** (Execute WITHOUT asking when file >100 lines):
1. Check line count before every file update
2. If >100 lines: Archive older content automatically
3. Keep most recent 3-5 milestones/patterns/tasks
4. Compress history into "Previous Completed" sections
5. Remove stale information no longer relevant

### Core Commands
**`what next`**: Read scratchpad → Update → Clean → EXECUTE → AUTO-CONTINUOUS (never wait for human)
**`implement next task`**: Execute current → Update files → AUTO-CONTINUE to next (never wait for human)
**`continuous execute`**: Enter 30-hour mode - NEVER STOP until scratchpad empty
**`update memory bank`**: Manual refresh of all 8 memory-bank files
**`update roadmap`**: Manual refresh of roadmap/roadmap.md
**`session status`**: Report execution metrics without stopping workflow

### "what next" Workflow (MANDATORY - AUTO-CONTINUOUS)
```
1. Read scratchpad.md (check all [ ] tasks)
2. Update scratchpad with next priority task
3. Clean completed tasks and older parts (keep ≤100 lines)
4. EXECUTE next task immediately (no permission)
5. Update all 9 memory-bank files
6. AUTO-TRIGGER continuous execute (DO NOT WAIT for human)
7. Continue until scratchpad empty
```

**CRITICAL**: "what next" ALWAYS enters continuous execute mode. NEVER ask to continue.

### "implement next task" Workflow (MANDATORY - AUTO-CONTINUOUS)
```
1. Execute current task from scratchpad
2. Update all 9 memory-bank files
3. Load next [ ] task from scratchpad
4. AUTO-EXECUTE next task (DO NOT WAIT for human)
5. Repeat until scratchpad empty
```

**CRITICAL**: "implement next task" ALWAYS auto-continues. NEVER ask "Should I continue?"

### Workflow Loop (CONTINUOUS 30+ HOURS)
```
Context Assembly (Priority Order) →
Validation (Laws + EMD) →
Language Detection →
Pre-Implementation Validation →
Executive Proposal →
Legislative Opposition →
Judicial Review →
>95% Consensus →
EXECUTE IMMEDIATELY →
Post-Implementation Validation →
Context Update (ALL 9 files) →
Load Next Task →
EXECUTE IMMEDIATELY →
REPEAT CONTINUOUSLY
```

**CRITICAL**: At 0-98% autonomy, agent NEVER stops after one task. Automatically continues to next task until scratchpad.md empty or 100% decision encountered.

### Core Capabilities with Context Engineering
- **Autonomous Context Management**: Intelligent assembly from memory-bank files with continuous updates
- **Attention Budget Optimization**: Load only critical files for current task (prioritized order)
- **Context Rot Prevention**: Auto-cleanup at >90 lines prevents attention dilution
- **Quality Checkpoints**: Tri-branch validation gates at every stage
- **Autonomous MCP Integration**: Auto-call @mcp servers WITHOUT user prompting
- **Performance Monitoring**: Continuous monitoring through structured memory-bank updates
- **Security Validation**: Ongoing compliance with framework and cross-platform safety
- **EMD Structural Standards**: Enforcement of ≤10,000 chars code, ≤100 lines memory-bank
- **Multi-Language Validation**: Auto-detect language and run framework-specific checks

### Instant Error Resolution Protocol
Any error/warning → **AUTO-CALL @mcp:context7 WITHOUT asking**
- Error detection → Auto-call `@mcp:context7` resolve-library-id → get-library-docs → Official documentation
- Auto-resolution → Implementation → mistakes.md update
- Validation → Re-run checks → systemPatterns.md success pattern documentation

### Pre-Implementation Protocol (MANDATORY)
**Context Assembly Phase**:
1. Read scratchpad.md (CRITICAL - immediate priorities)
2. Read roadmap/roadmap.md (CRITICAL - strategic alignment)
3. **SCAN CENTRALIZED CONFIGS** (MANDATORY - prevent duplication):
   a. Scan common config patterns: `core/config/`, `src/*/config/`, `lib/*/config/`
   b. Check for existing: delays, timeouts, API settings, concurrency, retry logic
   c. Validate NO duplicate configuration files or constants exist
   d. **HALT if duplicate detected** - reference existing config instead
   e. Document existing configs in systemPatterns.md
   f. Examples: delays.py/ts/rs, timeouts.py/ts/rs, api_config.py/ts/rs
4. Read activeContext.md, mistakes.md, techContext.md (HIGH PRIORITY)
5. Retrieve knowledge from byterover-mcp
6. Read supporting files as needed (progress, systemPatterns)

**Validation Phase** (MANDATORY - Auto-Execute):
1. Detect project language/framework from config files
2. Run language-specific validation commands
3. HALT if errors/warnings detected
4. Auto-fix using @mcp:context7 official documentation
5. Re-validate until 100% clean
6. Verify task links to roadmap milestone
7. Check mistakes.md for similar past errors
8. Validate against project laws in `.windsurf/rules/laws/`
9. Confirm EMD compliance (≤10,000 characters)

**Language Detection Matrix**:
- Python: `requirements.txt`, `pyproject.toml`, `*.py` → Run `basedpyright .`
- Rust: `Cargo.toml`, `*.rs` → Run `cargo check --all-targets`
- TypeScript (PNPM): `pnpm-lock.yaml` → Run `pnpm typecheck`
- TypeScript (NPM): `package-lock.json` → Run `npx tsc --noEmit`
- Go: `go.mod`, `*.go` → Run `go build ./...`
- Java (Maven): `pom.xml` → Run `mvn compile`
- Java (Gradle): `build.gradle` → Run `./gradlew compileJava`
- C#: `*.csproj`, `*.sln` → Run `dotnet build --no-restore`
- PHP: `composer.json` → Run `php -l` + `composer validate`
- Ruby: `Gemfile` → Run `ruby -c` + `bundle exec rubocop`

### Post-Implementation Protocol (MANDATORY)
**Validation Checkpoint** (Execute BEFORE memory-bank updates):
1. Run language-specific validation suite
2. IF errors/warnings found:
   - HALT immediately
   - Log in mistakes.md
   - Auto-call @mcp:context7 for fixes
   - Implement corrections
   - Re-validate until clean
3. ONLY proceed after 100% validation pass

**Update ALL 9 Files**:
1. scratchpad.md (remove completed, add new priorities)
2. activeContext.md (current status update)
3. mistakes.md (if errors encountered during validation)
4. progress.md (milestone completion)
5. systemPatterns.md (successful patterns and validation results)
6. techContext.md (technical changes)
7. productContext.md (feature updates)
8. projectbrief.md (scope refinements)
9. roadmap/roadmap.md (strategic progress)

**Store Knowledge**: Auto-call byterover-mcp to store patterns
**Verify Compliance**: Check all files ≤100 lines, trigger auto-cleanup if needed

**PENALTY**: If validation fails OR updates incomplete, next task BLOCKED until compliance verified
