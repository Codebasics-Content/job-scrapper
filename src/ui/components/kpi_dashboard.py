"""KPI Dashboard Component - Real-time Scraping Progress Visualization"""

import streamlit as st

from src.db.operations import JobStorageOperations


def render_kpi_dashboard(db_path: str = "data/jobs.db") -> None:
    """Render KPI dashboard showing scraping progress"""

    db_ops = JobStorageOperations(db_path)
    stats = db_ops.get_scraping_stats()

    st.header("📊 Scraping Progress KPIs")

    # Main KPI Metrics Row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="🔗 Total URLs Collected",
            value=f"{stats['total_urls']:,}",
            help="Phase 1: Total job URLs discovered",
        )

    with col2:
        st.metric(
            label="✅ Jobs Scraped",
            value=f"{stats['total_jobs']:,}",
            delta=f"{stats['progress_percent']}% complete",
            help="Phase 2: Jobs with full details extracted",
        )

    with col3:
        st.metric(
            label="⏳ Pending",
            value=f"{stats['urls_pending']:,}",
            delta=f"-{stats['urls_scraped']:,} done"
            if stats["urls_scraped"] > 0
            else None,
            delta_color="inverse",
            help="URLs waiting to be scraped",
        )

    with col4:
        # Progress percentage with color coding
        progress = stats["progress_percent"]
        if progress >= 90:
            status = "🟢"
        elif progress >= 50:
            status = "🟡"
        else:
            status = "🔴"

        st.metric(
            label=f"{status} Overall Progress",
            value=f"{progress}%",
            help="Percentage of URLs scraped",
        )

    # Progress Bar
    st.progress(
        stats["progress_percent"] / 100,
        text=f"Scraping Progress: {stats['urls_scraped']:,} / {stats['total_urls']:,}",
    )

    st.divider()

    # Platform Breakdown
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📱 By Platform")

        if stats["urls_by_platform"]:
            for platform, total in stats["urls_by_platform"].items():
                jobs = stats["jobs_by_platform"].get(platform, 0)
                pending = stats["pending_by_platform"].get(platform, 0)
                progress_pct = round(jobs / total * 100, 1) if total > 0 else 0

                st.markdown(f"**{platform.upper()}**")
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("URLs", f"{total:,}")
                col_b.metric("Done", f"{jobs:,}")
                col_c.metric("Pending", f"{pending:,}")
                st.progress(progress_pct / 100, text=f"{progress_pct}%")
                st.markdown("---")
        else:
            st.info("No data yet. Start scraping to see platform breakdown.")

    with col2:
        st.subheader("🎯 By Target Role")

        if stats["by_role"]:
            for role_data in stats["by_role"][:10]:  # Show top 10 roles
                role = role_data["role"] or "Unknown"
                total = role_data["total"]
                scraped = role_data["scraped"]
                pending = role_data["pending"]
                progress_pct = role_data["progress"]

                # Color code based on progress
                if progress_pct >= 90:
                    icon = "✅"
                elif progress_pct >= 50:
                    icon = "🔄"
                else:
                    icon = "⏳"

                with st.expander(f"{icon} {role} ({scraped}/{total})", expanded=False):
                    col_a, col_b, col_c = st.columns(3)
                    col_a.metric("Total", total)
                    col_b.metric("Scraped", scraped)
                    col_c.metric("Pending", pending)
                    st.progress(progress_pct / 100, text=f"{progress_pct}% complete")
        else:
            st.info("No data yet. Start scraping to see role breakdown.")

    # Refresh button
    st.divider()
    if st.button("🔄 Refresh KPIs", width="stretch"):
        st.rerun()


def render_compact_kpi(db_path: str = "data/jobs.db") -> None:
    """Render compact KPI strip for sidebar or header"""

    db_ops = JobStorageOperations(db_path)
    stats = db_ops.get_scraping_stats()

    # Compact display
    progress = stats["progress_percent"]

    st.markdown(
        f"""
    <div style="background: linear-gradient(90deg, #1a1a2e 0%, #16213e 100%);
                padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="text-align: center;">
                <span style="font-size: 24px; font-weight: bold; color: #00d4ff;">{stats["total_urls"]:,}</span>
                <br><span style="font-size: 12px; color: #888;">URLs</span>
            </div>
            <div style="text-align: center;">
                <span style="font-size: 24px; font-weight: bold; color: #00ff88;">{stats["total_jobs"]:,}</span>
                <br><span style="font-size: 12px; color: #888;">Jobs</span>
            </div>
            <div style="text-align: center;">
                <span style="font-size: 24px; font-weight: bold; color: #ffaa00;">{stats["urls_pending"]:,}</span>
                <br><span style="font-size: 12px; color: #888;">Pending</span>
            </div>
            <div style="text-align: center;">
                <span style="font-size: 24px; font-weight: bold; color: {"#00ff88" if progress >= 90 else "#ffaa00" if progress >= 50 else "#ff4444"};">{progress}%</span>
                <br><span style="font-size: 12px; color: #888;">Progress</span>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
