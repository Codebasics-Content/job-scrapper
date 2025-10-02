# System Patterns - Job Scrapper

## Anti-Bot Detection Patterns (Naukri.com)

**Naukri Anti-Bot System** (2025-10-02T12:38):
- **Akamai Bot Manager**: Active with reCAPTCHA enforcement
- **API Protection**: Returns `{"message":"recaptcha required","statusCode":406}`
- **Detection Method**: Advanced fingerprinting beyond headers
- **Required for API**: Valid browser session cookies + reCAPTCHA tokens
- **Direct API Calls**: BLOCKED - Cannot bypass reCAPTCHA programmatically
- **Working Solution**: Browser automation with Selenium + undetected-chromedriver
- **Alternative**: Use browser_scraper.py instead of api_fetcher.py
- **Pattern**: Sites with reCAPTCHA require full browser automation, not API calls
- **Lesson**: Test API endpoints first before building scraper architecture

## Documentation Patterns

**Multi-Platform README Structure** (2025-10-02T12:11):
- **Title Update**: Reflect all supported platforms in main heading
- **Platform Comparison**: Use separate sections for different approaches (browser vs API)
- **Step Numbering**: Adjust UI instructions when adding platform selection
- **Performance Metrics**: Provide platform-specific benchmarks for user expectations
- **Resource Usage**: Clarify differences (browser overhead vs API efficiency)
- **Pattern**: Clear visual separation between platform-specific features

## Multi-Language Validation Patterns (NEW)

**Validation Framework**: Article XIII enforcement
**Detection**: Auto-scan for `requirements.txt`, `Cargo.toml`, `pnpm-lock.yaml`, etc.
**Enforcement**: HALT on errors → @mcp:context7 → Fix → Re-validate → Continue

**Python Validation**:
- Primary: `basedpyright .` (stricter than mypy)
- Zero tolerance: Type errors, unused variables, import failures
- Auto-fix: Add type hints, fix imports, resolve modules

**Validation Checkpoints**:
- Pre-implementation: Detect language → Run validation
- During implementation: Validate after each file change  
- Post-implementation: Full validation before memory-bank updates
- Pre-commit: Final validation gate

**Success Pattern**: Error → mistakes.md → @mcp:context7 → Fix → Clean → Store pattern

**Last Updated**: 2025-10-01T18:03:00+05:30

## EMD (Elegant Modular Design) Standard

**Code Files**: ≤10,000 characters (updated from 80 lines on 2025-10-01)
**Memory Bank Files**: ≤100 lines
**Roadmap**: ≤12,000 characters

**Current Compliance**:
- All src/ files: ✅ Compliant (0 files over 10K)
- streamlit_app.py: ⚠️ Minor violation (10,897 chars, 8.9% over)
- All memory-bank: ✅ Under 100 lines

## Architecture Pattern: Minimalist Structure (2025-09-30)
**Problem**: 25+ dirs with 4-level nesting  
**Solution**: Flatten to 8 dirs, 2-level max  
**Target**: src/{models.py, db/, scraper/, analysis/}  
**Benefits**: 70% reduction, EMD compliant (≤80 lines), easier navigation

## Date Parsing Pattern
**Pattern**: Regex extract number → Map unit (hour/day/week/month) → timedelta → datetime  
**Location**: `utils/date_parser.py` (73 lines)  
**Fallback**: Return `datetime.now()` for unparseable strings

## Database Pattern: ConnectionManager + JobRetrieval
**Pattern**: `ConnectionManager(db_path)` → `with get_connection() as conn:` → `JobRetrieval().method(conn)`  
**Key**: JobRetrieval() takes NO constructor params, pass connection to methods

## 30-Hour Continuous Operation Pattern
**Loop**: Read context → Execute task → Update 9 files → Auto-recover errors → Checkpoint (every 10) → Continue  
**Key**: 0-98% autonomy = EXECUTE IMMEDIATELY, NEVER STOP until scratchpad empty  
**Recovery**: Error → @mcp:context7 → Fix → Continue (no human escalation)

## Real-Time Research Pattern (2024 - 8 MCPs)
**Before Implementation**: @mcp:context7 + @mcp:fetch + @mcp:time for latest timestamped docs
**On Error**: Instant @mcp:context7 activation for official documentation
**Temporal Awareness**: @mcp:time for deadlines, schedules, time-sensitive operations
**Knowledge Storage**: @mcp:byterover-mcp stores successful patterns with timestamps
**Continuous Learning**: Every task enriches knowledge base for future autonomy

## Context Engineering Pattern (Article III)
**Attention Budget**: Load files in priority order to prevent context rot
**Load Order**: 1) scratchpad+roadmap (CRITICAL) 2) activeContext+mistakes+tech (HIGH) 3) progress+systemPatterns (SUPPORT) 4) product+brief (REFERENCE)
**Cleanup Trigger**: Auto-archive when >90 lines

## Compliance Pattern
**Pre-Implementation**: Read 8 memory-bank files + roadmap + retrieve knowledge + validate EMD/laws  
**Post-Implementation**: Update all 9 files + store knowledge + document lessons + verify ≥80% adherence  
**Enforcement**: 1st=WARNING, 2nd=ROLLBACK, 3rd=ESCALATE

## Skill Validation Pattern (Triple-Layer - 2025-10-01)
**Guarantee**: Zero fake skills - all skills validated against actual JD text
**Layer 1 (NLP)**: SkillNER extracts from job description (`dynamic_skill_extractor.py:32-54`)
**Layer 2 (Text Verify)**: Regex `\bskill\b` confirms existence (`skill_validator.py:28-36`)
**Layer 3 (Filter)**: Removes boilerplate ("work", "team", "experience") (`skill_validator.py:48-61`)
**Result**: Only skills physically present in JD reach database
**Code**: `validate_skill_in_text()` returns `False` if skill NOT in original text

## Conditional UI Rendering Pattern (2025-10-02T12:08)
**Problem**: Different platforms have different capabilities (LinkedIn=multi-country, Naukri=India-only)  
**Solution**: Conditional form rendering based on platform selection  
**Implementation**: `if platform == "LinkedIn":` show country multiselect, else hide  
**Validation Logic**: `platform == "Naukri" or selected_countries` allows Naukri without countries  
**Error Messages**: Platform-specific ("Please select at least one country for LinkedIn scraping")  
**Pattern**: Always match UI form fields to actual scraper method signatures  
**Example**: Naukri `scrape_jobs(keyword, num_jobs)` vs LinkedIn `scrape_jobs(job_role, target_count, countries)`

## Dead Code Detection Pattern (2025-10-02T12:08)
**Detection**: File exists but no imports/usage found via grep search  
**Example**: `naukri/config/countries.py` imported in `__init__.py` but never used in scrapers  
**Validation**: Search codebase for variable/constant references  
**Cleanup**: Delete file + remove imports + run validation suite  
**Prevention**: Regular codebase scans for unused imports/files  
**Rule**: If mirroring structure (LinkedIn→Naukri), validate actual usage not just existence

## Naukri API Pattern (2025-10-01T20:26)
**Architecture**: Pure API-based (no Selenium), async pagination, EMD compliant  
**Search API**: `GET /jobapi/v3/search?keyword={role}&start={page}` → Returns list with 20 jobs  
**Job Detail API**: `GET /jobapi/v4/job/{jobId}?microsite=y&brandedConsultantJd=true` → Full job object  
**Response Path**: `data.jobDetails[]` → Extract `jobId`, `title`, `company`, `location`, `skills`, `jd`  
**Skills Extraction**: `jobDetails.keySkills.other[]` array with `{label, clickable}` objects  
**HTML Description**: `jobDetails.description` contains HTML tags - needs text extraction  
**Pagination**: Pages 1-50, async with 0.5s delay between requests  
**Implementation**: `NaukriAPIFetcher` (requests) → `NaukriJobParser` → `JobModel` (Pydantic v2)  
**No Country Support**: Naukri is India-only, no location filtering in scraper signature

## Naukri Pagination Pattern (2025-10-02T12:48)
**Discovery**: Naukri uses server-side pagination, not infinite scroll
**URL Structure**:
- Page 1: `/{keyword-slug}-jobs?k={keyword+param}`
- Page 2+: `/{keyword-slug}-jobs-{page_num}?k={keyword+param}`
**Example**: "AI Engineer" → `/ai-engineer-jobs?k=ai+engineer` (page 1)
**Jobs Per Page**: 20 (constant)
**Total Available**: 38,945 jobs for AI Engineer (verified on site)
**Dynamic Calculation**: `total_pages = (target_count // 20) + 1`
**Implementation**: Loop through pages, extract all job cards per page
**Anti-Pattern**: Scroll-based approach only loaded ~100 jobs (5 scrolls hardcoded)
**Lesson**: Always verify site behavior (pagination vs scroll) before implementation

## Scraper Architecture
**Base**: BaseJobScraper (abstract), AntiDetectionDriverFactory (uc.ChromeOptions), retry logic  
**LinkedIn**: Selenium-based (59 lines), infinite scroll, 1000+ jobs tested  
**Naukri**: API-based (70 lines), REST endpoints, type-safe parsing  
**UI**: Streamlit (251 lines - EMD violation, functional), 2 platform selector  
**Flow**: UI → {LinkedIn|Naukri} → JobModel list → SQLite (BatchOperations) → Skill validation → Analysis

## Core Patterns
**EMD**: ≤80 lines/file, deep nesting, single responsibility  
**Anti-Detection**: `uc.ChromeOptions()` not `selenium.Options`  
**Parallel**: ThreadPoolExecutor (4 workers) for I/O concurrency  
**Skill Stats**: (jobs_with_skill / total_jobs) * 100, lowercase normalization  
**Workflow**: Read scratchpad+mistakes → Implement → Update 9 files → Continue

## Working Patterns
- Pydantic v2 thread-safe models
- Context manager for WebDriver lifecycle
- Python 3.9+ type hints (`list[T]`, `str | None`)
- Exponential backoff retry logic
- SQLite WAL mode for concurrent writes
