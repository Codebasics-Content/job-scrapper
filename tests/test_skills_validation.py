"""Skills validation test against skills_reference_2025.json

Validates regex skill extractor with real job description samples.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analysis.skill_extraction.regex import extract_skills


def test_skill_extraction_basic():
    """Test basic skill extraction with known skills"""
    # Test with Python-focused job description
    job_desc = """
    Required: Python, FastAPI, PostgreSQL, Docker, AWS
    Experience with React, TypeScript, and CI/CD pipelines
    """
    
    extracted = extract_skills(job_desc)
    
    # Validate we got some skills back
    assert len(extracted) > 0, "No skills extracted"
    
    # Check expected skills present (case-insensitive)
    expected_skills = ["python", "fastapi", "postgresql", "docker"]
    extracted_lower = [s.lower() for s in extracted]
    
    for expected in expected_skills:
        assert expected in extracted_lower, \
            f"Expected skill '{expected}' not extracted. Got: {extracted}"


def test_false_positive_detection():
    """Test for false positives - common words that aren't skills"""
    job_desc = """
    We are looking for education in Computer Science.
    Experience with learning new technologies is important.
    """
    
    extracted = extract_skills(job_desc)
    
    # These should NOT be extracted as skills
    false_positives = ["education", "learning", "experience"]
    for fp in false_positives:
        assert fp.lower() not in [s.lower() for s in extracted], \
            f"False positive detected: '{fp}'"


def test_case_insensitivity():
    """Test skill extraction handles different cases"""
    job_desc = "Python JAVA javascript Node.js REACT"
    
    extracted = extract_skills(job_desc)
    
    # Should extract regardless of case
    assert len(extracted) >= 4, "Should extract at least 4 skills"
    
    # All extracted should be lowercase normalized
    for skill in extracted:
        assert skill.islower() or "-" in skill or "." in skill


if __name__ == "__main__":
    print("Running skills validation tests...")
    
    test_skill_extraction_basic()
    print("✅ Basic extraction test passed")
    
    test_false_positive_detection()
    print("✅ False positive test passed")
    
    test_case_insensitivity()
    print("✅ Case insensitivity test passed")
    
    print("\n✅ All skills validation tests passed!")
