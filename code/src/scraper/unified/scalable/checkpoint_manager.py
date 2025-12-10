"""Checkpoint manager for crash recovery in long-running scrapes

Enables resuming interrupted 10K+ job scraping sessions without data loss.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import TypedDict

logger = logging.getLogger(__name__)


class CheckpointData(TypedDict):
    """Checkpoint data structure"""
    platform: str
    job_role: str
    last_batch_index: int
    processed_count: int
    failed_count: int
    timestamp: str


class CheckpointManager:
    """Manage checkpoints for crash recovery"""

    def __init__(self, checkpoint_dir: str = ".checkpoints"):
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(exist_ok=True)

    def _get_checkpoint_path(self, platform: str, job_role: str) -> Path:
        """Get checkpoint file path for platform and job role"""
        safe_role = job_role.replace(" ", "_").lower()
        return self.checkpoint_dir / f"{platform}_{safe_role}.json"

    def save_checkpoint(
        self,
        platform: str,
        job_role: str,
        batch_index: int,
        processed: int,
        failed: int,
    ) -> None:
        """Save checkpoint to disk"""
        checkpoint_path = self._get_checkpoint_path(platform, job_role)
        
        data: CheckpointData = {
            "platform": platform,
            "job_role": job_role,
            "last_batch_index": batch_index,
            "processed_count": processed,
            "failed_count": failed,
            "timestamp": datetime.now().isoformat(),
        }
        
        with open(checkpoint_path, "w") as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Checkpoint saved: batch {batch_index}, {processed} processed")

    def load_checkpoint(
        self, platform: str, job_role: str
    ) -> CheckpointData | None:
        """Load checkpoint from disk, returns None if not found"""
        checkpoint_path = self._get_checkpoint_path(platform, job_role)
        
        if not checkpoint_path.exists():
            return None
        
        try:
            with open(checkpoint_path, "r") as f:
                data: CheckpointData = json.load(f)
            logger.info(f"Checkpoint loaded: resuming from batch {data['last_batch_index']}")
            return data
        except Exception as e:
            logger.error(f"Failed to load checkpoint: {e}")
            return None

    def clear_checkpoint(self, platform: str, job_role: str) -> None:
        """Clear checkpoint after successful completion"""
        checkpoint_path = self._get_checkpoint_path(platform, job_role)
        if checkpoint_path.exists():
            checkpoint_path.unlink()
            logger.info("Checkpoint cleared after successful completion")
