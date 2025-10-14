# Job Scraper - Architecture Documentation

**Last Updated**: 2025-10-14  
**Version**: 2.0 (2-Platform Architecture)

## Executive Summary

This is a **production-ready job scraping system** that collects AI/ML job postings from **LinkedIn** and **Naukri** platforms with advanced skill extraction and deduplication capabilities.

### Active Platforms
- ✅ **LinkedIn**: Via JobSpy library + BrightData proxy
- ✅ **Naukri**: Via Playwright browser automation

### Deprecated Platforms
- ❌ **Indeed**: Removed (deprecated October 2025)

---

## System Architecture

```
Job Scraper System
├── Data Collection Layer
│   ├── LinkedIn (JobSpy + BrightData Proxy)
│   └── Naukri (Playwright Browser Automation)
├── Processing Layer
│   ├── Skill Extraction (skills_reference_2025.json)
│   └── Fuzzy Deduplication (multi-layer)
├── Storage Layer
│   └── SQLite Database (jobs.db)
└── UI Layer
    └── Streamlit Dashboard (streamlit_app.py)
```

---

## Core Components

### 1. Multi-Platform Service (`src/scraper/multi_platform_service.py`)
**Purpose**: Unified orchestration layer for all scraping operations

**Key Function**: `scrape_jobs_with_skills()`
- Accepts: platforms, keyword, location, limit
- Returns: List of JobDetailModel with skills extracted
- Stores: Optionally saves to database

**Architecture**:
```python
async def scrape_jobs_with_skills(
    platforms: list[str],  # ["linkedin", "naukri"]
    keyword: str,          # e.g., "AI Engineer"
    location: str,         # e.g., "" for worldwide
    limit: int,            # Jobs per platform
    store_to_db: bool = True
) -> list[JobDetailModel]
```

### 2. Platform-Specific Scrapers

#### LinkedIn (`src/scraper/jobspy/`)
- **Technology**: python-jobspy library
- **Proxy**: BrightData rotating residential proxies
- **Features**:
  - Advanced skill extraction with context analysis
  - Multi-layer fuzzy deduplication (title + company + location)
  - Full job descriptions via API
- **Configuration**: `.env` (BRIGHTDATA_USERNAME, BRIGHTDATA_PASSWORD)

#### Naukri (`src/scraper/unified/naukri_unified.py`)
- **Technology**: Playwright browser automation
- **Features**:
  - 5-tab parallel scraping (asyncio.Semaphore)
  - CSS selector fallback logic for robustness
  - Skills extraction from job descriptions
- **Selectors**: `src/scraper/naukri/config/selectors.py`

### 3. Service Layer (`src/scraper/services/`)
- `naukri_api_client.py`: Naukri API interaction
- Handles authentication, headers, bulk operations

### 4. Database (`jobs.db`)
**Schema**:
- `jobs` table: Main job storage with deduplication
- `job_url` table: URL tracking to prevent re-scraping
- Indexes: platform+url, platform+title+company

### 5. UI Components (`src/ui/components/`)
```
components/
├── scraper_form.py          # Main scraping interface
├── form/
│   ├── two_phase_executor.py  # Scraping workflow execution
│   └── two_phase_panel.py     # UI panel for 2-phase scraping
└── analytics/
    ├── overview_metrics.py    # Job statistics
    ├── platform_charts.py     # Platform distribution
    └── skills_charts.py       # Skills analysis
```

### 6. Skills Reference (`skills_reference_2025.json`)
- **78KB JSON file** with 2025 tech skills taxonomy
- Categories: Programming, ML/AI, Cloud, Databases, DevOps
- Used for: Skill extraction and normalization

---

## Data Flow

```
User Input (Streamlit UI)
    ↓
streamlit_app.py → src/ui/components/scraper_form.py
    ↓
two_phase_executor.py calls multi_platform_service.scrape_jobs_with_skills()
    ↓
Platform Routing:
├── LinkedIn → JobSpy + BrightData → Skills Extraction → Fuzzy Dedup
└── Naukri → Playwright → 5-tab parallel scraping → Skills Extraction
    ↓
Merge Results → Store to jobs.db
    ↓
Display in Analytics Dashboard (src/ui/components/analytics/)
```

---

## Key Features

### 1. Advanced Skill Extraction
- Context-aware pattern matching
- Technology stack detection
- Role-based skill filtering
- Confidence scoring

### 2. Multi-Layer Deduplication
- **Layer 1**: Exact URL matching
- **Layer 2**: Fuzzy title + company (90% similarity)
- **Layer 3**: Location-based clustering

### 3. Parallel Processing
- Naukri: 5 concurrent browser tabs (`asyncio.Semaphore(5)`)
- LinkedIn: Batch API requests via JobSpy

### 4. Robust Error Handling
- Automatic CSS selector fallback (Naukri)
- Proxy rotation (LinkedIn via BrightData)
- Retry mechanisms with exponential backoff

---

## File Structure

```
Job_Scrapper/
├── streamlit_app.py              # Main entry point
├── requirements.txt              # Python dependencies
├── jobs.db                       # SQLite database
├── skills_reference_2025.json   # Skills taxonomy
├── .env                         # Configuration (BrightData credentials)
│
├── src/
│   ├── scraper/
│   │   ├── multi_platform_service.py    # ⭐ Unified orchestrator
│   │   ├── jobspy/                      # LinkedIn scraper
│   │   │   └── scraper.py
│   │   ├── services/                    # API clients
│   │   │   └── naukri_api_client.py
│   │   ├── unified/                     # Platform implementations
│   │   │   ├── naukri_unified.py       # ⭐ Naukri scraper
│   │   │   └── service.py
│   │   └── _deprecated/                 # Legacy code (archived)
│   │
│   ├── ui/
│   │   └── components/                  # ⭐ Streamlit UI components
│   │       ├── scraper_form.py
│   │       ├── form/
│   │       └── analytics/
│   │
│   ├── analysis/
│   │   └── skill_extraction/            # Skill extraction logic
│   │
│   └── db/
│       ├── connection.py                # Database connection
│       └── operations.py                # CRUD operations
│
└── tests/
    ├── test_linkedin_20_validation.py   # LinkedIn test (20 jobs)
    ├── test_naukri_20_validation.py     # Naukri test (20 jobs)
    └── test_2_platforms_1000.py         # Scale test (1000 jobs/platform)
```

---

## Setup & Execution

### Prerequisites
```bash
Python 3.13+
Playwright browsers installed
BrightData account (for LinkedIn)
```

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Configure BrightData proxy
cp .env.example .env
# Edit .env with your credentials
```

### Running the Application
```bash
streamlit run streamlit_app.py
```

### Running Tests
```bash
# Validate scrapers (20 jobs each)
python tests/test_linkedin_20_validation.py
python tests/test_naukri_20_validation.py

# Scale test (1000 jobs per platform)
python tests/test_2_platforms_1000.py
```

---

## Configuration

### Environment Variables (`.env`)
```env
# BrightData Proxy (LinkedIn)
BRIGHTDATA_USERNAME=your_username
BRIGHTDATA_PASSWORD=your_password
BRIGHTDATA_HOST=brd.superproxy.io
BRIGHTDATA_PORT=33335

# Database
DATABASE_PATH=jobs.db
```

### Proxy Configuration (`proxy_manager_config.json`)
```json
{
  "linkedin": {
    "enabled": true,
    "provider": "brightdata"
  },
  "naukri": {
    "enabled": false
  }
}
```

---

## Performance Metrics

### LinkedIn (JobSpy + BrightData)
- **Rate**: ~0.6 jobs/second
- **Success Rate**: 100% (20/20 jobs)
- **Description Coverage**: 100%
- **Skills per Job**: ~23 average

### Naukri (Playwright)
- **Rate**: ~0.7 jobs/second
- **Success Rate**: 100% (20/20 jobs)
- **Description Coverage**: 100%
- **Skills per Job**: ~6 average
- **Parallel Tabs**: 5 concurrent

---

## Troubleshooting

### LinkedIn Issues
- **Problem**: Proxy errors
- **Solution**: Check BrightData credentials in `.env`

### Naukri Issues
- **Problem**: 0 jobs scraped
- **Solution**: CSS selectors may have changed. Update `src/scraper/naukri/config/selectors.py`

### Database Issues
- **Problem**: Duplicate jobs
- **Solution**: Check deduplication logic in `multi_platform_service.py`

---

## Maintenance

### Updating Skills Reference
1. Edit `skills_reference_2025.json`
2. Maintain categories: programming, ml_ai, cloud, databases, devops
3. Test with `test_linkedin_20_validation.py`

### Updating Naukri Selectors
1. Capture current HTML: `capture_naukri_headers.py`
2. Update `src/scraper/naukri/config/selectors.py`
3. Test with `test_naukri_20_validation.py`

---

## Support & Contact

For issues or questions about this architecture, refer to:
- `README.md` - User documentation
- `docs/` - Technical documentation
- `.windsurf/aegiside/memory-bank/` - Development logs

---

**Architecture Version**: 2.0  
**Platforms**: LinkedIn, Naukri  
**Status**: Production Ready ✅
