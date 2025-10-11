# Job Scraper Application - Modular EMD Architecture
# Uses modular UI components for clean separation of concerns

import logging
import streamlit as st
from src.db import DatabaseConnection, SchemaManager, JobStorageOperations
from src.ui.components import (
    render_analytics_overview,
    render_platform_distribution,
    render_skills_analysis,
    render_scraper_form
)

logging.basicConfig(level=logging.INFO)
DB_PATH = "jobs.db"

# Initialize database
SchemaManager(DatabaseConnection(db_path=DB_PATH)).initialize_schema()

# Page configuration
st.set_page_config(
    page_title="Job Scraper & Analytics",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("🔍 Job Scraper & Analytics Dashboard")
st.markdown("**Scrape jobs from LinkedIn, Indeed & Naukri | Analyze skills & trends from database**")
st.divider()

# Main Tabs
tab1, tab2 = st.tabs(["🤖 Scraper", "📊 Analytics Dashboard"])

# ==================== TAB 1: SCRAPER ====================
with tab1:
    render_scraper_form(DB_PATH)

# ==================== TAB 2: ANALYTICS ====================
with tab2:
    st.header("📊 Analytics Dashboard")
    st.markdown("**Real-time insights from HeadlessX + Local Luminati Proxy architecture**")
    
    # Load data from database
    db_ops = JobStorageOperations(DB_PATH)
    all_jobs = db_ops.get_jobs_by_role("")  # Get all jobs
    
    # Render modular analytics components
    render_analytics_overview(all_jobs)
    st.divider()
    render_platform_distribution(all_jobs)
    st.divider()
    render_skills_analysis(all_jobs)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px;'>
    <small>Job Scraper & Analytics Dashboard v2.0 | Data stored in SQLite</small>
</div>
""", unsafe_allow_html=True)
