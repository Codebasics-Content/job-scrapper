# Skills Analysis Charts Component - EMD Architecture
# Renders skills analysis and distribution visualizations

from __future__ import annotations

import re
from collections import Counter
from typing import TypedDict

import pandas as pd
import plotly.express as px
import streamlit as st

from src.ui.components.analytics.role_normalizer import RoleNormalizer


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


def _format_percentage(value: int | float) -> str:
    """Format a numeric value as percentage string"""
    return f"{float(value):.1f}%"


def _clean_emoji(text: str) -> str:
    """Remove emojis and special Unicode symbols from text"""
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"  # dingbats
        "\U000024C2-\U0001F251"
        "\U0001F900-\U0001F9FF"  # supplemental symbols
        "\U00002600-\U000026FF"  # misc symbols
        "\U00002700-\U000027BF"  # dingbats
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub('', text).strip()

def render_skills_analysis(all_jobs: list[JobData]) -> None:
    """Render skills analysis charts and metrics with job role filtering"""
    if not all_jobs:
        st.info("No data available yet. Please scrape some jobs first!")
        return

    # Initialize role normalizer
    normalizer = RoleNormalizer()

    # Extract unique input_roles (what was searched) and normalized actual_roles
    input_roles: set[str] = set()
    normalized_roles: set[str] = set()
    for job in all_jobs:
        # Input role (original search term)
        input_role: str | None = job.get('input_role')
        if input_role:
            input_roles.add(input_role)
        # Actual role (normalized from LinkedIn/Naukri title)
        actual_role: str | None = job.get('actual_role')
        if actual_role:
            cleaned: str = _clean_emoji(actual_role)
            normalized: str = normalizer.normalize_role(cleaned)
            normalized_roles.add(normalized)

    input_role_list: list[str] = sorted(input_roles)
    job_roles: list[str] = sorted(normalized_roles)

    # Filter controls in two columns
    st.markdown("### Filter by Job Role")
    col1, col2 = st.columns(2)

    with col1:
        filter_type: str = st.radio(
            "Filter by",
            options=["Search Term (Input Role)", "Job Title (Actual Role)"],
            help="Choose to filter by what was searched OR by normalized job title",
            horizontal=True
        )

    with col2:
        if filter_type == "Search Term (Input Role)":
            selected_role: str | None = st.selectbox(
                "Select Search Term",
                options=["All Roles"] + input_role_list,
                help="Filter by original search term (e.g., 'Data Engineer' search)"
            )
        else:
            selected_role = st.selectbox(
                "Select Job Role",
                options=["All Roles"] + job_roles,
                help="Filter by normalized job title from LinkedIn/Naukri"
            )

    # Filter jobs based on selected role
    filtered_jobs: list[JobData]
    role_display: str
    if selected_role and selected_role != "All Roles":
        if filter_type == "Search Term (Input Role)":
            filtered_jobs = [
                job for job in all_jobs
                if job.get('input_role') == selected_role
            ]
            role_display = f" for '{selected_role}' searches"
        else:
            filtered_jobs = [
                job for job in all_jobs
                if normalizer.normalize_role(_clean_emoji(job.get('actual_role') or '')) == selected_role
            ]
            role_display = f" for {selected_role}"
    else:
        filtered_jobs = list(all_jobs)
        role_display = " (All Roles)"

    if not filtered_jobs:
        st.warning(f"No jobs found for role: {selected_role}")
        return

    # Show job count KPI for selected role
    if selected_role and selected_role != "All Roles":
        st.metric(
            label=f"{selected_role}",
            value=f"{len(filtered_jobs):,} Jobs",
            help=f"Total jobs matching {selected_role}"
        )
    else:
        st.metric(
            label="All Roles",
            value=f"{len(filtered_jobs):,} Jobs",
            help="Total jobs across all roles"
        )

    # Flatten all skills from filtered jobs
    all_skills: list[str] = []
    for job in filtered_jobs:
        skills_val: str | list[str] | None = job.get('skills')
        if skills_val:
            # Parse comma-separated skills string into list
            if isinstance(skills_val, str):
                skills_list: list[str] = [s.strip() for s in skills_val.split(',') if s.strip()]
                all_skills.extend(skills_list)
            else:
                all_skills.extend(skills_val)

    # Step 1: Build canonical mapping (lowercase -> most common capitalization)
    skill_variations: dict[str, dict[str, int]] = {}
    for skill in all_skills:
        skill_clean: str = skill.strip()
        if skill_clean:
            skill_lower: str = skill_clean.lower()
            if skill_lower not in skill_variations:
                skill_variations[skill_lower] = {skill_clean: 1}
            else:
                if skill_clean in skill_variations[skill_lower]:
                    skill_variations[skill_lower][skill_clean] += 1
                else:
                    skill_variations[skill_lower][skill_clean] = 1

    # Step 2: Pick most common capitalization for each skill
    canonical_map: dict[str, str] = {}
    for skill_lower, variations in skill_variations.items():
        # Get the variation with highest count
        max_count: int = max(variations.values())
        # Get all variations with max count, pick alphabetically first
        top_variations: list[str] = [k for k, v in variations.items() if v == max_count]
        sorted_variations: list[str] = sorted(top_variations)
        canonical_form: str = sorted_variations[0]
        canonical_map[skill_lower] = canonical_form

    # Step 3: Normalize all skills using canonical map
    all_skills = [canonical_map[s.strip().lower()] for s in all_skills if s.strip()]

    if not all_skills:
        st.warning("No skills data available for analysis")
        return

    # Calculate total jobs from filtered set
    total_jobs: int = len(filtered_jobs)
    skill_counts: Counter[str] = Counter(all_skills)

    # Slider for number of skills to display (default: 30, optimal for readability)
    num_skills: int = st.slider(
        "Number of skills to display",
        min_value=10,
        max_value=min(100, len(skill_counts)),
        value=30,
        step=5,
        help="30 is optimal for readability. Increase for detailed analysis."
    )

    st.subheader(f"Skills Analysis - Top {num_skills} Skills{role_display}")

    # Top skills analysis with percentages
    top_skills: list[tuple[str, int]] = skill_counts.most_common(num_skills)

    if top_skills:
        # Calculate percentages: (skill_count / total_jobs) * 100
        skills_data: list[dict[str, str | int | float]] = []
        for skill, count in top_skills:
            percentage: float = (count / total_jobs) * 100
            skills_data.append({
                'Skill': skill,
                'Count': count,
                'Percentage': round(percentage, 1)
            })

        skills_df: pd.DataFrame = pd.DataFrame(skills_data)

        # Sort by Count descending for chart (most populated at top)
        chart_df: pd.DataFrame = skills_df.sort_values('Count', ascending=True)

        # Create horizontal bar chart with gradient colors using Plotly
        fig = px.bar(
            chart_df,
            x='Count',
            y='Skill',
            orientation='h',
            color='Count',
            color_continuous_scale='Viridis',
            hover_data={'Percentage': True, 'Count': True}
        )

        # Update layout for better appearance
        # Height scales with number of skills (25px per bar, min 400px)
        chart_height: int = max(400, num_skills * 25)
        fig.update_layout(
            height=chart_height,
            showlegend=False,
            coloraxis_showscale=True,
            coloraxis_colorbar={"title": "Count"},
            yaxis={"tickfont": {"size": 11}},
            xaxis={"title": "Job Count"},
            margin={"l": 10, "r": 10, "t": 10, "b": 10}
        )

        col1, col2 = st.columns([2, 1])
        with col1:
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            # Format percentage for display
            display_df: pd.DataFrame = skills_df.copy()
            display_df['Percentage'] = display_df['Percentage'].apply(_format_percentage)
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )

    # Skills distribution metrics
    total_unique_skills: int = len(skill_counts)
    avg_skills_per_job: float = len(all_skills) / total_jobs if total_jobs > 0 else 0.0

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Unique Skills", total_unique_skills)
    with col2:
        st.metric("Avg Skills/Job", f"{avg_skills_per_job:.1f}")
