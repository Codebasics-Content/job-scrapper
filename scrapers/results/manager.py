# Results Manager - Main coordinator for results management
# EMD Compliance: ≤80 lines for orchestration

import logging
from models.job import JobModel
from scrapers.results.processing.aggregator import JobAggregator
from scrapers.results.statistics.calculator import StatisticsCalculator
from scrapers.results.reporting.formatter import ReportFormatter

logger = logging.getLogger(__name__)

class ResultsManager:
    """
    Main coordinator for results management
    Orchestrates job processing, statistics, and reporting
    """
    
    def __init__(self):
        self.aggregator = JobAggregator()
        self.calculator = StatisticsCalculator()
        self.formatter = ReportFormatter()
        
    def process_job_results(self, jobs: list[JobModel]) -> None:
        """Process and store job results for analysis"""
        self.aggregator.process_job_results(jobs)
        
    def generate_statistics_report(self) -> dict:
        """
        Generate comprehensive skill percentage statistics
        Returns structured report with top skills and metrics
        """
        if not self.aggregator.has_jobs():
            logger.warning("No jobs available for statistics generation")
            return {"error": "No jobs to analyze", "total_jobs": 0}
        
        jobs = self.aggregator.get_all_jobs()
        all_skills = self.aggregator.get_unique_skills()
        platform_counts = self.aggregator.get_platform_distribution()
        
        return self.calculator.generate_statistics_report(
            jobs, all_skills, platform_counts
        )
        
    def export_results_summary(self) -> str:
        """Export results in formatted string for console output"""
        stats = self.generate_statistics_report()
        return self.formatter.export_results_summary(stats)
