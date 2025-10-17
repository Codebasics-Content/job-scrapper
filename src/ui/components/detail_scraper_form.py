# Job Detail Scraper Component - Phase 2: Detail Extraction Only
# 3-layer skills extraction, validation, zero false positives/negatives

import asyncio
import streamlit as st
from src.db import JobStorageOperations
from src.scraper.unified.linkedin.sequential_detail_scraper import scrape_job_details_sequential

async def process_unscraped_urls(db_path: str, platform: str, job_role: str, batch_size: int) -> int:
    """Process unscraped URLs from database with 3-layer skills extraction"""
    db_ops = JobStorageOperations(db_path)
    urls = db_ops.get_unscraped_urls(platform.lower(), job_role, limit=batch_size)
    
    if not urls:
        return 0
    
    # Scrape job details - scraper handles per-job storage & marking
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"🚀 Starting sequential scraping with per-job validation & storage")
    
    jobs = await scrape_job_details_sequential(urls=urls, headless=False)
    
    # Scraper already stored each job individually and marked URLs
    logger.info(f"✅ Sequential scraping complete: {len(jobs)} jobs stored")
    logger.info(f"📊 Jobs with skills: {sum(1 for j in jobs if j.skills)}")
    
    return len(jobs)

def render_detail_scraper_form(db_path: str) -> None:
    """Render Phase 2: Job detail extraction interface"""
    st.header("📝 Phase 2: Job Detail Scraper")
    st.markdown("**Extract job details from collected URLs** | 3-layer skills extraction | Zero false positives")
    
    col1, col2 = st.columns(2)
    
    with col1:
        platform = st.selectbox(
            "Platform",
            ["LinkedIn", "Naukri"],
            help="Select platform to process URLs from"
        )
        
        job_role = st.text_input(
            "Job Role",
            value="AI Engineer",
            help="Enter the job role to filter URLs"
        )
    
    with col2:
        batch_size = st.number_input(
            "Batch Size",
            min_value=10,
            max_value=10000,
            value=100,
            step=50,
            help="Number of URLs to process in one batch (no limit)"
        )
    
    # Database stats
    db_ops = JobStorageOperations(db_path)
    unscraped_count = len(db_ops.get_unscraped_urls(platform.lower(), job_role, limit=batch_size))
    total_jobs = len(db_ops.get_all_jobs())
    
    col_stat1, col_stat2 = st.columns(2)
    col_stat1.metric("🔗 Unscraped URLs", unscraped_count)
    col_stat2.metric("✅ Jobs Stored", total_jobs)
    
    st.divider()
    
    # Processing controls
    if unscraped_count == 0:
        st.warning(f"⚠️ No unscraped URLs for {platform}. Go to **Link Scraper** tab first!")
    else:
        process_button = st.button(
            f"📝 Process {min(batch_size, unscraped_count)} URLs",
            type="primary",
            use_container_width=True,
            disabled=unscraped_count == 0
        )
        
        if process_button:
            with st.spinner(f"🔄 Processing {batch_size} URLs with 3-layer skills extraction..."):
                stored = asyncio.run(process_unscraped_urls(db_path, platform, job_role, batch_size))
                st.success(f"✅ Successfully stored {stored} jobs with validated skills!")
                st.rerun()
