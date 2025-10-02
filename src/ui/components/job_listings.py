# Job Listings Component - Display scraped jobs
# EMD Compliance: ≤80 lines

import streamlit as st
from src.models import JobModel

def render_job_listings(jobs: list[JobModel]) -> None:
    """Render job listings in expandable cards"""
    st.subheader("📋 Scraped Job Listings")
    
    if not jobs:
        st.info("No jobs to display. Start scraping to see results!")
        return
    
    st.write(f"Showing top {min(20, len(jobs))} of {len(jobs)} jobs")
    
    for i, job in enumerate(jobs[:20], 1):
        job_skills: list[str] = (
            job.skills_list if hasattr(job, 'skills_list') and job.skills_list 
            else []
        )
        skills_display = job_skills[:15]
        
        with st.expander(f"{i}. {job.job_role} @ {job.company}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Location:** {job.location or 'N/A'}")
                st.markdown(f"**Experience:** {job.experience or 'N/A'}")
                if job.salary:
                    st.markdown(f"**Salary:** {job.salary}")
                if job.posted_date:
                    st.markdown(f"**Posted:** {job.posted_date}")
            
            with col2:
                if job.url:
                    st.link_button("View Job", job.url, use_container_width=True)
            
            if skills_display:
                st.markdown("**Required Skills:**")
                st.write(", ".join(skills_display))
                if len(job_skills) > 15:
                    st.caption(f"...and {len(job_skills) - 15} more")
            
            if job.jd:
                with st.expander("Job Description"):
                    st.write(job.jd[:500] + "..." if len(job.jd) > 500 else job.jd)
