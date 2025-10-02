#!/usr/bin/env python3
"""
JobModel Validation Tests - Pydantic v2 Field Testing
Tests JobModel validation, serialization, and field processing
EMD Compliance: ≤80 lines
"""
import pytest
from datetime import datetime
from typing import TypedDict
from pydantic import ValidationError
from src.models import JobModel


class JobTestData(TypedDict, total=False):
    """Type definition for job test data"""
    job_id: str
    Job_Role: str
    Company: str
    Experience: str
    Skills: str
    jd: str
    platform: str
    scraped_at: datetime
    url: str | None
    location: str | None
    salary: str | None
    posted_date: datetime | None
    skills_list: list[str] | None
    normalized_skills: list[str] | None


class TestJobModelValidation:
    """Test suite for JobModel Pydantic v2 validation"""
    
    @pytest.fixture
    def valid_job_data(self) -> JobTestData:
        """Create valid job data for testing"""
        return {
            "job_id": "test_001",
            "Job_Role": "Software Engineer",
            "Company": "Tech Corp",
            "Experience": "2-4 years",
            "Skills": "Python, FastAPI, PostgreSQL",
            "jd": "Software engineer role with Python",
            "platform": "LinkedIn",
            "scraped_at": datetime(2024, 1, 16)
        }
    
    def test_job_model_creation(self, valid_job_data: JobTestData) -> None:
        """Test JobModel creation with valid data"""
        job = JobModel(**valid_job_data)
        
        assert job.job_id == "test_001"
        assert job.job_role == "Software Engineer"
        assert job.company == "Tech Corp"
        assert job.platform == "LinkedIn"
        assert job.skills_list == ["Python", "FastAPI", "PostgreSQL"]
        assert job.normalized_skills == ["python", "fastapi", "postgresql"]
    
    def test_job_model_serialization(self, valid_job_data: JobTestData) -> None:
        """Test JobModel dictionary and CSV serialization"""
        job = JobModel(**valid_job_data)
        
        job_dict = job.to_dict()
        assert "job_id" in job_dict
        assert "Job_Role" in job_dict
        
        csv_row = job.to_csv_row()
        assert csv_row["job_id"] == "test_001"
        assert csv_row["Job_Role"] == "Software Engineer"
        assert csv_row["Company"] == "Tech Corp"
    
    def test_job_model_missing_required_fields(self) -> None:
        """Test JobModel validation with missing required fields"""
        incomplete_data: JobTestData = {
            "job_id": "test_003",
            "Job_Role": "Developer"
        }
        
        with pytest.raises(ValidationError):
            model_result = JobModel(**incomplete_data)
            assert model_result is not None
    
    def test_skills_parsing(self) -> None:
        """Test skills string parsing into lists"""
        job = JobModel(
            job_id="test_004",
            Job_Role="Data Scientist",
            Company="Data Corp",
            Experience="3-5 years",
            Skills="Python, Machine Learning, SQL",
            jd="Data science role",
            platform="Indeed",
            url=None,
            location=None,
            salary=None,
            posted_date=None,
            scraped_at=datetime.now(),
            skills_list=None,
            normalized_skills=None
        )
        
        assert job.skills_list is not None
        assert len(job.skills_list) == 3
        assert "Machine Learning" in job.skills_list
        assert job.normalized_skills is not None
        assert "machine learning" in job.normalized_skills
