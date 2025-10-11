#!/usr/bin/env python3
"""Role-Based Advanced Chart Visualization - EMD Compliant
Generates comprehensive charts for job role analysis including:
- Role distribution horizontal bar charts
- Skill comparison across roles (stacked bars)
- Role-skill correlation heatmaps
"""
import logging
from collections import Counter, defaultdict
from collections.abc import Sequence
import pandas as pd
import numpy as np
from src.models import JobModel

logger = logging.getLogger(__name__)

def generate_role_distribution(
    jobs: Sequence[JobModel | dict[str, object]]
) -> pd.DataFrame:
    """Generate role distribution data for horizontal bar chart
    
    Args:
        jobs: List of job models
        
    Returns:
        DataFrame with roles and their job counts, sorted descending
    """
    if not jobs:
        logger.warning("No jobs provided for role distribution")
        return pd.DataFrame(columns=['role', 'count'])
    
    role_counter: Counter[str] = Counter()
    
    for job in jobs:
        role = None
        if isinstance(job, dict):
            role = job.get('job_role') or job.get('Job_Role')
        elif hasattr(job, 'Job_Role'):
            role = getattr(job, 'Job_Role')
        
        if role:
            role_counter[str(role)] += 1
    
    df = pd.DataFrame(role_counter.most_common(), columns=['role', 'count'])
    logger.info(f"Generated role distribution for {len(df)} unique roles")
    return df

def generate_skill_by_role_matrix(
    jobs: Sequence[JobModel | dict[str, object]],
    top_roles: int = 10,
    top_skills: int = 15
) -> pd.DataFrame:
    """Generate skill-role matrix for stacked bar chart or heatmap
    
    Args:
        jobs: List of job models
        top_roles: Number of top roles to include
        top_skills: Number of top skills to include
        
    Returns:
        DataFrame with roles as index, skills as columns, values are percentages
    """
    if not jobs:
        logger.warning("No jobs for skill-role matrix")
        return pd.DataFrame()
    
    # Build role -> skills mapping
    role_skills_map: dict[str, list[list[str]]] = defaultdict(list)
    
    for job in jobs:
        role = None
        skills: list[str] | None = None
        
        if isinstance(job, dict):
            role = job.get('job_role') or job.get('Job_Role')
            raw_skills = job.get('normalized_skills') or job.get('skills_list')
            if isinstance(raw_skills, list):
                skills = [str(s) for s in raw_skills if s]
            elif 'skills' in job and isinstance(job['skills'], str):
                skills_str = job['skills']
                if skills_str:
                    skills = [s.strip().lower() for s in skills_str.split(',') if s.strip()]
        elif hasattr(job, 'Job_Role'):
            role = getattr(job, 'Job_Role')
            if hasattr(job, 'normalized_skills'):
                raw_attr = getattr(job, 'normalized_skills')
                if isinstance(raw_attr, list):
                    skills = [str(s) for s in raw_attr if s]
        
        if role and skills:
            role_skills_map[str(role)].append(skills)
    
    if not role_skills_map:
        return pd.DataFrame()
    
    # Get top roles by job count
    role_counts = {role: len(skill_lists) for role, skill_lists in role_skills_map.items()}
    top_role_names = [role for role, _ in sorted(role_counts.items(), key=lambda x: x[1], reverse=True)[:top_roles]]
    
    # Get top skills overall
    all_skills_counter: Counter[str] = Counter()
    for skill_lists in role_skills_map.values():
        for skills in skill_lists:
            all_skills_counter.update(set(skills))
    top_skill_names = [skill for skill, _ in all_skills_counter.most_common(top_skills)]
    
    # Build matrix
    matrix_data = []
    for role in top_role_names:
        skill_lists = role_skills_map[role]
        total_jobs = len(skill_lists)
        
        role_row = {'role': role}
        for skill in top_skill_names:
            # Count jobs in this role that have this skill
            count = sum(1 for skills in skill_lists if skill in skills)
            percentage = round((count / total_jobs) * 100, 1) if total_jobs > 0 else 0
            role_row[skill] = percentage
        
        matrix_data.append(role_row)
    
    df = pd.DataFrame(matrix_data)
    df = df.set_index('role')
    
    logger.info(f"Generated {len(df)}x{len(df.columns)} skill-role matrix")
    return df

def generate_role_skill_heatmap_data(
    jobs: Sequence[JobModel | dict[str, object]],
    top_roles: int = 10,
    top_skills: int = 15
) -> dict[str, object]:
    """Generate heatmap data for role-skill correlation
    
    Args:
        jobs: List of job models
        top_roles: Number of roles to include
        top_skills: Number of skills to include
        
    Returns:
        Dict with 'roles', 'skills', and 'values' (2D array)
    """
    matrix_df = generate_skill_by_role_matrix(jobs, top_roles, top_skills)
    
    if matrix_df.empty:
        return {'roles': [], 'skills': [], 'values': []}
    
    return {
        'roles': matrix_df.index.tolist(),
        'skills': matrix_df.columns.tolist(),
        'values': matrix_df.values.tolist()
    }

def prepare_stacked_bar_data(
    jobs: Sequence[JobModel | dict[str, object]],
    top_roles: int = 10,
    top_skills: int = 10
) -> pd.DataFrame:
    """Prepare data for stacked bar chart showing skills per role
    
    Returns:
        DataFrame ready for Streamlit stacked bar visualization
    """
    matrix_df = generate_skill_by_role_matrix(jobs, top_roles, top_skills)
    
    if matrix_df.empty:
        return pd.DataFrame()
    
    # Transpose for better stacked bar visualization (skills as categories, roles as series)
    return matrix_df.T
