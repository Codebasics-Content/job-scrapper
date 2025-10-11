"""LinkedIn CSS and XPath selectors configuration"""

# Search results
SEARCH_SELECTOR = "a.base-card__full-link"

# Job card selectors (CSS primary, XPath fallback)
CARD_SELECTORS_CSS = ["div.base-card", "li.jobs-search-results__list-item"]
CARD_SELECTORS_XPATH = ["//div[contains(@class, 'base-card')]", "//li[contains(@class, 'jobs-search')]"]

# Job description selectors (CSS primary, XPath fallback)
DESC_SELECTORS_CSS = [
    "div.description__text",
    "div.show-more-less-html__markup",
    "section.description",
]
DESC_SELECTORS_XPATH = [
    "//div[contains(@class, 'description__text')]",
    "//div[contains(@class, 'show-more-less')]",
    "//section[contains(@class, 'description')]",
]
