"""Fix patterns to achieve 100% accuracy by analyzing actual job text."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import sqlite3
import json
import re

# Load reference JSON
with open("skills_reference_2025.json") as f:
    ref_data = json.load(f)

# Get test job with mismatches
conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()
cursor.execute("""
    SELECT job_description, skills 
    FROM jobs 
    WHERE skills LIKE '%Large Language Models%' 
    LIMIT 1
""")
job_desc, skills = cursor.fetchone()
conn.close()

print("JOB DESCRIPTION SNIPPET:")
print(job_desc[:500])
print("\nSTORED SKILLS:")
print(skills)

# Check patterns
print("\n" + "="*70)
print("PATTERN ANALYSIS:")
print("="*70)

# LLM pattern check
if "LLM's" in job_desc or "LLMs" in job_desc:
    print("\n✓ Found 'LLM's' or 'LLMs' in description")
    print("  Current pattern: ['llm', 'llms', 'large language models']")
    print("  Issue: Pattern 'llms' won't match \"LLM's\" (with apostrophe)")
    print("  FIX: Add pattern with apostrophe handling")

# Monday.com pattern check  
if "Monday" in job_desc:
    print("\n✓ Found 'Monday' in description")
    print("  Context:", [line for line in job_desc.split('.') if 'Monday' in line][0][:100])
    print("  Current pattern: ['monday.com', 'monday']")
    print("  Issue: 'monday' pattern too broad - matches day of week")
    print("  FIX: Make pattern more specific with word boundaries")

print("\n" + "="*70)
