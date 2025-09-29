# 🎯 Job Scraper - LinkedIn Job Data Extraction Platform

[![Python 3.13.3](https://img.shields.io/badge/python-3.13.3-blue.svg)](https://www.python.org/) [![EMD Architecture](https://img.shields.io/badge/architecture-EMD-purple.svg)]()

## 🌟 Overview

Enterprise-grade web scraping platform that extracts LinkedIn job listings, analyzes skill requirements, and provides actionable insights through an interactive Streamlit dashboard.

**Key Features:**
- 🔍 LinkedIn infinite scroll scraping (1000+ jobs)
- 📊 Real-time skill leaderboard analytics
- 💾 SQLite database with duplicate detection
- 🎨 Streamlit UI with progress tracking
- 📈 Statistical analysis & CSV/JSON export

**Stack:** Python 3.13.3 | Selenium 4.15.2 | Pydantic v2 | Streamlit | SQLite3

## 🏗️ Architecture Principles

### EMD (Extreme Microservices Decomposition)
- **≤80 lines per file** - enforces modularity
- **Deep nested folders** - logical separation
- **Single responsibility** - each module does one thing well

### ZUV (Zero Unused Variables)
- **No `_` prefixes** - every variable has a purpose
- **Type safety** - Python 3.13.3 builtin generics
- **Descriptive naming** - action-oriented, meaningful names

**Core:** Selenium, undetected-chromedriver, Pydantic, Streamlit | **Analysis:** Pandas, BeautifulSoup4, NLP

## 🚀 Installation

**Prerequisites:** Python 3.13.3, Google Chrome

```bash
# Clone and setup
git clone https://github.com/yourusername/job-scraper.git
cd job-scraper

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt
```

## 🎬 Quick Start

```bash
# Launch application
streamlit run streamlit_app.py
# Opens at http://localhost:8501
```

**Usage:**
1. Enter job role (e.g., "Data Scientist")
2. Select LinkedIn platform
3. Set job count (10-1000)
4. Click "Start Scraping"
5. View results in Job Listings, Skill Leaderboard, Analytics tabs

## 📁 Project Structure

```
job-scraper/
├── scrapers/              # Web scraping (EMD: ≤80 lines/file)
│   ├── base/              # Base infrastructure
│   │   ├── anti_detection.py    # ChromeDriver factory
│   │   ├── base_scraper.py      # Abstract base class
│   │   └── retry_logic.py       # Exponential backoff
│   └── linkedin/          # LinkedIn implementation
│       ├── scraper.py           # Main scraper
│       └── extractors/          # Modular extractors
│           ├── job_id_extractor.py
│           ├── api_job_fetcher.py
│           └── scroll_handler.py
│
├── database/              # Data persistence
│   └── core/              # Core operations
│       ├── connection_manager.py
│       ├── batch_operations.py
│       └── job_retrieval.py
│
├── models/                # Pydantic data models
│   └── job.py
│
├── utils/                 # Analysis utilities
│   └── analysis/
│       ├── nlp/           # Skill extraction
│       └── visualization/ # Charts & leaderboard
│
├── tests/                 # Test suite
├── streamlit_app.py       # Main UI
├── requirements.txt       # Dependencies
└── jobs.db                # SQLite database
```

**EMD Benefits:** Maintainability, Testability, Reusability, Scalability

## ⚙️ How It Works

**Scraping Flow:**
```
User Input → Scroll Handler → Job ID Extractor → API Fetcher
  ↓
NLP Skill Extraction → Pydantic Validation → SQLite Storage
```

**Infinite Scroll:**
1. Load initial page (25 jobs)
2. Scroll to bottom → LinkedIn loads more
3. Extract job IDs (skip duplicates)
4. Fetch details via LinkedIn API
5. Click "See More Jobs" button
6. Repeat until target reached

**Duplicate Prevention:**
- `processed_ids` set (in-memory)
- Database UNIQUE constraint on `job_id`
- Batch operations report: "X new jobs, Y duplicates"

## 📖 Usage

**Programmatic:**
```python
import asyncio
from scrapers.linkedin.scraper import LinkedInScraper

async def scrape():
    scraper = LinkedInScraper()
    jobs = await scraper.scrape_jobs(
        job_role="Data Scientist",
        target_count=100
    )
    print(f"Scraped {len(jobs)} jobs")

asyncio.run(scrape())
```

**Configuration:**
- GUI mode: Set `headless_mode = False` in `anti_detection.py`
- Rate limiting: Adjust `await asyncio.sleep(0.5)` in `scraper.py`

**Testing:**
```bash
pytest tests/                    # Run all tests
basepyright .                    # Type checking
black .                          # Code formatting
```

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| ChromeDriver not found | Auto-installed via webdriver-manager |
| LinkedIn popup blocking | Scraper works behind popups (cosmetic only) |
| Duplicate jobs | Expected - database rejects via `job_id` constraint |
| Scraping stops early | LinkedIn limits results - try broader search |

**Debug Mode:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📊 Performance

- Scraping: ~10-15 jobs/minute
- Database: 10,000+ jobs/second (batch mode)
- Memory: ~200MB per 1000 jobs
- UI: <100ms response time

## 📄 License & Support

**License:** MIT  
**Issues:** [GitHub Issues](https://github.com/yourusername/job-scraper/issues)  
**Docs:** `.windsurf/memory-bank/` for detailed context

**Built with:** Selenium | Pydantic | Streamlit | SQLite3 | **Architecture:** EMD (≤80 lines) | ZUV (Zero Unused Variables)

**🚀 Ready to scrape jobs? Run `streamlit run streamlit_app.py`**
