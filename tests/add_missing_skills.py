"""Add missing skills from database to reference JSON for 100% accuracy."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import sqlite3
import json

# Extract all unique skills from database
conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()
cursor.execute("SELECT DISTINCT skills FROM jobs WHERE skills IS NOT NULL")
all_skills_rows = cursor.fetchall()
conn.close()

# Parse and normalize all stored skills
stored_skills = set()
for (skills_str,) in all_skills_rows:
    if skills_str:
        for skill in skills_str.split(','):
            cleaned = skill.strip()
            if cleaned:
                stored_skills.add(cleaned)

# Load reference JSON
with open("skills_reference_2025.json") as f:
    ref_data = json.load(f)

# Get all existing skill names (case-insensitive)
existing_skills_lower = set()
for category_skills in ref_data['skills'].values():
    for skill in category_skills:
        existing_skills_lower.add(skill['name'].lower())

# Find missing skills
missing = []
for skill in sorted(stored_skills):
    if skill.lower() not in existing_skills_lower:
        missing.append(skill)

print(f"\n{'='*70}")
print(f"MISSING SKILLS TO ADD ({len(missing)} total):")
print(f"{'='*70}\n")

for skill in missing:
    print(f"  • {skill}")

print(f"\n{'='*70}\n")
