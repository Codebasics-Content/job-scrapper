# Job Scrapper - Export Formatter Module
# EMD Compliance: ≤80 lines for result formatting

import logging

logger = logging.getLogger(__name__)

class ExportFormatter:
    """
    Formats statistics reports for console output
    Handles result presentation and summary generation
    """
    
    def format_summary(self, stats: dict[str, object]) -> str:
        """Export statistics in formatted string for console"""
        if "error" in stats:
            return f"Statistics Error: {stats['error']}"
        
        summary_lines = self._build_header(stats)
        summary_lines.extend(self._format_top_skills(stats))
        
        return "\n".join(summary_lines)
    
    def _build_header(self, stats: dict[str, object]) -> list[str]:
        """Build summary header with job counts"""
        return [
            f"=== Job Scrapping Results Summary ===",
            f"Total Jobs Collected: {stats['total_jobs']}",
            f"Platforms Scraped: {stats['platforms_scraped']}",
            f"Top Skills Found:",
        ]
    
    def _format_top_skills(self, stats: dict[str, object]) -> list[str]:
        """Format top 10 skills with percentages"""
        skill_lines = []
        top_skills = list(stats['skill_percentages'].items())[:10]
        
        for skill, percentage in top_skills:
            skill_lines.append(f"  {skill}: {percentage}%")
        
        return skill_lines
