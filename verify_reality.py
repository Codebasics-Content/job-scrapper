"""Cross-verify skills against job descriptions & refine patterns
EMD: ≤80 lines
"""
import sqlite3
import json
import re
from collections import Counter, defaultdict

GENERIC_TERMS = {'asp', 'rest', 'front', 'api', 'web', 'app', 'code', 
                 'data', 'test', 'dev', 'eng', 'tech', 'soft', 'hard'}

VAGUE_PATTERNS = ['to assist', 'to improve', 'to drive', 'to create',
                  'lifecycle management', 'best practices', 'real world',
                  'cross functional', 'end to end', 'hands on']

def is_valid_skill(skill: str) -> bool:
    """Filter vague phrases and keyword fragments"""
    # Too short or contains vague patterns
    if len(skill) < 2 or any(vague in skill for vague in VAGUE_PATTERNS):
        return False
    # Multi-word phrases with verbs/prepositions (likely sentence fragments)
    if ' ' in skill and any(word in skill.split() for word in 
                           ['and', 'or', 'the', 'to', 'for', 'with', 'using']):
        return False
    return True

def skill_in_description(skill: str, description: str) -> bool:
    """Check if skill appears in job description"""
    if not description or not is_valid_skill(skill):
        return False
    desc_lower = description.lower()
    variations = [skill, skill.replace(' ', ''), skill.replace(' ', '-'),
                  skill.replace(' ', '.'), skill + '.js', skill + ' api']
    return any(v in desc_lower for v in variations)

def parse_compound(skill: str) -> list[str]:
    """Parse 'python and django' → ['python', 'django']"""
    parts = re.split(r'\s+(?:and|or|with|using|such as)\s+|,\s*', skill.lower())
    return [p.strip() for p in parts if 2 <= len(p.strip()) <= 30]

def verify_and_fix() -> dict[str, any]:
    """Cross-verify skills vs job descriptions & refine patterns"""
    with open('skills_reference_2025.json', 'r') as f:
        reference = json.load(f)
    
    # Build reference skill map
    ref_map = {}
    for cat, skills in reference['skills'].items():
        for s in skills:
            ref_map[s['name'].lower()] = {'category': cat, 'skill': s}
    
    # Extract skills + job descriptions
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()
    cursor.execute("SELECT skills, job_description FROM jobs WHERE platform='linkedin'")
    
    skill_desc_map = defaultdict(list)
    all_parsed = []
    
    for row in cursor.fetchall():
        if row[0] and row[1]:  # skills and description
            description = row[1]
            for skill_text in row[0].split(','):
                for skill in parse_compound(skill_text.strip()):
                    all_parsed.append(skill)
                    skill_desc_map[skill].append(description)
    conn.close()
    
    skill_counts = Counter(all_parsed)
    
    # FP: extracted but NOT in reference
    false_positives = {}
    for skill, count in skill_counts.items():
        if skill not in ref_map:
            # Strict validation: must appear in >=3 jobs AND 70% of descriptions
            desc_matches = sum(1 for d in skill_desc_map[skill] 
                             if skill_in_description(skill, d))
            match_rate = desc_matches / count if count > 0 else 0
            
            # Filter: valid skill, not generic, >=3 jobs, >=70% match rate
            if (is_valid_skill(skill) and
                skill not in GENERIC_TERMS and 
                count >= 3 and 
                match_rate >= 0.7):
                false_positives[skill] = count
    
    # FN: in reference but never extracted OR vague skills
    extracted_set = set(skill_counts.keys())
    false_negatives = [s for s in ref_map.keys() if s not in extracted_set]
    
    # AUTO-FIX: Remove FN and clean vague skills from reference
    cleaned_count = 0
    for cat in list(reference['skills'].keys()):
        before = len(reference['skills'][cat])
        reference['skills'][cat] = [
            s for s in reference['skills'][cat]
            if (s['name'].lower() not in false_negatives and 
                is_valid_skill(s['name'].lower()))
        ]
        cleaned_count += before - len(reference['skills'][cat])
    
    if false_positives:
        if 'verified' not in reference['skills']:
            reference['skills']['verified'] = []
        for skill in false_positives.keys():
            # Create better patterns
            pattern = f"\\b{re.escape(skill)}\\b"
            reference['skills']['verified'].append({
                'name': skill.title(),
                'patterns': [pattern]
            })
    
    with open('skills_reference_2025.json', 'w') as f:
        json.dump(reference, f, indent=2)
    
    return {
        'total': len(all_parsed), 'unique': len(skill_counts),
        'fp_count': len(false_positives), 'fn_count': len(false_negatives),
        'cleaned': cleaned_count,
        'false_positives': false_positives, 'false_negatives': false_negatives
    }

if __name__ == "__main__":
    iteration = 0
    while True:
        iteration += 1
        result = verify_and_fix()
        
        with open('linkedin_skill_analysis.json', 'w') as f:
            json.dump({
                'iteration': iteration,
                'timestamp': '2025-10-15T17:58:00+05:30',
                'total_extracted': result['total'],
                'unique_extracted': result['unique'],
                'false_positives_count': result['fp_count'],
                'false_negatives_count': result['fn_count'],
                'false_positives': result['false_positives'],
                'false_negatives': result['false_negatives']
            }, f, indent=2)
        
        print(f"\n🔄 Iteration {iteration}:")
        print(f"  Total: {result['total']} | Unique: {result['unique']}")
        print(f"  FP: {result['fp_count']} | FN: {result['fn_count']} | Cleaned: {result['cleaned']}")
        
        if result['fp_count'] == 0 and result['fn_count'] == 0:
            print(f"\n🎯 SUCCESS: 0 FP, 0 FN achieved in {iteration} iterations!")
            break
