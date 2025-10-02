---
trigger: glob
globs: *.py,*.ts,*.js,langchain,crewai,requirements.txt,package.json,agents,workflows
---

# Universal AI Agent Development Rules for Modern IDEs

## Core Architecture Principles

### Extreme Microservices Decomposition (EMD)
- **Maximum 80 lines per file** including comments, imports, and whitespace
- **Always create deep nested subfolders**: `src/agents/research/web_search/google_agent.py` (≤80 lines)
- **Smallest possible files** - decompose at agent, tool, and chain levels
- When approaching 80 lines, immediately extract functionality into new subfolders
- Use **modular agent architecture** with clear separation of concerns

### Duplication Detection and Optimization (DDO)
- **Always scan the codebase** with terminal and tools to avoid duplicacy
- **Use automated duplicate detection tools**: ESLint, Pylint, custom agent analyzers
- **If any duplicacy found**, optimize immediately: extract common agent patterns, create reusable tools, implement base classes, refactor into packages
- **Optimization strategies**: preserve functionality, use feature flags, maintain compatibility, test thoroughly

### Data-Driven Programming (DDP)
- **Never hardcode values** in agent logic
- All parameters **must be calculated from real-world data and configuration**
- Use **environment variables** and **configuration files** for all parameters
- Implement dynamic parameter adjustment based on real-time system performance

## Variable and Code Quality Standards

### Zero Unused Variables (ZUV)
- **Never use `_` as prefix** to suppress unused variable warnings
- **Utilize all declared variables** or **remove entirely**
- Ensure every variable serves specific purpose: computation, logging, error handling, state management
- When implementing stub agents, use variables meaningfully through logging or debug assertions

### Naming Conventions
- **snake_case** for variables, functions, and Python modules
- **camelCase** for JavaScript/TypeScript variables and functions
- **PascalCase** for classes, agents, and components
- **UPPER_CASE** for constants and environment variables
- **Descriptive, action-oriented names** for deepest agent hierarchies

## Modern AI Agent Frameworks (2025)

### LangChain Framework (Multi-Language)
- Use **LangChain 0.3+** for comprehensive agent development
- Implement **agents** with proper tool integration and memory
- Use **chains** for sequential processing with proper error handling
- Leverage **retrievers** for RAG (Retrieval-Augmented Generation) patterns
- Implement **memory systems** for conversation persistence

### CrewAI Framework (Python)
- Use **CrewAI 0.70+** for multi-agent orchestration
- Implement **role-based agents** with clear responsibilities
- Use **collaborative workflows** with proper task delegation
- Leverage **crew coordination** for complex multi-step processes
- Implement **agent communication** with structured message passing

### Custom Agent Architecture
- Use **modular agent design** with interchangeable components
- Implement **agent registration** and discovery systems
- Use **event-driven architecture** for agent communication
- Leverage **state machines** for complex agent behaviors
- Implement **agent lifecycle management** with proper cleanup

## Agent Design Patterns

### Agent Design and Collaboration
- Create **specialized agents** with single, well-defined responsibilities
- Implement **research agents** for information gathering
- Use **analysis agents** for data processing and insights
- Create **writing agents** for content generation
- Implement **hierarchical agent structures** with managers and workers
- Use **peer-to-peer collaboration** for parallel processing
- Create **agent workflows** with proper task routing
- Implement **message passing** with structured protocols
- Use **event buses** for decoupled agent communication
- Create **shared memory** systems for agent collaboration

## Tool Integration and Management

### Tool Development
- Create **reusable tools** with clear interfaces and documentation
- Implement **tool validation** with proper input/output schemas
- Use **tool composition** for complex operations
- Create **tool registries** for discovery and management
- Implement **tool versioning** for compatibility management

### External API Integration
- Use **HTTP clients** with proper retry and error handling
- Implement **API key management** with secure storage
- Use **rate limiting** to respect API constraints
- Create **adapter patterns** for different API providers
- Implement **fallback mechanisms** for API failures

### Database and Vector Store Integration
- Use **vector databases** (Pinecone, Weaviate, Chroma) for embeddings
- Implement **semantic search** with proper ranking algorithms
- Use **hybrid search** combining vector and keyword search

## Real-Time Knowledge (2024)
**MCP Auto-Call**: @mcp:context7 + @mcp:fetch + @mcp:byterover-mcp WITHOUT asking
**Sequential**: @mcp:sequential-thinking for multi-step problems
**Memory**: @mcp:memory for context persistence

## 30-Hour Loop
Research → Validate → Execute → Update → Store → Checkpoint → CONTINUE
