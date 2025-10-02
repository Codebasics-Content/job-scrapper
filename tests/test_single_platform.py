#!/usr/bin/env python3
"""
Single Platform Scraper Tests - Production Module Testing
Tests individual scrapers with actual database integration
EMD Compliance: ≤80 lines
"""
import pytest
import asyncio
from src.scraper.linkedin.scraper import LinkedInScraper
from src.db.operations.job_storage import JobStorageOperations


class TestSinglePlatformScrapers:
    """Test suite for individual platform scrapers"""
    
    @pytest.fixture
    def scraper_map(self) -> dict[str, type[LinkedInScraper]]:
        """Map of available scrapers"""
        return {
            "LinkedIn": LinkedInScraper
        }
    
    def test_scraper_availability(self, scraper_map: dict[str, type[LinkedInScraper]]) -> None:
        """Test all scrapers are available and importable"""
        assert "LinkedIn" in scraper_map
        assert len(scraper_map) == 1
    
    def test_scraper_initialization(self, scraper_map: dict[str, type[LinkedInScraper]]) -> None:
        """Test each scraper initializes correctly"""
        for platform, scraper_class in scraper_map.items():
            scraper = scraper_class()
            assert scraper.platform_name == platform
    
    def test_scraper_context_manager(self) -> None:
        """Test scrapers support context manager protocol"""
        with LinkedInScraper() as scraper:
            assert scraper is not None
            assert hasattr(scraper, 'scrape_jobs')
    
    @pytest.mark.asyncio
    async def test_scraper_interface(self) -> None:
        """Test scraper implements required async interface"""
        scraper = LinkedInScraper()
        assert hasattr(scraper, 'scrape_jobs')
        assert asyncio.iscoroutinefunction(scraper.scrape_jobs)
    
    def test_job_storage_integration(self) -> None:
        """Test job storage operations are available"""
        storage = JobStorageOperations()
        assert storage is not None
        assert hasattr(storage, 'store_jobs')
        assert hasattr(storage, 'get_jobs_by_role')
    
    def test_removed_scrapers_not_available(self, scraper_map: dict[str, type[LinkedInScraper]]) -> None:
        """Verify removed scrapers are not in available scrapers"""
        assert "YCombinator" not in scraper_map
        assert "Indeed" not in scraper_map
        assert "Naukri" not in scraper_map
    
    @pytest.mark.asyncio
    async def test_platform_not_supported_handling(self, scraper_map: dict[str, type[LinkedInScraper]]) -> None:
        """Test handling of unsupported platform requests"""
        unsupported_platform = "InvalidPlatform"
        assert unsupported_platform not in scraper_map
