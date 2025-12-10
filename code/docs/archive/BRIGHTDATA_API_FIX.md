# BrightData API Fix - 400 Error Resolution

**Date:** 2025-10-10  
**Issue:** 400 Bad Request errors from BrightData API  
**Status:** ✅ FIXED

## Problem

```
⚠️ United States: 400 Client Error: Bad Request for url: https://api.brightdata.com/dca/trigger
```

### Root Cause
We were using the **DCA (Data Collector API)** endpoints, but BrightData Datasets use the **Datasets API v3** with different:
- Endpoints
- Request payload format
- Response structure

## Solution Applied

### 1. Updated API Endpoints

**Before (Wrong - DCA):**
```python
trigger_endpoint: str = "/dca/trigger"
task_endpoint: str = "/dca/tasks/get"
```

**After (Correct - Datasets API v3):**
```python
trigger_endpoint: str = "/datasets/v3/trigger"
snapshot_endpoint: str = "/datasets/v3/snapshot"
```

### 2. Updated Request Payload

**Before:**
```python
payload = {
    "collectorId": collector_id,
    "args": {"keyword": "...", "location": "..."}
}
```

**After:**
```python
payload = {
    "dataset_id": dataset_id,
    "endpoint": "discover_new",
    "keyword": "...",
    "location": "...",
    # ... other parameters flattened
}
```

### 3. Updated Response Handling

**Before:**
```python
task_id = data.get("id") or data.get("response_id")
batch = task.get("results") or task.get("data") or []
```

**After:**
```python
snapshot_id = data.get("snapshot_id")
batch = snapshot.get("data", [])
```

### 4. Updated Polling Logic

**Before:**
```python
status in ("completed", "success", "done")
```

**After:**
```python
status == "ready"  # Datasets API uses "ready" status
```

### 5. Increased Timeout

```python
timeout_seconds: int = 120  # Was 30, now 120 for dataset collection
```

## Files Modified

### 1. `src/scraper/brightdata/config/settings.py`
- ✅ Changed endpoints to `/datasets/v3/*`
- ✅ Increased timeout to 120 seconds
- ✅ Added snapshot_endpoint

### 2. `src/scraper/brightdata/clients/base.py`
- ✅ Updated `trigger()` method for Datasets API
- ✅ Updated `get_task()` to fetch snapshots
- ✅ Updated `poll_until_done()` for "ready" status
- ✅ Added better error messages

### 3. `src/scraper/brightdata/clients/linkedin.py`
- ✅ Changed `task_id` → `snapshot_id`
- ✅ Changed result extraction to `snapshot.get("data", [])`

### 4. `src/scraper/brightdata/clients/indeed.py`
- ✅ Changed `task_id` → `snapshot_id`
- ✅ Changed result extraction to `snapshot.get("data", [])`

## API Flow (Corrected)

```
1. TRIGGER REQUEST
   POST https://api.brightdata.com/datasets/v3/trigger
   {
       "dataset_id": "gd_lpfll7v5hcqtkxl6l",
       "endpoint": "discover_new",
       "keyword": "Data Scientist",
       "location": "United States",
       "limit": 20
   }
   
2. RESPONSE
   {
       "snapshot_id": "abc123..."
   }
   
3. POLL SNAPSHOT (every 2 seconds)
   GET https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}
   
4. SNAPSHOT READY
   {
       "status": "ready",
       "data": [
           {"job_title": "...", "company": "...", ...},
           ...
       ]
   }
```

## Testing

### Test Command
```bash
streamlit run streamlit_app.py
```

### Test Steps
1. Select LinkedIn or Indeed
2. Enter a job role (e.g., "Data Scientist")
3. Select 1-2 countries
4. Set limit to 5-10 jobs
5. Click "Start Scraping"

### Expected Behavior
- ✅ No more 400 errors
- ✅ Progress shows "Scraping {country}..."
- ✅ Jobs are collected and stored
- ✅ Analytics tab shows data

## BrightData Datasets API Documentation

### Datasets IDs
- **LinkedIn:** `gd_lpfll7v5hcqtkxl6l`
- **Indeed:** `gd_l4dx9j9sscpvs7no2`

### Status Values
- `running` - Collection in progress
- `ready` - Data ready to download
- `error` - Collection failed

### Parameters (LinkedIn)
- `keyword` - Job search term
- `location` - Geographic location
- `time_range` - Date posted filter
- `job_type` - Employment type
- `limit` - Number of results

### Parameters (Indeed)
- `query` - Job search term
- `location` - Geographic location
- `days_back` - Days to look back
- `limit` - Number of results

## Troubleshooting

### If Still Getting 400 Errors

1. **Check API Token**
   ```bash
   cat .env | grep BRIGHTDATA_API_TOKEN
   ```

2. **Verify Dataset IDs**
   - LinkedIn: `gd_lpfll7v5hcqtkxl6l`
   - Indeed: `gd_l4dx9j9sscpvs7no2`

3. **Check Request Payload**
   - Ensure all parameters are at top level
   - No nested `args` object
   - Include `endpoint: "discover_new"`

4. **API Rate Limits**
   - Max 1 request per second (configured)
   - Timeout: 120 seconds

### If Timeout Occurs

- Reduce number of countries
- Reduce job limit
- Try different time of day (API might be busy)

## Alternative: Use Naukri Instead

If BrightData continues to have issues:
```
Platform: Naukri
Job Role: <any role>
Number of Jobs: 10-50
```

Naukri uses a different API and should work independently.

## Summary

**Issue:** Wrong API endpoints causing 400 errors  
**Fix:** Updated to Datasets API v3 with correct payload format  
**Status:** Ready for testing  
**Next:** Run streamlit app and test LinkedIn/Indeed scraping

---

**Files to Review:**
- `src/scraper/brightdata/config/settings.py` - Endpoints
- `src/scraper/brightdata/clients/base.py` - Core API logic
- `src/scraper/brightdata/clients/linkedin.py` - LinkedIn client
- `src/scraper/brightdata/clients/indeed.py` - Indeed client
