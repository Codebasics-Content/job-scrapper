# Base HeadlessX Configuration Classes - EMD Architecture
# Shared configuration dataclasses for HeadlessX clients

from dataclasses import dataclass
from enum import Enum


class CircuitState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, requests blocked
    HALF_OPEN = "half_open"  # Testing if service recovered


@dataclass
class RetryConfig:
    """Configuration for retry logic with exponential backoff"""
    max_attempts: int = 5
    base_delay: float = 1.0  # Initial delay in seconds
    max_delay: float = 60.0  # Maximum delay cap
    exponential_factor: float = 2.0
    jitter: bool = True  # Add randomization to prevent thundering herd


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker pattern"""
    failure_threshold: int = 5  # Failures before opening circuit
    recovery_timeout: float = 30.0  # Seconds before trying half-open
    success_threshold: int = 3  # Successes in half-open to close circuit
