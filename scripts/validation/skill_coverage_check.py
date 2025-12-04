#!/usr/bin/env python3
"""
Skill Coverage Analysis - Find missing skills and false positives
"""

import sqlite3
import re
from collections import Counter

# Common Data/ML skills to check if they're being extracted
SKILLS_TO_CHECK = [
    ('Pandas', r'\bpandas\b'),
    ('NumPy', r'\bnumpy\b'),
    ('Apache Spark', r'\bspark\b'),
    ('Airflow', r'\bairflow\b'),
    ('dbt', r'\bdbt\b'),
    ('Snowflake', r'\bsnowflake\b'),
    ('Redshift', r'\bredshift\b'),
    ('BigQuery', r'\bbigquery\b'),
    ('Databricks', r'\bdatabricks\b'),
    ('Kafka', r'\bkafka\b'),
    ('Hadoop', r'\bhadoop\b'),
    ('Hive', r'\bhive\b'),
    ('Looker', r'\blooker\b'),
    ('DAX', r'\bdax\b'),
    ('SSIS', r'\bssis\b'),
    ('Alteryx', r'\balteryx\b'),
    ('SAS', r'\bsas\b'),
    ('SPSS', r'\bspss\b'),
    ('Jupyter', r'\bjupyter\b'),
    ('Matplotlib', r'\bmatplotlib\b'),
    ('Seaborn', r'\bseaborn\b'),
    ('HuggingFace', r'\bhugging\s*face\b'),
    ('LangChain', r'\blangchain\b'),
    ('OpenAI API', r'\bopenai\b'),
    ('GPT', r'\bgpt-[34]\b|\bchatgpt\b'),
    ('BERT', r'\bbert\b'),
    ('XGBoost', r'\bxgboost\b'),
    ('LightGBM', r'\blightgbm\b'),
    ('MLflow', r'\bmlflow\b'),
    ('SageMaker', r'\bsagemaker\b'),
    ('Vertex AI', r'\bvertex\s*ai\b'),
    ('Streamlit', r'\bstreamlit\b'),
    ('FastAPI', r'\bfastapi\b'),
    ('Flask', r'\bflask\b'),
    ('Django', r'\bdjango\b'),
    ('MongoDB', r'\bmongodb\b'),
    ('PostgreSQL', r'\bpostgresql\b|\bpostgres\b'),
    ('MySQL', r'\bmysql\b'),
    ('Redis', r'\bredis\b'),
    ('Elasticsearch', r'\belasticsearch\b'),
    ('Neo4j', r'\bneo4j\b'),
    ('Pinecone', r'\bpinecone\b'),
    ('Weaviate', r'\bweaviate\b'),
    ('ChromaDB', r'\bchroma\s*db\b|\bchromadb\b'),
]

# Soft skills that might be false positives for tech analysis
SOFT_SKILLS = [
    'Communication',
    'Innovation',
    'Problem Solving',
    'Collaboration',
    'Decision Making',
    'Organization',
    'Leadership',
    'Flexibility',
    'Adaptability',
    'Creativity',
    'Teamwork',
    'Time Management',
]

def main():
    conn = sqlite3.connect('data/jobs.db')
    cursor = conn.cursor()

    cursor.execute("SELECT job_description, skills FROM jobs WHERE job_description IS NOT NULL")
    jobs = cursor.fetchall()

    print('=== SKILL COVERAGE ANALYSIS ===')
    print(f'Analyzing {len(jobs)} jobs...\n')

    # Check coverage for technical skills
    results = []
    for skill_name, pattern in SKILLS_TO_CHECK:
        mentioned = 0
        extracted = 0

        for desc, skills in jobs:
            if re.search(pattern, desc, re.IGNORECASE):
                mentioned += 1
                if skills and skill_name.lower() in skills.lower():
                    extracted += 1

        if mentioned > 0:
            results.append({
                'skill': skill_name,
                'mentioned': mentioned,
                'extracted': extracted,
                'gap': mentioned - extracted
            })

    # Sort by gap
    results.sort(key=lambda x: -x['gap'])

    print('--- MISSING SKILLS (in description but NOT extracted) ---')
    print(f"{'Skill':<20} {'Mentioned':>10} {'Extracted':>10} {'Gap':>10}")
    print('-' * 52)
    for r in [x for x in results if x['gap'] > 0]:
        print(f"{r['skill']:<20} {r['mentioned']:>10} {r['extracted']:>10} {r['gap']:>10}")

    print('\n--- WELL COVERED SKILLS ---')
    for r in [x for x in results if x['gap'] == 0 and x['mentioned'] > 10]:
        print(f"{r['skill']}: {r['mentioned']} mentions, all extracted")

    # Check soft skills counts
    print('\n--- SOFT SKILLS (potential false positives for tech analysis) ---')
    for soft_skill in SOFT_SKILLS:
        count = 0
        for desc, skills in jobs:
            if skills:
                job_skills = [s.strip() for s in skills.split(',')]
                if soft_skill in job_skills:
                    count += 1
        if count > 100:
            pct = count / len(jobs) * 100
            print(f"{soft_skill}: {count} jobs ({pct:.1f}%)")

    conn.close()

if __name__ == '__main__':
    main()
