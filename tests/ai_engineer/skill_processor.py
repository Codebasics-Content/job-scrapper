"""Skills extraction and database storage for AI Engineer jobs"""
import pandas as pd
from src.analysis.skill_extraction.regex_extractor import extract_skills_from_text
from src.analysis.skill_extraction.regex.pattern_loader import load_skill_patterns
from src.db.operations import JobStorageOperations
from src.models import JobDetailModel, JobUrlModel


def extract_and_store_skills(df: pd.DataFrame) -> int:
    """Extract skills and store to database"""
    # Load patterns
    print("\n🔧 Loading 943 skill patterns...")
    skill_patterns = load_skill_patterns()
    print(f"✅ Loaded {len(skill_patterns)} patterns\n")
    
    # Extract skills
    print(f"🔍 Extracting skills from {len(df)} jobs...")
    df['extracted_skills'] = df['description'].apply(
        lambda desc: extract_skills_from_text(str(desc), skill_patterns)
    )
    
    # Store to database
    print(f"\n💾 Storing to jobs.db...")
    db_ops = JobStorageOperations()
    job_models = []
    
    for idx, row in df.iterrows():
        posted_date = row.get('date_posted') if pd.notna(row.get('date_posted')) else None
        
        job_models.append(JobDetailModel(
            job_id=JobUrlModel.generate_job_id("linkedin", row['job_url']),
            platform="linkedin",
            actual_role=row['title'],
            url=row['job_url'],
            job_description=str(row['description'])[:5000],
            skills=", ".join(row['extracted_skills']),
            company_name=row['company'],
            company_detail="",
            posted_date=posted_date
        ))
    
    stored = db_ops.store_details(job_models)
    print(f"✅ Stored {stored} jobs to database")
    
    return stored
