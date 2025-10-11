# Scraper Form Component - EMD Orchestrator
# Uses modular form components for clean separation of concerns

import asyncio
import streamlit as st

from .form import render_config_panel, execute_scraping_workflow

def render_scraper_form(db_path: str) -> None:
    """Render the complete scraper form interface"""
    st.header("Job Scraper")
    st.markdown("Configure and run job scraping across multiple platforms")
    
    with st.form("scraper_form"):
        # Render configuration panel
        job_role, platform, selected_countries, num_jobs = render_config_panel()
        
        # Submit button
        submitted = st.form_submit_button(
            "🚀 Start Scraping",
            type="primary",
            help="Begin unified HeadlessX scraping workflow"
        )
    
    # Execute workflow if form submitted
    if submitted:
        asyncio.run(execute_scraping_workflow(
            platform=platform,
            job_role=job_role,
            selected_countries=selected_countries,
            num_jobs=num_jobs,
            db_path=db_path
        ))
