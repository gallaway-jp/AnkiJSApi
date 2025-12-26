# SPDX-License-Identifier: MIT
# Copyright (c) 2025 AnkiDroid JS API Desktop Contributors

"""
Security utilities for input validation and rate limiting.
This module provides defense-in-depth security measures for the AnkiDroid JS API:

Components:
    - InputValidator: Validates and sanitizes all user inputs from JavaScript
    - RateLimiter: Token bucket algorithm for API rate limiting (10 calls/second default)
    - sanitize_for_logging(): Prevents PII exposure in debug logs
    - generate_template_hash(): Creates unique template identifiers

Security Features:
    - Input validation with pre-compiled regex patterns for performance
    - Length limits to prevent DoS attacks (500 chars default for text)
    - Control character removal (injection attack prevention)
    - Rate limiting per template and function (prevents API abuse)
    - Path traversal protection for filenames
    - Automatic cleanup of stale rate limit entries (prevents memory leaks)

Usage:
    >>> from .security import InputValidator, RateLimiter
    >>> 
    >>> # Validate text input
    >>> safe_text = InputValidator.validate_text(user_input, max_length=100)
    >>> 
    >>> # Check rate limit before processing API call
    >>> if RateLimiter.check(template_id, "apiCall", max_per_second=10):
    ...     # Process API call
    ...     result = process_api_call()
    >>> else:
    ...     # Rate limit exceeded
    ...     return {"error": "Rate limit exceeded"}

Constants:
    All security-related constants are defined in constants.py:
    - MAX_TEXT_LENGTH: 500 characters
    - MAX_TAG_LENGTH: 100 characters
    - RATE_LIMITER_CLEANUP_INTERVAL_SEC: 300 seconds (5 minutes)
    - RATE_LIMITER_STALE_THRESHOLD_SEC: 3600 seconds (1 hour)"""

import re
import time
import hashlib
from typing import Dict, Any, Tuple
from collections import defaultdict
from .constants import (
    MAX_TEXT_LENGTH,
    MAX_TAG_LENGTH,
    MAX_LOG_MESSAGE_LENGTH,
    RATE_LIMITER_CLEANUP_INTERVAL_SEC,
    RATE_LIMITER_STALE_THRESHOLD_SEC,
)

class InputValidator:
    """Centralized input validation and sanitization."""
    
    # Pre-compiled regex patterns for performance
    _FILENAME_PATTERN = re.compile(r'^[\w\-]+\.\w+$')
    _TAG_PATTERN = re.compile(r'^[\w\-]+$')
    _CALLBACK_ID_PATTERN = re.compile(r'^-?\d+$')
    
    @staticmethod
    def validate_text(text: str, max_length: int = MAX_TEXT_LENGTH, 
                     pattern: str = r'^[\w\s.,!?;:\-\'「」。、]+$',
                     allow_newlines: bool = True) -> str:
        """Validate and sanitize text input.
        
        Args:
            text: Input text to validate
            max_length: Maximum allowed length (default: 500 chars)
            pattern: Regex pattern for allowed characters (default: alphanumeric + common punctuation)
            allow_newlines: Whether to allow newlines in text (default: True)
            
        Returns:
            Sanitized text with control characters removed and trimmed
            
        Raises:
            TypeError: If input is not a string
            ValueError: If text exceeds max_length or contains disallowed characters
            
        Example:
            >>> InputValidator.validate_text("Hello World")
            'Hello World'
            >>> InputValidator.validate_text("Hello\x00World")  # null byte removed
            'HelloWorld'
            >>> InputValidator.validate_text("A" * 1000, max_length=100)
            ValueError: Text too long: 1000 > 100
            
        Note:
            Control characters (except newlines/tabs if allowed) are automatically removed.
            This prevents injection attacks and ensures clean data.
        """
        if not isinstance(text, str):
            raise TypeError("Expected string input")
        
        if len(text) > max_length:
            raise ValueError(f"Text too long: {len(text)} > {max_length}")
        
        # Remove null bytes and control characters (except newlines if allowed)
        if allow_newlines:
            text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\t')
        else:
            text = ''.join(char for char in text if ord(char) >= 32 and char not in '\n\r')
        
        if not re.match(pattern, text, re.UNICODE | re.DOTALL):
            raise ValueError("Text contains invalid characters")
        
        return text.strip()
    
    @staticmethod
    def validate_integer(value: Any, min_val: int, max_val: int) -> int:
        """Validate integer input within range.
        
        Args:
            value: Value to validate
            min_val: Minimum allowed value
            max_val: Maximum allowed value
            
        Returns:
            Validated integer
            
        Raises:
            TypeError: If value cannot be converted to int
            ValueError: If value is out of range
        """
        try:
            value = int(value)
        except (TypeError, ValueError) as e:
            raise TypeError(f"Expected integer, got {type(value).__name__}")
        
        if not (min_val <= value <= max_val):
            raise ValueError(f"Value {value} out of range [{min_val}, {max_val}]")
        
        return value
    
    @staticmethod
    def validate_float(value: Any, min_val: float, max_val: float) -> float:
        """Validate float input within range.
        
        Args:
            value: Value to validate
            min_val: Minimum allowed value
            max_val: Maximum allowed value
            
        Returns:
            Validated float
            
        Raises:
            TypeError: If value cannot be converted to float
            ValueError: If value is out of range
        """
        try:
            value = float(value)
        except (TypeError, ValueError):
            raise TypeError(f"Expected float, got {type(value).__name__}")
        
        if not (min_val <= value <= max_val):
            raise ValueError(f"Value {value} out of range [{min_val}, {max_val}]")
        
        return value
    
    @staticmethod
    def validate_filename(filename: str) -> str:
        """Validate filename to prevent path traversal.
        
        Args:
            filename: Filename to validate
            
        Returns:
            Validated filename
            
        Raises:
            ValueError: If filename is invalid or contains path traversal
        """
        if not isinstance(filename, str):
            raise TypeError("Filename must be a string")
        
        # Only allow alphanumeric, dash, underscore, and single dot for extension
        if not InputValidator._FILENAME_PATTERN.match(filename):
            raise ValueError(f"Invalid filename: {filename}")
        
        # Explicitly check for path traversal attempts
        if '..' in filename or '/' in filename or '\\' in filename:
            raise ValueError(f"Path traversal detected in filename: {filename}")
        
        return filename
    
    @staticmethod
    def validate_tag(tag: str, max_length: int = MAX_TAG_LENGTH) -> str:
        """Validate tag name.
        
        Args:
            tag: Tag to validate
            max_length: Maximum tag length
            
        Returns:
            Validated tag
            
        Raises:
            ValueError: If tag is invalid
        """
        if not isinstance(tag, str):
            raise TypeError("Tag must be a string")
        
        tag = tag.strip()
        
        if len(tag) > max_length:
            raise ValueError(f"Tag too long: {len(tag)} > {max_length}")
        
        if not tag:
            raise ValueError("Tag cannot be empty")
        
        # Replace spaces with underscores
        tag = tag.replace(' ', '_')
        
        # Only allow alphanumeric, underscore, dash
        if not InputValidator._TAG_PATTERN.match(tag):
            raise ValueError(f"Invalid tag characters: {tag}")
        
        return tag


class RateLimiter:
    """Token bucket rate limiter for API calls."""
    
    _buckets: Dict[str, Tuple[float, float]] = {}  # {key: (tokens, last_refill)}
    _call_counts: Dict[str, int] = defaultdict(int)
    _last_cleanup: float = time.time()
    _CLEANUP_INTERVAL: float = RATE_LIMITER_CLEANUP_INTERVAL_SEC
    _STALE_THRESHOLD: float = RATE_LIMITER_STALE_THRESHOLD_SEC
    
    @classmethod
    def check(cls, identifier: str, operation: str, max_per_second: int = 10) -> bool:
        """Check if operation is within rate limit.
        
        Args:
            identifier: Unique identifier (e.g., template hash)
            operation: Operation name
            max_per_second: Maximum calls per second
            
        Returns:
            True if within limit, False otherwise
        """
        now = time.time()
        
        # Periodic cleanup to prevent memory leak
        if now - cls._last_cleanup > cls._CLEANUP_INTERVAL:
            cls._cleanup_stale_entries(now)
            cls._last_cleanup = now
        
        key = f"{identifier}:{operation}"
        
        if key not in cls._buckets:
            cls._buckets[key] = (float(max_per_second), now)
            cls._call_counts[key] = 1
            return True
        
        tokens, last_refill = cls._buckets[key]
        
        # Refill tokens based on time elapsed
        elapsed = now - last_refill
        tokens = min(float(max_per_second), tokens + (elapsed * max_per_second))
        
        if tokens >= 1.0:
            cls._buckets[key] = (tokens - 1.0, now)
            cls._call_counts[key] += 1
            return True
        
        # Rate limit exceeded
        return False
    
    @classmethod
    def get_call_count(cls, identifier: str, operation: str) -> int:
        """Get total call count for an operation."""
        key = f"{identifier}:{operation}"
        return cls._call_counts.get(key, 0)
    
    @classmethod
    def _cleanup_stale_entries(cls, now: float) -> None:
        """Remove stale entries to prevent memory leak."""
        stale_keys = [
            key for key, (_, last_refill) in cls._buckets.items()
            if now - last_refill > cls._STALE_THRESHOLD
        ]
        for key in stale_keys:
            del cls._buckets[key]
            if key in cls._call_counts:
                del cls._call_counts[key]
    
    @classmethod
    def reset(cls, identifier: str = None) -> None:
        """Reset rate limiter state."""
        if identifier:
            # Reset specific identifier
            keys_to_remove = [k for k in cls._buckets.keys() if k.startswith(f"{identifier}:")]
            for key in keys_to_remove:
                del cls._buckets[key]
                if key in cls._call_counts:
                    del cls._call_counts[key]
        else:
            # Reset all
            cls._buckets.clear()
            cls._call_counts.clear()


# Pre-compiled regex patterns for sanitization (performance)
_SANITIZE_TEXT_RE = re.compile(r'"text":\s*"[^"]*"')
_SANITIZE_QUERY_RE = re.compile(r'"query":\s*"[^"]*"')
_SANITIZE_TAGS_RE = re.compile(r'"tags":\s*\[[^\]]*\]')
_SANITIZE_PATH_RE = re.compile(r'File ".*[\\/]([^\\/]+\.py)"')


def sanitize_for_logging(data: str, max_length: int = MAX_LOG_MESSAGE_LENGTH) -> str:
    """Sanitize data for logging to prevent PII exposure.
    
    Args:
        data: Data to sanitize
        max_length: Maximum length to log
        
    Returns:
        Sanitized string suitable for logging
    """
    if not isinstance(data, str):
        data = str(data)
    
    # Remove potentially sensitive data from logs (use pre-compiled patterns)
    data = _SANITIZE_TEXT_RE.sub('"text":"[REDACTED]"', data)
    data = _SANITIZE_QUERY_RE.sub('"query":"[REDACTED]"', data)
    data = _SANITIZE_TAGS_RE.sub('"tags":"[REDACTED]"', data)
    
    # Strip file paths to just filename
    data = _SANITIZE_PATH_RE.sub(r'File "\1"', data)
    
    # Truncate to reasonable length (use slice for better performance)
    return data[:max_length] + "..." if len(data) > max_length else data


def generate_template_hash(template_content: str) -> str:
    """Generate a hash for template identification.
    
    Args:
        template_content: Template HTML content
        
    Returns:
        SHA-256 hash of template
    """
    return hashlib.sha256(template_content.encode('utf-8')).hexdigest()
