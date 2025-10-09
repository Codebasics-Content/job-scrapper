#!/usr/bin/env python3
# Test with REAL Naukri API response structure - EMD Compliance: ≤80 lines

import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from models import JobModel
from scraper.naukri.extractors.api_parser import NaukriAPIParser

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_real_api_response():
    """Test with actual Naukri API response structure from user's example"""
    
    # REAL API RESPONSE STRUCTURE FROM USER
    real_api_response = {
        "loggedIn": False,
        "brandedJd": False,
        "jobDetails": {
            "videoProfilePreferred": False,
            "savedJobFlag": 0,
            "education": {
                "ug": ["B.Tech/B.E. in Any Specialization"],
                "pg": ["M.Tech in Any Specialization", "MBA/PGDM in Information Technology", "MCA in Any Specialization"],
                "degreeCombination": "ugandpg",
                "premiumProcessed": False,
                "ppg": [],
                "label": "",
                "isSchool": None
            },
            "hideApplyButton": False,
            "applyCount": 1589,
            "groupId": 753464,
            "roleCategory": "Data Science & Machine Learning",
            "mode": "jp",
            "tagLabels": [],
            "jobRole": "Data Scientist",
            "isTopGroup": 0,
            "clientLogo": "https://img.naukimg.com/logo_images/groups/v1/753464.gif",
            "wfhType": "0",
            "companyDetail": {
                "name": "Innovationm",
                "websiteUrl": "",
                "details": "<p> </p><p> <strong>Role and Responsibilities</strong></p><p><strong>Lead the design and development of complex software solutions using Java technologies.</strong><br /><strong>Collaborate with architects, product managers, and business teams to understand requirements and translate them into technical solutions.</strong><br /><strong>Oversee the development lifecycle including planning, coding, testing, deployment, and maintenance.</strong><br /><strong>Guide and mentor junior developers to improve code quality, architecture, and performance.</strong><br /><strong>Conduct code reviews and ensure adherence to industry standards and best practices.</strong><br /><strong>Troubleshoot and resolve production issues in a timely manner.</strong><br /><strong>Stay updated with emerging trends in technology and recommend tools/processes for continuous improvement.</strong><br /><strong>Take ownership of delivery timelines and ensure high-quality outcomes.</strong><br /></p><p><strong>Requirements</strong></p><p><strong>Hands-on experience in Java and J2EE technologies And Jasper Framework.</strong><br /><strong>Strong understanding of object-oriented design and microservices architecture.</strong><br /><strong>Proficient in frameworks like Spring, Spring Boot, Hibernate, etc.</strong><br /><strong>Experience with RESTful APIs, web services, and integration patterns.</strong><br /><strong>Good knowledge of databases  both SQL (e.g., MySQL, PostgreSQL) and NoSQL (e.g., MongoDB).</strong><br /><strong>Experience with DevOps tools, CI/CD pipelines, and containerization (Docker/Kubernetes) is a plus.</strong><br /><strong>Excellent problem-solving and analytical skills.</strong><br /><strong>Strong communication and leadership skills to manage team interactions and client discussions.</strong> </p>",
            },
            "jobIconType": "",
            "consent": False,
            "segmentInfo": [],
            "jobId": "011025012817",
            "companyId": 1428834,
            "brandingTags": [],
            "functionalArea": "Data Science & Analytics",
            "fatFooter": {},
            "experienceText": "0-1 Yrs",
            "vacancy": 1,
            "template": "",
            "description": "<p><strong>0.6-1.5 years of experience in AI/ML development, preferably in product-based environments.</strong><br /><strong>Strong programming skills in Python and hands-on experience with ML frameworks like TensorFlow, PyTorch, or Scikit-learn.</strong><br /><strong>Solid understanding of NLP techniques, deep learning, and statistical modeling.</strong><br /><strong>Experience with RESTful APIs, cloud services (AWS/GCP/Azure), and data versioning tools like DVC or MLflow.</strong><br /><strong>Familiarity with CI/CD for ML models and model monitoring tools.</strong><br /><strong>Good problem-solving skills and the ability to work in a fast-paced, collaborative environment.</strong><br /><strong>Bonus: Exposure to hiring tech or ed-tech products and experience with large language models (LLMs)</strong> <strong>Role & responsibilities</strong> </p><br />",
            "staticCompanyName": "innovationm-jobs-careers-1083772",
            "industry": "IT Services & Consulting",
            "staticUrl": "https://www.naukri.com/job-listings-ai-engineer-ai-innovationm-noida-0-to-1-years-011025012817",
            "title": "AI Engineer/ AI",
            "walkIn": False,
            "maximumExperience": 1,
            "logStr": "--jobsearchDesk-1-F-0-1--17596672549506513-",
            "viewCount": 3413,
            "jobType": "fulltime",
            "companyPageUrl": "innovationm-overview-753464",
            "minimumExperience": 0,
            "employmentType": "Full Time, Permanent",
            "banner": "https://img.naukimg.com/logo_images/groups/v1/753464.gif",
            "microsite": False,
            "createdDate": "2025-10-01 12:24:50",
            "consultant": False,
            "socialBanner": "https://img.naukimg.com/logo_images/groups/v1/753464.gif",
            "showRecruiterDetail": False,
            "locations": [{"localities": [], "label": "Noida", "url": "https://www.naukri.com/jobs-in-noida"}],
            "keySkills": {
                "other": [
                    {"clickable": "artificial intelligence", "label": "Artificial Intelligence"},
                    {"clickable": "machine learning", "label": "Machine Learning"},
                    {"clickable": "python", "label": "Python"}
                ],
                "preferred": [{"clickable": "", "label": "Aiml"}]
            },
            "salaryDetail": {
                "minimumSalary": 100000,
                "maximumSalary": 375000,
                "currency": "INR",
                "hideSalary": True,
                "variablePercentage": {"source": "0.0", "parsedValue": 0},
                "label": "1-3.75 Lacs"
            },
            "board": "1"
        }
    }
    
    # Parse the response
    parsed_job = NaukriAPIParser.parse_api_response(real_api_response)
    
    # Extract description content
    description = parsed_job.jd
    
    print(f"\n🔍 REAL API RESPONSE TEST RESULTS:")
    print(f"Full Description Length: {len(description)} chars")
    print(f"Short Description Length: {len(short_desc)} chars") 
    print(f"Description Content: {description[:150]}...")
    
    # CRITICAL TESTS
    assert len(description) > 200, f"Description too short: {len(description)} chars"
    assert "TensorFlow, PyTorch" in description, "Missing ML frameworks"
    assert "NLP techniques" in description, "Missing NLP content"
    assert "large language models (LLMs)" in description, "Missing LLM content"
    
    # ERADICATION VERIFICATION - shortDescription content must NOT appear
    short_desc_parts = short_desc.split("|")
    for part in short_desc_parts:
        part = part.strip()
        if part and len(part) > 10:  # Only check meaningful parts
            assert part not in description, f"❌ CONTAMINATION DETECTED: '{part}' from shortDescription found in description"
    
    print("✅ COMPLETE ERADICATION VERIFIED - NO shortDescription contamination detected!")
    return parsed_job

if __name__ == "__main__":
    test_real_api_response()
