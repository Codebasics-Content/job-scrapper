#!/usr/bin/env python3
# Data Converter - Row to JobModel Data Conversion
# EMD Compliance: ≤80 lines

import json
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DataConverter:
    """
    Converts SQLite row data to JobModel format with proper type handling
    """
    
    def convert_row_to_job_data(self, row_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Convert SQLite row dict to JobModel format with proper types"""
        
        # Map database columns to JobModel fields
        job_data = {
            'job_id': self._safe_str(row_dict.get('job_id')),
            'Job_Role': self._safe_str(row_dict.get('job_role')),
            'Company': self._safe_str(row_dict.get('company')),  
            'Experience': self._safe_str(row_dict.get('experience')),
            'Skills': self._safe_str(row_dict.get('skills')),
            'jd': self._safe_str(row_dict.get('jd')),
            'platform': self._safe_str(row_dict.get('platform')),
            'url': row_dict.get('url'),
            'location': row_dict.get('location'),
            'salary': row_dict.get('salary'),
            'posted_date': self._safe_datetime(row_dict.get('posted_date')),
            'scraped_at': self._safe_datetime(row_dict.get('scraped_at')) or datetime.now(),
            'skills_list': self._safe_json_list(row_dict.get('skills')),
            'normalized_skills': self._safe_json_list(row_dict.get('skills'))
        }
        return job_data
    
    def _safe_str(self, value: Any) -> str:
        """Safely convert value to string with None handling"""
        return str(value) if value is not None else ""
    
    def _safe_datetime(self, value: Any) -> Optional[datetime]:
        """Safely convert value to datetime with None handling"""
        if value is None:
            return None
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace('Z', '+00:00'))
        return value
    
    def _safe_json_list(self, value: Any) -> Optional[List[str]]:
        """Safely convert JSON string to list with None handling"""
        if value is None or value == "":
            return None
        try:
            if isinstance(value, str):
                return json.loads(value)
            return value
        except (json.JSONDecodeError, TypeError):
            return None
