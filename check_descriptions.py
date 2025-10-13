"""Check and clean jobs with None descriptions from database"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "jobs.db"

def check_and_clean_descriptions() -> None:
    """Check for None descriptions by platform and remove them"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    print("=" * 80)
    print("📊 CHECKING JOB DESCRIPTIONS BY PLATFORM")
    print("=" * 80)
    
    # Check each platform
    platforms = ['linkedin', 'indeed', 'naukri']
    total_removed = 0
    
    for platform in platforms:
        # Count None descriptions
        cursor.execute("""
            SELECT COUNT(*) 
            FROM jobs 
            WHERE site = ? AND (description IS NULL OR description = '')
        """, (platform,))
        none_count = cursor.fetchone()[0]
        
        # Count total jobs
        cursor.execute("SELECT COUNT(*) FROM jobs WHERE site = ?", (platform,))
        total_count = cursor.fetchone()[0]
        
        print(f"\n{platform.upper()}:")
        print(f"   Total jobs: {total_count}")
        print(f"   None/Empty descriptions: {none_count}")
        print(f"   Valid descriptions: {total_count - none_count}")
        
        if none_count > 0:
            print(f"   🗑️  Removing {none_count} jobs with missing descriptions...")
            cursor.execute("""
                DELETE FROM jobs 
                WHERE site = ? AND (description IS NULL OR description = '')
            """, (platform,))
            total_removed += none_count
    
    conn.commit()
    
    print(f"\n{'=' * 80}")
    print(f"✅ CLEANUP COMPLETE")
    print(f"   Total jobs removed: {total_removed}")
    print(f"{'=' * 80}\n")
    
    # Show final counts
    print("📊 FINAL DATABASE STATE:")
    for platform in platforms:
        cursor.execute("SELECT COUNT(*) FROM jobs WHERE site = ?", (platform,))
        count = cursor.fetchone()[0]
        print(f"   {platform.capitalize()}: {count} jobs (all with descriptions)")
    
    conn.close()

if __name__ == "__main__":
    check_and_clean_descriptions()
