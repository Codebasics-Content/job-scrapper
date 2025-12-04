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
        datetime object or None if parsing fails or date is invalid
    """
    if not date_str:
        return None
    
    # Clean and lowercase
    date_str = date_str.strip().lower()
    
    # Extract number and unit using regex
    match = re.search(r'(\d+)\s*(minute|hour|day|week|month|year)', date_str)
    if not match:
        return None
    
    value = int(match.group(1))
    unit = match.group(2)
    
    # Validate reasonable ranges to catch errors
    if 'minute' in unit and value > 1440:  # More than 24 hours in minutes
        return None
    elif 'hour' in unit and value > 168:  # More than 1 week in hours
        return None
    elif 'day' in unit and value > 365:  # More than 1 year in days
        return None
    elif 'week' in unit and value > 52:  # More than 1 year in weeks
        return None
    elif 'month' in unit and value > 24:  # More than 2 years in months
        return None
    elif 'year' in unit and value > 5:  # More than 5 years (very old)
        return None
    
    # Calculate timedelta
    now = datetime.now()
    parsed_date = None
    
    if 'minute' in unit:
        parsed_date = now - timedelta(minutes=value)
    elif 'hour' in unit:
        parsed_date = now - timedelta(hours=value)
    elif 'day' in unit:
        parsed_date = now - timedelta(days=value)
    elif 'week' in unit:
        parsed_date = now - timedelta(weeks=value)
    elif 'month' in unit:
        # Approximate: 30 days per month
        parsed_date = now - timedelta(days=value * 30)
    elif 'year' in unit:
        # Approximate: 365 days per year
        parsed_date = now - timedelta(days=value * 365)
    
    # Final validation: ensure date is not in the future
    if parsed_date and parsed_date > now:
        return None
    
    return parsed_date


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
