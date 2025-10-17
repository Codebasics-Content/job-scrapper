# Skills Analysis Charts Component - EMD Architecture
# Renders skills analysis and distribution visualizations

import streamlit as st
import pandas as pd
import re
from typing import List, Dict, Any
from collections import Counter
from src.ui.components.analytics.role_normalizer import RoleNormalizer

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

def render_skills_analysis(all_jobs: List[Dict[str, Any]]) -> None:
    """Render skills analysis charts and metrics with job role filtering"""
    if not all_jobs:
        st.info("📭 No data available yet. Please scrape some jobs first!")
        return
    
    # Initialize role normalizer
    normalizer = RoleNormalizer()
    
    # Normalize and extract unique job roles for filter
    normalized_roles = set()
    for job in all_jobs:
        if job.get('actual_role'):
            cleaned = _clean_emoji(job.get('actual_role', ''))
            normalized = normalizer.normalize_role(cleaned)
            normalized_roles.add(normalized)
    
    job_roles = sorted(normalized_roles)
    
    # Job role filter dropdown
    st.markdown("### 🎯 Filter by Job Role")
    selected_role = st.selectbox(
        "Select Job Role",
        options=["All Roles"] + job_roles,
        help="Filter skills analysis by specific job role"
    )
    
    # Filter jobs based on selected role (compare normalized versions)
    if selected_role != "All Roles":
        filtered_jobs = [
            job for job in all_jobs 
            if normalizer.normalize_role(_clean_emoji(job.get('actual_role', ''))) == selected_role
        ]
        role_display = f" for {selected_role}"
    else:
        filtered_jobs = all_jobs
        role_display = " (All Roles)"
    
    if not filtered_jobs:
        st.warning(f"No jobs found for role: {selected_role}")
        return
    
    # Flatten all skills from filtered jobs
    all_skills = []
    for job in filtered_jobs:
        if job.get('skills'):
            # Parse comma-separated skills string into list
            if isinstance(job['skills'], str):
                skills_list = [s.strip() for s in job['skills'].split(',') if s.strip()]
                all_skills.extend(skills_list)
            else:
                all_skills.extend(job['skills'])
    
    # Step 1: Build canonical mapping (lowercase -> most common capitalization)
    skill_variations = {}
    for skill in all_skills:
        skill_clean = skill.strip()
        if skill_clean:
            skill_lower = skill_clean.lower()
            if skill_lower not in skill_variations:
                skill_variations[skill_lower] = {skill_clean: 1}
            else:
                if skill_clean in skill_variations[skill_lower]:
                    skill_variations[skill_lower][skill_clean] += 1
                else:
                    skill_variations[skill_lower][skill_clean] = 1
    
    # Step 2: Pick most common capitalization for each skill
    canonical_map: Dict[str, str] = {}
    for skill_lower, variations in skill_variations.items():
        # Get the variation with highest count
        max_count = max(variations.values())
        # Get all variations with max count, pick alphabetically first
        top_variations = [k for k, v in variations.items() if v == max_count]
        canonical_form: str = sorted(top_variations)[0]
        canonical_map[skill_lower] = canonical_form
    
    # Step 3: Normalize all skills using canonical map
    all_skills = [canonical_map[s.strip().lower()] for s in all_skills if s.strip()]
    
    if not all_skills:
        st.warning("No skills data available for analysis")
        return
    
    st.subheader(f"🚀 Skills Analysis - Top 50 Skills{role_display}")
    
    # Calculate total jobs from filtered set
    total_jobs = len(filtered_jobs)
    
    # Top skills analysis with percentages
    skill_counts = Counter(all_skills)
    top_skills = skill_counts.most_common(50)
    
    if top_skills:
        # Calculate percentages: (skill_count / total_jobs) * 100
        skills_data = []
        for skill, count in top_skills:
            percentage = (count / total_jobs) * 100
            skills_data.append({'Skill': skill, 'Count': count, 'Percentage': f"{percentage:.1f}%"})
        
        skills_df = pd.DataFrame(skills_data)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.bar_chart(skills_df.set_index('Skill')['Count'])
        with col2:
            st.dataframe(
                skills_df,
                width='stretch',
                hide_index=True
            )
    
    # Skills distribution metrics
    total_unique_skills = len(skill_counts)
    avg_skills_per_job = len(all_skills) / total_jobs if total_jobs > 0 else 0
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Unique Skills", total_unique_skills)
    with col2:
        st.metric("Avg Skills/Job", f"{avg_skills_per_job:.1f}")
