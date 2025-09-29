#!/usr/bin/env python3
# NLP-based skill extraction from job descriptions
# EMD Compliance: Pattern-based extraction with dynamic strategies

import re
from utils.analysis.nlp.soft_skills_patterns import SOFT_SKILLS_PATTERNS
import logging

logger = logging.getLogger(__name__)

# Comprehensive tech skills for AI/ML/Data/Software roles (150+ patterns)
SKILL_PATTERNS: dict[str, list[str]] = {
    # Programming Languages
    "python": ["python", "\\bpy\\b"], "r": ["\\br\\b", "r programming"],
    "sql": ["sql", "mysql", "postgresql", "t-sql", "plsql"],
    "java": ["\\bjava\\b"], "javascript": ["javascript", "\\bjs\\b", "node.js", "nodejs"],
    "typescript": ["typescript", "ts"], "c++": ["c\\+\\+", "cpp"],
    "c#": ["c#", "csharp", "c sharp"], "go": ["\\bgolang\\b", "\\bgo\\b"],
    "scala": ["scala"], "julia": ["julia"], "ruby": ["ruby"],
    "php": ["\\bphp\\b"], "swift": ["swift"], "kotlin": ["kotlin"],
    "rust": ["rust"], "perl": ["perl"], "shell": ["bash", "shell script"],
    
    # ML/AI Frameworks & Libraries
    "tensorflow": ["tensorflow", "\\btf\\b"], "pytorch": ["pytorch", "torch"],
    "keras": ["keras"], "scikit-learn": ["scikit-learn", "sklearn"],
    "xgboost": ["xgboost", "xgb"], "lightgbm": ["lightgbm", "lgbm"],
    "catboost": ["catboost"], "fastai": ["fastai"], "mxnet": ["mxnet"],
    "caffe": ["caffe"], "theano": ["theano"], "jax": ["jax"],
    
    # Data Processing & Analysis
    "pandas": ["pandas", "\\bpd\\b"], "numpy": ["numpy", "\\bnp\\b"],
    "scipy": ["scipy"], "dask": ["dask"], "polars": ["polars"],
    "spark": ["spark", "pyspark", "apache spark"],
    "hadoop": ["hadoop", "hdfs"], "hive": ["hive"], "pig": ["pig"],
    "kafka": ["kafka", "apache kafka"], "airflow": ["airflow"],
    "nifi": ["nifi"], "flink": ["flink"], "beam": ["apache beam"],
    
    # Cloud Platforms
    "aws": ["aws", "amazon web services", "ec2", "s3", "lambda"],
    "azure": ["azure", "microsoft azure"], "gcp": ["gcp", "google cloud"],
    "databricks": ["databricks"], "snowflake": ["snowflake"],
    
    # DevOps & Infrastructure  
    "docker": ["docker", "container"], "kubernetes": ["kubernetes", "k8s"],
    "jenkins": ["jenkins"], "gitlab": ["gitlab", "gitlab ci"],
    "github actions": ["github actions"], "terraform": ["terraform"],
    "ansible": ["ansible"], "ci/cd": ["ci/cd", "cicd"],
    
    # Databases
    "mongodb": ["mongodb", "mongo"], "redis": ["redis"],
    "elasticsearch": ["elasticsearch", "elastic"],
    "cassandra": ["cassandra"], "dynamodb": ["dynamodb"],
    "oracle": ["oracle db"], "mssql": ["mssql", "sql server"],
    "sqlite": ["sqlite"], "neo4j": ["neo4j"], "graphql": ["graphql"],
    
    # LLM & GenAI
    "langchain": ["langchain"], "openai": ["openai", "gpt"],
    "huggingface": ["huggingface", "hugging face", "transformers"],
    "llm": ["llm", "large language model"], "genai": ["genai", "generative ai"],
    "rag": ["rag", "retrieval augmented"],
    "vector database": ["vector database", "pinecone", "weaviate", "chroma"],
    "bert": ["bert"], "gpt": ["gpt"], "llama": ["llama"],
    
    # Web Frameworks
    "react": ["react", "reactjs"], "angular": ["angular"],
    "vue": ["vue", "vuejs"], "django": ["django"],
    "flask": ["flask"], "fastapi": ["fastapi"],
    "express": ["express"], "nextjs": ["next.js", "nextjs"],
    
    # Visualization & BI
    "tableau": ["tableau"], "power bi": ["power bi", "powerbi"],
    "matplotlib": ["matplotlib"], "seaborn": ["seaborn"],
    "plotly": ["plotly"], "d3": ["d3.js", "d3"],
    "looker": ["looker"], "qlik": ["qlik"],
    
    # Testing & Quality
    "pytest": ["pytest"], "junit": ["junit"], "selenium": ["selenium"],
    "jest": ["jest"], "mocha": ["mocha"], "cypress": ["cypress"],
    
    # Methodologies & Practices  
    "agile": ["agile", "scrum"], "git": ["git", "github", "version control"],
    "rest api": ["rest api", "restful"], "microservices": ["microservices"],
    "etl": ["etl"], "nlp": ["nlp", "natural language processing"],
    "computer vision": ["computer vision", "cv", "image processing"],
    "deep learning": ["deep learning", "\\bdl\\b"],
    "machine learning": ["machine learning", "\\bml\\b"],
    "statistics": ["statistics", "statistical"],
}

# Merge with soft skills patterns for comprehensive extraction
ALL_SKILL_PATTERNS = {**SKILL_PATTERNS, **SOFT_SKILLS_PATTERNS}

def extract_skills_from_text(text: str) -> list[str]:
    """Dynamic NLP-based skill extraction with multiple strategies
    
    Strategies:
    1. Context keyword extraction (skills:, experience with:, etc.)
    2. Comma-separated list parsing
    3. Bullet point detection
    4. N-gram analysis (bi-grams, tri-grams)
    5. Full-text pattern matching
    
    Args:
        text: Job description text
        
    Returns:
        List of extracted skills (normalized, deduplicated)
    """
    if not text:
        return []
    
    text_lower = text.lower()
    found_skills: set[str] = set()
    
    # Strategy 1: Context-based extraction after skill keywords
    skill_contexts = [
        r'skills?:', r'technologies:', r'tools?:', r'frameworks?:',
        r'experience (with|in):', r'proficiency (with|in):',
        r'knowledge of:', r'expertise (with|in):', r'familiar with:'
    ]
    
    for context_pattern in skill_contexts:
        for match in re.finditer(context_pattern, text_lower):
            start = match.end()
            end = text_lower.find('.', start)
            if end == -1:
                end = start + 200
            context_text = text_lower[start:end]
            _extract_from_delimited_text(context_text, found_skills)
    
    # Strategy 2: Comma-separated lists parsing
    sentences = re.split(r'[.!?]', text_lower)
    for sentence in sentences:
        if ',' in sentence:
            _extract_from_delimited_text(sentence, found_skills)
    
    # Strategy 3: Bullet points (•, -, *, numbers)
    bullet_lines = re.split(r'[\n•\-\*]|\d+\.', text_lower)
    for line in bullet_lines:
        if line.strip():
            _extract_from_delimited_text(line, found_skills)
    
    # Strategy 4: N-gram analysis
    words = text_lower.split()
    for i in range(len(words) - 2):
        bigram = f"{words[i]} {words[i+1]}"
        trigram = f"{words[i]} {words[i+1]} {words[i+2]}"
        _match_skill_patterns(bigram, found_skills)
        _match_skill_patterns(trigram, found_skills)
    
    # Strategy 5: Full-text pattern matching
    _match_skill_patterns(text_lower, found_skills)
    
    return list(found_skills)

def _extract_from_delimited_text(text: str, found_skills: set[str]) -> None:
    """Extract skills from comma/semicolon delimited text"""
    parts = re.split(r'[,;]', text)
    for part in parts:
        part_clean = part.strip()
        if part_clean:
            _match_skill_patterns(part_clean, found_skills)

def _match_skill_patterns(text: str, found_skills: set[str]) -> None:
    """Match skill patterns in given text (hard + soft skills)"""
    for skill_name, patterns in ALL_SKILL_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                found_skills.add(skill_name)
                break
