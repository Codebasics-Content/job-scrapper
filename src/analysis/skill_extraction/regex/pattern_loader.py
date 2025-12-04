"""Load and compile skill patterns from JSON"""

from __future__ import annotations

import json
import re
from typing import TypedDict

from .config import EXCLUDED_SKILLS, SKILLS_JSON_PATH


class SkillPatternData(TypedDict, total=False):
    """Type for skill pattern data from JSON"""
    name: str
    patterns: list[str]
    category: str


class SkillsJsonData(TypedDict, total=False):
    """Type for skills JSON file structure"""
    skills: list[SkillPatternData]


def load_skill_patterns() -> dict[str, list[re.Pattern[str]]]:
    """Load and compile skill patterns from JSON for fast matching"""

    with open(SKILLS_JSON_PATH, 'r', encoding='utf-8') as f:
        data: SkillsJsonData = json.load(f)

    compiled_patterns: dict[str, list[re.Pattern[str]]] = {}

    # skills is now a flat list, not categorized dict
    skills_list: list[SkillPatternData] = data.get("skills", [])

    for skill_obj in skills_list:
        skill_name: str = skill_obj.get("name", "")

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
