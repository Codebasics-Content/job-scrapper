#!/usr/bin/env python3
"""
Analyze job descriptions to find skills missing from reference JSON
Cross-checks extracted skills vs actual job description content
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import sqlite3
import json
import re
from collections import Counter
from typing import Any

# Common technical terms to search for
TECH_PATTERNS = [
    # Cloud & Infrastructure
    r'\bAWS\b', r'\bAzure\b', r'\bGCP\b', r'\bKubernetes\b', r'\bDocker\b',
    r'\bTerraform\b', r'\bAnsible\b', r'\bJenkins\b', r'\bCI/CD\b',
    
    # Programming Languages
    r'\bPython\b', r'\bJava\b', r'\bJavaScript\b', r'\bTypeScript\b',
    r'\bC\+\+\b', r'\bGo\b', r'\bRust\b', r'\bScala\b', r'\bR\b',
    
    # AI/ML
    r'\bLLM\b', r'\bGPT\b', r'\bRAG\b', r'\bLangChain\b', r'\bLlamaIndex\b',
    r'\bHugging Face\b', r'\bTransformers\b', r'\bOpenAI\b', r'\bClaude\b',
    
    # Databases
    r'\bPostgreSQL\b', r'\bMySQL\b', r'\bMongoDB\b', r'\bRedis\b',
    r'\bElasticsearch\b', r'\bPinecone\b', r'\bWeaviate\b', r'\bChroma\b',
    
    # Frameworks
    r'\bDjango\b', r'\bFlask\b', r'\bFastAPI\b', r'\bReact\b', r'\bNode\.js\b',
    r'\bPyTorch\b', r'\bTensorFlow\b', r'\bKeras\b', r'\bScikit-learn\b',
]


def analyze_missing_skills(db_path: str, ref_json_path: str) -> None:
    """Find skills in job descriptions not in reference JSON"""
    
    # Load reference skills
    with open(ref_json_path) as f:
        ref_data = json.load(f)
    
    # Extract all skill names and patterns
    all_ref_skills = set()
    all_ref_patterns = set()
    
    for category_skills in ref_data['skills'].values():
        for skill in category_skills:
            all_ref_skills.add(skill['name'].lower())
            for pattern in skill['patterns']:
                all_ref_patterns.add(pattern.lower())
    
    print(f"📚 Loaded {len(all_ref_skills)} skills from reference JSON")
    print(f"📝 Total patterns: {len(all_ref_patterns)}\n")
    
    # Query database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT job_description, skills 
        FROM jobs 
        WHERE job_description IS NOT NULL 
        AND job_description != ''
        LIMIT 100
    """)
    
    jobs = cursor.fetchall()
    conn.close()
    
    print(f"🔍 Analyzing {len(jobs)} job descriptions...\n")
    
    # Find missing skills
    found_terms: dict[str, int] = Counter()
    
    for desc, extracted_skills in jobs:
        desc_lower = desc.lower()
        
        # Search for technical patterns
        for pattern in TECH_PATTERNS:
            matches = re.findall(pattern, desc, re.IGNORECASE)
            for match in matches:
                term = match.lower().strip()
                # Check if NOT in reference
                if (term not in all_ref_patterns and 
                    term not in all_ref_skills):
                    found_terms[match] += 1
    
    # Report findings
    print("="*70)
    print("🚨 Skills Found in Descriptions But NOT in Reference JSON")
    print("="*70)
    
    if found_terms:
        print(f"\n📊 Found {len(found_terms)} missing skills:\n")
        for term, count in found_terms.most_common(30):
            print(f"  • {term:20} → {count:3} occurrences")
    else:
        print("\n✅ All common skills are already in reference JSON!")
    
    print(f"\n{'='*70}\n")


if __name__ == "__main__":
    db_path = "jobs.db"
    ref_path = "skills_reference_2025.json"
    
    analyze_missing_skills(db_path, ref_path)
