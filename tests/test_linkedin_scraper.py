#!/usr/bin/env python3
"""
LinkedIn Scraper Tests - API-based Implementation
Tests async LinkedIn scraper with proper fixtures and mocking
EMD Compliance: ≤80 lines
"""
import pytest
import asyncio
from unittest.mock import Mock, patch, MagicMock
from models.job import JobModel
from scrapers.linkedin.scraper import LinkedInScraper


class TestLinkedInScraper:
    """Test suite for LinkedIn API-based scraper"""
    
    @pytest.fixture
    def scraper(self):
        """Initialize LinkedIn scraper for testing"""
        return LinkedInScraper()
    
    @pytest.fixture
    def mock_driver(self):
        """Create mock WebDriver for testing"""
        driver = MagicMock()
        driver.get = Mock()
        driver.execute_script = Mock(return_value=None)
        return driver
    
    @pytest.fixture
    def sample_jobs(self):
        """Create sample JobModel instances for testing"""
        return [
            JobModel(
                job_id=f"test-{i}",
                job_role="Python Developer",
                company=f"Company{i}",
                experience="2-5 years",
                skills="Python, Django, REST APIs",
                jd=f"Job description {i}",
                platform="LinkedIn"
            )
            for i in range(3)
        ]
    
    def test_scraper_initialization(self, scraper):
        """Test LinkedIn scraper initializes correctly"""
        assert scraper.platform_name == "LinkedIn"
        assert scraper.base_url == "https://www.linkedin.com/jobs/search"
    
    @pytest.mark.asyncio
    async def test_scrape_jobs_basic(self, scraper, mock_driver, sample_jobs):
        """Test basic job scraping with mocked driver"""
        with patch.object(scraper, 'get_driver', return_value=mock_driver):
            with patch.object(scraper, 'return_driver'):
                with patch('scrapers.linkedin.extractors.job_id_extractor.extract_job_ids_from_page', 
                          return_value=['job1', 'job2', 'job3']):
                    with patch('scrapers.linkedin.extractors.api_job_fetcher.fetch_job_via_api',
                              side_effect=sample_jobs):
                        jobs = await scraper.scrape_jobs("Python Developer", 3)
                        
                        assert len(jobs) == 3
                        assert all(job.platform == "LinkedIn" for job in jobs)
    
    def test_context_manager_protocol(self, scraper):
        """Test scraper supports context manager protocol"""
        assert hasattr(scraper, '__enter__')
        assert hasattr(scraper, '__exit__')
