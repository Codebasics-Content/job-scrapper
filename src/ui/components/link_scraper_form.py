# Link Scraper Component - Phase 1: URL Collection Only
# Multi-country sequential scraping with real-time deduplication

import asyncio
import streamlit as st
from src.db import JobStorageOperations
from src.config.countries import LINKEDIN_COUNTRIES
from src.config.naukri_locations import NAUKRI_ALL_LOCATIONS
from src.scraper.unified.linkedin.infinite_scroll_scraper import scrape_linkedin_urls_infinite_scroll
from src.scraper.unified.naukri.url_scraper import scrape_naukri_urls

def render_link_scraper_form(db_path: str) -> None:
    """Render Phase 1: Link/URL collection interface"""
    st.header("🔗 Phase 1: Link Scraper")
    st.markdown("**Collect valid job URLs** | Real-time deduplication | No duplicates stored")
    
    col1, col2 = st.columns(2)
    
    with col1:
        platform = st.selectbox(
            "Platform",
            ["LinkedIn", "Naukri"],
            help="Select platform to scrape URLs from"
        )
        
        job_role = st.text_input(
            "Job Role",
            value="AI Engineer",
            help="Enter the job role to search for"
        )
    
    with col2:
        num_jobs = st.number_input(
            "Number of URLs to Collect",
            min_value=10,
            max_value=10000,
            value=500,
            step=50,
            help="Maximum URLs to scrape per location (unlimited collection enabled)"
        )
    
    # Database stats
    db_ops = JobStorageOperations(db_path)
    existing_count = len(db_ops.get_unscraped_urls(platform.lower(), job_role, limit=num_jobs))
    
    st.info(f"📊 **Current Stats**: {existing_count} unscraped URLs in database for {platform}")
    
    # Platform-specific location scraping
    st.divider()
    st.subheader("🌍 Multi-Location Scraping")
    
    if platform.lower() == "linkedin":
        locations = LINKEDIN_COUNTRIES
        st.info(f"**{len(locations)} countries** will be scraped sequentially for LinkedIn")
    else:  # Naukri
        locations = list(NAUKRI_ALL_LOCATIONS.keys())
        st.info(f"**{len(locations)} locations** will be scraped sequentially for Naukri (India + International)")
    
    # Action buttons
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        location_count = len(LINKEDIN_COUNTRIES) if platform.lower() == "linkedin" else len(NAUKRI_ALL_LOCATIONS)
        scrape_button = st.button(
            f"🔗 Scrape {location_count} Locations ({num_jobs} URLs each)",
            type="primary",
            use_container_width=True
        )
        
        if scrape_button:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            async def scrape_all_locations():
                total_collected = 0
                
                if platform.lower() == "linkedin":
                    locations_to_scrape = LINKEDIN_COUNTRIES
                else:  # Naukri
                    locations_to_scrape = list(NAUKRI_ALL_LOCATIONS.keys())
                
                for idx, location in enumerate(locations_to_scrape):
                    status_text.text(f"🌍 Scraping {location} ({idx+1}/{len(locations_to_scrape)})...")
                    
                    try:
                        if platform.lower() == "linkedin":
                            urls = await scrape_linkedin_urls_infinite_scroll(
                                keyword=job_role,
                                location=location,
                                limit=num_jobs,
                                headless=False
                            )
                        else:  # Naukri
                            city_gid = NAUKRI_ALL_LOCATIONS.get(location)
                            urls = await scrape_naukri_urls(
                                keyword=job_role,
                                location=location,
                                limit=num_jobs,
                                headless=False,
                                store_to_db=False,
                                city_gid=city_gid
                            )
                        
                        if urls:
                            db_ops.store_urls(urls)
                            total_collected += len(urls)
                            status_text.success(f"✅ {location}: {len(urls)} URLs | Total: {total_collected}")
                    except Exception as e:
                        status_text.warning(f"⚠️ {location}: Error - {str(e)}")
                    
                    progress_bar.progress((idx + 1) / len(locations_to_scrape))
                
                return total_collected
            
            total = asyncio.run(scrape_all_locations())
            location_count = len(LINKEDIN_COUNTRIES) if platform.lower() == "linkedin" else len(NAUKRI_ALL_LOCATIONS)
            st.success(f"✅ Completed! Collected {total} URLs from {location_count} locations")
            st.rerun()
    
    with col_btn2:
        clear_button = st.button(
            "🗑️ Clear All URLs",
            use_container_width=True,
            help="Delete all unscraped URLs from database"
        )
        
        if clear_button:
            st.warning("⚠️ Clear URLs Not Yet Implemented")
