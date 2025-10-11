#!/bin/bash
# Cleanup Script for Job Scraper Project
# Removes old UI components that are no longer used in v2.0

echo "🧹 Starting cleanup of unused files..."

# Remove all __pycache__ directories
echo "📦 Removing Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
find . -type f -name "*.pyo" -delete 2>/dev/null

# Remove old UI component files (no longer used, everything in streamlit_app.py now)
echo "🗑️  Removing old UI component files (replaced by streamlit_app.py)..."
rm -f src/ui/components/analytics_dashboard.py
rm -f src/ui/components/analytics_helpers.py
rm -f src/ui/components/job_listings.py
rm -f src/ui/components/progress_tracker.py
rm -f src/ui/components/scraper_form.py
rm -f src/ui/components/skill_leaderboard.py
rm -f src/ui/components/__init__.py

# Create a minimal __init__.py to keep src/ui as a valid package
echo "# UI functionality moved to streamlit_app.py" > src/ui/__init__.py

# Remove .pytest_cache if exists
echo "🧪 Removing test cache..."
rm -rf .pytest_cache

# Remove .git files that might be large
echo "🔄 Cleaning git cache..."
rm -rf .git/hooks/fsmonitor--daemon.log 2>/dev/null

# List removed files
echo ""
echo "✅ Cleanup complete!"
echo ""
echo "📋 Summary:"
echo "  ✓ Removed all __pycache__ directories"
echo "  ✓ Removed 6 old UI component files"
echo "  ✓ Removed .pyc/.pyo files"
echo "  ✓ Cleaned test cache"
echo ""
echo "📁 Current structure:"
echo "  • streamlit_app.py - Main app (single file with 2 tabs)"
echo "  • src/db/ - Database layer"
echo "  • src/models.py - JobModel definition"
echo "  • src/scraper/brightdata/ - LinkedIn & Indeed"
echo "  • src/scraper/naukri/ - Naukri scraper"
echo "  • jobs.db - SQLite database"
echo ""
echo "🚀 Ready to run: streamlit run streamlit_app.py"
