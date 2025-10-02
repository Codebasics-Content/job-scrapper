#!/usr/bin/env python3
# Browser cleanup utilities for LinkedIn scraper
# EMD Compliance: ≤80 lines

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...base.window_manager import WindowManager

logger = logging.getLogger(__name__)

async def cleanup_browsers(window_manager: "WindowManager") -> None:
    """Close all browser windows and cleanup resources
    
    Args:
        window_manager: Window manager instance with active browsers
    """
    try:
        window_count = window_manager.window_count()
        logger.info(f"🧹 [CLEANUP] Closing {window_count} browser windows...")
        
        # Close all windows
        window_manager.close_all()
        
        logger.info("✅ [CLEANUP] All browser windows closed successfully")
        
    except Exception as error:
        logger.error(f"❌ [CLEANUP] Failed to close browsers: {error}")
        # Don't raise - cleanup is best effort
