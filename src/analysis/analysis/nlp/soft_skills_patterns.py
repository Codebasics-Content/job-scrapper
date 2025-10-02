#!/usr/bin/env python3
# Soft skills patterns for job description extraction
# EMD Compliance: ≤80 lines

# Soft skills pattern dictionary
SOFT_SKILLS_PATTERNS: dict[str, list[str]] = {
    # Communication Skills
    "communication": ["communication", "communicator", "communicate"],
    "presentation": ["presentation", "presenting", "present to"],
    "writing": ["written communication", "writing skills", "technical writing"],
    "verbal": ["verbal communication", "oral communication", "speaking"],
    
    # Leadership & Management
    "leadership": ["leadership", "leading teams", "team lead"],
    "management": ["project management", "program management", "manage"],
    "mentoring": ["mentor", "mentorship", "coaching"],
    "delegation": ["delegation", "delegate tasks"],
    
    # Interpersonal Skills
    "teamwork": ["teamwork", "team player", "collaborative"],
    "collaboration": ["collaboration", "cross-functional", "work with teams"],
    "negotiation": ["negotiation", "negotiate", "consensus building"],
    "conflict resolution": ["conflict resolution", "resolve conflicts"],
    
    # Problem Solving
    "problem solving": ["problem solving", "troubleshooting", "root cause"],
    "analytical thinking": ["analytical", "analysis", "analyze"],
    "critical thinking": ["critical thinking", "evaluate", "assess"],
    "creativity": ["creative", "innovative", "innovation"],
    
    # Work Ethic
    "time management": ["time management", "prioritize", "deadline"],
    "attention to detail": ["attention to detail", "detail oriented", "meticulous"],
    "self motivated": ["self motivated", "self starter", "proactive"],
    "adaptability": ["adaptable", "flexible", "adapt to change"],
    
    # Emotional Intelligence
    "empathy": ["empathy", "empathetic", "understanding"],
    "active listening": ["active listening", "listening skills"],
    "emotional intelligence": ["emotional intelligence", "eq", "self aware"],
    
    # Additional Soft Skills
    "customer service": ["customer service", "client facing", "customer focus"],
    "strategic thinking": ["strategic", "strategic planning", "vision"],
    "decision making": ["decision making", "make decisions", "decisive"],
    "initiative": ["initiative", "take ownership", "ownership"],
    "multitasking": ["multitask", "multi task", "juggle priorities"],
    "organization": ["organizational skills", "organized", "organize"],
    "reliability": ["reliable", "dependable", "accountable"],
    "patience": ["patient", "patience", "calm under pressure"],
    "interpersonal": ["interpersonal skills", "people skills"],
    "networking": ["networking", "relationship building", "build relationships"],
}

# Contextual phrases indicating soft skills
SOFT_SKILL_CONTEXTS: list[str] = [
    r"strong (communication|leadership|analytical)",
    r"excellent (communication|interpersonal|organizational)",
    r"ability to (work|collaborate|communicate)",
    r"(team player|self[ -]?starter|detail[ -]?oriented)",
    r"proven (leadership|communication|problem[ -]?solving)",
]
