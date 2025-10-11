"""Skill extraction validation with false positive/negative detection"""
import json
import re
from pathlib import Path
from collections import defaultdict

import pytest

from src.analysis.skill_extraction.regex_extractor import extract_skills_from_text


SKILLS_REF_PATH = "skills_reference_2025.json"


@pytest.fixture(scope="module")
def skills_database():
    """Load and index skills reference"""
    with open(SKILLS_REF_PATH) as f:
        data = json.load(f)
    
    # Index by normalized name
    skills_index = {}
    pattern_map = {}
    
    for category, skills in data["skills"].items():
        for skill in skills:
            name = skill["name"].lower()
            skills_index[name] = {
                "canonical": skill["name"],
                "category": category,
                "patterns": skill["patterns"]
            }
            
            # Map patterns to canonical name
            for pattern in skill["patterns"]:
                pattern_map[pattern.lower()] = skill["name"]
    
    return {
        "index": skills_index,
        "patterns": pattern_map,
        "total": data["total_skills"]
    }


def test_skill_extraction_accuracy(skills_database):
    """Test skill extraction with known job descriptions"""
    test_cases = [
        {
            "text": "Experience with Python, TensorFlow, PyTorch for ML",
            "expected": ["Python", "TensorFlow", "PyTorch", "Machine Learning"]
        },
        {
            "text": "AWS, Docker, Kubernetes deployment experience",
            "expected": ["AWS", "Docker", "Kubernetes"]
        },
        {
            "text": "React.js, Node.js, TypeScript full-stack dev",
            "expected": ["React", "Node.js", "TypeScript"]
        }
    ]
    
    results = {
        "total_tests": len(test_cases),
        "false_positives": [],
        "false_negatives": [],
        "accuracy": 0.0
    }
    
    for case in test_cases:
        extracted = extract_skills_from_text(case["text"])
        expected_set = set(s.lower() for s in case["expected"])
        extracted_set = set(s.lower() for s in extracted)
        
        # False positives: extracted but not expected
        fp = extracted_set - expected_set
        if fp:
            results["false_positives"].extend(list(fp))
        
        # False negatives: expected but not extracted
        fn = expected_set - extracted_set
        if fn:
            results["false_negatives"].extend(list(fn))
    
    # Calculate accuracy
    total_expected = sum(len(c["expected"]) for c in test_cases)
    total_correct = total_expected - len(results["false_negatives"])
    results["accuracy"] = total_correct / total_expected if total_expected > 0 else 0
    
    print(f"\n{'='*60}")
    print(f"SKILL EXTRACTION VALIDATION REPORT")
    print(f"{'='*60}")
    print(f"Accuracy: {results['accuracy']:.2%}")
    print(f"False Positives: {len(results['false_positives'])}")
    print(f"False Negatives: {len(results['false_negatives'])}")
    
    assert results["accuracy"] >= 0.8, f"Low accuracy: {results['accuracy']}"
