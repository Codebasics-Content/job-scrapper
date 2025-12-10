"""Match skills in text using compiled patterns"""

import re


def match_skills_in_text(
    text: str,
    skill_patterns: dict[str, list[re.Pattern[str]]]
) -> list[str]:
    """
    Match skills in text using compiled regex patterns
    
    Args:
        text: Job description text
        skill_patterns: Pre-compiled regex patterns
    
    Returns:
        Sorted list of unique skill names found
    """
    
    if not text:
        return []
    
    found_skills: set[str] = set()
    text_lower = text.lower()
    
    # Fast matching: check each skill's patterns
    for skill_name, patterns in skill_patterns.items():
        for pattern in patterns:
            if pattern.search(text_lower):
                found_skills.add(skill_name)
                break  # Found match, move to next skill
    
    return sorted(list(found_skills))
