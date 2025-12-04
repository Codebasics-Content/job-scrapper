#!/usr/bin/env python3
"""
Standalone LinkedIn Job Scraper Script
Run directly from terminal: python run_scraper.py

Phase 1: Scrape job URLs (infinite scroll)
Phase 2: Scrape job details from URLs
"""

import asyncio
import logging
import sys
from datetime import datetime

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)


async def phase1_scrape_urls(keyword: str, location: str, limit: int = 100):
    """Phase 1: Scrape LinkedIn job URLs using infinite scroll"""
    from src.scraper.unified.linkedin.infinite_scroll_scraper import (
        scrape_linkedin_urls_infinite_scroll,
    )
    from src.db.operations import JobStorageOperations

    print("\n" + "=" * 60)
    print(f"PHASE 1: Scraping {limit} LinkedIn Job URLs")
    print(f"Keyword: {keyword} | Location: {location}")
    print("Mode: Visible Browser (headless=False)")
    print("=" * 60 + "\n")

    urls = await scrape_linkedin_urls_infinite_scroll(
        keyword=keyword, location=location, limit=limit
    )

    print(f"\n✅ Phase 1 Complete: {len(urls)} URLs collected")

    if urls:
        db = JobStorageOperations("data/jobs.db")
        stored = db.store_urls(urls)
        print(f"📦 Stored {stored} NEW URLs to database")

    return urls


async def phase2_scrape_details(platform: str, role: str, batch_size: int = 100):
    """Phase 2: Scrape job details from stored URLs"""
    from src.scraper.unified.linkedin.sequential_detail_scraper import (
        scrape_job_details_sequential,
    )
    from src.db.operations import JobStorageOperations

    db = JobStorageOperations("data/jobs.db")

    # Get unscraped URLs
    urls = db.get_unscraped_urls(platform, role, batch_size)

    if not urls:
        print(f"\n⚠️ No unscraped URLs found for {role} on {platform}")
        return []

    print("\n" + "=" * 60)
    print(f"PHASE 2: Scraping {len(urls)} Job Details")
    print(f"Platform: {platform} | Role: {role}")
    print("Mode: Visible Browser (headless=False)")
    print("=" * 60 + "\n")

    results = await scrape_job_details_sequential(
        urls=urls, headless=False, prefetch_size=5
    )

    print(f"\n✅ Phase 2 Complete: {len(results)} jobs scraped successfully")

    # Summary
    if results:
        all_skills = set()
        for job in results:
            if job.skills:
                for s in job.skills.split(","):
                    all_skills.add(s.strip())
        print(f"📊 Unique skills extracted: {len(all_skills)}")

    return results


async def full_scrape(
    keyword: str, location: str, url_limit: int = 100, detail_batch: int = 100
):
    """Run both phases: URL collection + Detail scraping"""

    start_time = datetime.now()
    print("\n" + "🚀" * 20)
    print("LINKEDIN JOB SCRAPER - FULL RUN")
    print(f"Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("🚀" * 20 + "\n")

    # Phase 1: Collect URLs
    urls = await phase1_scrape_urls(keyword, location, url_limit)

    # Phase 2: Scrape details
    if urls:
        jobs = await phase2_scrape_details("linkedin", keyword, detail_batch)
    else:
        # Try scraping existing unscraped URLs
        jobs = await phase2_scrape_details("linkedin", keyword, detail_batch)

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    print("\n" + "=" * 60)
    print("SCRAPING COMPLETE")
    print("=" * 60)
    print(f"Duration: {duration:.1f} seconds")
    print(f"URLs Collected: {len(urls) if urls else 0}")
    print(f"Jobs Scraped: {len(jobs) if jobs else 0}")
    print("=" * 60 + "\n")

    return urls, jobs


def show_menu():
    """Show interactive menu"""
    print("\n" + "=" * 60)
    print("LINKEDIN JOB SCRAPER")
    print("=" * 60)
    print("1. Full Scrape (URLs + Details)")
    print("2. Phase 1 Only (Scrape URLs)")
    print("3. Phase 2 Only (Scrape Details from existing URLs)")
    print("4. Check Database Status")
    print("5. Exit")
    print("=" * 60)
    return input("Select option (1-5): ").strip()


def check_db_status():
    """Show current database status"""
    import sqlite3

    conn = sqlite3.connect("data/jobs.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM job_urls")
    total_urls = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM job_urls WHERE scraped = 0")
    unscraped = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM jobs")
    total_jobs = cursor.fetchone()[0]

    print("\n" + "=" * 60)
    print("DATABASE STATUS")
    print("=" * 60)
    print(f"Total URLs: {total_urls}")
    print(f"Unscraped URLs: {unscraped}")
    print(f"Total Jobs: {total_jobs}")

    cursor.execute("""
        SELECT actual_role, COUNT(*)
        FROM job_urls
        WHERE scraped = 0
        GROUP BY actual_role
    """)
    roles = cursor.fetchall()
    if roles:
        print(f"\nUnscraped by Role:")
        for role, count in roles:
            print(f"  {role}: {count}")

    conn.close()
    print("=" * 60 + "\n")


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        # Command line arguments
        cmd = sys.argv[1].lower()

        if cmd == "full":
            keyword = sys.argv[2] if len(sys.argv) > 2 else "Data Engineer"
            location = sys.argv[3] if len(sys.argv) > 3 else "India"
            limit = int(sys.argv[4]) if len(sys.argv) > 4 else 100
            asyncio.run(full_scrape(keyword, location, limit, limit))

        elif cmd == "urls":
            keyword = sys.argv[2] if len(sys.argv) > 2 else "Data Engineer"
            location = sys.argv[3] if len(sys.argv) > 3 else "India"
            limit = int(sys.argv[4]) if len(sys.argv) > 4 else 100
            asyncio.run(phase1_scrape_urls(keyword, location, limit))

        elif cmd == "details":
            role = sys.argv[2] if len(sys.argv) > 2 else "Data Engineer"
            batch = int(sys.argv[3]) if len(sys.argv) > 3 else 100
            asyncio.run(phase2_scrape_details("linkedin", role, batch))

        elif cmd == "status":
            check_db_status()

        else:
            print("Usage:")
            print("  python run_scraper.py full [keyword] [location] [limit]")
            print("  python run_scraper.py urls [keyword] [location] [limit]")
            print("  python run_scraper.py details [role] [batch_size]")
            print("  python run_scraper.py status")

    else:
        # Interactive menu
        while True:
            choice = show_menu()

            if choice == "1":
                keyword = (
                    input("Enter keyword (default: Data Engineer): ").strip()
                    or "Data Engineer"
                )
                location = input("Enter location (default: India): ").strip() or "India"
                limit = input("Enter URL limit (default: 100): ").strip() or "100"
                asyncio.run(full_scrape(keyword, location, int(limit), int(limit)))

            elif choice == "2":
                keyword = (
                    input("Enter keyword (default: Data Engineer): ").strip()
                    or "Data Engineer"
                )
                location = input("Enter location (default: India): ").strip() or "India"
                limit = input("Enter URL limit (default: 100): ").strip() or "100"
                asyncio.run(phase1_scrape_urls(keyword, location, int(limit)))

            elif choice == "3":
                role = (
                    input("Enter role (default: Data Engineer): ").strip()
                    or "Data Engineer"
                )
                batch = input("Enter batch size (default: 100): ").strip() or "100"
                asyncio.run(phase2_scrape_details("linkedin", role, int(batch)))

            elif choice == "4":
                check_db_status()

            elif choice == "5":
                print("Goodbye!")
                break

            else:
                print("Invalid option. Please select 1-5.")


if __name__ == "__main__":
                print("Invalid option. Please select 1-5.")


if __name__ == '__main__':
    main()
