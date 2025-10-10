from __future__ import annotations
from typing import Any, Dict, List, Optional

from .base import BrightDataBaseClient
from ..config.settings import get_settings


class IndeedClient(BrightDataBaseClient):
    """Indeed jobs client via BrightData DCA.

    Provide a collector configured to search/query Indeed.
    """

    def __init__(self, collector_id: Optional[str] = None) -> None:
        settings = get_settings()
        super().__init__(collector_id or settings.indeed_collector_id)

    def discover_jobs(
        self,
        query: str,
        location: Optional[str] = None,
        days_back: Optional[int] = 7,
        limit: int = 50,
        extra_args: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        args: Dict[str, Any] = {
            "query": query,
            "location": location,
            "days_back": days_back,
            "limit": limit,
        }
        if extra_args:
            args.update({k: v for k, v in extra_args.items() if v is not None})
        args = {k: v for k, v in args.items() if v is not None}

        task_id = self.trigger(args=args)
        task = self.poll_until_done(task_id)
        return task.get("results") or task.get("data") or task.get("jobs") or []
