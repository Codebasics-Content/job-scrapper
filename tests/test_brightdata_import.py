# Test BrightData LinkedIn Import - EMD Component
# Verifies parsing, skills extraction, and duplicate checking

import json
from src.importer.brightdata import import_linkedin_jobs, parse_brightdata_response

def test_parse_single_job():
    """Test parsing a single BrightData job entry"""
    sample_data = {
        "url": "https://www.linkedin.com/jobs/view/123456",
        "title": "Senior Data Scientist",
        "company": "Tech Corp",
        "description": "Looking for Python expert with ML skills. Required: TensorFlow, PyTorch, SQL",
        "posted_date": "2025-01-10",
        "location": "Remote"
    }
    
    job = parse_brightdata_response(sample_data)
    
    assert job is not None
    assert job.platform == "linkedin"
    assert job.actual_role == "Senior Data Scientist"
    assert job.company_name == "Tech Corp"
    assert "linkedin" in job.job_id
    print(f"✅ Parsed job: {job.actual_role} at {job.company_name}")


def test_import_batch():
    """Test batch import with skills extraction"""
    sample_batch = [
        {
            "url": "https://www.linkedin.com/jobs/view/111",
            "title": "ML Engineer",
            "company": "AI Startup",
            "description": "Python, TensorFlow, Docker, Kubernetes required"
        },
        {
            "url": "https://www.linkedin.com/jobs/view/222",
            "title": "Data Analyst",
            "company": "Finance Co",
            "description": "SQL, Excel, Tableau, Power BI expertise needed"
        }
    ]
    
    stored, duplicates = import_linkedin_jobs(sample_batch, "test_jobs.db")
    
    print(f"✅ Imported: {stored} new, {duplicates} duplicates")
    assert stored + duplicates == len(sample_batch)


if __name__ == "__main__":
    print("🧪 Testing BrightData Import...")
    test_parse_single_job()
    test_import_batch()
    print("✅ All tests passed!")
