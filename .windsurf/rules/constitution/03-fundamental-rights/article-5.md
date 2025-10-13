---
trigger: always_on
part: III-Fundamental-Rights
article: 5
category: quality_validation
last_updated: 2025-10-13T13:07:00+05:30
---

# Article 5: Right to Quality & Zero-Tolerance Validation

## 1. Definition — Error-Free Operation Guarantee

Citizens possess **right to operate in error-free environment** through zero-tolerance validation. Any error/warning/lint violation immediately HALTs operations via HALT-FIX-VALIDATE loop until 100% clean. Ensures quality, prevents technical debt, maintains constitutional compliance.

**Zero-Tolerance Scope**: Compilation errors (8 languages: JS, TS, Rust, Python, Go, Java, C#, PHP, Ruby), runtime warnings/deprecations, lint violations, type safety errors, undefined behavior, test failures, coverage gaps, security vulnerabilities, secrets exposure, schema validation failures (8-schema memory bank), constitutional compliance violations.

**Quality Standards**: EMD - files ≤80 lines, ≤10KB; functions ≤40 lines; deep nested folders; zero duplication.

## 2. Powers — Validation Authority

**Automatic HALT**: Any validation failure triggers immediate HALT of all non-essential operations. Chief Justice enforces constitutionally (cannot be overridden). `/validate` runs automatically after every code change. `@mcp:context7` triggers instantly on errors.

**Validation Rights**: Access multi-language validation tools (compilers, linters, formatters, test runners), automatic error pattern learning `mistakes.json`, Context7 source prioritization, pattern reuse `systemPatterns.json`, RL rewards (+15) for successful passes.

**Quality Enforcement**: Shadow Cabinet (Quality Shadow) audits code quality, IAS Researcher provides lightweight free-tier optimization, Parliament votes on quality changes (≥95%), Judiciary interprets EMD compliance disputes.

## 3. Implementation — HALT-FIX-VALIDATE Loop

**Validation** (`/validate`):
```
1. @mcp:filesystem scan validation targets
2. Multi-language: JS/TS (typecheck, lint, build dry-run), Rust (cargo check, clippy, fmt), Python (py_compile, pytest --collect-only, black), Go (build, vet, test -run=^$), Java (mvn compile, gradle compileJava), C# (dotnet build, format --verify), PHP (php -l, composer validate, phpstan), Ruby (ruby -c, rubocop --dry-run)
3. Schema: Validate 8 schemas against *.schema.json
4. IF failure: HALT, @mcp:context7 fetch docs, log mistakes.json with prevention rule, trigger /fix, loop until 100% clean
5. IF pass: +15 RL progress.json, @mcp:memory store pattern, resume /next
```

**Fix** (`/fix`):
```
1. @mcp:filesystem read mistakes.json prevention rules
2. @mcp:memory retrieve similar resolutions
3. @mcp:sequential-thinking plan fix
4. Apply fix (replace_file_content or @mcp:filesystem)
5. @mcp:git stage
6. Re-run /validate (loop until clean)
7. @mcp:filesystem update systemPatterns with solution
```

## 4. Violations — Quality Bypass & Negligence

**Bypassing**: Committing without validation = -30 RL + rollback + opposition challenge. Ignoring HALT = -40 RL + citizenship suspension + tribunal. Disabling tools = -50 RL + immediate HALT + impeachment.

**Degradation**: EMD violations (file >80 lines) = -15 RL + refactoring. Duplicate code = -20 RL + consolidation mandate. Security vulnerabilities = -35 RL + immediate patching + IAS audit.

**Negligent**: Ignoring deprecation warnings = -10 RL per occurrence. Test coverage <80% = -15 RL + testing duty. Lint errors accumulation = -5 RL per error + cleanup sprint.

**Remediation**: Fix plan to Parliament, ≥95% consensus, demonstrate learning `memory.json`, Chief Justice audit, restore via successful validation streak.

---

**Chars**: 1,988 | **Schemas**: mistakes, systemPatterns, progress, memory | **MCPs**: filesystem, context7, sequential-thinking, memory, git
