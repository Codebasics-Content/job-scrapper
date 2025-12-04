"""Database skill deduplication utility
EMD Compliance: <=80 lines
"""
from __future__ import annotations

import sqlite3

from .extractor import AdvancedSkillExtractor


def _extract_skills_as_list(extractor: AdvancedSkillExtractor, text: str) -> list[str]:
    """Extract skills and ensure list[str] return type"""
    result = extractor.extract(text, return_confidence=False)
    # Type narrow: when return_confidence=False, returns list[str]
    skills: list[str] = []
    for item in result:
        if isinstance(item, str):
            skills.append(item)
    return skills


def deduplicate_database_skills(db_path: str, skills_reference: str) -> dict[str, dict[str, list[str]]]:
    """Re-extract and deduplicate all skills in database"""
    extractor = AdvancedSkillExtractor(skills_reference)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all jobs with descriptions
    cursor.execute("SELECT job_id, job_description, skills FROM jobs WHERE job_description IS NOT NULL")
    rows: list[tuple[str, str, str]] = cursor.fetchall()

    updates: dict[str, dict[str, list[str]]] = {}
    for job_id, description, old_skills in rows:
        # Re-extract with updated deduplication
        new_skills_list: list[str] = _extract_skills_as_list(extractor, description)
        new_skills_str: str = ','.join(new_skills_list) if new_skills_list else ''

        if new_skills_str != old_skills:
            old_skills_list: list[str] = old_skills.split(',') if old_skills else []
            updates[job_id] = {
                'old': old_skills_list,
                'new': new_skills_list,
                'removed': list(set(old_skills_list) - set(new_skills_list)) if old_skills else []
            }

            # Update database
            cursor.execute("UPDATE jobs SET skills = ? WHERE job_id = ?", (new_skills_str, job_id))

    conn.commit()
    conn.close()

    return updates


def show_deduplication_report(updates: dict[str, dict[str, list[str]]]) -> None:
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
