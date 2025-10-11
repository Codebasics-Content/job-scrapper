"""Indeed CSS and XPath selectors configuration"""

# Search results
SEARCH_SELECTOR = "a.tapItem"

# Job card selectors (CSS primary, XPath fallback)
CARD_SELECTORS_CSS = ["div.job_seen_beacon", "div.jobsearch-SerpJobCard"]
CARD_SELECTORS_XPATH = ["//div[contains(@class, 'job_seen_beacon')]", "//div[contains(@class, 'jobsearch-SerpJobCard')]"]

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
