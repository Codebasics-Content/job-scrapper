# Job Scraper - Modern Streamlit Application (EMD: ≤80 lines)
import asyncio
import logging
from typing import cast

import streamlit as st
from src.scraper.linkedin.scraper import LinkedInScraper
from src.scraper.naukri.browser_scraper import NaukriBrowserScraper, NaukriBrowserManager
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
    # Type-safe access to form data
    job_role = cast(str, form_data["job_role"])
    platform = cast(str, form_data["platform"])
    num_jobs = cast(int, form_data["num_jobs"])
    countries = cast(list[dict[str, str]], form_data.get("countries", []))

    # Select scraper based on platform
    if platform == "LinkedIn":
        scraper = LinkedInScraper()
    elif platform == "Naukri":
        browser_manager = NaukriBrowserManager()
        scraper = NaukriBrowserScraper(browser_manager)
    else:
        st.error(f"Unsupported platform: {platform}")
        st.stop()

    # Progress tracking
    progress_tracker = ProgressTracker(
        target_count=num_jobs,
        num_countries=len(countries) if countries else 1
    )

    async def scrape_jobs():
        try:
            progress_tracker.update_loading(platform)
            
            if platform == "LinkedIn":
                jobs = await scraper.scrape_jobs(
                    job_role=job_role, 
                    target_count=num_jobs, 
                    countries=countries
                )
            else:  # Naukri
                jobs = await scraper.scrape_jobs(
                    job_role=job_role, 
                    target_count=num_jobs
                )
            
            progress_tracker.update_scraped(len(jobs))
            
            # Store in database
            db_ops = JobStorageOperations(DB_PATH)
            stored_count = db_ops.store_jobs(jobs)
            
            progress_tracker.update_complete(len(jobs), stored_count)
            
            # Update session state
            st.session_state["scraped_jobs"] = jobs
            
        except Exception as error:
            progress_tracker.update_error(str(error))

    if st.button("🔍 Start Scraping", type="primary"):
        asyncio.run(scrape_jobs())

# Display results using existing UI components
if "scraped_jobs" in st.session_state:
    tab1, tab2 = st.tabs(["📋 Jobs", "📈 Analytics"])
    
    with tab1:
        render_job_listings(st.session_state["scraped_jobs"])
    
    with tab2:
        render_analytics_dashboard(DB_PATH)
