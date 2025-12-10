# User Interface Module

## Purpose
Provides the interactive Streamlit dashboard where users control scraping and view analytics.

## What It Does
- **Link Scraper Tab** - Controls for Phase 1 URL collection
- **Detail Scraper Tab** - Controls for Phase 2 job detail extraction
- **Analytics Dashboard** - Real-time visualizations of collected data
- **Progress Tracking** - Live updates showing scraping status and validation results
- **Data Export** - Download results as CSV or JSON for external analysis

## Components
- `components/link_scraper_form.py` - Phase 1 interface
- `components/detail_scraper_form.py` - Phase 2 interface with validation gates display
- `components/analytics/` - Charts and visualizations (skills, companies, platforms)

## Why It Matters
This is the stakeholder-facing layer. Non-technical users can operate the entire system without touching code. Real-time feedback builds confidence that the system is working correctly.

## User Experience
Clean, three-tab design with visual progress indicators ensures users always know what's happening and what to do next.
