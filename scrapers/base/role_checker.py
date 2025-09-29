# Universal job role relevance checker - cross-platform
# EMD Compliance: ≤80 lines

import logging

logger = logging.getLogger(__name__)

# Codebasics target job roles for filtering
CODEBASICS_JOB_ROLES = [
    'data scientist', 'data analyst', 'machine learning', 'ml engineer',
    'data engineer', 'python developer', 'sql analyst', 'business analyst',
    'ai engineer', 'deep learning', 'data science', 'analytics', 'tableau',
    'power bi', 'excel analyst', 'statistician', 'quantitative analyst',
    'research analyst', 'data visualization', 'bi developer'
]

def is_codebasics_relevant_role(job_title: str) -> bool:
    """Check if job title matches Codebasics target roles"""
    if not job_title:
        return False
    
    title_lower = job_title.lower()
    for target_role in CODEBASICS_JOB_ROLES:
        if target_role in title_lower:
            return True
    
    logger.debug(f"Job title '{job_title}' not relevant to Codebasics")
    return False
