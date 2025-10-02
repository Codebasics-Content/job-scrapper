#!/usr/bin/env python3
"""Quick DB inspection script"""
import sqlite3
import json

conn = sqlite3.connect('jobs.db')
cursor = conn.cursor()

print("=== DATABASE INSPECTION ===\n")

# Check total jobs by platform
print("1. Jobs by Platform:")
cursor.execute("SELECT platform, COUNT(*) as count FROM jobs GROUP BY platform")
for row in cursor.fetchall():
    print(f"   {row[0]}: {row[1]} jobs")

print("\n2. Schema Check:")
cursor.execute("PRAGMA table_info(jobs)")
columns = cursor.fetchall()
column_names = [col[1] for col in columns]
print(f"   Columns ({len(column_names)}): {column_names}")

print("\n3. Sample Jobs by Platform:")
for platform in ['linkedin', 'Naukri']:
    print(f"\n   === {platform} ===")
    cursor.execute(f"""
        SELECT job_id, job_role, company, location, 
               LENGTH(skills) as skills_len,
               skills
        FROM jobs WHERE platform = ? LIMIT 2
    """, (platform,))
    
    for row in cursor.fetchall():
        job_id, job_role, company, location, skills_len, skills = row
        print(f"   Job ID: {job_id}")
        print(f"   Role: {job_role}")
        print(f"   Company: {company}")
        print(f"   Location: {location}")
        print(f"   Skills length: {skills_len} chars")
        
        if skills:
            try:
                skills_list = json.loads(skills)
                print(f"   Skills count: {len(skills_list)}")
                print(f"   Skills sample: {skills_list[:3]}")
            except:
                print(f"   Skills (raw): {skills[:50]}...")
        print()

conn.close()
