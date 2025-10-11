# Form Configuration Panel - EMD Component
# Handles job role and platform configuration inputs

import streamlit as st
from typing import List

# LinkedIn country options for unified HeadlessX architecture
LINKEDIN_COUNTRIES = [
    "United States", "United Kingdom", "Canada", "Australia", 
    "Germany", "France", "Netherlands", "Singapore", "India"
]

def render_config_panel() -> tuple[str, str, List[str], int]:
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
            options=["Naukri", "LinkedIn", "Indeed"],
            help="⚠️ HeadlessX + Local Luminati Proxy for all platforms"
        )
        
    with col2:
        num_jobs = st.number_input(
            "📊 Number of Jobs",
            min_value=1,
            max_value=100,
            value=10,
            help="Recommended: 10-50 jobs for optimal performance"
        )
        
        selected_countries = []
        if platform == "LinkedIn":
            selected_countries = st.multiselect(
                "🌍 Countries",
                options=LINKEDIN_COUNTRIES,
                default=["United States"],
                help="LinkedIn supports multiple countries"
            )
    
    return job_role, platform, selected_countries, num_jobs
