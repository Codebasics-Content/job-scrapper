# Job Scraper - BrightData + Skills Analytics
import asyncio
import logging
from types import SimpleNamespace
from typing import cast, List, Dict, Any

import streamlit as st
from src.db import DatabaseConnection, SchemaManager, JobStorageOperations
from src.ui.components import (render_scraper_form, ProgressTracker, render_job_listings,
                              render_analytics_dashboard)
from src.scraper.brightdata.clients.linkedin import LinkedInClient
from src.scraper.brightdata.clients.indeed import IndeedClient
from src.scraper.naukri.scraper import NaukriScraper
from src.scraper.brightdata.parsers.skills_parser import SkillsParser

logging.basicConfig(level=logging.INFO)
DB_PATH = "jobs.db"

# Initialize database
SchemaManager(DatabaseConnection(db_path=DB_PATH)).initialize_schema()

st.set_page_config(page_title="Job Scraper", page_icon="🔍", layout="wide")
st.title("🔍 Job Scraper with Skill Analysis (BrightData)")

form_data = render_scraper_form()

if form_data:
    job_role = cast(str, form_data["job_role"])
    platform = cast(str, form_data["platform"])
    num_jobs = cast(int, form_data["num_jobs"])
    countries = cast(List[Dict[str, str]], form_data.get("countries", []))

    progress_tracker = ProgressTracker(
        target_count=num_jobs,
        num_countries=len(countries) if countries else 1
    )

    # Initialize appropriate client based on platform
    client = None
    naukri_scraper = None
    
    if platform == "LinkedIn":
        client = LinkedInClient()
    elif platform == "Indeed":
        client = IndeedClient()
    elif platform == "Naukri":
        naukri_scraper = NaukriScraper()
    
    parser = SkillsParser()

    def _mk_job_model(raw: Dict[str, Any]) -> SimpleNamespace:
        title = cast(str, raw.get("job_title") or raw.get("title") or "")
        company = cast(str, raw.get("company_name") or raw.get("company") or "")
        url = cast(str, raw.get("job_url") or raw.get("url") or "")
        jd = cast(str, raw.get("job_description") or raw.get("description") or "")
        location = cast(str, raw.get("job_location") or raw.get("location") or "")
        posted = cast(str, raw.get("posted_time") or raw.get("posted_date") or "")
        skills_list = parser.extract_from_job({
            "title": title,
            "description": jd
        })
        skills = ", ".join(skills_list)
        job_id = raw.get("id") or url or f"{title}:{company}:{location}"
        return SimpleNamespace(
            job_id=str(job_id),
            job_role=title,
            company=company,
            experience="",
            skills=skills,
            jd=jd,
            company_detail="",
            platform=platform,
            url=url,
            location=location,
            salary=str(raw.get("salary") or ""),
            posted_date=posted
        )

    async def scrape_jobs():
        try:
            progress_tracker.update_loading(platform)
            
            # Handle Naukri separately (uses different scraper pattern)
            if platform == "Naukri" and naukri_scraper:
                naukri_jobs = await naukri_scraper.scrape_jobs(
                    keyword=job_role,
                    num_jobs=num_jobs
                )
                # Convert Naukri JobModels to SimpleNamespace for consistency
                jobs = [SimpleNamespace(**job.model_dump()) for job in naukri_jobs]
                progress_tracker.update_scraped(len(jobs))
            
            # Handle LinkedIn and Indeed via BrightData
            elif client:
                results: List[Dict[str, Any]] = []
                if countries:
                    for c in countries:
                        if len(results) >= num_jobs:
                            break
                        loc = c.get("name") or c.get("code") or ""
                        batch = client.discover_jobs(keyword=job_role, location=loc, limit=max(1, num_jobs - len(results)))
                        results.extend(batch)
                else:
                    results = client.discover_jobs(keyword=job_role, limit=num_jobs)

                jobs = [_mk_job_model(r) for r in results][:num_jobs]
                progress_tracker.update_scraped(len(jobs))
            else:
                raise RuntimeError(f"No scraper configured for platform: {platform}")

            db_ops = JobStorageOperations(DB_PATH)
            stored_count = db_ops.store_jobs(jobs)
            progress_tracker.update_complete(len(jobs), stored_count)
            st.session_state["scraped_jobs"] = [j.__dict__ for j in jobs]
        except Exception as error:
            progress_tracker.update_error(str(error))

    if st.button("🔍 Start Scraping", type="primary"):
        asyncio.run(scrape_jobs())

if "scraped_jobs" in st.session_state:
    tab1, tab2 = st.tabs(["📋 Jobs", "📈 Analytics"])
    with tab1:
        render_job_listings(st.session_state["scraped_jobs"])
    with tab2:
        render_analytics_dashboard(DB_PATH)
