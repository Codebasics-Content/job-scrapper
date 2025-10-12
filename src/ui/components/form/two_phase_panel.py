# Two-Phase Scraper Configuration Panel - EMD Component
# Separate UI for URL collection and detail scraping
import streamlit as st
from src.db import JobStorageOperations
from src.models import JobUrlModel


def render_two_phase_panel(db_path: str) -> tuple[str, str, str, int, str]:
    """Render two-phase scraper configuration with separate buttons"""
    st.subheader("🔄 Two-Phase Job Scraper (80-90% Faster)")
    st.markdown("**Phase 1:** Collect URLs quickly | **Phase 2:** Scrape details for unscraped jobs")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⚙️ Configuration")
        platform = st.selectbox(
            "Platform",
            ["Naukri", "Indeed"],
            help="Select job platform to scrape"
        )
        job_role = st.text_input(
            "Job Role",
            value="AI Engineer",
            help="Job title to search for"
        )
        location = st.text_input(
            "Location",
            value="India" if platform == "Naukri" else "United States",
            help="Search location"
        )
        num_jobs = st.number_input(
            "Number of URLs/Details",
            min_value=1,
            max_value=1000,
            value=100,
            step=10,
            help="Limit for scraping"
        )
    
    with col2:
        st.markdown("### 📊 Database Status")
        db_ops = JobStorageOperations(db_path)
        input_role = JobUrlModel.normalize_role(job_role)
        
        # Query unscraped count
        unscraped = db_ops.get_unscraped_urls(platform, input_role, limit=10000)
        unscraped_count = len(unscraped) if unscraped else 0
        
        st.metric("Unscraped URLs", unscraped_count, 
                 help="URLs in database without full details")
        st.info(f"**Ready for Phase 2:** {unscraped_count} jobs need details")
    
    st.divider()
    
    # Phase buttons
    phase_col1, phase_col2 = st.columns(2)
    
    with phase_col1:
        phase1_clicked = st.button(
            "🔗 Phase 1: Scrape URLs",
            type="primary",
            use_container_width=True,
            help="Fast URL collection (10-100x faster)"
        )
    
    with phase_col2:
        phase2_clicked = st.button(
            "📄 Phase 2: Scrape Details",
            type="secondary",
            use_container_width=True,
            help="Scrape full details for unscraped URLs",
            disabled=unscraped_count == 0
        )
    
    phase = "phase1" if phase1_clicked else ("phase2" if phase2_clicked else "none")
    
    return platform, job_role, location, num_jobs, phase
