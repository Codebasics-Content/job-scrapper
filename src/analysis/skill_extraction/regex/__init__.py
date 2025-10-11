"""Regex-based skill extraction module"""

from .pattern_loader import load_skill_patterns
from .skill_matcher import match_skills_in_text

__all__ = ["load_skill_patterns", "match_skills_in_text"]
