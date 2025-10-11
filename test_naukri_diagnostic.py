#!/usr/bin/env python3
"""
Naukri API Diagnostic Test
===========================
This script thoroughly tests the Naukri API to identify issues.
"""

import requests
import json
from datetime import datetime

print("=" * 70)
print("NAUKRI API DIAGNOSTIC TEST")
print("=" * 70)
print(f"Timestamp: {datetime.now()}")
print()

# Test 1: Basic connectivity
print("🔍 TEST 1: Basic Connectivity")
print("-" * 70)
try:
    response = requests.get("https://www.naukri.com", timeout=10)
    print(f"✅ Naukri.com is reachable")
    print(f"   Status: {response.status_code}")
    print(f"   Response time: {response.elapsed.total_seconds():.2f}s")
except Exception as e:
    print(f"❌ Cannot reach Naukri.com: {e}")
    exit(1)

print()

# Test 2: API endpoint with minimal headers
print("🔍 TEST 2: API Endpoint (Minimal Headers)")
print("-" * 70)

api_url = "https://www.naukri.com/jobapi/v3/search"
params = {
    "noOfResults": 5,
    "urlType": "search_by_keyword",
    "searchType": "adv",
    "keyword": "Python Developer",
    "pageNo": 1,
    "k": "Python Developer",
    "seoKey": "python-developer-jobs",
    "src": "jobsearchDesk",
    "latLong": "19.0760_72.8777"
}

minimal_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json"
}

try:
    response = requests.get(api_url, params=params, headers=minimal_headers, timeout=15)
    print(f"Status Code: {response.status_code}")
    print(f"Response Size: {len(response.content)} bytes")
    
    if response.status_code == 200:
        print("✅ API returned 200 OK")
        data = response.json()
        print(f"   Response keys: {list(data.keys())}")
        if 'jobDetails' in data:
            print(f"   Jobs returned: {len(data.get('jobDetails', []))}")
        else:
            print("   ⚠️  'jobDetails' key missing in response")
    else:
        print(f"❌ API returned {response.status_code}")
        print(f"   Response: {response.text[:500]}")
except Exception as e:
    print(f"❌ Request failed: {e}")

print()

# Test 3: API endpoint with full headers (current config)
print("🔍 TEST 3: API Endpoint (Full Headers - Current Config)")
print("-" * 70)

full_headers = {
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0",
    "Referer": "https://www.naukri.com",
    "Origin": "https://www.naukri.com",
    "Connection": "keep-alive",
    "appid": "109",
    "clientid": "d3skt0p",
    "systemid": "Naukri",
    "gid": "LOCATION,INDUSTRY,EDUCATION,FAREA_ROLE",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "TE": "trailers",
    "Priority": "u=4"
}

try:
    response = requests.get(api_url, params=params, headers=full_headers, timeout=15)
    print(f"Status Code: {response.status_code}")
    print(f"Response Size: {len(response.content)} bytes")
    
    if response.status_code == 200:
        print("✅ API returned 200 OK")
        data = response.json()
        print(f"   Response keys: {list(data.keys())}")
        
        if 'jobDetails' in data:
            jobs = data.get('jobDetails', [])
            print(f"   Jobs returned: {len(jobs)}")
            print(f"   Total available: {data.get('noOfJobs', 'N/A')}")
            
            if jobs:
                print("\n   📋 Sample Job Structure:")
                sample = jobs[0]
                print(f"      Keys: {list(sample.keys())}")
                print(f"      Title: {sample.get('title', 'N/A')}")
                print(f"      Company: {sample.get('companyName', 'N/A')}")
                print(f"      Job ID: {sample.get('jobId', 'N/A')}")
        else:
            print("   ⚠️  'jobDetails' key missing in response")
            print(f"   Full response: {json.dumps(data, indent=2)[:500]}")
    else:
        print(f"❌ API returned {response.status_code}")
        print(f"   Response headers: {dict(response.headers)}")
        print(f"   Response: {response.text[:1000]}")
except Exception as e:
    print(f"❌ Request failed: {e}")
    import traceback
    traceback.print_exc()

print()

# Test 4: Check for rate limiting
print("🔍 TEST 4: Rate Limiting Check (3 rapid requests)")
print("-" * 70)

rate_limit_detected = False
for i in range(3):
    try:
        response = requests.get(api_url, params={**params, "pageNo": i+1}, headers=full_headers, timeout=10)
        print(f"Request {i+1}: Status {response.status_code}")
        
        if response.status_code == 429:
            rate_limit_detected = True
            print("   ⚠️  Rate limit detected!")
        elif response.status_code != 200:
            print(f"   ⚠️  Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")

if not rate_limit_detected:
    print("✅ No rate limiting detected in 3 rapid requests")

print()

# Test 5: Alternative user agents
print("🔍 TEST 5: Testing Different User Agents")
print("-" * 70)

user_agents = [
    ("Chrome Windows", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"),
    ("Firefox Linux", "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"),
    ("Safari Mac", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"),
]

for name, ua in user_agents:
    test_headers = full_headers.copy()
    test_headers["User-Agent"] = ua
    
    try:
        response = requests.get(api_url, params=params, headers=test_headers, timeout=10)
        print(f"{name:20} → Status: {response.status_code} → Size: {len(response.content):,} bytes")
    except Exception as e:
        print(f"{name:20} → ❌ Failed: {str(e)[:50]}")

print()

# Test 6: Check API response structure changes
print("🔍 TEST 6: API Response Structure Validation")
print("-" * 70)

try:
    response = requests.get(api_url, params=params, headers=full_headers, timeout=15)
    if response.status_code == 200:
        data = response.json()
        
        # Expected keys
        expected_keys = ['jobDetails', 'noOfJobs', 'pageSize']
        found_keys = [k for k in expected_keys if k in data]
        missing_keys = [k for k in expected_keys if k not in data]
        
        print(f"Expected keys found: {found_keys}")
        if missing_keys:
            print(f"⚠️  Missing keys: {missing_keys}")
        
        # Check job structure
        if 'jobDetails' in data and data['jobDetails']:
            job = data['jobDetails'][0]
            expected_job_keys = ['title', 'companyName', 'jobId', 'jobDescription', 'skills']
            found_job_keys = [k for k in expected_job_keys if k in job]
            missing_job_keys = [k for k in expected_job_keys if k not in job]
            
            print(f"Expected job keys found: {found_job_keys}")
            if missing_job_keys:
                print(f"⚠️  Missing job keys: {missing_job_keys}")
                print(f"   Actual keys in job: {list(job.keys())}")
        
        print("✅ API structure validated")
    else:
        print(f"❌ Cannot validate - got status {response.status_code}")
except Exception as e:
    print(f"❌ Validation failed: {e}")

print()

# Summary
print("=" * 70)
print("DIAGNOSTIC SUMMARY")
print("=" * 70)
print("""
If all tests pass:
  ✅ Naukri API is working fine
  → Check your scraper code for bugs

If Test 2 fails but Test 3 passes:
  ⚠️  Headers are critical
  → Keep using full headers configuration

If both Test 2 and 3 fail:
  ❌ API may be blocked or changed
  → Consider switching to Playwright-based scraping

If Test 6 shows missing keys:
  ⚠️  API structure changed
  → Update parser to match new structure

Check logs above for specific issues!
""")
print("=" * 70)
