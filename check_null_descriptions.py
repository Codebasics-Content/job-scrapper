"""Deep check for NULL/None descriptions in database"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "jobs.db"

conn = sqlite3.connect(str(DB_PATH))
cursor = conn.cursor()

# Check for SQL NULL
cursor.execute("SELECT COUNT(*) FROM jobs WHERE job_description IS NULL")
null_count = cursor.fetchone()[0]
print(f"SQL NULL descriptions: {null_count}")

# Check for empty strings
cursor.execute("SELECT COUNT(*) FROM jobs WHERE job_description = ''")
empty_count = cursor.fetchone()[0]
print(f"Empty string descriptions: {empty_count}")

# Check for string "None"
cursor.execute("SELECT COUNT(*) FROM jobs WHERE job_description = 'None'")
none_string_count = cursor.fetchone()[0]
print(f"String 'None' descriptions: {none_string_count}")

# Total invalid
cursor.execute("""
    SELECT COUNT(*) FROM jobs 
    WHERE job_description IS NULL 
       OR job_description = '' 
       OR job_description = 'None'
""")
total_invalid = cursor.fetchone()[0]
print(f"\nTotal invalid descriptions: {total_invalid}")

# By platform
cursor.execute("""
    SELECT platform, COUNT(*) 
    FROM jobs 
    WHERE job_description IS NULL 
       OR job_description = '' 
       OR job_description = 'None'
    GROUP BY platform
""")
print("\nInvalid descriptions by platform:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")

# Sample some NULL records
cursor.execute("""
    SELECT job_id, platform, actual_role, job_description
    FROM jobs 
    WHERE job_description IS NULL 
       OR job_description = '' 
       OR job_description = 'None'
    LIMIT 5
""")
print("\nSample invalid records:")
for row in cursor.fetchall():
    desc_preview = str(row[3])[:50] if row[3] else "NULL"
    print(f"  {row[1]} | {row[2][:30]} | {desc_preview}")

conn.close()
