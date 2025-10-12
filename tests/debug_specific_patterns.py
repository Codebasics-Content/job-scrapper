"""Debug specific pattern matching for LLM and Monday.com."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import re
import sqlite3

# Get the problematic job
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

print("STORED SKILLS:", skills)
print("\n" + "="*70)

# Test LLM pattern
llm_patterns = ["llm[''']?s?", "large language models"]
print("\nTESTING LLM PATTERNS:")
for pattern in llm_patterns:
    matches = re.findall(pattern, job_desc, re.IGNORECASE)
    print(f"  Pattern '{pattern}': {matches[:5] if matches else 'NO MATCH'}")

# Check for actual LLM mentions
if "LLM" in job_desc or "llm" in job_desc.lower():
    print(f"\n  ✓ Text contains 'LLM' or 'llm'")
    # Find exact context
    for line in job_desc.split('.'):
        if 'llm' in line.lower():
            print(f"    Context: {line.strip()[:100]}")

# Test Monday.com pattern
monday_patterns = ["monday\\.com"]
print("\n" + "="*70)
print("\nTESTING MONDAY.COM PATTERNS:")
for pattern in monday_patterns:
    matches = re.findall(pattern, job_desc, re.IGNORECASE)
    print(f"  Pattern '{pattern}': {matches[:5] if matches else 'NO MATCH'}")

# Check for Monday mentions
print(f"\n  Monday mentions:")
for line in job_desc.split('.'):
    if 'monday' in line.lower():
        print(f"    {line.strip()[:120]}")
