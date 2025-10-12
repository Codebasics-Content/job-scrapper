"""Store JobSpy scraped jobs to SQLite database (≤80 lines EMD)"""
import pandas as pd
from src.db.operations import store_jobs
from src.models import JobModel


def store_jobspy_to_db(jobs_df: pd.DataFrame) -> int:
    """
    Convert JobSpy DataFrame to JobModel and store to database
    
    Args:
        jobs_df: DataFrame from JobSpy scraper
    
    Returns:
        Number of jobs stored
    """
    if jobs_df is None or len(jobs_df) == 0:
        return 0
    
    job_models = []
    
    for index, row in jobs_df.iterrows():
        # Convert JobSpy data to JobModel format
        job_model = JobModel(
            platform="linkedin",
            url=row.get('job_url', ''),
            title=row.get('title', ''),
            company=row.get('company', ''),
            location=row.get('location', ''),
            job_type=row.get('job_type', ''),
            description=row.get('description', ''),
            date_posted=row.get('date_posted', ''),
            salary=_format_salary(row),
            skills=row.get('skills_str', '') if 'skills_str' in row else '',
            experience_level=row.get('job_level', ''),
            company_size=row.get('company_num_employees', ''),
            industry=row.get('company_industry', ''),
            remote=row.get('is_remote', False)
        )
        job_models.append(job_model)
    
    # Store to database
    stored_count = store_jobs(job_models)
    
    return stored_count


def _format_salary(row: pd.Series) -> str:
    """Format salary information from JobSpy row"""
    min_amount = row.get('min_amount', '')
    max_amount = row.get('max_amount', '')
    currency = row.get('currency', 'USD')
    interval = row.get('interval', '')
    
    if not min_amount and not max_amount:
        return ''
    
    if min_amount and max_amount:
        return f"{currency} {min_amount}-{max_amount}/{interval}"
    elif min_amount:
        return f"{currency} {min_amount}+/{interval}"
    else:
        return f"{currency} up to {max_amount}/{interval}"
