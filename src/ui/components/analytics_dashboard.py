# Analytics Dashboard Component - Comprehensive job analytics
# EMD Compliance: ≤80 lines

import streamlit as st
import pandas as pd
from src.db import JobStorageOperations
from src.analysis.skill_normalizer import normalize_jobs_skills
from src.analysis.analysis.visualization import generate_skill_leaderboard
from .analytics_helpers import (extract_summary_metrics, extract_top_companies,
                                extract_role_distribution)

def render_analytics_dashboard(db_path: str) -> None:
    """Render comprehensive analytics dashboard"""
    st.subheader("📈 Analytics Dashboard")
    
    query_ops = JobStorageOperations(db_path)
    db_jobs_dicts = query_ops.get_jobs_by_role("")
    
    if not db_jobs_dicts:
        st.info("No data available. Scrape jobs first!")
        return
    
    # Summary metrics
    metrics = extract_summary_metrics(db_jobs_dicts)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Jobs", metrics['total_jobs'])
    col2.metric("Avg Skills/Job", f"{metrics['avg_skills']:.1f}")
    col3.metric("Unique Companies", metrics['unique_companies'])
    col4.metric("Unique Roles", metrics['unique_roles'])
    
    st.divider()
    
    # Top companies
    st.subheader("🏢 Top Companies Hiring")
    companies_df = extract_top_companies(db_jobs_dicts, top_n=100)
    st.dataframe(companies_df, use_container_width=True)
    
    st.divider()
    
    # Role distribution
    st.subheader("💼 Role Distribution")
    roles_df = extract_role_distribution(db_jobs_dicts)
    st.dataframe(roles_df, use_container_width=True)
    st.bar_chart(roles_df.set_index("Role")["Count"])
    
    st.divider()
    
    # Skill Analysis
    st.subheader("📊 Top Skills Analysis")
    
    # Normalize skills from database (used for both viz and export)
    normalized_jobs = normalize_jobs_skills(db_jobs_dicts)
    skills_leaderboard = generate_skill_leaderboard(normalized_jobs, top_n=20)
    
    if skills_leaderboard:
        skills_df = pd.DataFrame(skills_leaderboard)
        col1, col2, col3 = st.columns(3)
        col1.metric("Unique Skills", len(skills_leaderboard))
        col2.metric("Top Skill", skills_leaderboard[0]['skill'])
        col3.metric("Top Skill Count", skills_leaderboard[0]['count'])
        
        st.dataframe(
            skills_df,
            use_container_width=True
        )
        st.bar_chart(skills_df.set_index('skill')['percentage'])
