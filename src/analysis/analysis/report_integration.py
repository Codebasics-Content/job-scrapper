#!/usr/bin/env python3
"""
Report Generation Integration - EMD Compliant Module

Connects database retrieval, skill analysis, and report formatting
into a complete end-to-end report generation pipeline.

EMD Compliance: ≤80 lines, single responsibility principle.
"""

import logging
from src.db.connection import ConnectionManager
from src.db.operations import JobRetrieval
from .skill_analysis_integration import SkillAnalysisIntegration
from .report_formatter import ReportFormatter

logger = logging.getLogger(__name__)

class ReportIntegration:
    """Complete report generation pipeline from database to formatted output"""
    
    def __init__(self, db_path: str):
        self.db_path: str = db_path
        self.conn_manager: ConnectionManager = ConnectionManager(db_path)
        self.job_retrieval: JobRetrieval = JobRetrieval()
        self.skill_analyzer: SkillAnalysisIntegration = SkillAnalysisIntegration(db_path)
        self.formatter: ReportFormatter = ReportFormatter()
    
    def generate_skill_report(self, role: str | None = None) -> str:
        """Generate complete skill analysis report for all jobs or specific role"""
        
        try:
            with self.conn_manager.get_connection() as conn:
                # Retrieve jobs
                if role:
                    jobs = self.job_retrieval.retrieve_jobs_by_role(conn, role)
                    report_role = role
                else:
                    jobs = self.job_retrieval.retrieve_all_jobs(conn)
                    report_role = "All Roles"
                
                if not jobs:
                    logger.warning(f"No jobs found for report generation: {report_role}")
                    return f"No jobs available for analysis: {report_role}"
                
                # Analyze skills
                if role:
                    skill_percentages = self.skill_analyzer.analyze_by_role(role)
                else:
                    skill_percentages = self.skill_analyzer.analyze_all_jobs()
                
                if not skill_percentages:
                    logger.warning(f"No skills extracted from {len(jobs)} jobs")
                    return f"No skills found in {len(jobs)} jobs"
                
                # Format report
                report = self.formatter.format_skill_report(
                    report_role,
                    skill_percentages,
                    len(jobs)
                )
                
                logger.info(f"Generated report for {len(jobs)} jobs, {len(skill_percentages)} skills")
                return report
                
        except Exception as error:
            logger.error(f"Report generation failed: {error}")
            return f"Report generation error: {str(error)}"
    
    def get_console_summary(self, role: str | None = None) -> str:
        """Get brief console summary of top skills"""
        
        if role:
            skill_percentages = self.skill_analyzer.analyze_by_role(role)
        else:
            skill_percentages = self.skill_analyzer.analyze_all_jobs()
        
        return self.formatter.format_console_output(skill_percentages)
