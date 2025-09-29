# Report Formatter - Exports results in formatted output
# EMD Compliance: ≤80 lines for report generation

class ReportFormatter:
    """
    Formats statistical reports for console output
    Provides readable summary of scraping results
    """
    
    def export_results_summary(self, stats: dict) -> str:
        """Export results in formatted string for console output"""
        if "error" in stats:
            return f"Statistics Error: {stats['error']}"
        
        summary_lines = [
            "=== Job Scrapping Results Summary ===",
            f"Total Jobs Collected: {stats['total_jobs']}",
            f"Platforms Scraped: {stats['platforms_scraped']}",
            "Top Skills Found:",
        ]
        
        # Add top 10 skills to summary
        top_skills = list(stats['skill_percentages'].items())[:10]
        for skill, percentage in top_skills:
            summary_lines.append(f"  {skill}: {percentage}%")
            
        return "\n".join(summary_lines)
