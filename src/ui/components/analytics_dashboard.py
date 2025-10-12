# Analytics Dashboard Orchestrator - EMD Architecture
# Orchestrates modular analytics components for unified display

from typing import List, Dict, Any

from .analytics.overview_metrics import render_analytics_overview as _render_overview
from .analytics.platform_charts import render_platform_distribution as _render_platform
from .analytics.skills_charts import render_skills_analysis as _render_skills

def render_analytics_overview(all_jobs: List[Dict[str, Any]]) -> None:
    """Render analytics overview section"""
    _render_overview(all_jobs)

def render_platform_distribution(all_jobs: List[Dict[str, Any]]) -> None:
    """Render platform distribution charts"""
    _render_platform(all_jobs)

def render_skills_analysis(all_jobs: List[Dict[str, Any]]) -> None:
    """Render skills analysis charts"""
    _render_skills(all_jobs)
