#!/usr/bin/env python3
"""
Report Integration Tests - Verify end-to-end report generation

Tests the complete pipeline: database → skill analysis → formatted report
EMD Compliance: ≤80 lines
"""

import pytest
import os
from utils.analysis.report_integration import ReportIntegration

# Use existing test database
TEST_DB_PATH = "jobs.db"

@pytest.fixture
def report_integration():
    """Create ReportIntegration instance with test database"""
    if not os.path.exists(TEST_DB_PATH):
        pytest.skip(f"Test database not found: {TEST_DB_PATH}")
    return ReportIntegration(TEST_DB_PATH)

def test_report_integration_initialization(report_integration):
    """Test ReportIntegration initializes correctly"""
    assert report_integration is not None
    assert report_integration.db_path == TEST_DB_PATH
    assert report_integration.conn_manager is not None
    assert report_integration.job_retrieval is not None
    assert report_integration.skill_analyzer is not None
    assert report_integration.formatter is not None

def test_generate_all_jobs_report(report_integration):
    """Test generating report for all jobs"""
    report = report_integration.generate_skill_report()
    
    assert isinstance(report, str)
    assert len(report) > 0
    assert "SKILL ANALYSIS REPORT" in report or "No jobs" in report

def test_generate_role_specific_report(report_integration):
    """Test generating report for specific role"""
    report = report_integration.generate_skill_report(role="Data Scientist")
    
    assert isinstance(report, str)
    assert len(report) > 0

def test_console_summary(report_integration):
    """Test console summary generation"""
    summary = report_integration.get_console_summary()
    
    assert isinstance(summary, str)

def test_report_contains_percentages(report_integration):
    """Test that report includes percentage values"""
    report = report_integration.generate_skill_report()
    
    if "No jobs" not in report:
        assert "%" in report

def test_report_has_proper_structure(report_integration):
    """Test report has expected structure elements"""
    report = report_integration.generate_skill_report()
    
    if "SKILL ANALYSIS REPORT" in report:
        assert "Generated:" in report
        assert "Total Jobs Analyzed:" in report
        assert "=" in report
