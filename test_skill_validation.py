"""Validate regex skill extractor with real job samples"""
from src.analysis.skill_extraction.regex_extractor import (
    load_skill_patterns,
    extract_skills_from_text
)

# Load patterns once for performance
patterns = load_skill_patterns()

# Sample AI Engineer job description
ai_job = """
Senior AI Engineer - Join our team building cutting-edge GenAI solutions!
Requirements: 5+ years Python, TensorFlow, PyTorch experience. Strong knowledge 
of LLMs, prompt engineering, vector databases (Pinecone, Weaviate). Experience 
with AWS, Docker, Kubernetes. Proficient in SQL, MongoDB. Bachelor's degree in 
Computer Science required. Excellent communication and teamwork skills.
"""

# Sample Data Scientist job
ds_job = """
Data Scientist position open! Work with large-scale datasets using Python, R, 
Pandas, NumPy, Scikit-learn. Build ML models with XGBoost, Random Forests. 
Visualize insights using Tableau, Power BI. Experience with Spark, Hadoop 
preferred. Strong mathematical background in statistics and linear algebra.
"""

# Sample ML Engineer job
ml_job = """
ML Engineer needed for production ML pipelines. Tech stack: Python, FastAPI, 
Docker, Kubernetes, MLflow, Airflow. Deploy models on AWS SageMaker or GCP 
Vertex AI. Experience with model monitoring, CI/CD, Git, GitHub Actions. 
Knowledge of REST APIs, microservices architecture essential.
"""

print("=" * 70)
print("SKILLS EXTRACTION VALIDATION TEST")
print("=" * 70)

test_cases = [
    ("AI Engineer Job", ai_job),
    ("Data Scientist Job", ds_job),
    ("ML Engineer Job", ml_job)
]

for name, description in test_cases:
    print(f"\n{name}:")
    print("-" * 70)
    skills = extract_skills_from_text(description, patterns)
    print(f"Found {len(skills)} technical skills:")
    for skill in skills:
        print(f"  ✓ {skill}")
    
    # Validate no false positives
    false_positives = ["Education", "Healthcare", "Communication", "Teamwork"]
    found_fp = [fp for fp in false_positives if fp in skills]
    if found_fp:
        print(f"\n  ⚠️ WARNING: Found false positives: {found_fp}")
    else:
        print(f"\n  ✅ No false positives detected")

print("\n" + "=" * 70)
print("VALIDATION COMPLETE")
print("=" * 70)
