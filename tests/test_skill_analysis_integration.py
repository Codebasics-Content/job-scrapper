# Test Skill Analysis Integration
import pytest
from utils.analysis.skill_analysis_integration import SkillAnalysisIntegration

def test_skill_analysis_integration_initialization() -> None:
    """Test that SkillAnalysisIntegration initializes correctly."""
    
    integration = SkillAnalysisIntegration(db_path="jobs.db")
    
    assert integration.db_path == "jobs.db"
    assert integration.job_retrieval is not None
    assert integration.analyzer is not None
    
def test_get_total_jobs_count() -> None:
    """Test retrieving total jobs count from src.db."""
    
    integration = SkillAnalysisIntegration(db_path="jobs.db")
    count = integration.get_total_jobs_count()
    
    assert isinstance(count, int)
    assert count >= 0
    
def test_analyze_all_jobs() -> None:
    """Test analyzing skills from all jobs."""
    
    integration = SkillAnalysisIntegration(db_path="jobs.db")
    skill_percentages = integration.analyze_all_jobs()
    
    assert isinstance(skill_percentages, dict)
    
    # If jobs exist, verify percentages are valid
    if skill_percentages:
        for skill, percentage in skill_percentages.items():
            assert isinstance(skill, str)
            assert isinstance(percentage, float)
            assert 0 <= percentage <= 100
            
def test_analyze_by_role() -> None:
    """Test analyzing skills for specific role."""
    
    integration = SkillAnalysisIntegration(db_path="jobs.db")
    
    # Test with a common role
    skill_percentages = integration.analyze_by_role("Data Scientist")
    
    assert isinstance(skill_percentages, dict)
    
    # If jobs exist for this role, verify percentages
    if skill_percentages:
        for skill, percentage in skill_percentages.items():
            assert isinstance(skill, str)
            assert isinstance(percentage, float)
            assert 0 <= percentage <= 100

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
