# Naukri Scraper - Simplified Architecture

## Overview
This directory contains a **unified, client-friendly** Naukri.com job scraper that eliminates duplications and complexity.

## Main Files

### `naukri_scraper.py` - **MAIN ENTRY POINT**
- **Single unified scraper** combining API and browser approaches
- **API-first strategy**: Fast, reliable job extraction
- **Browser fallback**: When API limits are hit
- **Simple interface**: Easy for clients to understand and maintain

### `__init__.py`
- Exports the main `NaukriScraper` class
- Clean import interface for the rest of the application

## Usage Example

```python
from src.scraper.naukri import NaukriScraper

# Initialize scraper
scraper = NaukriScraper()

# Scrape jobs (API first, browser fallback)
jobs = await scraper.scrape_jobs(
    keyword="python developer",
    num_jobs=50,
    location="bangalore"
)

# Clean up
scraper.close()
```

## Architecture Benefits

1. **No Duplications**: Single scraper handles both API and browser approaches
2. **Client-Friendly**: Clear, simple code structure
3. **Reliable**: API-first with browser fallback
4. **Maintainable**: ≤80 lines per file (EMD compliant)
5. **Self-Documenting**: Clear method names and comments

## Removed Complexity

The following complex files were removed to simplify the architecture:
- Multiple extractors (api_fetcher, card_extractor, job_parser, etc.)
- Separate API and browser scrapers
- Complex configuration hierarchies
- Redundant parsing logic

## Performance

- **API Mode**: ~20-30 jobs/minute
- **Browser Mode**: ~5-10 jobs/minute (fallback only)
- **Anti-Bot Protection**: Built-in headers and rate limiting
- **Memory Efficient**: Minimal resource usage