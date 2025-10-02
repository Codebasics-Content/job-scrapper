#!/usr/bin/env python3
# Skill validation module - verifies extracted skills exist in JD text
# EMD Compliance: ≤80 lines

import logging
import re

logger = logging.getLogger(__name__)

def validate_skill_in_text(skill: str, text: str) -> bool:
    """Verify skill actually appears in job description text
    
    Args:
        skill: Extracted skill name
        text: Original job description text
        
    Returns:
        True if skill appears in text, False otherwise
    """
    if not skill or not text:
        return False
    
    # Normalize both for case-insensitive matching
    normalized_text = text.lower()
    normalized_skill = skill.lower().strip()
    
    # Check exact phrase match
    if normalized_skill in normalized_text:
        return True
    
    # Check word boundary match (handles "python" vs "python3")
    pattern = r'\b' + re.escape(normalized_skill) + r'\b'
    if re.search(pattern, normalized_text):
        return True
    
    return False

def filter_boilerplate_skills(skills: list[str]) -> list[str]:
    """Remove generic boilerplate skills that don't add value
    
    Args:
        skills: List of extracted skills
        
    Returns:
        Filtered list without boilerplate terms
    """
    # Generic terms that appear in most JDs but aren't real skills
    boilerplate_terms = {
        'work', 'team', 'company', 'role', 'job', 'position',
        'experience', 'skills', 'knowledge', 'ability', 'opportunity',
        'benefits', 'equal', 'employer', 'apply', 'candidate'
    }
    
    filtered_skills = [
        skill for skill in skills
        if skill.lower() not in boilerplate_terms
        and len(skill) > 2  # Skip single/double character matches
    ]
    
    logger.info(f"Filtered {len(skills) - len(filtered_skills)} boilerplate skills")
    return filtered_skills

def validate_extracted_skills(
    skills: list[str],
    job_description: str
) -> list[str]:
    """Validate and filter extracted skills against original text
    
    Args:
        skills: List of extracted skills from SkillNER
        job_description: Original job description text
        
    Returns:
        Validated list of skills that actually appear in JD
    """
    if not skills or not job_description:
        return []
    
    # First, filter boilerplate
    filtered_skills = filter_boilerplate_skills(skills)
    
    # Validate each skill exists in text
    validated_skills = [
        skill for skill in filtered_skills
        if validate_skill_in_text(skill, job_description)
    ]
    
    rejected_count = len(skills) - len(validated_skills)
    logger.info(
        f"Validated {len(validated_skills)}/{len(skills)} skills "
        f"(rejected {rejected_count} hallucinated/boilerplate)"
    )
    
    return validated_skills
