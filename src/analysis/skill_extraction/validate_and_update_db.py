# Autonomous 5-Batch Skill Validation & DB Update (EMD ≤80 lines)
# Processes LinkedIn jobs, validates against 557 canonical skills, updates DB

import sqlite3
import json
from pathlib import Path
from typing import Dict, List
from .skill_validator import SkillValidator

def validate_linkedin_jobs_batch(
    db_path: str,
    reference_path: str,
    batch_size: int = 5,
    num_batches: int = 5
) -> Dict[str, any]:
    """Process 5 batches of LinkedIn jobs with RL tracking"""
    
    validator = SkillValidator(reference_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    metrics = {
        'batches_processed': 0,
        'jobs_updated': 0,
        'total_precision': 0.0,
        'total_recall': 0.0,
        'false_positives_eliminated': 0,
        'false_negatives_recovered': 0
    }
    
    for batch_idx in range(num_batches):
        offset = batch_idx * batch_size
        
        # Fetch batch
        cursor.execute("""
            SELECT job_id, job_description, skills 
            FROM jobs 
            WHERE platform='linkedin' 
            LIMIT ? OFFSET ?
        """, (batch_size, offset))
        
        jobs = cursor.fetchall()
        if not jobs:
            break
            
        for job_id, description, old_skills in jobs:
            # Validate and extract canonical skills
            accuracy = validator.calculate_accuracy(description, old_skills or '')
            new_skills = ','.join(accuracy['canonical_skills'])
            
            # Update database
            cursor.execute(
                "UPDATE jobs SET skills = ? WHERE job_id = ?",
                (new_skills, job_id)
            )
            
            # Track metrics
            metrics['jobs_updated'] += 1
            metrics['total_precision'] += accuracy['precision']
            metrics['total_recall'] += accuracy['recall']
            metrics['false_positives_eliminated'] += len(accuracy['false_positives'])
            metrics['false_negatives_recovered'] += len(accuracy['false_negatives'])
        
        conn.commit()
        metrics['batches_processed'] += 1
    
    conn.close()
    
    # Calculate averages
    if metrics['jobs_updated'] > 0:
        metrics['avg_precision'] = round(metrics['total_precision'] / metrics['jobs_updated'], 2)
        metrics['avg_recall'] = round(metrics['total_recall'] / metrics['jobs_updated'], 2)
    
    return metrics
