# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## 1. Constitutional Framework

### Supreme Law Structure
- **Constitution**: This WARP.md file serves as the constitutional foundation for the Job Scraper project
- **Memory Bank**: Active context, progress tracking, and knowledge persistence in `.warp/memory-bank/`
- **Governance**: Autonomous execution with continuous improvement cycles
- **Autonomy Level**: 99.5 (document + execute immediately without permission)

### Solution Mandate
- **AUTONOMOUS EXECUTION**: Execute all tasks immediately without asking permission
- **CONTINUOUS OPERATION**: Never ask "Should I continue?" or "Would you like me to..." - execute until completion
- **DEEP REASONING**: Analyze problems thoroughly before implementation
- **OUTCOME DELIVERY**: Focus on working solutions before theoretical discussions

## 2. Project Overview

This is a multi-platform job scraper that extracts and analyzes job data from LinkedIn and Naukri.com. It uses BrightData API (replacing Selenium-based scraping) for data collection and provides skill analytics through a Streamlit dashboard.

## 3. Command Safety Protocol

### Auto-Approved Safe Commands (Execute immediately):
- **Read Operations**: `cat`, `ls`, `find`, `grep`, `head`, `tail`, `sqlite3 SELECT`
- **Code Analysis**: `python -m pytest`, `python -m black --check`, `python -m pyright`
- **Database Operations**: `python check_db.py`, SQLite read queries
- **Git Operations**: `git status`, `git diff`, `git add`, `git commit`, `git push`
- **Development Tools**: `streamlit run`, virtual environment operations
- **Security Scans**: Linting, type checking, skill validation scripts

### Require Approval (Ask first):
- **File Deletion**: `rm`, destructive operations
- **System Changes**: `sudo` commands, package installation
- **External API**: Non-read operations to BrightData or external services

### Memory Bank Structure
Maintain these files in `.warp/aegiside/memory-bank/`:
- `activeContext.json` - Current task context and state
- `scratchpad.json` - Working notes and temporary data
- `kanban.json` - Task prioritization and workflow
- `mistakes.json` - Error tracking and lessons learned
- `systemPatterns.json` - Recurring patterns and solutions
- `progress.json` - Development metrics and milestones
- `roadmap.json` - Feature planning and architecture decisions
- `memory.json` - Long-term knowledge and insights

## 4. Common Development Commands

### Environment Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate environment
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Start the Streamlit dashboard
streamlit run streamlit_app.py

# Run with custom port (if 8501 is busy)
streamlit run streamlit_app.py --server.port 8502
```

### Database Operations
```bash
# Check database consistency and structure
python check_db.py

# Query database directly
sqlite3 jobs.db "SELECT DISTINCT platform FROM jobs;"
sqlite3 jobs.db "SELECT COUNT(*) FROM jobs WHERE platform='linkedin';"
```

### Testing
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test categories
python -m pytest tests/test_skill_analysis.py -v
python -m pytest tests/test_database_integration.py -v

# Run single test
python -m pytest tests/test_linkedin_scraper.py::test_specific_function -v
```

### Code Quality
```bash
# Format code with Black
python -m black src/ tests/ streamlit_app.py

# Type checking (uses pyrightconfig.json)
python -m pyright src/

# Run validation scripts
python scripts/validate_skills.py
python scripts/bulk_skill_extraction.py
```

## 5. Architecture Overview

### High-Level Structure

The application follows a layered architecture with clear separation of concerns:

**Data Flow:**
1. **Scraper Layer** (`src/scraper/`) - Handles data collection from job platforms
2. **Skills Processing** (`src/scraper/brightdata/parsers/`) - Extracts and validates skills using JSON database
3. **Data Layer** (`src/db/`) - Manages SQLite database operations with schema management
4. **Analysis Layer** (`src/analysis/`) - Processes data for insights and statistics
5. **UI Layer** (`src/ui/`) - Streamlit components for dashboard interface

### Key Components

#### BrightData Integration (`src/scraper/brightdata/`)
- **Base Client** - Abstract client for API operations with polling mechanisms
- **LinkedIn Client** - Specialized client for LinkedIn job discovery via BrightData DCA
- **Skills Parser** - Regex-based skill extraction using `skills_reference_2025.json` (20,000+ technical skills)

#### Database Layer (`src/db/`)
- **Connection Management** - Thread-safe SQLite connection handling with context managers
- **Schema Management** - Automated table creation with performance indexes
- **Operations** - Job storage, duplicate detection, and bulk operations

#### Data Models (`src/models.py`)
- **JobModel** - Pydantic v2 model with field validation and alias support
- **Database Schema Compliance** - Maps to SQLite table structure with proper field aliases
- **Skills Processing** - Automatic parsing of comma-separated skills into lists

### Skill Validation System

The project uses a sophisticated skill validation system:

1. **JSON Database** (`skill_db_relax_20.json`) - Pre-compiled database of 20,000+ technical skills
2. **Pattern Matching** - Regex patterns with word boundaries for accurate skill detection
3. **Text Verification** - Skills must exist in original job description text
4. **Boilerplate Filtering** - Removes generic terms like "work", "team", "experience"

### Platform Architecture

#### LinkedIn (BrightData API-based)
```
User Input → LinkedInClient → BrightData API → Skills Parser → Database
```

#### Legacy Architecture (Archived)
The project maintains archived versions of browser-based scrapers for both LinkedIn and Naukri with complex multi-window parallel processing, but current implementation uses BrightData API for better reliability and compliance.

### Data Storage

**SQLite Schema:**
- Primary table: `jobs` with indexed columns for performance
- Key fields: `job_id` (primary key), `job_role`, `company`, `skills`, `jd`, `platform`
- Indexes: skills, platform, job_role, company, scraped_at

## 6. Development Guidelines

### Skills Database
- Skills are stored in `skills_reference_2025.json` with pattern-based matching
- Alternative database: `skill_db_relax_20.json` for relaxed matching rules
- Skills validation happens at extraction time, not storage time

### Database Consistency
- Platform names use lowercase format: `"linkedin"`, `"naukri"`
- Job IDs follow pattern: `platform_identifier` (LinkedIn) or hash (Naukri)
- Skills stored as comma-separated strings in database, parsed to lists in models

### Error Handling
- BrightData client includes automatic polling and task completion detection
- Database operations use context managers for proper connection handling
- Skills parser gracefully handles missing or malformed data

### Testing Strategy
- Unit tests for individual components in `tests/`
- Integration tests for database operations
- Skill validation tests with real job description samples
- LinkedIn scraper validation with API response testing

### Performance Considerations
- Skills parsing uses pre-compiled regex patterns loaded once at initialization
- Database uses indexes on commonly queried columns
- BrightData API eliminates browser automation overhead
- Async operations in data processing pipeline

### File Organization
- `archive/` contains legacy browser-based scraper implementations
- `src/scraper/brightdata/` contains current API-based implementation
- `scripts/` contains utility scripts for database maintenance
- Configuration files use separate modules under `config/` subdirectories

## 7. Environment Requirements

- **Python**: 3.13+ (specified in pyrightconfig.json)
- **Platform**: Linux (Ubuntu) as primary development environment
- **Dependencies**: See `requirements.txt` for complete list including Pydantic v2, Streamlit, BrightData clients

## 8. Quality & Validation Protocols

### Zero-Error Policy
- All code changes must pass validation before completion
- Run full test suite before any database schema changes
- Skills validation must maintain 100% accuracy with original job descriptions
- Database consistency checks required after bulk operations

### Security & Compliance
- BrightData API calls must respect rate limits and terms of service
- Skills data extraction must not store personal information
- Database queries must use parameterized statements to prevent injection
- All external API interactions logged for audit compliance

### Continuous Validation Loop
1. **Implementation**: Apply changes with minimal diff
2. **Testing**: Run relevant test suite (`pytest tests/`)
3. **Validation**: Execute `python check_db.py` for database integrity
4. **Quality Check**: Run `python -m black --check` and `python -m pyright`
5. **Skills Validation**: Execute `python scripts/validate_skills.py`
6. **Documentation**: Update memory bank schemas

## 9. Important Notes

- This project transitioned from browser automation to API-based scraping for better compliance
- Legacy browser-based implementations are preserved in `archive/` directory
- Database schema is optimized for skill analysis and job market insights
- Skills extraction is deterministic and repeatable using JSON pattern database