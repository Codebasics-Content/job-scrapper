"""Main skill extraction interface

Provides simple extract_skills() function for skill extraction.
"""
from __future__ import annotations

from typing import List

from .pattern_loader import load_skill_patterns
from .skill_matcher import match_skills_in_text


def extract_skills(text: str) -> List[str]:
    """Extract skills from text using regex patterns
    
    Args:
        text: Job description or any text containing skills
        
    Returns:
        List of extracted skill names (lowercase normalized)
    """
    patterns = load_skill_patterns()
    skills = match_skills_in_text(text, patterns)
    
    # Normalize to lowercase and deduplicate
    normalized = list(set(s.lower() for s in skills))
    return sorted(normalized)
