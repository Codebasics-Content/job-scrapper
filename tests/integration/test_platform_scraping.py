"""Platform-specific scraping tests with database validation"""
import sqlite3
from pathlib import Path

import pytest

from src.db import DatabaseConnection, JobStorageOperations
from src.scraper.unified.linkedin_unified import scrape_linkedin_jobs
from src.scraper.unified.indeed_unified import scrape_indeed_jobs
from src.scraper.unified.naukri_unified import scrape_naukri_jobs


TEST_DB = "jobs_integration_test.db"
JOB_ROLE = "AI Engineer"
NUM_JOBS = 100


@pytest.fixture(scope="module")
def setup_database():
    """Initialize test database"""
    db_path = Path(TEST_DB)
    if db_path.exists():
        db_path.unlink()
    
    with DatabaseConnection(TEST_DB) as conn:
        JobStorageOperations.create_tables(conn)
    
    yield TEST_DB
    
    # Cleanup
    if db_path.exists():
        db_path.unlink()


def validate_job_data(job, platform):
    """Validate job has required fields"""
    assert job.job_id, f"{platform}: Missing job_id"
    assert job.jd, f"{platform}: Missing job description"
    assert job.platform == platform.lower(), f"{platform}: Wrong platform"
    assert job.skills, f"{platform}: Missing skills"
    assert len(job.skills_list) > 0, f"{platform}: No skills extracted"


def test_linkedin_scraping(setup_database):
    """Test LinkedIn scraping and database storage"""
    jobs = scrape_linkedin_jobs(JOB_ROLE, NUM_JOBS)
    
    assert len(jobs) > 0, "No jobs scraped from LinkedIn"
    assert len(jobs) <= NUM_JOBS, f"Scraped too many jobs: {len(jobs)}"
    
    # Validate first job
    validate_job_data(jobs[0], "LinkedIn")
    
    # Store in database
    with DatabaseConnection(setup_database) as conn:
        stored = JobStorageOperations.bulk_insert_jobs(conn, jobs)
    
    assert stored == len(jobs), f"Storage mismatch: {stored} != {len(jobs)}"
