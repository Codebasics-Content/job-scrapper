#!/usr/bin/env python3
# Test Runner - Execute all Naukri fix tests
# EMD Compliance: ≤80 lines

import sys
import logging
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from test_naukri_fixes import test_description_extraction, test_ai_skills_detection

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Run all Naukri scraper fix tests"""
    logger.info("🚀 Starting Naukri scraper fix tests...")
    
    try:
        # Test 1: Description extraction
        logger.info("\n=== Test 1: Full Description Extraction ===")
        parsed_job = test_description_extraction()
        
        # Test 2: AI skills detection
        logger.info("\n=== Test 2: Modern AI Skills Detection ===")
        extracted_skills = test_ai_skills_detection()
        
        # Summary
        logger.info("\n=== Test Summary ===")
        logger.info("✅ All tests passed successfully!")
        logger.info(f"✅ Full description extraction: Working")
        logger.info(f"✅ AI skills detection: {len(extracted_skills)} skills found")
        logger.info("✅ Naukri scraper fixes verified!")
        
        return True
        
    except Exception as error:
        logger.error(f"❌ Test failed: {error}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
