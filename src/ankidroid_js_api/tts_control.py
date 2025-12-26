# SPDX-License-Identifier: MIT
# Copyright (c) 2025 AnkiDroid JS API Desktop Contributors

"""
Text-to-Speech (TTS) control APIs.
This module provides cross-platform text-to-speech functionality using the Strategy pattern.

Architecture:
    - TTSController: Main controller class using strategy pattern
    - TTSStrategy: Abstract base class (see tts_strategies.py)
    - Platform-specific strategies: WindowsTTSStrategy, MacOSTTSStrategy, LinuxTTSStrategy

Features:
    - Cross-platform TTS support (Windows, macOS, Linux)
    - Configurable speech rate and pitch
    - Multi-language support (language codes like "en-US", "ja-JP")
    - Automatic strategy selection based on platform
    - Input sanitization (removes HTML, control characters)
    - Queue mode support (always stops previous speech)

Configuration:
    TTS can be enabled/disabled in config.json:
    {
        "tts": {
            "enabled": true  // Set to false to disable TTS
        }
    }

Limits:
    Speech parameters are validated against constants:
    - Rate: -10 to 10 (TTS_MIN_RATE to TTS_MAX_RATE)
    - Pitch: 0.5 to 2.0 (TTS_MIN_PITCH to TTS_MAX_PITCH)

Usage:
    From JavaScript in card templates:
    >>> await api.ankiTtsSpeak("Hello World", 0);  // Speak text
    >>> await api.ankiTtsSetLanguage("ja-JP");     // Set Japanese
    >>> await api.ankiTtsSetSpeechRate(1.5);       // Faster speech
    >>> await api.ankiTtsSetPitch(1.2);            // Higher pitch
    >>> await api.ankiTtsStop();                   // Stop speaking
    >>> const speaking = await api.ankiTtsIsSpeaking();  // Check status

Platform Notes:
    - Windows: Uses PowerShell and SAPI (Speech API)
    - macOS: Uses native 'say' command
    - Linux: Uses espeak or spd-say (must be installed)"""

from typing import Optional

from .utils import log_api_call, get_config
from .security import InputValidator
from .constants import TTS_MIN_RATE, TTS_MAX_RATE, TTS_MIN_PITCH, TTS_MAX_PITCH
from .tts_strategies import get_tts_strategy, TTSStrategy


class TTSController:
    """Controller for text-to-speech functionality using strategy pattern."""
    
    def __init__(self):
        """Initialize TTS controller with platform-specific strategy."""
        self.language = "en-US"
        self.pitch = 1.0
        self.rate = 1.0
        self.strategy: Optional[TTSStrategy] = get_tts_strategy()
    
    def speak(self, text: str, queue_mode: int = 0) -> bool:
        """Speak text using system TTS."""
        log_api_call("ankiTtsSpeak", {"text": text[:50], "queue_mode": queue_mode})
        
        config = get_config()
        if not config.get("tts", {}).get("enabled", True):
            return False
        
        if not self.strategy:
            # Platform not supported
            return False
        
        # Validate and sanitize input
        text = self.strategy._sanitize_text(text)
        if not text:
            return False
        
        # Always stop current speech before starting new one
        # This prevents multiple TTS instances playing simultaneously
        self.stop()
        
        try:
            return self.strategy.speak(text, rate=self.rate, pitch=self.pitch)
        except Exception as e:
            error_details = {
                "error": str(e),
                "text_length": len(text),
                "rate": self.rate,
                "pitch": self.pitch
            }
            print(f"TTS Error: {error_details}")
            log_api_call("ankiTtsSpeak_error", error_details)
            return False
    
    def set_language(self, language_code: str) -> bool:
        """Set the TTS language."""
        log_api_call("ankiTtsSetLanguage", {"language_code": language_code})
        self.language = language_code
        if self.strategy:
            self.strategy.language = language_code
        return True
    
    def set_pitch(self, pitch: float) -> bool:
        """Set the TTS pitch."""
        log_api_call("ankiTtsSetPitch", {"pitch": pitch})
        # Validate pitch
        pitch = InputValidator.validate_float(pitch, min_val=TTS_MIN_PITCH, max_val=TTS_MAX_PITCH)
        self.pitch = pitch
        return True
    
    def set_speech_rate(self, rate: float) -> bool:
        """Set the TTS speech rate."""
        log_api_call("ankiTtsSetSpeechRate", {"rate": rate})
        # Validate rate
        rate = InputValidator.validate_float(rate, min_val=TTS_MIN_RATE, max_val=TTS_MAX_RATE)
        self.rate = rate
        return True
    
    def is_speaking(self) -> bool:
        """Check if TTS is currently speaking."""
        log_api_call("ankiTtsIsSpeaking")
        
        if not self.strategy:
            return False
        
        # Check if process is still running
        if self.strategy.process and self.strategy.process.poll() is None:
            return True
        
        return False
    
    def stop(self) -> bool:
        """Stop TTS playback."""
        log_api_call("ankiTtsStop")
        
        if self.strategy:
            return self.strategy.stop()
        
        return True


# Global TTS controller instance
_tts_controller = TTSController()


def anki_tts_speak(text: str, queue_mode: int = 0) -> bool:
    """Speak text using text-to-speech."""
    return _tts_controller.speak(text, queue_mode)


def anki_tts_set_language(language_code: str) -> bool:
    """Set the TTS language."""
    return _tts_controller.set_language(language_code)


def anki_tts_set_pitch(pitch: float) -> bool:
    """Set the TTS pitch."""
    return _tts_controller.set_pitch(pitch)


def anki_tts_set_speech_rate(rate: float) -> bool:
    """Set the TTS speech rate."""
    return _tts_controller.set_speech_rate(rate)


def anki_tts_is_speaking() -> bool:
    """Check if TTS is currently speaking."""
    return _tts_controller.is_speaking()


def anki_tts_stop() -> bool:
    """Stop TTS playback."""
    return _tts_controller.stop()


def anki_tts_field_modifier_is_available() -> bool:
    """Check if TTS field modifier is available."""
    log_api_call("ankiTtsFieldModifierIsAvailable")
    # Desktop Anki has its own TTS field modifier
    return True
