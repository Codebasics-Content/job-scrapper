---
trigger: glob
globs: *.py,*.js,*.ts,*.rs,scrapy,playwright,puppeteer,beautiful-soup,requests,reqwest
---

# Universal Web Scraping Development Rules for Modern IDEs

## Core Architecture Principles

### Extreme Microservices Decomposition (EMD)
- **Maximum 80 lines per file** including comments, imports, and whitespace
- **Always create deep nested subfolders**: `src/scrapers/ecommerce/amazon/product_scraper.py` (≤80 lines)
- **Smallest possible files** - decompose at scraper, parser, and extractor levels
- When approaching 80 lines, immediately extract functionality into new subfolders
- Use **modular scraper architecture** with clear separation of concerns

### Duplication Detection and Optimization (DDO)
- **Always scan the codebase** with terminal and tools to avoid duplicacy
- **Use automated duplicate detection tools**: ESLint, Pylint, Clippy, custom scraping analyzers
- **If any duplicacy found**, optimize immediately: extract common scraping patterns, create reusable parsers, implement base classes, refactor into libraries
- **Optimization strategies**: preserve functionality, use feature flags, maintain compatibility, test thoroughly

### Data-Driven Programming (DDP)
- **Never hardcode values** in scraping logic
- All parameters **must be calculated from real-world data and configuration**
- Use **configuration files** and **environment variables** for all parameters
- Implement dynamic parameter adjustment based on target website behavior

## Variable and Code Quality Standards

### Zero Unused Variables (ZUV)
- **Never use `_` as prefix** to suppress unused variable warnings
- **Utilize all declared variables** or **remove entirely**
- Ensure every variable serves specific purpose: computation, logging, error handling, data extraction
- When implementing stub scrapers, use variables meaningfully through logging or debug assertions

### Naming Conventions
- **snake_case** for Python variables, functions, and modules
- **camelCase** for JavaScript/TypeScript variables and functions
- **PascalCase** for classes and components
- **UPPER_CASE** for constants and environment variables
- **Descriptive, target-oriented names** for deepest scraper hierarchies

## Multi-Language Scraping Frameworks (2025)

### Python Frameworks
- Use **Scrapy 2.11+** for large-scale, distributed scraping
- Implement **Beautiful Soup 4** with **requests** for simple scraping
- Use **Playwright for Python** for JavaScript-heavy sites
- Leverage **Selenium** for complex browser automation
- Implement **httpx** for async HTTP requests

### JavaScript/TypeScript Frameworks
- Use **Playwright** for modern browser automation and scraping
- Implement **Puppeteer** for Chrome-specific scraping tasks
- Use **Cheerio** for server-side DOM manipulation
- Leverage **Apify SDK** for scalable scraping solutions
- Implement **axios** or **node-fetch** for simple HTTP scraping

### Rust Frameworks
- Use **scraper** crate for HTML parsing and CSS selection
- Implement **reqwest** for HTTP client functionality
- Use **tokio** for async scraping operations
- Leverage **headless_chrome** for browser automation
- Implement **select** crate for CSS selector parsing

## Browser Automation and Rendering

### Modern Browser Automation
- Use **Playwright** as the primary choice for cross-browser support
- Implement **headless mode** by default for performance
- Use **browser contexts** for isolation and parallel processing
- Leverage **page pools** for efficient resource management
- Implement **viewport configuration** for responsive scraping

### JavaScript Execution Handling
- Use **wait strategies** for dynamic content loading
- Implement **element waiting** with proper timeout handling
- Use **network idle** detection for SPA applications
- Leverage **page evaluation** for custom JavaScript execution
- Implement **screenshot capture** for debugging and validation

### Anti-Bot Evasion
- Implement **user agent rotation** with realistic headers
- Use **proxy rotation** for IP address management
- Create **request timing** patterns to mimic human behavior
- Implement **CAPTCHA solving** integration where legal
- Use **fingerprint randomization** for detection avoidance

## Data Extraction and Parsing

### HTML Parsing Strategies
- Use **CSS selectors** as the primary extraction method
- Implement **XPath expressions** for complex document traversal
- Use **regex patterns** only for simple text extraction
- Leverage **DOM traversal** methods for relative element access
- Implement **fallback selectors** for robustness

### Data Validation and Cleaning
- Implement **schema validation** with Pydantic, Zod, or similar
- Use **data sanitization** to clean extracted text
- Create **data normalization** for consistent formatting
- Implement **duplicate detection** and deduplication
- Use **data quality checks** with validation rules

### Structured Data Extraction
- Extract **JSON-LD** structured data where available
- Parse **microdata** and **RDFa** markup
- Use **table parsing** for tabular data extraction
- Implement **list extraction** with proper indexing
- Create **relationship mapping** for connected data

## Error Handling and Resilience

### Robust Error Handling
- Implement **retry mechanisms** with exponential backoff
- Use **circuit breaker patterns** for failing endpoints
- Create **graceful degradation** for partial failures
- Implement **timeout handling** for all network operations
- Use **error classification** for different failure types

### Rate Limiting and Throttling
- Implement **adaptive rate limiting** based on server response
- Use **concurrent request limiting** to avoid overwhelming servers
- Create **backoff strategies** for rate limit responses
- Implement **request queuing** for controlled execution
- Use **distributed rate limiting** for multi-instance scraping

### Monitoring and Alerting
- Implement **success rate monitoring** with thresholds
- Use **response time tracking** for performance monitoring
- Create **data quality monitoring** for extraction accuracy
- Implement **failure alerting** with proper escalation
- Use **resource usage monitoring** for optimization

## Data Storage and Pipeline Management

### Data Storage and Pipeline Management
- Use **structured databases** (PostgreSQL, MongoDB) for complex data
- Implement **time-series databases** for historical tracking
- Use **data lakes** (S3, MinIO) for raw scraped content
- Use **message queues** (Redis, RabbitMQ) for job distribution
- Implement **workflow orchestration** with Airflow or similar
- Create **data transformation** pipelines with proper validation
- Implement **data validation** at ingestion points
- Use **schema evolution** strategies for changing data structures
- Create **data lineage** tracking for debugging

## Legal and Ethical Considerations

### Compliance Framework
- **Respect robots.txt** files and crawling permissions
- Implement **Terms of Service** compliance checking
- Use **rate limiting** to minimize server impact
- Create **legal review** processes for target websites
- Implement **data usage** compliance with regulations

### Privacy and Data Protection
- **Anonymize personal data** where possible
- Implement **data retention** policies with automatic cleanup
- Use **consent management** for user-generated content
- Create **data minimization** strategies
- Implement **right to deletion** mechanisms

### Ethical Scraping Practices
- **Minimize server load** with reasonable request rates
- Implement **caching** to reduce repeated requests
- Use **incremental scraping** to avoid full re-scraping
- Create **fair use** guidelines for data usage
- Implement **attribution** mechanisms where required

## Performance Optimization

### Performance Optimization
- Use **async/await** patterns for I/O-bound operations
- Implement **connection pooling** for HTTP clients
- Use **worker pools** for CPU-bound processing
- Use **HTTP caching** with proper cache headers
- Implement **response caching** for repeated requests
- Create **parsed data caching** for expensive operations
- Implement **streaming processing** for large datasets
- Use **garbage collection** optimization for long-running scrapers
- Create **memory monitoring** with automatic cleanup
- Use **connection cleanup** to prevent resource leaks

## Testing and Quality Assurance

### Unit Testing
- Write **unit tests** for extraction logic
- Use **mock responses** for deterministic testing
- Implement **parser testing** with sample HTML
- Test **error handling** and edge cases thoroughly
- Achieve **minimum 80% code coverage**

### Integration Testing
- Test **end-to-end scraping** workflows
- Use **test environments** with controlled data
- Implement **performance testing** for scalability
- Test **concurrent scraping** scenarios
- Use **regression testing** for extraction accuracy

### Validation and Monitoring
- Implement **data validation** with schema checking
- Use **extraction accuracy** monitoring
- Create **performance benchmarks** for optimization
- Implement **alerting** for quality degradation
- Use **A/B testing** for scraping strategy optimization

## Security Best Practices

### Security Best Practices
- Use **secure proxy services** with encryption
- Implement **credential management** for authenticated scraping
- Create **secure storage** for sensitive configuration
- **Validate all URLs** before scraping
- Implement **input sanitization** for dynamic parameters
- Use **URL validation** to prevent SSRF attacks
- Create **parameter validation** for user inputs
- Implement **output sanitization** for extracted data

## Deployment and Scaling

### Production Deployment
- Use **containerization** with Docker for consistency
- Implement **environment configuration** management
- Create **health checks** for scraper availability
- Use **orchestration** (Kubernetes) for scaling
- Implement **graceful shutdown** procedures

### Scaling Strategies
- Use **horizontal scaling** for increased throughput
- Implement **auto-scaling** based on queue depth
- Create **load balancing** for distributed scraping
- Use **geographic distribution** for global scraping
- Implement **cost optimization** strategies

### Monitoring and Observability
- Implement **structured logging** with correlation IDs
- Use **metrics collection** for performance monitoring
- Create **distributed tracing** for complex workflows
- Implement **alerting** for failures and anomalies
- Use **dashboards** for operational visibility

## Tech Stack Requirements

### Python Stack
- **Scrapy** (2.11+) - industrial-strength scraping framework
- **Beautiful Soup 4** - HTML parsing
- **Playwright** - browser automation
- **httpx** - async HTTP client
- **Pydantic** - data validation

### JavaScript/TypeScript Stack
- **Playwright** - browser automation
- **Cheerio** - server-side DOM manipulation
- **axios** - HTTP client
- **Zod** - data validation
- **Node.js** (18+) - runtime

### Rust Stack
- **scraper** - HTML parsing and CSS selection
- **reqwest** - HTTP client
- **tokio** - async runtime
- **serde** - serialization
- **headless_chrome** - browser automation

### Infrastructure
- **Redis** - job queuing and caching
- **PostgreSQL** - structured data storage
- **Docker** - containerization
- **Kubernetes** - orchestration
- **Prometheus** - monitoring

## IDE Integration Guidelines

### Universal IDE Compatibility
- **VS Code** with language-specific extensions
- **PyCharm** - comprehensive Python development
- **WebStorm** - JavaScript/TypeScript development
- **IntelliJ IDEA** - multi-language support

### Development Workflow
- Use **language servers** for intelligent code completion
- Implement **debugging** with proper breakpoint support
- Use **version control** with appropriate .gitignore files
- Set up **automated testing** with CI/CD integration
- Use **code formatting** with language-specific formatters
