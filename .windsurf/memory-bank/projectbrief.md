# Job Scrapper Project Brief

## Project Overview
**CURRENT STATUS**: Architecture restructuring phase - Minimalist design completed
**CURRENT FOCUS**: Flatten scattered file structure (25+ dirs → 8 dirs, 4-level → 2-level nesting)
**CONSTITUTIONAL FRAMEWORK**: Article XIV ratified (2025-09-30) - Mandatory AI compliance active
**NEXT PHASE**: Phase 1 implementation (database/ → src/db/), then complete scrapers

## Core Requirements
1. ✅ **Database Integration**: ConnectionManager + JobRetrieval pattern working
2. ✅ **Skill Analysis**: SkillAnalysisIntegration calculating percentages correctly
3. ✅ **Report Generation**: End-to-end pipeline operational (database → analysis → formatting)
4. ✅ **Constitutional Framework**: Article XIV ratified - AI governance active
5. **Next**: Production testing - Scrape 500+ jobs for given roles from 4 platforms
6. **Analyze Skills**: Calculate skill percentage using formula: (jobs_with_skill / total_jobs) * 100
   - Handle case variations (sql, SQL, Sql → normalize to lowercase)
   - Within each job: count each skill only once, even if mentioned multiple times
   - Example: Job mentions "SQL" 5 times → count as 1 occurrence for that job
5. **Generate Reports**: Export results in CSV/JSON format matching requirements ("RAG 89%, Langchain 62%")

## Target Platforms
- **LinkedIn Jobs** (Production ready)

## Success Metrics
- **Priority 1**: Fix compilation errors to enable basic execution
- Collect 500+ job postings minimum across all platforms
- Generate accurate skill percentage reports
- Export clean CSV/JSON data with proper formatting

## Tech Stack
- Python 3.11+ with proper type annotations
- Pydantic v2 (data validation and thread safety)
- Selenium + undetected-chromedriver (anti-detection)
- SQLite with WAL mode (concurrent operations)
- ThreadPoolExecutor (parallel scraping)
- Pandas (data processing and export)

## Completed Milestones (2025-09-30)
- ✅ **Constitutional Framework**: Article XIV ratified - Mandatory AI compliance
- ✅ **Database Layer**: ConnectionManager + JobRetrieval fully integrated
- ✅ **Skill Analysis**: SkillAnalysisIntegration operational with proper connection handling
- ✅ **Report Generation**: Complete pipeline working (demo successful)
- ✅ **Type Safety**: Basepyright compliant with Python 3.13.3

## Remaining Tasks
- 🎯 **PRIORITY: Architecture Restructuring** (2025-09-30)
  - Phase 1: Flatten database/ → src/db/ (10 files → 4-5 files)
  - Phase 2: Flatten utils/ → src/analysis/ (20+ files → 5-6 files)
  - Phase 3: Flatten scrapers/ → src/scraper/ (simplified structure)
  - Update all import statements across codebase
  - Test after each phase
- **Production Testing**: Test with 500+ real jobs across all platforms
- **Basepyright Lints**: Fix remaining type warnings
- **EMD Compliance**: Maintain ≤80 lines per file during restructuring

## Future LLM Integration
- Career recommendations based on skill analysis
- Trend analysis and market insights
- Personalized job seeker guidance
- requests, BeautifulSoup (web scraping)
- SQLite (data storage)

## Future Enhancement
- LLM integration for job seeker recommendations (Phase 2)
