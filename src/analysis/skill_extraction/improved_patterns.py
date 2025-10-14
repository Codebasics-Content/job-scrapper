"""
Improved regex patterns with lookaround for false positive elimination
"""

# Single-letter patterns with context requirements
IMPROVED_SINGLE_LETTER = {
    'C': r'\b[C](?=\s*(?:programming|language|\+\+))',
    'R': r'\b[R](?=\s*(?:programming|statistical|language))',
    'Go': r'(?<!on\s)(?<!to\s)\b(?:Go|Golang)\b(?!ing|ogle)',
}

# REMOVED: Short words causing false positives
# Rely on skills_reference_2025.json for all pattern matching
# Previous patterns over-matched: Gin ("Engineering"), etc.
IMPROVED_SHORT_WORDS = {}

# Exclude common non-skill contexts
EXCLUDE_CONTEXTS = {
    'education': r'(?<!Bachelor\'s\s+degree\s+in\s)(?<!Master\'s\s+degree\s+in\s)education\b',
    'communication': r'(?<!strong\s)(?<!excellent\s)communication(?=\s+skills)',
}

# Cloud platforms (strict matching)
CLOUD_PLATFORMS = {
    'AWS': r'\b(?:AWS|Amazon\s+Web\s+Services)\b',
    'Azure': r'\b(?:Azure|Microsoft\s+Azure)\b',
    'GCP': r'\b(?:GCP|Google\s+Cloud(?:\s+Platform)?)\b',
}

# Programming languages (improved)
PROGRAMMING_LANGUAGES = {
    'Python': r'\bPython(?:\s+\d+(?:\.\d+)?)?(?!\s+snake)\b',
    'Java': r'\b(?:Java)(?:\s+\d+)?(?!Script)\b',
    'JavaScript': r'\b(?:JavaScript|JS|ES6|ES2015|ES2020)\b',
    'TypeScript': r'\b(?:TypeScript|TS)\b',
}
