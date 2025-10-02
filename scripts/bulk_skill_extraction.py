#!/usr/bin/env python3
# Bulk skill extraction - Fast keyword-based approach
# EMD Compliance: ≤80 lines

import re
import json
import logging
import sqlite3
from pathlib import Path

project_root = Path(__file__).parent.parent

# Load skill database (29,091 hard skills)
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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info(f"Loaded {len(SKILL_PATTERNS)} skill patterns for fast matching")

def extract_skills_from_jd(description_text: str) -> str:
    """Accurate skill extraction with compiled regex patterns"""
    if not description_text or not description_text.strip():
        return ""
    
    # Find matching skills using pre-compiled regex patterns
    found_skills: dict[str, str] = {}  # skill_id -> skill_name
    
    for pattern, (skill_id, skill_name) in SKILL_PATTERNS.items():
        # Use pre-compiled regex for accurate word boundary matching
        if pattern.search(description_text):
            # Deduplicate by skill_id (same skill may have multiple forms)
            if skill_id not in found_skills:
                found_skills[skill_id] = skill_name
    
    # Return top 20 skills sorted alphabetically
    unique_skills = sorted(set(found_skills.values()))[:20]
    return ", ".join(unique_skills)

def extract_skills_from_database(db_path: str = "jobs.db") -> None:
    """Extract skills from all jobs with pending extraction"""
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all jobs with pending skills
    cursor.execute("""
        SELECT job_id, jd 
        FROM jobs 
        WHERE skills = 'Pending extraction' OR skills IS NULL OR skills = ''
    """)
    jobs_to_process = cursor.fetchall()
    
    logger.info(f"Found {len(jobs_to_process)} jobs requiring skill extraction")
    
    processed = 0
    for job_id, jd in jobs_to_process:
        if not jd or jd.strip() == "":
            logger.warning(f"Skipping {job_id}: Empty job description")
            continue
        
        try:
            # Extract skills from job description
            skills_str = extract_skills_from_jd(jd)
            
            # Update database
            cursor.execute("""
                UPDATE jobs 
                SET skills = ? 
                WHERE job_id = ?
            """, (skills_str, job_id))
            
            processed += 1
            if processed % 10 == 0:
                logger.info(f"Processed {processed}/{len(jobs_to_process)} jobs")
                
        except Exception as error:
            logger.error(f"Failed to extract skills for {job_id}: {error}")
    
    conn.commit()
    conn.close()
    logger.info(f"✅ Skill extraction complete: {processed} jobs updated")

if __name__ == "__main__":
    extract_skills_from_database()
