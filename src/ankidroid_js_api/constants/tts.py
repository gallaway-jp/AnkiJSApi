# SPDX-License-Identifier: MIT
# Copyright (c) 2025 AnkiDroid JS API Desktop Contributors

"""
Text-to-Speech (TTS) constants for the AnkiDroid JS API.

This module contains configuration for:
- Speech rate limits
- Pitch limits
- Platform-specific settings (Windows SAPI)
"""

# TTS Configuration
TTS_DEFAULT_WPM = 175  # Words per minute - Standard English speaking rate
TTS_MIN_RATE = 0.5  # Minimum speech rate multiplier
TTS_MAX_RATE = 2.0  # Maximum speech rate multiplier
TTS_MIN_PITCH = 0.5  # Minimum pitch multiplier
TTS_MAX_PITCH = 2.0  # Maximum pitch multiplier
TTS_MIN_RATE_WINDOWS = -10  # Windows SAPI rate range
TTS_MAX_RATE_WINDOWS = 10  # Windows SAPI rate range
