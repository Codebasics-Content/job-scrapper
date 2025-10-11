#!/usr/bin/env python3
"""
Lightweight Regex-Based Skill Extractor - FASTEST METHOD
NO heavy packages (SkillNER, spaCy) - Pure regex + JSON
Uses skills_reference_2025.json with compiled patterns for speed

Author: Job Scrapper Team
Created: 2025-10-11
EMD Compliance: ≤80 lines
"""

import json
import re
from pathlib import Path
from typing import Any

SKILLS_JSON_PATH = Path(__file__).parent.parent.parent.parent / "skills_reference_2025.json"

def load_skill_patterns() -> dict[str, list[re.Pattern[str]]]:
    """Load and compile skill patterns from JSON for fast matching"""
    
    with open(SKILLS_JSON_PATH, 'r', encoding='utf-8') as f:
        data: dict[str, Any] = json.load(f)
    
    compiled_patterns: dict[str, list[re.Pattern[str]]] = {}
    
    # Filter out non-technical categories (industry domains, soft skills)
    excluded_categories = {
        "industry_domains", "soft_skills", "business_domains", 
        "sectors", "domains", "industries"
    }
    
    for category, skills_list in data.get("skills", {}).items():
        # Skip non-technical skill categories
        if category in excluded_categories:
            continue
            
        for skill_obj in skills_list:
            skill_name: str = skill_obj["name"]
            
            # Skip specific non-technical skills
            if skill_name in {"Education", "Healthcare", "Financial Services", 
                             "E-commerce", "Manufacturing", "Telecommunications"}:
                continue
                
            patterns: list[str] = skill_obj.get("patterns", [skill_name.lower()])
            
            # Compile regex patterns with word boundaries for accuracy
            compiled_patterns[skill_name] = [
                re.compile(rf'\b{re.escape(p)}\b', re.IGNORECASE)
                for p in patterns
            ]
    
    return compiled_patterns

def extract_skills_from_text(
    text: str,
    skill_patterns: dict[str, list[re.Pattern[str]]] | None = None
) -> list[str]:
    """
    Extract skills from text using compiled regex patterns
    
    Args:
        text: Job description text
        skill_patterns: Pre-compiled patterns (loaded once for speed)
    
    Returns:
        List of unique skill names found
    """
    
    if not text:
        return []
    
    # Load patterns if not provided (cache externally for best performance)
    if skill_patterns is None:
        skill_patterns = load_skill_patterns()
    
    found_skills: set[str] = set()
    text_lower = text.lower()
    
    # Fast matching: check each skill's patterns
    for skill_name, patterns in skill_patterns.items():
        for pattern in patterns:
            if pattern.search(text_lower):
                found_skills.add(skill_name)
                break  # Found match, move to next skill
    
    return sorted(list(found_skills))
