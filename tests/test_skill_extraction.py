#!/usr/bin/env python3
# Test script for Codebasics-focused skill extraction
# EMD Compliance: ≤80 lines

from scrapers.linkedin.skill_extractor import (
    extract_skills_from_description,
    is_codebasics_relevant_role,
    format_skills_as_string
)

def test_skill_extraction():
    """Test skill extraction with sample job descriptions"""
    
    # Sample data science job description
    ds_description = """
    We are looking for a Data Scientist with experience in Python, pandas, 
    machine learning, and SQL. The role involves working with large datasets,
    building predictive models using scikit-learn and TensorFlow, and creating
    visualizations with matplotlib and Power BI. Experience with AWS and 
    statistical analysis is preferred.
    """
    
    # Sample business analyst job description  
    ba_description = """
    Business Analyst position requiring expertise in Excel, SQL, and Tableau.
    You will work on data warehousing projects, create KPI dashboards, and
    perform statistical analysis. Knowledge of ETL processes and reporting
    tools like Looker is a plus.
    """
    
    # Test skill extraction
    ds_skills = extract_skills_from_description(ds_description)
    ba_skills = extract_skills_from_description(ba_description)
    
    print("Data Science Job Skills:", ds_skills)
    print("Business Analyst Job Skills:", ba_skills)
    
    # Test job role relevance
    test_roles = [
        "Data Scientist", "Business Analyst", "AI Engineer", 
        "Machine Learning Engineer", "Marketing Manager"
    ]
    
    for role in test_roles:
        is_relevant = is_codebasics_relevant_role(role)
        print(f"{role}: {'✓ Relevant' if is_relevant else '✗ Not Relevant'}")
    
    # Test skill formatting
    formatted_ds = format_skills_as_string(ds_skills, "Data Scientist")
    formatted_ba = format_skills_as_string(ba_skills, "Business Analyst")
    
    print("\nFormatted Skills:")
    print("DS:", formatted_ds)
    print("BA:", formatted_ba)

if __name__ == "__main__":
    test_skill_extraction()
