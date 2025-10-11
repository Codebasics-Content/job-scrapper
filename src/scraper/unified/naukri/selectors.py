"""Naukri CSS and XPath selectors configuration"""

# Job card selectors (CSS primary, XPath fallback)
CARD_SELECTORS_CSS = [
    "article.jobTuple",
    ".cust-job-tuple",
    "article[data-job-id]",
]
CARD_SELECTORS_XPATH = [
    "//article[contains(@class, 'jobTuple')]",
    "//div[contains(@class, 'cust-job-tuple')]",
    "//article[@data-job-id]",
]

# Job title link selectors (CSS primary, XPath fallback)
TITLE_SELECTORS_CSS = ["a.title", "a.title-text", "a[title]"]
TITLE_SELECTORS_XPATH = ["//a[contains(@class, 'title')]", "//a[@title]"]

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
