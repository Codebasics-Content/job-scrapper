# Progress Tracker Component - Real-time scraping progress display
# EMD Compliance: ≤80 lines

import streamlit as st

class ProgressTracker:
    """Manages real-time progress display for scraping operations"""
    
    def __init__(self, target_count: int, num_countries: int):
        self.target_count = target_count
        self.num_countries = num_countries
        self.container = st.container()
        self.status_text = self.container.empty()
        self.progress_bar = self.container.progress(0)
        
        metrics_col1, metrics_col2 = self.container.columns(2)
        self.scraped_metric = metrics_col1.empty()
        self.stored_metric = metrics_col2.empty()
        
    def update_loading(self, platform: str) -> None:
        """Update status to loading"""
        self.status_text.info(f"🌐 Loading {platform} page...")
        self.scraped_metric.metric("Jobs Scraped", "0", f"Target: {self.target_count}")
        self.stored_metric.metric("Jobs Stored", "0")
        
    def update_scraping(self) -> None:
        """Update status to scraping"""
        self.status_text.info(f"🌍 Scraping from {self.num_countries} countries in parallel...")
        self.progress_bar.progress(0.3)
        
    def update_scraped(self, scraped_count: int) -> None:
        """Update status after scraping complete"""
        self.progress_bar.progress(0.7)
        self.status_text.info(f"💾 Storing {scraped_count} jobs in database...")
        self.scraped_metric.metric("Jobs Scraped", scraped_count, "✓ Complete")
        
    def update_complete(self, scraped_count: int, stored_count: int) -> None:
        """Update status after storage complete"""
        self.progress_bar.progress(1.0)
        duplicates = scraped_count - stored_count
        
        # Show different message if fewer jobs available than requested
        if scraped_count < self.target_count:
            self.status_text.warning(
                f"⚠️ Only {scraped_count}/{self.target_count} jobs available on platform. "
                f"Stored {stored_count} new jobs."
            )
        else:
            self.status_text.success(
                f"✅ Completed! Scraped {scraped_count} jobs, stored {stored_count} new jobs"
            )
        
        self.stored_metric.metric(
            "Jobs Stored", 
            stored_count, 
            f"{duplicates} duplicates" if duplicates > 0 else "All new"
        )
        
    def update_error(self, error_msg: str) -> None:
        """Update status on error"""
        self.status_text.error(f"❌ Error: {error_msg}")
        self.progress_bar.progress(0)
