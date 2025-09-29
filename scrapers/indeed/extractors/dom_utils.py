#!/usr/bin/env python3
# Indeed DOM utilities for safe element extraction
# EMD Compliance: ≤80 lines

from typing import Optional
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def safe_find_element(parent: WebElement, selector: str) -> Optional[WebElement]:
    """Safely find element using CSS selector"""
    try:
        return parent.find_element(By.CSS_SELECTOR, selector)
    except NoSuchElementException:
        return None

def safe_text(element: Optional[WebElement]) -> str:
    """Safely extract text from element"""
    return element.text.strip() if element else ""

def safe_attribute(element: Optional[WebElement], attr: str) -> str:
    """Safely extract attribute from element"""
    if not element:
        return ""
    try:
        return element.get_attribute(attr) or ""
    except Exception:
        return ""

def find_elements_safe(parent: WebElement, selector: str) -> list:
    """Safely find multiple elements"""
    try:
        return parent.find_elements(By.CSS_SELECTOR, selector)
    except NoSuchElementException:
        return []
