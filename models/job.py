# Job Data Model - Pydantic v2 Thread-Safe Implementation
# EMD Compliance: ≤80 lines from typing import Callable, cast, Any
from datetime import datetime
from pydantic import BaseModel, Field, model_validator, ConfigDict
from typing import cast

class JobModel(BaseModel):
    """
    Thread-safe Job data model using Pydantic v2
    Database Schema: job_id, Job_Role, Company, Experience, Skills, jd
    """
    
    # Primary Fields (Database Schema Compliance)
    job_id: str = Field(..., description="Unique job identifier")
    job_role: str = Field(..., alias="Job_Role", description="Job title/role")
    company: str = Field(..., alias="Company", description="Company name")
    experience: str = Field(..., alias="Experience", description="Experience requirement")
    skills: str = Field(..., alias="Skills", description="Comma-separated skills")
    jd: str = Field(..., description="Job description text")
    
    # Additional Fields for Processing
    platform: str = Field(..., description="Source platform (LinkedIn, Indeed, etc.)")
    url: str | None = Field(None, description="Job posting URL")
    location: str | None = Field(None, description="Job location")
    salary: str | None = Field(None, description="Salary information")
    posted_date: datetime | None = Field(None, description="Job posting date")
    scraped_at: datetime = Field(default_factory=datetime.now, description="Scrape timestamp")
    
    # Processed Fields
    skills_list: list[str] | None = Field(None, description="Parsed skills list")
    normalized_skills: list[str] | None = Field(None, description="Normalized skills")
    
    model_config = ConfigDict(
        populate_by_name=True,  # Allow alias usage
        str_strip_whitespace=True,
        validate_assignment=True,
        use_enum_values=True,
        json_encoders={datetime: lambda dt: cast(datetime, dt).isoformat()}
    )
    
    @model_validator(mode='after')
    def parse_and_normalize_skills(self):
        """Parse skills string and create normalized skills list"""
        if self.skills:
            # Parse skills_list from comma-separated string
            if self.skills_list is None:
                self.skills_list = [skill.strip() for skill in self.skills.split(',') if skill.strip()]
            
            # Create normalized skills from skills_list
            if self.normalized_skills is None and self.skills_list:
                self.normalized_skills = [skill.lower() for skill in self.skills_list]
        
        return self
    
    def to_dict(self) -> dict[str, str | datetime | list[str] | None]:
        """Convert to dictionary for database storage"""
        return self.model_dump(by_alias=True, exclude_unset=True)
    
    def to_csv_row(self) -> dict[str, str]:
        """Convert to CSV-compatible row format"""
        return {
            'job_id': self.job_id,
            'Job_Role': self.job_role,
            'Company': self.company,
            'Experience': self.experience,
            'Skills': self.skills,
            'jd': self.jd,
            'platform': self.platform,
            'location': self.location or '',
            'salary': self.salary or '',
            'scraped_at': self.scraped_at.isoformat()
        }
