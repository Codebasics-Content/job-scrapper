"""Naukri CSS selectors configuration"""

# Job card selectors (try in order)
CARD_SELECTORS = [
    "article.jobTuple",
    ".cust-job-tuple",
    "article[data-job-id]",
]

# Job title link selector
TITLE_SELECTOR = "a.title, a.title-text, a[title]"

# Job description selectors (try in order)
DESC_SELECTORS = [
    "div.jd-content",
    "div.job-description",
    "div.JDC",
    "section.job-desc",
]

# Skills section selector
SKILLS_SELECTOR = "div.key-skill"
