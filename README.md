# 🔍 Job Scraper & Analytics Dashboard

Automated job data collection from LinkedIn and Naukri with built-in validation and analytics.

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/playwright-1.40+-green.svg)](https://playwright.dev/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)

## Features

- **Two-Phase Architecture**: Separate URL collection and detail scraping for efficiency
- **Triple Validation**: Field validation, skill validation (794 canonical skills), atomic database transactions
- **Role Normalization**: 150 standardized job role categories with pattern matching
- **Real-Time Analytics**: Interactive dashboard with role-based skill filtering and company insights
- **Resume Capability**: Automatic progress tracking and recovery
- **Anti-Detection**: Human-like browsing patterns with adaptive concurrency (8 workers)

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Launch dashboard
streamlit run streamlit_app.py
```

## Usage

### Phase 1: URL Collection
1. Select platform (LinkedIn/Naukri)
2. Enter job role
3. Set URL count (10-1000)
4. Click "Start URL Collection"

### Phase 2: Detail Scraping
1. Select platform
2. Set batch size
3. Click "Start Detail Scraping"
4. Monitor validation gates (Field → Skills → Database)

### Analytics
- Filter skills by job role (150 standardized categories)
- View skill demand trends
- Compare platforms
- Export data (CSV/JSON)

## Project Structure

```
├── data/
│   └── jobs.db                    # SQLite database
├── src/
│   ├── config/
│   │   ├── skills_reference_2025.json   # 794 validated skills
│   │   └── roles_reference_2025.json    # 150 role categories
│   ├── analysis/
│   │   └── skill_extraction/      # Skill validation modules
│   ├── ui/
│   │   └── components/analytics/   # Analytics components
│   ├── scraper/
│   │   └── unified/
│   │       ├── linkedin/          # LinkedIn scrapers
│   │       ├── naukri/            # Naukri scrapers
│   │       └── scalable/          # Adaptive rate limiter
│   └── db/                        # Database operations
├── tests/                         # Validation tests
└── streamlit_app.py              # Main dashboard
```

## Technical Stack

- **Browser Automation**: Playwright (headless Chrome)
- **Validation**: Pydantic models with triple-gate system
- **Database**: SQLite with atomic transactions
- **UI**: Streamlit modular components (EMD architecture)
- **Concurrency**: Adaptive rate limiting (8 concurrent workers)
- **Skills**: 794 canonical technical skills + 150 role categories

## Validation Gates

1. **Field Validation**: Ensures required fields (title, company, description >100 chars)
2. **Skill Validation**: Matches against canonical skills, filters false positives
3. **Database Storage**: Atomic transactions for data integrity

## Performance

- **URL Collection**: 200-300 URLs/min
- **Detail Scraping**: 15-20 jobs/min (8 concurrent workers)
- **Validation Rate**: 85-95% pass rate
- **Storage**: ~2KB per job

## Configuration

Key files:
- `src/config/skills_reference_2025.json` - Skill validation reference (794 skills)
- `src/config/roles_reference_2025.json` - Role normalization patterns (150 categories)
- `data/jobs.db` - Main database
- `.env` - Environment variables (optional)

## Troubleshooting

**No jobs collected**: Check internet connection or try different search terms

**High validation failures**: Platform structure may have changed, check selector configs

**System stopped**: Simply restart - automatic resume from last checkpoint

## License

MIT License - See LICENSE file for details

---

**Ready to use?** Run `streamlit run streamlit_app.py` 🚀
