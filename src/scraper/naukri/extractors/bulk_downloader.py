#!/usr/bin/env python3
# Simple bulk HTML downloader for Naukri jobs
# EMD Compliance: ≤80 lines

import logging
import os
import tempfile
import time
from typing import List, Dict
from selenium.webdriver.remote.webdriver import WebDriver

logger = logging.getLogger(__name__)

class NaukriBulkDownloader:
    """Simple bulk HTML downloader for job pages"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix="naukri_bulk_")
        logger.info(f"[BULK] Temp dir: {self.temp_dir}")
    
    def download_batch(self, driver: WebDriver, job_urls: List[str], 
                      batch_size: int = 20) -> List[Dict[str, str]]:
        """Download HTML files for job URLs in batches"""
        downloaded_files = []
        
        for i in range(0, len(job_urls), batch_size):
            batch_urls = job_urls[i:i + batch_size]
            logger.info(f"[BULK] Batch {i//batch_size + 1}: {len(batch_urls)} jobs")
            
            for j, url in enumerate(batch_urls):
                try:
                    driver.get(url)
                    time.sleep(2)  # Simple wait
                    
                    # Save HTML content
                    html_content = driver.page_source
                    filename = f"job_{i+j+1}.html"
                    filepath = os.path.join(self.temp_dir, filename)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    
                    downloaded_files.append({
                        'url': url,
                        'filepath': filepath,
                        'filename': filename
                    })
                    
                    logger.info(f"[BULK] Downloaded: {filename}")
                    
                except Exception as e:
                    logger.warning(f"[BULK] Failed {url}: {e}")
                    continue
        
        logger.info(f"[BULK] Downloaded {len(downloaded_files)} HTML files")
        return downloaded_files
    
    def cleanup(self):
        """Clean up temporary files"""
        try:
            import shutil
            shutil.rmtree(self.temp_dir)
            logger.info(f"[BULK] Cleaned up temp dir")
        except Exception as e:
            logger.warning(f"[BULK] Cleanup failed: {e}")
