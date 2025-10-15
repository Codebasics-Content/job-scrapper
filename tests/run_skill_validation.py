#!/usr/bin/env python3
"""
Autonomous Skill Validation Runner - 5 Batches with RL Tracking
Validates LinkedIn jobs against 557 canonical skills and updates DB
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from analysis.skill_extraction.validate_and_update_db import validate_linkedin_jobs_batch

def main() -> None:
    """Execute 5-batch validation with RL tracking"""
    
    db_path = 'jobs.db'
    reference_path = 'skills_reference_2025.json'
    
    print("🚀 Starting Autonomous Skill Validation...")
    print(f"📊 Target: 5 batches × 5 jobs = 25 LinkedIn jobs")
    print(f"✅ Reference: 557 canonical skills\n")
    
    # Execute autonomous validation
    metrics = validate_linkedin_jobs_batch(
        db_path=db_path,
        reference_path=reference_path,
        batch_size=5,
        num_batches=5
    )
    
    # Report results
    print("\n" + "="*60)
    print("📈 VALIDATION COMPLETE - RL METRICS")
    print("="*60)
    print(f"✅ Batches Processed: {metrics['batches_processed']}")
    print(f"✅ Jobs Updated: {metrics['jobs_updated']}")
    print(f"📊 Average Precision: {metrics['avg_precision']:.0%}")
    print(f"📊 Average Recall: {metrics['avg_recall']:.0%}")
    print(f"❌ False Positives Eliminated: {metrics['false_positives_eliminated']}")
    print(f"✅ False Negatives Recovered: {metrics['false_negatives_recovered']}")
    print("="*60)
    
    # RL Reward Calculation
    rl_reward = 0
    rl_reward += metrics['batches_processed'] * 5  # +5 per batch
    rl_reward += int(metrics['avg_precision'] * 20)  # Up to +20 for precision
    rl_reward += int(metrics['avg_recall'] * 20)  # Up to +20 for recall
    
    print(f"\n🎯 RL REWARD: +{rl_reward} RL")
    print(f"   • Batch completion: +{metrics['batches_processed'] * 5} RL")
    print(f"   • Precision bonus: +{int(metrics['avg_precision'] * 20)} RL")
    print(f"   • Recall bonus: +{int(metrics['avg_recall'] * 20)} RL")
    print("="*60)

if __name__ == '__main__':
    main()
