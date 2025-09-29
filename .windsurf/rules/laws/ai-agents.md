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
- Create **data ingestion pipelines** for knowledge base updates
- Implement **data versioning** for knowledge base management

## Memory and State Management

### Conversation Memory
- Implement **short-term memory** for conversation context
- Use **long-term memory** for persistent agent knowledge
- Create **episodic memory** for experience-based learning
- Implement **memory compression** for efficiency
- Use **memory retrieval** with semantic similarity

### State Persistence
- Use **database storage** for persistent agent state
- Implement **state serialization** with proper versioning
- Create **state recovery** mechanisms for failure scenarios
- Use **distributed state** for multi-agent systems
- Implement **state synchronization** across agent instances

### Context Management
- Implement **context window management** for large conversations
- Use **context compression** techniques for efficiency
- Create **context prioritization** for important information
- Implement **context sharing** between related agents
- Use **context validation** for consistency checks

## LLM Integration and Optimization

### Model Selection and Configuration
- Use **model routing** based on task complexity and requirements
- Implement **model fallbacks** for reliability
- Use **fine-tuned models** for specialized tasks
- Create **model comparison** and evaluation frameworks
- Implement **cost optimization** strategies for model usage

### Prompt Engineering
- Create **prompt templates** with variable substitution
- Implement **prompt optimization** with A/B testing
- Use **few-shot learning** with relevant examples
- Create **prompt chaining** for complex reasoning
- Implement **prompt validation** and safety checks

### Response Processing
- Implement **structured output parsing** with validation
- Use **response streaming** for better user experience
- Create **response caching** for efficiency
- Implement **response filtering** for safety and quality
- Use **response scoring** for quality assessment

## Testing and Evaluation

### Unit Testing
- Write **unit tests** for individual agent components
- Use **mock LLM responses** for deterministic testing
- Implement **tool testing** with proper input/output validation
- Test **error handling** and edge cases thoroughly
- Achieve **minimum 80% code coverage**

### Integration Testing
- Test **agent workflows** end-to-end
- Use **test environments** with controlled data
- Implement **performance testing** for response times
- Test **concurrent agent** interactions
- Use **chaos testing** for resilience validation

### Evaluation Metrics
- Implement **task completion** success rate tracking
- Use **response quality** evaluation with LLM judges
- Create **efficiency metrics** for resource usage
- Implement **user satisfaction** scoring systems
- Use **A/B testing** for agent performance comparison

## Security and Safety

### Input Validation and Sanitization
- **Validate all inputs** from users and external systems
- Implement **prompt injection** protection mechanisms
- Use **content filtering** for inappropriate inputs
- Create **input sanitization** for special characters
- Implement **rate limiting** for abuse prevention

### Output Safety
- Implement **content moderation** for generated responses
- Use **fact-checking** mechanisms where appropriate
- Create **bias detection** and mitigation strategies
- Implement **hallucination detection** systems
- Use **response guardrails** for safety constraints

### Data Privacy and Security
- Implement **data encryption** for sensitive information
- Use **access controls** for agent and tool permissions
- Create **audit logging** for all agent activities
- Implement **data retention** policies
- Use **privacy-preserving** techniques where needed

## Performance Optimization

### Latency Optimization
- Use **response streaming** for immediate feedback
- Implement **parallel processing** where possible
- Create **caching strategies** for frequent operations
- Use **connection pooling** for external services
- Implement **request batching** for efficiency

### Resource Management
- Monitor **memory usage** and implement cleanup
- Use **connection limits** for external services
- Implement **graceful degradation** under load
- Create **resource monitoring** and alerting
- Use **auto-scaling** strategies for cloud deployment

### Cost Optimization
- Implement **token counting** and cost tracking
- Use **model selection** based on cost/performance trade-offs
- Create **budget limits** and monitoring
- Implement **usage analytics** for optimization insights
- Use **caching** to reduce API calls

## Deployment and Monitoring

### Production Deployment
- Use **containerization** with Docker for consistency
- Implement **environment configuration** management
- Create **health checks** for agent availability
- Use **load balancing** for high availability
- Implement **graceful shutdown** procedures

### Monitoring and Observability
- Implement **structured logging** with correlation IDs
- Use **metrics collection** for performance monitoring
- Create **distributed tracing** for agent workflows
- Implement **alerting** for failures and anomalies
- Use **dashboards** for operational visibility

### Continuous Improvement
- Implement **feedback loops** for agent improvement
- Use **model retraining** with new data
- Create **A/B testing** frameworks for optimization
- Implement **version control** for agent configurations
- Use **automated evaluation** for regression detection

## Tech Stack Requirements

### Python Stack
- **LangChain** (0.3+) - comprehensive agent framework
- **CrewAI** (0.70+) - multi-agent orchestration
- **OpenAI** or **Anthropic** - LLM providers
- **ChromaDB** or **Pinecone** - vector storage
- **FastAPI** - API development

### TypeScript/JavaScript Stack
- **LangChain.js** (0.3+) - JavaScript agent framework
- **Vercel AI SDK** - modern AI development
- **OpenAI SDK** - LLM integration
- **Vector databases** - Pinecone, Supabase Vector
- **Next.js** or **Express** - web framework

### Development Tools
- **Jupyter Notebooks** - prototyping and experimentation
- **LangSmith** - LangChain debugging and monitoring
- **Weights & Biases** - experiment tracking
- **Docker** - containerization
- **Git** - version control with LFS for models

## IDE Integration Guidelines

### Universal IDE Compatibility
- **VS Code** with Python/TypeScript extensions
- **PyCharm** - comprehensive Python development
- **Cursor** - AI-powered development
- **Jupyter Lab** - interactive development and research

### Development Workflow
- Use **language servers** for intelligent code completion
- Implement **debugging** with proper breakpoint support
- Use **version control** with proper .gitignore for models
- Set up **automated testing** with CI/CD integration
- Use **code formatting** with Black (Python) or Prettier (JS/TS)
