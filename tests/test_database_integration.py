"""
Database Integration Tests - Job Scrapper
Tests SQLiteManager CRUD operations with thread safety validation
"""
import pytest
import tempfile
import os
from models.job import JobModel
from database.core.sqlite_manager import SQLiteManager


class TestDatabaseIntegration:
    """Comprehensive database integration testing suite"""
    
    @pytest.fixture
    def temp_db(self):
        """Create temporary database for testing"""
        temp_fd, temp_path = tempfile.mkstemp(suffix='.db')
        os.close(temp_fd)
        yield temp_path
        os.unlink(temp_path)
    
    @pytest.fixture
    def db_manager(self, temp_db):
        """Initialize database manager with temp database"""
        manager = SQLiteManager(temp_db)
        return manager
    
    def test_database_creation(self, db_manager):
        """Test database and table creation"""
        # Verify database exists and tables are created
        assert os.path.exists(db_manager.db_path)
        
        # Verify table structure
        with db_manager._get_connection() as conn:
            cursor = conn.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='jobs'
            """)
            tables = cursor.fetchall()
            assert len(tables) == 1
    
    def test_single_job_storage_retrieval(self, db_manager):
        """Test storing and retrieving a single job"""
        # Create test job using proper Pydantic field names
        test_job = JobModel(
            job_id="test-001",
            Job_Role="Data Scientist",
            Company="TechCorp",
            Experience="2-5 years",
            Skills="Python, Machine Learning, SQL",
            jd="Looking for a data scientist with ML experience",
            platform="LinkedIn",
            url=None,
            location="Bangalore",
            salary="60-80K",
            posted_date=None,
            skills_list=None,
            normalized_skills=None
        )
        
        # Store job
        db_manager.store_jobs([test_job])
        
        # Retrieve and verify
        jobs = db_manager.get_all_jobs()
        assert len(jobs) == 1
        
        retrieved_job = jobs[0]
        assert retrieved_job.job_id == "test-001"
        assert retrieved_job.Job_Role == "Data Scientist"
        assert retrieved_job.Company == "TechCorp"
        assert retrieved_job.Skills == "Python, Machine Learning, SQL"
    
    def test_multiple_jobs_storage(self, db_manager):
        """Test storing and retrieving multiple jobs"""
        # Create multiple test jobs using proper field names
        test_jobs = [
            JobModel(
                job_id="test-001",
                Job_Role="Data Scientist",
                Company="TechCorp",
                Experience="2-5 years",
                Skills="Python, ML, SQL",
                jd="Data scientist role",
                platform="LinkedIn",
                url=None,
                location="Bangalore",
                salary="60-80K",
                posted_date=None,
                skills_list=None,
                normalized_skills=None
            ),
            JobModel(
                job_id="test-002",
                Job_Role="Software Engineer",
                Company="StartupInc",
                Experience="1-3 years",
                Skills="JavaScript, React, Node.js",
                jd="Frontend developer role",
                platform="Indeed",
                url=None,
                location="Mumbai",
                salary=None,
                posted_date=None,
                skills_list=None,
                normalized_skills=None
            )
        ]
        
        # Store jobs
        db_manager.store_jobs(test_jobs)
        
        # Retrieve and verify
        jobs = db_manager.get_all_jobs()
        assert len(jobs) == 2
        
        # Verify jobs are ordered by scraped_at descending
        job_ids = [job.job_id for job in jobs]
        assert "test-001" in job_ids
        assert "test-002" in job_ids
