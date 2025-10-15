"""Load and compile skill patterns from JSON"""

import json
import re
from typing import Any

from .config import SKILLS_JSON_PATH, EXCLUDED_CATEGORIES, EXCLUDED_SKILLS


def load_skill_patterns() -> dict[str, list[re.Pattern[str]]]:
    """Load and compile skill patterns from JSON for fast matching"""
    
    with open(SKILLS_JSON_PATH, 'r', encoding='utf-8') as f:
        data: dict[str, Any] = json.load(f)
    
    compiled_patterns: dict[str, list[re.Pattern[str]]] = {}
    
    # skills is now a flat list, not categorized dict
    skills_list: list[dict[str, Any]] = data.get("skills", [])
    
    for skill_obj in skills_list:
        skill_name: str = skill_obj["name"]
        
        # Skip specific non-technical skills
        if skill_name in EXCLUDED_SKILLS:
            continue
            
        patterns: list[str] = skill_obj.get("patterns", [skill_name.lower()])
        
        # Compile regex patterns (patterns already have \b boundaries)
        compiled_patterns[skill_name] = [
            re.compile(p, re.IGNORECASE)
            for p in patterns
        ]
    
    return compiled_patterns
