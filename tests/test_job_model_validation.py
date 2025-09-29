#!/usr/bin/env python3
"""
JobModel Validation Tests - Pydantic v2 Field Testing
Tests JobModel validation, serialization, and field processing
EMD Compliance: ≤80 lines
"""
import pytest
from datetime import datetime
from pydantic import ValidationError
from models.job import JobModel


class TestJobModelValidation:
    """Test suite for JobModel Pydantic v2 validation"""
    
    @pytest.fixture
    def valid_job_data(self):
        """Create valid job data for testing"""
        return {
            "job_id": "test_001",
            "job_role": "Software Engineer",
            "company": "Tech Corp",
            "experience": "2-4 years",
            "skills": "Python, FastAPI, PostgreSQL",
            "jd": "Software engineer role with Python",
            "platform": "LinkedIn",
            "scraped_at": datetime(2024, 1, 16)
        }
    
    def test_job_model_creation(self, valid_job_data):
        """Test JobModel creation with valid data"""
        job = JobModel(**valid_job_data)
        
        assert job.job_id == "test_001"
        assert job.job_role == "Software Engineer"
        assert job.company == "Tech Corp"
        assert job.platform == "LinkedIn"
        assert job.skills_list == ["Python", "FastAPI", "PostgreSQL"]
        assert job.normalized_skills == ["python", "fastapi", "postgresql"]
    
    def test_job_model_serialization(self, valid_job_data):
        """Test JobModel dictionary and CSV serialization"""
        job = JobModel(**valid_job_data)
        
        job_dict = job.to_dict()
        assert "job_id" in job_dict
        assert "Job_Role" in job_dict
        
        csv_row = job.to_csv_row()
        assert csv_row["job_id"] == "test_001"
        assert csv_row["Job_Role"] == "Software Engineer"
        assert csv_row["Company"] == "Tech Corp"
    
    def test_job_model_missing_required_fields(self):
        """Test JobModel validation with missing required fields"""
        incomplete_data = {
            "job_id": "test_003",
            "job_role": "Developer"
        }
        
        with pytest.raises(ValidationError) as exc_info:
            JobModel(**incomplete_data)
        
        assert exc_info.value.error_count() > 0
    
    def test_skills_parsing(self):
        """Test skills string parsing into lists"""
        job = JobModel(
            job_id="test_004",
            job_role="Data Scientist",
            company="Data Corp",
            experience="3-5 years",
            skills="Python, Machine Learning, SQL",
            jd="Data science role",
            platform="Indeed",
            scraped_at=datetime.now()
        )
        
        assert len(job.skills_list) == 3
        assert "Machine Learning" in job.skills_list
        assert "machine learning" in job.normalized_skills
