# UI Components Module - EMD Architecture
# Exports for modular Streamlit dashboard components

"""Streamlit UI components for job scraper dashboard"""

from .analytics_dashboard import render_analytics_overview, render_skills_analysis
from .detail_scraper_form import render_detail_scraper_form
from .kpi_dashboard import render_compact_kpi, render_kpi_dashboard
from .link_scraper_form import render_link_scraper_form

__all__ = [
    "render_analytics_overview",
    "render_skills_analysis",
    "render_link_scraper_form",
    "render_detail_scraper_form",
    "render_kpi_dashboard",
    "render_compact_kpi",
]
