# Skills Analysis Charts Component - EMD Architecture
# Renders skills analysis and distribution visualizations

import streamlit as st
import pandas as pd
from typing import List, Dict, Any
from collections import Counter

def render_skills_analysis(all_jobs: List[Dict[str, Any]]) -> None:
    """Render skills analysis charts and metrics"""
    # Flatten all skills from jobs
    all_skills = []
    for job in all_jobs:
        if job.get('skills'):
            all_skills.extend(job['skills'])
    
    if not all_skills:
        st.warning("No skills data available for analysis")
        return
    
    st.subheader("🚀 Skills Analysis")
    
    # Top skills analysis
    skill_counts = Counter(all_skills)
    top_skills = skill_counts.most_common(20)
    
    if top_skills:
        skills_df = pd.DataFrame(top_skills, columns=['Skill', 'Count'])
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.bar_chart(skills_df.set_index('Skill')['Count'])
        with col2:
            st.dataframe(
                skills_df,
                use_container_width=True,
                hide_index=True
            )
    
    # Skills distribution metrics
    total_unique_skills = len(skill_counts)
    avg_skills_per_job = len(all_skills) / len(all_jobs) if all_jobs else 0
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Unique Skills", total_unique_skills)
    with col2:
        st.metric("Avg Skills/Job", f"{avg_skills_per_job:.1f}")
