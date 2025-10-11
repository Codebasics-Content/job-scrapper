# 🔐 Environment Variables Setup Guide

## Required Environment Variables

This application requires **only 2 environment variables** to work with BrightData:

```bash
BRIGHTDATA_API_TOKEN=your_api_token_here
BRIGHTDATA_BROWSER_URL=wss://brd-customer-hl_xxxxx-zone-scraping_browser1:xxxxx@brd.superproxy.io:9222
```

---

## 📝 How to Get These Values

### Step 1: Log in to BrightData
1. Go to https://brightdata.com
2. Log in to your account

### Step 2: Get Your Scraping Browser URL
1. Navigate to **"Proxies & Scraping Infrastructure"** or **"Scraping Browser"**
2. Find your **Scraping Browser** zone
3. Look for the **WebSocket URL** (starts with `wss://`)
4. Copy the full URL → This is your `BRIGHTDATA_BROWSER_URL`

**Format:**
```
wss://brd-customer-hl_[CUSTOMER_ID]-zone-scraping_browser1:[PASSWORD]@brd.superproxy.io:9222
```

### Step 3: Get Your API Token
1. Go to **Account Settings** or **API Access**
2. Find your **API Token** or generate a new one
3. Copy the token → This is your `BRIGHTDATA_API_TOKEN`

---

## 🛠️ Setting Up Environment Variables

### Option 1: Using `.env` File (Recommended)

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file:**
   ```bash
   nano .env
   # or
   vim .env
   # or use any text editor
   ```

3. **Add your actual values:**
   ```env
   BRIGHTDATA_API_TOKEN=abc123xyz456
   BRIGHTDATA_BROWSER_URL=wss://brd-customer-hl_12345-zone-scraping_browser1:mypassword@brd.superproxy.io:9222
   ```

4. **Save and close the file**

5. **The app will automatically load `.env` when you run it** ✅

---

### Option 2: Export in Terminal Session

For temporary use (lasts only for current terminal session):

```bash
export BRIGHTDATA_API_TOKEN="your_api_token"
export BRIGHTDATA_BROWSER_URL="wss://brd-customer-hl_xxxxx-zone-scraping_browser1:xxxxx@brd.superproxy.io:9222"
```

Then run the app:
```bash
streamlit run streamlit_app.py
```

---

### Option 3: Add to Shell Profile (Permanent)

To make these permanent across all terminal sessions:

#### For Bash (Linux/Mac):
```bash
echo 'export BRIGHTDATA_API_TOKEN="your_api_token"' >> ~/.bashrc
echo 'export BRIGHTDATA_BROWSER_URL="wss://brd-customer-..."' >> ~/.bashrc
source ~/.bashrc
```

#### For Zsh (Mac):
```bash
echo 'export BRIGHTDATA_API_TOKEN="your_api_token"' >> ~/.zshrc
echo 'export BRIGHTDATA_BROWSER_URL="wss://brd-customer-..."' >> ~/.zshrc
source ~/.zshrc
```

#### For Windows PowerShell:
```powershell
[System.Environment]::SetEnvironmentVariable('BRIGHTDATA_API_TOKEN', 'your_api_token', 'User')
[System.Environment]::SetEnvironmentVariable('BRIGHTDATA_BROWSER_URL', 'wss://brd-customer-...', 'User')
```

---

## ✅ Verifying Your Setup

### Quick Test:
```bash
python -c "
import os
print('API Token:', os.getenv('BRIGHTDATA_API_TOKEN', 'NOT SET'))
print('Browser URL:', os.getenv('BRIGHTDATA_BROWSER_URL', 'NOT SET')[:30] + '...' if os.getenv('BRIGHTDATA_BROWSER_URL') else 'NOT SET')
"
```

**Expected Output:**
```
API Token: abc123xyz456
Browser URL: wss://brd-customer-hl_12345-...
```

### Run the App:
```bash
streamlit run streamlit_app.py
```

**If environment variables are missing, you'll see:**
```
ValueError: BRIGHTDATA_API_TOKEN environment variable is required.
```

**If everything is correct, you'll see:**
```
✅ BrightData browser client initialized
```

---

## 🔒 Security Best Practices

### DO ✅
- ✅ Store credentials in `.env` file (already in `.gitignore`)
- ✅ Use environment variables for credentials
- ✅ Keep your API token private
- ✅ Rotate tokens periodically

### DON'T ❌
- ❌ Commit `.env` file to Git
- ❌ Share your `BRIGHTDATA_BROWSER_URL` (contains password!)
- ❌ Hardcode credentials in Python files
- ❌ Post credentials in public forums/issues

---

## 🐛 Troubleshooting

### Problem: "BRIGHTDATA_API_TOKEN environment variable is required"

**Solution:**
1. Check if `.env` file exists: `ls -la .env`
2. Verify file contains: `cat .env`
3. Ensure no typos in variable names (case-sensitive!)
4. Try Option 2 (export in terminal) as a test

### Problem: "BRIGHTDATA_BROWSER_URL not configured"

**Solution:**
1. Verify the URL format starts with `wss://`
2. Ensure URL includes password component
3. No extra spaces or quotes in `.env` file
4. URL should be one continuous string (no line breaks)

### Problem: "Connection failed" or "Browser won't connect"

**Solution:**
1. Check if BrightData account has active credits
2. Verify the Scraping Browser zone is active
3. Test URL in BrightData dashboard first
4. Check your internet connection
5. Ensure no firewall blocking WebSocket connections

### Problem: ".env file not loading"

**Solution:**
1. Verify `.env` is in project root directory (same level as `streamlit_app.py`)
2. Check file has no extension (not `.env.txt`)
3. Ensure proper formatting: `KEY=value` (no spaces around `=`)
4. Try absolute path in code: `env_file="/full/path/to/.env"`

---

## 📋 Example `.env` File

```env
# BrightData Configuration
BRIGHTDATA_API_TOKEN=abc123xyz789
BRIGHTDATA_BROWSER_URL=wss://brd-customer-hl_a1b2c3d4-zone-scraping_browser1:mypassword123@brd.superproxy.io:9222

# Optional: Other app settings (if needed)
# LOG_LEVEL=INFO
# DATABASE_PATH=jobs.db
```

---

## 🎯 Why Only These Two Variables?

### **Old Approach** (Not Used):
```bash
BRIGHTDATA_USERNAME=user@example.com
BRIGHTDATA_PASSWORD=password123
BRIGHTDATA_ZONE=scraping_browser1
```
Required 3+ variables and manual authentication flow.

### **New Approach** (Current):
```bash
BRIGHTDATA_API_TOKEN=token123
BRIGHTDATA_BROWSER_URL=wss://...
```
✅ Direct WebSocket connection  
✅ Authentication embedded in URL  
✅ Simpler setup  
✅ Faster connection  

---

## 📞 Need Help?

1. **BrightData Docs**: https://docs.brightdata.com
2. **BrightData Support**: support@brightdata.com
3. **Check logs**: Run `streamlit run streamlit_app.py` and read error messages
4. **Verify credentials**: Log in to BrightData dashboard

---

## ✨ Summary

**Required Variables:**
- `BRIGHTDATA_API_TOKEN` - Your API token
- `BRIGHTDATA_BROWSER_URL` - WebSocket URL (starts with `wss://`)

**Setup Method:**
1. Create `.env` file in project root
2. Add both variables
3. Run `streamlit run streamlit_app.py`
4. Start scraping! 🚀

---

**That's it! Just 2 environment variables and you're ready to scrape! 🎉**
