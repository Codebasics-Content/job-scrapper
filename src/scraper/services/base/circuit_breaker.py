# Circuit Breaker Logic - EMD Architecture
# Handles failure detection and recovery for HeadlessX clients

import time
from typing import Optional

from .config import CircuitState, CircuitBreakerConfig


class HeadlessXError(RuntimeError):
    """Base exception for HeadlessX client errors"""
    pass


class CircuitOpenError(HeadlessXError):
    """Raised when circuit breaker is open"""
    pass


class CircuitBreaker:
    """Circuit breaker implementation for HeadlessX clients"""
    
    def __init__(self, config: Optional[CircuitBreakerConfig] = None):
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0.0
        self.success_count = 0
    
    def check_state(self) -> None:
        """Check and update circuit breaker state"""
        current_time = time.time()
        
        if self.state == CircuitState.OPEN:
            if current_time - self.last_failure_time > self.config.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
            else:
                raise CircuitOpenError("Circuit breaker is OPEN - service unavailable")
    
    def record_success(self) -> None:
        """Record successful request"""
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.config.success_threshold:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
        elif self.state == CircuitState.CLOSED:
            self.failure_count = max(0, self.failure_count - 1)
    
    def record_failure(self) -> None:
        """Record failed request"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.config.failure_threshold:
            self.state = CircuitState.OPEN
