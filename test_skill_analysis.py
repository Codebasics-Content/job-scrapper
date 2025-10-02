#!/usr/bin/env python3
"""Test skill analysis with actual database"""
import sys
from src.db import JobStorageOperations
from src.analysis.skill_normalizer import normalize_jobs_skills
from src.analysis.analysis.visualization import generate_skill_leaderboard

def test_skill_analysis():
    """Test skill normalization and leaderboard generation"""
    print("=== Testing Skill Analysis ===\n")
    
    # Get jobs from database
    db_ops = JobStorageOperations("jobs.db")
    jobs = db_ops.get_jobs_by_role("")
    print(f"✓ Loaded {len(jobs)} jobs from database\n")
    
    # Test normalization
    print("Testing skill normalization...")
    if jobs:
        sample_job = jobs[0]
        print(f"Sample job skills (raw): {str(sample_job.get('skills', ''))[:100]}...")
    
    normalized_jobs = normalize_jobs_skills(jobs)
    print(f"✓ Normalized {len(normalized_jobs)} jobs\n")
    
    if normalized_jobs:
        sample_normalized = normalized_jobs[0]
        normalized_skills = sample_normalized.get('normalized_skills', [])
        print(f"Sample normalized skills (first 10): {normalized_skills[:10]}\n")
    
    # Generate leaderboard
    print("Generating skill leaderboard...")
    leaderboard = generate_skill_leaderboard(normalized_jobs, top_n=20)
    
    if leaderboard:
        print(f"✓ Generated leaderboard with {len(leaderboard)} skills\n")
        print("Top 20 Skills Analysis:")
        print("-" * 60)
        for i, skill_data in enumerate(leaderboard, 1):
            skill = skill_data['skill']
            count = skill_data['count']
            percentage = skill_data['percentage']
            print(f"{i:2d}. {skill:30s} | Count: {count:3d} | {percentage:5.1f}%")
        
        total_jobs = len(normalized_jobs)
        print("-" * 60)
        print(f"\nTotal jobs analyzed: {total_jobs}")
        print(f"Formula: (Distinct jobs with skill / Total jobs) × 100")
        print(f"\nExample: '{leaderboard[0]['skill']}' appears in {leaderboard[0]['count']} jobs")
        print(f"Percentage: ({leaderboard[0]['count']} / {total_jobs}) × 100 = {leaderboard[0]['percentage']}%")
    else:
        print("❌ No skills found in leaderboard")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_skill_analysis()
