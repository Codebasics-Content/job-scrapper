# Universal skill extraction - cross-platform reusable
# EMD Compliance: ≤80 lines

import re
import logging

logger = logging.getLogger(__name__)

def extract_skills_from_description(description_text: str) -> list[str]:
    """Extract skills using consolidated pattern matching"""
    
    skills = set()
    text_lower = description_text.lower()
    
    # Core skill patterns for data science roles
    skill_patterns = [
        r'\b(python|sql|excel|tableau|power bi|machine learning|ai)\b',
        r'\b(pandas|numpy|scikit-learn|tensorflow|pytorch)\b',
        r'\b(data analysis|analytics|statistics|business intelligence)\b',
        r'\b(aws|azure|docker|git|jupyter)\b'
    ]
    
    # Extract predefined skills
    for pattern in skill_patterns:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        skills.update(matches)
    
    # Try dynamic extraction if available
    try:
        from .dynamic_skill_extractor import extract_dynamic_skills, clean_and_validate_skills
        dynamic_skills = extract_dynamic_skills(description_text)
        validated_skills = clean_and_validate_skills(dynamic_skills)
        skills.update(validated_skills)
    except ImportError:
        logger.warning("Dynamic skill extractor not available")
    
    # Clean and return unique skills
    unique_skills = [skill for skill in skills if skill and len(skill.strip()) > 1]
    logger.debug(f"Extracted {len(unique_skills)} skills: {unique_skills}")
    
    return unique_skills

def get_job_description_from_card(card_element) -> str:
    """Extract job description text from a WebElement card"""
    try:
        # Try common job description selectors
        selectors = [
            ".job-search-card__snippet",
            ".base-search-card__summary", 
            "[data-test='job-snippet']",
            ".job-description",
            ".description"
        ]
        
        for selector in selectors:
            elements = card_element.find_elements("css selector", selector)
            if elements:
                return elements[0].text.strip()
        
        # Fallback to card text if no specific description found
        return card_element.text[:500]  # Limit to 500 chars
    except Exception:
        return ""


def format_skills_as_string(skills: list[str], job_role: str) -> str:
    """Format extracted skills into a comma-separated string"""
    if not skills:
        return f"Job for {job_role}"
    
    # Limit to top 10 skills and capitalize them
    formatted_skills = [skill.capitalize() for skill in skills[:10]]
    skills_str = ", ".join(formatted_skills)
    
    return f"{skills_str} - Job for {job_role}"
