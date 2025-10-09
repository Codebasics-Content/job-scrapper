# Skill Normalizer Package
# EMD Compliance: ≤80 lines

# Import from the normalizer module within this package
from .normalizer import (
    normalize_skills_from_string,
    normalize_jobs_skills_enhanced,
    normalize_jobs_skills,
    load_skill_normalizer_config
)
from .modern_ai_skills import ModernAISkillsUpdater
from .skill_db_updater import SkillDatabaseUpdater

# Export functions
__all__ = [
    "normalize_skills_from_string",
    "normalize_jobs_skills_enhanced", 
    "normalize_jobs_skills",
    "load_skill_normalizer_config",
    "ModernAISkillsUpdater",
    "SkillDatabaseUpdater"
]
