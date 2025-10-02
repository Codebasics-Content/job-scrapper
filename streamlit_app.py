# Job Scraper - Modern Streamlit Application (EMD: ≤80 lines)
import streamlit as st
import asyncio
import logging
from src.scraper.linkedin.scraper import LinkedInScraper
from src.scraper.naukri.browser_scraper import NaukriBrowserScraper
from src.db import DatabaseConnection, SchemaManager, JobStorageOperations
from src.ui.components import (render_scraper_form, ProgressTracker, render_job_listings,
                                render_analytics_dashboard)

logging.basicConfig(level=logging.INFO)
DB_PATH = "jobs.db"

# Initialize database
SchemaManager(DatabaseConnection(db_path=DB_PATH)).initialize_schema()

# Page configuration
st.set_page_config(page_title="Job Scraper", page_icon="🔍", layout="wide")
st.title("🔍 Job Scraper with Skill Analysis")

# Handle form submission
form_data = render_scraper_form()

if form_data:
    # Select scraper based on platform
    if form_data["platform"] == "LinkedIn":
        scraper = LinkedInScraper()
    elif form_data["platform"] == "Naukri":
        scraper = NaukriBrowserScraper()
    else:
        st.error(f"Unsupported platform: {form_data['platform']}")
        st.stop()
    
    storage_ops = JobStorageOperations(DB_PATH)
    tracker = ProgressTracker(form_data["num_jobs"], len(form_data["countries"]))
    
    try:
        tracker.update_loading(form_data["platform"])
        tracker.update_scraping()
        
        # LinkedIn uses countries, Naukri uses single location
        if form_data["platform"] == "LinkedIn":
            scraped_jobs = asyncio.run(scraper.scrape_jobs(
                job_role=form_data["job_role"],
                target_count=form_data["num_jobs"],
                countries=form_data["countries"]
            ))
        else:  # Naukri
            scraped_jobs = asyncio.run(scraper.scrape_jobs(
                job_role=form_data["job_role"],
                target_count=form_data["num_jobs"]
            ))
        
        tracker.update_scraped(len(scraped_jobs))
        stored_count = storage_ops.store_jobs(scraped_jobs)
        tracker.update_complete(len(scraped_jobs), stored_count)
        
        st.session_state['last_scraped_jobs'] = scraped_jobs
        
    except Exception as error:
        tracker.update_error(str(error))
        logging.error(f"Scraping error: {error}", exc_info=True)

# Render tabs
if 'last_scraped_jobs' in st.session_state or st.button("📊 Load from Database"):
    tab1, tab2 = st.tabs(["📋 Jobs", "📈 Analytics"])
    
    with tab1:
        if 'last_scraped_jobs' in st.session_state:
            render_job_listings(st.session_state['last_scraped_jobs'])
    
    with tab2:
        render_analytics_dashboard(DB_PATH)
