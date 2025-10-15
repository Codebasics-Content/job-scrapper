"""LinkedIn Skill Analysis - False Positives & False Negatives Detector
EMD Compliance: ≤80 lines, analyzes extracted skills vs job descriptions
"""
import sqlite3
import json
from collections import Counter

def load_reference_skills(path: str = 'skills_reference_2025.json') -> set[str]:
    """Load skill names from nested structure with 'name' field"""
    with open(path, 'r') as f:
        data = json.load(f)
    skills = set()
    
    def extract_skills(obj: object) -> None:
        if isinstance(obj, dict):
            # Extract 'name' field if present
            if 'name' in obj and isinstance(obj['name'], str):
                skills.add(obj['name'].lower())
            # Recursively process all values
            for value in obj.values():
                extract_skills(value)
        elif isinstance(obj, list):
            for item in obj:
                extract_skills(item)
    
    extract_skills(data)
    return skills

def extract_linkedin_jobs() -> list[dict[str, str]]:
    """Extract all LinkedIn jobs from database"""
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT job_id, actual_role, job_description, skills, url 
        FROM jobs WHERE platform='linkedin'
    """)
    jobs = []
    for row in cursor.fetchall():
        jobs.append({
            'job_id': row[0],
            'role': row[1],
            'description': row[2] or '',
            'extracted_skills': row[3] or '',
            'url': row[4]
        })
    conn.close()
    return jobs

def analyze_skills(jobs: list[dict[str, str]], reference_skills: set[str]) -> dict:
    """Analyze false positives and false negatives"""
    false_positives = Counter()  # Extracted but not real skills
    false_negatives = Counter()  # In description but not extracted
    
    for job in jobs:
        extracted = set(s.strip().lower() for s in job['extracted_skills'].split(',') if s.strip())
        desc_lower = job['description'].lower()
        
        # False positives: extracted skills NOT in reference
        for skill in extracted:
            if skill and skill not in reference_skills:
                false_positives[skill] += 1
        
        # False negatives: reference skills in description but NOT extracted
        # Only count if skill appears in description AND not in extracted list
        for skill in reference_skills:
            # Skip single letter/very short noise words
            if len(skill) <= 2 and skill not in ['r', 'c', 'go']:
                continue
            # Check if skill appears in description with word boundaries
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, desc_lower) and skill not in extracted:
                # Verify it's not already extracted under a different name
                # (e.g., "llm" extracted as "Large Language Models")
                if not any(skill in ext_skill.lower() or ext_skill.lower() in skill 
                          for ext_skill in extracted):
                    false_negatives[skill] += 1
    
    return {
        'total_jobs_analyzed': len(jobs),
        'false_positives': dict(false_positives.most_common(100)),
        'false_negatives': dict(false_negatives.most_common(100)),
        'sample_jobs': jobs[:5]
    }

def main():
    """Run LinkedIn skill analysis"""
    print("🔍 Analyzing LinkedIn skills...")
    
    reference_skills = load_reference_skills()
    print(f"📚 Loaded {len(reference_skills)} reference skills")
    
    jobs = extract_linkedin_jobs()
    print(f"📋 Extracted {len(jobs)} LinkedIn jobs")
    
    analysis = analyze_skills(jobs, reference_skills)
    
    with open('linkedin_skill_analysis.json', 'w') as f:
        json.dump(analysis, f, indent=2)
    
    print(f"✅ Analysis saved to linkedin_skill_analysis.json")
    print(f"   False Positives: {len(analysis['false_positives'])} unique")
    print(f"   False Negatives: {len(analysis['false_negatives'])} unique")

if __name__ == "__main__":
    main()
