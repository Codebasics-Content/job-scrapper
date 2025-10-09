#!/usr/bin/env python3
# Update Skills Databases with Modern AI/ML Terms
# EMD Compliance: ≤80 lines

import sys
import logging
from pathlib import Path

# Add src to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

# Import with error handling - suppress type checker warnings for dynamic import
try:
    from analysis.skill_normalizer import ModernAISkillsUpdater, SkillDatabaseUpdater # type: ignore[import-untyped]
except ImportError as e:
    logging.error(f"Failed to import skill modules: {e}")
    sys.exit(1)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Update both skill databases with modern AI/ML skills"""
    project_root = Path(__file__).parent.parent
    
    # File paths
    token_dist_path = project_root / "token_dist.json"
    skill_db_path = project_root / "skill_db_relax_20.json"
    
    logger.info("Starting skills database update...")
    
    try:
        # Initialize updaters
        ai_skills_updater = ModernAISkillsUpdater()
        skill_db_updater = SkillDatabaseUpdater(skill_db_path)
        
        # Update token distribution
        logger.info("Updating token distribution database...")
        ai_skills_updater.update_token_dist(token_dist_path)
        
        # Update skill database
        logger.info("Updating skill database...")
        skill_db_updater.add_modern_ai_skills(ai_skills_updater.MODERN_AI_SKILLS)
        
        logger.info("Successfully updated both skill databases!")
        
        # Print summary
        skills_count = len(ai_skills_updater.MODERN_AI_SKILLS)
        logger.info(f"Added {skills_count} modern AI/ML skills to databases")
        
    except Exception as error:
        logger.error(f"Error updating skill databases: {error}")
        sys.exit(1)

if __name__ == "__main__":
    main()
