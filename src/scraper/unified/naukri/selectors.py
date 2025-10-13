"""Naukri CSS and XPath selectors configuration"""

# Job card selectors (CSS primary, XPath fallback) - 2025 Naukri
CARD_SELECTORS_CSS = [
    ".srp-jobtuple-wrapper",  # Primary: <div class="srp-jobtuple-wrapper" data-job-id="...">
    ".cust-job-tuple",  # Secondary: nested inside srp-jobtuple-wrapper
    "div[data-job-id]",  # Fallback: any div with data-job-id
]

CARD_SELECTORS_XPATH = [
    "//div[contains(@class, 'srp-jobtuple-wrapper')]",
    "//div[contains(@class, 'cust-job-tuple')]",
    "//div[@data-job-id]",
]

# Job title link selectors (CSS primary, XPath fallback) - 2025 Naukri
TITLE_SELECTORS_CSS = [
    "a.title",  # Primary: <a class="title" href="..." title="Python Developer">
    ".row1 h2 a",  # Nested: <div class="row1"><h2><a class="title">
    "h2 > a",  # Fallback: any h2 > a inside card
    "a[href*='job-listings']",  # URL pattern match
]

TITLE_SELECTORS_XPATH = [
    ".//a[contains(@class, 'title')]",
    ".//div[contains(@class, 'row1')]//h2/a",
    ".//h2/a",
    ".//a[contains(@href, 'job-listings')]",
]

# Job description selectors (CSS primary, XPath fallback)
DESC_SELECTORS_CSS = [
    "div.jd-content",
    "div.job-description",
    "div.JDC",
    "section.job-desc",
]
DESC_SELECTORS_XPATH = [
    "//div[contains(@class, 'jd-content')]",
    "//div[contains(@class, 'job-description')]",
    "//div[contains(@class, 'JDC')]",
    "//section[contains(@class, 'job-desc')]",
]

# Skills section selectors (CSS primary, XPath fallback)
SKILLS_SELECTORS_CSS = ["div.key-skill", "div.key-skills"]
SKILLS_SELECTORS_XPATH = ["//div[contains(@class, 'key-skill')]"]
