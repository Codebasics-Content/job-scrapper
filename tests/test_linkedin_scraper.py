#!/usr/bin/env python3
"""
LinkedIn Scraper Tests - API-based Implementation
Tests async LinkedIn scraper with proper fixtures and mocking
EMD Compliance: ≤80 lines
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.models import JobModel
from src.scraper.linkedin.scraper import LinkedInScraper


class TestLinkedInScraper:
    """Test suite for LinkedIn API-based scraper"""
    
    @pytest.fixture
    def scraper(self) -> LinkedInScraper:
        """Initialize LinkedIn scraper for testing"""
        return LinkedInScraper()
    
    @pytest.fixture
    def mock_driver(self) -> MagicMock:
        """Create mock WebDriver for testing"""
        driver = MagicMock()
        driver.get = Mock()
        driver.execute_script = Mock(return_value=None)
        return driver
    
    @pytest.fixture
    def sample_jobs(self) -> list[JobModel]:
        """Create sample JobModel instances for testing"""
        return [
            JobModel(
                job_id=f"test-{i}",
                Job_Role="Python Developer",
                Company=f"Company{i}",
                Experience="2-5 years",
                Skills="Python, Django, REST APIs",
                jd=f"Job description {i}",
                platform="LinkedIn",
                url=None,
                location=None,
                salary=None,
                posted_date=None,
                skills_list=None,
                normalized_skills=None
            )
            for i in range(3)
        ]
    
    def test_scraper_initialization(self, scraper: LinkedInScraper) -> None:
        """Test LinkedIn scraper initializes correctly"""
        assert scraper.platform_name == "LinkedIn"
        assert scraper.base_url == "https://www.linkedin.com/jobs/search"
    
    @pytest.mark.asyncio
    async def test_scrape_jobs_basic(self, scraper: LinkedInScraper, mock_driver: MagicMock, sample_jobs: list[JobModel]) -> None:
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
    
    def test_context_manager_protocol(self, scraper: LinkedInScraper) -> None:
        """Test scraper supports context manager protocol"""
        assert hasattr(scraper, '__enter__')
        assert hasattr(scraper, '__exit__')
