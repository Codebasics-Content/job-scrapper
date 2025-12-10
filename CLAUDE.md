# Claude Code Awareness - Job Scrapper Project

## CRITICAL: Git Commit Rules

**NEVER include in commit messages:**
- "Generated with Claude Code"
- "Co-Authored-By: Claude"
- Any mention of Claude or AI assistance

## Project Overview

LinkedIn Job Scraper pipeline built with Python, Playwright, and Streamlit.
- Scrapes job listings from LinkedIn
- Extracts skills from job descriptions using regex patterns
- Stores data in SQLite database
- Provides Streamlit UI for interaction

## Root Directory Structure

Only 2 folders at root level:
```
Job_Scrapper/
├── code/           # All source code and project files
└── Analysis/       # Downloaded CSVs and notebooks (gitignored)
```

## Analysis Folder Structure

Downloaded from Analysis tab - **NOT tracked in git**:
```
Analysis/
├── Data Analysis/
│   ├── [Role Name]/
│   │   ├── analysis_notebook.ipynb  # Reusable template
│   │   └── role_data.csv            # Role-specific data
│   └── ...
├── Data Engineering/
│   ├── [Role Name]/
│   │   ├── analysis_notebook.ipynb
│   │   └── role_data.csv
│   └── ...
└── GenAI&DataScience Bootcamp/
    ├── [Role Name]/
    │   ├── analysis_notebook.ipynb
    │   └── role_data.csv
    └── ...
```

**Note**: Single notebook template is reusable across all folders - only CSV file name changes.

## CRITICAL: File Locations

### Configuration Files (ALWAYS use these paths)

| File | Path | Description |
|------|------|-------------|
| Skills Reference | `code/src/config/skills_reference_2025.json` | 977 skills with regex patterns |
| Roles Reference | `code/src/config/roles_reference_2025.json` | 150 roles with regex patterns |

### DO NOT create config files at root level
- Always use `code/src/config/` directory for reference files
- Root-level JSON files are for exports/temporary data only

## Database

- **Location**: `code/data/jobs.db` (SQLite)
- **Main table**: `jobs`

| Column | Type | Description |
|--------|------|-------------|
| job_id | TEXT | Primary key |
| platform | TEXT | e.g., "LinkedIn" |
| actual_role | TEXT | Job role |
| url | TEXT | Job URL (unique) |
| job_description | TEXT | Full description |
| skills | TEXT | Comma-separated skills |
| company_name | TEXT | Company name |
| posted_date | TEXT | When posted |
| scraped_at | DATETIME | Scrape timestamp |

## Code Directory Structure

```
code/
├── streamlit_app.py           # Main Streamlit app
├── run_scraper.py             # CLI scraper runner
├── save_linkedin_cookies.py   # Cookie auth setup
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables
├── data/
│   └── jobs.db                # SQLite database
├── src/
│   ├── config/                    # Configuration files
│   │   ├── skills_reference_2025.json   # Skills patterns (977 skills)
│   │   └── roles_reference_2025.json    # Roles patterns (150 roles)
│   ├── scraper/
│   │   └── unified/
│   │       └── linkedin/          # LinkedIn scraper components
│   │           ├── concurrent_detail_scraper.py  # Multi-tab scraper (up to 10 tabs)
│   │           ├── sequential_detail_scraper.py  # Single-tab scraper
│   │           ├── retry_helper.py               # Retry logic, 404/503 handling
│   │           ├── selector_config.py            # LinkedIn CSS selectors
│   │           └── job_validator.py              # Job validation
│   ├── db/
│   │   └── operations.py          # Database CRUD operations
│   ├── ui/
│   │   └── components/            # Streamlit UI components
│   ├── analysis/
│   │   └── skill_extraction/      # Skill extraction logic
│   │       ├── extractor.py       # AdvancedSkillExtractor class
│   │       └── layer3_direct.py   # Pattern matching from JSON
│   └── utils/                     # Utility functions
├── scripts/                   # Utility scripts
├── tests/                     # Test files
├── docs/                      # Documentation
└── venv/                      # Virtual environment
```

## Key Components

### Skill Extraction
Skills are extracted using `AdvancedSkillExtractor` class:
```python
from src.analysis.skill_extraction.extractor import AdvancedSkillExtractor
extractor = AdvancedSkillExtractor('src/config/skills_reference_2025.json')
skills = extractor.extract(job_description)
```

### Concurrent Scraping
- Supports up to 10 browser tabs
- Smart rate limiting with delays (no proxy needed)
- Staggered tab starts to avoid detection
- Cooldown periods every 10 batches

### Error Handling
- **404 errors**: Delete job URL from database
- **503 errors**: Retry with exponential backoff
- **Rate limiting**: 30s backoff on 429 errors

## Running the App

```bash
cd code
streamlit run streamlit_app.py
```

## Verification Tools

Cross-verify skills extraction (fast, uses Node.js):
```bash
cd code
node fast_verify.js
```

## Notes

- **No proxy required**: Smart delays protect against rate limits
- **Cookie-based auth**: Uses `linkedin_cookies.json` for authentication
- Archived proxy configs are in `code/docs/archive/` (not in use)
