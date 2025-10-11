"""Unified API integration test for all platforms"""
import sqlite3
from pathlib import Path
from datetime import datetime

import pytest

from src.db import DatabaseConnection, JobStorageOperations
from src.scraper.unified.linkedin_unified import scrape_linkedin_jobs
from src.scraper.unified.indeed_unified import scrape_indeed_jobs  
from src.scraper.unified.naukri_unified import scrape_naukri_jobs


TEST_CONFIG = {
    "db_path": "unified_test.db",
    "job_role": "Machine Learning Engineer",
    "jobs_per_platform": 100
}


@pytest.fixture(scope="module")
def test_database():
    """Setup test database"""
    db = Path(TEST_CONFIG["db_path"])
    if db.exists():
        db.unlink()
    
    with DatabaseConnection(TEST_CONFIG["db_path"]) as conn:
        JobStorageOperations.create_tables(conn)
    
    yield TEST_CONFIG["db_path"]
    
    # Keep database for manual inspection
    print(f"\n✓ Test database: {TEST_CONFIG['db_path']}")


@pytest.mark.order(1)
def test_linkedin_unified(test_database):
    """Test LinkedIn unified API"""
    jobs = scrape_linkedin_jobs(
        TEST_CONFIG["job_role"],
        TEST_CONFIG["jobs_per_platform"]
    )
    
    assert len(jobs) > 0, "LinkedIn: No jobs scraped"
    
    with DatabaseConnection(test_database) as conn:
        stored = JobStorageOperations.bulk_insert_jobs(conn, jobs)
    
    assert stored > 0, "LinkedIn: Storage failed"
    print(f"\n✓ LinkedIn: {stored} jobs")


@pytest.mark.order(2) 
def test_indeed_unified(test_database):
    """Test Indeed unified API"""
    jobs = scrape_indeed_jobs(
        TEST_CONFIG["job_role"],
        TEST_CONFIG["jobs_per_platform"]
    )
    
    assert len(jobs) > 0, "Indeed: No jobs scraped"
    
    with DatabaseConnection(test_database) as conn:
        stored = JobStorageOperations.bulk_insert_jobs(conn, jobs)
    
    assert stored > 0, "Indeed: Storage failed"
    print(f"\n✓ Indeed: {stored} jobs")


@pytest.mark.order(3)
def test_naukri_unified(test_database):
    """Test Naukri unified API"""
    jobs = scrape_naukri_jobs(
        TEST_CONFIG["job_role"],
        TEST_CONFIG["jobs_per_platform"]
    )
    
    assert len(jobs) > 0, "Naukri: No jobs scraped"
    
    with DatabaseConnection(test_database) as conn:
        stored = JobStorageOperations.bulk_insert_jobs(conn, jobs)
    
    assert stored > 0, "Naukri: Storage failed"
    print(f"\n✓ Naukri: {stored} jobs")
