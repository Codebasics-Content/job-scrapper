#!/usr/bin/env python3
"""
Test suite for lightweight skill extraction module

Author: Job Scrapper Team
Created: 2025-10-11
"""

import pytest
from src.analysis.skill_extraction import extract_skills_from_text, load_skill_patterns

def test_load_skill_patterns():
    """Test pattern loading from JSON"""
    patterns = load_skill_patterns()
    
    assert isinstance(patterns, dict)
    assert len(patterns) > 0
    assert "Python" in patterns
    assert "JavaScript" in patterns

def test_extract_skills_basic():
    """Test basic skill extraction"""
    text = "Looking for Python and JavaScript developer with SQL experience"
    skills = extract_skills_from_text(text)
    
    assert "Python" in skills
    assert "JavaScript" in skills
    assert "SQL" in skills

def test_extract_skills_case_insensitive():
    """Test case-insensitive matching"""
    text = "need PYTHON, javascript, and Sql developer"
    skills = extract_skills_from_text(text)
    
    assert "Python" in skills
    assert "JavaScript" in skills
    assert "SQL" in skills

def test_extract_skills_empty():
    """Test empty text handling"""
    skills = extract_skills_from_text("")
    assert skills == []

def test_extract_skills_patterns():
    """Test pattern variants"""
    text = "We need golang, cpp, and python3 expertise"
    skills = extract_skills_from_text(text)
    
    assert "Go" in skills  # golang -> Go
    assert "C++" in skills  # cpp -> C++
    assert "Python" in skills  # python3 -> Python

def test_extract_skills_performance():
    """Test performance with pre-compiled patterns"""
    patterns = load_skill_patterns()
    text = "Python JavaScript Java C++ Go Rust TypeScript" * 100
    
    skills = extract_skills_from_text(text, patterns)
    assert len(skills) > 0
