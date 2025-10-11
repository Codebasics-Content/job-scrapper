# Overview Metrics Component - EMD Architecture
# Renders job overview metrics and statistics

import streamlit as st
import pandas as pd
from typing import List, Dict, Any

def render_analytics_overview(all_jobs: List[Dict[str, Any]]) -> None:
    """Render overview metrics section"""
    if not all_jobs:
        st.info("📭 No data available yet. Please scrape some jobs first!")
        return
    
    df = pd.DataFrame(all_jobs)
    total_jobs = len(df)
    
    st.subheader("📈 Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Jobs", f"{total_jobs:,}")
    with col2:
        unique_companies = df['company'].nunique()
        st.metric("Companies", f"{unique_companies:,}")
    with col3:
        unique_roles = df['job_role'].nunique()
        st.metric("Unique Roles", f"{unique_roles:,}")
    with col4:
        skills_counts = df['skills'].str.split(',').str.len()
        avg_skills = skills_counts.mean()
        st.metric("Avg Skills/Job", f"{avg_skills:.1f}")
