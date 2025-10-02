#!/usr/bin/env python3
"""
Skill Analysis Report Formatter - EMD Compliant Module

Creates professional report output matching requirements format:
RAG: 89%, Langchain: 62%, Crew AI: 41%

EMD Compliance: ≤80 lines, single responsibility principle.
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ReportFormatter:
    """Format skill analysis results into professional reports"""
    
    report_timestamp: str
    
    def __init__(self) -> None:
        self.report_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def format_skill_report(
        self, 
        role: str, 
        skill_percentages: dict[str, float],
        total_jobs: int
    ) -> str:
        """Generate formatted skill analysis report"""
        
        if not skill_percentages:
            logger.warning("No skill data provided for report")
            return "No skill analysis data available"
        
        # Sort skills by percentage (descending)
        sorted_skills = sorted(
            skill_percentages.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        # Build report
        report_lines = [
            f"=" * 60,
            f"SKILL ANALYSIS REPORT - {role.upper()}",
            f"Generated: {self.report_timestamp}",
            f"Total Jobs Analyzed: {total_jobs}",
            f"=" * 60,
            ""
        ]
        
        # Add skill percentages
        for skill, percentage in sorted_skills:
            if percentage > 0:  # Only show skills that appear in jobs
                report_lines.append(f"{skill}: {percentage}%")
        
        report_lines.extend([
            "",
            f"=" * 60,
            f"Report completed at {self.report_timestamp}"
        ])
        
        report_content = "\n".join(report_lines)
        logger.info(f"Generated skill report for {role} with {len(sorted_skills)} skills")
        
        return report_content
    
    def format_console_output(self, skill_percentages: dict[str, float]) -> str:
        """Format skill percentages for console display"""
        
        if not skill_percentages:
            return "No skills found"
        
        sorted_skills = sorted(skill_percentages.items(), key=lambda x: x[1], reverse=True)
        output_lines = [f"{skill}: {percentage}%" for skill, percentage in sorted_skills if percentage > 0]
        
        return " | ".join(output_lines[:5])  # Show top 5 skills
