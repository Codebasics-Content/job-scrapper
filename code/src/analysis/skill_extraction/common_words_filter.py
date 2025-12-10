"""Common words and grammatical terms filter
EMD Compliance: ≤80 lines, NO pattern creation, ONLY filtering
"""

# Common grammatical words to remove (lowercase, UPPERCASE, Capitalize all handled)
COMMON_WORDS = {
    # Articles
    "a", "an", "the",
    
    # Conjunctions (splits like "MCP And Servers" into separate skills)
    "and", "or", "but", "yet", "so", "nor",
    
    # Prepositions  
    "at", "by", "for", "from", "in", "of", "on", "to", "with",
    "about", "across", "after", "among", "around", "before",
    "between", "during", "into", "near", "through", "under",
    
    # Pronouns
    "i", "you", "he", "she", "it", "we", "they", "me", "him", 
    "her", "us", "them", "my", "your", "his", "its", "our", "their",
    
    # Common verbs (not technical)
    "is", "am", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would",
    
    # Generic words
    "not", "no", "yes", "all", "some", "any", "each", "every",
    "both", "few", "many", "more", "most", "other", "such",
    "than", "then", "there", "these", "this", "those",
    "what", "when", "where", "which", "who", "why", "how",
    
    # Generic tech terms (filter ONLY when standalone, not in compound skills)
    "framework", "frameworks", "platform", "platforms",
    "server", "servers", "service", "services",
    "tool", "tools", "library", "libraries",
    "agentic"  # Generic "agentic" without specific framework name
}


def is_common_word(word: str) -> bool:
    """Check if word is common/grammatical (case-insensitive)"""
    return word.lower().strip() in COMMON_WORDS


def filter_common_words(skill: str) -> str | None:
    """
    Remove ONLY common/grammatical words from skill
    Returns None if empty after filtering
    Case-insensitive matching (lowercase, UPPERCASE, Capitalize)
    """
    words = skill.split()
    filtered = [w for w in words if not is_common_word(w)]
    
    return ' '.join(filtered) if filtered else None


def split_by_conjunctions(text: str) -> list[str]:
    """
    Split text by conjunctions (And, Or) into separate skills
    Example: "MCP And Servers" → ["MCP", "Servers"]
    Note: Generic terms like "Framework" will be filtered by filter_common_words()
    """
    import re
    # Split by And/Or (case-insensitive) but preserve other text
    parts = re.split(r'\s+(?:and|or)\s+', text, flags=re.IGNORECASE)
    return [p.strip() for p in parts if p.strip()]
