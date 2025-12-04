"""
Context-aware filter to reduce False Positives
Filters out skills that appear in degree/education contexts
"""
from __future__ import annotations

import re
from typing import TypedDict


class ContextMatch(TypedDict):
    """Type for context match result"""
    skill: str
    start: int
    end: int
    is_degree_context: bool


# Patterns that indicate degree/education context (NOT actual skills)
DEGREE_CONTEXT_PATTERNS = [
    # Degree patterns
    r"(?:bachelor'?s?|master'?s?|phd|doctorate|degree|diploma)\s+(?:in|of)\s+",
    r"(?:bs|ba|ms|ma|mba|phd|bsc|msc)\s+(?:in|of)?\s*",
    r"(?:undergraduate|graduate|postgraduate)\s+(?:degree|program|study)\s+(?:in|of)\s+",

    # Education requirement patterns
    r"(?:education|educational)\s*(?:requirement|background|qualification)s?\s*:?\s*",
    r"(?:required|preferred)\s+(?:education|degree)\s*:?\s*",
    r"(?:field|area)\s+of\s+study\s*:?\s*",

    # University/academic patterns
    r"(?:major|minor|concentration)\s+(?:in|of)\s+",
    r"(?:studied|studying|study)\s+",
]

# Compile patterns for efficiency
DEGREE_CONTEXT_REGEX = [re.compile(p, re.IGNORECASE) for p in DEGREE_CONTEXT_PATTERNS]


def is_degree_context(text: str, match_start: int, match_end: int, window: int = 100) -> bool:
    """
    Check if a skill match appears in a degree/education context.

    Args:
        text: Full job description text
        match_start: Start position of the skill match
        match_end: End position of the skill match
        window: Characters to look back for context (default 100)

    Returns:
        True if the skill appears in a degree context (should be filtered)
    """
    # Get context window before the match
    context_start = max(0, match_start - window)
    context_text = text[context_start:match_end].lower()

    # Check if any degree pattern precedes the match
    for pattern in DEGREE_CONTEXT_REGEX:
        if pattern.search(context_text):
            return True

    return False


def filter_degree_contexts(
    text: str,
    skills: list[dict],
    skills_to_check: set[str] | None = None
) -> list[dict]:
    """
    Filter out skills that appear in degree/education contexts.

    Args:
        text: Full job description text
        skills: List of skill dicts with 'skill', 'start', 'end' keys
        skills_to_check: Optional set of skill names to check (default: common FP skills)

    Returns:
        Filtered list of skills with degree contexts removed
    """
    # Skills commonly appearing as false positives in degree contexts
    if skills_to_check is None:
        skills_to_check = {
            'Computer Science',
            'Data Science',
            'Mathematics',
            'Statistics',
            'Information Technology',
            'Computer Engineering',
            'Software Engineering',
            'Electrical Engineering',
            'Physics',
            'Economics',
            'Business Administration',
        }

    filtered_skills = []

    for skill_dict in skills:
        skill_name = skill_dict.get('skill', '')
        start = skill_dict.get('start', 0)
        end = skill_dict.get('end', 0)

        # Only check specific skills for degree context
        if skill_name in skills_to_check:
            if is_degree_context(text, start, end):
                # Skip this skill - it's in a degree context
                continue

        filtered_skills.append(skill_dict)

    return filtered_skills


def get_context_snippet(text: str, start: int, end: int, window: int = 50) -> str:
    """
    Get a context snippet around a match for debugging.

    Args:
        text: Full text
        start: Match start position
        end: Match end position
        window: Characters to show before and after

    Returns:
        Context snippet with match highlighted
    """
    context_start = max(0, start - window)
    context_end = min(len(text), end + window)

    before = text[context_start:start]
    match = text[start:end]
    after = text[end:context_end]

    return f"...{before}[{match}]{after}..."
