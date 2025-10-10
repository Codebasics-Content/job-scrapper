#!/usr/bin/env python3
# Skill Database Updater - Updates skill_db_relax_20.json with modern AI skills
# EMD Compliance: ≤80 lines

import json
import logging
from pathlib import Path
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class SkillDatabaseUpdater:
    """Updates skill_db_relax_20.json with modern AI/ML skills"""
    
    def __init__(self, skill_db_path: Path):
        self.skill_db_path = skill_db_path
        self.skill_counter = 0
    
    def _generate_skill_id(self) -> str:
        """Generate unique string-based skill ID"""
        import random
        import string
        
        # Generate ID similar to existing format (e.g., KS126XS6CQCFGC3NG79X)
        prefix = "KSAI"  # AI skills prefix
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        skill_id = f"{prefix}{random_part}"
        self.skill_counter += 1
        return skill_id
    
    def add_modern_ai_skills(self, modern_skills: Dict[str, Dict[str, Any]]) -> None:
        """Add modern AI skills to skill database"""
        logger.info(f"Adding {len(modern_skills)} modern AI skills to database")
        
        with open(self.skill_db_path, 'r') as file:
            skill_db = json.load(file)
        
        for skill_name, skill_data in modern_skills.items():
            # Generate unique skill ID
            skill_id = self._generate_skill_id()
            
            # Create skill entry matching existing structure
            skill_entry = {
                "skill_name": skill_name.title(),
                "skill_type": skill_data["type"],
                "skill_len": len(skill_data["tokens"]),
                "high_surfce_forms": {"full": skill_name.lower()},
                "low_surface_forms": self._generate_surface_forms(skill_name, skill_data["tokens"]),
                "match_on_tokens": len(skill_data["tokens"]) > 2
            }
            
            skill_db[skill_id] = skill_entry
        
        # Write updated database
        with open(self.skill_db_path, 'w') as file:
            json.dump(skill_db, file, separators=(',', ':'))
        
        logger.info(f"Successfully added {len(modern_skills)} skills")
    
    def _generate_surface_forms(self, skill_name: str, tokens: List[str]) -> List[str]:
        """Generate surface forms for skill matching"""
        surface_forms = [skill_name, skill_name.lower(), skill_name.upper()]
        
        # Add token variations
        surface_forms.extend(tokens)
        surface_forms.extend([token.upper() for token in tokens])
        surface_forms.extend([token.capitalize() for token in tokens])
        
        # Add joined variations for multi-token skills
        if len(tokens) > 1:
            joined = ''.join(tokens)
            surface_forms.extend([joined, joined.upper(), joined.capitalize()])
        
        return list(set(surface_forms))  # Remove duplicates
