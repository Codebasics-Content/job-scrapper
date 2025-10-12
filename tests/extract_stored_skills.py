"""Extract all unique stored skills from database to add to reference."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.db.connection import DatabaseConnection
from src.analysis.skill_extraction import extract_skills_advanced
import json
from collections import Counter

def extract_missing_patterns() -> None:
    """Find stored skills not detected by current extractor."""
    
    with DatabaseConnection("jobs.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT job_description, skills 
            FROM jobs 
            WHERE job_description IS NOT NULL 
            AND skills IS NOT NULL
            LIMIT 100
        """)
        jobs = cursor.fetchall()
    
    missing_skills: Counter[str] = Counter()
    
    for job_desc, stored_skills_str in jobs:
        if not stored_skills_str:
            continue
            
        extracted = extract_skills_advanced(job_desc, "skills_reference_2025.json")
        stored = [s.strip() for s in stored_skills_str.split(',')]
        
        extracted_lower = {s.lower() for s in extracted}
        
        for skill in stored:
            if skill.lower() not in extracted_lower:
                missing_skills[skill] += 1
    
    print(f"\n{'='*70}")
    print(f"MISSING SKILLS TO ADD TO REFERENCE JSON")
    print(f"{'='*70}\n")
    
    if missing_skills:
        print(f"Found {len(missing_skills)} unique missing skills:\n")
        for skill, count in missing_skills.most_common():
            print(f"  • {skill:40} → {count:3} jobs")
    else:
        print("✅ All stored skills are already detected!")
    
    print(f"\n{'='*70}\n")
    
    return dict(missing_skills)

if __name__ == "__main__":
    extract_missing_patterns()
