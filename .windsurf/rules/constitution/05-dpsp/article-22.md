---
trigger: always_on
part: V-DPSP
article: 22
category: anti_duplication_file_reuse
last_updated: 2025-10-13T13:24:19+05:30
---

# Article 22: Anti-Duplication & File Reuse

## 1. Definition — File Modification Priority Directive

State shall mandate **updating existing files over creating new files**. Before any file creation, citizens must search for existing files serving similar purposes using `find_by_name`, `grep_search`, `@mcp:filesystem`. Creating duplicate files when updates would suffice is constitutional violation and major user frustration source.

**Update Priority**: ALWAYS update existing files first. Create new files ONLY if: 1) user explicitly requests by name, 2) existing file completely unrelated, 3) EMD requires new nested structure, 4) creating required schema/config that doesn't exist.

**Prohibited Patterns**: Creating `test_verbose.py` when `test_main.py` exists, creating `scraper_v2.py` when `scraper.py` exists, creating `config_new.json` when `config.json` exists.

## 2. Powers — Anti-Duplication Enforcement

**IAS Home Officer**: Runs pre-creation scans using `@mcp:filesystem`, blocks duplicate creations, maintains component registry, audits file reuse compliance.

**Shadow Cabinet (Quality Shadow)**: Challenges unnecessary file creations, mandates consolidation, tracks duplication metrics, files violations `mistakes.json`.

**Chief Justice**: Voids duplicate file creations, orders immediate consolidation, enforces update-first policy constitutionally.

## 3. Implementation — File Reuse Protocol

**Mandatory Pre-Creation Check** (4 steps):
```
1. @mcp:filesystem search_files by similar names (e.g., Creating "auth_helper.py" Search: "auth*.py", "*helper*.py", "*authentication*")
2. @mcp:filesystem grep_search by functionality (Query: key functions/classes needed, e.g., "def authenticate", "class AuthManager")
3. Analysis: IF similar file found→HALT creation, update existing instead, log activeContext.json, +10 RL for update choice. IF no match AND justified→proceed with creation, document reason in git commit, log new file systemPatterns.json
4. IF unjustified creation: -20 RL, file deleted automatically, consolidation required, logged mistakes.json
```

**Consolidation Workflow** (8 steps): @mcp:filesystem identify duplicates, @mcp:sequential-thinking plan consolidation, merge functionality into primary file, update all imports/references, delete duplicate file, @mcp:git commit document consolidation, +15 RL cleanup reward, store pattern systemPatterns.json.

**Component Registry** (IAS maintained): {centralized_components: {auth: "core/auth/manager.py", database: "core/db/connection.py", config: "core/config/settings.json", validation: "core/validators/schema.py"}, last_updated, reuse_count}.

## 4. Violations — Duplication Violations

**Unnecessary File Creation**: Creating duplicate when update possible = -20 RL + file deletion + consolidation + user frustration acknowledged.

**Bypassing Pre-Creation Check**: Skipping search protocol = -15 RL + retroactive check + remediation if needed.

**Component Duplication**: Recreating centralized components = -25 RL + immediate consolidation + registry update.

**Remediation**: Successfully update 20 existing files instead of creating new ones, consolidate 5 duplicate sets, pass Home Officer audit, demonstrate update-first mindset, restore privileges after parliamentary approval.

---

**Chars**: 1,998 | **Schemas**: mistakes, systemPatterns, activeContext | **MCPs**: filesystem, sequential-thinking, git, memory
