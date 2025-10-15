"""Re-extract skills from existing job descriptions using AdvancedSkillExtractor
EMD: ≤80 lines, updates database with improved extraction
"""
import sqlite3
from src.analysis.skill_extraction.extractor import AdvancedSkillExtractor

def re_extract_linkedin_skills(db_path: str = 'jobs.db') -> int:
    """Re-extract all LinkedIn job skills from descriptions"""
    extractor = AdvancedSkillExtractor('skills_reference_2025.json')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT job_id, job_description 
        FROM jobs 
        WHERE platform='linkedin' AND job_description IS NOT NULL
    """)
    
    updated = 0
    
    for job_id, description in cursor.fetchall():
        try:
            # Extract skills using 3-layer advanced extractor
            skills = extractor.extract(description, return_confidence=False)
            
            if skills:
                skills_str = ','.join(skills)
                cursor.execute(
                    "UPDATE jobs SET skills=? WHERE job_id=?",
                    (skills_str, job_id)
                )
                updated += 1
        except Exception as e:
            print(f"⚠️  Error extracting job {job_id}: {e}")
            continue
    
    conn.commit()
    conn.close()
    return updated

if __name__ == "__main__":
    print("🔄 Re-extracting LinkedIn skills with improved patterns...")
    updated = re_extract_linkedin_skills()
    print(f"✅ Re-extracted skills for {updated} jobs")
