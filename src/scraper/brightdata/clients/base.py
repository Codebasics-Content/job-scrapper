from __future__ import annotations
from typing import Any, Dict, Optional
import time
import requests

from ..config.settings import get_settings


class BrightDataBaseClient:
    """Minimal BrightData DCA client with trigger + poll helpers.

    Uses env-driven settings from BrightDataSettings. Keep ≤80 lines per EMD.
    """

    def __init__(self, collector_id: Optional[str] = None) -> None:
        self.settings = get_settings()
        self.collector_id = collector_id
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.settings.api_token}",
            "Content-Type": "application/json",
        })

    def trigger(self, collector_id: Optional[str] = None, args: Optional[Dict[str, Any]] = None) -> str:
        cid = collector_id or self.collector_id
        if not cid:
            raise ValueError("collector_id is required")
        url = f"{self.settings.base_url}{self.settings.trigger_endpoint}"
        payload = {"collectorId": cid, "args": args or {}}
        resp = self.session.post(url, json=payload, timeout=self.settings.timeout_seconds)
        resp.raise_for_status()
        data = resp.json()
        # BrightData responds with an id/response_id depending on collector type
        task_id = data.get("id") or data.get("response_id") or data.get("responseId")
        if not task_id:
            raise RuntimeError(f"Unexpected trigger response: {data}")
        return task_id

    def get_task(self, task_id: str) -> Dict[str, Any]:
        url = f"{self.settings.base_url}{self.settings.task_endpoint}"
        resp = self.session.get(url, params={"id": task_id}, timeout=self.settings.timeout_seconds)
        resp.raise_for_status()
        return resp.json()

    def poll_until_done(self, task_id: str, timeout_s: Optional[int] = None) -> Dict[str, Any]:
        timeout_s = timeout_s or self.settings.timeout_seconds
        interval = max(1.0 / max(self.settings.rate_limit_qps, 0.1), 0.5)
        start = time.time()
        while True:
            task = self.get_task(task_id)
            status = (task.get("status") or task.get("state") or "").lower()
            if status in ("completed", "success", "done"):
                return task
            if status in ("failed", "error"):
                raise RuntimeError(f"Task failed: {task}")
            if time.time() - start > timeout_s:
                raise TimeoutError(f"Polling timed out for task {task_id}")
            time.sleep(interval)
