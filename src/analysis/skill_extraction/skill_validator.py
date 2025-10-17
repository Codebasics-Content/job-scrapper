# Skill Validator - Reference-Only Extraction (EMD ≤80 lines)
# Validates job descriptions against canonical 557 skills

import json
import re
from typing import Dict, List, Set, Union
from pathlib import Path

class SkillValidator:
    """Validates and extracts ONLY canonical skills from reference file"""
    
    def __init__(self, reference_path: str):
        self.reference_path = Path(reference_path)
        self.canonical_skills: List[Dict[str, Union[str, List[str]]]] = []
        self.skill_patterns: List[tuple[str, List[str]]] = []
        self._load_reference()
    
    def _load_reference(self) -> None:
        """Load 557 canonical skills with regex patterns"""
        with open(self.reference_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.canonical_skills = data['skills']
            
        # Build (skill_name, patterns) lookup
        for skill in self.canonical_skills:
            name = str(skill['name'])
            patterns = list(skill['patterns']) if isinstance(skill['patterns'], list) else []
            self.skill_patterns.append((name, patterns))
    
    def validate_and_extract(self, job_description: str) -> Set[str]:
        """Extract ONLY skills matching canonical 557 patterns"""
        if not job_description:
            return set()
        
        extracted_skills: Set[str] = set()
        text = job_description.lower()
        
        # Match against canonical patterns ONLY
        for skill_name, patterns in self.skill_patterns:
            for pattern in patterns:
                try:
                    if re.search(pattern, text, re.IGNORECASE):
                        extracted_skills.add(skill_name)
                        break  # Found match, move to next skill
                except re.error:
                    continue  # Skip invalid patterns
        
        return extracted_skills
    
    def calculate_accuracy(self, 
                          job_description: str, 
                          scraped_skills: str) -> Dict[str, Union[List[str], float]]:
        """Calculate false positive/negative rates"""
        canonical = self.validate_and_extract(job_description)
        scraped = set([s.strip() for s in scraped_skills.split(',') if s.strip()])
        
        true_positives = canonical & scraped
        false_positives = scraped - canonical
        false_negatives = canonical - scraped
        
        precision = len(true_positives) / len(scraped) if scraped else 0
        recall = len(true_positives) / len(canonical) if canonical else 0
        
        return {
            'canonical_skills': list(canonical),
            'true_positives': list(true_positives),
            'false_positives': list(false_positives),
            'false_negatives': list(false_negatives),
            'precision': round(precision, 2),
            'recall': round(recall, 2)
        }
