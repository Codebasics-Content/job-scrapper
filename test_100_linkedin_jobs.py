#!/usr/bin/env python3
"""Load CSV, re-extract skills with comprehensive reference, store to SQLite"""
import pandas as pd
from src.analysis.skill_extraction.regex_extractor import extract_skills_from_text
from src.analysis.skill_extraction.regex.pattern_loader import load_skill_patterns
from src.db.operations import JobStorageOperations
from src.models import JobDetailModel, JobUrlModel

def main():
    print("=" * 70)
    print("LinkedIn Jobs: Re-extract Skills + Store to SQLite")
    print("=" * 70)
    
    # Load CSV
    csv_file = "linkedin_100_jobs_20251012_191110.csv"
    print(f"\n📂 Loading {csv_file}...")
    df = pd.read_csv(csv_file)
    print(f"✅ Loaded {len(df)} jobs")
    
    # Load comprehensive skill patterns (850 skills)
    print("\n🔧 Loading comprehensive skill patterns (850 skills)...")
    skill_patterns = load_skill_patterns()
    print(f"✅ Loaded {len(skill_patterns)} skill patterns")
    
    # Re-extract skills
    print("\n🔍 Re-extracting skills with comprehensive patterns...")
    old_skills = df['skills'].str.split(', ').apply(lambda x: set(x) if isinstance(x, list) else set())
    new_skills = df['description'].apply(lambda desc: extract_skills_from_text(str(desc), skill_patterns))
    
    # Create JobDetailModel objects
    print("\n💾 Creating job models...")
    job_details = []
    for idx, row in df.iterrows():
        skills_list = new_skills.iloc[idx]
        posted_date = row['date_posted'] if pd.notna(row['date_posted']) else None
        job_details.append(JobDetailModel(
            job_id=JobUrlModel.generate_job_id("linkedin", row['job_url']),
            platform="linkedin",
            actual_role=row['title'],
            url=row['job_url'],
            job_description=str(row['description'])[:5000],
            skills=", ".join(skills_list),
            company_name=row['company'],
            company_detail="",
            posted_date=posted_date
        ))
    
    # Store to SQLite
    print(f"\n💾 Storing {len(job_details)} jobs to SQLite...")
    db_ops = JobStorageOperations()
    stored = db_ops.store_details(job_details)
    print(f"✅ Stored {stored} jobs to database")
    
    # Comparison
    improvements = sum(1 for old, new in zip(old_skills, new_skills) if len(new) > len(old))
    print("\n" + "=" * 70)
    print("📊 RESULTS")
    print("=" * 70)
    print(f"Jobs with improved extraction: {improvements}/{len(df)}")
    print(f"Avg skills (old): {old_skills.apply(len).mean():.1f}")
    print(f"Avg skills (new): {pd.Series(new_skills).apply(len).mean():.1f}")
    
    # Sample comparison
    sample_idx = new_skills.apply(len).idxmax()
    print(f"\n📋 Best example (Job {sample_idx}):")
    print(f"   Title: {df.iloc[sample_idx]['title']}")
    print(f"   Old: {len(old_skills.iloc[sample_idx])} skills")
    print(f"   New: {len(new_skills[sample_idx])} skills")
    print(f"   Skills: {', '.join(new_skills[sample_idx][:10])}...")

if __name__ == "__main__":
    main()
