"""
Skill normalization and synonym handling
"""
from typing import Any


# REMOVED: All hardcoded SKILL_SYNONYMS to prevent hallucinations
# ALL normalization must come from skills_reference_2025.json patterns
# This ensures single source of truth and eliminates duplicate/conflicting mappings


def normalize_skill(skill: str) -> str:
    """
    Normalize skill name - preserve exact canonical name from extraction
    All mapping handled by skills_reference_2025.json, no transformation needed
    """
    # Return exact skill name as extracted (already canonical from layer3_direct)
    return skill.strip()


def deduplicate_skills(skills: list[dict[str, Any]]) -> list[str]:
    """
    Extract skill names, normalize, and deduplicate
    Handles overlapping patterns (e.g., CI/CD contains CI and CD)
    """
    skill_names = [s['skill'] for s in skills]
    normalized = [normalize_skill(name) for name in skill_names]
    
    # Deduplicate while preserving order
    seen = set()
    unique_skills = []
    for skill in normalized:
        if skill.lower() not in seen:
            seen.add(skill.lower())
            unique_skills.append(skill)
    
    # Remove overlapping duplicates:
    # "Continuous Integration/Continuous Deployment" supersedes individual CI/CD components
    cicd_long = 'Continuous Integration/Continuous Deployment'
    if cicd_long in unique_skills:
        unique_skills = [s for s in unique_skills if s.upper() not in ['CI', 'CD', 'CI/CD']]
    
    return unique_skills
