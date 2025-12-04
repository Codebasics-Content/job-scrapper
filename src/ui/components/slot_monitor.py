# Slot Monitor Component - Real-time Per-Slot Logging
# Provides transparency into what each browser slot is doing

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal, Mapping, Union

import streamlit as st


@dataclass
class SlotLog:
    """Single log entry for a slot"""
    timestamp: datetime
    action: str
    details: str
    status: Literal["info", "success", "warning", "error"]


@dataclass
class SlotState:
    """State tracking for a single slot"""
    slot_id: int
    status: Literal["idle", "working", "done", "error"] = "idle"
    current_job_id: str = ""
    current_url: str = ""
    jobs_processed: int = 0
    jobs_success: int = 0
    jobs_failed: int = 0
    logs: list[SlotLog] = field(default_factory=list)
    last_error: str = ""

    def add_log(self, action: str, details: str, status: Literal["info", "success", "warning", "error"] = "info"):
        """Add a log entry (keeps last 5 logs)"""
        self.logs.append(SlotLog(
            timestamp=datetime.now(),
            action=action,
            details=details,
            status=status
        ))
        # Keep only last 5 logs per slot
        if len(self.logs) > 5:
            self.logs = self.logs[-5:]


class SlotMonitor:
    """Manages and displays per-slot monitoring using st.empty() for real-time updates"""

    def __init__(self, num_slots: int):
        self.num_slots = num_slots
        self.slots: dict[int, SlotState] = {
            i: SlotState(slot_id=i) for i in range(num_slots)
        }
        # Use st.empty() placeholders for real-time updates (not containers!)
        self.slot_placeholders: dict[int, st.delta_generator.DeltaGenerator] = {}
        # Global alert placeholder for deadlock warnings
        self.alert_placeholder: st.delta_generator.DeltaGenerator | None = None

    def setup_ui(self) -> None:
        """Create the slot monitor UI layout with st.empty() placeholders"""
        st.markdown("### Slot Activity Monitor")

        # Alert placeholder for deadlock warnings (at top)
        self.alert_placeholder = st.empty()

        # Create columns based on number of slots (max 5 per row)
        slots_per_row = min(5, self.num_slots)
        rows_needed = (self.num_slots + slots_per_row - 1) // slots_per_row

        slot_idx = 0
        for _ in range(rows_needed):
            cols = st.columns(slots_per_row)
            for _, col in enumerate(cols):
                if slot_idx < self.num_slots:
                    with col:
                        # Use st.empty() for each slot - allows replacing content
                        self.slot_placeholders[slot_idx] = st.empty()
                        self._render_slot(slot_idx)
                    slot_idx += 1

    def _render_slot(self, slot_id: int) -> None:
        """Render a single slot's status card using placeholder.container()"""
        slot = self.slots[slot_id]
        placeholder = self.slot_placeholders.get(slot_id)

        if not placeholder:
            return

        # Use placeholder.container() to replace all content at once
        with placeholder.container():
            # Status indicator and header
            status_icons = {
                "idle": "⚪",
                "working": "🟡",
                "done": "🟢",
                "error": "🔴"
            }
            icon = status_icons.get(slot.status, "⚪")

            # Slot header with stats
            st.markdown(f"**{icon} Slot {slot_id}**")
            st.caption(f"✅ {slot.jobs_success} | ❌ {slot.jobs_failed} | 📊 {slot.jobs_processed}")

            # Current job info
            if slot.status == "working" and slot.current_job_id:
                job_display = slot.current_job_id[:15] + "..." if len(slot.current_job_id) > 15 else slot.current_job_id
                st.info(f"🔄 {job_display}")
            elif slot.status == "error" and slot.last_error:
                st.error(f"⚠️ {slot.last_error[:30]}")
            elif slot.status == "done":
                st.success("✓ Ready")
            else:
                st.markdown("_Idle_")

            # Recent logs - simplified display (no expander for better real-time updates)
            if slot.logs:
                st.caption("**Recent:**")
                for log in reversed(slot.logs[-2:]):  # Show last 2 only
                    time_str = log.timestamp.strftime("%H:%M:%S")
                    log_text = f"`{time_str}` {log.action}"
                    if log.status == "error":
                        st.markdown(f"🔴 {log_text}")
                    elif log.status == "warning":
                        st.markdown(f"🟠 {log_text}")
                    elif log.status == "success":
                        st.markdown(f"🟢 {log_text}")
                    else:
                        st.markdown(f"⚪ {log_text}")

    def update_from_event(self, event: Mapping[str, Union[str, int, float, bool, None, dict[str, int]]]) -> None:
        """Update slot state from a progress event"""
        event_type = event.get("event", "")
        slot_id = event.get("slot_id")

        # Handle global events FIRST (before slot_id check)
        if event_type == "deadlock_warning":
            # This is a global event - show alert and log to all busy slots
            message = str(event.get("message", "Potential deadlock"))[:30]
            if self.alert_placeholder:
                self.alert_placeholder.error(f"⚠️ **DEADLOCK WARNING**: {message}")
            for s in self.slots.values():
                if s.status == "working":
                    s.add_log("Deadlock", message, "error")
            # Re-render all slots
            for sid in self.slots:
                self._render_slot(sid)
            return

        # For slot-specific events, check slot_id
        if not isinstance(slot_id, int) or slot_id not in self.slots:
            return

        slot = self.slots[slot_id]

        if event_type == "slot_navigate":
            slot.status = "working"
            slot.current_job_id = str(event.get("job_id", ""))[:20]
            slot.current_url = str(event.get("url", ""))
            slot.add_log("Navigate", f"Loading {slot.current_job_id}", "info")

        elif event_type == "slot_extracting":
            slot.add_log("Extract", "Parsing job details", "info")

        elif event_type == "slot_success":
            slot.status = "done"
            slot.jobs_processed += 1
            slot.jobs_success += 1
            company = str(event.get("company", "Unknown"))[:20]
            slot.add_log("Success", f"Scraped: {company}", "success")
            slot.current_job_id = ""
            slot.last_error = ""

        elif event_type == "slot_expired":
            slot.status = "done"
            slot.jobs_processed += 1
            reason = str(event.get("reason", "Expired"))[:30]
            slot.add_log("Expired", reason, "warning")
            slot.current_job_id = ""

        elif event_type == "slot_error":
            slot.status = "error"
            slot.jobs_processed += 1
            slot.jobs_failed += 1
            error = str(event.get("error", "Unknown error"))[:50]
            slot.last_error = error
            slot.add_log("Error", error, "error")
            slot.current_job_id = ""

        elif event_type == "slot_authwall":
            slot.status = "error"
            slot.jobs_processed += 1
            slot.jobs_failed += 1
            slot.last_error = "Authwall/Login redirect"
            slot.add_log("Authwall", "Login page detected", "error")
            slot.current_job_id = ""

        elif event_type == "slot_timeout":
            slot.status = "error"
            slot.jobs_processed += 1
            slot.jobs_failed += 1
            timeout_sec = event.get("timeout", 15)
            slot.last_error = f"Timeout ({timeout_sec}s)"
            slot.add_log("Timeout", f"Exceeded {timeout_sec}s limit", "error")
            slot.current_job_id = ""

        elif event_type == "slot_reset":
            slot.status = "idle"
            slot.current_job_id = ""
            slot.add_log("Reset", "Slot cleared for next job", "info")

        elif event_type == "slot_idle":
            slot.status = "idle"
            slot.current_job_id = ""
            slot.add_log("Idle", "Slot ready for next job", "info")

        elif event_type == "slot_warning":
            # Slow task warning (10s elapsed)
            elapsed = event.get("elapsed", 0)
            slot.add_log("Warning", f"Slow task - {elapsed:.0f}s", "warning")

        # Note: deadlock_warning is handled at the top of this method (global event)

        elif event_type == "job_dispatch":
            # Also handle the existing job_dispatch event
            slot.status = "working"
            slot.current_job_id = str(event.get("job_id", ""))[:20]
            slot.add_log("Dispatch", "Job assigned", "info")

        elif event_type == "job_complete":
            status = event.get("status", "unknown")
            slot.jobs_processed += 1

            if status == "success":
                slot.status = "done"
                slot.jobs_success += 1
                company = str(event.get("company", ""))[:20]
                slot.add_log("Complete", f"Success: {company}", "success")
            elif status == "expired":
                slot.status = "done"
                error = str(event.get("error", "Expired"))[:30]
                slot.add_log("Complete", f"Expired: {error}", "warning")
            else:
                slot.status = "error"
                slot.jobs_failed += 1
                error = str(event.get("error", "Failed"))[:30]
                slot.last_error = error
                slot.add_log("Complete", f"Failed: {error}", "error")

            slot.current_job_id = ""

        # Re-render the slot (slot_id is already validated as int at line 152)
        self._render_slot(slot_id)

    def refresh_all(self) -> None:
        """Refresh all slot displays"""
        for slot_id in range(self.num_slots):
            self._render_slot(slot_id)


def create_slot_monitor(num_slots: int) -> SlotMonitor:
    """Factory function to create a slot monitor"""
    monitor = SlotMonitor(num_slots)
    monitor.setup_ui()
    return monitor
