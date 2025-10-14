# 2-Platform Workflow Executor - EMD Component
# Executes LinkedIn + Naukri scraping with skills extraction
import streamlit as st
from datetime import datetime

from src.scraper.multi_platform_service import scrape_jobs_with_skills


async def execute_scraping_workflow(
    platforms: list[str], job_role: str, location: str, num_jobs: int, db_path: str
) -> None:
    """Execute multi-platform scraping workflow with skills"""
    progress_container = st.container()
    with progress_container:
        st.info(f"🎬 Scraping from {', '.join([p.capitalize() for p in platforms])}...")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        col1, col2 = st.columns(2)
        jobs_metric = col1.empty()
        time_metric = col2.empty()
    
    start_time = datetime.now()
    
    try:
        status_text.write(f"⚡ Initializing scrapers for {', '.join(platforms)}...")
        progress_bar.progress(0.2)
        
        # Call unified scraping service
        jobs = await scrape_jobs_with_skills(
            platforms=platforms,
            keyword=job_role,
            location=location,
            limit=num_jobs,
            store_to_db=True
        )
        
        progress_bar.progress(0.9)
        status_text.write("✅ Scraping completed!")
        
        elapsed = (datetime.now() - start_time).total_seconds()
        jobs_count = len(jobs) if jobs else 0
        
        progress_bar.progress(1.0)
        jobs_metric.metric("Jobs Scraped", jobs_count, "✓ Stored with Skills")
        time_metric.metric("Time", f"{elapsed:.1f}s")
        
        if jobs_count > 0:
            st.success(f"✅ Scraping Complete! Collected {jobs_count} jobs with skills extraction")
            st.balloons()
        else:
            st.warning("⚠️ No jobs found")
    except Exception as error:
        st.error(f"❌ Scraping failed: {str(error)}")
