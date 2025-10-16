"""LinkedIn Date Parser - Convert relative times to datetime
EMD Compliance: ≤80 lines
"""
from datetime import datetime, timedelta
import re


def parse_linkedin_date(date_str: str) -> datetime | None:
    """Convert LinkedIn relative date string to datetime
    
    Examples: '2 minutes ago', '3 hours ago', '5 days ago', '2 weeks ago',
              '1 month ago', '3 months ago', '1 year ago'
    
    Args:
        date_str: LinkedIn date string (e.g., "2 days ago")
    
    Returns:
        datetime object or None if parsing fails
    """
    if not date_str or not isinstance(date_str, str):
        return None
    
    # Clean and lowercase
    date_str = date_str.strip().lower()
    
    # Extract number and unit using regex
    match = re.search(r'(\d+)\s*(minute|hour|day|week|month|year)', date_str)
    if not match:
        return None
    
    value = int(match.group(1))
    unit = match.group(2)
    
    # Calculate timedelta
    now = datetime.now()
    
    if 'minute' in unit:
        return now - timedelta(minutes=value)
    elif 'hour' in unit:
        return now - timedelta(hours=value)
    elif 'day' in unit:
        return now - timedelta(days=value)
    elif 'week' in unit:
        return now - timedelta(weeks=value)
    elif 'month' in unit:
        # Approximate: 30 days per month
        return now - timedelta(days=value * 30)
    elif 'year' in unit:
        # Approximate: 365 days per year
        return now - timedelta(days=value * 365)
    
    return None


def format_posted_date(dt: datetime | None) -> str | None:
    """Format datetime to ISO string for database storage
    
    Args:
        dt: datetime object
    
    Returns:
        ISO formatted string (YYYY-MM-DD HH:MM:SS) or None
    """
    if dt is None:
        return None
    
    return dt.strftime("%Y-%m-%d %H:%M:%S")
