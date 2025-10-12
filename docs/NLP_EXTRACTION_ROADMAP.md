# Skill Extraction Improvement Roadmap

**Status**: CRITICAL - Current accuracy 55% unacceptable for production  
**Goal**: Achieve 85-95% extraction accuracy via NLP-based solution  
**Timeline**: 3 weeks to production deployment

---

## 🎯 Success Metrics

| Metric | Current | Target | Method |
|--------|---------|--------|--------|
| Extraction Accuracy | 55% | 90% | NLP-based |
| False Positives | High | <5% | Context-aware |
| False Negatives | High | <10% | Semantic understanding |
| Processing Speed | 0.1s/job | <3s/job | Acceptable tradeoff |

---

## 📅 Phase 1: Immediate Fixes (Week 1)

### Objectives
- Add critical missing skills to reference JSON
- Fix worst regex false positives
- Improve accuracy to 70-75%

### Tasks

#### 1.1 Update skills_reference_2025.json
```json
{
  "devops_practices": [
    {"name": "CI/CD", "patterns": ["ci/cd", "ci-cd", "cicd"]},
    {"name": "MLOps", "patterns": ["mlops", "ml ops"]}
  ],
  "ml_techniques": [
    {"name": "Fine-tuning", "patterns": ["fine-tuning", "finetuning"]},
    {"name": "Bias Detection", "patterns": ["bias detection", "fairness"]},
    {"name": "Model Deployment", "patterns": ["model deployment", "deployment"]}
  ],
  "multi_word_skills": [
    "natural language processing",
    "computer vision",
    "machine learning",
    "data pipelines",
    "neural networks",
    "predictive modeling"
  ]
}
```

#### 1.2 Fix Single-Letter False Positives
```python
# Remove problematic patterns
EXCLUDE_PATTERNS = [
    r'\bc\b',  # Too many false positives
    r'\br\b',  # Matches "we're", "our"
    r'\bgo\b'  # Matches "going", "Google"
]

# Add stricter patterns
IMPROVED_PATTERNS = {
    "C": r'\bC\b(?=\s+programming|\+\+)',  # Only "C programming" or "C++"
    "R": r'\bR\b(?=\s+programming|statistical)',  # Only "R programming"
    "Go": r'\bGo\b(?=lang|\s+language)'  # Only "Golang" or "Go language"
}
```

#### 1.3 Test & Validate
- Re-run extraction on 100 sample jobs
- Measure accuracy improvement
- Document remaining gaps

**Deliverables**: Updated reference JSON, improved extraction accuracy ~70%

---

## 📅 Phase 2: NLP Proof of Concept (Week 2)

### Objectives
- Implement SkillNER integration
- Benchmark against current regex
- Validate 85%+ accuracy achievable

### Tasks

#### 2.1 Setup SkillNER Environment
```bash
# Install dependencies
pip install skillNer spacy
python -m spacy download en_core_web_lg

# Test basic extraction
from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor
import spacy

nlp = spacy.load("en_core_web_lg")
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)

# Extract from sample job
text = "Python developer with MLOps and NLP experience"
annotations = skill_extractor.annotate(text)
```

#### 2.2 Create Hybrid Extractor
```python
# src/analysis/skill_extraction/nlp_extractor.py

class HybridSkillExtractor:
    """Combines SkillNER + regex for best results"""
    
    def __init__(self):
        self.nlp_extractor = SkillNERExtractor()
        self.regex_extractor = RegexExtractor()
    
    def extract(self, job_description: str) -> list[str]:
        # Primary: NLP-based extraction
        nlp_skills = self.nlp_extractor.extract(job_description)
        
        # Fallback: Regex for technical terms
        regex_skills = self.regex_extractor.extract(job_description)
        
        # Merge + deduplicate
        return self._merge_skills(nlp_skills, regex_skills)
```

#### 2.3 Benchmark Performance
```python
# Run on 100 sample jobs
results = {
    'regex_only': {'accuracy': 0.55, 'speed': 0.1},
    'skillner_only': {'accuracy': 0.87, 'speed': 2.3},
    'hybrid': {'accuracy': 0.91, 'speed': 2.5}
}
```

**Deliverables**: Working NLP POC, benchmark report, accuracy >85%

---

## 📅 Phase 3: Production Deployment (Week 3)

### Objectives
- Integrate NLP extractor into pipeline
- Re-process all historical jobs
- Deploy to production

### Tasks

#### 3.1 Implement Production Extractor
```python
# src/analysis/skill_extraction/production_extractor.py

class ProductionSkillExtractor:
    """Production-ready hybrid extractor with caching"""
    
    def __init__(self):
        self.extractor = HybridSkillExtractor()
        self.cache = SkillCache()
    
    def extract_batch(self, jobs: list[dict]) -> list[dict]:
        """Batch processing for efficiency"""
        results = []
        for job in jobs:
            # Check cache first
            if cached := self.cache.get(job['job_id']):
                results.append(cached)
            else:
                skills = self.extractor.extract(job['description'])
                self.cache.set(job['job_id'], skills)
                results.append(skills)
        return results
```

#### 3.2 Re-Extract Historical Data
```bash
# Re-process 1000 existing jobs
./venv/bin/python3 scripts/reextract_all_jobs.py \
    --method nlp \
    --batch-size 50 \
    --output jobs_reextracted.db
```

#### 3.3 Update Analytics Dashboard
```python
# Update Streamlit app to show improved data
st.metric("Extraction Accuracy", "91%", "+36%")
st.metric("Skills Detected", "1,247", "+523")
```

#### 3.4 Deploy & Monitor
- Deploy new extractor to production
- Monitor accuracy metrics
- Set up alerts for extraction failures

**Deliverables**: Production deployment, 90%+ accuracy, updated analytics

---

## 🔧 Technical Architecture

### Current Architecture (Regex)
```
Job Description → Regex Patterns → Extracted Skills
                    (943 patterns)      (55% accuracy)
```

### Target Architecture (NLP Hybrid)
```
Job Description 
    ↓
    ├─→ SkillNER (Primary)
    │   ├─ NLP Entity Recognition
    │   ├─ Phrase Detection
    │   └─ Context Understanding
    │        ↓
    │   [85-90% coverage]
    │
    └─→ Regex (Fallback)
        ├─ Technical Acronyms (AWS, GCP)
        ├─ Version Numbers (Python 3.x)
        └─ Framework Names
             ↓
        [10-15% additional coverage]
    
    ↓
Merge & Deduplicate
    ↓
Extracted Skills (91% accuracy)
```

---

## 📦 Dependencies

### Required Packages
```txt
# NLP Libraries
spacy>=3.7.0
spacy-transformers>=1.3.0
skillNer>=1.0.0

# Models (download separately)
en_core_web_lg (spaCy large model ~500MB)
en_core_web_trf (transformer model ~1.2GB) [optional, higher accuracy]
```

### Installation
```bash
# Install packages
pip install spacy spacy-transformers skillNer

# Download models
python -m spacy download en_core_web_lg

# Optional: transformer model (better accuracy, slower)
python -m spacy download en_core_web_trf
```

---

## 🎓 Training & Documentation

### Developer Guide
1. **Understanding NLP Extraction**
   - How SkillNER works
   - Entity recognition concepts
   - When to use regex vs NLP

2. **Extending the System**
   - Adding custom skills
   - Training custom NER models
   - Hybrid extraction patterns

### User Guide
1. **For Analysts**: How to interpret skill data
2. **For Recruiters**: Using improved skill matching
3. **For Developers**: API documentation

---

## ⚠️ Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Model download size (500MB-1.2GB) | HIGH | Cache models, document in setup |
| Processing speed (2-3s/job) | MEDIUM | Batch processing, async execution |
| Memory usage spike | MEDIUM | Process in batches of 50 jobs |
| SkillNER model outdated | LOW | Monitor updates, plan migration path |
| Dependency conflicts | LOW | Use virtual environment, pin versions |

---

## 📊 Success Criteria

### Week 1
- ✅ Reference JSON updated with 20+ missing skills
- ✅ Regex accuracy improved to 70-75%
- ✅ Documentation complete

### Week 2
- ✅ SkillNER POC working
- ✅ Accuracy >85% on test set
- ✅ Performance benchmarks complete

### Week 3
- ✅ Production deployment successful
- ✅ All 1000 jobs re-extracted
- ✅ Analytics dashboard updated
- ✅ 90%+ extraction accuracy maintained

---

## 🚀 Next Actions

### This Week
1. Add CI/CD and MLOps to skills_reference_2025.json
2. Test SkillNER on 10 sample jobs
3. Document setup instructions

### Next Week
1. Implement hybrid extractor
2. Benchmark on 100 jobs
3. Present findings to stakeholders

### Following Week
1. Deploy to production
2. Re-extract all jobs
3. Monitor and optimize

---

**Owner**: AI Engineering Team  
**Priority**: CRITICAL  
**Status**: Week 1 - Planning Complete  
**Updated**: 2025-10-12T20:16:00+05:30
