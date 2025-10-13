"""Validate job_description field behavior across all 3 platforms"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "jobs.db"

conn = sqlite3.connect(str(DB_PATH))
cursor = conn.cursor()

print("=" * 80)
print("📊 JOB DESCRIPTION VALIDATION BY PLATFORM")
print("=" * 80)

platforms = ['linkedin', 'indeed', 'naukri']

for platform in platforms:
    print(f"\n{'='*60}")
    print(f"🔍 {platform.upper()}")
    print('='*60)
    
    # Total jobs
    cursor.execute("SELECT COUNT(*) FROM jobs WHERE platform = ?", (platform,))
    total = cursor.fetchone()[0]
    
    # Valid descriptions (not NULL, not empty, not "None")
    cursor.execute("""
        SELECT COUNT(*) FROM jobs 
        WHERE platform = ? 
        AND job_description IS NOT NULL 
        AND job_description != '' 
        AND job_description != 'None'
        AND LENGTH(job_description) > 50
    """, (platform,))
    valid = cursor.fetchone()[0]
    
    # Invalid (NULL, empty, "None", or too short)
    cursor.execute("""
        SELECT COUNT(*) FROM jobs 
        WHERE platform = ? 
        AND (job_description IS NULL 
             OR job_description = '' 
             OR job_description = 'None'
             OR LENGTH(job_description) <= 50)
    """, (platform,))
    invalid = cursor.fetchone()[0]
    
    print(f"Total Jobs: {total}")
    print(f"✅ Valid Descriptions (>50 chars): {valid} ({valid/total*100 if total > 0 else 0:.1f}%)")
    print(f"❌ Invalid Descriptions: {invalid} ({invalid/total*100 if total > 0 else 0:.1f}%)")
    
    if valid > 0:
        # Sample valid description length
        cursor.execute("""
            SELECT AVG(LENGTH(job_description)) 
            FROM jobs 
            WHERE platform = ? 
            AND job_description IS NOT NULL 
            AND job_description != '' 
            AND job_description != 'None'
        """, (platform,))
        avg_len = cursor.fetchone()[0]
        print(f"📏 Average Description Length: {int(avg_len) if avg_len else 0} chars")
        
        # Sample one valid description
        cursor.execute("""
            SELECT actual_role, SUBSTR(job_description, 1, 100)
            FROM jobs 
            WHERE platform = ? 
            AND job_description IS NOT NULL 
            AND job_description != '' 
            AND job_description != 'None'
            LIMIT 1
        """, (platform,))
        row = cursor.fetchone()
        if row:
            print(f"📝 Sample: {row[0][:40]}")
            print(f"   Description: {row[1]}...")

print("\n" + "=" * 80)
print("🎯 RECOMMENDATION")
print("=" * 80)
print("""
Based on validation:
1. LinkedIn: Check if linkedin_fetch_description=True is working
2. Indeed: Should return descriptions by default
3. Naukri: Check if descriptions are available

⚠️  CRITICAL: Only extract skills from jobs with valid descriptions (>50 chars)
""")

conn.close()
