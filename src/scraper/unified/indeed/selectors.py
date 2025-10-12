"""Indeed CSS and XPath selectors configuration"""

# Search results
SEARCH_SELECTOR = "a.tapItem"

# Job card selectors (CSS primary, XPath fallback) - 2025 structure
CARD_SELECTORS_CSS = [
    "div.job_seen_beacon",
    "div[class*='mosaic']",
    "div.jobsearch-SerpJobCard",
    "li.css-5lfssm",
    "div[data-jk]",
]
CARD_SELECTORS_XPATH = [
    "//div[contains(@class, 'job_seen_beacon')]",
    "//div[contains(@class, 'mosaic')]",
    "//div[contains(@class, 'jobsearch-SerpJobCard')]",
    "//li[contains(@class, 'css-5lfssm')]",
    "//div[@data-jk]",
]

# Job description selectors (CSS primary, XPath fallback)
DESC_SELECTORS_CSS = [
    "div#jobDescriptionText",
    "div.jobsearch-jobDescriptionText",
    "div.job-snippet",
]
DESC_SELECTORS_XPATH = [
    "//div[@id='jobDescriptionText']",
    "//div[contains(@class, 'jobsearch-jobDescriptionText')]",
    "//div[contains(@class, 'job-snippet')]",
]
