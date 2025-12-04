# Job Scraper & Analytics Dashboard

**Automated job data pipeline** for LinkedIn and Naukri with intelligent skill extraction and real-time analytics.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/playwright-1.40+-2EAD33?logo=playwright&logoColor=white)](https://playwright.dev/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/sqlite-3-003B57?logo=sqlite&logoColor=white)](https://sqlite.org/)

---

## Overview

A production-ready job scraping system that collects job listings from LinkedIn and Naukri, extracts technical skills using regex-based NLP, and provides interactive analytics through a Streamlit dashboard.

### Key Capabilities

| Feature | Description |
|---------|-------------|
| **Two-Phase Scraping** | Separate URL collection and detail extraction for resilience |
| **3-Layer Skill Extraction** | 951 skills with regex patterns, zero false positives |
| **150 Role Categories** | Automatic role normalization with pattern matching |
| **Real-Time Analytics** | Interactive charts, skill trends, and platform comparison |
| **Adaptive Rate Limiting** | Circuit breaker with auto-tuning concurrency (2-8 workers) |
| **Resume Capability** | Checkpoint-based recovery from interruptions |

---

## Installation

### Prerequisites

- Python 3.11 or higher
- Node.js 18+ (for validation scripts)
- Git

### Step 1: Clone & Create Virtual Environment

#### Windows (PowerShell)

```powershell
# Clone repository
git clone https://github.com/your-username/job-scraper.git
cd job-scraper

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

#### Windows (Command Prompt)

```cmd
# Clone repository
git clone https://github.com/your-username/job-scraper.git
cd job-scraper

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt
```

#### Linux / WSL

```bash
# Clone repository
git clone https://github.com/your-username/job-scraper.git
cd job-scraper

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### macOS

```bash
# Clone repository
git clone https://github.com/your-username/job-scraper.git
cd job-scraper

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Install Playwright Browsers

#### Standard Installation (Windows/macOS)

```bash
playwright install chromium
```

#### WSL/Linux (Recommended)

Use the setup script to install browsers in the project directory (prevents cache cleanup issues):

```bash
chmod +x setup_playwright.sh
./setup_playwright.sh
```

This sets `PLAYWRIGHT_BROWSERS_PATH` to `.playwright-browsers/` within your project.

### Step 3: Launch Dashboard

```bash
streamlit run streamlit_app.py
```

The dashboard opens at `http://localhost:8501`

---

## Architecture

### Why Two-Phase Scraping?

```
Phase 1: URL Collection          Phase 2: Detail Scraping
┌─────────────────────┐         ┌─────────────────────┐
│  Search Results     │         │  Individual Jobs    │
│  ├── Fast scroll    │   ──▶   │  ├── Full desc      │
│  ├── Extract URLs   │         │  ├── Skills parse   │
│  └── Store to DB    │         │  └── Store details  │
└─────────────────────┘         └─────────────────────┘
      job_urls table                  jobs table
```

**Benefits:**
- **Resilience**: If detail scraping fails, URLs are preserved
- **Efficiency**: Batch process 8 jobs concurrently in Phase 2
- **Resumable**: Pick up exactly where you left off
- **Deduplication**: Skip already-scraped URLs automatically

### Why Regex-Based Skill Extraction (Not NLP)?

| Approach | Speed | Accuracy | Maintenance |
|----------|-------|----------|-------------|
| **Regex (chosen)** | 0.3s/job | 85-90% | Pattern file updates |
| spaCy NER | 3-5s/job | 75-80% | Model retraining |
| GPT-based | 2-10s/job | 90%+ | API costs |

**Our 3-layer approach achieves 85-90% accuracy at 10x speed of NLP:**

1. **Layer 1**: Multi-word phrase extraction (priority matching)
2. **Layer 2**: Context-aware extraction (technical context detection)
3. **Layer 3**: Direct pattern matching (951 skill patterns from JSON)

### Why Adaptive Rate Limiting?

LinkedIn and Naukri have aggressive bot detection. Our `AdaptiveLinkedInRateLimiter`:

- Starts with 8 concurrent workers
- Auto-reduces to 2 on 429 errors
- Circuit breaker triggers 60s pause after 3 consecutive failures
- Gradually increases concurrency when success rate > 95%
- Random jitter (2-4s) mimics human behavior

---

## Project Structure

```
job-scraper/
├── streamlit_app.py              # Main dashboard entry point
├── requirements.txt              # Production dependencies
├── requirements-dev.txt          # Development dependencies (pytest, pyright)
├── setup_playwright.sh           # Playwright browser installer (WSL/Linux)
├── save_linkedin_cookies.py      # LinkedIn authentication helper
│
├── data/
│   ├── jobs.db                   # SQLite database (auto-created)
│   └── *.json                    # Export files, reports
│
├── src/
│   ├── config/                   # Configuration files
│   │   ├── skills_reference_2025.json    # 951 skills with regex patterns
│   │   ├── roles_reference_2025.json     # 150 role categories
│   │   ├── countries.py          # Country/location mappings
│   │   └── naukri_locations.py   # Naukri city GIDs
│   │
│   ├── db/                       # Database layer
│   │   ├── connection.py         # SQLite connection manager
│   │   ├── schema.py             # Two-table schema (job_urls, jobs)
│   │   └── operations.py         # CRUD operations
│   │
│   ├── models/
│   │   └── models.py             # Pydantic models (JobUrlModel, JobDetailModel)
│   │
│   ├── scraper/
│   │   ├── unified/
│   │   │   ├── linkedin/         # LinkedIn scraper components
│   │   │   │   ├── concurrent_detail_scraper.py  # Multi-tab scraper (8 tabs)
│   │   │   │   ├── playwright_url_scraper.py     # URL collection
│   │   │   │   ├── selector_config.py            # CSS selectors
│   │   │   │   ├── retry_helper.py               # 404/503 handling
│   │   │   │   └── job_validator.py              # Field validation
│   │   │   │
│   │   │   ├── naukri/           # Naukri scraper components
│   │   │   │   ├── url_scraper.py         # URL collection with dedup
│   │   │   │   ├── detail_scraper.py      # Detail extraction
│   │   │   │   ├── selectors.py           # CSS selectors
│   │   │   │   └── url_builder.py         # Search URL generator
│   │   │   │
│   │   │   ├── scalable/         # Rate limiting & resilience
│   │   │   │   ├── adaptive_rate_limiter.py   # Circuit breaker
│   │   │   │   ├── checkpoint_manager.py      # Resume capability
│   │   │   │   └── progress_tracker.py        # Batch progress
│   │   │   │
│   │   │   ├── linkedin_unified.py    # LinkedIn orchestrator
│   │   │   └── naukri_unified.py      # Naukri orchestrator
│   │   │
│   │   └── services/             # External service clients
│   │       ├── playwright_browser.py   # Browser automation
│   │       └── session_manager.py      # Cookie/session handling
│   │
│   ├── analysis/
│   │   └── skill_extraction/     # 3-layer skill extraction
│   │       ├── extractor.py            # Main AdvancedSkillExtractor class
│   │       ├── advanced_regex_extractor.py   # Layer 1 & 2
│   │       ├── layer3_direct.py        # Layer 3 pattern matching
│   │       ├── confidence_scorer.py    # Skill confidence scores
│   │       ├── common_words_filter.py  # Filter grammatical words
│   │       ├── deduplicator.py         # Skill normalization
│   │       └── batch_reextract.py      # Re-process existing jobs
│   │
│   ├── ui/
│   │   └── components/           # Streamlit UI components
│   │       ├── kpi_dashboard.py        # Key metrics display
│   │       ├── link_scraper_form.py    # Phase 1 UI
│   │       ├── detail_scraper_form.py  # Phase 2 UI
│   │       └── analytics/
│   │           ├── skills_charts.py    # Skill visualizations
│   │           ├── overview_metrics.py # Summary stats
│   │           └── role_normalizer.py  # Role categorization
│   │
│   └── validation/
│       ├── validation_pipeline.py      # Field validation
│       └── single_job_validator.py     # Per-job validation
│
├── scripts/
│   ├── extraction/
│   │   ├── reextract_skills.py   # Python: Batch re-extraction
│   │   └── reextract_skills.js   # Node.js: Fast re-extraction
│   │
│   └── validation/               # 7-layer validation suite
│       ├── layer1_syntax_check.sh      # Regex pattern syntax
│       ├── layer2_coverage.sh          # Skill coverage analysis
│       ├── layer3_fp_detection.sh      # False positive detection
│       ├── layer4_fn_detection.sh      # False negative detection
│       ├── layer5_context.sh           # Context validation
│       ├── layer6_emerging_skills.sh   # New skill discovery
│       ├── layer7_trend_analysis.sh    # Trend & drift tracking
│       ├── run_all_validations.sh      # Run all 7 layers
│       ├── fast_verify.js              # Quick Node.js verification
│       ├── full_skill_audit.js         # Comprehensive audit
│       └── cross_verify_skills.py      # Python cross-verification
│
├── tests/
│   ├── test_skill_validation_comprehensive.py
│   ├── test_linkedin_selectors.py
│   └── validate_skills_vs_descriptions.py
│
└── docs/                         # Documentation
    ├── VALIDATION_ARCHITECTURE.md
    ├── 2PLATFORM_ARCHITECTURE.md
    └── archive/                  # Historical docs
```

---

## File Roles Reference

### Core Application

| File | Role |
|------|------|
| `streamlit_app.py` | Dashboard entry point, tab routing |
| `src/db/operations.py` | All database CRUD operations |
| `src/db/schema.py` | Two-table schema definition |
| `src/models/models.py` | Pydantic data models with validation |

### Scraping Engine

| File | Role |
|------|------|
| `src/scraper/unified/linkedin/concurrent_detail_scraper.py` | Multi-tab LinkedIn scraping (8 concurrent) |
| `src/scraper/unified/linkedin/selector_config.py` | LinkedIn CSS selectors (2025 updated) |
| `src/scraper/unified/naukri/url_scraper.py` | Naukri URL collection with dedup |
| `src/scraper/unified/scalable/adaptive_rate_limiter.py` | Circuit breaker & auto-tuning |

### Skill Extraction

| File | Role |
|------|------|
| `src/config/skills_reference_2025.json` | 951 skills with regex patterns |
| `src/config/roles_reference_2025.json` | 150 role categories |
| `src/analysis/skill_extraction/extractor.py` | Main 3-layer extraction interface |
| `src/analysis/skill_extraction/layer3_direct.py` | Pattern matching from JSON |

### Validation Scripts

| File | Language | Role |
|------|----------|------|
| `scripts/validation/fast_verify.js` | Node.js | Quick skill verification (10x faster) |
| `scripts/validation/full_skill_audit.js` | Node.js | Comprehensive pattern audit |
| `scripts/validation/cross_verify_skills.py` | Python | Cross-platform verification |
| `scripts/validation/layer*.sh` | Bash | 7-layer validation pipeline |

---

## Usage

### Dashboard Workflow

1. **KPI Dashboard** - View overall statistics
2. **Link Scraper** - Phase 1: Collect job URLs
3. **Detail Scraper** - Phase 2: Extract job details & skills
4. **Analytics** - Analyze skill trends and distributions

### Command Line

```bash
# Run validation suite
bash scripts/validation/run_all_validations.sh

# Quick skill verification (Node.js - fast)
node scripts/validation/fast_verify.js

# Re-extract skills for existing jobs
python -m src.analysis.skill_extraction.batch_reextract --batch-size 100

# Full skill audit
node scripts/validation/full_skill_audit.js
```

### LinkedIn Authentication (Optional)

For authenticated scraping with higher limits:

```bash
python save_linkedin_cookies.py
```

This saves cookies to `linkedin_cookies.json` for subsequent sessions.

---

## Configuration

### Skills Reference (`src/config/skills_reference_2025.json`)

```json
{
  "total_skills": 951,
  "skills": [
    {
      "name": "Python",
      "patterns": ["\\bPython\\b", "\\bpython\\b", "\\bPython3\\b"]
    }
  ]
}
```

### Roles Reference (`src/config/roles_reference_2025.json`)

Contains 150 standardized job role categories with pattern matching for normalization.

### Environment Variables (Optional)

Create `.env` file:

```env
# Database path (default: data/jobs.db)
DB_PATH=data/jobs.db

# Playwright browser path (for WSL)
PLAYWRIGHT_BROWSERS_PATH=.playwright-browsers

# BrightData proxy (optional)
BRIGHTDATA_WS_URL=wss://brd-customer-xxx-zone-scraping_browser2:PASSWORD@brd.superproxy.io:9222
```

---

## Database Schema

### Two-Table Architecture

```sql
-- Phase 1: URL Collection (lightweight)
CREATE TABLE job_urls (
    job_id TEXT PRIMARY KEY,
    platform TEXT NOT NULL,        -- 'LinkedIn' or 'Naukri'
    input_role TEXT NOT NULL,      -- Search keyword
    actual_role TEXT NOT NULL,     -- Job title from listing
    url TEXT NOT NULL UNIQUE,
    scraped INTEGER DEFAULT 0      -- 0=pending, 1=scraped
);

-- Phase 2: Full Details
CREATE TABLE jobs (
    job_id TEXT PRIMARY KEY,
    platform TEXT NOT NULL,
    actual_role TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    job_description TEXT,          -- Full HTML/text
    skills TEXT,                   -- Comma-separated skills
    company_name TEXT,
    posted_date TEXT,
    scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## Performance

| Metric | Value |
|--------|-------|
| URL Collection | 200-300 URLs/min |
| Detail Scraping | 15-20 jobs/min (8 workers) |
| Skill Extraction | 0.3s/job |
| Validation Pass Rate | 85-95% |
| Storage per Job | ~2KB |

---

## Troubleshooting

### Playwright Browser Not Found (WSL/Linux)

```bash
# Error: Executable doesn't exist at ~/.cache/ms-playwright/
./setup_playwright.sh
```

### No Jobs Collected

- Check internet connection
- Try different search terms
- LinkedIn may require authentication - run `python save_linkedin_cookies.py`

### High Validation Failures

- Platform selectors may have changed
- Check `src/scraper/unified/linkedin/selector_config.py`
- Check `src/scraper/unified/naukri/selectors.py`

### Rate Limited (429 Errors)

The adaptive rate limiter handles this automatically:
- Concurrency reduces from 8 → 2
- Circuit breaker triggers 60s pause
- Gradually recovers when stable

### Database Locked

```bash
# Kill any zombie processes
pkill -f streamlit

# Restart
streamlit run streamlit_app.py
```

---

## Development

### Install Dev Dependencies

```bash
pip install -r requirements-dev.txt
```

### Run Tests

```bash
pytest tests/ -v
```

### Type Checking

```bash
basedpyright src/
```

---

## License

MIT License - See [LICENSE](LICENSE) file for details.

---

**Ready to start?** Run `streamlit run streamlit_app.py` and navigate to `http://localhost:8501`
