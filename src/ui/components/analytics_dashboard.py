# Analytics Dashboard Orchestrator - EMD Architecture
# Orchestrates modular analytics components for unified display

from typing import List, Dict, Any

from .analytics import (
    render_overview_metrics,
    render_platform_distribution,
    render_skills_analysis
)

def render_analytics_dashboard(all_jobs: List[Dict[str, Any]]) -> None:
    """Main analytics dashboard orchestrator"""
    render_overview_metrics(all_jobs)
    render_platform_distribution(all_jobs)
    render_skills_analysis(all_jobs)
