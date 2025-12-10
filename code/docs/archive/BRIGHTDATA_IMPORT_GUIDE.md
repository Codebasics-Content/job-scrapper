# BrightData LinkedIn Import Guide

## Overview
Import pre-scraped LinkedIn job data from BrightData with automatic skills extraction and duplicate checking.

## Features
✅ **JSON Import** - Upload BrightData JSON files  
✅ **Skills Extraction** - Automatic extraction using existing patterns  
✅ **Duplicate Prevention** - Uses job_id matching to skip existing jobs  
✅ **Direct Storage** - Saves directly to jobs table (no real-time scraping)

## Expected JSON Format

### Option 1: Array Format
```json
[
  {
    "url": "https://www.linkedin.com/jobs/view/123456",
    "title": "Senior Data Scientist",
    "company": "Tech Corp",
    "description": "Full job description with skills...",
    "posted_date": "2025-01-10",
    "location": "San Francisco, CA"
  },
  {
    "url": "https://www.linkedin.com/jobs/view/789012",
    "title": "ML Engineer",
    "company": "AI Startup",
    "description": "Another job description...",
    "posted_date": "2025-01-09",
    "location": "Remote"
  }
]
```

### Option 2: Object with Results Key
```json
{
  "results": [
    {
      "url": "...",
      "title": "...",
      "company": "...",
      "description": "..."
    }
  ],
  "total": 150
}
```

## Required Fields
- **url** (string) - Job posting URL (used for deduplication)
- **title** (string) - Job title

## Optional Fields
- **description** (string) - Job description for skills extraction
- **company** (string) - Company name
- **company_detail** (string) - Company details
- **posted_date** (string) - ISO format or human-readable
- **location** (string) - Job location

## Usage via Streamlit UI

1. Navigate to **📥 LinkedIn Import** tab
2. Click **Browse files** to upload JSON
3. Click **🚀 Import Jobs**
4. View results: stored count and duplicates

## Usage via Python

```python
from src.importer.brightdata import import_linkedin_jobs

# From JSON file
from src.importer.brightdata.linkedin_importer import import_from_json_file

stored, duplicates = import_from_json_file("brightdata_jobs.json")
print(f"Stored: {stored}, Duplicates: {duplicates}")

# From Python list
data = [
    {"url": "...", "title": "...", "description": "..."},
    # more jobs...
]

stored, duplicates = import_linkedin_jobs(data)
```

## How It Works

1. **Parse** - Converts BrightData JSON to `JobDetailModel`
2. **Generate job_id** - Creates unique ID from platform + URL hash
3. **Extract Skills** - Scans description using skill patterns
4. **Check Duplicates** - Queries database for existing job_id
5. **Store** - Inserts only new jobs into jobs table

## Architecture

```
src/importer/brightdata/
├── __init__.py                  # Package exports
├── linkedin_parser.py           # JSON → JobDetailModel (≤80 lines)
└── linkedin_importer.py         # Batch import + skills (≤80 lines)
```

## Database Integration

- **Platform**: Always "linkedin"
- **Table**: Directly to `jobs` table
- **Duplicate Check**: Uses `INSERT OR IGNORE` on job_id
- **Skills**: Comma-separated in skills column

## Notes

- No real-time scraping required
- Leverages existing skills extraction pipeline
- Compatible with two-phase scraper database schema
- All files follow EMD principles (≤80 lines)
