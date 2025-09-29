# Product Context - Job Scrapper

## Business Requirements
**Product Vision**: Multi-platform job scraping tool providing skill analysis and career insights for job seekers
**Current Status**: Core analysis pipeline operational, ready for production testing

## Core Business Value
- **For Job Seekers**: Understand skill demand trends across platforms (LinkedIn, Indeed, Naukri, YCombinator)
- **For Career Planning**: Data-driven insights on skill requirements for specific roles
- **For Market Analysis**: Comprehensive view of job market trends and skill popularity

## Target Users
1. **Individual Job Seekers** - Analyzing skills for target roles
2. **Career Counselors** - Providing data-backed guidance
3. **Educational Institutions** - Curriculum alignment with industry needs
4. **HR Professionals** - Market research for skill requirements

## Success Metrics
- **Data Quality**: >95% accurate job extraction from platforms
- **Coverage**: Support for 4+ major job platforms
- **Performance**: Complete analysis for 100+ jobs within 5 minutes
- **Skill Accuracy**: >90% accuracy in skill extraction and normalization
- **✅ Pipeline Operational**: End-to-end report generation working (database → analysis → formatting)
- **✅ Constitutional Compliance**: Article XIV ratified - AI agent governance framework active

## Platform Requirements
- **LinkedIn**: Premium job listings with detailed requirements
- **Indeed**: High-volume job postings with standardized formats
- **Naukri**: India-specific job market coverage
- **YCombinator**: Startup ecosystem and emerging tech roles

## Report Format Requirements
**Output Example**: "RAG 89%, Langchain 62%, Crew AI 41%, Python 95%"
- Skill percentage = (jobs_mentioning_skill / total_jobs_scraped) * 100
- Skills normalized to lowercase for consistency
- Results sorted by percentage (highest first)

## Business Constraints
- **Legal Compliance**: Respect robots.txt and rate limiting
- **Data Privacy**: No personal information storage
- **Anti-Detection**: Maintain low-profile scraping to avoid IP blocks
- **Resource Limits**: Optimize for single-machine deployment

## Future Business Opportunities
- **LLM Integration**: AI-powered career recommendations
- **Trend Analysis**: Historical skill demand tracking
- **Premium Features**: Advanced analytics and personalized insights
- **API Services**: B2B integration for career platforms
