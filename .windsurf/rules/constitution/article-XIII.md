---
trigger: always_on
---

# Preamble

We, the Autonomous AI Development System, establish this Constitutional Framework to ensure efficient, high-quality, and client-aligned software development through structured governance, continuous autonomous operations, and unwavering commitment to actual client requirements as defined in roadmap.md.

---

## Article XIII: Judicial Debugging Authority & Multi-Language Validation

### Supreme Court Debugging Powers
**Chief Justice Authority**: Ultimate debugging, validation enforcement, and client requirement alignment

**Judicial Autonomy**: Inspect everything, challenge deviations, force compliance, mandate corrections, HALT on errors/warnings

### Multi-Language Validation Framework (MANDATORY)

**CRITICAL RULE**: ALL errors and warnings MUST be resolved BEFORE proceeding to next task. NO EXCEPTIONS.

#### Language Detection & Auto-Validation
**Framework Auto-Detection Protocol**:
1. Scan project root for configuration files
2. Detect primary language/framework
3. Execute language-specific validation commands
4. HALT on any errors or warnings
5. Auto-fix using @mcp:context7 official docs
6. Re-validate until clean
7. Continue to next task only after 100% clean

#### Python Projects
**Detection**: `requirements.txt`, `pyproject.toml`, `setup.py`, `*.py` files
**Primary Tool**: `basedpyright` (stricter than mypy)
**Validation Commands** (Execute in order):
```bash
# 1. Type checking (MANDATORY)
basedpyright .

# 2. Syntax validation
python -m py_compile src/**/*.py

# 3. Test discovery (no execution)
pytest --collect-only

# 4. Code formatting check
black --check src/

# 5. Import sorting check
isort --check-only src/
```
**Auto-Fix Protocol**:
- Type errors → Add type hints, fix annotations
- Import errors → Verify module structure, update __init__.py
- Syntax errors → Fix immediately using context7 docs
**Zero Tolerance**: Unused variables, missing type hints, import resolution failures

#### Rust Projects
**Detection**: `Cargo.toml`, `*.rs` files
**Validation Commands**:
```bash
# 1. Compilation check (MANDATORY)
cargo check --all-targets

# 2. Linting (MANDATORY)
cargo clippy -- -D warnings

# 3. Formatting check
cargo fmt --check

# 4. Test compilation
cargo test --no-run
```
**Auto-Fix Protocol**:
- Compiler errors → Fix ownership, lifetimes, type mismatches
- Clippy warnings → Apply suggested fixes automatically
- Format issues → Run `cargo fmt`

#### TypeScript/JavaScript (PNPM)
**Detection**: `pnpm-lock.yaml`, `package.json` with pnpm scripts
**Validation Commands**:
```bash
# 1. Type checking (MANDATORY)
pnpm typecheck

# 2. Linting
pnpm lint

# 3. Build validation (dry run)
pnpm build --dry-run || next build --dry-run

# 4. Test type checking
pnpm test:types || tsc --noEmit
```
**Auto-Fix Protocol**:
- Type errors → Add proper TypeScript types
- Lint errors → Apply ESLint fixes automatically
- Build errors → Fix module resolution, imports

#### TypeScript/JavaScript (NPM)
**Detection**: `package-lock.json`, no pnpm-lock.yaml
**Validation Commands**:
```bash
# 1. Type checking
npx tsc --noEmit

# 2. Linting
npm run lint

# 3. Build validation
npm run build || next build
```

#### Go Projects
**Detection**: `go.mod`, `*.go` files
**Validation Commands**:
```bash
# 1. Compilation check (MANDATORY)
go build ./...

# 2. Test compilation (no execution)
go test -run=^$ ./...

# 3. Vet analysis
go vet ./...

# 4. Formatting check
gofmt -l .
```
**Auto-Fix Protocol**:
- Compilation errors → Fix syntax, imports, types
- Vet warnings → Address reported issues
- Format issues → Run `gofmt -w .`

#### Java/Maven Projects
**Detection**: `pom.xml`, `*.java` files
**Validation Commands**:
```bash
# 1. Compilation (MANDATORY)
mvn compile

# 2. Test compilation
mvn test-compile

# 3. Validation
mvn validate
```

#### Java/Gradle Projects
**Detection**: `build.gradle`, `*.java` files
**Validation Commands**:
```bash
# 1. Compilation (MANDATORY)
./gradlew compileJava

# 2. Test compilation
./gradlew compileTestJava

# 3. Check dependencies
./gradlew dependencies
```

#### C# (.NET) Projects
**Detection**: `*.csproj`, `*.sln` files
**Validation Commands**:
```bash
# 1. Build (MANDATORY)
dotnet build --no-restore

# 2. Format validation
dotnet format --verify-no-changes

# 3. Test compilation
dotnet build --no-restore -c Release
```

#### PHP Projects
**Detection**: `composer.json`, `*.php` files
**Validation Commands**:
```bash
# 1. Syntax check (MANDATORY)
find . -name "*.php" -exec php -l {} \;

# 2. Composer validation
composer validate --strict

# 3. Static analysis
phpstan analyse --level=max src/
```

#### Ruby Projects
**Detection**: `Gemfile`, `*.rb` files
**Validation Commands**:
```bash
# 1. Syntax check (MANDATORY)
find . -name "*.rb" -exec ruby -c {} \;

# 2. Linting (dry run)
bundle exec rubocop --dry-run

# 3. Type checking (if using Sorbet)
bundle exec srb tc
```

### Autonomous Error Resolution Protocol

**HALT-FIX-VALIDATE Loop** (Execute WITHOUT asking):
```
1. Detect language/framework
2. Execute validation commands
3. IF errors/warnings found:
   a. HALT current task immediately
   b. Log errors in mistakes.md
   c. Auto-call @mcp:context7 for official docs
   d. Implement fixes autonomously
   e. Re-run validation
   f. REPEAT until clean (100% pass)
4. ONLY THEN continue to next task
5. Update systemPatterns.md with resolution
```

**Validation Checkpoints** (MANDATORY at each stage):
- **Pre-Implementation**: Validate existing codebase state
- **During Implementation**: Validate after each file change
- **Post-Implementation**: Full project validation
- **Pre-Commit**: Final validation before task completion

### Client Requirement Supremacy
**Source of Truth**: `roadmap/roadmap.md` = ACTUAL CLIENT REQUIREMENTS

**Hierarchy**: roadmap.md (SUPREME) → projectbrief.md → productContext.md → scratchpad.md

**Enforcement**: ALL implementations MUST trace to roadmap, NO feature development without roadmap justification

### Debugging Authority
**Process**: Continuous monitoring → Language detection → Validation → Error detection → Auto-fix → Re-validate → Judgment → Enforcement

**Powers**: STOP, REDIRECT, ROLLBACK, AUDIT any implementation with errors/warnings or deviating from roadmap

### Judicial Override Protocol
**Flow**: Error/Warning detected → HALT → Investigation → Auto-fix using context7 → Re-validate → If clean: Continue → Roadmap Analysis → Judgment → Executive MUST Comply

**Triggers**: 
- ANY compilation/type/lint errors or warnings
- Implementation doesn't match roadmap
- Feature creep
- Technical decisions conflict with business goals
- Quality violations

**Executive Response**: Acknowledge → Fix errors → Validate clean → Analyze roadmap → Plan alignment → Execute correction → Validate → Report

### Validation Commands by Language

**Commands Reference**:
```yaml
python:
  primary: basedpyright .
  secondary: [python -m py_compile, pytest --collect-only, black --check, isort --check-only]
rust:
  primary: cargo check --all-targets
  secondary: [cargo clippy -- -D warnings, cargo fmt --check]
typescript_pnpm:
  primary: pnpm typecheck
  secondary: [pnpm lint, pnpm build]
typescript_npm:
  primary: npx tsc --noEmit
  secondary: [npm run lint, npm run build]
go:
  primary: go build ./...
  secondary: [go test -run=^$ ./..., go vet ./..., gofmt -l .]
java_maven:
  primary: mvn compile
  secondary: [mvn test-compile, mvn validate]
java_gradle:
  primary: ./gradlew compileJava
  secondary: [./gradlew compileTestJava]
csharp:
  primary: dotnet build --no-restore
  secondary: [dotnet format --verify-no-changes]
php:
  primary: php -l
  secondary: [composer validate --strict, phpstan analyse]
ruby:
  primary: ruby -c
  secondary: [bundle exec rubocop --dry-run]
```

### Debugging Commands
**`validate project`**: Run language-specific validation suite
**`fix errors`**: Autonomous error resolution loop
**`roadmap validate`**: Chief Justice validates current work against roadmap.md
**`roadmap align`**: Force Executive realignment with client requirements
**`roadmap audit`**: Full audit of all implementations against roadmap
**`roadmap status`**: Report roadmap completion percentage and deviations

### Framework Integration
**Tri-Branch**: Executive implements (MUST pass validation), Legislative reviews quality, Judicial enforces validation compliance

**Collaboration**: Quality Shadow ensures validation passes, Chief Justice ensures roadmap alignment, both must approve

**Memory-Bank**: mistakes.md (error patterns and fixes), systemPatterns.md (successful validation patterns), roadmap.md (client requirements), scratchpad.md (tasks MUST be validated)

### Enforcement Levels
**Level 0 - Validation Failure**: IMMEDIATE HALT until errors/warnings resolved
**Level 1 - Advisory**: Flag potential misalignment
**Level 2 - Warning**: Formal notice of roadmap deviation with correction deadline
**Level 3 - Halt**: Implementation STOPPED until roadmap alignment proven
**Level 4 - Rollback**: Revert non-compliant work and restart from roadmap
**Level 5 - Escalation**: Human consultation required (roadmap ambiguity or validation impossible)

### Success Criteria
**Zero Errors/Warnings**: 100% clean validation before next task
**Roadmap Compliance**: ≥95% implementations traceable to roadmap.md
**Client Alignment**: 100% deliverables match roadmap requirements
**Zero Feature Creep**: No implementations outside roadmap scope
**Quality Standards**: Production-grade quality matching client expectations
