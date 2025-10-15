"""Skill Refinement - Normalize extracted skills to canonical names
EMD: ≤80 lines, batch updates database skills using pattern matching
"""
import sqlite3
import json
import re

def load_pattern_to_name_map(ref_path: str = 'skills_reference_2025.json') -> dict[str, str]:
    """Build pattern→canonical_name lookup from reference"""
    with open(ref_path, 'r') as f:
        data = json.load(f)
    
    pattern_map = {}
    
    def extract_mappings(obj: object) -> None:
        if isinstance(obj, dict):
            if 'name' in obj and 'patterns' in obj:
                canonical_name = obj['name']
                for pattern in obj['patterns']:
                    # Remove regex markers for simple matching
                    clean = pattern.replace('\\b', '').replace('\\s+', ' ')
                    clean = re.sub(r'[\\()[\]{}?+*|^$.]', '', clean).lower().strip()
                    if clean:
                        pattern_map[clean] = canonical_name
            for value in obj.values():
                extract_mappings(value)
        elif isinstance(obj, list):
            for item in obj:
                extract_mappings(item)
    
    extract_mappings(data)
    return pattern_map

def normalize_skill(skill: str, pattern_map: dict[str, str]) -> str | None:
    """Map extracted skill to canonical name, filter invalid"""
    skill_lower = skill.lower().strip()
    
    # Filter truncated/invalid (>30 chars or ends with incomplete word)
    if len(skill) > 30 or skill.endswith(('wo', 'en', 'an', 'or', 'er', 'le', 'de')):
        return None
    
    # Direct match
    if skill_lower in pattern_map:
        return pattern_map[skill_lower]
    
    # Fuzzy match (for minor variations)
    for pattern, name in pattern_map.items():
        if skill_lower in pattern or pattern in skill_lower:
            return name
    
    return None  # No match = filter out

def refine_linkedin_skills(db_path: str = 'jobs.db') -> tuple[int, int]:
    """Refine all LinkedIn job skills, return (updated_count, filtered_count)"""
    pattern_map = load_pattern_to_name_map()
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT job_id, skills FROM jobs WHERE platform='linkedin'")
    
    updated = 0
    filtered = 0
    
    for job_id, skills_str in cursor.fetchall():
        if not skills_str:
            continue
        
        skills = [s.strip() for s in skills_str.split(',') if s.strip()]
        normalized = set()
        
        for skill in skills:
            canonical = normalize_skill(skill, pattern_map)
            if canonical:
                normalized.add(canonical)
            else:
                filtered += 1
        
        if normalized:
            new_skills = ','.join(sorted(normalized))
            cursor.execute("UPDATE jobs SET skills=? WHERE job_id=?", (new_skills, job_id))
            updated += 1
    
    conn.commit()
    conn.close()
    return updated, filtered

if __name__ == "__main__":
    print("🔧 Refining LinkedIn skills...")
    updated, filtered = refine_linkedin_skills()
    print(f"✅ Updated {updated} jobs, filtered {filtered} invalid skills")
