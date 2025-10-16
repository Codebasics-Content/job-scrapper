# Company Skills Charts Component - EMD Architecture
# Renders unique skills by company visualization

import streamlit as st
import pandas as pd
from typing import List, Dict, Any

def render_platform_distribution(all_jobs: List[Dict[str, Any]]) -> None:
    """Render unique skills by company (Top 20)"""
    if not all_jobs:
        st.info("📭 No data available yet. Please scrape some jobs first!")
        return
    
    df = pd.DataFrame(all_jobs)
    
    st.subheader("🏢 Unique Skills by Company (Top 20)")
    if 'company_name' not in df.columns or 'skills' not in df.columns:
        st.warning("⚠️ Company or skills data not available in database")
        return
    
    # Calculate unique skills per company
    company_skills = {}
    for idx, row in df.iterrows():
        company = row.get('company_name', 'Unknown')
        skills_str = row.get('skills', '')
        
        if company not in company_skills:
            company_skills[company] = set()
        
        if skills_str:
            skills = [s.strip() for s in skills_str.split(',')]
            company_skills[company].update(skills)
    
    # Convert to dataframe and get top 20
    skills_data = pd.DataFrame([
        {'Company': company, 'Unique Skills': len(skills)}
        for company, skills in company_skills.items()
    ]).sort_values('Unique Skills', ascending=False).head(20)
    
    if skills_data.empty:
        st.info("📊 No company skills data available")
        return
    
    # Display chart and table
    col1, col2 = st.columns([2, 1])
    with col1:
        st.bar_chart(skills_data.set_index('Company')['Unique Skills'])
    with col2:
        st.dataframe(
            skills_data.reset_index(drop=True),
            width='stretch',
            hide_index=True
        )
