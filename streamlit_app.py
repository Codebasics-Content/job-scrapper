# Job Scraper Application - Modular EMD Architecture
# Uses modular UI components for clean separation of concerns

import logging
import os

import streamlit as st
from dotenv import load_dotenv

# Load environment variables (including PLAYWRIGHT_BROWSERS_PATH)
load_dotenv()

# FIX: Force TMPDIR to Linux filesystem (NTFS causes Playwright SIGTRAP crash)
os.environ["TMPDIR"] = "/tmp"
os.environ["TMP"] = "/tmp"
os.environ["TEMP"] = "/tmp"

from src.db import DatabaseConnection, JobStorageOperations, SchemaManager
from src.ui.components import (
    render_analytics_overview,
    render_compact_kpi,
    render_detail_scraper_form,
    render_kpi_dashboard,
    render_link_scraper_form,
    render_skills_analysis,
)

logging.basicConfig(level=logging.INFO)
DB_PATH = "data/jobs.db"

# Initialize database
SchemaManager(DatabaseConnection(db_path=DB_PATH)).initialize_schema()

# Page configuration
st.set_page_config(
    page_title="Job Scraper & Analytics",
    page_icon="🔍",
    initial_sidebar_state="expanded",
)

# Title
st.title("🔍 Job Scraper & Analytics Dashboard")
st.markdown(
    "**2-Phase Architecture: Link Collection → Detail Extraction | 3-Layer Skills | Zero False Positives**"
)

# Compact KPI Strip at the top
render_compact_kpi(DB_PATH)

st.divider()

# Main Tabs - Split Scraper Logic
tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 KPI Dashboard", "🔗 Link Scraper", "📝 Detail Scraper", "📈 Analytics"]
)

# ==================== TAB 1: KPI DASHBOARD ====================
with tab1:
    render_kpi_dashboard(DB_PATH)

# ==================== TAB 2: LINK SCRAPER ====================
with tab2:
    render_link_scraper_form(DB_PATH)

# ==================== TAB 3: DETAIL SCRAPER ====================
with tab3:
    render_detail_scraper_form(DB_PATH)

# ==================== TAB 4: ANALYTICS ====================
with tab4:
    st.header("📈 Analytics Dashboard")
    st.markdown(
        "**Real-time insights from 2-platform architecture (LinkedIn + Naukri)**"
    )

    # Load data from database
    db_ops = JobStorageOperations(DB_PATH)
    all_jobs = db_ops.get_all_jobs()

    # Render modular analytics components
    render_analytics_overview(all_jobs)
    st.divider()
    render_skills_analysis(all_jobs)

# Footer
st.divider()
st.markdown(
    "<div style='text-align: center; color: gray; padding: 20px;'><small>Job Scraper & Analytics Dashboard v2.0 | Data stored in SQLite</small></div>",
    unsafe_allow_html=True,
)
