# AegisIDE JSON Schema Library

## Overview

The AegisIDE schemas directory contains the JSON schema definitions that validate and structure the 8 essential memory-bank files plus helper schemas for enhanced functionality. This comprehensive schema system ensures data integrity, cross-file referencing, and constitutional compliance across all AI governance operations.

## Essential Memory-Bank Schemas (8 Core Files)

### 1. `activeContext.schema.json`
**Purpose**: Validates `activeContext.json` - Real-time execution state with session management, MCP integration tracking, and event streams.

**Schema Structure:**
- **Required Fields**: `schema_version`, `last_updated`, `current_implementation`, `ai_state`, `session_management`, `mcp_integration`
- **Key Components**:
  - `current_implementation`: Active task tracking with progress percentages and phase management
  - `event_tracking`: Array of up to 100 events with MCP integration status
  - `current_context`: Working files, connections, processes, and memory references
  - `ai_state`: Current minister assignment and checkpoint status
  - `session_management`: IDE type, workspace path, and connection timestamps
  - `linkage`: Cross-file identifiers linking to proposals, tasks, milestones, and decisions
  - `mcp_integration`: Mandatory MCP server status and anti-hallucination tracking

**Validation Rules:**
- Progress percentage: 0-100
- Phase enum: ["planning", "implementation", "testing", "review", "deployment"]
- Minister enum: ["project_manager", "dev_minister", "tech_minister", "quality_shadow", "innovation_shadow", "analytics_shadow", "chief_justice"]
- IDE enum: ["claude_desktop", "windsurf", "vscode", "cursor", "jetbrains"]

### 2. `scratchpad.schema.json`
**Purpose**: Validates `scratchpad.json` - Immediate priorities with MCP validation state, task queue with parliamentary approval metadata, and focus mode management.

**Schema Structure:**
- **Required Fields**: `schema_version`, `last_updated`, `immediate_priorities`, `mcp_validation_state`, `task_queue`
- **Key Components**:
  - `immediate_priorities`: Array of up to 10 urgent tasks with dependencies and deadlines
  - `task_queue`: Array of up to 50 tasks with parliamentary approval scores
  - `mcp_validation_state`: Status of all mandatory MCP servers and anti-hallucination checks
  - `focus_mode`: Concentration settings with duration and break reminders

**Validation Rules:**
- Urgency enum: ["critical", "high", "medium", "low"]
- Task status enum: ["todo", "in_progress", "blocked", "completed"]
- Parliamentary approval: 0-100 percentage
- MCP server status: Boolean validation for all 8 mandatory servers

### 3. `kanban.schema.json`
**Purpose**: Validates `kanban.json` - Task workflow management with parliamentary approval tracking, WIP limits, and cross-file linkage.

**Schema Structure:**
- **Required Fields**: `schema_version`, `last_updated`, `columns`, `tasks`
- **Key Components**:
  - `columns`: Four required columns (todo, in_progress, done, approved) with WIP limits
  - `tasks`: Array of up to 100 tasks with full lifecycle tracking
  - `parliamentary_approval`: Tri-branch consensus scoring with executive, legislative, judicial votes
  - `workflow_metrics`: Cycle time, throughput, WIP current, blocked count

**Validation Rules:**
- Task status enum: ["todo", "in_progress", "done", "approved", "blocked"]
- Priority enum: ["P0", "P1", "P2", "P3"]
- WIP limits: in_progress column limited to 1-5 tasks
- Consensus scores: Executive (0-30%), Legislative (0-45%), Judicial (0-25%)

### 4. `mistakes.schema.json`
**Purpose**: Validates `mistakes.json` - Error patterns with predictive analytics, instant lint tracking, and Context7 source prioritization for learning optimization.

**Schema Structure:**
- **Required Fields**: `schema_version`, `last_updated`, `error_patterns`, `context7_source_priority`
- **Key Components**:
  - `error_patterns`: Categorized errors with frequency tracking and fix strategies
  - `instant_lint_tracking`: Real-time linting errors with auto-fix status
  - `predictive_warnings`: Up to 10 AI-generated warnings with confidence scores
  - `context7_source_priority`: Verified documentation sources with accuracy scoring
  - `anti_hallucination_metrics`: Context7 call tracking and accuracy improvements

**Validation Rules:**
- Severity enum: ["critical", "high", "medium", "low"]
- Confidence scores: 0-1 decimal range
- Accuracy scores: 0-1 decimal range for source verification
- Frequency: Minimum 1, tracks error occurrence patterns

### 5. `systemPatterns.schema.json`
**Purpose**: Validates `systemPatterns.json` - Architecture patterns with MCP-enriched documentation links, successful implementations, and constitutional compliance tracking.

**Schema Structure:**
- **Required Fields**: `schema_version`, `last_updated`, `architecture_patterns`, `mcp_enriched_links`
- **Key Components**:
  - `architecture_patterns`: Reusable patterns with success rates and usage tracking
  - `successful_implementations`: Historical implementation data with quality scores
  - `pattern_relationships`: Dependencies, alternatives, enhancements, and conflicts
  - `governance_decisions`: Parliamentary oversight decisions with consensus scoring
  - `mcp_enriched_links`: Verified documentation links with Context7 validation
  - `constitutional_compliance`: Tri-branch approvals and governance validation scores

**Validation Rules:**
- Success rates: 0-100 percentage
- Complexity scores: 0-10 scale
- Relationship types: ["dependency", "alternative", "enhancement", "conflict"]
- Governance decision patterns: "gd-[A-Za-z0-9_-]+" format

### 6. `progress.schema.json`
**Purpose**: Validates `progress.json` - Development milestones with constitutional compliance metrics, compressed history, and anti-hallucination tracking.

**Schema Structure:**
- **Required Fields**: `schema_version`, `last_updated`, `milestone_tracking`, `constitutional_metrics`
- **Key Components**:
  - `milestone_tracking`: Project milestones with completion percentages and quality metrics
  - `compressed_history`: Aggregated statistics for performance analysis
  - `current_sprint`: Active sprint tracking with points and timeline
  - `constitutional_metrics`: Compliance scoring and tri-branch efficiency metrics
  - `achievements`: Milestone achievements with impact descriptions

**Validation Rules:**
- Milestone status enum: ["not_started", "in_progress", "completed", "blocked"]
- Completion percentage: 0-100
- Quality scores: 0-10 scale for code quality and performance
- Compliance scores: 0-100 percentage for constitutional adherence

### 7. `roadmap.schema.json`
**Purpose**: Validates `roadmap.json` - Strategic planning with AegisKG strategic knowledge graphs, milestone dependencies, and anti-hallucination roadmap integration.

**Schema Structure:**
- **Required Fields**: `schema_version`, `last_updated`, `strategic_objectives`
- **Key Components**:
  - `strategic_objectives`: High-level phases with milestones and dependencies
  - `resource_allocation`: Development, design, testing, and documentation hours
  - `anti_hallucination_roadmap`: Context7 integration milestones and link storage objectives

**Validation Rules:**
- Phase status enum: ["not_started", "in_progress", "completed", "blocked"]
- Business impact enum: ["critical", "high", "medium", "low"]
- Risk probability: 0-1 decimal range
- Completion percentage: 0-100

### 8. `memory.schema.json`
**Purpose**: Validates `memory.json` - Knowledge graph storage with entities, relations, observations, and user context for personalization via @mcp:memory integration.

**Schema Structure:**
- **Required Fields**: `schema_version`, `last_updated`, `entities`, `relations`
- **Key Components**:
  - `entities`: Knowledge graph nodes with typed observations
  - `relations`: Directed connections in active voice
  - `metadata`: Graph statistics and query tracking
  - `user_context`: Personalization data including identity, behaviors, preferences, goals

**Validation Rules:**
- Entity types: ["person", "organization", "event", "project", "technology", "concept", "location", "tool", "pattern", "error", "solution"]
- Relation types: ["works_at", "manages", "uses", "knows", "created", "depends_on", "implements", "resolves", "caused_by", "related_to", "part_of", "similar_to", "replaces", "extends"]
- Entity names: Pattern "^[A-Za-z0-9_]+$"
- Observations: 1-500 character limit per observation

## Helper Schemas (3 Support Files)

### 1. `helpers/common-mistakes.json`
**Purpose**: Documents frequent LLM errors and tool usage pitfalls with MCP prevention strategies.

**Key Features:**
- **Severity Classification**: HIGH, MEDIUM, LOW severity levels
- **Tool-Specific Errors**: Detailed examples for each tool with wrong/correct formats
- **MCP Prevention**: Pre-call validation, execution monitoring, post-call verification
- **Pattern Storage**: Integration with @mcp:memory for learning and prevention

**Critical Patterns Documented:**
- Stringified arrays instead of actual array objects
- Partial whitespace matching in file edits
- Relative vs absolute path usage
- Type mismatches in tool parameters

### 2. `helpers/error-recovery.json`
**Purpose**: Provides MCP-enhanced error recovery strategies and protocols for different failure types.

**Key Features:**
- **Severity-Based Recovery**: Critical, High, Medium, Low severity protocols
- **Immediate Response**: Step-by-step recovery procedures with MCP integration
- **Recovery Strategies**: Simplify edits, alternative tools, manual verification
- **Prevention Integration**: Learning loops with @mcp:memory storage

**Recovery Protocols:**
- Edit failures: Git status checks, filesystem verification, memory retrieval
- Tool failures: Context7 documentation lookup, alternative tool selection
- Silent failures: Detection strategies and verification protocols

### 3. `helpers/tool-usage-patterns.json`
**Purpose**: Contains MCP-enhanced tool usage patterns for error prevention and validation.

**Key Features:**
- **Correct Formats**: Detailed examples for all major tools
- **MCP Integration**: Validation workflows with all 8 mandatory MCP servers
- **Error Prevention Protocol**: 5-step validation and learning process
- **Constitutional Integration**: Article XV compliance enforcement

**Tool Coverage:**
- `replace_file_content`: File editing with exact content matching
- `mcp3_edit_file`: Filesystem MCP editing with array validation
- `mcp3_write_file`: New file creation with safety checks
- `run_command`: Command execution with safety validation
- `grep_search`: Search operations with optimization

## Schema Validation Process

### Validation Workflow
1. **Pre-Validation**: Check required fields and data types
2. **Format Validation**: Verify date-time, URI, and pattern formats
3. **Cross-Reference Validation**: Ensure linkage keys are properly formatted
4. **Size Validation**: Confirm files remain under 10KB limit
5. **Constitutional Compliance**: Verify governance requirements are met

### Validation Tools
- **JSON Schema Validators**: Use `jsonschema` CLI or language-specific libraries
- **Custom Validators**: AegisIDE-specific validation for linkage keys and patterns
- **MCP Integration**: @mcp:filesystem for file validation, @mcp:memory for pattern checking

### Error Handling
- **Validation Failures**: Automatic rollback to last known good state
- **Schema Violations**: Detailed error messages with correction guidance
- **Recovery Procedures**: Step-by-step remediation with MCP assistance

## Cross-File Linkage System

### Standardized Linkage Keys
All schemas support cross-referencing through standardized ID patterns:

```json
{
  "proposal_id": "proposal-feature-auth",
  "kanban_task_id": "task-implement-login", 
  "roadmap_milestone_id": "rm-auth-system",
  "governance_decision_id": "gd-consensus-vote-001"
}
```

### Linkage Patterns
- **Proposal ID**: `^proposal-[A-Za-z0-9_-]+$`
- **Kanban Task ID**: `^task-[A-Za-z0-9_-]+$`
- **Roadmap Milestone ID**: `^rm-[A-Za-z0-9_-]+$`
- **Governance Decision ID**: `^gd-[A-Za-z0-9_-]+$`

### Traceability Benefits
- **End-to-End Tracking**: Follow features from roadmap to implementation
- **Impact Analysis**: Understand dependencies and relationships
- **Audit Trails**: Complete history of decisions and implementations
- **Parliamentary Oversight**: Track consensus and approval processes

## Performance Optimization

### JSON Performance Benefits
- **2.6x Faster Parsing**: Compared to markdown processing
- **65% Memory Optimization**: Structured data reduces overhead
- **Automatic Validation**: Prevents data corruption and inconsistencies
- **Type Safety**: Ensures consistent data structures across sessions

### Size Management
- **10KB File Limit**: Constitutional requirement for optimal performance
- **Array Limits**: Maximum items defined for each array type
- **String Limits**: Maximum lengths for descriptions and titles
- **Compression Strategies**: Automatic cleanup of old entries

### Optimization Techniques
- **Indexed Access**: Use linkage keys for fast cross-references
- **Cached Validation**: Store validation results for repeated operations
- **Lazy Loading**: Load only required schema sections
- **Batch Operations**: Group multiple validations for efficiency

## Constitutional Compliance

### Article Integration
- **Article III**: 8-schema memory-bank integrity and update requirements
- **Article IV**: EMD compliance with ≤10KB file size limits
- **Article XIII**: Zero-tolerance validation with HALT-FIX-VALIDATE loop
- **Article XV**: Tool usage governance and error prevention protocols

### Governance Requirements
- **Parliamentary Approval**: Consensus scoring in kanban and systemPatterns
- **Tri-Branch Validation**: Executive, Legislative, Judicial vote tracking
- **Constitutional Metrics**: Compliance scoring in progress schema
- **Amendment Authority**: Schema changes require >95% consensus

### Compliance Monitoring
- **Real-Time Validation**: Continuous schema compliance checking
- **Violation Detection**: Automatic identification of non-compliant data
- **Remediation Protocols**: Step-by-step correction procedures
- **Audit Trails**: Complete history of compliance actions

## Migration and Version Control

### Semantic Versioning
- **Schema Versions**: All schemas use semver format (e.g., "1.0.0")
- **Backward Compatibility**: New versions maintain compatibility with previous data
- **Migration Scripts**: Automated upgrade procedures between versions
- **Deprecation Notices**: Advance warning for breaking changes

### Git Integration
- **Change Tracking**: All schema modifications tracked in version control
- **Rollback Capability**: Ability to revert to previous schema versions
- **Branch Management**: Schema changes follow constitutional amendment process
- **Merge Conflicts**: Resolution procedures for concurrent schema changes

### Upgrade Procedures
1. **Validation**: Test new schema against existing data
2. **Migration**: Automated data transformation scripts
3. **Verification**: Confirm successful migration with validation
4. **Rollback Plan**: Prepared procedures for migration failures

## Usage Examples

### Basic Validation
```bash
# Validate active context file
jsonschema -i activeContext.json activeContext.schema.json

# Validate all memory-bank files
for file in *.json; do
  jsonschema -i "$file" "${file%.json}.schema.json"
done
```

### Programming Integration
```javascript
// Node.js validation example
const Ajv = require('ajv');
const ajv = new Ajv();

const schema = require('./activeContext.schema.json');
const data = require('./activeContext.json');

const validate = ajv.compile(schema);
const valid = validate(data);
if (!valid) console.log(validate.errors);
```

### Cross-Reference Queries
```bash
# Find all tasks linked to a specific milestone
jq '.tasks[] | select(.roadmap_milestone_id == "rm-auth-system")' kanban.json

# Find governance decisions for a proposal
jq '.governance_decisions[] | select(.proposal_id == "proposal-feature-auth")' systemPatterns.json
```

## Common Schema Errors and Solutions

### 1. Missing Required Fields
**Error**: Required property 'schema_version' missing
**Solution**: Ensure all required fields are present in JSON data
```json
{
  "schema_version": "1.0.0",
  "last_updated": "2025-01-08T10:30:00Z"
}
```

### 2. Type Mismatches
**Error**: Expected number, got string for 'completion_percentage'
**Solution**: Use correct data types as defined in schema
```json
{
  "completion_percentage": 75,  // Number, not "75"
  "approved": true             // Boolean, not "true"
}
```

### 3. Invalid Formats
**Error**: String does not match format 'date-time'
**Solution**: Use ISO 8601 format for timestamps
```json
{
  "last_updated": "2025-01-08T10:30:00Z"  // Correct ISO format
}
```

### 4. Pattern Violations
**Error**: String does not match pattern '^task-[A-Za-z0-9_-]+$'
**Solution**: Follow standardized ID patterns
```json
{
  "kanban_task_id": "task-implement-auth"  // Correct pattern
}
```

### 5. Array Limit Violations
**Error**: Array has too many items (maximum: 100)
**Solution**: Implement cleanup procedures for large arrays
```json
{
  "event_tracking": [/* Keep only recent 100 events */]
}
```

## Performance Tips and Best Practices

### Schema Design
- **Minimize Nesting**: Keep object hierarchies shallow for faster parsing
- **Use Enums**: Constrain string values to improve validation speed
- **Optimize Patterns**: Use efficient regex patterns for ID validation
- **Limit Array Sizes**: Set reasonable maximum items for arrays

### Data Management
- **Regular Cleanup**: Remove old entries to maintain performance
- **Compress History**: Aggregate old data into summary statistics
- **Index Efficiently**: Use linkage keys for fast cross-references
- **Cache Results**: Store validation results for repeated operations

### Validation Optimization
- **Validate Early**: Check schemas before file operations
- **Batch Validation**: Group multiple validations together
- **Incremental Updates**: Validate only changed portions when possible
- **Error Recovery**: Implement fast rollback for validation failures

## Support and Documentation

### File Locations
- **Core Schemas**: `.aegiside/schemas/*.schema.json`
- **Helper Schemas**: `.aegiside/schemas/helpers/*.json`
- **Memory Bank Files**: `.aegiside/memory-bank/*.json`
- **Constitutional Framework**: `.windsurf/rules/constitution/`

### Validation Tools
- **CLI Tools**: `jsonschema`, `ajv-cli`, `jq` for JSON processing
- **Programming Libraries**: Language-specific JSON Schema validators
- **Custom Validators**: AegisIDE-specific validation utilities
- **MCP Integration**: @mcp:filesystem and @mcp:memory for validation

### Getting Help
- **Schema Documentation**: This README and individual schema files
- **Constitutional Framework**: Complete governance documentation
- **Error Recovery**: Helper schemas provide detailed recovery procedures
- **Community Support**: AegisIDE community forums and documentation (1.0.0 → 1.1.0)
- **Patch**: Bug fixes, clarifications (1.0.0 → 1.0.1)

### Backward Compatibility
- New required fields added with defaults
- Deprecated fields marked but functional

## Linkage Keys (Cross-File Referencing)

| Key | Pattern | Source Fields | Target File(s) | Purpose |
|-----|---------|---------------|----------------|---------|
| `proposal_id` | `^proposal-[A-Za-z0-9_-]+$` | `activeContext.linkage`, `scratchpad.immediate_priorities[*]`, `kanban.tasks[*]`, `progress.milestone_tracking[*]`, `roadmap.strategic_objectives[*].milestones[*]`, `mistakes.*` | `systemPatterns.governance_decisions[*].proposal_id` | Link work to a governance proposal and approval |
| `kanban_task_id` | `^task-[A-Za-z0-9_-]+$` | `activeContext.linkage`, `scratchpad.immediate_priorities[*]`, `progress.milestone_tracking[*]`, `mistakes.*` | `kanban.tasks[*].id` | Bind active work and quality signals to a specific task |
| `roadmap_milestone_id` | `^rm-[A-Za-z0-9_-]+$` | `activeContext.linkage`, `scratchpad.immediate_priorities[*]`, `kanban.tasks[*]`, `progress.milestone_tracking[*]`, `roadmap.strategic_objectives[*].milestones[*]`, `mistakes.*` | `roadmap.strategic_objectives[*].milestones[*].id` | Tie tactical tasks to strategic milestones |
| `governance_decision_id` | `^gd-[A-Za-z0-9_-]+$` | `activeContext.linkage`, `kanban.tasks[*]`, `progress.milestone_tracking[*]` | `systemPatterns.governance_decisions[*].decision_id` | Reference the persisted oversight decision |

Notes:
- Linkage keys are optional but recommended for traceability and anti‑hallucination analytics.
- Validation scripts should verify that all referenced IDs exist in their target files.

## Support

### Schema Errors
Common issues and fixes:
1. **Missing required field**: Add field with valid value
2. **Invalid date format**: Use ISO 8601 (YYYY-MM-DDTHH:mm:ssZ)
3. **Type mismatch**: Check number vs string
4. **Enum violation**: Use predefined values from schema

### Performance Issues
If JSON parsing seems slow:
1. Check file sizes (should be ≤10KB)
2. Validate schema compliance
3. Clear old event history
4. Run cleanup utility

---

**AegisKG Integration**: Custom Archon-inspired local knowledge graph  
**Archon Reference**: https://github.com/coleam00/Archon  
**Constitutional Authority**: Article VI Amendment III-A  
**Effective Date**: 2025-10-06T19:23:00+05:30  
**Schema Consolidation**: Reduced from 17 to 8 essential files
