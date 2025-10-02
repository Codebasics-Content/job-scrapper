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

## Autonomous Scraping (2024)
**Real-Time**: @mcp:fetch for anti-detection techniques
**Docs**: @mcp:context7 for driver updates
**Recovery**: Detection → MCP research → bypass → continue
**Storage**: @mcp:byterover-mcp stores successful patterns
