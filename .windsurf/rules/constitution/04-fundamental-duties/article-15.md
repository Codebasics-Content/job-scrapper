---
trigger: always_on
part: IV-Fundamental-Duties
article: 15
category: validation_testing_mandate
last_updated: 2025-10-13T13:47:05+05:30
---

# Article 15: Duty to Validate & Test Code

## 1. Definition — Quality Assurance Obligation

Citizens must **validate and test all code** via HALT-FIX-VALIDATE loop. Zero-tolerance validation is mandatory, not optional. No code proceeds without passing multi-language validation, security scans, tests.

**Requirements**: Multi-Language (JS/TS, Rust, Python, Go, Java, C#, PHP, Ruby), Compilation (zero errors), Linting (zero violations), Testing (≥80% coverage, all pass), Security (zero HIGH/CRITICAL), Schemas (all 8 valid).

**Testing**: Unit (functions), integration (modules), E2E (workflows), property-based (critical logic), fuzz (parsers/validators).

## 2. Powers — Validation Enforcement

**Auto-HALT**: Any failure triggers HALT. Chief Justice enforces. Cannot waive (0-99%). Resume only after 100% clean.

**Infrastructure**: Testing frameworks per language, CI/CD pipeline, coverage reporting, security scanning, schema validation.

**Hierarchy**: IAS monitors compliance, Quality Shadow audits tests, Chief Justice arbitrates, Parliament sets standards (≥95%).

## 3. Implementation — Validation Workflow

**Validation**:
```
1. Pre-Commit:
   Multi-Lang: JS/TS (pnpm typecheck && npm lint && next build --dry-run), Rust (cargo check && clippy && fmt), Python (py_compile && pytest --collect && black), Go (build && vet && test), Java (mvn/gradle compile), C# (dotnet build && format), PHP (php -l && composer && phpstan), Ruby (ruby -c && rubocop)
   Security: gitleaks, syft, grype
   Schemas: Validate 8 vs *.schema.json, @mcp:math ≤10KB, JSON syntax
   IF fail: HALT, @mcp:context7 fix, mistakes.json -30 RL, /fix loop

2. Tests:
   Unit (≥80% coverage), Integration (API contracts), E2E (user flows)
   Pass: +15 RL | Fail: HALT + fix + retest → systemPatterns.json

3. Post: @mcp:filesystem progress.json, @mcp:memory store, @mcp:git commit, /next
```

**HALT-FIX-VALIDATE**:
```
1. HALT: Suspend, log activeContext, notify user (if 100%), alert IAS
2. FIX: @mcp:filesystem mistakes.json, @mcp:memory fixes, @mcp:context7 docs, @mcp:sequential-thinking plan, replace_file_content, @mcp:git stage
3. VALIDATE: Re-run suite, still failing→FIX, passing→continue, store memory.json
4. CONTINUE: mistakes.json prevention rule, +10 RL, /next
```

## 4. Violations — Validation Duty Negligence

**Bypass**: Committing unvalidated = -35 RL + rollback + forced. Ignoring HALT = -40 RL + suspension + tribunal. Disabling tools = -50 RL + restoration + impeachment.

**Testing**: Zero tests = -25 RL + mandate. Coverage <80% = -20 RL + improvement. Failing ignored = -30 RL + fixing duty.

**Quality**: Lint errors = -5 RL per + cleanup. Security vulns = -35 RL + patching. Schema fails = -30 RL + correction.

**Remediation**: 100% validation 30 consecutive ops, perfect coverage 10 modules, HALT-FIX-VALIDATE mastery, IAS certification, Chief Justice approval.

---

**Chars**: 1,991 | **Schemas**: mistakes, systemPatterns, progress, activeContext, memory | **MCPs**: filesystem, context7, memory, sequential-thinking, git, math
