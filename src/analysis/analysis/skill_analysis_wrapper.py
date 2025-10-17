# Skill Analysis Wrapper - Main Interface for Job Market Analysis
# EMD Compliance: ≤80 lines, single responsibility principle
import logging
from src.models import JobModel
from src.analysis.analysis.skill_analyzer import SkillAnalysisEngine
from src.analysis.analysis.report_formatter import ReportFormatter
from src.db.connection import ConnectionManager
from src.db.operations import DataConverter

logger = logging.getLogger(__name__)

class SkillAnalysisWrapper:
    """Main interface for comprehensive job market skill analysis"""
    
    def __init__(self):
        self.engine = SkillAnalysisEngine()
        self.formatter = ReportFormatter()
        
    def analyze_jobs_by_role(self, jobs: list[JobModel], role: str) -> dict[str, object]:
        """Complete skill analysis for jobs filtered by role"""
        
        if not jobs:
            logger.warning(f"No jobs provided for role: {role}")
            return self._empty_analysis(role)
            
        try:
            # Filter jobs by role (case-insensitive partial match)
            filtered_jobs = [job for job in jobs 
                           if role.lower() in job.job_role.lower()]
            
            if not filtered_jobs:
                logger.warning(f"No jobs found matching role: {role}")
                return self._empty_analysis(role)
            
            # Analyze skills
            skill_percentages = self.engine.analyze_job_skills(filtered_jobs, role)
            
            # Format results
            report = self.formatter.format_skill_report(
                role, skill_percentages, len(filtered_jobs)
            )
            console_output = self.formatter.format_console_output(skill_percentages)
            
            logger.info(f"Successfully analyzed {len(filtered_jobs)} jobs for role '{role}'")
            
            return {
                'role': role,
                'total_jobs': len(filtered_jobs),
                'skill_percentages': skill_percentages,
                'report': report,
                'console_summary': console_output,
                'success': True
            }
            
        except Exception as error:
            logger.error(f"Analysis failed for role '{role}': {error}")
            return self._error_analysis(role, str(error))
            
    def _empty_analysis(self, role: str) -> dict[str, object]:
        """Return empty analysis structure"""
        return {
            'role': role,
            'total_jobs': 0,
            'skill_percentages': {},
            'report': f"No jobs found for role: {role}",
            'console_summary': "No data available",
            'success': False
        }
        
    def _error_analysis(self, role: str, error_msg: str) -> dict[str, object]:
        """Return error analysis structure"""
        return {
            'role': role,
            'total_jobs': 0,
            'skill_percentages': {},
            'report': f"Analysis error for {role}: {error_msg}",
            'console_summary': "Analysis failed",
            'success': False
        }
    
    def generate_skill_report(self, job_role: str, db_path: str = "data/jobs.db") -> str:
        """Generate skill report by reading jobs from database"""
        try:
            from src.models import JobModel
            conn_manager = ConnectionManager(db_path)
            converter = DataConverter()
            
            with conn_manager.get_connection() as conn:
                cursor = conn.execute(
                    "SELECT * FROM jobs WHERE Job_Role LIKE ?",
                    (f"%{job_role}%",)
                )
                rows = cursor.fetchall()
                jobs_data = [converter.convert_row_to_job_data(dict(row)) for row in rows]
                jobs = [JobModel(**data) for data in jobs_data]
            
            if not jobs:
                return f"No jobs found for role: {job_role}"
            
            result = self.analyze_jobs_by_role(jobs, job_role)
            report = result.get('report', 'Analysis completed')
            return str(report)
            
        except Exception as error:
            logger.error(f"Report generation failed: {error}")
            return f"Error generating report: {str(error)}"
