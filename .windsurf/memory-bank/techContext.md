# Technical Context - Job Scrapper

## ✅ CURRENT STATUS - SINGLE PLATFORM STREAMLIT UI
**ARCHITECTURE**: Single-platform scraping via Streamlit web interface
**UI**: http://localhost:8501 with job role input and platform selection
**CAPABILITY**: 10-500 jobs per session from one selected platform
**PRIORITY**: Test 500-job scraping, fix async race condition

## 🔧 TECHNICAL STACK

### Core Technologies
- **Python 3.13.3** - Latest Python with modern type hints (`list[T]` instead of `List[T]`)
- **Pydantic v2** - Data validation with JobModel schema (✅ WORKING)
- **SQLite with WAL mode** - Thread-safe database with concurrent access (✅ INTEGRATED)
- **ConnectionManager** - Database connection management with context managers (✅ WORKING)
- **JobRetrieval** - Database retrieval operations (✅ WORKING)
- **basepyright** - Strict static type checker (stricter than mypy) (✅ ACTIVE)
- **Constitutional Framework** - Article XIV mandatory compliance (✅ RATIFIED)

### Web Scraping Stack
- **Selenium 4.13+** - Browser automation for dynamic content
- **undetected-chromedriver 3.5+** - Anti-bot detection bypass
- **fake-useragent 1.5+** - User agent rotation for stealth
- **requests 2.31+** - HTTP client for simple scraping (Indeed)
- **beautifulsoup4 4.12+** - HTML parsing for static content (Indeed) (✅ WORKING)

### Data Processing Stack
- **datetime + timedelta** - Date/time calculations for relative date parsing
- **re (regex)** - Pattern matching for extracting numbers from text
- **Date Parser Utility** - Custom utils/date_parser.py (73 lines)

### Development Tools
- **pytest + pytest-asyncio** - Async testing framework
- **black** - Code formatting (PEP 8 compliance)
- **basepyright** - Strict static type checking (primary type checker)
- **mypy** - Alternative static type checker (basepyright preferred)
- **pylint** - Linting and code quality

### Scraper-Specific Configurations
- **GUI Mode** - Browser runs in visible mode for debugging
- **Single Browser** - One shared browser with multiple tabs (one per platform)
- **Streamlit UI** - Web form with job role, platform selection, job count slider
- **Auto Cleanup** - Browser cleanup after scraping session
- **Database Storage** - Automatic storage via BatchOperations

## Implemented Tech Stack (BLOCKED)
**Core Framework**: Python 3.13.3 with asyncio and threading support
**Data Validation**: Pydantic v2 for thread-safe models and serialization (✅ WORKING)
**Web Scraping**: Selenium WebDriver + undetected-chromedriver (✅ SETUP COMPLETE)
**HTTP Requests**: requests library with session management (✅ READY)
**Parallel Processing**: ThreadPoolExecutor design complete (❌ BLOCKED by LinkedIn errors)
**Database**: SQLite with WAL mode design ready (❌ NOT IMPLEMENTED)
**Data Processing**: Pandas for analysis (❌ PENDING - blocked by scraper issues)

## Critical Lint Errors Blocking System
```python
# BROKEN: LinkedIn scraper compilation failures
# Error IDs: 1039df20, c782fb50, b49dfb54, d33ae992, 5e0744e8, etc.

# Import Resolution Issues:
from models.job import Job  # FAILS - path not found

# Variable Definition Issues:
def scrape_jobs(self, job_role: str, count: int = 100):
    for page in range(0, min(count, 1000), 25):  # 'count' undefined

# Missing Override Decorators:
def scrape_jobs(...):  # Missing @override annotation

# Type Annotation Failures:
# All Job types resolve as 'Unknown' due to import failure
```

## Architecture Overview (PARTIAL IMPLEMENTATION)
```
Job_Scrapper/
├── models/
│   └── job.py            # ✅ Pydantic Job model (79 lines)
├── scrapers/
│   ├── coordinator/
│   │   └── parallel_coordinator.py  # ✅ ThreadPoolExecutor (77 lines)
│   ├── worker_pool/
│   │   ├── worker_pool_manager.py   # ✅ Pool management (77 lines)
│   │   └── worker_process.py        # ✅ Individual workers (80 lines)
│   ├── platforms/
│   │   ├── __init__.py    # ✅ Imports all 4 scrapers
│   │   ├── linkedin.py    # ❌ CRITICAL - 16+ lint errors
│   │   ├── indeed.py      # ❌ NOT IMPLEMENTED
│   │   ├── naukri.py      # ❌ NOT IMPLEMENTED
│   │   └── ycombinator.py # ❌ NOT IMPLEMENTED
│   ├── base/
│   │   ├── base_scraper.py          # ✅ Abstract base (79 lines)
│   │   └── anti_detection.py        # ✅ Chrome setup
│   └── application/
│       └── job_scrapper_app.py      # ✅ Main entry (80 lines)
├── database/
│   └── sqlite_manager.py  # ❌ NOT IMPLEMENTED
├── utils/
│   ├── statistics.py      # ❌ NOT IMPLEMENTED
│   └── skill_statistics.py # ❌ NOT IMPLEMENTED
└── main.py               # ❌ BLOCKED by LinkedIn errors
```

## Execution Flow (CURRENTLY BLOCKED)
1. **ParallelCoordinator** ✅ Ready (77 lines)
2. **ThreadPoolExecutor** ✅ Design complete
3. **Platform scrapers** ❌ BLOCKED - LinkedIn compilation failure
4. **Results aggregation** ❌ BLOCKED - cannot execute scrapers
5. **Statistical analysis** ❌ NOT IMPLEMENTED
6. **Export functionality** ❌ NOT IMPLEMENTED

## Key Implementation Details

### Thread-Safe Data Models (✅ WORKING)
```python
# ✅ Pydantic v2 model working (79 lines)
class Job(BaseModel):
    job_id: str = Field(..., description="Unique job identifier")
    job_role: str = Field(..., description="Job title/role")
    company: str = Field(..., description="Company name")
    experience: str = Field(..., description="Required experience")
    skills: List[str] = Field(default_factory=list)
    jd: str = Field(..., description="Job description")
    platform: str = Field(..., description="Source platform")
```

### Anti-Detection Strategy (✅ SETUP COMPLETE)
- **undetected-chromedriver**: ✅ Properly configured with uc.ChromeOptions()
- **fake-useragent**: ✅ Ready for realistic browser headers
- **Request delays**: ✅ Design ready (2-5 seconds configurable)
- **Session management**: ✅ Architecture designed

### Database Schema (DESIGN READY - NOT IMPLEMENTED)
```sql
-- PENDING: SQLite implementation needed
CREATE TABLE jobs (
    job_id TEXT PRIMARY KEY,
    Job_Role TEXT NOT NULL,
    Company TEXT NOT NULL, 
    Experience TEXT NOT NULL,
    Skills TEXT NOT NULL,  -- JSON array of skills
    jd TEXT NOT NULL
);
```

## IMMEDIATE TECHNICAL PRIORITIES

### Priority 1: BASEPYRIGHT TYPE COMPLIANCE (Python 3.13.3)
- **Add Class Attribute Type Annotations**: All class attributes must have explicit type hints
- **Remove Unused Imports**: Delete all unused imports (e.g., unused asyncio)
- **Add Generic Type Arguments**: Use `dict[str, Any]` instead of plain `dict`
- **Add Parameter Type Annotations**: All function parameters need type hints (including __exit__ methods)
- **Fix Unknown Types**: Ensure all types are properly imported and annotated
- **Context Manager Types**: Add proper type hints for exc_type, exc_val, exc_tb parameters

### Priority 2: Core Implementation (After Fixes)
- **Role-Based Scraping**: Accept job role parameters
- **Database Integration**: SQLite with WAL mode and threading
- **Skill Analysis**: Statistical engine with percentage calculations
- **Export Functions**: CSV/JSON output with proper formatting

## Performance Specifications (TARGETS)
- **Target Volume**: 500+ job postings (125+ per platform)
- **Execution Time**: <20 minutes (currently 0 - compilation fails)
- **Memory Usage**: <2GB RAM with 4 concurrent browsers
- **Success Rate**: >95% (currently 0% due to compilation failure)
- **Skill Accuracy**: >90% (blocked - cannot test)

## Current Technical Status
- **Compilation**: ❌ FAILED (16+ critical lint errors)
- **Architecture**: ✅ EMD-compliant design complete
- **Models**: ✅ Pydantic v2 working
- **Anti-Detection**: ✅ Setup complete
- **Parallel Design**: ✅ ThreadPoolExecutor ready
- **Database**: ❌ Not implemented
- **Statistics**: ❌ Not implemented
- **Export**: ❌ Not implemented
