# LinkedIn Scraper Test Script
# EMD Compliance: ≤80 lines for testing LinkedIn scraper functionality

import asyncio
import logging
from scrapers.linkedin import LinkedInScraper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_linkedin_scraper():
    """Test the LinkedIn scraper with a small dataset"""
    print("Testing LinkedIn Scraper Implementation...")
    
    # Initialize the LinkedIn scraper
    linkedin_scraper = LinkedInScraper()
    
    try:
        # Test with context manager to ensure proper cleanup
        with linkedin_scraper:
            print(f"Pool status: {linkedin_scraper.pool_status}")
            
            # Test scraping with a small number of jobs
            test_role = "Python Developer"
            target_count = 5
            
            print(f"Scraping {target_count} jobs for '{test_role}'...")
            jobs = await linkedin_scraper.scrape_jobs(test_role, target_count)
            
            print(f"\n=== SCRAPING RESULTS ===")
            print(f"Jobs found: {len(jobs)}")
            
            # Display sample job data
            for i, job in enumerate(jobs[:3]):  # Show first 3 jobs
                print(f"\nJob {i+1}:")
                print(f"  ID: {job.job_id}")
                print(f"  Title: {job.job_role}")
                print(f"  Company: {job.company}")
                print(f"  Platform: {job.platform}")
                print(f"  Location: {job.location}")
                
    except Exception as error:
        print(f"Error during testing: {error}")
        
    print("\nLinkedIn Scraper test completed!")

if __name__ == "__main__":
    # Run the test
    asyncio.run(test_linkedin_scraper())
