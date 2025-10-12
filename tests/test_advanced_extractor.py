"""
Test advanced regex skill extractor on sample jobs
Validates 80%+ accuracy target
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analysis.skill_extraction.extractor import extract_skills_advanced
from src.db.connection import DatabaseConnection


def test_extractor_on_sample_jobs(limit: int = 10) -> None:
    """Test advanced extractor on sample jobs from database"""
    db = DatabaseConnection("jobs.db")
    with db.get_connection_context() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT job_id, actual_role, job_description, skills
            FROM jobs 
            WHERE job_description IS NOT NULL 
            AND job_description != ''
            LIMIT ?
        """, (limit,))
        jobs = cursor.fetchall()
    
    print(f"\n{'='*80}")
    print(f"TESTING ADVANCED REGEX EXTRACTOR ON {len(jobs)} SAMPLE JOBS")
    print(f"{'='*80}\n")
    
    total_accuracy = 0
    results = []
    
    for job_id, actual_role, job_description, stored_skills in jobs:
        extracted = extract_skills_advanced(job_description, "skills_reference_2025.json")
        stored = [s.strip() for s in stored_skills.split(',')] if stored_skills else []
        
        # Normalize to lowercase for case-insensitive comparison
        extracted_lower = {s.lower() for s in extracted}
        stored_lower = {s.lower() for s in stored}
        
        if stored:
            matched = len(extracted_lower & stored_lower)
            accuracy = (matched / len(stored)) * 100
        else:
            accuracy = 100 if extracted else 0
        
        total_accuracy += accuracy
        results.append({
            'job_id': job_id,
            'role': actual_role[:50],
            'stored_count': len(stored),
            'extracted_count': len(extracted),
            'matched': matched,
            'accuracy': accuracy,
            'extracted': extracted[:10]
        })
    
    for idx, r in enumerate(results):
        print(f"Job: {r['role']}")
        print(f"  Stored: {r['stored_count']} | Extracted: {r['extracted_count']} | Matched: {r['matched']}")
        print(f"  Accuracy: {r['accuracy']:.1f}%")
        print(f"  Sample: {', '.join(r['extracted'])}")
        if idx == 0:
            job_id, actual_role, job_description, stored_skills_str = jobs[0]
            stored_list = [s.strip() for s in stored_skills_str.split(',')] if stored_skills_str else []
            extracted_list = results[0]['extracted']
            stored_lower = {s.lower() for s in stored_list}
            extracted_lower = {s.lower() for s in extracted_list}
            print(f"  DETAILED: Stored={stored_list}")
            print(f"  DETAILED: Only in Stored={sorted(stored_lower - extracted_lower)}")
            print(f"  DETAILED: Only in Extracted={sorted(list(extracted_lower - stored_lower)[:10])}")
        print()
    
    avg_accuracy = total_accuracy / len(jobs)
    print(f"{'='*80}")
    print(f"AVERAGE ACCURACY: {avg_accuracy:.1f}%")
    print(f"TARGET: 80%+")
    print(f"STATUS: {'✅ PASS' if avg_accuracy >= 80 else '❌ FAIL'}")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    test_extractor_on_sample_jobs(10)
