# 🚀 Quick Start Guide - BrightData Job Scraper

## Prerequisites

### 1. BrightData Credentials
Set these environment variables:
```bash
export BRIGHTDATA_API_TOKEN="your_api_token"
export BRIGHTDATA_BROWSER_URL="wss://brd-customer-hl_xxxxx-zone-scraping_browser1:xxxxx@brd.superproxy.io:9222"
```

**Get these from BrightData:**
1. Log in to https://brightdata.com
2. Go to "Scraping Browser" section
3. Copy your WebSocket URL → `BRIGHTDATA_BROWSER_URL`
4. Get API token from account settings → `BRIGHTDATA_API_TOKEN`

### 2. Python Dependencies
```bash
pip install streamlit playwright pandas numpy aiohttp
playwright install chromium
```

---

## Running the Application

### Start Streamlit Dashboard:
```bash
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`

---

## Using the Dashboard

### 📝 **Scraper Tab** (Tab 1)
1. **Enter Job Role**: e.g., "Data Scientist", "Python Developer"
2. **Select Platform**: 
   - **Naukri** (Recommended - reliable, no extra setup)
   - **LinkedIn** (Requires BrightData setup)
   - **Indeed** (Requires BrightData setup)
3. **Set Number of Jobs**: 5-1000 jobs
4. **Select Countries** (LinkedIn/Indeed only)
5. **Click "Start Scraping"** - Jobs will be scraped and saved to SQLite

### 📊 **Analytics Dashboard** (Tab 2)
View comprehensive insights from scraped data:

#### **Overview Section**
- Total jobs, companies, roles, avg skills per job

#### **Platform Distribution**
- Bar chart showing jobs per platform

#### **Top Companies**
- Top 20 companies hiring

#### **Top Skills** (3 Tabs)
1. **📊 Bar Chart**: All top 20 skills with percentages
2. **🥧 Top 10 Pie**: Visual distribution of top skills
3. **📈 Table View**: Detailed leaderboard with counts

#### **Job Role Analysis** (3 Tabs)
1. **📊 Role Distribution**: Top 15 job roles by count
2. **🎯 Skills by Role**: Comparative skill demand across roles
3. **🔥 Role-Skill Matrix**: Heatmap showing skill-role correlations

#### **Location Distribution**
- Top 15 hiring locations

#### **Recent Jobs Table**
- Last 50 scraped jobs

#### **Export Data**
- Download as CSV or JSON

---

## Platform-Specific Notes

### 🇮🇳 **Naukri** (Recommended)
- ✅ **Most Reliable**: Works consistently with BrightData
- ✅ **No Extra Setup**: Just needs BrightData credentials
- ✅ **Bypasses reCAPTCHA**: BrightData handles all protections
- ⚡ **Fast**: ~10-20 seconds for 20 jobs

**Best For:** Testing, reliable production scraping

### 💼 **LinkedIn**
- ⚡ **Optimized**: 5-6x faster than before (removed slow clicks)
- 🌍 **Multi-Country**: Scrapes across selected countries
- 📊 **Rich Data**: Detailed job information
- ⏱️ **Speed**: ~10-20 seconds for 20 jobs

**Note:** Requires BrightData Scraping Browser configured for LinkedIn

### 🔍 **Indeed**
- 🌐 **Global Coverage**: Works across countries
- 📝 **Job Listings**: Good for market analysis
- ⏱️ **Speed**: ~15-25 seconds for 20 jobs

**Note:** Requires BrightData Scraping Browser configured for Indeed

---

## Architecture Overview

```
User → Streamlit UI → Platform Selector
                            ↓
            ┌──────────────┼──────────────┐
            ↓              ↓              ↓
        Naukri        LinkedIn        Indeed
            ↓              ↓              ↓
    BrightData     BrightData     BrightData
      Browser        Browser        Browser
            ↓              ↓              ↓
        ────────────────────────────────────
                      ↓
                SQLite Database
                      ↓
              Analytics Dashboard
```

**Key Point:** All platforms use **BrightData** - no manual scraping!

---

## Troubleshooting

### Issue: "BrightData connection failed"
**Solution:** Check environment variables are set correctly

### Issue: "No jobs found"
**Solutions:**
- Try different keywords (more general)
- Check platform availability for selected country
- Verify BrightData account has active credits

### Issue: "Scraping too slow"
**Solutions:**
- Reduce number of jobs to scrape
- Use Naukri (fastest platform)
- Check internet connection speed

### Issue: "Charts not displaying"
**Solutions:**
- Ensure jobs are scraped first
- Refresh the Analytics Dashboard tab
- Check browser console for errors

---

## Performance Tips

### 🚀 **Fastest Setup:**
1. Use **Naukri** platform
2. Scrape **20-50 jobs** at a time
3. Focus on specific, popular roles

### 📊 **Best Analytics:**
1. Scrape from **multiple platforms**
2. Collect **100+ jobs** for meaningful insights
3. Use **Role-Skill Matrix** to find correlations

### 💾 **Database Management:**
- Database: `jobs.db` (SQLite)
- Location: Project root directory
- Backup: Copy `jobs.db` file periodically

---

## Example Workflows

### 🎯 **Workflow 1: Quick Market Research**
```
1. Scraper Tab → Naukri → "Data Scientist" → 50 jobs → Scrape
2. Analytics Tab → Top Skills → View bar chart
3. Analytics Tab → Role-Skill Matrix → Identify key skills
```

### 📈 **Workflow 2: Comprehensive Analysis**
```
1. Scrape Naukri: "Python Developer" → 100 jobs
2. Scrape LinkedIn: "Python Developer" → 50 jobs
3. Scrape Indeed: "Python Developer" → 50 jobs
4. Analytics Tab → Compare platforms
5. Export data as CSV for further analysis
```

### 🔍 **Workflow 3: Role Comparison**
```
1. Scrape multiple roles: "Data Scientist", "ML Engineer", "AI Engineer"
2. Analytics Tab → Role Analysis → Skills by Role
3. View stacked bar chart to compare skill requirements
```

---

## Key Features

✅ **100% BrightData** - Reliable, fast, bypasses all protections  
✅ **3 Platforms** - Naukri, LinkedIn, Indeed  
✅ **Advanced Charts** - 6 different visualization types  
✅ **Role Analysis** - Compare skills across job roles  
✅ **Heatmap** - Skill-role correlation matrix  
✅ **Export** - CSV/JSON download  
✅ **Real-time** - Live scraping with progress bars  
✅ **SQLite Storage** - Persistent data storage  

---

## Next Steps

1. ✅ **Test the scraper** with Naukri (most reliable)
2. ✅ **Explore analytics** with different chart tabs
3. ✅ **Export data** for external analysis
4. 🔜 **Add more platforms** (optional)
5. 🔜 **Track trends over time** (future enhancement)

---

## Support

- **Documentation**: See `BRIGHTDATA_MIGRATION_SUMMARY.md`
- **Issues**: Check Troubleshooting section above
- **BrightData Docs**: https://docs.brightdata.com

---

**Happy Scraping! 🎉**
