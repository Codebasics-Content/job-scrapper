#!/usr/bin/env python3
# Batch skill extraction processor for post-scraping
# EMD Compliance: ≤80 lines

import logging
import asyncio
from typing import Callable
from src.scraper.base.dynamic_skill_extractor import extract_dynamic_skills

logger = logging.getLogger(__name__)

async def process_skills_batch(
    jobs_data: list[tuple[str, str]],  # (job_id, job_description)
    update_callback: Callable[[str, list[str]], None],
    batch_size: int = 10
) -> int:
    """Process skills extraction for scraped jobs in batches
    
    Args:
        jobs_data: List of (job_id, description) tuples
        update_callback: Function to update job with extracted skills
        batch_size: Number of jobs to process concurrently
        
    Returns:
        Number of jobs processed
    """
    total = len(jobs_data)
    processed = 0
    
    logger.info(f"🔧 Starting batch skill extraction for {total} jobs...")
    
    for i in range(0, total, batch_size):
        batch = jobs_data[i:i + batch_size]
        
        # Process batch concurrently
        tasks = [
            _extract_and_update(job_id, description, update_callback)
            for job_id, description in batch
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Count successful extractions
        batch_processed = sum(1 for r in results if isinstance(r, int) and r > 0)
        processed += batch_processed
        
        logger.info(
            f"✅ Batch {i//batch_size + 1}/{(total + batch_size - 1)//batch_size}: "
            f"{batch_processed}/{len(batch)} jobs processed"
        )
    
    logger.info(f"🎉 Batch processing complete: {processed}/{total} jobs updated")
    return processed


async def _extract_and_update(
    job_id: str,
    description: str,
    update_callback: Callable[[str, list[str]], None]
) -> int:
    """Extract skills and update single job"""
    try:
        # Run CPU-intensive SkillNER in thread pool
        loop = asyncio.get_event_loop()
        skills = await loop.run_in_executor(
            None,
            extract_dynamic_skills,
            description
        )
        
        # Update job with extracted skills
        if skills:
            update_callback(job_id, skills)
            return len(skills)
        
        return 0
        
    except Exception as error:
        logger.error(f"Failed to extract skills for {job_id}: {error}")
        return 0
