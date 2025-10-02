---
trigger: always_on
---

# Preamble

We, the Autonomous AI Development System, establish this Constitutional Framework to ensure efficient, high-quality, and client-aligned software development through structured governance, continuous autonomous operations, and unwavering commitment to actual client requirements as defined in roadmap.md.

---

## Article X: Integration and Interoperability

### Integration Authority
Tri-branch oversight with >95% consensus required for all system integrations.

### MCP Integration Standards (9 Servers - 2024)
**Real-Time Research & Documentation**:
- **@mcp:context7**: Official documentation lookup (auto-call on ANY error)
- **@mcp:fetch**: Web content retrieval for latest best practices
- **@mcp:time**: Temporal awareness (current time, timezone conversions, date operations)
- **@mcp:math**: Mathematical calculations, conversions, evaluations

**File & Version Control**:
- **@mcp:filesystem**: Project file access (read, write, list directories)
- **@mcp:git**: Version control, repository status, commit tracking

**Knowledge & Reasoning** (Dual Storage Strategy):
- **@mcp:memory**: Offline knowledge graph (unlimited, local, primary storage)
- **@mcp:byterover-mcp**: Cloud knowledge storage (free tier limits, fallback/sharing)
- **@mcp:sequential-thinking**: Multi-step problem decomposition and reasoning

**Autonomous Usage** (0-98% autonomy):
All 9 MCP servers auto-called WITHOUT user prompting based on task requirements

**Dual Knowledge Storage Protocol**:
- **Primary**: Use @mcp:memory for frequent pattern storage (unlimited, local)
- **Fallback**: Use @mcp:byterover-mcp when sharing across projects (free tier monthly limits)
- **Strategy**: Store all patterns in memory first, sync to byterover for cross-project access
- **Benefit**: Avoid hitting Byterover free tier limits while maintaining cloud backup

**Real-Time Awareness Protocol**:
- Use @mcp:time for temporal context (deadlines, timestamps, schedules)
- Use @mcp:fetch + @mcp:context7 for latest documentation/best practices
- Use @mcp:math for calculations, data analysis, metric computations
- Use @mcp:filesystem for direct project file operations

### Cross-Platform Integration
- **Data Flow**: Seamless context sharing across Windows, Linux, macOS
- **Command Mapping**: Platform-specific command translation with safety validation
- **Error Resolution**: Platform-aware @mcp:context7 documentation retrieval

### Cross-Language Integration
- **Rust**: Cargo ecosystem integration with context7 error resolution
- **JavaScript/TypeScript**: NPM/PNPM integration with auto-linting
- **Python**: Pip/Poetry integration with pytest validation
- **Go**: Go modules integration with build validation
- **Framework Compliance**: All languages follow EMD ≤10,000 characters standard

### MCP Security & Reliability
- All MCP calls logged in systemPatterns.md
- Failed MCP calls trigger fallback to manual research
- MCP response validation before implementation
- Temporal tracking via @mcp:time for audit trails
- Memory MCP provides offline fallback when cloud services unavailable
