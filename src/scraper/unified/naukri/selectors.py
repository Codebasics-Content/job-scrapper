"""Naukri CSS and XPath selectors configuration"""

# Job card selectors (CSS primary, XPath fallback) - 2025 Naukri
CARD_SELECTORS_CSS = [
    ".srp-jobtuple-wrapper",
    "div.srp-jobtuple-wrapper",
    "article.jobTuple",
    ".cust-job-tuple",
    "article[data-job-id]",
    "div[class*='tuple']",
]
CARD_SELECTORS_XPATH = [
    "//div[contains(@class, 'srp-jobtuple-wrapper')]",
    "//article[contains(@class, 'jobTuple')]",
    "//div[contains(@class, 'cust-job-tuple')]",
    "//article[@data-job-id]",
]

# Job title link selectors (CSS primary, XPath fallback) - 2025 Naukri
TITLE_SELECTORS_CSS = [
    "a.title.fw500",
    "a.title",
    "a[href*='/job-listings-']",
    "a[href*='/jobDetail/']",
    ".row1 a",
    "a.jobTitle",
    "a[title]",
]
TITLE_SELECTORS_XPATH = [
    "//a[contains(@class, 'title') and contains(@class, 'fw500')]",
    "//a[contains(@class, 'title')]",
    "//div[@class='row1']//a",
    "//a[contains(@href, '/job-listings-')]",
    "//a[contains(@href, '/jobDetail/')]",
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
