# Platform Charts Component - EMD Architecture
# Renders platform distribution visualization charts

import streamlit as st
import pandas as pd
from typing import List, Dict, Any

def render_platform_distribution(all_jobs: List[Dict[str, Any]]) -> None:
    """Render platform distribution charts"""
    if not all_jobs:
        st.info("📭 No data available yet. Please scrape some jobs first!")
        return
    
    df = pd.DataFrame(all_jobs)
    
    st.subheader("🌐 Jobs by Platform")
    if 'platform' not in df.columns:
        st.warning("⚠️ Platform data not available in database")
        return
    
    platform_counts = df['platform'].value_counts()
    col1, col2 = st.columns([2, 1])
    with col1:
        st.bar_chart(platform_counts)
    with col2:
        st.dataframe(
            platform_counts.reset_index().rename(columns={'index': 'Platform', 'platform': 'Count'}),
            width='stretch',
            hide_index=True
        )
