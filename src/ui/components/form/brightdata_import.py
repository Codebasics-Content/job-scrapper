# BrightData LinkedIn Import UI Component - EMD
# File upload interface for pre-scraped LinkedIn data

import streamlit as st
import json
from src.importer.brightdata.linkedin_importer import import_linkedin_jobs

def render_brightdata_import(db_path: str) -> None:
    """Render BrightData LinkedIn import interface"""
    st.subheader("📥 BrightData LinkedIn Import")
    st.info("Fetch LinkedIn jobs from BrightData Web Datasets (pre-collected data via API)")
    st.markdown("""
    **Import pre-scraped LinkedIn jobs from BrightData**
    - Upload JSON file with job data
    - Automatic skills extraction
    - Duplicate checking via job_id
    - Direct storage to jobs table
    """)
    
    uploaded_file = st.file_uploader(
        "Upload BrightData JSON",
        type=['json'],
        help="JSON file from BrightData LinkedIn scraper"
    )
    
    if uploaded_file and st.button("🚀 Import Jobs", type="primary"):
        try:
            # Read and parse JSON
            data = json.load(uploaded_file)
            
            # Handle both array and object with 'results' key
            if isinstance(data, dict) and 'results' in data:
                jobs_data = data['results']
            elif isinstance(data, list):
                jobs_data = data
            else:
                st.error("Invalid JSON format. Expected array or object with 'results' key")
                return
            
            st.info(f"Found {len(jobs_data)} jobs in file. Processing...")
            
            # Import with progress bar
            with st.spinner("Extracting skills and importing..."):
                stored, duplicates = import_linkedin_jobs(jobs_data, db_path)
            
            # Display results
            st.success(
                f"✅ Import Complete!\n\n"
                f"**{stored}** new jobs stored\n\n"
                f"**{duplicates}** duplicates skipped"
            )
            
            if stored > 0:
                st.balloons()
        
        except json.JSONDecodeError:
            st.error("Invalid JSON file. Please check file format.")
        except Exception as error:
            st.error(f"Import failed: {error}")
