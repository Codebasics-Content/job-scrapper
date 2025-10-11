# 🔧 BrightData Credentials Error - Fix Guide

## ❌ Error Encountered

```
WebSocket error: wss://brd-customer-hl_xxxxx-zone-scraping_browser1:xxxxx@brd.superproxy.io:9222/ 
403 Auth Failed (wrong_customer_name)
Wrong customer name
```

**Cause:** The `.env` file contains placeholder/example credentials instead of your actual BrightData credentials.

---

## ✅ Solution: Get Your Real BrightData Credentials

### Step 1: Log in to BrightData

1. Go to https://brightdata.com
2. Log in to your account

### Step 2: Get Your Scraping Browser URL

1. Navigate to **"Proxies & Scraping Infrastructure"** or **"Scraping Browser"**
2. Find your **Scraping Browser** zone
3. Look for the **WebSocket URL** (it should start with `wss://`)

**The URL format is:**
```
wss://brd-customer-hl_[YOUR_CUSTOMER_ID]-zone-[YOUR_ZONE]:[YOUR_PASSWORD]@brd.superproxy.io:9222
```

### Step 3: Get Your API Token

1. Go to **Account Settings** → **API Access**
2. Copy your **API Token**
3. If you don't have one, click "Generate New Token"

---

## 📝 Update Your `.env` File

### Current (Wrong - Placeholders):
```env
BRIGHTDATA_API_TOKEN=5155712f-1f24-46b1-a954-af64fc007f6e
BRIGHTDATA_BROWSER_URL=wss://brd-customer-hl_864cf5cf-zone-scraping_browser2:bdx2gk7k5euj@brd.superproxy.io:9222
```

### What You Need to Do:

1. **Open the `.env` file:**
   ```bash
   nano .env
   # or
   vim .env
   ```

2. **Replace with YOUR actual credentials:**
   ```env
   BRIGHTDATA_API_TOKEN=your_actual_api_token_from_dashboard
   BRIGHTDATA_BROWSER_URL=wss://brd-customer-hl_YOUR_ID-zone-YOUR_ZONE:YOUR_PASSWORD@brd.superproxy.io:9222
   ```

3. **Save the file** (Ctrl+X, then Y in nano)

---

## 🧪 Verify Your Credentials

### Test 1: Check Environment Variables Load

```bash
python3 -c "from src.scraper.brightdata.config.settings import get_settings; s = get_settings(); print(f'API Token: {s.api_token[:20]}...'); print(f'Browser URL: {s.browser_url[:50]}...')"
```

**Expected output:**
```
✅ Loaded environment variables from: /path/to/.env
API Token: your_actual_token...
Browser URL: wss://brd-customer-hl_YOUR_ID-zone-...
```

### Test 2: Try Connecting to BrightData

```bash
streamlit run streamlit_app.py
```

Then try scraping. If credentials are correct, you should see:
```
✅ Connected to BrightData Scraping Browser
```

---

## 🔍 Common Issues & Solutions

### Issue 1: "Auth Failed (wrong_customer_name)"

**Cause:** Wrong customer ID in the URL

**Solution:** 
- Copy the EXACT URL from BrightData dashboard
- Don't modify any part of it
- Make sure there are no extra spaces

### Issue 2: "Auth Failed (wrong_password)"

**Cause:** Wrong password in the URL

**Solution:**
- Get a fresh URL from BrightData dashboard
- Password is embedded in the URL (after the zone name)

### Issue 3: "Zone not found"

**Cause:** Wrong zone name

**Solution:**
- Verify the zone name in BrightData dashboard
- Common zones: `scraping_browser1`, `scraping_browser2`
- Use the exact name from your dashboard

### Issue 4: URL format is wrong

**Correct format:**
```
wss://brd-customer-hl_[CUSTOMER_ID]-zone-[ZONE_NAME]:[PASSWORD]@brd.superproxy.io:9222
```

**Parts explained:**
- `hl_[CUSTOMER_ID]` - Your unique customer ID (starts with `hl_`)
- `zone-[ZONE_NAME]` - Your scraping browser zone name
- `:[PASSWORD]` - Your zone password (after the colon)
- `@brd.superproxy.io:9222` - BrightData server (don't change this)

---

## 📋 Quick Checklist

- [ ] Logged in to BrightData dashboard
- [ ] Copied WebSocket URL from Scraping Browser section
- [ ] Copied API Token from account settings
- [ ] Updated `.env` file with real credentials
- [ ] No extra spaces or line breaks in `.env`
- [ ] Saved the `.env` file
- [ ] Restarted the Streamlit app

---

## 🎯 Where to Find Your Credentials

### BrightData Dashboard Navigation:

1. **For Scraping Browser URL:**
   ```
   Dashboard → Proxies & Scraping Infrastructure → Scraping Browser → 
   Your Zone → Connection Parameters → WebSocket URL
   ```

2. **For API Token:**
   ```
   Dashboard → Account Settings → API Access → API Token
   ```

### What It Should Look Like:

**WebSocket URL (in dashboard):**
```
wss://brd-customer-hl_a1b2c3d4e5f6-zone-scraping_browser1:myp4ssw0rd@brd.superproxy.io:9222
```

**API Token (in dashboard):**
```
abc12345-6789-def0-1234-56789abcdef0
```

---

## 🚨 Security Note

**NEVER share or commit your actual credentials!**

- ✅ `.env` is already in `.gitignore`
- ✅ Don't post credentials in issues/forums
- ✅ Don't share screenshots with visible credentials
- ✅ Rotate credentials if accidentally exposed

---

## 💡 Still Having Issues?

### Check Your BrightData Account:

1. **Is your account active?**
   - Log in to BrightData dashboard
   - Check if your subscription is active
   - Verify you have credits available

2. **Is the Scraping Browser zone active?**
   - Go to Scraping Browser section
   - Check zone status (should be "Active")
   - If inactive, activate it

3. **Test with BrightData's built-in test:**
   - Most zones have a "Test" button in dashboard
   - Click it to verify the zone works

### Contact Support:

If credentials are correct but still failing:
- **BrightData Support:** support@brightdata.com
- **Check:** https://docs.brightdata.com
- **Status Page:** https://status.brightdata.com

---

## ✅ Success Indicators

When credentials are correct, you'll see:

```bash
$ streamlit run streamlit_app.py

✅ Loaded environment variables from: /path/to/.env
✅ BrightData browser client initialized
🔌 Connecting to BrightData Scraping Browser...
✅ Connected to BrightData Scraping Browser
🔍 Starting LinkedIn scrape: keyword='AI Engineer'...
```

---

## 📝 Summary

**The Issue:**
- `.env` file has placeholder credentials
- Need to replace with YOUR actual BrightData credentials

**The Fix:**
1. Log in to BrightData dashboard
2. Copy your WebSocket URL and API Token
3. Update `.env` file with real values
4. Restart the app

**Test Command:**
```bash
python3 -c "from src.scraper.brightdata.config.settings import get_settings; get_settings()"
```

Should show:
```
✅ Loaded environment variables from: /path/to/.env
```

---

**Get your real credentials from BrightData dashboard and update `.env`! 🔑**
