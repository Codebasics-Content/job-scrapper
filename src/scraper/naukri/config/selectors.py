#!/usr/bin/env python3
"""Naukri CSS selectors configuration"""

# Job card selectors - Updated for 2025 Naukri structure
JOB_CARD_SELECTORS = [
    "article.jobTuple",           # Primary selector for job cards
    ".cust-job-tuple",            # Alternative selector
    "article[data-job-id]",       # Fallback selector
    ".list article"               # Generic article selector
]

# Element selectors within job cards
ELEMENT_SELECTORS = {
    "title": [
        "a.title",
        ".jobTupleHeader a",
        ".title.ellipsis",
        "h2 a"
    ],
    "company": [
        "a.comp-name",
        ".companyInfo a",
        ".comp-dtls a",
        ".company-name a"
    ],
    "experience": [
        ".exp-wrap",
        ".experience",
        ".exp",
        "li.exp-salary .exp"
    ],
    "salary": [
        ".sal-wrap",
        ".salary",
        ".sal",
        "li.exp-salary .sal"
    ],
    "location": [
        ".loc-wrap",
        ".location",
        ".loc",
        "li.location span"
    ],
    "skills": [
        ".tags-gt li",
        ".skill-tags li",
        ".tag-li",
        "ul.tags li"
    ],
    "posted_date": [
        ".job-post-day",
        ".postedDate",
        ".posted-date"
    ]
}

# Wait selectors to check page load
WAIT_SELECTORS = {
    "job_list": "article.jobTuple, .cust-job-tuple",
    "pagination": ".pagination",
    "total_count": ".sortAndH1Cont .count"
}
