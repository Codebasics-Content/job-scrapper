# 7-Layer Skill Extraction Validation Architecture

## Overview

A comprehensive validation system for skill extraction that ensures accuracy, discovers emerging skills, and tracks quality over time.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    7-LAYER VALIDATION PIPELINE                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐ │
│  │   LAYER 1   │   │   LAYER 2   │   │   LAYER 3   │   │   LAYER 4   │ │
│  │   Pattern   │──▶│  Coverage   │──▶│     FP      │──▶│     FN      │ │
│  │   Syntax    │   │  Analysis   │   │  Detection  │   │  Detection  │ │
│  └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘ │
│        │                                                      │         │
│        ▼                                                      ▼         │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐                   │
│  │   LAYER 5   │   │   LAYER 6   │   │   LAYER 7   │                   │
│  │   Context   │──▶│  Emerging   │──▶│   Trend &   │                   │
│  │ Validation  │   │   Skills    │   │    Drift    │                   │
│  └─────────────┘   └─────────────┘   └─────────────┘                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Layer Details

### Layer 1: Pattern Syntax Validation (Pre-flight)
**Purpose:** Validate all regex patterns before extraction runs

| Check | Description | Severity |
|-------|-------------|----------|
| Syntax validity | Regex compiles without errors | Critical |
| Backtracking | Detect catastrophic backtracking | Critical |
| Escape chars | Proper escaping of special chars | High |
| Empty patterns | No empty or whitespace-only patterns | Medium |
| Duplicates | No duplicate patterns | Low |

**Output:** Pattern health report, invalid pattern list

---

### Layer 2: Coverage Analysis
**Purpose:** Measure skill detection across job descriptions

| Metric | Description |
|--------|-------------|
| Match count | How many JDs contain each skill |
| Coverage % | Percentage of JDs with skill |
| Distribution | Skill frequency distribution |
| Top N skills | Most common skills |

**Output:** Coverage report, skill frequency table

---

### Layer 3: False Positive Detection
**Purpose:** Find skills extracted incorrectly

| Check | Description |
|-------|-------------|
| Pattern mismatch | Extracted but pattern doesn't match JD |
| Word collision | Common words matching (Go, Make, R) |
| Partial match | Matching inside larger words |

**Metric:** Precision = TP / (TP + FP)

**Output:** FP list with examples, precision score

---

### Layer 4: False Negative Detection
**Purpose:** Find skills that should have been extracted

| Check | Description |
|-------|-------------|
| Pattern match | Pattern matches JD but skill not extracted |
| Variant miss | Skill variant not in patterns |
| Case issues | Case sensitivity problems |

**Metric:** Recall = TP / (TP + FN)

**Output:** FN list with examples, recall score

---

### Layer 5: Context Validation
**Purpose:** Validate skills appear in correct context

| Context Type | Pattern Examples |
|--------------|------------------|
| Negative | "no Python", "not required", "without" |
| Wrong context | Non-technical usage |
| Requirement level | "required" vs "preferred" vs "nice to have" |
| Experience level | "5+ years", "senior", "junior" |

**Output:** Context-aware skill extraction, confidence scores

---

### Layer 6: Emerging Skills Detection
**Purpose:** Discover new skills not in reference file

| Detection Method | Description |
|------------------|-------------|
| CamelCase terms | NewTechName, FastAPI |
| Acronyms | LLM, RAG, MLOps |
| Tech patterns | *.js, *.io, *DB, *ML |
| N-gram analysis | Frequent multi-word tech terms |
| Version patterns | v2, 3.0, 2024 |

**Thresholds:**
- Minimum frequency: 10+ occurrences
- Minimum JD coverage: 0.5%

**Output:** Candidate skills list, frequency analysis

---

### Layer 7: Trend & Drift Analysis
**Purpose:** Track skill extraction quality over time

| Metric | Description |
|--------|-------------|
| F1 trend | F1 score over time |
| New skills rate | New skills discovered per period |
| Pattern decay | Patterns becoming less effective |
| Skill velocity | Rising/falling skill trends |

**Output:** Trend charts, drift alerts, skill velocity report

---

## Metrics Summary

| Metric | Formula | Target |
|--------|---------|--------|
| Precision | TP / (TP + FP) | > 95% |
| Recall | TP / (TP + FN) | > 90% |
| F1 Score | 2 * (P * R) / (P + R) | > 92% |
| Coverage | Skills matched / Total skills | > 60% |

---

## File Structure

```
scripts/validation/
├── layer1_syntax_check.sh      # Pattern syntax validation
├── layer2_coverage.sh          # Coverage analysis (existing)
├── layer3_fp_detection.sh      # False positive detection (existing)
├── layer4_fn_detection.sh      # False negative detection (existing)
├── layer5_context.sh           # Context validation
├── layer6_emerging_skills.sh   # Emerging skills detection
├── layer7_trend_analysis.sh    # Trend & drift analysis
├── run_all_validations.sh      # Orchestrator (all 7 layers)
└── lib/
    └── common.sh               # Shared utilities
```

---

## Usage

```bash
# Run all 7 layers
bash scripts/validation/run_all_validations.sh

# Run individual layers
bash scripts/validation/layer1_syntax_check.sh
bash scripts/validation/layer6_emerging_skills.sh

# Run with custom sample size
bash scripts/validation/run_all_validations.sh data/jobs.db 1000
```
