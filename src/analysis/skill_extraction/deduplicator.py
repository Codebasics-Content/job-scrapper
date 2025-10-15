"""Database skill deduplication utility
EMD Compliance: ≤80 lines
"""
import sqlite3
from .extractor import AdvancedSkillExtractor


def deduplicate_database_skills(db_path: str, skills_reference: str) -> dict[str, list[str]]:
    """Re-extract and deduplicate all skills in database"""
    extractor = AdvancedSkillExtractor(skills_reference)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all jobs with descriptions
    cursor.execute("SELECT job_id, job_description, skills FROM jobs WHERE job_description IS NOT NULL")
    rows = cursor.fetchall()
    
    updates = {}
    for job_id, description, old_skills in rows:
        # Re-extract with updated deduplication
        new_skills = extractor.extract(description)
        new_skills_str = ','.join(new_skills) if new_skills else ''
        
        if new_skills_str != old_skills:
            updates[job_id] = {
                'old': old_skills.split(',') if old_skills else [],
                'new': new_skills,
                'removed': list(set(old_skills.split(',')) - set(new_skills)) if old_skills else []
            }
            
            # Update database
            cursor.execute("UPDATE jobs SET skills = ? WHERE job_id = ?", (new_skills_str, job_id))
    
    conn.commit()
    conn.close()
    
    return updates


def show_deduplication_report(updates: dict[str, list[str]]) -> None:
    """Display deduplication changes"""
    print("\n" + "="*70)
    print("SKILL DEDUPLICATION REPORT")
    print("="*70)
    
    if not updates:
        print("\n✅ No duplicates found - all skills already clean!")
        return
    
    print(f"\n📊 Updated {len(updates)} jobs\n")
    
    for job_id, changes in updates.items():
        print(f"\n{job_id}:")
        print(f"  ❌ Removed: {changes['removed']}")
        print(f"  ✅ Final: {len(changes['new'])} skills")
