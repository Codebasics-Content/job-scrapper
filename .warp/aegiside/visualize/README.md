# AegisIDE Memory Bank Visualization Dashboard

## Quick Start Guide (5-Minute Setup)

### Step 1: Navigate to Project Root
```bash
cd /path/to/your/project/src/.aegiside
# The memory-bank and visualize directories are located here
```

### Step 2: Start Local Server
```bash
# Option 1: Using Python (Recommended)
python3 -m http.server 7777

# Option 2: Using Node.js http-server
npx http-server -p 7777 -c-1 --cors
```
**Note**: Press **CTRL+C** to stop the server. Python's HTTP server handles the interrupt signal gracefully.

### Step 3: Open Dashboard
Open browser and navigate to:
```
http://localhost:7777/visualize/dashboard.html
```
**Important**: The dashboard file is located at `src/.aegiside/visualize/dashboard.html`

## Dashboard Overview (v2.8.8)

### Real-Time AI Memory Bank Frontend

**Enhanced UI/UX (v2.8.0)**:
- Professional dark theme optimized for developer productivity
- Full content visibility with removed scroll constraints
- Improved typography with enhanced text sizing (text-sm) for better readability
- Clean interface with eliminated visual distractions and animations

**Live Metrics**:
- Real-time project progress tracking
- Dynamic task completion status
- Active bug monitoring with root cause analysis
- Comprehensive event timeline

**Optimized Performance**:
- Auto-refresh every 5 minutes (optimal balance)
- Intelligent memory bank synchronization
- Constitutional compliance monitoring
- Zero-interruption AI agent tracking

### Dashboard Sections (Minimal 8-Schema)

#### Header Section
- **Title**: Current project name and phase
- **Refresh Button**: Manual refresh of all JSON files
- **Auto-Refresh Toggle**: Enable/disable 5-minute auto-updates (optimized)
- **Last Update Time**: Timestamp of most recent data load

#### Phase Overview Cards (4 Cards)
1. **Current Phase**: Phase name and description
2. **Progress**: Percentage complete with progress bar
3. **Pending Tasks**: Count of TODO items
4. **Completed**: Count of finished tasks

#### Content Sections
- **Kanban Snapshot**: Renders `kanban.json` content in compact card format
- **Quality & Patterns**: Displays `mistakes.json` and `systemPatterns.json` in JSON cards
- **Current Activity**: Shows `activeContext.json` and `scratchpad.json` in JSON cards
- **Strategy**: Presents `progress.json` and `roadmap.json` JSON cards

### Visualized JSON Files (8 Essential Memory-Bank Files)

- `activeContext.json` - Current implementation status
- `scratchpad.json` - Priority task queue
- `mistakes.json` - Error patterns and resolutions
- `progress.json` - Milestone tracking
- `systemPatterns.json` - Architecture patterns
- `roadmap.json` - Strategic planning
- `kanban.json` - Task workflow
- `memory.json` - Knowledge graph storage

## Constitutional Compliance

Per Articles I-XIV of the AegisIDE Constitutional Framework (max 12,000 characters each):

**Article III - Context-Engineered Development**:
- 8-schema architecture with tiered updates
- Event-driven context management
- Real-time dashboard synchronization

**Article VII - Autonomous Operations**:
- 98% autonomous execution
- Self-management without interruption
- Continuous task chain updates

**Article XI - Mandatory Compliance**:
- Pre-implementation validation
- Post-implementation JSON refresh
- Memory-bank health monitoring

**Article XIII - Multi-Language Validation**:
- Zero tolerance error resolution
- Integration test results tracking
- Validation status visualization

## Dashboard Controls & Usage

### Manual Refresh
Click **🔄 Refresh** button to immediately reload all JSON files.

### Auto-Refresh
- Click **⏱️ Auto: OFF** to enable (changes to **Auto: ON (5m)**)
- Dashboard auto-refreshes every 5 minutes (optimized performance)
- Click again to disable

### Task Interaction
- Click task cards to view details (future enhancement)
- Hover over tasks for tooltips (future enhancement)

## Real-Time Usage & Synchronization

The dashboard automatically reflects changes when:
- AI agents update JSON files
- Tasks are completed
- New bugs are detected
- Progress milestones are reached
- Events are logged

### Typical Workflow
1. **AI starts task** → `activeContext.json` updated → Dashboard shows in "In Progress"
2. **Task completed** → `kanban.json` updated → Card moves to "Done" column
3. **Bug detected** → `mistakes.json` updated → Appears in "Active Issues"
4. **Fix implemented** → Bug removed from dashboard

### Technical Implementation
The dashboard automatically detects JSON file changes via:
1. **5-minute polling** - Optimized refresh interval for performance
2. **Fetch API** - Intelligent JSON loading with error handling
3. **Component re-render** - Seamless UI updates without scroll loss
4. **State preservation** - Maintains user interactions and view state

**AI Agent Integration**:
- When AI completes a task → `kanban.json` updated → Dashboard shows in Task Management
- When progress made → `progress.json`/`roadmap.json` updated → Overview recalculated

## Technical Stack & Performance

### Technology
- **Tailwind CSS** (CDN) - Utility-first styling
- **Vanilla JavaScript** - Zero dependencies

### Performance Metrics
- Load time: <200ms for all 8 JSON files (optimized)
- Memory usage: <40MB browser memory (reduced)
- Refresh rate: 5 minutes (performance optimized)
- File size limit: ≤10KB per JSON (constitutional requirement)

### Performance Tips
- **Keep JSON files ≤10KB**: Constitutional requirement, ensures fast loading
- **Use auto-refresh wisely**: Disable when not actively monitoring
- **Close unused browser tabs**: Reduces memory usage
- **Use modern browser**: Chrome, Firefox, Edge for best performance

## Troubleshooting & Common Issues

### Dashboard Issues
**Dashboard not loading**:
- Verify HTTP server running: `ps aux | grep "python3 -m http.server"`
- Check port 7777 is not in use by another service
- Ensure you're in the correct directory

**JSON data not updating**:
- Check if auto-refresh is enabled
- Manually click refresh button
- Verify JSON files have valid syntax
- Check browser console for errors

**External CDN blocked**:
- Tailwind CDN required for styling. If blocked, inline minimal CSS.

**Performance is slow**:
- Reduce refresh interval
- Check JSON file sizes (should be ≤10KB each)
- Close other resource-intensive applications

### Advanced Configuration
Edit `dashboard.html` to:
- Add new visualization sections
- Modify refresh interval (default: 300000ms = 5 minutes)
- Change color schemes (Tailwind classes)
- Include additional metrics

## Integration with Development Workflow

### Recommended Setup
1. **Keep dashboard open while coding** - Monitor AI agent progress in real-time
2. **Use dual monitors** - Code on one, dashboard on the other
3. **Enable auto-refresh during active development** - See changes immediately
4. **Bookmark the URL** - Quick access: `http://localhost:7777/visualize/dashboard.html`
5. **Check events timeline** - Understand what AI is doing and why

### Constitutional Framework Integration
The dashboard reflects:
- **Article III**: 8-schema architecture and tiered updates
- **Article VII**: Autonomous operations tracking
- **Article XI**: Compliance indicators

### Security Notes
- Dashboard runs locally only (no external data transmission)
- Read-only access to JSON files
- CORS-safe with local HTTP server
- No authentication required (local development only)

## Support & Additional Resources

### Documentation
- **Schema Documentation**: `src/.aegiside/schemas/README.md`
- **Constitutional Framework**: `src/rules/constitution/`
- **Memory Bank Structure**: `src/.aegiside/memory-bank/README.md`
- **Workflow Documentation**: `src/workflow/`

### Getting Help
For issues or questions:
1. Check troubleshooting section above
2. Review Constitutional Framework articles
3. Check browser console for error messages
4. Verify JSON file syntax and structure

## License

Part of AegisIDE Framework - Governed by AegisIDE Constitutional Framework (v2.8.8)
