"""Phase 3: Skills Analysis Dashboard - Database-Driven Analytics
Streamlit dashboard for analyzing scraped job skills from database
"""
import streamlit as st
import pandas as pd
from collections import Counter
from src.db.connection import get_db_connection

st.set_page_config(page_title="Job Skills Analytics", page_icon="📊", layout="wide")

def fetch_all_jobs() -> pd.DataFrame:
    """Fetch all jobs from database"""
    conn = get_db_connection()
    query = """
        SELECT job_role, company, platform, location, 
               experience, skills, scraped_at 
        FROM jobs 
        ORDER BY scraped_at DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def extract_skills_list(df: pd.DataFrame) -> list[str]:
    """Extract all skills from jobs dataframe"""
    all_skills: list[str] = []
    for skills_str in df['skills'].dropna():
        if skills_str and skills_str != 'N/A':
            skills = [s.strip() for s in str(skills_str).split(',')]
            all_skills.extend(skills)
    return all_skills

# Main Dashboard
st.title("📊 Job Skills Analysis Dashboard")
st.markdown("Real-time analytics from scraped job data")

# Fetch data
with st.spinner("Loading data from database..."):
    jobs_df = fetch_all_jobs()

# Metrics Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Jobs", len(jobs_df))
with col2:
    naukri_count = len(jobs_df[jobs_df['platform'] == 'Naukri'])
    st.metric("Naukri Jobs", naukri_count)
with col3:
    indeed_count = len(jobs_df[jobs_df['platform'] == 'Indeed'])
    st.metric("Indeed Jobs", indeed_count)
with col4:
    unique_companies = jobs_df['company'].nunique()
    st.metric("Unique Companies", unique_companies)

# Skills Analysis
st.header("🎯 Skills Analysis")

all_skills = extract_skills_list(jobs_df)
skill_counts = Counter(all_skills)
top_skills = skill_counts.most_common(20)

# Top Skills Chart
col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("Top 20 Skills")
    skills_df = pd.DataFrame(top_skills, columns=['Skill', 'Count'])
    st.bar_chart(skills_df.set_index('Skill'))

with col2:
    st.subheader("Skills Stats")
    st.metric("Total Skills Found", len(all_skills))
    st.metric("Unique Skills", len(skill_counts))
    avg_skills = len(all_skills) / len(jobs_df) if len(jobs_df) > 0 else 0
    st.metric("Avg Skills/Job", f"{avg_skills:.1f}")

# Platform Comparison
st.header("📈 Platform Comparison")
platform_stats = jobs_df.groupby('platform').agg({
    'job_role': 'count',
    'company': 'nunique'
}).rename(columns={'job_role': 'Jobs', 'company': 'Companies'})
st.dataframe(platform_stats, use_container_width=True)

# Recent Jobs
st.header("🆕 Recent Jobs")
st.dataframe(jobs_df.head(10), use_container_width=True)
