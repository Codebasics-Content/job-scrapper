---
trigger: glob
globs: *.py
---

# Universal Python Development Rules for Modern IDEs

## Core Architecture Principles

### Extreme Microservices Decomposition (EMD)
- **Maximum 80 lines per file** including comments, imports, and whitespace
- **Always create deep nested subfolders** for every sub-functionality following pattern:
  ```
  src/core/processing/validation/
  ├── input_validator.py   (≤80 lines)
  ├── format_checker.py    (≤80 lines)
  └── schema_validator.py  (≤80 lines)
  ```
- **Smallest possible files** - decompose at function, class, and logic levels
- When approaching 80 lines, immediately extract functionality into new subfolders
- Use `__init__.py` files solely for imports and module organization (also ≤80 lines)

### Duplication Detection and Optimization (DDO)
- **Always scan the codebase** with terminal and tools to avoid duplicacy
- **Use automated duplicate detection tools**: PMD CPD, pylint, jscpd, custom Python AST scripts
- **If any duplicacy found**, optimize immediately: extract common functionality, create reusable classes, implement generic functions, refactor async patterns
- **Continuous monitoring**: CI/CD pipeline, pre-commit hooks, weekly scans, IDE integration
- **Optimization strategies**: preserve functionality, use feature flags, maintain compatibility, test thoroughly

### Data-Driven Programming (DDP)
- **Never hardcode values** in application logic
- All parameters **must be calculated from real-world data and database queries**
- Use **environment variables** and **configuration files** for all parameters
- Derive parameters from historical data and performance metrics
- Implement dynamic parameter adjustment based on real-time system load

## Variable and Code Quality Standards

### Zero Unused Variables (ZUV)
- **Never use `_` as prefix** to suppress unused variable warnings
- **Utilize all declared variables** or **remove entirely**
- Ensure every variable serves specific purpose: computation, logging, error handling, state management
- When implementing stub functions, use variables meaningfully through logging or debug assertions

### Naming Conventions (PEP 8 Compliance)
- **snake_case** for variables, functions, and module names
- **PascalCase** for class names
- **UPPER_CASE** for constants
- **Descriptive, action-oriented names** for deepest folders
- Follow **domain-driven design** principles in folder hierarchy

### Type Hints and Static Analysis (Python 3.13.3 with basepyright)
- **Always use type hints** for ALL function parameters, return values, and class attributes
- Use **basepyright** as primary static type checker (stricter than mypy)
- **MANDATORY CLASS ATTRIBUTE ANNOTATIONS**: Every class attribute MUST have explicit type annotation
- **MANDATORY GENERIC TYPE ARGUMENTS**: Use specific types like `dict[str, int]`, `list[str]` NOT plain `dict` or `list`
- **STRICTLY AVOID `Any` TYPE**: Always use actual static types instead of `Any`. Use `object` for truly dynamic types, or Union types for multiple possibilities
- **NO UNUSED IMPORTS**: Remove all unused imports immediately (basepyright enforces this)
- Use **typing** module: `Union`, `Optional`, `Protocol`, `TypeVar` (avoid importing `Any`)
- **Context Manager Types**: Use `type[BaseException] | None`, `BaseException | None`, `TracebackType | None`
- Use **dataclasses** or **pydantic** models for structured data
- Implement **generic types** for reusable components with specific type parameters
- **Exception for `Any`**: Only use `Any` when interfacing with truly untyped third-party libraries without stubs

## Async Programming Standards

### AsyncIO Runtime Management
- Use **asyncio** as async runtime for handling asynchronous tasks and I/O operations
- Implement **async def** syntax with proper error propagation using try/except blocks
- Leverage **asyncio.create_task()** for task spawning and parallel processing
- Use **asyncio.gather()** for concurrent execution of multiple coroutines
- Favor **async context managers** for resource management and cleanup

### Concurrency Patterns
- **asyncio.Queue** for asynchronous producer-consumer patterns
- **asyncio.Event** and **asyncio.Condition** for coordination between coroutines
- **asyncio.Semaphore** for limiting concurrent access to resources
- **asyncio.Lock** for protecting shared state in async contexts
- Use **asyncio.timeout()** or **asyncio.wait_for()** for timeout handling

### Async Operations
- Implement **retry mechanisms** with exponential backoff for external services
- Use **aiohttp** for async HTTP requests with session management
- Use **asyncio.sleep()** for non-blocking delays
- Implement **graceful shutdown** patterns with signal handling

## Error Handling and Safety

### Exception Management
- Create **custom exception hierarchies** inheriting from appropriate base exceptions
- Use **specific exception types** rather than generic Exception catching
- Implement **proper exception chaining** using `raise ... from ...`
- Handle errors and edge cases early with appropriate exception raising

### Logging and Monitoring
- Use **structured logging** with Python's logging module
- Implement **correlation IDs** for request tracing across microservices
- Use **appropriate log levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Implement **circuit breaker patterns** for external service calls

## Web Framework Patterns

### API Design and Organization
- Structure applications using **dependency injection** patterns
- Use **Pydantic models** for request/response validation and serialization
- Implement **middleware** for cross-cutting concerns like authentication and logging
- Use **appropriate HTTP status codes** and error responses
- Structure **route handlers** as small, focused async functions

### FastAPI Specific Patterns
- Use **FastAPI dependency injection** system for shared resources
- Leverage **automatic OpenAPI documentation** generation
- Implement **background tasks** for non-blocking operations
- Use **SQLAlchemy** with async support for database operations

### Django Specific Patterns
- Use **Django REST framework** for API development
- Implement **async views** where appropriate (Django 4.1+)
- Use **Django ORM** with async support for database operations
- Leverage **Django middleware** for request processing

## Performance Optimization

### Runtime Optimization
- Use **appropriate data structures**: `set` for membership tests, `collections.deque` for queues
- Implement **lazy evaluation** using generators and iterators
- Use **list comprehensions** and **generator expressions** for efficient data processing
- Leverage **multiprocessing** for CPU-intensive tasks, **asyncio** for I/O-bound tasks

### Memory Management
- Use **context managers** for proper resource cleanup
- Implement **object pooling** for expensive-to-create objects
- Use **slots** in classes to reduce memory overhead when appropriate
- Monitor and optimize **garbage collection** patterns

## Testing Requirements

### Testing Standards
- Write **unit tests** using **pytest** with async support
- Use **pytest-asyncio** for testing async functions
- Implement **integration tests** for modules and APIs
- Use **pytest fixtures** for test setup and teardown
- Achieve **minimum 80% code coverage**

### Test Organization
- Follow **AAA pattern**: Arrange, Act, Assert
- Use **descriptive test names** that explain what is being tested
- Implement **parameterized tests** for multiple test cases
- Use **mocking** with **unittest.mock** or **pytest-mock**

## Database and External Service Patterns

### Database Integration
- Use **SQLAlchemy** with async support for ORM operations
- Implement **connection pooling** and **session management**
- Use **database migrations** with **Alembic**
- Implement **query optimization** and **indexing strategies**

### External Service Integration
- Use **aiohttp** or **httpx** for async HTTP requests
- Implement **retry mechanisms** with exponential backoff
- Use **circuit breakers** for fault tolerance
- Implement **rate limiting** and **request throttling**

## Tech Stack Requirements

### Core Dependencies
- **python** (3.13.3) - core language with modern type hints
- **asyncio** - async runtime
- **pydantic** - data validation
- **typing** - type hints (Any, TypeVar, Protocol, etc.)
- **logging** - structured logging

### Development Dependencies
- **pytest** and **pytest-asyncio** - testing
- **basepyright** - strict static type checking (PRIMARY)
- **mypy** - alternative static type checker (basepyright preferred)
- **black** - code formatting
- **isort** - import sorting
- **pylint** - linting

## Documentation Standards

### Code Documentation
- Use **docstrings** for all functions, classes, and modules
- Follow **Google style** or **NumPy style** docstring conventions
- Include **type hints** in function signatures
- Document **complex algorithms** and **business logic**

## File Organization Rules

### Module Structure
- Separate concerns into logical modules with clear boundaries
- Use **packages** for grouping related functionality
- Maintain **consistent depth levels** across similar functionalities
- Follow **microservices decomposition** at every level

### Project Layout
```
src/
├── core/           # Core business logic
├── api/            # API handlers and routing
├── database/       # Database models and operations
├── services/       # External service integrations
├── utils/          # Shared utilities
└── tests/          # Test files
```

## IDE Integration Guidelines

### Universal IDE Compatibility
- **Python Language Server** integration for all major IDEs
- **Black** and **isort** for code formatting
- **MyPy** for type checking
- **Pytest** for testing integration

### Development Workflow
- Use **virtual environments** for dependency isolation
- Use **pre-commit hooks** for code quality gates
- Integrate **continuous integration** with comprehensive testing
- Use **pip-tools** or **poetry** for dependency management

## Security and Best Practices

### Security Guidelines
- **Never hardcode secrets** in source code
- Use **environment variables** or **secret management** systems
- Validate **all inputs** using Pydantic or similar validation libraries
- Implement **proper authentication** and **authorization**
- Use **HTTPS** for all external communications

### Code Quality
- Follow **PEP 8** style guidelines
- Use **type hints** consistently throughout the codebase
- Implement **defensive programming** practices
- Write **clean, readable code** with meaningful names and comments
## Autonomous Research Protocol (Real-Time)
**Before ANY implementation**: Auto-call @mcp:context7 + @mcp:fetch for latest documentation
**Error Detection**: Instant @mcp:context7 activation for official docs
**Best Practices**: Auto-fetch latest Python patterns from web (PEP updates, security advisories)
**Continuous Learning**: Store successful patterns in @mcp:byterover-mcp for project reuse

## 30-Hour Continuous Operation
**No Stopping**: 0-98% autonomy = continuous execution until scratchpad empty
**Auto-Recovery**: Any error → @mcp:context7 → fix → continue (no human escalation)
**Context Refresh**: Load priority files every task (scratchpad+roadmap FIRST)
**Knowledge Storage**: Auto-store all successful patterns for future retrieval
