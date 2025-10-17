# Source Code Architecture

## Overview
This directory contains the complete job scraping system organized into specialized modules that work together to collect, validate, and analyze job market data.

## System Architecture

```
src/
├── analysis/          # Skill extraction and validation engine
├── config/            # Centralized configuration and reference data
├── db/                # Database operations and data persistence
├── models/            # Data structures and validation rules
├── scraper/           # Web scraping automation (LinkedIn & Naukri)
└── ui/                # Streamlit dashboard interface
```

## Module Responsibilities

### 📊 Analysis Module
**Purpose**: Extracts technical skills from job descriptions  
**Key Output**: Validated skill lists matching 749 canonical skills  
**Quality Impact**: Eliminates false positives, ensures accurate analytics

### ⚙️ Config Module
**Purpose**: Stores system-wide reference data  
**Contains**: 749 skills, country codes, location mappings  
**Benefit**: Update once, apply everywhere

### 💾 Database Module
**Purpose**: Manages SQLite data storage with atomic transactions  
**Key Feature**: Resume capability—never lose progress  
**Reliability**: Two-phase commit ensures data integrity

### 📋 Models Module
**Purpose**: Defines data structures and validation rules  
**Role**: Powers Gate 1 of triple validation system  
**Protection**: Prevents incomplete data from entering pipeline

### 🌐 Scraper Module
**Purpose**: Automated job collection from LinkedIn and Naukri  
**Architecture**: Two-phase (URL collection → Detail extraction)  
**Performance**: 8 concurrent workers with adaptive rate limiting  
**Features**: Anti-detection, real-time deduplication, fallback selectors

### 🖥️ UI Module
**Purpose**: User-facing Streamlit dashboard  
**Interface**: 3-tab design (Link Scraper, Detail Scraper, Analytics)  
**Experience**: Real-time progress tracking, visual validation gates

## Data Flow

```
1. USER INPUT (via UI)
   ↓
2. SCRAPER collects URLs → stores in DB
   ↓
3. SCRAPER extracts details → validates via MODELS
   ↓
4. ANALYSIS extracts skills → validates against CONFIG
   ↓
5. DB stores validated data atomically
   ↓
6. UI displays analytics from DB
```

## Quality Gates Integration

**Gate 1** (Models): Field validation—required fields, minimum lengths  
**Gate 2** (Analysis): Skill validation—749 canonical skills matching  
**Gate 3** (Database): Atomic storage—all-or-nothing transactions

## Key Design Principles

- **Modularity**: Each module has single, clear responsibility
- **Centralization**: Configuration managed in one place
- **Reliability**: Atomic transactions and resume capability
- **Efficiency**: Concurrent processing with adaptive rate limiting
- **Quality**: Triple validation ensures data accuracy

## For Developers

Each subfolder contains its own README with detailed module documentation. Start with the module most relevant to your work area.

## For Stakeholders

This architecture ensures:
- **Data Quality**: Triple validation catches bad data early
- **Reliability**: System can resume after interruptions
- **Scalability**: Concurrent processing handles large datasets
- **Maintainability**: Modular design simplifies updates
- **Transparency**: Real-time progress visible through UI

---

**Total Modules**: 6 specialized components  
**Total LOC**: ~3,500 lines (excluding tests)  
**Design Philosophy**: EMD (Elegant Modular Design) with ≤80 lines per file
