#!/usr/bin/env python3
"""
Deep analysis: Find ALL missing skills in job descriptions
Searches for 200+ technical terms across multiple categories
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import sqlite3
import json
import re
from collections import Counter
from typing import Any

# Comprehensive technical term patterns
SEARCH_PATTERNS = {
    'llm_genai': [
        r'\bLLM\b', r'\bLLMs\b', r'\bGPT\b', r'\bRAG\b', r'\bLangChain\b',
        r'\bLlamaIndex\b', r'\bLlama\b', r'\bMistral\b', r'\bClaude\b',
        r'\bGemini\b', r'\bGrok\b', r'\bBard\b', r'\bPaLM\b',
        r'\bPrompt Engineering\b', r'\bFine-tuning\b', r'\bLORA\b',
        r'\bQuantization\b', r'\bVLLM\b', r'\bOllama\b',
    ],
    'vector_db': [
        r'\bPinecone\b', r'\bWeaviate\b', r'\bChroma\b', r'\bQdrant\b',
        r'\bMilvus\b', r'\bFAISS\b', r'\bAnnoy\b', r'\bPgvector\b',
    ],
    'mlops': [
        r'\bMLOps\b', r'\bMLflow\b', r'\bKubeflow\b', r'\bWandB\b',
        r'\bDVC\b', r'\bBentoML\b', r'\bSeldon\b', r'\bKServe\b',
    ],
    'cicd': [
        r'\bCI/CD\b', r'\bCI-CD\b', r'\bJenkins\b', r'\bGitHub Actions\b',
        r'\bGitLab CI\b', r'\bCircleCI\b', r'\bTravis CI\b',
    ],
    'observability': [
        r'\bPrometheus\b', r'\bGrafana\b', r'\bDatadog\b', r'\bNew Relic\b',
        r'\bSplunk\b', r'\bELK\b', r'\bLoki\b', r'\bTempo\b',
    ]
}


def deep_analyze(db_path: str, ref_path: str) -> None:
    """Comprehensive missing skills analysis"""
    
    # Load reference
    with open(ref_path) as f:
        ref_data = json.load(f)
    
    all_ref_patterns = set()
    for category_skills in ref_data['skills'].values():
        for skill in category_skills:
            for pattern in skill['patterns']:
                all_ref_patterns.add(pattern.lower())
    
    print(f"📚 Reference: {len(all_ref_patterns)} patterns\n")
    
    # Query DB
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT job_description FROM jobs 
        WHERE job_description IS NOT NULL 
        AND job_description != ''
        LIMIT 200
    """)
    descriptions = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    print(f"🔍 Analyzing {len(descriptions)} descriptions\n")
    
    # Find missing
    missing: dict[str, dict[str, int]] = {}
    
    for category, patterns in SEARCH_PATTERNS.items():
        missing[category] = Counter()
        for desc in descriptions:
            for pattern in patterns:
                matches = re.findall(pattern, desc, re.IGNORECASE)
                for match in matches:
                    term = match.strip()
                    # Check if NOT in reference
                    if term.lower() not in all_ref_patterns:
                        missing[category][term] += 1
    
    # Report
    print("="*70)
    print("🚨 MISSING SKILLS BY CATEGORY")
    print("="*70)
    
    total_missing = 0
    for category, terms in missing.items():
        if terms:
            print(f"\n📁 {category.upper().replace('_', ' ')}")
            print("-"*70)
            for term, count in terms.most_common(10):
                print(f"  • {term:25} → {count:3} occurrences")
                total_missing += 1
    
    print(f"\n{'='*70}")
    print(f"📊 Total unique missing skills: {total_missing}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    deep_analyze("jobs.db", "skills_reference_2025.json")
