# AegisIDE Memory Bank Visualization Dashboard

## Quick Access

```bash
# From project root
cd .windsurf/memory-bank  # or .cursor/memory-bank for Cursor IDE
npx http-server -p 7777 -c-1 --cors

# Open: http://localhost:7777/visualize/dashboard.html
```

## Dashboard Features (v2.8.4)

### Real-Time AI Memory Bank Frontend

**Enhanced UI/UX**:
- Professional dark theme with optimized visibility
- Removed scroll constraints for full content display
- Improved text sizing (text-sm) for better readability
- Clean, modern interface without visual distractions

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

### Visualized JSON Files (7 Total)

- `activeContext.json` - Current implementation status
- `scratchpad.json` - Priority task queue
- `mistakes.json` - Error patterns and resolutions
- `progress.json` - Milestone tracking
- `systemPatterns.json` - Architecture patterns
- `roadmap.json` - Strategic planning
- `kanban.json` - Task workflow

## Constitutional Compliance

Per Articles I-XIV of the AegisIDE Constitutional Framework (max 12,000 characters each):

**Article III - Context-Engineered Development**:
- 7-schema architecture with tiered updates
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

## Dashboard Sections (Minimal)

- **Overview Cards**: quick stats (Active Tasks, Completed, Issues, Schema Health)
- **Current Activity**: `activeContext.json`, `scratchpad.json`
- **Task Management**: `kanban.json`
- **Progress & Strategy**: `progress.json`, `roadmap.json`
- **Quality & Patterns**: `mistakes.json`, `systemPatterns.json`

## Real-Time Synchronization

The dashboard automatically detects JSON file changes via:
1. **5-minute polling** - Optimized refresh interval for performance
2. **Fetch API** - Intelligent JSON loading with error handling
3. **Component re-render** - Seamless UI updates without scroll loss
4. **State preservation** - Maintains user interactions and view state

**AI Agent Integration**:
- When AI completes a task → `kanban.json` updated → Dashboard shows in Task Management
- When progress made → `progress.json`/`roadmap.json` updated → Overview recalculated

## Technical Stack

- **Tailwind CSS** (CDN) - Utility-first styling
- **Vanilla JavaScript** - Zero dependencies

## Performance

- Load time: <200ms for all 7 JSON files (optimized)
- Memory usage: <40MB browser memory (reduced)
- Refresh rate: 5 minutes (performance optimized)
- File size limit: ≤10KB per JSON (constitutional requirement)

## Customization

Edit `dashboard.html` to:
- Add new visualization sections
- Modify refresh interval (default: 300000ms = 5 minutes)
- Change color schemes (Tailwind classes)
- Add custom Mermaid diagrams
- Include additional metrics

## Troubleshooting

**Dashboard not loading**:
- Verify HTTP server running: `ps aux | grep http.server`
- Check port 8080 availability
- Ensure correct directory: `.windsurf/memory-bank`

**JSON not updating**:
- Enable auto-refresh toggle
- Check browser console for errors
- Verify JSON file syntax validity
- Confirm file paths are correct

**Mermaid diagrams missing**:
- Check internet connection (CDN access)
- Review browser console for Mermaid.js errors
- Verify diagram syntax correctness

## Project-Specific Insights

> Project-specific examples removed to keep docs generic and minimal.

## Integration with Development Workflow

**Recommended Setup**:
1. Keep dashboard open on secondary monitor
2. Enable auto-refresh during active development
3. Monitor event timeline for AI agent activities
4. Check active issues before starting new tasks
5. Review completed tasks for learning patterns

**Constitutional Framework Alignment**:
- Real-time visibility into autonomous operations
- Transparent tri-branch decision tracking
- Continuous progress monitoring

## License

Part of ServeUPSC Rust Backend - Governed by AegisIDE Constitutional Framework
