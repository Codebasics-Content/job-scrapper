"""Lightweight skill extraction module - EMD compliant"""
from .regex_extractor import extract_skills_from_text, load_skill_patterns

__all__ = ["extract_skills_from_text", "load_skill_patterns"]
