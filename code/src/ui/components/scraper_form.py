# Scraper Form Component - 2-Platform EMD Orchestrator
# LinkedIn + Naukri with multi-layer fuzzy deduplication

import asyncio
import streamlit as st

from .form import render_two_phase_panel, execute_scraping_workflow

def render_scraper_form(db_path: str) -> None:
    """Render the 2-platform scraper form interface"""
    st.header("🚀 2-Platform Job Scraper")
    st.markdown("**LinkedIn** (99.9%+ deduplication) + **Naukri** (Playwright) | Skills extraction included")
    
    # Render 2-platform configuration panel
    platforms, job_role, location, num_jobs, action = render_two_phase_panel(db_path)
    
    # Execute workflow when scrape button clicked
    if action == "scrape":
        asyncio.run(execute_scraping_workflow(
            platforms=platforms,
            job_role=job_role,
            location=location,
            num_jobs=num_jobs,
            db_path=db_path
        ))
