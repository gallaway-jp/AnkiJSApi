# SPDX-License-Identifier: MIT
# Copyright (c) 2025 AnkiDroid JS API Desktop Contributors

"""
Card-related constants for the AnkiDroid JS API.

This module contains definitions for:
- Card types (new, learning, review)
- Card queue states (suspended, buried, etc.)
- Card ease buttons
- Card properties (flags, factors, due dates)
"""

# Card Time Estimates (seconds)
NEW_CARD_TIME_ESTIMATE_SEC = 20  # Average time to review a new card
LEARNING_CARD_TIME_ESTIMATE_SEC = 10  # Average time to review a learning card
REVIEW_CARD_TIME_ESTIMATE_SEC = 10  # Average time to review a review card

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
