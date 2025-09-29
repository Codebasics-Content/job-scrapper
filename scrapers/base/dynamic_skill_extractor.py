#!/usr/bin/env python3
# Dynamic skill extraction for emerging technologies and GenAI
# EMD Compliance: ≤80 lines

import re
import logging

logger = logging.getLogger(__name__)

def extract_dynamic_skills(description_text: str) -> list[str]:
    """Extract dynamic skills using NLP-based patterns"""
    
    dynamic_skills = set()
    text_lower = description_text.lower()
    
    # Extract capitalized technology names (likely brand names)
    capitalized_tech = re.findall(r'\b[A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*)*\b', description_text)
    tech_keywords = ['AI', 'ML', 'API', 'SDK', 'GPT', 'LLM', 'NLP', 'CV']
    
    for tech in capitalized_tech:
        if any(keyword in tech.upper() for keyword in tech_keywords):
            dynamic_skills.add(tech.lower())
    
    # Extract version-specific technologies
    version_patterns = [
        r'\b([a-zA-Z]+)\s*(?:v?[0-9]+(?:\.[0-9]+)*)\b',  # TensorFlow 2.0
        r'\b([a-zA-Z]+)\s*(?:version\s+[0-9]+(?:\.[0-9]+)*)\b'  # Python version 3.9
    ]
    
    for pattern in version_patterns:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        for match in matches:
            if len(match) > 2:  # Filter out short matches
                dynamic_skills.add(match.strip())
    
    # Extract framework patterns (.js, .py, etc.)
    framework_pattern = r'\b([a-zA-Z]+)(?:\.(?:js|py|rb|php|go|rs|java))\b'
    framework_matches = re.findall(framework_pattern, text_lower)
    dynamic_skills.update(framework_matches)
    
    # Extract skill context patterns
    skill_contexts = [
        r'experience (?:with|in)\s+([^,.]+)',
        r'knowledge of\s+([^,.]+)',
        r'proficient (?:with|in)\s+([^,.]+)',
        r'familiar with\s+([^,.]+)',
        r'expertise in\s+([^,.]+)'
    ]
    
    for pattern in skill_contexts:
        matches = re.findall(pattern, text_lower)
        for match in matches:
            # Clean and validate extracted skills
            skills = [s.strip() for s in match.split(' and ') if len(s.strip()) > 2]
            dynamic_skills.update(skills)
    
    return list(dynamic_skills)

def clean_and_validate_skills(skills: list[str]) -> list[str]:
    """Clean and validate extracted skills"""
    
    cleaned_skills = set()
    common_words = {'and', 'or', 'the', 'in', 'on', 'at', 'to', 'for', 'with', 'by', 'from'}
    
    for skill in skills:
        # Remove common words and clean
        skill_clean = skill.strip().lower()
        if (len(skill_clean) > 2 and 
            skill_clean not in common_words and 
            not skill_clean.isdigit()):
            cleaned_skills.add(skill_clean)
    
    return list(cleaned_skills)
