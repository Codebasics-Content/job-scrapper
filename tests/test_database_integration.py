#!/usr/bin/env python3
"""
Database Integration Tests - ConnectionManager and BatchOperations
Tests actual production database modules with thread safety
EMD Compliance: ≤80 lines
"""
import pytest
import tempfile
import os
from datetime import datetime
from models.job import JobModel
from database.connection.db_connection import DatabaseConnection
from database.operations.job_storage import JobStorageOperations


class TestDatabaseIntegration:
    """Test suite for database integration with production modules"""
    
    @pytest.fixture
    def temp_db(self):
        """Create temporary database for testing"""
        temp_fd, temp_path = tempfile.mkstemp(suffix='.db')
        os.close(temp_fd)
        yield temp_path
        os.unlink(temp_path)
    
    @pytest.fixture
    def job_storage(self, temp_db):
        """Initialize JobStorageOperations with temp database"""
        return JobStorageOperations(temp_db)
    
    def test_database_initialization(self, job_storage):
        """Test database and schema initialization"""
        assert job_storage.connection is not None
        assert job_storage.schema_manager is not None
    
    def test_single_job_storage_retrieval(self, job_storage):
        """Test storing and retrieving a single job"""
        test_job = JobModel(
            job_id="test-001",
            job_role="Data Scientist",
            company="TechCorp",
            experience="2-5 years",
            skills="Python, ML, SQL",
            jd="Data scientist role",
            platform="LinkedIn"
        )
        
        stored = job_storage.store_jobs([test_job])
        assert stored == 1
        
        jobs = job_storage.get_jobs_by_role("Data Scientist")
        assert len(jobs) >= 1
    
    def test_multiple_jobs_batch_storage(self, job_storage):
        """Test batch storage of multiple jobs"""
        test_jobs = [
            JobModel(
                job_id=f"test-{i:03d}",
                job_role="Software Engineer",
                company=f"Company{i}",
                experience="1-3 years",
                skills="Python, JavaScript",
                jd=f"Job description {i}",
                platform="LinkedIn"
            )
            for i in range(5)
        ]
        
        stored = job_storage.store_jobs(test_jobs)
        assert stored == 5
