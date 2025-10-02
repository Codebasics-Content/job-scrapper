#!/usr/bin/env python3
# Fast keyword-based skill extraction (100x faster than SkillNER)
# EMD Compliance: ≤80 lines

import re
import json
import logging
from pathlib import Path
from src.scraper.base.skill_validator import validate_extracted_skills

logger = logging.getLogger(__name__)

# Load skill database once at module import
project_root = Path(__file__).parent.parent.parent.parent
skill_db_path = project_root / "skill_db_relax_20.json"

with open(skill_db_path) as f:
    SKILL_DB = json.load(f)

# Build fast lookup with compiled regex patterns for accurate word boundaries
SKILL_PATTERNS: dict[re.Pattern[str], tuple[str, str]] = {}  # pattern -> (skill_id, skill_name)

for skill_id, skill_info in SKILL_DB.items():
    if skill_info.get("skill_type") == "Hard Skill":
        skill_name = skill_info.get("skill_name", "").lower()
        if skill_name and len(skill_name) > 2:
            # Compile regex pattern with word boundaries once
            pattern = re.compile(r'\b' + re.escape(skill_name) + r'\b', re.IGNORECASE)
            SKILL_PATTERNS[pattern] = (skill_id, skill_name)
        
        # Add low surface forms (only if >3 chars to avoid false positives)
        for form in skill_info.get("low_surface_forms", []):
            if form and len(form) > 3:  # Stricter length check
                pattern = re.compile(r'\b' + re.escape(form.lower()) + r'\b', re.IGNORECASE)
                SKILL_PATTERNS[pattern] = (skill_id, skill_name)

logger.info(f"Loaded {len(SKILL_PATTERNS)} skill patterns for fast matching")

def extract_dynamic_skills(description_text: str) -> list[str]:
    """Accurate skill extraction with compiled regex patterns"""
    
    if not description_text or not description_text.strip():
        return []
    
    try:
        # Find matching skills using pre-compiled regex patterns
        found_skills: dict[str, str] = {}  # skill_id -> skill_name
        
        for pattern, (skill_id, skill_name) in SKILL_PATTERNS.items():
            # Use pre-compiled regex for accurate word boundary matching
            if pattern.search(description_text):
                # Deduplicate by skill_id (same skill may have multiple forms)
                if skill_id not in found_skills:
                    found_skills[skill_id] = skill_name
        
        # Get unique skills sorted alphabetically (no limit)
        unique_skills = sorted(set(found_skills.values()))
        validated = validate_extracted_skills(unique_skills, description_text)
        
        logger.info(f"Accurate extraction: {len(validated)} technical skills found")
        return validated
        
    except Exception as e:
        logger.error(f"Error extracting skills: {e}")
        return []
