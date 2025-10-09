#!/usr/bin/env python3
# Type definitions for Naukri scraper
# EMD Compliance: ≤80 lines

from typing import TypedDict


class CompanyDetail(TypedDict, total=False):
    """Type definition for company detail in bulk API data."""
    name: str


class BulkJobData(TypedDict, total=False):
    """Type definition for bulk API job data structure."""
    jobDescription: str
    companyDetail: CompanyDetail
    tagsAndSkills: str


class JobCardHTML(TypedDict):
    """Structure for storing job card HTML temporarily."""
    job_id: str
    html_content: str
    card_index: int


class ScrapingMetrics(TypedDict):
    """Metrics tracking for scraping performance."""
    total_processed: int
    successful_extractions: int
    failed_extractions: int
    batch_count: int
    processing_time: float


class BatchConfig(TypedDict):
    """Configuration for batch processing."""
    batch_size: int
    max_retries: int
    timeout_seconds: int
    memory_cleanup_threshold: int
