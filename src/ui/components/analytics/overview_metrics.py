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
        unique_companies = df['platform'].nunique()
        st.metric("Platforms", f"{unique_companies:,}")
    with col3:
        unique_roles = df['actual_role'].nunique()
        st.metric("Unique Roles", f"{unique_roles:,}")
    with col4:
        # Display job count by platform
        linkedin_count = len(df[df['platform'].str.lower() == 'linkedin'])
        naukri_count = len(df[df['platform'].str.lower() == 'naukri'])
        st.metric("LinkedIn/Naukri", f"{linkedin_count}/{naukri_count}")
