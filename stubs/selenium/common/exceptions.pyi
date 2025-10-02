# Selenium exception type stubs
# EMD Compliance: ≤80 lines

class WebDriverException(Exception):
    """Base exception for WebDriver errors"""
    pass

class NoSuchElementException(WebDriverException):
    """Raised when element cannot be found"""
    pass

class TimeoutException(WebDriverException):
    """Raised when a command times out"""
    pass

class StaleElementReferenceException(WebDriverException):
    """Raised when element is no longer in DOM"""
    pass
