#!/usr/bin/env python3
"""
Detailed gap analysis: Compare job descriptions with extracted skills
Shows exactly what skills are mentioned but not extracted
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import sqlite3
import json
import re
from typing import Any

def analyze_extraction_gaps(db_path: str, ref_path: str) -> None:
    """Detailed comparison of descriptions vs extracted skills"""
    
    # Load reference
    with open(ref_path) as f:
        ref_data = json.load(f)
    
    # Build skill name map
    skill_names = set()
    for category_skills in ref_data['skills'].values():
        for skill in category_skills:
            skill_names.add(skill['name'].lower())
    
    # Query database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT job_description, skills, company_name, actual_role
        FROM jobs 
        WHERE job_description IS NOT NULL 
        AND job_description != ''
        LIMIT 10
    """)
    
    results = cursor.fetchall()
    conn.close()
    
    print("="*80)
    print("DETAILED SKILL EXTRACTION GAP ANALYSIS")
    print("="*80)
    
    for idx, (desc, extracted_str, company, role) in enumerate(results, 1):
        print(f"\n{'='*80}")
        print(f"JOB {idx}: {company or 'Unknown'} - {role}")
        print(f"{'='*80}")
        
        # Parse extracted skills
        extracted = set()
        if extracted_str:
            extracted = {s.strip().lower() for s in extracted_str.split(',')}
        
        print(f"\n📊 Extracted Skills ({len(extracted)}):")
        if extracted:
            for skill in sorted(extracted):
                print(f"  ✓ {skill}")
        else:
            print("  (none)")
        
        # Find skills mentioned in description but not extracted
        mentioned_not_extracted = []
        desc_lower = desc.lower()
        
        for skill_name in skill_names:
            # Check if skill name appears in description
            if skill_name in desc_lower and skill_name not in extracted:
                mentioned_not_extracted.append(skill_name)
        
        print(f"\n🚨 Skills in Description BUT NOT Extracted ({len(mentioned_not_extracted)}):")
        if mentioned_not_extracted:
            for skill in sorted(mentioned_not_extracted)[:20]:  # Top 20
                # Show context
                pattern = re.compile(f'(.{{0,40}}{re.escape(skill)}.{{0,40}})', re.IGNORECASE)
                match = pattern.search(desc)
                context = match.group(1) if match else skill
                print(f"  ✗ {skill:25} → Context: ...{context}...")
        else:
            print("  (none - perfect extraction!)")
        
        # Calculate accuracy
        total_skills = len(extracted) + len(mentioned_not_extracted)
        if total_skills > 0:
            accuracy = (len(extracted) / total_skills) * 100
            print(f"\n📈 Extraction Accuracy: {accuracy:.1f}% ({len(extracted)}/{total_skills})")
        
        print()


if __name__ == "__main__":
    analyze_extraction_gaps("jobs.db", "skills_reference_2025.json")
