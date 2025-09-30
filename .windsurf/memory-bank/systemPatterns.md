# System Patterns - Job Scrapper

## Date Parsing Pattern (Relative Time to DateTime)

### Relative Date Calculation Pattern
```python
from datetime import datetime, timedelta
import re

def parse_relative_date(date_text: str) -> datetime:
    """Parse relative date strings to datetime objects"""
    # Extract number: "2 days ago" -> 2
    number_match = re.search(r'(\d+)', date_text)
    number = int(number_match.group(1)) if number_match else 1
    
    # Map time units to timedelta
    now = datetime.now()
    if 'hour' in date_text or 'hr' in date_text:
        return now - timedelta(hours=number)
    elif 'day' in date_text:
        return now - timedelta(days=number)
    elif 'week' in date_text:
        return now - timedelta(weeks=number)
    elif 'month' in date_text:
        return now - timedelta(days=number * 30)
    return now
```

### Key Lessons
1. **Regex Extraction**: Use `re.search(r'(\d+)', text)` to extract numbers
2. **Unit Mapping**: Map keywords (hour, day, week, month) to timedelta
3. **Fallback**: Always return `datetime.now()` for unparseable strings
4. **Integration**: Extract from HTML → Parse → Store in database
5. **EMD Compliance**: Keep utility file ≤80 lines

## Database Integration Pattern (ConnectionManager + JobRetrieval)

### Correct Pattern for Database Operations
```python
from database.core.connection_manager import ConnectionManager
from database.core.job_retrieval import JobRetrieval

class SkillAnalysisIntegration:
    def __init__(self, db_path: str = "jobs.db"):
        self.db_path: str = db_path
        self.conn_manager: ConnectionManager = ConnectionManager(db_path)
        # JobRetrieval takes NO parameters in constructor
        self.job_retrieval: JobRetrieval = JobRetrieval()
    
    def analyze_all_jobs(self) -> dict[str, float]:
        # Use context manager to get connection
        with self.conn_manager.get_connection() as conn:
            # Pass connection explicitly to retrieval methods
            jobs = self.job_retrieval.retrieve_all_jobs(conn)
            return self._calculate_percentages(jobs)
```

### Key Lessons
1. **JobRetrieval constructor**: Takes NO parameters (no db_path)
2. **ConnectionManager**: Manages connections via context manager
3. **Connection passing**: Always pass `conn` explicitly to retrieval methods
4. **Type annotations**: All class attributes must have explicit types
5. **Integration classes**: Use ConnectionManager + JobRetrieval pattern

## Constitutional Compliance Pattern (Article XIV)

### Mandatory Pre-Implementation Checklist
```python
# BEFORE ANY IMPLEMENTATION:
# 1. Read memory-bank (8 files)
files = ['activeContext.md', 'scratchpad.md', 'mistakes.md', 
         'progress.md', 'systemPatterns.md', 'techContext.md',
         'productContext.md', 'projectbrief.md']

# 2. Read strategic context
roadmap = 'roadmap/roadmap.md'

# 3. Retrieve knowledge via MCP
byterover-retrieve-knowledge()

# 4. Validate constitutional compliance
verify_emd_compliance()  # ≤80 lines
check_constitutional_laws()
```

### Mandatory Post-Implementation Checklist
```python
# AFTER EVERY IMPLEMENTATION:
# 1. Update ALL 8 memory-bank files + roadmap
update_all_memory_bank_files()

# 2. Store knowledge
byterover-store-knowledge()

# 3. Document lessons
update_mistakes_md()

# 4. Verify constitutional compliance (≥80%)
confirm_constitutional_adherence()
```

### Enforcement
- **1st Violation**: WARNING + mandatory correction
- **2nd Violation**: ROLLBACK + restart workflow  
- **3rd Violation**: ESCALATE to human (Level 100)

## 🏗️ SYSTEM ARCHITECTURE PATTERNS

### Scraper Architecture (Multi-Platform Web Scraping)
**Base Infrastructure** (`scrapers/base/`):
- `base_scraper.py` - Abstract base class with driver pool and context manager
- `anti_detection.py` - AntiDetectionDriverFactory using undetected-chromedriver
- `driver_pool.py` - WebDriver connection pooling for resource management
- `common_scraper.py` - Shared scraping utilities and helper functions
- `retry_handler.py` + `retry_logic.py` - Exponential backoff error handling
- `skill_extractor.py` + `dynamic_skill_extractor.py` - Skill parsing from job descriptions
- `role_checker.py` - Job role validation and normalization

**Platform Scrapers** (4 platforms implemented):
- **LinkedIn** (`scrapers/linkedin/`) - 59 lines, async Selenium, EMD compliant
- **Indeed** (`scrapers/indeed/`) - Scraper + extractor modules
- **Naukri** (`scrapers/naukri/`) - India-focused scraper with detailed docs
- **YCombinator** (`scrapers/ycombinator/`) - Startup-focused with company profiles

**Orchestration**:
- `streamlit_app.py` (82 lines) - Single-platform UI with form input and database storage
- `test_single_platform.py` - Test script for single platform scraping
- Removed: `main_wrapper.py` (multi-platform batch orchestration)
- Removed: `test_multi_platform_scraper.py` (concurrent platform testing)

### EMD-Compliant Module Structure
- **Maximum 80 lines per file** - strict enforcement (results_manager.py violates at 97)
- **Deep nested folders** - scrapers organized by platform and functionality
- **Single responsibility** - each file handles one specific concern

### Single Platform Flow
```
Streamlit UI → Platform Selection → Single Scraper → Jobs List → Database → Analysis
     ↓              ↓                    ↓                ↓           ↓
  Job Role     LinkedIn/Indeed      100-500 jobs    BatchOperations  Reports
               Naukri/YCombinator                      SQLite
```

### Core Scraping Patterns
**Base Scraper Interface**:
- All platform scrapers inherit from `BaseJobScraper` in `scrapers/base/base_scraper.py`
- Abstract `scrape_jobs(job_role, target_count) -> list[JobModel]` method
- Context manager pattern: `with LinkedInScraper():` for WebDriver lifecycle
- Built-in rate limiting (asyncio.sleep) and anti-detection (undetected-chromedriver)
- Python 3.9+ type hints: `list[JobModel]` instead of `List[JobModel]`

**Platform-Specific Implementation**:
- Each platform has `scraper.py` (orchestration) and `extractor.py` (data parsing)
- Scraper handles pagination, URL construction, rate limiting
- Extractor parses HTML elements into JobModel using CSS selectors/XPath
- All scrapers are async-compatible using `asyncio.run_in_executor` or native async

**Data Flow**:
1. `main_wrapper.py` → JobScrapperRunner.run_scraping(job_role, count)
2. Parallel async tasks for each platform (LinkedIn, Indeed, Naukri, YCombinator)
3. Each scraper returns `list[JobModel]` with normalized data
4. ResultsManager aggregates and calculates skill statistics
5. Export to database via `database/core/` modules

### EMD (Elegant Modular Design) Pattern 
**File Limit**: Maximum 80 lines per file (ENFORCED)
**Structure**: Deep nested folders for logical separation
```
scrapers/
├── coordinator/           # Parallel execution coordination (77 lines)
├── worker_pool/          # Thread pool management (77 lines)
├── platforms/            # Platform-specific scrapers (BLOCKED - lint errors)
├── base/                 # Base classes and utilities (79 lines)
└── application/          # Main application entry (80 lines)
```

### Workflow Loop Pattern (MANDATORY)
**BEFORE Implementation**: Read scratchpad.md + mistakes.md for context + errors
**DURING Implementation**: INSTANT mistakes.md update when errors/lints detected
**AFTER Every Task**: Update ALL 8 memory bank files + roadmap (9 FILES TOTAL)
**ERROR WORKFLOW**: Lint/Error → mistakes.md → scratchpad.md fix task

### Anti-Detection Pattern (Working)
```python
# : CORRECT: Undetected-chromedriver pattern
import undetected_chromedriver as uc

class AntiDetection:
    @staticmethod
    def create_driver():
        chrome_options = uc.ChromeOptions()  # NOT selenium Options!
        chrome_options.add_argument('--headless')
        return uc.Chrome(options=chrome_options)
```

### Parallel Coordination Pattern (Ready - Blocked)
```python
# : IMPLEMENTED: 77-line ParallelCoordinator
class ParallelCoordinator:
    def __init__(self, max_workers: int = 4):
        self.platforms = self._initialize_platforms()
        
    def execute_parallel_scraping(self, job_role: str) -> List[Job]:
        # BLOCKED: LinkedIn scraper compilation failures
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(platform.scrape_jobs, job_role) 
                      for platform in self.platforms]
            return self._aggregate_results(futures)
```

### Statistical Processing Pattern (Design Ready)
**Formula**: (jobs_with_skill / total_jobs) * 100
**Normalization**: Convert "SQL", "sql", "Sql" to lowercase consistency
**Deduplication**: Count each skill once per job

```python
# PENDING: Statistical calculation pattern
def calculate_skill_percentage(jobs: List[Job], skill: str) -> float:
    skill_lower = skill.lower()
    jobs_with_skill = sum(1 for job in jobs 
                         if skill_lower in [s.lower() for s in job.skills])
    return (jobs_with_skill / len(jobs)) * 100 if jobs else 0.0
```

### Data Validation Pattern (Working)
```python
# : IMPLEMENTED: Pydantic v2 model (79 lines)
class Job(BaseModel):
    job_id: str
    job_role: str
    company: str
    experience: str
    skills: List[str]
    jd: str
    platform: str
    
    class Config:
        validate_assignment = True
        use_enum_values = True
```

## Design Principles

### Processing Principles
- **Compilation First**: Fix lint errors before any development (CRITICAL)
- **Parallel Ready**: Concurrent execution design complete (BLOCKED)
- **Fail Safe**: Graceful handling patterns designed (PENDING)
- **Anti-Detection**: Working patterns implemented (READY)

### Validation Principles
- **Schema First**: Pydantic models implemented (COMPLETE)
- **Type Safe**: Strong typing required (BROKEN - lint errors)
- **EMD Compliance**: 80-line limit enforced (MAINTAINED)
- **Memory Loop**: 8-file + roadmap updates mandatory (ENFORCED)

### Error Recovery Principles
- **Instant Tracking**: mistakes.md updated immediately on errors (ENFORCED)
- **Fix Task Creation**: scratchpad.md updated with error fixes (ENFORCED)
- **Compilation Priority**: Fix lint errors before feature development (CRITICAL)
- **Workflow Validation**: All 9 files reflect true project state (MANDATORY)
