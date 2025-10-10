# Quick Start Guide - AegisIDE Memory Bank Dashboard (v2.8.5)

## 5-Minute Setup

### Step 1: Navigate to Memory Bank
```bash
cd .windsurf/memory-bank
# or
cd .cursor/memory-bank  # for Cursor IDE
```

### Step 2: Start Local Server
```bash
python3 -m http.server 7777
```
**Note**: Press **CTRL+C** to stop the server. Python's HTTP server handles the interrupt signal gracefully.

### Step 3: Open Dashboard
Open browser and navigate to:
```
http://localhost:7777/visualize/dashboard.html
```
**Important**: The dashboard file is located at `.windsurf/memory-bank/visualize/dashboard.html`

## Dashboard Overview (Minimal 8-Schema)

### Header Section
- **Title**: Current project name and phase
- **Refresh Button**: Manual refresh of all JSON files
- **Auto-Refresh Toggle**: Enable/disable 5-minute auto-updates (optimized)
- **Last Update Time**: Timestamp of most recent data load

### Enhanced User Experience (v2.8.0)
- **Professional Dark Theme**: Optimized for developer productivity
- **Full Content Visibility**: Removed scroll constraints for better information access
- **Improved Typography**: Enhanced text sizing (text-sm) for better readability
- **Clean Interface**: Eliminated visual distractions and animations

### Phase Overview Cards (4 Cards)
1. **Current Phase**: Phase name and description
2. **Progress**: Percentage complete with progress bar
3. **Pending Tasks**: Count of TODO items
4. **Completed**: Count of finished tasks

### Kanban Snapshot
- Renders `kanban.json` content in a compact card (no heavy JS components)

### Quality & Patterns
- Renders `mistakes.json` and `systemPatterns.json` in JSON cards

### Current Activity
- `activeContext.json` and `scratchpad.json` in JSON cards

### Strategy
- `progress.json` and `roadmap.json` JSON cards

## Controls

### Manual Refresh
Click **🔄 Refresh** button to immediately reload all JSON files.

### Auto-Refresh
- Click **⏱️ Auto: OFF** to enable (changes to **Auto: ON (5m)**)
- Dashboard auto-refreshes every 5 minutes (optimized performance)
- Click again to disable

### Task Interaction
- Click task cards to view details (future enhancement)
- Hover over tasks for tooltips (future enhancement)

## Real-Time Usage

The dashboard automatically reflects changes when:
- AI agents update JSON files
- Tasks are completed
- New bugs are detected
- Progress milestones are reached
- Events are logged

### Typical Workflow
1. **AI starts task** → `activeContext.json` updated → Dashboard shows in "In Progress"
2. **Task completed** → `kanban.json` updated → Card moves to "Done" column
3. **Bug detected** → `bugfix.json` updated → Appears in "Active Issues"
4. **Fix implemented** → Bug removed from dashboard

## Supported JSON Files

The dashboard visualizes the 8 essential memory-bank JSON files:
- activeContext.json, scratchpad.json, mistakes.json, progress.json, systemPatterns.json, roadmap.json, kanban.json, memory.json

## Advanced Usage

- To change the 5-minute auto-refresh, edit the `toggleAuto()`/`startAutoRefresh()` intervals in `dashboard.html`.
- Tailwind classes in the HTML control color/themes.

## Performance Tips

- **Keep JSON files ≤10KB**: Constitutional requirement, ensures fast loading
- **Use auto-refresh wisely**: Disable when not actively monitoring
- **Close unused browser tabs**: Reduces memory usage
- **Use modern browser**: Chrome, Firefox, Edge for best performance

## Common Issues

**Dashboard shows "Failed to load"**:
- Verify HTTP server is running: `ps aux | grep "python3 -m http.server"`
- Check port 7777 is not in use by another service
- Ensure you're in the correct directory

**JSON data not updating**:
- Check if auto-refresh is enabled
- Manually click refresh button
- Verify JSON files have valid syntax
- Check browser console for errors

**External CDN blocked?**:
- Tailwind CDN required for styling. If blocked, inline minimal CSS.

**Performance is slow**:
- Reduce refresh interval
- Check JSON file sizes (should be ≤10KB each)
- Close other resource-intensive applications

## Constitutional Framework Integration

The dashboard reflects:
- **Article III**: 8-schema architecture and tiered updates
- **Article VII**: Autonomous operations tracking
- **Article XI**: Compliance indicators

## Security Notes

- Dashboard runs locally only (no external data transmission)
- Read-only access to JSON files
- CORS-safe with local HTTP server
- No authentication required (local development only)

## Additional Resources

- Main README: `core/visualize/README.md`
- Constitutional Framework: `core/constitution/`
- Memory Bank Structure: `.windsurf/memory-bank/schemas/`
- AegisIDE Documentation: `docs/`

## Tips & Tricks

1. **Keep dashboard open while coding** - Monitor AI agent progress in real-time
2. **Use dual monitors** - Code on one, dashboard on the other
3. **Enable auto-refresh during active development** - See changes immediately
4. **Bookmark the URL** - Quick access: `http://localhost:7777/visualize/dashboard.html`
5. **Check events timeline** - Understand what AI is doing and why

## Support

For issues or questions:
1. Check troubleshooting section in main README
2. Review Constitutional Framework articles
3. Check browser console for error messages
4. Verify JSON file syntax and structure
