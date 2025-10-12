# Fix BrightData Proxy Authentication

## Current Issue
- Docker IP `172.19.0.1` is **PENDING APPROVAL**
- Getting 407 Proxy Authentication Required
- Credentials are correct but IP not whitelisted yet

## Solution: Approve Pending IP via Web UI

### Step 1: Access Proxy Manager
Open in browser: http://localhost:22999

### Step 2: Navigate to Settings
Click "Settings" or "General" tab

### Step 3: Whitelist IPs Section
Look for "Whitelist IPs" or "Pending IPs" section

### Step 4: Approve Pending IPs
You'll see `172.19.0.1` in pending list
Click "Approve" or move it to the whitelist section

### Step 5: Save Settings
Click "Save" and wait 10 seconds for reload

### Step 6: Test Proxy
```bash
curl -x http://brd-customer-hl_864cf5cf-zone-residential:gkl7gk6qk7s0@localhost:24000 https://lumtest.com/myip.json
```

Should return US IP address (not your local IP)

### Step 7: Test JobSpy with Proxy
```bash
python test_jobspy_linkedin.py
```

Should successfully scrape 10 LinkedIn jobs through proxy

---

## Alternative: Use Without Proxy (Already Working)

JobSpy works perfectly **WITHOUT proxy**:
- ✅ 10 jobs scraped in 30 seconds
- ✅ No rate limiting
- ✅ Free forever
- ✅ Good for 50-200 jobs/session

Just remove proxy from environment:
```bash
unset PROXY_URL
python test_jobspy_linkedin.py
```

---

## Troubleshooting

If web UI still blocks you:
```bash
# Access from inside container
docker exec -it luminati-proxy sh -c "curl http://127.0.0.1:22999"
```

Or check logs:
```bash
docker logs luminati-proxy --tail 50
```
