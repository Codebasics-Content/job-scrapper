# Two-Phase Workflow Executor - EMD Component
# Handles Phase 1 (URL) and Phase 2 (Details) scraping with progress
import streamlit as st
from datetime import datetime

from src.models import JobUrlModel
from src.scraper.unified.naukri_unified import scrape_naukri_urls, scrape_naukri_details
from src.db import JobStorageOperations


async def execute_phase1_workflow(
    platform: str, job_role: str, location: str, num_jobs: int, db_path: str
) -> None:
    """Execute Phase 1: URL collection workflow"""
    progress_container = st.container()
    with progress_container:
        st.info(f"🎬 Phase 1: Collecting URLs from {platform}...")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        col1, col2 = st.columns(2)
        urls_metric = col1.empty()
        time_metric = col2.empty()
    
    start_time = datetime.now()
    
    try:
        status_text.write(f"⚡ Initializing Playwright for {platform}...")
        progress_bar.progress(0.2)
        
        if platform.lower() == "naukri":
            url_models = await scrape_naukri_urls(
                keyword=job_role,
                location=location,
                limit=num_jobs,
                store_to_db=True
            )
        else:
            st.warning("⚠️ Indeed two-phase scraper coming soon!")
            return
        
        progress_bar.progress(0.8)
        
        elapsed = (datetime.now() - start_time).total_seconds()
        progress_bar.progress(1.0)
        urls_metric.metric("URLs Collected", len(url_models), "✓ Stored")
        time_metric.metric("Time", f"{elapsed:.1f}s")
        
        if len(url_models) > 0:
            st.success(f"✅ Phase 1 Complete! Collected {len(url_models)} URLs")
            st.info(f"💡 **Next Step:** Run Phase 2 to scrape full details")
            st.balloons()
        else:
            st.warning("⚠️ No new URLs found")
    except Exception as error:
        st.error(f"❌ Phase 1 failed: {str(error)}")


async def execute_phase2_workflow(
    platform: str, job_role: str, num_jobs: int, db_path: str
) -> None:
    """Execute Phase 2: Detail scraping workflow"""
    progress_container = st.container()
    with progress_container:
        st.info(f"🎬 Phase 2: Scraping details from {platform}...")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        col1, col2 = st.columns(2)
        details_metric = col1.empty()
        time_metric = col2.empty()
    
    start_time = datetime.now()
    input_role = JobUrlModel.normalize_role(job_role)
    
    try:
        status_text.write(f"⚡ Querying unscraped URLs...")
        progress_bar.progress(0.2)
        
        if platform.lower() == "naukri":
            detail_models = await scrape_naukri_details(
                platform=platform,
                input_role=input_role,
                limit=num_jobs,
                store_to_db=True
            )
        else:
            st.warning("⚠️ Indeed two-phase scraper coming soon!")
            return
        
        progress_bar.progress(0.9)
        
        elapsed = (datetime.now() - start_time).total_seconds()
        progress_bar.progress(1.0)
        details_metric.metric("Details Scraped", len(detail_models), "✓ Stored")
        time_metric.metric("Time", f"{elapsed:.1f}s")
        
        if len(detail_models) > 0:
            st.success(f"✅ Phase 2 Complete! Scraped {len(detail_models)} job details")
            st.balloons()
        else:
            st.warning("⚠️ No unscraped jobs found or all failed")
    except Exception as error:
        st.error(f"❌ Phase 2 failed: {str(error)}")
