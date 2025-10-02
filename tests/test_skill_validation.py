#!/usr/bin/env python3
# Quick test for skill validation functionality

from src.scraper.base.skill_validator import (
    validate_skill_in_text,
    filter_boilerplate_skills,
    validate_extracted_skills
)

# Test 1: Skill exists in text
job_description = """
We are looking for a Python developer with experience in Django and React.
Must have strong skills in JavaScript and PostgreSQL.
"""

print("Test 1: Validate skills that exist in JD")
print(f"Python in text: {validate_skill_in_text('python', job_description)}")
print(f"Django in text: {validate_skill_in_text('django', job_description)}")
print(f"JavaScript in text: {validate_skill_in_text('javascript', job_description)}")
print(f"Ruby in text (should be False): {validate_skill_in_text('ruby', job_description)}")

# Test 2: Filter boilerplate
print("\nTest 2: Filter boilerplate skills")
skills_with_boilerplate = ['python', 'work', 'team', 'javascript', 'experience']
filtered = filter_boilerplate_skills(skills_with_boilerplate)
print(f"Before: {skills_with_boilerplate}")
print(f"After: {filtered}")

# Test 3: Full validation
print("\nTest 3: Full validation (skills that don't exist should be rejected)")
extracted_skills = ['python', 'django', 'ruby', 'java', 'react', 'work', 'team']
validated = validate_extracted_skills(extracted_skills, job_description)
print(f"Extracted: {extracted_skills}")
print(f"Validated: {validated}")
print(f"\nRejected: {set(extracted_skills) - set(validated)}")
