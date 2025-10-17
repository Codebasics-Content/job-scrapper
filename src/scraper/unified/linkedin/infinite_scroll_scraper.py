# LinkedIn Infinite Scroll URL Scraper with Real-Time Deduplication
# Clicks "See more jobs" button, counts only NEW URLs
import os
import asyncio
import logging
from typing import List
from playwright.async_api import async_playwright, ProxySettings
from src.models.models import JobUrlModel
from src.db.operations import JobStorageOperations
from .selector_config import SEARCH_SELECTORS
from .network_monitor import NetworkMonitor

logger = logging.getLogger(__name__)

async def scrape_linkedin_urls_infinite_scroll(
    keyword: str,
    location: str,
    limit: int = 10000,
    headless: bool = False
) -> List[JobUrlModel]:
    """Infinite scroll scraper with real-time deduplication"""
    
    # Database for real-time deduplication
    db_ops = JobStorageOperations()
    
    # Proxy configuration
    proxy_url = os.getenv("PROXY_URL")
    proxy_config = None
    if proxy_url:
        parts = proxy_url.replace("http://", "").split("@")
        if len(parts) == 2:
            auth, server = parts
            username, password = auth.split(":")
            proxy_config = ProxySettings(
                server=f"http://{server}",
                username=username,
                password=password
            )
        else:
            server = parts[0]
            proxy_config = ProxySettings(server=f"http://{server}")
        logger.info(f"🔗 Using proxy: {parts[1] if len(parts)==2 else parts[0]}")
    else:
        logger.info("🔗 No proxy - direct connection")
    
    search_url = f"https://www.linkedin.com/jobs/search/?keywords={keyword.replace(' ', '+')}&location={location.replace(' ', '+')}"
    # State tracking
    new_urls: List[JobUrlModel] = []
    seen_in_session: set[str] = set()
    total_duplicates_database = 0
    all_urls: list[str] = []
    total_scroll_rounds = 0
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless, proxy=proxy_config)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = await context.new_page()
        
        # Setup network monitoring
        network_monitor = NetworkMonitor()
        page.on("response", network_monitor.handle_response)
        
        try:
            await page.goto(search_url, timeout=60000)
            
            # Close popup/ad (human behavior)
            await asyncio.sleep(2)  # Wait for popup to appear
            try:
                close_button = await page.query_selector("xpath=/html/body/div[4]/div/div/section/button")
                if close_button:
                    await close_button.click()
                    logger.info("✅ Closed popup/ad")
                    await asyncio.sleep(0.5)
            except Exception:
                pass  # No popup, continue
            
            # Try fallback selectors until one works
            job_cards_loaded = False
            for selector in SEARCH_SELECTORS["job_card"]:
                try:
                    await page.wait_for_selector(selector, timeout=10000)
                    logger.info(f"📄 Loaded page with selector: {selector}")
                    job_cards_loaded = True
                    break
                except Exception:
                    continue
            
            if not job_cards_loaded:
                raise Exception("No job cards found with any selector")
            
            # Phase 1: Scroll to END to load ALL jobs
            print(f"\n{'='*70}")
            print(f"📜 PHASE 1: SCROLLING TO LOAD ALL JOBS")
            print(f"{'='*70}\n")
            
            max_scroll_rounds = 20
            scroll_attempts_without_new = 0
            max_attempts_without_new = 3
            previous_card_count = 0
            
            while total_scroll_rounds < max_scroll_rounds:
                
                # Count job cards on current page
                job_cards = []
                for selector in SEARCH_SELECTORS["job_card"]:
                    job_cards = await page.query_selector_all(selector)
                    if job_cards:
                        break
                
                current_card_count = len(job_cards)
                print(f"\n📊 Scroll Round #{total_scroll_rounds + 1}: {current_card_count} job cards loaded")
                
                # Check if new cards loaded
                if current_card_count == previous_card_count:
                    scroll_attempts_without_new += 1
                    print(f"⚠️  No new jobs loaded ({scroll_attempts_without_new}/{max_attempts_without_new})")
                    if scroll_attempts_without_new >= max_attempts_without_new:
                        print(f"\n🛑 Reached end - no more jobs loading")
                        break
                else:
                    scroll_attempts_without_new = 0
                    previous_card_count = current_card_count
                
                total_scroll_rounds += 1
                
                # Human-like scrolling
                scroll_count = 3 + (total_scroll_rounds % 3)
                print(f"📜 Scrolling {scroll_count} times...")
                for i in range(scroll_count):
                    await page.evaluate("window.scrollBy(0, 800)")
                    await asyncio.sleep(1.5 + (i * 0.3))
                    print(f"   ↓ Scroll {i+1}/{scroll_count} completed")
                
                # Check for infinite loader (jobs stuck loading)
                try:
                    loader = await page.query_selector(".jobs-search-results__list-item--is-loading")
                    if loader and current_card_count == previous_card_count:
                        print(f"⚠️  Infinite loader detected - no new jobs loading")
                        logger.warning(f"🛑 Stopping: Jobs stuck in loading state")
                        break
                except Exception:
                    pass
                
                # Check network health
                status = network_monitor.get_status()
                if status["rate_limited"]:
                    print(f"🚫 Rate limiting detected - stopping to prevent blocking")
                    logger.warning(f"🛑 LinkedIn rate limit active")
                    break
                
                # Wait for new jobs to load after scroll
                await asyncio.sleep(2)
            
            # Phase 2: Extract ALL URLs at once
            print(f"\n{'='*70}")
            print(f"🔍 PHASE 2: EXTRACTING ALL JOB URLS")
            print(f"{'='*70}\n")
            
            # Get all job cards from fully loaded page
            all_job_cards = []
            for selector in SEARCH_SELECTORS["job_card"]:
                all_job_cards = await page.query_selector_all(selector)
                if all_job_cards:
                    break
            
            print(f"📄 Total job cards found: {len(all_job_cards)}")
            
            # Extract all URLs
            all_urls = []
            for card in all_job_cards:
                link = None
                for link_selector in SEARCH_SELECTORS["job_link"]:
                    link = await card.query_selector(link_selector)
                    if link:
                        break
                
                if link:
                    try:
                        url = await link.get_attribute('href')
                        if url and 'linkedin.com/jobs/view/' in url:
                            url = url.split('?')[0]
                            if url not in seen_in_session:
                                all_urls.append(url)
                                seen_in_session.add(url)
                    except Exception as e:
                        logger.debug(f"Error extracting URL: {e}")
            
            print(f"📊 Unique URLs extracted: {len(all_urls)}")
            
            # Phase 3: Database deduplication
            print(f"\n{'='*70}")
            print(f"💾 PHASE 3: DATABASE DEDUPLICATION")
            print(f"{'='*70}\n")
            
            if all_urls:
                existing_urls = db_ops.get_existing_urls(all_urls)
                total_duplicates_database = len(existing_urls)
            else:
                existing_urls = set()
                total_duplicates_database = 0
            
            print(f"✅ Already in database: {total_duplicates_database}")
            print(f"🆕 New URLs to add: {len(all_urls) - total_duplicates_database}")
            
            # Create models for new URLs only
            for url in all_urls:
                if url not in existing_urls and len(new_urls) < limit:
                    job_id = f"linkedin_{url.split('/')[-1]}"
                    new_urls.append(JobUrlModel(
                        job_id=job_id,
                        platform="linkedin",
                        input_role=keyword,
                        actual_role=keyword,
                        url=url
                    ))
                    print(f"✅ NEW #{len(new_urls)}/{limit}: {url[:70]}")
            
            # Summary
            if total_scroll_rounds >= max_scroll_rounds:
                print(f"\n⏱️  Max scroll rounds ({max_scroll_rounds}) reached")
            
        except Exception as e:
            logger.error(f"Scraping error: {e}")
        finally:
            # Print network summary before closing
            network_monitor.print_summary()
            await context.close()
            await browser.close()
    
    print(f"\n{'='*70}")
    print(f"✅ SCRAPING COMPLETED")
    print(f"{'='*70}")
    print(f"📊 FINAL STATISTICS:")
    print(f"   ├─ Total jobs found: {len(all_urls)}")
    print(f"   ├─ Already in database: {total_duplicates_database}")
    print(f"   ├─ NEW URLs collected: {len(new_urls)}")
    print(f"   └─ Scroll rounds completed: {total_scroll_rounds}")
    print(f"{'='*70}\n")
    return new_urls
