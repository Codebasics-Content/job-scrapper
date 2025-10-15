"""
Skill normalization and synonym handling
"""
from typing import Any


# Synonym mapping (canonical -> variants)
SKILL_SYNONYMS = {
    "Machine Learning": ["machine learning", "ml", "ml engineering"],
    "Natural Language Processing": ["natural language processing", "nlp"],
    "MLOps": ["mlops", "ml ops", "machine learning operations"],
    "CI/CD": ["ci/cd", "ci-cd", "cicd", "continuous integration", "continuous deployment"],
    "Deep Learning": ["deep learning", "dl"],
    "RAG": ["rag", "retrieval augmented generation"],
    "LLM": ["llm", "large language model", "large language models"],
    "GenAI": ["genai", "gen ai", "generative ai"],
}


def normalize_skill(skill: str) -> str:
    """
    Map skill variant to canonical form
    Returns title-cased original if no synonym found
    """
    skill_lower = skill.lower().strip()
    
    # Check all synonym groups
    for canonical, variants in SKILL_SYNONYMS.items():
        if skill_lower in variants:
            return canonical
    
    # Return title-cased original
    return skill.title()


def deduplicate_skills(skills: list[dict[str, Any]]) -> list[str]:
    """
    Extract skill names, normalize, and deduplicate
    Handles overlapping patterns (e.g., CI/CD contains CI and CD)
    """
    skill_names = [s['skill'] for s in skills]
    normalized = [normalize_skill(name) for name in skill_names]
    
    # Deduplicate while preserving order
    seen = set()
    unique_skills = []
    for skill in normalized:
        if skill.lower() not in seen:
            seen.add(skill.lower())
            unique_skills.append(skill)
    
    # Remove overlapping duplicates: if "CI/CD" present, remove "CI", "Ci", "CD", "Cd"
    if 'CI/CD' in unique_skills:
        unique_skills = [s for s in unique_skills if s.upper() not in ['CI', 'CD']]
    
    return unique_skills
