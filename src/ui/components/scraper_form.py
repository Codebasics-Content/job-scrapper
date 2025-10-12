# Scraper Form Component - Two-Phase EMD Orchestrator
# Uses modular two-phase components for 80-90% speedup

import asyncio
import streamlit as st

from .form import render_two_phase_panel, execute_phase1_workflow, execute_phase2_workflow

def render_scraper_form(db_path: str) -> None:
    """Render the two-phase scraper form interface"""
    st.header("🚀 Two-Phase Job Scraper")
    st.markdown("**80-90% faster** through URL caching | Scrape URLs first, details later")
    
    # Render two-phase configuration panel
    platform, job_role, location, num_jobs, phase = render_two_phase_panel(db_path)
    
    # Execute workflow based on phase button clicked
    if phase == "phase1":
        asyncio.run(execute_phase1_workflow(
            platform=platform,
            job_role=job_role,
            location=location,
            num_jobs=num_jobs,
            db_path=db_path
        ))
    elif phase == "phase2":
        asyncio.run(execute_phase2_workflow(
            platform=platform,
            job_role=job_role,
            num_jobs=num_jobs,
            db_path=db_path
        ))
