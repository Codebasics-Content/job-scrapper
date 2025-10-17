# Autonomous 5-Batch Skill Validation & DB Update (EMD ≤80 lines)
# Processes LinkedIn jobs, validates against 557 canonical skills, updates DB

import sqlite3
from typing import Dict, Union
from .skill_validator import SkillValidator

def validate_linkedin_jobs_batch(
    db_path: str,
    reference_path: str,
    batch_size: int = 5,
    num_batches: int = 5
) -> Dict[str, Union[int, float]]:
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
            canonical_skills_list = accuracy['canonical_skills']
            if isinstance(canonical_skills_list, list):
                new_skills = ','.join(canonical_skills_list)
            else:
                new_skills = ''
            
            # Update database
            cursor.execute(
                "UPDATE jobs SET skills = ? WHERE job_id = ?",
                (new_skills, job_id)
            )
            
            # Track metrics
            metrics['jobs_updated'] += 1
            precision = accuracy['precision']
            recall = accuracy['recall']
            false_pos = accuracy['false_positives']
            false_neg = accuracy['false_negatives']
            
            if isinstance(precision, (int, float)):
                metrics['total_precision'] += float(precision)
            if isinstance(recall, (int, float)):
                metrics['total_recall'] += float(recall)
            if isinstance(false_pos, list):
                metrics['false_positives_eliminated'] += len(false_pos)
            if isinstance(false_neg, list):
                metrics['false_negatives_recovered'] += len(false_neg)
        
        conn.commit()
        metrics['batches_processed'] += 1
    
    conn.close()
    
    # Calculate averages
    if metrics['jobs_updated'] > 0:
        metrics['avg_precision'] = round(metrics['total_precision'] / metrics['jobs_updated'], 2)
        metrics['avg_recall'] = round(metrics['total_recall'] / metrics['jobs_updated'], 2)
    
    return metrics
