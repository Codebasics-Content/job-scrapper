#!/usr/bin/env python3
# Date parsing utilities for relative date strings
# EMD Compliance: ≤80 lines

import re
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def parse_relative_date(date_text: str) -> datetime:
    """Parse relative date strings like '2 days ago', '1 week ago' to datetime
    
    Args:
        date_text: Relative date string from job posting
        
    Returns:
        Calculated datetime object
        
    Examples:
        '2 days ago' -> datetime 2 days before now
        '1 week ago' -> datetime 1 week before now
        '3 hours ago' -> datetime 3 hours before now
    """
    if not date_text:
        return datetime.now()
    
    date_text = date_text.lower().strip()
    now = datetime.now()
    
    # Extract number from text
    number_match = re.search(r'(\d+)', date_text)
    number = int(number_match.group(1)) if number_match else 1
    
    # Determine time unit and calculate
    if 'hour' in date_text or 'hr' in date_text:
        return now - timedelta(hours=number)
    elif 'minute' in date_text or 'min' in date_text:
        return now - timedelta(minutes=number)
    elif 'day' in date_text:
        return now - timedelta(days=number)
    elif 'week' in date_text or 'wk' in date_text:
        return now - timedelta(weeks=number)
    elif 'month' in date_text or 'mo' in date_text:
        return now - timedelta(days=number * 30)  # Approximate
    elif 'year' in date_text or 'yr' in date_text:
        return now - timedelta(days=number * 365)  # Approximate
    elif 'just now' in date_text or 'now' in date_text:
        return now
    else:
        logger.warning(f"Could not parse date: {date_text}, using current time")
        return now


def format_date_for_db(dt: datetime) -> str:
    """Format datetime for database storage
    
    Args:
        dt: datetime object
        
    Returns:
        ISO format string (YYYY-MM-DD HH:MM:SS)
    """
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def get_days_ago(date_text: str) -> int:
    """Get number of days ago from relative date string
    
    Args:
        date_text: Relative date string
        
    Returns:
        Number of days ago as integer
    """
    parsed_date = parse_relative_date(date_text)
    delta = datetime.now() - parsed_date
    return delta.days
