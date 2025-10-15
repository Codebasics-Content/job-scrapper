# 2-Platform Scraper Configuration Panel - EMD Component
# LinkedIn + Naukri with multi-layer fuzzy deduplication
import streamlit as st
from src.db import JobStorageOperations


def render_two_phase_panel(db_path: str) -> tuple[list[str], str, str, int, str]:
    """Render 2-platform scraper configuration panel"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⚙️ Configuration")
        platforms = st.multiselect(
            "Platforms",
            ["linkedin", "naukri"],
            default=["linkedin"],
            help="Select platforms to scrape (LinkedIn with deduplication, Naukri with Playwright)"
        )
        job_role = st.text_input(
            "Job Role",
            value="AI Engineer",
            help="Job title to search for"
        )
        location = st.text_input(
            "Location",
            value="",
            help="Leave empty for worldwide jobs (recommended for LinkedIn)"
        )
        num_jobs = st.number_input(
            "Jobs per Platform",
            min_value=1,
            max_value=100000,
            value=100,
            step=10,
            help="Number of jobs to scrape per platform"
        )
    
    with col2:
        st.markdown("### 📊 Database Status")
        db_ops = JobStorageOperations(db_path)
        
        # Query total jobs in database
        all_jobs = db_ops.get_all_jobs()
        total_count = len(all_jobs)
        
        # Count by platform
        linkedin_count = len([j for j in all_jobs if j.get('platform', '').lower() == 'linkedin'])
        naukri_count = len([j for j in all_jobs if j.get('platform', '').lower() == 'naukri'])
        
        st.metric("Total Jobs", total_count, help="Total jobs in database")
        st.info(f"**LinkedIn:** {linkedin_count} | **Naukri:** {naukri_count}")
    
    st.divider()
    
    # Scrape button
    scrape_clicked = st.button(
        "🚀 Start Scraping",
        type="primary",
        use_container_width=True,
        help="Scrape jobs with skills from selected platforms",
        disabled=len(platforms) == 0
    )
    
    action = "scrape" if scrape_clicked else "none"
    
    return platforms, job_role, location, num_jobs, action
