#!/usr/bin/env python3
# Validate extracted skills against job descriptions
# EMD Compliance: ≤80 lines

import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_skills_in_jd(db_path: str = "jobs.db") -> None:
    """Validate extracted skills actually appear in job descriptions"""
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT job_id, job_role, jd, skills FROM jobs LIMIT 10")
    jobs = cursor.fetchall()
    
    total_skills = 0
    matched_skills = 0
    mismatched_jobs = []
    
    for job_id, job_role, jd, skills_str in jobs:
        if not skills_str or not jd:
            continue
        
        jd_lower = jd.lower()
        skills = [s.strip() for s in skills_str.split(",")]
        
        job_matched = 0
        job_total = len(skills)
        total_skills += job_total
        
        print(f"\n{'='*80}")
        print(f"Job: {job_role[:50]}")
        print(f"Job ID: {job_id[:30]}")
        print(f"\nSkills validation:")
        
        for skill in skills:
            # Check if skill appears in JD
            if skill.lower() in jd_lower:
                job_matched += 1
                matched_skills += 1
                print(f"  ✓ {skill}")
            else:
                print(f"  ✗ {skill} (NOT FOUND IN JD)")
        
        match_rate = (job_matched / job_total * 100) if job_total > 0 else 0
        print(f"\nMatch rate: {job_matched}/{job_total} ({match_rate:.1f}%)")
        
        if match_rate < 70:
            mismatched_jobs.append((job_id, job_role, match_rate))
    
    overall_rate = (matched_skills / total_skills * 100) if total_skills > 0 else 0
    print(f"\n{'='*80}")
    print(f"OVERALL: {matched_skills}/{total_skills} skills found ({overall_rate:.1f}%)")
    
    if mismatched_jobs:
        print(f"\n⚠️  Jobs with <70% match rate:")
        for jid, role, rate in mismatched_jobs:
            print(f"  - {role[:40]}: {rate:.1f}%")
    
    conn.close()

if __name__ == "__main__":
    validate_skills_in_jd()
