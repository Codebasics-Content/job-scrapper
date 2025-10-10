from __future__ import annotations
from typing import Any, Dict, List, Optional

from .base import BrightDataBaseClient
from ..config.settings import get_settings


class LinkedInClient(BrightDataBaseClient):
    """LinkedIn jobs client via BrightData DCA.

    Expects a LinkedIn collector configured in BrightData. Arguments are generic
    and passed to the collector as-is.
    """

    def __init__(self, collector_id: Optional[str] = None) -> None:
        settings = get_settings()
        super().__init__(collector_id or settings.linkedin_collector_id)

    def discover_jobs(
        self,
        keyword: str,
        location: Optional[str] = None,
        time_range: Optional[str] = "past_week",
        job_type: Optional[str] = None,
        limit: int = 50,
        extra_args: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        args: Dict[str, Any] = {
            "keyword": keyword,
            "location": location,
            "time_range": time_range,
            "job_type": job_type,
            "limit": limit,
        }
        if extra_args:
            args.update({k: v for k, v in extra_args.items() if v is not None})
        # Remove None values
        args = {k: v for k, v in args.items() if v is not None}

        task_id = self.trigger(args=args)
        task = self.poll_until_done(task_id)
        # Most collectors return a list under a known key; fallback to raw
        return task.get("results") or task.get("data") or task.get("jobs") or []
