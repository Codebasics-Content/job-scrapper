from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Dict, Iterable, List, Set


DEFAULT_SKILLS_PATH = Path(__file__).resolve().parents[3] / "skills_reference_2025.json"


class SkillsParser:
    """Regex-based skills extractor using skills_reference_2025.json.

    Keeps ≤80 lines (EMD). Patterns are compiled once at init.
    """

    def __init__(self, skills_path: Path | None = None) -> None:
        self.skills_path = skills_path or DEFAULT_SKILLS_PATH
        self._pattern_map = self._load_patterns()

    def _load_patterns(self) -> Dict[re.Pattern[str], str]:
        data = json.loads(self.skills_path.read_text(encoding="utf-8"))
        categories = data.get("skills", {})
        compiled: Dict[re.Pattern[str], str] = {}
        for items in categories.values():
            for item in items:
                name = item["name"].strip()
                for pat in item.get("patterns", []):
                    pat_escaped = re.escape(pat.strip())
                    regex = re.compile(rf"\b{pat_escaped}\b", re.IGNORECASE)
                    compiled[regex] = name
        return compiled

    def extract_from_text(self, text: str) -> List[str]:
        found: Set[str] = set()
        for rx, name in self._pattern_map.items():
            if rx.search(text):
                found.add(name)
        return sorted(found)

    def extract_from_job(self, job: Dict) -> List[str]:
        parts: List[str] = []
        for key in ("description", "job_description", "title", "job_title"):
            val = job.get(key)
            if isinstance(val, str):
                parts.append(val)
        return self.extract_from_text("\n".join(parts))
