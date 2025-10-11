# Workflow Execution Component - EMD Component
# Handles async scraping workflow with progress tracking

import streamlit as st
from typing import List
from datetime import datetime

from src.models import JobModel
from src.db import JobStorageOperations
from src.scraper.unified.service import scrape_jobs

async def execute_scraping_workflow(
    platform: str, 
    job_role: str, 
    selected_countries: List[str], 
    num_jobs: int,
    db_path: str
) -> None:
    """Execute the unified scraping workflow with progress tracking"""
    progress_container = st.container()
    with progress_container:
        st.info(f"🎬 Initializing {platform} scraper...")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Create metrics columns
        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
        scraped_metric = metrics_col1.empty()
        stored_metric = metrics_col2.empty()
        time_metric = metrics_col3.empty()
    
    start_time = datetime.now()
    jobs: List[JobModel] = []
    
    try:
        status_text.write(f"⚡ Initializing HeadlessX renderer and local proxy for {platform}...")
        progress_bar.progress(0.1)

        target_location = (
            "India" if platform == "Naukri" else (selected_countries[0] if selected_countries else "United States")
        )

        status_text.write(f"🔍 Scraping {num_jobs} jobs from {platform}...")
        progress_bar.progress(0.3)

        platform_key = platform.lower()
        jobs = await scrape_jobs(
            platform=platform_key,
            keyword=job_role,
            location=target_location,
            limit=num_jobs,
        )

        scraped_metric.metric("Jobs Scraped", len(jobs))
        progress_bar.progress(0.7)
        
        status_text.write("💾 Storing jobs in database...")
        progress_bar.progress(0.9)
        
        db_ops = JobStorageOperations(db_path)
        stored_count = db_ops.store_jobs(jobs)
        
        elapsed = (datetime.now() - start_time).total_seconds()
        progress_bar.progress(1.0)
        scraped_metric.metric("Jobs Scraped", len(jobs), "✓ Complete")
        stored_metric.metric("Jobs Stored", stored_count, f"{len(jobs) - stored_count} duplicates")
        time_metric.metric("Time Taken", f"{elapsed:.1f}s")
        
        if stored_count > 0:
            st.success(f"✅ Successfully scraped and stored {stored_count} jobs!")
            st.balloons()
        else:
            st.warning("⚠️ All jobs were duplicates. Database not updated.")
            
    except Exception as error:
        st.error(f"❌ Unified scraping failed: {str(error)}")
