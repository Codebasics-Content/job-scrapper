"""Analyze false positives and missing skills in stored data."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import sqlite3
from src.analysis.skill_extraction import extract_skills_advanced
from collections import Counter

# Analyze sample jobs
conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()
cursor.execute("""
    SELECT job_description, skills 
    FROM jobs 
    WHERE skills IS NOT NULL 
    LIMIT 50
""")
jobs = cursor.fetchall()
conn.close()

false_positives = Counter()
only_in_extracted = Counter()
only_in_stored = Counter()

for job_desc, stored_skills_str in jobs:
    if not stored_skills_str:
        continue
    
    extracted = extract_skills_advanced(job_desc, "skills_reference_2025.json")
    stored = [s.strip() for s in stored_skills_str.split(',')]
    
    extracted_lower = {s.lower() for s in extracted}
    stored_lower = {s.lower() for s in stored}
    
    # Skills only in stored (potential false positives)
    for skill in stored:
        if skill.lower() not in extracted_lower:
            only_in_stored[skill] += 1
    
    # Skills only in extracted (potential additions)
    for skill in extracted:
        if skill.lower() not in stored_lower:
            only_in_extracted[skill] += 1

print("="*70)
print("FALSE POSITIVES (in stored but not extracted):")
print("="*70)
for skill, count in only_in_stored.most_common(20):
    print(f"{skill:40} {count:3} occurrences")

print("\n" + "="*70)
print("MISSING SKILLS (extracted but not in stored):")
print("="*70)
for skill, count in only_in_extracted.most_common(30):
    print(f"{skill:40} {count:3} occurrences")
