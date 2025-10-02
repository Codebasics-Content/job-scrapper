# Skill Leaderboard Component - Top skills visualization
# EMD Compliance: ≤80 lines

import streamlit as st
import pandas as pd
from src.db import JobStorageOperations
from src.analysis.analysis.visualization import generate_skill_leaderboard

def render_skill_leaderboard(db_path: str) -> None:
    """Render skill leaderboard with top N skills"""
    st.subheader("📊 Top Skills Leaderboard")
    
    query_ops = JobStorageOperations(db_path)
    db_jobs_dicts = query_ops.get_jobs_by_role("")
    
    if not db_jobs_dicts:
        st.info("No jobs in database. Scrape jobs first to see skill analysis!")
        return
    
    leaderboard = generate_skill_leaderboard(db_jobs_dicts, top_n=20)
    
    if not leaderboard:
        st.warning("No skills found in the database")
        return
    
    df = pd.DataFrame(leaderboard)
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Jobs", len(db_jobs_dicts))
    col2.metric("Unique Skills", len(leaderboard))
    col3.metric("Top Skill", leaderboard[0]['skill'])
    
    # Display table and chart
    st.dataframe(
        df.style.background_gradient(subset=['percentage'], cmap='Blues'),
        use_container_width=True
    )
    
    st.bar_chart(df.set_index('skill')['percentage'])
    
    # Export functionality
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download Skill Leaderboard CSV",
        data=csv,
        file_name="skill_leaderboard.csv",
        mime="text/csv",
        key="download_skill_leaderboard",
        use_container_width=True
    )
