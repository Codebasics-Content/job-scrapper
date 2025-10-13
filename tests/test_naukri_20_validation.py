"""Test Naukri Unified with 20 jobs + visible browser (≤80 lines)"""
from __future__ import annotations

import logging
import sys
import asyncio
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scraper.unified.naukri_unified import scrape_naukri_jobs_unified
from src.db.operations import JobStorageOperations

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


async def test_naukri_validation() -> None:
    """Test Naukri Unified: 20 jobs with visible browser"""
    logger.info("="*70)
    logger.info("🧪 NAUKRI UNIFIED TEST: 20 Jobs (Visible Browser)")
    logger.info("="*70)
    
    start = datetime.now()
    
    # Scrape 20 jobs using unified scraper with visible browser
    jobs = await scrape_naukri_jobs_unified(
        keyword="AI Engineer",
        location="",
        limit=20,
        headless=False,  # Visible browser bypasses CAPTCHA
    )
    
    duration = (datetime.now() - start).total_seconds()
    
    # Query from database for validation
    logger.info("\n" + "="*70)
    logger.info("📊 VALIDATION RESULTS")
    logger.info("="*70)
    
    db_ops = JobStorageOperations()
    conn = db_ops.get_connection()
    cursor = conn.execute(
        "SELECT job_description FROM jobs WHERE platform='naukri' ORDER BY created_at DESC LIMIT 20"
    )
    db_jobs = cursor.fetchall()
    
    total = len(db_jobs)
    logger.info(f"Total Jobs in DB: {total}")
    
    valid_pct = 0.0
    
    if total > 0:
        valid_desc = [j for j in db_jobs if j[0] and len(str(j[0])) > 50 and str(j[0]) != "None"]
        valid_count = len(valid_desc)
        valid_pct = (valid_count / total * 100)
        avg_len = sum(len(str(j[0])) for j in valid_desc) / len(valid_desc) if valid_desc else 0
        
        logger.info(f"✅ Valid Descriptions (>50 chars): {valid_count}/{total} ({valid_pct:.1f}%)")
        logger.info(f"   Avg Length: {avg_len:.0f} chars")
        
        if valid_desc:
            sample = str(valid_desc[0][0])[:100]
            logger.info(f"   Sample: {sample}...")
    
    logger.info(f"\n⏱️  Duration: {duration:.1f}s")
    logger.info(f"{'✅ PASS' if valid_pct >= 80 else '❌ FAIL'}: {valid_pct:.1f}% valid (need ≥80%)")


if __name__ == "__main__":
    asyncio.run(test_naukri_validation())
