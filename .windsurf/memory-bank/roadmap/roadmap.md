# Job Scrapper Project Roadmap - Architecture Restructuring Phase

**Architecture**: Minimalist structure design completed (2025-09-30)
**Current Status**: 25+ directories with 4-level nesting → Target: 8 directories with 2-level max
**Priority**: Phase 1 - Flatten database/ → src/db/ (70% directory reduction)
**Next**: Complete 3-phase migration, then resume platform expansion

## 🎯 Project Goal
Build a tool to scrape jobs for a given role (e.g., "AI Engineer") and generate skill analysis reports with LLM-powered recommendations.

## What We're Building (Aligned to Requirements)
1. **Scrape Jobs**: Collect job data from LinkedIn for specific job role
2. **Store Data**: Save to database with schema: Job_Id, Job_Role, Company, Experience, Skills, jd
3. **Skill Analysis**: Generate report showing skills with % of jobs mentioning them (e.g., RAG 89%, Langchain 62%, Crew AI 41%)
4. **LLM Recommendations**: Use LLM to generate job seeker recommendations based on skill gap analysis

## Success Targets - CORE FUNCTIONALITY
- **Job Collection**: Scrape jobs for specific role (e.g., "AI Engineer") from all platforms
- **Database Storage**: Store with exact schema - Job_Id, Job_Role, Company, Experience, Skills, jd
- **Skill Analysis**: Calculate percentage of jobs mentioning each skill (skill_count/total_jobs * 100)
- **Report Generation**: Output skill percentages (e.g., RAG 89%, Langchain 62%, Crew AI 41%)
- **LLM Recommendations**: Generate actionable advice for job seekers based on skill gaps
- **Parallel Efficiency**: 4x faster execution with concurrent scraping

## 📋 Current Implementation Status & Next Steps

### ✅ COMPLETED: Foundation & Infrastructure (Phase 1-2)
- [x] **JobModel (Pydantic v2)**: Exact schema - Job_Id, Job_Role, Company, Experience, Skills, jd
- [x] **Database Layer (8 modules)**: Thread-safe SQLite with ConnectionManager, JobRetrieval, BatchOperations
  - `database/connection/` - Database connection management
  - `database/core/` - Core operations (6 modules)
  - `database/operations/` - Job storage operations
  - `database/schema/` - Schema management
- [x] **Python 3.13.3 + basepyright**: Modern type hints (list[T], dict[K, V]), strict type checking
- [x] **EMD Architecture**: Deep nested folder structure, most files ≤80 lines

### ✅ COMPLETED: Platform Scraper (Phase 2)
- [x] **LinkedIn Scraper**: ✅ PRODUCTION READY
  - Infinite scroll pagination working (scroll_handler.py)
  - API job fetcher (api_job_fetcher.py - 71 lines)
  - Job ID extractor (job_id_extractor.py - 74 lines)
  - Duplicate tracking with processed_ids set
  - GUI mode enabled for debugging
  - Tested with 1000+ job scraping
- [x] **Base Infrastructure**: AntiDetectionDriverFactory, driver pool, retry logic, role checker
- [x] **Results Management**: Single platform operational (LinkedIn)

### ✅ COMPLETED: Skill Extraction & NLP (Phase 3)
- [x] **Unified Skill Patterns (190+)**: Single list combining hard + soft skills
  - 150 technical skills (languages, frameworks, cloud, DevOps, ML/AI, databases)
  - 40 soft skills (communication, leadership, problem-solving, work ethic)
- [x] **Dynamic NLP Extraction (5 strategies)**:
  1. Context keyword extraction ("skills:", "experience with:")
  2. Comma-separated list parsing
  3. Bullet point detection (•, -, *, numbers)
  4. N-gram analysis (bi-grams, tri-grams)
  5. Full-text pattern matching
- [x] **Modular Design**: `utils/analysis/nlp/skill_extractor.py` + `soft_skills_patterns.py`
- [x] **Posted Date Calculation (2025-09-30)**: Date parser utility for temporal tracking
  - Created `utils/date_parser.py` (73 lines - EMD compliant)
  - Regex-based extraction from relative time strings
  - Supports hours, days, weeks, months, years, "just now"
  - Integrated with LinkedIn API job fetcher
  - All scraped jobs now have accurate `posted_date` timestamps

### ✅ COMPLETED: Analysis & Reporting Pipeline (Phase 3-4)
- [x] **Skill Analysis Engine**: SkillAnalysisIntegration with percentage calculations
- [x] **Role Analysis System**: Role-specific job filtering and skill aggregation
  - `utils/analysis/role_analyzer.py` - Main orchestrator
  - `utils/analysis/role/` - Job filter, skill calculator (9 modules)
- [x] **Report Generation**: End-to-end pipeline (database → analysis → formatting)
  - `utils/analysis/report_generator.py` - Report orchestration
  - `utils/analysis/report_formatter.py` - Output formatting
  - `utils/analysis/report_integration.py` - Pipeline integration
- [x] **Skill Calculator**: Statistical formula implementation (skill_count/total_jobs * 100)

### 🔄 IN PROGRESS: User Interface (Phase 4)
- [x] **Streamlit Web App**: ⚠️ FUNCTIONAL but EMD VIOLATION (176 lines)
  - Single-platform form working (LinkedIn only)
  - Progress tracking with real-time metrics
  - 3 tabs: Job Listings, Skill Leaderboard, Analytics
  - **CRITICAL**: Needs splitting into modules:
    - `ui/components/` for reusable UI elements
    - `ui/forms/scraper_form.py` (≤80 lines)
    - `ui/tabs/job_listings.py` (≤80 lines)
    - `ui/tabs/skill_leaderboard.py` (≤80 lines)
    - `ui/tabs/analytics.py` (≤80 lines)
- [x] **Skill Leaderboard Visualization**: ✅ COMPLETE
  - Top 20 skills with percentage ranking
  - Bar chart visualization
  - CSV export functionality
  - Interactive dataframe display
- [x] **Analytics Dashboard**: ✅ COMPLETE
  - Total jobs, avg skills/job metrics
  - Top companies hiring
  - Role distribution visualization
- [x] **Skill Percentage Calculation**: Statistical formula implemented

### ⏳ PENDING: Production Testing & Quality Assurance (Phase 5)
- [ ] **Production Scale Testing**: Test with 500+ jobs per platform
  - Verify data quality across all 4 platforms
  - Validate skill extraction accuracy (target: 95%)
  - Test database performance under load
  - Monitor scraping success rates
- [ ] **EMD Compliance Fixes**: Resolve files exceeding 80-line limit
- [ ] **Basepyright Lints**: Clean up remaining type warnings
  - Fix `Any` type usage in database operations
  - Add proper type annotations for unknown types
  - Resolve unused variable warnings

### 🚀 PENDING: LLM Integration & Recommendations (Phase 5)
- [ ] **LLM Connection**: Integrate OpenAI/Anthropic API for recommendations
- [ ] **Skill Gap Analysis**: Compare scraped skills vs job seeker profile
- [ ] **Personalized Recommendations**: Generate actionable career advice
  - Identify high-demand skills from analysis
  - Suggest learning paths based on skill gaps
  - Prioritize skills by job market percentage
  - Create role-specific career roadmaps

### 🎯 IMMEDIATE PRIORITIES (Architecture Restructuring)
1. **🏗️ PHASE 1: Flatten database/** (CRITICAL - 45 min)
   - Create src/db/ directory structure
   - Consolidate database/connection/ → src/db/connection.py
   - Merge database/core/*.py (7 files) → src/db/operations.py + manager.py
   - Move database/schema/ → src/db/schema.py
   - Update all database imports across codebase
   - Test database operations after migration

2. **🏗️ PHASE 2: Flatten utils/** (HIGH - 60 min)
   - Create src/analysis/ directory
   - Consolidate utils/analysis/nlp/*.py → src/analysis/skills.py
   - Merge utils/analysis/role/*.py → src/analysis/roles.py
   - Combine *_analyzer.py files → src/analysis/analyzer.py
   - Move date_parser.py, statistics.py → src/analysis/utils.py
   - Update all analysis imports

3. **🏗️ PHASE 3: Flatten scrapers/** (HIGH - 45 min)
   - Create src/scraper/ directory structure
   - Consolidate scrapers/base/ utilities → src/scraper/base.py
   - Move dynamic_skill_extractor.py → src/scraper/skills.py
   - Organize linkedin/ folder under src/scraper/linkedin/
   - Update all scraper imports

4. **📦 Consolidate models/** (MEDIUM - 15 min)
   - Move models/job.py → src/models.py
   - Update all JobModel imports

5. **🧪 Test Restructured Architecture** (30 min)
   - Run full test suite after migration
   - Verify all imports working correctly
   - Test LinkedIn scraper with sample jobs

## 🔗 Tech Stack (Aligned to Requirements)
- **Python 3.13.3+**: Core language for web scraping
- **Selenium + undetected-chromedriver**: Browser automation with anti-detection
- **Pydantic v2**: Data modeling with exact schema (Job_Id, Job_Role, Company, Experience, Skills, jd)
- **SQLite**: Database storage for job data
- **concurrent.futures**: Parallel execution across platforms
- **LLM Integration**: For generating job seeker recommendations
- **Skill Analysis**: Calculate skill mention percentages
- **Report Generation**: Output skill statistics in required format

## 📂 Actual EMD-Compliant Architecture (Deep Nested Structure)
```
job_scrapper/
├── models/
│   └── job.py                           # Pydantic v2 JobModel
├── database/
│   ├── connection/
│   │   └── db_connection.py             # Database connection setup
│   ├── core/
│   │   ├── batch_operations.py          # Batch insert operations
│   │   ├── connection_manager.py        # Thread-safe connection pool
│   │   ├── data_converter.py            # JobModel to SQLite converter
│   │   ├── job_retrieval.py             # Query operations
│   │   └── sqlite_manager.py            # SQLite manager
│   ├── operations/
│   │   └── job_storage.py               # Job storage operations
│   └── schema/
│       └── schema_manager.py            # Schema creation/migration
├── scrapers/
│   ├── base/
│   │   ├── anti_detection.py            # Undetected chromedriver setup
│   │   ├── base_scraper.py              # Abstract base class
│   │   ├── driver_pool.py               # WebDriver pool management
│   │   ├── retry_handler.py             # Retry logic with backoff
│   │   └── role_checker.py              # Job role validation
│   ├── linkedin/
│   │   ├── scraper.py                   # LinkedIn scraper logic
│   │   ├── extractor.py                 # Job card data extraction
│   │   └── extractors/                  # Specialized extractors
│   └── results/
│       ├── manager.py                   # Results aggregation
│       ├── export/                      # Export modules
│       ├── processing/                  # Data processing
│       ├── reporting/                   # Report generation
│       └── statistics/                  # Statistical calculations
├── utils/
│   ├── analysis/
│   │   ├── nlp/
│   │   │   ├── skill_extractor.py       # 190+ skill patterns (unified)
│   │   │   └── soft_skills_patterns.py  # 40 soft skill patterns
│   │   ├── role/
│   │   │   ├── job_filter.py            # Role-based filtering
│   │   │   └── skill_calculator.py      # Percentage calculations
│   │   ├── role_analyzer.py             # Role analysis orchestrator
│   │   ├── skill_analyzer.py            # Skill analysis engine
│   │   ├── skill_calculator.py          # Statistical calculations
│   │   ├── skill_analysis_integration.py # Analysis pipeline
│   │   ├── report_generator.py          # Report orchestration
│   │   ├── report_formatter.py          # Output formatting
│   │   └── report_integration.py        # End-to-end pipeline
│   ├── skill_statistics.py              # Skill statistics utilities
│   └── statistics.py                    # General statistics
├── tests/
│   └── integration/
│       └── test_main_runner.py          # Integration tests
├── streamlit_app.py                     # Streamlit web UI
├── demo_report_generation.py            # Demo pipeline
└── jobs.db                              # SQLite database
```

**Architecture Principles:**
- **EMD Compliant**: Most files ≤80 lines
- **Deep Nesting**: 3-4 level folder hierarchy
- **Separation of Concerns**: Clear module boundaries
- **Platform-Specific**: Each scraper in own folder
- **Centralized Utils**: Shared analysis components

## 🎯 Future Enhancement
- **Phase 2**: Add LLM integration for job seeker recommendations
- Keep current code simple and focused
- All files under 80 lines (EMD principle)

---

**Status**: Simple, focused roadmap for basic job scraping and statistical analysis tool.
