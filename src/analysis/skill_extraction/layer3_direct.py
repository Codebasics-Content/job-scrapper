"""
Layer 3: Direct pattern matching with improved regex
"""
import re
from typing import Any
from .improved_patterns import (
    IMPROVED_SINGLE_LETTER,
    CLOUD_PLATFORMS,
    PROGRAMMING_LANGUAGES
)


def layer3_extract_direct(
    text: str,
    consumed: list[tuple[int, int]],
    skills_reference: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """
    Layer 3: Extract using ONLY patterns from skills_reference_2025.json
    Returns canonical skill names, not pattern text
    """
    skills = []
    
    # Build pattern -> canonical_name mapping from skills_reference
    pattern_to_skill: dict[str, str] = {}
    
    # Add improved patterns (for backward compatibility)
    for skill_name, pattern_str in IMPROVED_SINGLE_LETTER.items():
        pattern_to_skill[pattern_str] = skill_name
    for skill_name, pattern_str in CLOUD_PLATFORMS.items():
        pattern_to_skill[pattern_str] = skill_name
    for skill_name, pattern_str in PROGRAMMING_LANGUAGES.items():
        pattern_to_skill[pattern_str] = skill_name
    
    # Add patterns from skills_reference - map pattern -> canonical name
    for skill_data in skills_reference:
        canonical_name = skill_data['name']
        for pattern_str in skill_data.get('patterns', []):
            pattern_to_skill[pattern_str] = canonical_name
    
    # Extract using patterns and return canonical names
    for pattern_str, canonical_name in pattern_to_skill.items():
        try:
            pattern = re.compile(pattern_str, re.IGNORECASE)
            
            for match in pattern.finditer(text):
                start, end = match.span()
                
                # Skip if region already consumed
                if any(s <= start < e or s < end <= e for s, e in consumed):
                    continue
                
                skills.append({
                    'skill': canonical_name,  # Use canonical name from JSON
                    'start': start,
                    'end': end,
                    'layer': 3
                })
        except re.error:
            # Skip invalid patterns
            continue
    
    return skills
