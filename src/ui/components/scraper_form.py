# Scraper Form Component - Job scraping configuration UI
# EMD Compliance: ≤80 lines

import streamlit as st
from src.scraper.linkedin.config.countries import LINKEDIN_COUNTRIES

def render_scraper_form() -> dict[str, object] | None:
    """Render job scraper form and return form data if submitted"""
    with st.form("job_scraper_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            job_role = st.text_input(
                "Job Role",
                value="Data Scientist",
                placeholder="e.g., Data Scientist, AI Engineer"
            )
            platform = st.selectbox("Platform", options=["LinkedIn", "Naukri"])
        
        with col2:
            num_jobs = st.slider(
                "Number of Jobs",
                min_value=5,
                max_value=50000,
                value=10,
                step=5
            )
        
        # Country selection ONLY for LinkedIn (Naukri is India-only)
        selected_countries = []
        if platform == "LinkedIn":
            st.subheader("🌍 Country Selection")
            country_names = [c['name'] for c in LINKEDIN_COUNTRIES]
            
            select_all = st.checkbox("Select All Countries", value=True)
            
            if select_all:
                selected_countries = st.multiselect(
                    "Countries to scrape",
                    options=country_names,
                    default=country_names,
                    help="Scraping from multiple countries in parallel for diverse global data"
                )
            else:
                selected_countries = st.multiselect(
                    "Countries to scrape",
                    options=country_names,
                    default=["United States", "India", "United Kingdom"],
                    help="Select specific countries to scrape from"
                )
        
        submit = st.form_submit_button("🔍 Start Scraping", type="primary", width="stretch")
        
        # LinkedIn requires countries, Naukri doesn't
        if submit and job_role and (platform == "Naukri" or selected_countries):
            countries_to_scrape = [
                country for country in LINKEDIN_COUNTRIES 
                if country['name'] in selected_countries
            ]
            
            return {
                "job_role": job_role,
                "platform": platform,
                "num_jobs": num_jobs,
                "countries": countries_to_scrape
            }
        elif submit and platform == "LinkedIn" and not selected_countries:
            st.error("⚠️ Please select at least one country for LinkedIn scraping")
    
    return None
