#!/usr/bin/env python3
"""Enhanced Skill Extraction Module - EMD Compliant
Extracts skills from both job description and company details
"""
import logging
import re

logger = logging.getLogger(__name__)

def extract_skills_from_combined_text(
    jd: str, 
    company_detail: str, 
    existing_skills: str = ""
) -> list[str]:
    """Extract skills from job description, company details, and existing skills
    
    Args:
        jd: Job description text
        company_detail: Company detail text
        existing_skills: Comma-separated existing skills
        
    Returns:
        Combined list of unique normalized skills
    """
    if not any([jd, company_detail, existing_skills]):
        return []
    
    # Combine all text sources
    combined_text = f"{jd} {company_detail}".strip()
    
    # Extract skills from existing comma-separated list
    existing_skill_list = _parse_existing_skills(existing_skills)
    
    # Extract skills from combined text using pattern matching
    text_extracted_skills = _extract_skills_from_text(combined_text)
    
    # Combine and deduplicate
    all_skills = existing_skill_list + text_extracted_skills
    unique_skills = list(set(skill.lower().strip() for skill in all_skills if skill.strip()))
    
    logger.info(f"Extracted {len(unique_skills)} skills from combined sources")
    return unique_skills

def _parse_existing_skills(skills_str: str) -> list[str]:
    """Parse comma-separated skills string"""
    if not skills_str:
        return []
    
    return [
        skill.strip() 
        for skill in skills_str.split(',') 
        if skill.strip()
    ]

def _extract_skills_from_text(text: str) -> list[str]:
    """Extract potential skills from free text using pattern matching"""
    if not text:
        return []
    
    # Common skill patterns (programming languages, frameworks, tools)
    skill_patterns = [
        r'\b(?:Python|Java|JavaScript|TypeScript|C\+\+|C#|Go|Rust|PHP|Ruby)\b',
        r'\b(?:React|Angular|Vue|Django|Flask|Spring|Express|Node\.js)\b',
        r'\b(?:SQL|MySQL|PostgreSQL|MongoDB|Redis|Docker|Kubernetes)\b',
        r'\b(?:AWS|Azure|GCP|Git|Jenkins|CI/CD|DevOps)\b',
        r'\b(?:Machine Learning|AI|Data Science|Analytics|Statistics)\b'
    ]
    
    extracted_skills = []
    text_lower = text.lower()
    
    for pattern in skill_patterns:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        extracted_skills.extend(matches)
    
    return extracted_skills
