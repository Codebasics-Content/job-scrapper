# Analytics Dashboard Helper Functions
# EMD Compliance: ≤80 lines

import pandas as pd
from typing import Any

def extract_summary_metrics(db_jobs_dicts: list[dict[str, Any]]) -> dict[str, Any]:
    """Extract summary metrics from job data"""
    skills_lists = []
    
    for job in db_jobs_dicts:
        # Parse skills from TEXT column (comma-separated) or skills_list array
        skills_raw = job.get('skills', '') or job.get('skills_list', [])
        
        if isinstance(skills_raw, str):
            skills_list = [s.strip() for s in skills_raw.split(',') if s.strip()]
        elif isinstance(skills_raw, list):
            skills_list = [str(s).strip() for s in skills_raw if s]
        else:
            skills_list = []
        
        skills_lists.append(skills_list)
    
    total_skills = sum(len(skills) for skills in skills_lists)
    avg_skills = total_skills / len(db_jobs_dicts) if db_jobs_dicts else 0
    
    unique_companies = len(set(
        str(job.get('company', 'Unknown')) for job in db_jobs_dicts
    ))
    
    unique_roles = len(set(
        str(job.get('job_role', 'Unknown')) for job in db_jobs_dicts
    ))
    
    return {
        'total_jobs': len(db_jobs_dicts),
        'avg_skills': avg_skills,
        'unique_companies': unique_companies,
        'unique_roles': unique_roles
    }

def extract_top_companies(db_jobs_dicts: list[dict[str, Any]], top_n: int = 10) -> pd.DataFrame:
    """Extract top companies hiring"""
    companies: dict[str, int] = {}
    for job in db_jobs_dicts:
        company = str(job.get('company', 'Unknown'))
        companies[company] = companies.get(company, 0) + 1
    
    top_companies = sorted(companies.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return pd.DataFrame(top_companies, columns=["Company", "Jobs"])

def extract_role_distribution(db_jobs_dicts: list[dict[str, Any]]) -> pd.DataFrame:
    """Extract role distribution data"""
    roles: dict[str, int] = {}
    for job in db_jobs_dicts:
        role = str(job.get('job_role', 'Unknown'))
        roles[role] = roles.get(role, 0) + 1
    
    return pd.DataFrame(list(roles.items()), columns=["Role", "Count"])

def prepare_export_data(db_jobs_dicts: list[dict[str, Any]]) -> pd.DataFrame:
    """Prepare comprehensive export data"""
    analytics_data = []
    
    for job in db_jobs_dicts:
        # Parse skills from TEXT column (comma-separated) or skills_list array
        skills_raw = job.get('skills', '') or job.get('skills_list', [])
        
        if isinstance(skills_raw, str):
            # Database stores as comma-separated string
            skills_list = [s.strip() for s in skills_raw.split(',') if s.strip()]
        elif isinstance(skills_raw, list):
            # Already a list
            skills_list = [str(s).strip() for s in skills_raw if s]
        else:
            skills_list = []
        
        analytics_data.append({
            "Job Role": str(job.get('job_role', 'Unknown')),
            "Company": str(job.get('company', 'Unknown')),
            "Location": str(job.get('location', 'Unknown')),
            "Experience": str(job.get('experience', '')),
            "Skills Count": len(skills_list),
            "Skills": ", ".join(skills_list),
            "Posted Date": str(job.get('posted_date', '')),
            "Platform": str(job.get('platform', '')),
            "Job URL": str(job.get('url', ''))
        })
    
    return pd.DataFrame(analytics_data)
