"""Full integration test for all 3 platforms with skill validation"""
import json
import subprocess
from pathlib import Path
from collections import defaultdict

import pytest

from src.db import DatabaseConnection, JobStorageOperations
from src.scraper.unified.linkedin_unified import scrape_linkedin_jobs
from src.scraper.unified.indeed_unified import scrape_indeed_jobs
from src.scraper.unified.naukri_unified import scrape_naukri_jobs


# Test configuration
TEST_CONFIG = {
    "job_role": "Data Scientist",
    "num_jobs": 100,
    "platforms": ["LinkedIn", "Indeed", "Naukri"],
    "db_path": "jobs_test.db",
    "skills_ref": "skills_reference_2025.json"
}


@pytest.fixture(scope="module")
def check_docker_services():
    """Verify Docker services are running"""
    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
            check=True
        )
        containers = result.stdout.strip().split("\n")
        
        required = ["headlessx", "proxy"]
        running = [c for c in containers if any(r in c.lower() for r in required)]
        
        if len(running) < 2:
            pytest.skip(f"Docker services not running. Found: {running}")
        
        return running
    except subprocess.CalledProcessError:
        pytest.skip("Docker daemon not running")


@pytest.fixture(scope="module")
def skills_reference():
    """Load skills reference database"""
    ref_path = Path(TEST_CONFIG["skills_ref"])
    with open(ref_path) as f:
        data = json.load(f)
    
    # Flatten all skills with patterns
    all_skills = {}
    for category, skills_list in data["skills"].items():
        for skill in skills_list:
            all_skills[skill["name"].lower()] = {
                "category": category,
                "patterns": skill["patterns"]
            }
    
    return all_skills
