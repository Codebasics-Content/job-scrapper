# Analysis Module

## Purpose
Extracts and validates technical skills from job descriptions using intelligent pattern matching.

## What It Does
- **Identifies Skills**: Scans job descriptions to find technical skills (Python, React, AWS, etc.)
- **Validates Accuracy**: Matches found skills against 749 canonical skills to prevent false positives
- **Batch Processing**: Processes multiple jobs efficiently for faster analysis
- **Quality Assurance**: Filters generic terms like "work" and "team" that aren't real skills

## Why It Matters
Without accurate skill extraction, the analytics would show meaningless data. This module ensures every skill counted is a real, industry-recognized technical requirement.

## Key Component
- `skill_validator.py` - Core validation engine using regex patterns
- `batch_processor.py` - Handles multiple job analysis efficiently
