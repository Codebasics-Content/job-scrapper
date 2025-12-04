# Overview Metrics Component - EMD Architecture
# Renders job overview metrics and statistics

from __future__ import annotations

from typing import TypedDict

import pandas as pd
import streamlit as st


class JobData(TypedDict, total=False):
    """Type for job data dict from database"""
    job_id: str
    platform: str
    actual_role: str
    url: str
    job_description: str
    skills: str | list[str]
    company_name: str
    posted_date: str | None
    scraped_at: str | None


def render_analytics_overview(all_jobs: list[JobData]) -> None:
    """Render overview metrics section"""
    if not all_jobs:
        st.info("No data available yet. Please scrape some jobs first!")
        return

    df: pd.DataFrame = pd.DataFrame(all_jobs)
    total_jobs: int = len(df)

    st.subheader("Overview")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Jobs", f"{total_jobs:,}")
    with col2:
        unique_companies: int = int(df['platform'].nunique())
        st.metric("Platforms", f"{unique_companies:,}")
    with col3:
        unique_roles: int = int(df['actual_role'].nunique())
        st.metric("Unique Roles", f"{unique_roles:,}")
    with col4:
        # Display job count by platform
        linkedin_count: int = len(df[df['platform'].str.lower() == 'linkedin'])
        naukri_count: int = len(df[df['platform'].str.lower() == 'naukri'])
        st.metric("LinkedIn/Naukri", f"{linkedin_count}/{naukri_count}")
