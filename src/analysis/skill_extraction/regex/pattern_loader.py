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
    
    for category, skills_list in data.get("skills", {}).items():
        # Skip non-technical skill categories
        if category in EXCLUDED_CATEGORIES:
            continue
            
        for skill_obj in skills_list:
            skill_name: str = skill_obj["name"]
            
            # Skip specific non-technical skills
            if skill_name in EXCLUDED_SKILLS:
                continue
                
            patterns: list[str] = skill_obj.get("patterns", [skill_name.lower()])
            
            # Compile regex patterns with word boundaries for accuracy
            compiled_patterns[skill_name] = [
                re.compile(rf'\b{re.escape(p)}\b', re.IGNORECASE)
                for p in patterns
            ]
    
    return compiled_patterns
