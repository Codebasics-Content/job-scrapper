# Streamlit Job Scraper - Single Form Interface
import streamlit as st
import logging
import asyncio
from scrapers.linkedin.scraper import LinkedInScraper
from scrapers.linkedin.config.countries import LINKEDIN_COUNTRIES
from database.core.connection_manager import ConnectionManager
from database.core.batch_operations import BatchOperations
from database.core.job_retrieval import JobRetrieval
from database.schema.schema_manager import SchemaManager
from database.connection.db_connection import DatabaseConnection
from utils.analysis.visualization import generate_skill_leaderboard

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database schema on app startup (idempotent)
DB_PATH = "jobs.db"
db_conn = DatabaseConnection(db_path=DB_PATH)
schema_mgr = SchemaManager(db_conn)
schema_mgr.initialize_schema()
logger.info("Database schema initialized")

st.set_page_config(page_title="Job Scraper", page_icon="🔍", layout="wide")
st.title("🔍 Job Scraper with Skill Analysis")

# Single form for scraping
with st.form("job_scraper_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        job_role = st.text_input(
            "Job Role",
            value="Data Scientist",
            placeholder="e.g., Data Scientist, AI Engineer"
        )
        platform = st.selectbox(
            "Platform",
            options=["LinkedIn"]
        )
    
    with col2:
        num_jobs = st.slider(
            "Number of Jobs",
            min_value=5,
            max_value=1000,
            value=10,
            step=5
        )
    
    # Country selection
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
    
    submit = st.form_submit_button("🔍 Start Scraping", type="primary", use_container_width=True)

if submit and job_role:
    # Create progress containers
    progress_container = st.container()
    status_text = progress_container.empty()
    progress_bar = progress_container.progress(0)
    metrics_col1, metrics_col2 = progress_container.columns(2)
    
    with metrics_col1:
        scraped_metric = st.empty()
    with metrics_col2:
        stored_metric = st.empty()
    
    # Initialize scraper
    scraper = LinkedInScraper()
    
    # Update initial status
    status_text.info(f"🌐 Loading {platform} page...")
    scraped_metric.metric("Jobs Scraped", "0", f"Target: {num_jobs}")
    stored_metric.metric("Jobs Stored", "0")
    
    # Filter selected countries
    countries_to_scrape = [
        country for country in LINKEDIN_COUNTRIES 
        if country['name'] in selected_countries
    ]
    
    if not countries_to_scrape:
        st.error("⚠️ Please select at least one country to scrape")
        st.stop()
    
    # Scrape jobs from selected countries in parallel
    st.info(f"🌍 Scraping from {len(countries_to_scrape)} selected countries in parallel")
    scraped_jobs = asyncio.run(scraper.scrape_jobs(
        job_role=job_role,
        target_count=num_jobs,
        countries=countries_to_scrape
    ))
    
    # Update after scraping
    progress_bar.progress(0.7)
    status_text.info(f"💾 Storing {len(scraped_jobs)} jobs in database...")
    scraped_metric.metric("Jobs Scraped", len(scraped_jobs), "✓ Complete")
    
    # Store in database
    conn_mgr = ConnectionManager("jobs.db")
    batch_ops = BatchOperations()
    with conn_mgr.get_connection() as conn:
        stored_count = batch_ops.batch_store_jobs(conn, scraped_jobs)
    
    # Final update
    progress_bar.progress(1.0)
    status_text.success(f"✅ Completed! Scraped {len(scraped_jobs)} jobs, stored {stored_count} new jobs")
    stored_metric.metric("Jobs Stored", stored_count, f"{len(scraped_jobs) - stored_count} duplicates")
    
    st.session_state['last_scraped_jobs'] = scraped_jobs
else:
    st.warning("No jobs found")

# Visualization tabs
if 'last_scraped_jobs' in st.session_state or st.button("📊 Load from Database"):
    tab1, tab2, tab3 = st.tabs(["📋 Job Listings", "📊 Skill Leaderboard", "📈 Analytics"])
    
    with tab1:
        st.subheader("Scraped Job Listings")
        if 'last_scraped_jobs' in st.session_state:
            jobs = st.session_state['last_scraped_jobs']
            for i, job in enumerate(jobs[:20], 1):
                with st.expander(f"{i}. {job.job_role} @ {job.company}"):
                    st.write(f"**Skills:** {', '.join(job.skills_list[:15])}")
    
    with tab2:
        st.subheader("Top Skills Leaderboard")
        conn_mgr = ConnectionManager("jobs.db")
        retrieval = JobRetrieval()
        
        with conn_mgr.get_connection() as conn:
            db_jobs = retrieval.retrieve_all_jobs(conn)
        
        if db_jobs:
            leaderboard = generate_skill_leaderboard(db_jobs, top_n=20)
            if leaderboard:
                import pandas as pd
                df = pd.DataFrame(leaderboard)
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Jobs", len(db_jobs))
                col2.metric("Unique Skills", len(leaderboard))
                col3.metric("Top Skill", leaderboard[0]['skill'])
                
                st.dataframe(df, use_container_width=True)
                st.bar_chart(df.set_index('skill')['percentage'])
                
                csv = df.to_csv(index=False)
                st.download_button("📥 CSV", csv, "leaderboard.csv")
    
    with tab3:
        st.subheader("📈 Analytics Dashboard")
        
        if db_jobs:
            import pandas as pd
            
            # Basic statistics
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Jobs", len(db_jobs))
            
            total_skills = sum(len(job.skills_list) for job in db_jobs if job.skills_list)
            avg_skills = total_skills / len(db_jobs) if db_jobs else 0
            col2.metric("Avg Skills/Job", f"{avg_skills:.1f}")
            
            unique_companies = len(set(job.company for job in db_jobs))
            col3.metric("Unique Companies", unique_companies)
            
            unique_roles = len(set(job.job_role for job in db_jobs))
            col4.metric("Unique Roles", unique_roles)
            
            st.divider()
            
            # Top companies
            st.subheader("Top Companies Hiring")
            company_counts = {}
            for job in db_jobs:
                company_counts[job.company] = company_counts.get(job.company, 0) + 1
            
            top_companies = sorted(company_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            company_df = pd.DataFrame(top_companies, columns=["Company", "Jobs"])  # type: ignore[call-overload]
            st.dataframe(company_df, use_container_width=True)
            
            st.divider()
            
            # Role distribution
            st.subheader("Role Distribution")
            role_counts = {}
            for job in db_jobs:
                role_counts[job.job_role] = role_counts.get(job.job_role, 0) + 1
            
            role_df = pd.DataFrame(list(role_counts.items()), columns=["Role", "Count"])  # type: ignore[call-overload]
            st.bar_chart(role_df.set_index("Role")["Count"])
            
            st.divider()
            
            # CSV Export
            st.subheader("📥 Export Analytics Data")
            
            # Prepare comprehensive analytics data
            analytics_data = []
            for job in db_jobs:
                analytics_data.append({
                    "Job Role": job.job_role,
                    "Company": job.company,
                    "Location": job.location,
                    "Skills Count": len(job.skills_list) if job.skills_list else 0,
                    "Skills": ", ".join(job.skills_list) if job.skills_list else "",
                    "Posted Date": job.posted_date,
                    "Job URL": job.url
                })
            
            analytics_df = pd.DataFrame(analytics_data)
            csv_data = analytics_df.to_csv(index=False)
            
            st.download_button(
                label="📥 Download Complete Analytics CSV",
                data=csv_data,
                file_name="job_analytics_complete.csv",
                mime="text/csv",
                width="stretch"
            )
        else:
            st.info("No data available. Scrape jobs first!")
