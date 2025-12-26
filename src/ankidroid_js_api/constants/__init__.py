# SPDX-License-Identifier: MIT
# Copyright (c) 2025 AnkiDroid JS API Desktop Contributors

"""
Constants package for the AnkiDroid JS API.

This package organizes constants into logical categories:
- security: API security, rate limiting, validation limits
- cards: Card types, states, flags, ease factors
- tts: Text-to-speech configuration
- ui: UI elements and notifications

All constants are re-exported from this module for backward compatibility.
"""

# Re-export all constants from sub-modules
from .security import *
from .cards import *
from .tts import *
from .ui import *

__all__ = [
    # Security constants
    'MAX_JSON_PAYLOAD_BYTES',
    'DEFAULT_API_RATE_LIMIT_PER_SECOND',
    'RATE_LIMITER_CLEANUP_INTERVAL_SEC',
    'RATE_LIMITER_STALE_THRESHOLD_SEC',
    'MAX_TEXT_LENGTH',
    'MAX_TEXT_LENGTH_TTS',
    'MAX_TAG_LENGTH',
    'MAX_LOG_MESSAGE_LENGTH',
    
    # Card constants
    'NEW_CARD_TIME_ESTIMATE_SEC',
    'LEARNING_CARD_TIME_ESTIMATE_SEC',
    'REVIEW_CARD_TIME_ESTIMATE_SEC',
    'MIN_CARD_DUE_DAYS',
    'MAX_CARD_DUE_DAYS',
    'FLAG_NONE',
    'FLAG_RED',
    'FLAG_ORANGE',
    'FLAG_GREEN',
    'FLAG_BLUE',
    'FLAG_PINK',
    'FLAG_TURQUOISE',
    'FLAG_PURPLE',
    'FLAG_COLOR_MAP',
    'EASE_AGAIN',
    'EASE_HARD',
    'EASE_GOOD',
    'EASE_EASY',
    'CARD_TYPE_NEW',
    'CARD_TYPE_LEARNING',
    'CARD_TYPE_REVIEW',
    'CARD_TYPE_RELEARNING',
    'QUEUE_NEW',
    'QUEUE_LEARNING',
    'QUEUE_REVIEW',
    'QUEUE_DAY_LEARNING',
    'QUEUE_PREVIEW',
    'QUEUE_SUSPENDED',
    'QUEUE_BURIED',
    'QUEUE_MANUALLY_BURIED',
    'DEFAULT_CARD_FACTOR',
    
    # TTS constants
    'TTS_DEFAULT_WPM',
    'TTS_MIN_RATE',
    'TTS_MAX_RATE',
    'TTS_MIN_PITCH',
    'TTS_MAX_PITCH',
    'TTS_MIN_RATE_WINDOWS',
    'TTS_MAX_RATE_WINDOWS',
    
    # UI constants
    'DEFAULT_TOAST_DURATION_MS',
    'TOAST_DURATION_MULTIPLIER_LONG',
]
