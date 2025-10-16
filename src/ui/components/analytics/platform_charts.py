# Top Skills Analytics Component - EMD Architecture
# Renders most in-demand skills across all jobs

import streamlit as st
import pandas as pd
from typing import List, Dict, Any
from collections import Counter

def render_platform_distribution(all_jobs: List[Dict[str, Any]]) -> None:
    """Render top in-demand skills (Top 20)"""
    if not all_jobs:
        st.info("📭 No data available yet. Please scrape some jobs first!")
        return
    
    df = pd.DataFrame(all_jobs)
    
    st.subheader("🔥 Top 20 In-Demand Skills")
    if 'skills' not in df.columns:
        st.warning("⚠️ Skills data not available in database")
        return
    
    # Extract all skills and count frequency
    all_skills = []
    for skills_str in df['skills'].dropna():
        if skills_str:
            skills = [s.strip() for s in skills_str.split(',')]
            all_skills.extend(skills)
    
    if not all_skills:
        st.info("📊 No skills data available")
        return
    
    # Count skill frequency and get top 20
    skill_counts = Counter(all_skills)
    top_skills = skill_counts.most_common(20)
    
    skills_df = pd.DataFrame(top_skills, columns=['Skill', 'Jobs Count'])
    
    # Calculate percentage
    total_jobs = len(df)
    skills_df['% of Jobs'] = (skills_df['Jobs Count'] / total_jobs * 100).round(1)
    
    # Display chart and table
    col1, col2 = st.columns([2, 1])
    with col1:
        st.bar_chart(skills_df.set_index('Skill')['Jobs Count'])
    with col2:
        st.dataframe(
            skills_df,
            width='stretch',
            hide_index=True
        )
