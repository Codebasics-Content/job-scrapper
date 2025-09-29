# Job Model Validation Tests - EMD Compliance: ≤80 lines
# Tests for JobModel Pydantic validation and field processing
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
# ValidationError imported but used in pytest.raises context
from models.job import JobModel
import pytest

def test_job_model_creation_with_valid_data():
    """Test JobModel creation with all required fields"""
    valid_job_data = {
        "job_id": "test_001",
        "job_role": "Software Engineer",
        "company": "Tech Corp",
        "experience": "2-4 years",
        "skills": "Python, FastAPI, PostgreSQL",
        "jd": "We are looking for a skilled software engineer...",
        "platform": "LinkedIn",
        "url": "https://linkedin.com/jobs/123",
        "location": "San Francisco, CA",
        "salary": "$80,000 - $120,000",
        "posted_date": datetime(2024, 1, 15),
        "scraped_at": datetime(2024, 1, 16)
    }
    
    job = JobModel(**valid_job_data)
    
    # Verify all fields are set correctly
    assert job.job_id == "test_001"
    assert job.job_role == "Software Engineer"
    assert job.company == "Tech Corp"
    assert job.experience == "2-4 years"
    assert job.skills == "Python, FastAPI, PostgreSQL"
    assert job.jd == "We are looking for a skilled software engineer..."
    assert job.platform == "LinkedIn"
    assert job.url == "https://linkedin.com/jobs/123"
    assert job.location == "San Francisco, CA"
    assert job.salary == "$80,000 - $120,000"
    assert job.posted_date == datetime(2024, 1, 15)
    assert job.scraped_at == datetime(2024, 1, 16)
    # Test that validators parsed skills correctly
    assert job.skills_list == ["Python", "FastAPI", "PostgreSQL"]
    assert job.normalized_skills == ["python", "fastapi", "postgresql"]

def test_job_model_serialization():
    """Test JobModel to_dict and to_csv_row methods"""
    job_data = {
        "job_id": "test_002",
        "job_role": "Data Scientist", 
        "company": "Data Inc",
        "experience": "3-5 years",
        "skills": "Python, Machine Learning, SQL",
        "jd": "Data scientist role for ML projects",
        "platform": "Indeed",
        "scraped_at": datetime(2024, 1, 16)
    }
    
    job = JobModel(**job_data)
    
    # Test dictionary conversion
    job_dict = job.to_dict()
    assert "job_id" in job_dict
    assert "Job_Role" in job_dict  # Alias field
    
    # Test CSV row conversion
    csv_row = job.to_csv_row()
    assert csv_row["job_id"] == "test_002"
    assert csv_row["Job_Role"] == "Data Scientist"
    assert csv_row["Company"] == "Data Inc"
    assert csv_row["platform"] == "Indeed"

def test_job_model_validation_errors():
    """Test JobModel validation with missing required fields"""
    incomplete_data = {
        "job_id": "test_003",
        "job_role": "Developer",
        # Missing required fields: company, experience, skills, jd, platform, scraped_at
    }
    
    with pytest.raises(ValueError):
        job_result = JobModel(**incomplete_data)
        print(f"Job created unexpectedly: {job_result}")

if __name__ == "__main__":
    test_job_model_creation_with_valid_data()
    test_job_model_serialization()
    print("✅ JobModel validation tests passed!")
