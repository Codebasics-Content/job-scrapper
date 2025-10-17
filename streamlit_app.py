# Job Scraper Application - Modular EMD Architecture
# Uses modular UI components for clean separation of concerns

import logging
import streamlit as st
from src.db import DatabaseConnection, SchemaManager, JobStorageOperations
from src.ui.components import (
    render_analytics_overview,
    render_skills_analysis,
    render_link_scraper_form,
    render_detail_scraper_form
)

logging.basicConfig(level=logging.INFO)
DB_PATH = "data/jobs.db"

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
st.markdown("**2-Phase Architecture: Link Collection → Detail Extraction | 3-Layer Skills | Zero False Positives**")
st.divider()

# Main Tabs - Split Scraper Logic
tab1, tab2, tab3 = st.tabs(["🔗 Link Scraper", "📝 Detail Scraper", "📊 Analytics"])

# ==================== TAB 1: LINK SCRAPER ====================
with tab1:
    render_link_scraper_form(DB_PATH)

# ==================== TAB 2: DETAIL SCRAPER ====================
with tab2:
    render_detail_scraper_form(DB_PATH)

# ==================== TAB 3: ANALYTICS ====================
with tab3:
    st.header("📊 Analytics Dashboard")
    st.markdown("**Real-time insights from 2-platform architecture (LinkedIn + Naukri)**")
    
    # Load data from database
    db_ops = JobStorageOperations(DB_PATH)
    all_jobs = db_ops.get_all_jobs()
    
    # Render modular analytics components
    render_analytics_overview(all_jobs)
    st.divider()
    render_skills_analysis(all_jobs)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px;'>
    <small>Job Scraper & Analytics Dashboard v2.0 | Data stored in SQLite</small>
</div>
""", unsafe_allow_html=True)
