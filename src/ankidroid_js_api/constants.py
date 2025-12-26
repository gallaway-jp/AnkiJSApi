# SPDX-License-Identifier: MIT
# Copyright (c) 2025 AnkiDroid JS API Desktop Contributors

"""
Constants used throughout the AnkiDroid JS API add-on.

This module centralizes magic numbers and configuration values
to improve maintainability and make the code more self-documenting.
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

# Card Time Estimates (seconds)
NEW_CARD_TIME_ESTIMATE_SEC = 20  # Average time to review a new card
LEARNING_CARD_TIME_ESTIMATE_SEC = 10  # Average time to review a learning card
REVIEW_CARD_TIME_ESTIMATE_SEC = 10  # Average time to review a review card

# TTS Configuration
TTS_DEFAULT_WPM = 175  # Words per minute - Standard English speaking rate
TTS_MIN_RATE = 0.5  # Minimum speech rate multiplier
TTS_MAX_RATE = 2.0  # Maximum speech rate multiplier
TTS_MIN_PITCH = 0.5  # Minimum pitch multiplier
TTS_MAX_PITCH = 2.0  # Maximum pitch multiplier
TTS_MIN_RATE_WINDOWS = -10  # Windows SAPI rate range
TTS_MAX_RATE_WINDOWS = 10  # Windows SAPI rate range

# UI Configuration
DEFAULT_TOAST_DURATION_MS = 2000  # Default toast notification duration
TOAST_DURATION_MULTIPLIER_LONG = 2  # Multiplier for long toast messages

# Card Due Date Limits
MIN_CARD_DUE_DAYS = -365  # Can set card due up to 1 year in the past
MAX_CARD_DUE_DAYS = 3650  # Can set card due up to 10 years in the future

# Flag Colors (Anki's internal representation)
FLAG_NONE = 0
FLAG_RED = 1
FLAG_ORANGE = 2
FLAG_GREEN = 3
FLAG_BLUE = 4
FLAG_PINK = 5
FLAG_TURQUOISE = 6
FLAG_PURPLE = 7

# Flag Color Name Mapping
FLAG_COLOR_MAP = {
    "none": FLAG_NONE,
    "red": FLAG_RED,
    "orange": FLAG_ORANGE,
    "green": FLAG_GREEN,
    "blue": FLAG_BLUE,
    "pink": FLAG_PINK,
    "turquoise": FLAG_TURQUOISE,
    "purple": FLAG_PURPLE,
}

# Card Ease Buttons
EASE_AGAIN = 1
EASE_HARD = 2
EASE_GOOD = 3
EASE_EASY = 4

# Card Types (Anki's internal representation)
CARD_TYPE_NEW = 0
CARD_TYPE_LEARNING = 1
CARD_TYPE_REVIEW = 2
CARD_TYPE_RELEARNING = 3

# Card Queue States
QUEUE_NEW = 0
QUEUE_LEARNING = 1
QUEUE_REVIEW = 2
QUEUE_DAY_LEARNING = 3
QUEUE_PREVIEW = 4
QUEUE_SUSPENDED = -1
QUEUE_BURIED = -2
QUEUE_MANUALLY_BURIED = -3

# Default Card Factor (2500 = 250% = default ease)
DEFAULT_CARD_FACTOR = 2500
