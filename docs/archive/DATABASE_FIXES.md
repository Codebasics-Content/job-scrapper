# Database Consistency Fixes - Oct 2025

## Issues Identified

### 1. Platform Naming Inconsistency
**Problem:** 
- LinkedIn: `"linkedin"` (lowercase)
- Naukri: `"Naukri"` (capitalized)

**Impact:** Inconsistent querying, filtering, and analytics

### 2. Job ID Format Inconsistency
**Problem:**
- LinkedIn: `"linkedin_4145920846"` (prefixed)
- Naukri: `"24d1e84245bbca9ad4f5414d8830cccc"` (raw hash, no prefix)

**Impact:** Cannot distinguish platform from ID alone, potential collisions

### 3. Skills Visualization Warning
**Problem:** `WARNING: No skills found in jobs`
**Root Cause:** Skills stored as JSON strings not properly parsed in viz layer

## Fixes Applied

### ✅ Platform Name Standardization
Changed all Naukri scraper files to use lowercase `"naukri"`:

**Files Modified:**
- `src/scraper/naukri/browser_scraper.py` (Line 23)
- `src/scraper/naukri/extractors/job_parser.py` (Line 67)
- `src/scraper/naukri/extractors/api_parser.py` (Line 51)
- `src/scraper/naukri/extractors/card_extractor.py` (Line 77)

**Result:** Both platforms now use lowercase names consistently

## Remaining Issues (Outside Scope)

### Job ID Prefix for Naukri
**Status:** NOT FIXED (requires architecture decision)
**Options:**
1. Add `naukri_` prefix to all Naukri job IDs
2. Keep raw hashes (current behavior)
3. Create platform-agnostic UUID system

**Recommendation:** Add prefix for consistency, but requires testing

### Skills Visualization Fix
**Status:** Separate issue in `src/analysis/` visualization layer
**Root Cause:** JSON parsing not applied before visualization
**Fix Location:** `src/analysis/analysis/visualization/skill_leaderboard.py`

## Validation Commands

```bash
# Check database consistency
python check_db.py

# Verify platform names
sqlite3 jobs.db "SELECT DISTINCT platform FROM jobs;"
# Expected: linkedin, naukri (both lowercase)

# Check job ID patterns
sqlite3 jobs.db "SELECT platform, job_id FROM jobs LIMIT 2;"
```

## Database Schema

```sql
Column                Type
-------------------  ------
job_id               TEXT
job_role             TEXT  
company              TEXT
experience           TEXT
skills               TEXT (JSON string)
jd                   TEXT
platform             TEXT
url                  TEXT
location             TEXT
salary               TEXT
posted_date          TEXT
scraped_at           TEXT
```

**Note:** No `description` column exists (user initially looked for it)
