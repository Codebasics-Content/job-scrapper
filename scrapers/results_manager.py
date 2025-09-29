# Job Scrapper - Results Management Coordinator
# EMD Compliance: ≤80 lines for coordination layer

import logging
from models.job import JobModel
from scrapers.results.statistics.generator import StatisticsGenerator
from scrapers.results.export.formatter import ExportFormatter

logger = logging.getLogger(__name__)

class ResultsManager:
    """
    Coordinates results management and delegates to specialized modules
    Acts as facade for statistics generation and export formatting
    """
    
    def __init__(self):
        self.processed_jobs: list[JobModel] = []
        self.stats_generator: StatisticsGenerator = StatisticsGenerator()
        self.export_formatter: ExportFormatter = ExportFormatter()
        
    def process_job_results(self, jobs: list[JobModel]) -> None:
        """Process and store job results for analysis"""
        self.processed_jobs = jobs
        logger.info(f"Processed {len(jobs)} job results for analysis")
        
    def generate_statistics_report(self) -> dict[str, str | int | float | dict[str, float] | dict[str, int]]:
        """
        Generate comprehensive statistics report
        Delegates to StatisticsGenerator for calculation
        """
        return self.stats_generator.generate_report(self.processed_jobs)
        
    def export_results_summary(self) -> str:
        """
        Export formatted results summary
        Delegates to ExportFormatter for presentation
        """
        stats = self.generate_statistics_report()
        return self.export_formatter.format_summary(stats)
