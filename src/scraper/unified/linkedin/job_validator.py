"""Job validation logic for LinkedIn scraped data"""

import logging
import re
from typing import Tuple

from src.models.models import JobDetailModel

logger = logging.getLogger(__name__)

# Placeholder patterns that indicate incomplete/test postings
PLACEHOLDER_PATTERNS = [
    r"\btbd\b",
    r"\bto be determined\b",
    r"\bcoming soon\b",
    r"\blorem ipsum\b",
    r"\btest\s+(company|job|posting)\b",
    r"\bplaceholder\b",
    r"^\s*\.\.\.+\s*$",  # Just dots
    r"^\s*-+\s*$",  # Just dashes
]

# English language indicators (common words that appear in most English job postings)
ENGLISH_INDICATORS = [
    "experience",
    "required",
    "responsibilities",
    "qualifications",
    "skills",
    "position",
    "opportunity",
    "team",
    "company",
    "work",
    "role",
    "job",
    "candidate",
    "develop",
    "manage",
    "support",
    "project",
    "business",
    "knowledge",
    "ability",
    "strong",
    "excellent",
    "professional",
    # FIX FN-5: Added more common English words for better detection
    "requirements",
    "about",
    "years",
    "looking",
    "join",
    "working",
    "data",
    "analysis",
    "engineer",
    "analyst",
    "will",
    "must",
    "have",
]

# Non-English indicators - common words in other languages that indicate non-English content
# If multiple of these are found, the job is likely NOT in English
NON_ENGLISH_INDICATORS = {
    # German
    "german": ["erfahrung", "anforderungen", "aufgaben", "kenntnisse", "stellenbeschreibung",
               "arbeit", "bewerben", "unternehmen", "mindestens", "wünschenswert", "deutsch",
               "arbeiten", "verantwortung", "berufserfahrung", "qualifikationen"],
    # French
    "french": ["expérience", "responsabilités", "compétences", "poste", "entreprise",
               "travail", "années", "candidat", "développement", "équipe", "français",
               "recherchons", "profil", "missions", "rejoindre"],
    # Spanish
    "spanish": ["experiencia", "requisitos", "responsabilidades", "conocimientos", "puesto",
                "empresa", "trabajo", "años", "candidato", "desarrollo", "español",
                "habilidades", "funciones", "buscamos", "equipo"],
    # Portuguese
    "portuguese": ["experiência", "requisitos", "responsabilidades", "conhecimentos", "vaga",
                   "empresa", "trabalho", "anos", "candidato", "desenvolvimento", "português",
                   "habilidades", "atividades", "procuramos", "equipe"],
    # Italian
    "italian": ["esperienza", "requisiti", "responsabilità", "competenze", "posizione",
                "azienda", "lavoro", "anni", "candidato", "sviluppo", "italiano",
                "cerchiamo", "attività", "ruolo", "sede"],
    # Dutch
    "dutch": ["ervaring", "verantwoordelijkheden", "vaardigheden", "functie", "bedrijf",
              "werk", "jaar", "kandidaat", "ontwikkeling", "team", "nederlands",
              "zoeken", "profiel", "taken", "werken"],
    # Polish
    "polish": ["doświadczenie", "wymagania", "obowiązki", "umiejętności", "stanowisko",
               "firma", "praca", "lat", "kandydat", "rozwój", "polski"],
    # Swedish
    "swedish": ["erfarenhet", "krav", "ansvar", "kompetens", "tjänst",
                "företag", "arbete", "år", "kandidat", "utveckling", "svenska"],
    # Chinese (Pinyin patterns)
    "chinese": ["经验", "要求", "职责", "技能", "公司", "工作", "年", "开发", "团队"],
    # Japanese
    "japanese": ["経験", "必須", "業務", "スキル", "会社", "仕事", "年", "開発", "チーム"],
    # Korean
    "korean": ["경험", "요구", "업무", "기술", "회사", "근무", "년", "개발", "팀"],
}


def detect_non_english_language(text: str) -> tuple[bool, str]:
    """
    Detect if text contains significant non-English content.

    Returns:
        (is_non_english, detected_language) - True if non-English detected
    """
    text_lower = text.lower()

    for language, indicators in NON_ENGLISH_INDICATORS.items():
        # Count matches for this language
        matches = sum(1 for word in indicators if word in text_lower)

        # If 3+ indicators from a single language, it's likely that language
        if matches >= 3:
            return True, language

    return False, ""


def is_english_content(text: str, threshold: int | None = None) -> bool:
    """
    Check if text is primarily in English using dual detection:
    1. Positive: Count English indicators
    2. Negative: Detect non-English language patterns

    FIX FN-5: Uses ADAPTIVE threshold based on text length to prevent false negatives.

    Args:
        text: Text to check
        threshold: Minimum English indicators (None = auto-calculate based on length)

    Returns:
        True if text appears to be English, False otherwise
    """
    if not text or len(text) < 50:
        return False

    text_lower = text.lower()
    text_len = len(text)

    # STEP 1: Check for non-English language patterns (fast rejection)
    is_non_english, detected_lang = detect_non_english_language(text_lower)
    if is_non_english:
        logger.debug(f"Non-English detected: {detected_lang}")
        return False

    # STEP 2: FIX FN-5: Adaptive threshold based on description length
    # Shorter descriptions need fewer indicators to be considered English
    if threshold is None:
        if text_len < 200:
            threshold = 2  # Short descriptions: 2 indicators
        elif text_len < 500:
            threshold = 3  # Medium descriptions: 3 indicators
        elif text_len < 1000:
            threshold = 4  # Long descriptions: 4 indicators
        else:
            threshold = 5  # Very long descriptions: 5 indicators

    # STEP 3: Count English indicators
    english_count = sum(1 for indicator in ENGLISH_INDICATORS if indicator in text_lower)

    return english_count >= threshold


class JobValidator:
    """Validates job detail data for quality and completeness"""

    def __init__(self, min_description_length: int = 50, max_skills: int = 50):
        self.min_description_length = min_description_length
        self.max_skills = max_skills

    def validate_job(self, job: JobDetailModel) -> Tuple[bool, str]:
        """Validate single job - returns (is_valid, reason)"""

        # Check 0: English language only (reject non-English jobs)
        # FIX FN-5: Use adaptive threshold (None = auto-calculate based on text length)
        if job.job_description:
            is_non_english, detected_lang = detect_non_english_language(job.job_description.lower())
            if is_non_english:
                return False, f"Non-English content detected ({detected_lang})"
            if not is_english_content(job.job_description):
                return False, "Non-English content (insufficient English indicators)"

        # Check 1: Required fields present
        if not job.actual_role or not job.company_name:
            return False, "Missing required fields (actual_role/company_name)"

        # Check 2: Description quality
        if (
            not job.job_description
            or len(job.job_description) < self.min_description_length
        ):
            return (
                False,
                f"Description too short (min {self.min_description_length} chars)",
            )

        # Check 2a: Placeholder content detection
        desc_lower = job.job_description.lower()
        for pattern in PLACEHOLDER_PATTERNS:
            if re.search(pattern, desc_lower, re.IGNORECASE):
                return False, "Placeholder/test content detected in description"

        # Check 2b: Title placeholder detection
        if job.actual_role:
            title_lower = job.actual_role.lower()
            for pattern in PLACEHOLDER_PATTERNS:
                if re.search(pattern, title_lower, re.IGNORECASE):
                    return False, "Placeholder/test content detected in title"

        # Check 3: URL validity
        if not job.url or not job.url.startswith("https://"):
            return False, "Invalid URL format"

        # Check 4: Skills extraction (flexible - allow 0 skills for manual review)
        skills = job.skills.split(",") if job.skills else []
        if len(skills) > self.max_skills:
            return False, f"Excessive skills ({len(skills)})"

        # Check 5: Job ID validity (alphanumeric + dashes/underscores/percent for URL encoding, min 5 chars)
        if not job.job_id or len(job.job_id) < 5:
            return False, "Invalid job ID (too short)"

        # Check for valid characters (letters, numbers, dashes, underscores, percent for URL-encoded chars)
        if not re.match(r"^[\w\-%]+$", job.job_id):
            return False, "Invalid job ID format (invalid characters)"

        # All checks passed
        return True, "Valid job"

    def batch_validate(
        self, jobs: list[JobDetailModel]
    ) -> Tuple[list[JobDetailModel], list[dict[str, str]]]:
        """Validate batch of jobs - returns (valid_jobs, rejected_jobs)"""
        valid_jobs: list[JobDetailModel] = []
        rejected_jobs: list[dict[str, str]] = []

        for idx, job in enumerate(jobs, 1):
            is_valid, reason = self.validate_job(job)

            if is_valid:
                valid_jobs.append(job)
                logger.info(f"✅ Job {idx}: VALID")
            else:
                rejected_jobs.append(
                    {
                        "job_id": job.job_id,
                        "job_title": job.actual_role or "Unknown",
                        "company": job.company_name or "Unknown",
                        "reason": reason,
                    }
                )
                logger.warning(msg=f"❌ Job {idx}: REJECTED - {reason}")

        logger.info(
            f"📊 Validation: {len(valid_jobs)} valid, {len(rejected_jobs)} rejected"
        )
        logger.info(
            f"📊 Validation: {len(valid_jobs)} valid, {len(rejected_jobs)} rejected"
        )
        return valid_jobs, rejected_jobs
