"""Test Indeed with 20 jobs for description & skill validation (≤80 lines)"""
from __future__ import annotations

import logging
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scraper.jobspy import scrape_multi_platform

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


def test_indeed_validation() -> None:
    """Test Indeed: 20 jobs with description & skill validation"""
    logger.info("="*70)
    logger.info("🧪 INDEED VALIDATION TEST: 20 Jobs")
    logger.info("="*70)
    
    start = datetime.now()
    
    # Scrape 20 jobs from Indeed
    jobs_df = scrape_multi_platform(
        platforms=["indeed"],
        search_term="AI Engineer",
        location="",
        results_wanted=20,
        hours_old=72,
        linkedin_fetch_description=False,
    )
    
    duration = (datetime.now() - start).total_seconds()
    
    # Validation Analysis
    logger.info("\n" + "="*70)
    logger.info("📊 VALIDATION RESULTS")
    logger.info("="*70)
    
    total = len(jobs_df)
    logger.info(f"Total Jobs Scraped: {total}")
    
    # Check descriptions
    if 'description' in jobs_df.columns:
        valid_desc = jobs_df[
            (jobs_df['description'].notna()) & 
            (jobs_df['description'] != 'None') &
            (jobs_df['description'].str.len() > 50)
        ]
        valid_count = len(valid_desc)
        valid_pct = (valid_count / total * 100) if total > 0 else 0
        
        logger.info(f"✅ Valid Descriptions (>50 chars): {valid_count}/{total} ({valid_pct:.1f}%)")
        logger.info(f"   Avg Length: {valid_desc['description'].str.len().mean():.0f} chars")
        
        # Check skills extraction
        if 'skills' in jobs_df.columns:
            with_skills = jobs_df[jobs_df['skills'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False)]
            skills_count = len(with_skills)
            skills_pct = (skills_count / total * 100) if total > 0 else 0
            
            logger.info(f"🔍 Jobs with Skills Extracted: {skills_count}/{total} ({skills_pct:.1f}%)")
            logger.info(f"   Avg Skills per Job: {with_skills['skills'].apply(len).mean():.1f}")
            
            # Sample skills
            if skills_count > 0:
                sample_skills = with_skills.iloc[0]['skills'][:5]
                logger.info(f"   Sample Skills: {', '.join(sample_skills)}")
    
    logger.info(f"\n⏱️  Duration: {duration:.1f}s")
    logger.info(f"{'✅ PASS' if valid_pct >= 80 else '❌ FAIL'}: {valid_pct:.1f}% valid (need ≥80%)")


if __name__ == "__main__":
    test_indeed_validation()
