#!/usr/bin/env python3
# LinkedIn country codes for worldwide scraping
# EMD Compliance: ≤80 lines

"""
LinkedIn geoId codes for major countries
Use these to bypass the 60-job per query limitation
by scraping sequentially across countries
"""

LINKEDIN_COUNTRIES: list[dict[str, str]] = [
    {"name": "Worldwide", "geoId": ""},  # No geoId = worldwide
    {"name": "United States", "geoId": "103644278"},
    {"name": "India", "geoId": "102713980"},
    {"name": "United Kingdom", "geoId": "101165590"},
    {"name": "Canada", "geoId": "101174742"},
    {"name": "Germany", "geoId": "101282230"},
    {"name": "France", "geoId": "105015875"},
    {"name": "Australia", "geoId": "101452733"},
    {"name": "Netherlands", "geoId": "102890719"},
    {"name": "Singapore", "geoId": "102454443"},
    {"name": "Brazil", "geoId": "106057199"},
    {"name": "United Arab Emirates", "geoId": "104305776"},
    {"name": "Spain", "geoId": "105646813"},
    {"name": "Italy", "geoId": "103350119"},
    {"name": "Switzerland", "geoId": "106693272"},
    {"name": "Poland", "geoId": "105072130"},
    {"name": "Sweden", "geoId": "105117694"},
    {"name": "Belgium", "geoId": "100565514"},
    {"name": "Ireland", "geoId": "104738515"},
    {"name": "Austria", "geoId": "103883259"},
    {"name": "Denmark", "geoId": "104514075"},
    {"name": "Norway", "geoId": "103819153"},
    {"name": "Finland", "geoId": "100456013"},
    {"name": "Portugal", "geoId": "100364837"},
    {"name": "Israel", "geoId": "101620260"},
    {"name": "South Africa", "geoId": "102264497"},
    {"name": "New Zealand", "geoId": "105490917"},
    {"name": "Mexico", "geoId": "103323778"},
    {"name": "Argentina", "geoId": "100876405"},
    {"name": "Chile", "geoId": "104621616"},
    {"name": "Colombia", "geoId": "100876405"},
    {"name": "Romania", "geoId": "106670623"},
    {"name": "Czech Republic", "geoId": "104508036"},
    {"name": "Greece", "geoId": "104677530"},
    {"name": "Turkey", "geoId": "105149562"},
    {"name": "Ukraine", "geoId": "102264497"},
    {"name": "Malaysia", "geoId": "106808692"},
    {"name": "Philippines", "geoId": "103121230"},
    {"name": "Indonesia", "geoId": "102478259"},
    {"name": "Thailand", "geoId": "105146118"},
    {"name": "Vietnam", "geoId": "104195383"},
    {"name": "Japan", "geoId": "101355337"},
    {"name": "South Korea", "geoId": "105149562"},
    {"name": "Hong Kong", "geoId": "102095887"},
    {"name": "Taiwan", "geoId": "104187078"},
    {"name": "Pakistan", "geoId": "101165590"},
    {"name": "Bangladesh", "geoId": "100218597"},
    {"name": "Egypt", "geoId": "106155005"},
    {"name": "Nigeria", "geoId": "105365761"},
    {"name": "Kenya", "geoId": "102065699"},
]
