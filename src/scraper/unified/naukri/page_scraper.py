# Naukri Single Page URL Scraper - EMD Extracted Module
from __future__ import annotations

import logging
from pathlib import Path
from bs4 import BeautifulSoup

from src.scraper.services.playwright_browser import PlaywrightBrowser
from .selectors import CARD_SELECTORS_CSS
from .url_builder import normalize_job_url
from .card_parser import parse_search_card

logger = logging.getLogger(__name__)


async def scrape_page_urls(
    browser: PlaywrightBrowser,
    search_url: str,
    page_num: int,
    save_debug: bool = False
) -> list[tuple[str, str]]:
    """Scrape URLs from a single Naukri search page.
    
    Returns:
        List of (title, url) tuples
    """
    html = await browser.render_url(
        search_url, 
        wait_seconds=5.0, 
        timeout_ms=60000, 
        wait_until='networkidle'
    )
    
    if not html:
        logger.error(f"❌ No HTML returned for page {page_num}")
        return []
    
    logger.debug(f"📄 Page {page_num} HTML length: {len(html)} bytes")
    
    if save_debug:
        debug_file = Path("debug_naukri_listing.html")
        debug_file.write_text(html, encoding="utf-8")
        logger.info(f"✅ Saved HTML to {debug_file.absolute()}")
    
    soup = BeautifulSoup(html, "html.parser")
    urls: list[tuple[str, str]] = []
    
    for card_sel in CARD_SELECTORS_CSS:
        cards = soup.select(card_sel)
        logger.info(f"🔍 Page {page_num} selector '{card_sel}': {len(cards)} cards")
        
        for card in cards:
            card_data = parse_search_card(card)
            if card_data["url"] and card_data["title"]:
                url = normalize_job_url(card_data["url"]) or card_data["url"]
                urls.append((card_data["title"], url))
        
        if urls:
            break
    
    logger.info(f"✅ Page {page_num}: extracted {len(urls)} URLs")
    return urls
