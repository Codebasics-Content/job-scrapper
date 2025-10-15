"""
Layer 3: Direct pattern matching with improved regex
"""
import re
from typing import Any
from .improved_patterns import (
    IMPROVED_SINGLE_LETTER,
    IMPROVED_SHORT_WORDS,
    CLOUD_PLATFORMS,
    PROGRAMMING_LANGUAGES
)


def layer3_extract_direct(
    text: str,
    consumed: list[tuple[int, int]],
    skills_reference: dict[str, list[dict[str, Any]]]
) -> list[dict[str, Any]]:
    """
    Layer 3: Extract individual skills using improved patterns
    Skips regions already consumed by layer 1 & 2
    """
    skills = []
    
    # Combine all improved patterns
    all_patterns = {
        **IMPROVED_SINGLE_LETTER,
        **IMPROVED_SHORT_WORDS,
        **CLOUD_PLATFORMS,
        **PROGRAMMING_LANGUAGES
    }
    
    # Add patterns from skills reference (it's a list, not dict)
    for skill_data in skills_reference:
        skill_name = skill_data['name']
        for pattern_str in skill_data.get('patterns', []):
            if skill_name not in all_patterns:
                all_patterns[skill_name] = pattern_str
    
    # Extract using improved patterns
    for skill_name, pattern_str in all_patterns.items():
        try:
            pattern = re.compile(pattern_str, re.IGNORECASE)
            
            for match in pattern.finditer(text):
                start, end = match.span()
                
                # Skip if region already consumed
                if any(s <= start < e or s < end <= e for s, e in consumed):
                    continue
                
                skills.append({
                    'skill': skill_name,
                    'start': start,
                    'end': end,
                    'layer': 3
                })
        except re.error:
            # Skip invalid patterns
            continue
    
    return skills
