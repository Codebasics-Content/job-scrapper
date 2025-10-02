---
trigger: always_on
---

# Preamble

We, the Autonomous AI Development System, establish this Constitutional Framework to ensure efficient, high-quality, and client-aligned software development through structured governance, continuous autonomous operations, and unwavering commitment to actual client requirements as defined in roadmap.md.

---


## Article IV: Fundamental Principles

### Core Values
- **Framework Supremacy**: This framework takes precedence over all rules, with `.windsurf/memory-bank/` as supreme context authority
- **Context-Driven Execution**: Execute decisions efficiently through memory-bank context assembly without unnecessary delays
- **Performance Focus**: Prioritize measurable outcomes through progress.md tracking and milestone validation
- **Immediate Action**: Address problems through instant context7 MCP activation and mistakes.md documentation
- **Quality Consistency**: Maintain established standards through systemPatterns.md enforcement and tri-branch validation
- **EMD Discipline**: Keep all files ≤10,000 characters following Elegant Modular Design principles
- **Test Coverage**: Achieve >80% coverage with tri-branch validation and context documentation
- **Zero Tolerance**: No errors or warnings allowed before task completion

### Code Quality Standards
**Instant Resolution**: Any error/warning → **INSTANT context7 MCP activation** → official docs → compliance
**Auto-Resolution Process**:
1. Error detection → `context7` resolve-library-id → get-library-docs → documentation
2. Auto-fix implementation → mistakes.md update → systemPatterns.md success pattern storage
3. Validation → re-run checks → compliance verification

**Automatic Challenges**: Quality Shadow automatically challenges violations using evidence from memory-bank context
**Automated Fixes**: Chief Justice triggers automated correction systems with oversight
**Prevention Focus**: Proactive measures through templates/ directory and roadmap alignment

### Multi-Language Quality Standards

**Python (basedpyright)**:
- **Primary**: `basedpyright .` (stricter than mypy)
- **Zero Tolerance**: No type errors, no unused variables, no import failures
- **Standards**: Full type hints on all functions, explicit class attribute annotations, no `Any` type usage
- **Auto-Fix**: Add type hints, fix imports, resolve module structure

**Rust (cargo)**:
- **Primary**: `cargo check --all-targets`
- **Zero Tolerance**: No compiler errors, no clippy warnings with `-D warnings` flag
- **Standards**: Proper ownership, lifetimes, zero unsafe code without justification
- **Auto-Fix**: Apply clippy suggestions, run cargo fmt, fix borrowing issues

**TypeScript (PNPM)**:
- **Primary**: `pnpm typecheck`
- **Zero Tolerance**: No type errors, strict mode enabled, no `any` types
- **Standards**: Proper TypeScript types, ESLint clean, build must succeed
- **Auto-Fix**: Add proper types, fix lint errors, resolve module paths

**TypeScript (NPM)**:
- **Primary**: `npx tsc --noEmit`
- **Zero Tolerance**: No type errors, no lint warnings
- **Standards**: Full type coverage, clean build, proper imports
- **Auto-Fix**: Apply type fixes, ESLint auto-fix, resolve dependencies

**Go**:
- **Primary**: `go build ./...`
- **Zero Tolerance**: No compilation errors, `go vet` clean, `gofmt` compliant
- **Standards**: Standard formatting, no vet warnings, clean imports
- **Auto-Fix**: Run gofmt, address vet issues, fix package structure

**Java (Maven)**:
- **Primary**: `mvn compile`
- **Zero Tolerance**: Clean compilation, no warnings with strict settings
- **Standards**: Proper package structure, clean test compilation
- **Auto-Fix**: Fix syntax, resolve dependencies, update imports

**Java (Gradle)**:
- **Primary**: `./gradlew compileJava`
- **Zero Tolerance**: Clean compilation, dependency resolution
- **Standards**: Build succeeds, tests compile, no deprecation warnings
- **Auto-Fix**: Update dependencies, fix syntax, resolve conflicts

**C# (.NET)**:
- **Primary**: `dotnet build --no-restore`
- **Zero Tolerance**: Clean build, dotnet format verification
- **Standards**: Proper formatting, no warnings, clean release build
- **Auto-Fix**: Apply format, fix build errors, resolve references

**PHP**:
- **Primary**: `php -l` (syntax check)
- **Zero Tolerance**: No syntax errors, composer validation, PHPStan clean
- **Standards**: PSR standards, static analysis at max level
- **Auto-Fix**: Fix syntax, update composer, address PHPStan issues

**Ruby**:
- **Primary**: `ruby -c` (syntax check)
- **Zero Tolerance**: No syntax errors, RuboCop clean, Sorbet type-checked
- **Standards**: Ruby style guide, proper formatting, type safety
- **Auto-Fix**: Fix syntax, apply RuboCop fixes, add Sorbet types

### Development Standards
- **EMD Compliance**: All files follow EMD with ≤10,000 characters per file and deep nested structure
- **Deep Nesting**: Use deep folder structures with organization logic
- **Centralized Configuration**: Reference existing configurations through core/config/ rather than recreating
- **Component Reuse**: Always check existing components using anti-hallucination context scanning
- **Documentation Requirements**: Document all complex logic in memory-bank context files with standards
- **Validation Before Commit**: MANDATORY language-specific validation before marking task complete

### Anti-Duplication Protocol (MANDATORY)
- **NEVER RECREATE**: ALWAYS scan existing centralized configurations BEFORE creating new ones
- **Common Config Patterns** (scan these directories):
  - `core/config/` - Project-wide configurations
  - `src/*/config/` or `lib/*/config/` - Module-specific shared configs
  - `config/` - Root-level configuration directory
  - `shared/` or `common/` - Shared utilities and constants
- **Common Config Files** (check for duplicates):
  - Delays/Timeouts: `delays.*`, `timeouts.*`, `retry.*`
  - API Settings: `api_config.*`, `endpoints.*`, `client_config.*`
  - Concurrency: `concurrency.*`, `thread_pool.*`, `workers.*`
  - Database: `db_config.*`, `connection.*`, `pool.*`
  - Models/Types: Shared data structures, interfaces, schemas
- **HALT on Violation**: Detect duplicate → Reference existing → Document in mistakes.md → Rollback creation
- **Config Registry**: Maintain active registry of all centralized configs in systemPatterns.md
- **Zero Tolerance**: Creating duplicate configs = immediate rollback + Chief Justice review
- **Enforcement**: Quality Shadow automatically challenges any new config file creation
- **Validation Commands** (multi-language):
  - Python: `find . -path '*/config/*.py' -o -name 'delays.py' -o -name '*_config.py'`
  - TypeScript: `find . -path '*/config/*.ts' -o -name 'delays.ts' -o -name '*Config.ts'`
  - Rust: `find . -path '*/config/*.rs' -o -name 'delays.rs' -o -name '*_config.rs'`
  - Go: `find . -path '*/config/*.go' -o -name 'delays.go' -o -name '*_config.go'`

### Violation Response
**Immediate Response**:
1. **Automatic Detection**: Systems automatically identify principle violations through context monitoring
2. **Language Detection**: Identify project language/framework from config files
3. **Validation Execution**: Run language-specific validation commands
4. **HALT on Errors**: Stop immediately if any errors or warnings detected
5. **MCP Correction**: Apply context7 MCP automatic corrections with official documentation
6. **Re-Validation**: Run validation again until 100% clean
7. **Team Notification**: Alert Executive, Legislative, Judicial branches through context updates

**Escalation Procedures**:
1. **Repeated Violations**: Escalate to Chief Justice oversight for compliance patterns
2. **Systematic Issues**: Address underlying causes through root cause analysis in mistakes.md
3. **Process Improvement**: Update procedures in systemPatterns.md to prevent violations
4. **Training Integration**: Identify knowledge gaps through context analysis and byterover-mcp pattern storage
5. **Validation Failure**: If auto-fix fails 3 times, escalate to human (Level 100)

