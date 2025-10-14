"""
Confidence Scoring System for Skill Extraction
Assigns 0.0-1.0 confidence scores based on pattern quality
"""
class ConfidenceScorer:
    """Calculate confidence scores for extracted skills"""
    
    def __init__(self):
        # Pattern type weights
        self.pattern_weights = {
            'exact_match': 1.0,           # Full skill name found
            'multi_word': 0.95,           # Multi-word phrase match
            'context_aware': 0.90,        # Context pattern match
            'skills_reference': 0.85,     # From skills_reference.json
            'abbreviation': 0.80,         # Abbreviation match (e.g., ML, AI)
            'partial': 0.60,              # Partial word match
        }
        
        # Skill length penalties (shorter = more ambiguous)
        self.length_penalties = {
            2: -0.15,   # 2 chars (e.g., AI, ML)
            3: -0.10,   # 3 chars (e.g., AWS, GCP)
            4: -0.05,   # 4 chars
        }
    
    def calculate(
        self,
        skill: str,
        pattern_type: str,
        match_count: int = 1,
        has_technical_context: bool = False
    ) -> float:
        """
        Calculate confidence score for a skill
        
        Args:
            skill: The extracted skill name
            pattern_type: Type of pattern that matched
            match_count: Number of times skill appears
            has_technical_context: Whether technical keywords nearby
        
        Returns:
            Confidence score between 0.0 and 1.0
        """
        # Base confidence from pattern type
        base_confidence = self.pattern_weights.get(pattern_type, 0.70)
        
        # Apply skill length penalty
        skill_len = len(skill.replace(' ', ''))
        if skill_len <= 4:
            penalty = self.length_penalties.get(skill_len, 0)
            base_confidence += penalty
        
        # Boost for multiple occurrences
        if match_count > 1:
            base_confidence = min(1.0, base_confidence + 0.05 * (match_count - 1))
        
        # Boost for technical context
        if has_technical_context:
            base_confidence = min(1.0, base_confidence + 0.05)
        
        # Clamp to valid range
        return max(0.0, min(1.0, base_confidence))
    
    def get_confidence_level(self, score: float) -> str:
        """Convert score to human-readable level"""
        if score >= 0.8:
            return "high"
        elif score >= 0.6:
            return "medium"
        else:
            return "low"
