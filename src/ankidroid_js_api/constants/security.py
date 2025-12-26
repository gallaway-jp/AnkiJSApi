# SPDX-License-Identifier: MIT
# Copyright (c) 2025 AnkiDroid JS API Desktop Contributors

"""
Security-related constants for the AnkiDroid JS API.

This module contains limits and configurations for:
- API rate limiting
- Input validation
- Payload size limits
- Memory management
"""

# API Security
MAX_JSON_PAYLOAD_BYTES = 10 * 1024  # 10KB - Prevent DoS attacks via large payloads
DEFAULT_API_RATE_LIMIT_PER_SECOND = 10  # Maximum API calls per second per template

# Rate Limiter Memory Management
RATE_LIMITER_CLEANUP_INTERVAL_SEC = 300.0  # 5 minutes - Balance between memory usage and performance
RATE_LIMITER_STALE_THRESHOLD_SEC = 3600.0  # 1 hour - Remove entries older than this

# Input Validation Limits
MAX_TEXT_LENGTH = 500  # Maximum characters in text fields
MAX_TEXT_LENGTH_TTS = 10000  # Maximum characters for TTS (larger for long passages)
MAX_TAG_LENGTH = 100  # Maximum tag name length
MAX_LOG_MESSAGE_LENGTH = 100  # Maximum length for log messages (prevent log spam)
