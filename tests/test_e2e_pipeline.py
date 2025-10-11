"""End-to-End Pipeline Test: Scraping → Database → Analysis

Tests the complete workflow:
1. Scrape jobs from platform (LinkedIn)
2. Store in SQLite database
3. Extract skills
4. Calculate statistics using formula: (distinct_skills_per_job / total_jobs) * 100
5. Verify all components work correctly
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.db.operations import JobStorageOperations
from src.models import JobModel
from src.analysis.skill_extraction.regex import extract_skills
from src.analysis.skill_statistics import calculate_skill_percentages


def test_full_pipeline():
    """Test complete pipeline: Database → Skills → Analysis"""
    
    print("\n" + "="*60)
    print("🚀 STARTING END-TO-END PIPELINE TEST")
    print("="*60)
    
    # Step 1: Create test data (simulating scraped jobs)
    print("\n[1/5] 📝 Creating test jobs...")
    jobs = [
        {
            'title': 'Data Analyst',
            'company': 'Tech Corp',
            'location': 'India',
            'description': '''We are seeking a highly motivated Data Analyst to join our analytics team. The ideal candidate will have strong proficiency in Python programming for data manipulation and analysis, advanced SQL skills for complex database queries, and expertise in Tableau for creating interactive dashboards and data visualizations. You should be comfortable working with large datasets, performing statistical analysis, and translating business requirements into actionable insights. Experience with Excel for ad-hoc analysis, pandas for data processing, and NumPy for numerical computations is essential. Knowledge of data warehousing concepts and ETL processes would be a plus. This role requires excellent communication skills to present findings to stakeholders.''',
            'platform': 'linkedin'
        },
        {
            'title': 'Senior Data Analyst',
            'company': 'Data Inc',
            'location': 'India',
            'description': '''Looking for an experienced Senior Data Analyst with 5+ years of hands-on experience in data analysis and business intelligence. Must have expert-level proficiency in Python (pandas, scikit-learn), SQL (complex queries, stored procedures, optimization), and Power BI for enterprise-level reporting solutions. The role involves leading analytics projects, mentoring junior analysts, and collaborating with cross-functional teams. Strong understanding of machine learning concepts, predictive modeling, and statistical analysis is highly valued. Experience with Apache Spark for big data processing, AWS or Azure cloud platforms, and Git for version control would be advantageous. Excellent problem-solving skills and ability to work in fast-paced environments are must-haves.''',
            'platform': 'linkedin'
        },
        {
            'title': 'Business Analyst',
            'company': 'Business Solutions',
            'location': 'India',
            'description': '''We are hiring a Business Analyst to bridge the gap between business stakeholders and technical teams. The successful candidate will have strong SQL skills for data extraction and analysis, advanced Excel proficiency including VBA macros and pivot tables, and experience with Tableau for building comprehensive business dashboards. Python knowledge is preferred for automation and advanced analytics. Your responsibilities will include gathering business requirements, conducting gap analysis, creating process flow diagrams, and documenting technical specifications. Experience in agile methodologies, JIRA for project tracking, and stakeholder management is important. Strong analytical thinking, attention to detail, and excellent communication skills are essential for success in this role.''',
            'platform': 'linkedin'
        },
        {
            'title': 'Data Scientist',
            'company': 'AI Labs',
            'location': 'India',
            'description': '''Exciting opportunity for a Data Scientist to work on cutting-edge machine learning and deep learning projects. Required skills include advanced Python programming with extensive experience in TensorFlow, PyTorch, and scikit-learn for building and deploying ML models. Strong foundation in mathematics, statistics, and probability theory is essential. You should be proficient in deep learning architectures including CNNs, RNNs, and transformers. Experience with natural language processing, computer vision, and time series forecasting is highly desirable. Knowledge of MLOps practices, Docker for containerization, and cloud platforms (AWS SageMaker, Google Cloud AI) for model deployment is important. SQL for data querying and pandas for data preprocessing are must-have skills. PhD or Master's degree in Computer Science, Statistics, or related field preferred.''',
            'platform': 'linkedin'
        },
        {
            'title': 'Junior Analyst',
            'company': 'Startup Co',
            'location': 'India',
            'description': '''Entry-level position for a Junior Analyst to join our growing data team. This role is perfect for recent graduates or professionals with 1-2 years of experience looking to build their career in data analytics. Strong Excel skills are mandatory including VLOOKUP, pivot tables, and basic formulas. SQL proficiency for writing SELECT queries and joining tables is required. Python knowledge is a nice-to-have and will be advantageous for automation tasks. You will work closely with senior team members to learn data extraction, cleaning, and basic statistical analysis. The role involves creating reports, maintaining databases, and supporting ad-hoc analysis requests. We value curiosity, attention to detail, and willingness to learn new tools and technologies. This is an excellent opportunity to grow your analytical skills in a supportive environment.''',
            'platform': 'linkedin'
        }
    ]
    
    print(f"✅ Created {len(jobs)} test jobs")
    
    # Step 2: Extract skills for each job
    print("\n[2/5] 🔍 Extracting skills from job descriptions...")
    jobs_with_skills = []
    
    for job in jobs:
        description = f"{job.get('title', '')} {job.get('description', '')}"
        skills = extract_skills(description)
        job['skills'] = ', '.join(skills) if skills else ''
        jobs_with_skills.append(job)
        print(f"  - {job.get('title', 'Unknown')}: {len(skills)} skills")
    
    # Step 3: Save to database
    print("\n[3/5] 💾 Saving jobs to database...")
    db_storage = JobStorageOperations("test_jobs.db")
    
    # Convert dict jobs to JobModel (using aliases for Pydantic fields)
    job_models = []
    for job in jobs_with_skills:
        job_model = JobModel(
            job_id=f"{job['platform']}_{job['company']}_{job['title']}".replace(' ', '_'),
            Job_Role=job['title'],
            Company=job['company'],
            Experience="Not specified",  # Required field
            Skills=job.get('skills', ''),
            jd=job.get('description', ''),
            platform=job['platform'],
            location=job.get('location', '')
        )
        job_models.append(job_model)
    
    save_result = db_storage.store_jobs(job_models)
    print(f"✅ Saved {save_result} jobs to database")
    
    # Step 4: Retrieve from database
    print("\n[4/5] 📊 Retrieving jobs from database...")
    # Get all jobs by querying with empty role
    db_jobs_dicts = db_storage.get_jobs_by_role("")
    
    # Convert dict results to JobModel for analysis
    db_jobs = []
    for job_dict in db_jobs_dicts[:10]:  # Limit to 10
        job_model = JobModel(
            job_id=str(job_dict.get('job_id', '')),
            Job_Role=str(job_dict.get('job_role', '')),
            Company=str(job_dict.get('company', '')),
            Experience=str(job_dict.get('experience', 'Not specified')),
            Skills=str(job_dict.get('skills', '')),
            jd=str(job_dict.get('jd', '')),
            platform=str(job_dict.get('platform', '')),
            location=str(job_dict.get('location', ''))
        )
        db_jobs.append(job_model)
    
    print(f"✅ Retrieved {len(db_jobs)} jobs from database")
    
    # Step 5: Calculate skill statistics
    print("\n[5/5] 📈 Calculating skill statistics...")
    print("\nFormula: (Distinct jobs with skill / Total jobs) * 100")
    
    percentages = calculate_skill_percentages(db_jobs)
    
    # Manual verification
    total_jobs = len(db_jobs)
    skill_counts = {}
    
    for job in db_jobs:
        if hasattr(job, 'skills') and job.skills:
            job_skills = [s.strip().lower() for s in job.skills.split(',') if s.strip()]
            for skill in job_skills:
                skill_counts[skill] = skill_counts.get(skill, 0) + 1
    
    print(f"\n📊 Analysis Results (from {total_jobs} jobs):")
    print("-" * 60)
    
    # Show top 10 skills
    sorted_skills = sorted(percentages.items(), key=lambda x: x[1], reverse=True)[:10]
    
    for skill, percentage in sorted_skills:
        count = skill_counts.get(skill.lower(), 0)
        expected = (count / total_jobs) * 100
        match = "✅" if abs(percentage - expected) < 0.01 else "❌"
        
        print(f"{match} {skill:20s} | {percentage:6.2f}% | "
              f"({count}/{total_jobs} jobs) | Expected: {expected:.2f}%")
    
    # Verification
    print("\n" + "="*60)
    print("🔍 VERIFICATION")
    print("="*60)
    
    all_correct = True
    for skill, percentage in percentages.items():
        count = skill_counts.get(skill.lower(), 0)
        expected = (count / total_jobs) * 100
        
        if abs(percentage - expected) > 0.01:
            print(f"❌ MISMATCH: {skill} - Got {percentage}%, Expected {expected}%")
            all_correct = False
    
    if all_correct:
        print("✅ All calculations verified correctly!")
        print(f"✅ Formula working: (distinct_jobs_with_skill / {total_jobs}) * 100")
    else:
        print("❌ Some calculations don't match expected values")
    
    print("\n" + "="*60)
    print("✅ END-TO-END PIPELINE TEST COMPLETE")
    print("="*60 + "\n")
    
    return all_correct


if __name__ == "__main__":
    result = test_full_pipeline()
    sys.exit(0 if result else 1)
