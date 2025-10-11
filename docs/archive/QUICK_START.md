# Job Scraper - Quick Start Guide

## 🚀 Run the Application

```bash
# Navigate to project directory
cd /mnt/windows_d/Gauravs-Files-and-Folders/Freelance/Codebasics/Job_Scrapper

# Run with absolute path to venv
.venv/bin/streamlit run streamlit_app.py
```

## 🌐 Access the UI

Once running, open your browser to:
- **Local:** http://localhost:8501
- **Network:** Check terminal for network URL

## 📝 How to Use

### 1. Select Platform
Choose from:
- **LinkedIn** - Global job board (49 countries)
- **Indeed** - Global job search engine
- **Naukri** - India's leading job portal

### 2. Enter Job Role
Examples:
- Data Scientist
- Software Engineer
- Python Developer
- Machine Learning Engineer
- Full Stack Developer

### 3. Set Number of Jobs
- Minimum: 5 jobs
- Maximum: 50,000 jobs
- Default: 10 jobs

### 4. Select Countries (LinkedIn/Indeed only)
- Choose from 49 countries
- Use "Select All" for global search
- Or pick specific countries

### 5. Start Scraping
Click "🔍 Start Scraping" and watch:
- Real-time progress updates
- Jobs scraped counter
- Jobs stored counter
- Duplicate detection

## 📊 View Results

### Jobs Tab
- View scraped job listings
- Expandable cards with details
- Skills highlighted
- Direct links to job postings

### Analytics Tab
- Total jobs metrics
- Top companies hiring
- Role distribution
- Skill leaderboard (top 20)
- Interactive charts

## 🔧 Troubleshooting

### Port Already in Use
```bash
.venv/bin/streamlit run streamlit_app.py --server.port 8502
```

### Database Locked
- Close any open SQLite viewers
- Restart the application

### Import Errors
```bash
# Reinstall dependencies
.venv/bin/pip install -r requirements.txt
```

### BrightData API Errors
- Check `.env` file has correct API token
- Verify dataset IDs are correct
- Check rate limits

## 📁 Output Files

### Database
- **Location:** `jobs.db`
- **Format:** SQLite
- **Tables:** jobs (with indexes)

### Logs
- Displayed in terminal
- INFO: Normal operations
- WARNING: Recoverable issues
- ERROR: Critical problems

## 🎯 Sample Queries

### For Data Science Jobs
```
Platform: LinkedIn
Job Role: Data Scientist
Countries: United States, India, United Kingdom
Number of Jobs: 20
```

### For Software Engineering
```
Platform: Indeed
Job Role: Software Engineer
Countries: Canada, Germany, Australia
Number of Jobs: 30
```

### For India-Specific Search
```
Platform: Naukri
Job Role: Python Developer
Number of Jobs: 50
(Countries not needed for Naukri)
```

## 💡 Pro Tips

1. **Start Small:** Begin with 10-20 jobs to test
2. **Use Specific Keywords:** More specific = better results
3. **Check Analytics:** Use the dashboard to identify trends
4. **Monitor Progress:** Watch for duplicates and errors
5. **Save Results:** Database persists across sessions

## 🔐 API Configuration

### BrightData Setup
Already configured in `.env`:
```env
BRIGHTDATA_API_TOKEN=5155712f-1f24-46b1-a954-af64fc007f6e
```

### Dataset IDs
- LinkedIn: `gd_lpfll7v5hcqtkxl6l`
- Indeed: `gd_l4dx9j9sscpvs7no2`

## 📞 Support

### Check These Files
- `SETUP_VERIFICATION.md` - Full verification report
- `README.md` - Project documentation
- `WARP.md` - Development guidelines

### Common Issues Fixed
✅ Import paths corrected
✅ Countries configuration populated
✅ Database schema initialized
✅ All dependencies installed
✅ Platform-specific parameters handled

---

**Status:** ✅ Ready to Run
**Last Updated:** 2025-10-10
**Version:** 1.0.0
