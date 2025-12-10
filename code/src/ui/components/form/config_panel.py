# Form Configuration Panel - EMD Component
# Handles job role and platform configuration inputs

import streamlit as st

def render_config_panel() -> tuple[str, str, int]:
    """Render configuration panel and return form values"""
    col1, col2 = st.columns(2)
    
    with col1:
        job_role = st.text_input(
            "🎯 Job Role",
            value="Data Scientist",
            placeholder="e.g., Data Scientist, AI Engineer, Python Developer"
        )
        platform = st.selectbox(
            "🌐 Platform",
            options=["Naukri", "Indeed"],
            help="Two-phase scraping: URLs first, details later"
        )
        
    with col2:
        num_jobs = st.number_input(
            "📊 Number of Jobs",
            min_value=1,
            max_value=100000,
            value=10,
            help="Scale: 1-100,000 jobs (Recommended: 10-50 for testing, 1000+ for production)"
        )
    
    return job_role, platform, num_jobs
