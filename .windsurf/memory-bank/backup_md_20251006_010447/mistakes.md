# Mistakes & Lessons - Job Scrapper

## CSV Export - Visualization Data Mismatch (2025-10-02T13:08)

**Issue**: CSV export data didn't match what visualizations showed - different skill counts and processing

**Root Cause**: 
- Visualizations used `normalized_jobs` (processed by `normalize_jobs_skills()`)
- CSV export used raw `db_jobs_dicts` (unprocessed database data)
- Two different data sources = inconsistent results

**Fix Applied**:
1. Updated `analytics_dashboard.py` to pass `normalized_jobs` to CSV export
2. Updated `extract_summary_metrics()` to parse skills from TEXT column
3. Now both visualization and CSV use same data pipeline

**Pattern**: Always use the same data source for visualization and export to ensure consistency

**Files Updated**: `analytics_dashboard.py`, `analytics_helpers.py`

## CSV Export - Skills Data Mismatch (2025-10-02T13:03)

**Issue**: CSV export missing skills count and skills list - columns showing 0 and empty

**Root Cause**: Database stores `skills` as comma-separated TEXT, but CSV export expected `skills_list` JSON array

**Investigation**: 
- Database schema: `skills TEXT` column stores "python, machine learning, tensorflow"
- Export function looked for `skills_list` array (doesn't exist in DB)
- Result: Skills Count = 0, Skills = empty string

**Fix Applied**:
- Updated `prepare_export_data()` to parse both TEXT and array formats
- Added string split logic: `skills.split(',')` for TEXT columns
- Added Experience and Platform columns for completeness
- Proper job_role extraction ensured

**Pattern**: Always check actual database schema before assuming data format

**Files Updated**: `analytics_helpers.py`

## Streamlit Download Button - Missing Key (2025-10-02T13:00)

**Error**: `MediaFileStorageError: Bad filename ... (No media file with id ...)`

**Root Cause**: `st.download_button()` without unique `key` parameter loses file reference on rerun

**Fix Applied**:
- Added unique keys to all 3 download buttons
- `skill_leaderboard.py`: `key="download_skill_leaderboard"`
- `analytics_dashboard.py`: `key="download_skills_analysis"`, `key="download_all_jobs"`

**Pattern**: ALWAYS add `key` parameter to Streamlit widgets that maintain state

**Files Updated**: `skill_leaderboard.py`, `analytics_dashboard.py`

## Misleading UX - Duplicates vs Availability (2025-10-02T12:54)

**UX Issue**: User requested 355 jobs, scraped 260, UI didn't clarify only 260 available

**Root Cause**: Progress tracker always showed success message regardless of availability

**User Confusion**: "Does 100 jobs were duplicate?" - No, only 260 exist on platform

**Fix Applied**:
- Added early exit when page returns 0 jobs (stop pagination)
- Browser scraper logs: `"only {X} available on Naukri"`
- UI shows warning: `"⚠️ Only {scraped}/{target} jobs available on platform"`
- Changed from green success to yellow warning when `scraped < target`

**UX Pattern**: Always distinguish between:
- **Availability limit**: Platform has fewer jobs than requested
- **Duplicates**: Jobs already in database
- **Success**: Target met exactly

**Files Updated**: `browser_scraper.py`, `progress_tracker.py`

## Hardcoded Scroll Limit (2025-10-02T12:45)

**Error**: Browser scraper only collected 100 jobs when 355 requested

**Root Cause**: Hardcoded `range(5)` limited scrolling to 5 times (~100 jobs max)

**Fix Applied**:
- Calculate dynamic scrolls: `max_scrolls = (target_count // 20) + 5`
- For 355 jobs: (355 ÷ 20) + 5 = 22 scrolls
- Added buffer to ensure target met

**Lesson**: NEVER hardcode iteration limits when target is user-provided. Always calculate dynamically from data.

**Pattern**: Use DDP (Data-Driven Programming) - derive ALL parameters from actual requirements.

## HTTP 406 - reCAPTCHA Required (2025-10-02T12:38)

**Error**: `{"message":"recaptcha required","statusCode":406}`

**Root Cause**: 
Naukri's Akamai Bot Manager detects API requests as bot traffic even with correct headers. Requires reCAPTCHA verification.

**Why API Approach Failed**:
1. Missing browser session cookies from real login
2. No reCAPTCHA tokens (cannot bypass programmatically)
3. Advanced fingerprinting detects automated requests
4. Headers alone insufficient for anti-bot bypass

**Solution**: Use browser-based scraper (src/scraper/naukri/browser_scraper.py) with Selenium + undetected-chromedriver instead of direct API calls.

**Lesson**: For sites with reCAPTCHA, browser automation is required. Direct API calls will be blocked.

**Pattern**: Always test API endpoints before building scraper. If reCAPTCHA detected, switch to browser automation immediately.

## Recent Errors & Patterns (Last 20)

### 12. UI-Implementation Mismatch (2025-10-02)
**Problem**: UI showed country selection for both platforms, but Naukri scraper doesn't support countries parameter  
**Root Cause**: Copied LinkedIn UI pattern without validating against actual Naukri scraper signature  
**Solution**: Conditional rendering `if platform == "LinkedIn"` to show/hide country selector based on platform capabilities  
**Implementation**: Updated validation logic to `platform == "Naukri" or selected_countries`  
**Prevention**: Always verify UI form fields match actual method signatures before implementing

### 13. Dead Code - Unused Config File (2025-10-02)
**Problem**: `naukri/config/countries.py` existed but was never used anywhere in codebase  
**Root Cause**: Mirrored LinkedIn structure without validating actual usage in Naukri scraper  
**Lesson**: Don't copy-paste structure between platforms without verifying necessity  
**Solution**: Grep search revealed zero usage → Delete file + clean imports → Validate with basedpyright  
**Prevention**: Regular dead code scans, validate all imports are actually used, check method signatures

### 11. WebDriver Creation Failure (2025-10-01)
**Problem**: `driver_factory.create_driver()` returned `None`, causing `RuntimeError: Failed to create shared browser`  
**Root Cause**: Silent exception handling without detailed logging, no retry mechanism for transient failures  
**Solution**: Added exponential backoff retry (3 attempts: 1s, 2s, 4s), comprehensive error logging with specific diagnostics  
**Implementation**: `version_main=None` parameter for automatic Chrome version detection, detailed error messages with installation checks  
**Prevention**: Always implement retry logic for external dependencies (Chrome, chromedriver), log full error details for debugging

### 1. ARCHITECTURE: Scattered File Structure (2025-09-30)
**Problem**: 25+ directories with 4-level nesting made navigation difficult  
**Lesson**: EMD means ≤80 lines per FILE, not deep folder nesting  
**Solution**: Flatten to 8 directories, 2-level max depth (70% reduction)  
**Prevention**: Always favor shallow structure over deep nesting

### 2. Pydantic V2 Field Aliases (2025-09-30)
**Problem**: Basepyright doesn't understand `populate_by_name=True`  
**Lesson**: Use ALIASES (Job_Role, Company) not field names (job_role, company) for type safety  
**Solution**: Always use aliases in JobModel instantiations  
**Pattern**: `JobModel(Job_Role="Engineer")` ✅ vs `JobModel(job_role="Engineer")` ⚠️

### 3. LinkedIn Extraction Failure (2025-01-XX)
**Problem**: `extract_job_from_url` returned 0 jobs  
**Lesson**: CSS selectors break when LinkedIn updates page structure  
**Solution**: Update selectors, add wait strategies, implement fallback selectors  
**Prevention**: Use multiple selector strategies with fallbacks

### 4. Python Type Hints & Imports (2025-09-30)
**Problem**: Using deprecated `List`, `Dict`, `Optional` from typing module  
**Lesson**: Python 3.9+ supports built-in generics (`list`, `dict`), Python 3.10+ uses `| None`  
**Solution**: Use modern syntax: `list[JobModel]` not `List[JobModel]`  
**Pattern**: `def func() -> str | None:` ✅ vs `def func() -> Optional[str]:` ⚠️

### 5. LinkedIn Import Error (2025-09-30)
**Problem**: Import path `models.job` failed in LinkedIn scraper  
**Lesson**: Relative imports required for nested modules  
**Solution**: Use `...models.job` for proper relative import  
**Prevention**: Always verify import paths in nested package structures

### 6. EMD Violations (2025-09-30)
**Problem**: main.py (106 lines) exceeds 80-line limit  
**Lesson**: Decompose large files into logical components  
**Solution**: Split into coordinator.py, worker_pool.py, results_manager.py  
**Prevention**: Monitor line counts during development

## ✅ Working Patterns
- Pydantic v2 thread-safe validation
- ThreadPoolExecutor for I/O-bound tasks
- EMD compliance (≤80 lines per file)
- undetected-chromedriver + fake-useragent
- Automated skill normalization (lowercase)
  - **Lesson**: Always validate line count before implementation

### 7. Threading & Concurrency (2025-09-30)
**Pattern**: ThreadPoolExecutor with 4 workers for I/O concurrency  
**Lesson**: Pydantic v2 models are thread-safe, SQLite needs WAL mode for concurrent writes  
**Prevention**: Always enable WAL mode for concurrent database operations

### 8. Component Reuse (2025-09-30)
**Problem**: Creating duplicate implementations instead of reusing base classes  
**Lesson**: Always use centralized components from `/scrapers/base/`, `/models/job.py`  
**Solution**: Follow memory-bank guidance before implementing  
**Prevention**: Check existing implementations first

### 9. Anti-Detection & Selectors (2025-09-30)
**Problem**: Using `selenium.webdriver.chrome.options.Options` breaks undetected-chromedriver  
**Lesson**: Must use `uc.ChromeOptions()` directly for anti-bot features  
**Solution**: Replace Options with uc.ChromeOptions in anti_detection.py  
**Prevention**: Always verify proper undetected-chromedriver usage

### 10. LinkedIn Selector Reliability (2025-09-30)
**Problem**: Single '.job-search-card' selector has 30% failure rate  
**Lesson**: Platform selectors break frequently with UI updates  
**Solution**: Implement fallback selector array: ['.job-search-card', 'div[data-job-id]', 'li[data-occludable-job-id]']  
**Prevention**: Always use multiple selector strategies





