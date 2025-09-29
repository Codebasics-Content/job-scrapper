# Role Analysis Package - EMD Compliance: ≤80 lines
# Provides job role analysis and skill percentage calculations

from .job_filter import JobRoleFilter
from .skill_calculator import SkillPercentageCalculator

__all__ = [
    'JobRoleFilter',
    'SkillPercentageCalculator'
]
