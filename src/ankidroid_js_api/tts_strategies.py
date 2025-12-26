# SPDX-License-Identifier: MIT
# Copyright (c) 2025 AnkiDroid JS API Desktop Contributors

"""
Text-to-Speech (TTS) strategy implementations for different platforms.

This module defines an abstract TTS strategy interface and concrete
implementations for Windows, macOS, and Linux platforms.

Architecture:
    - TTSStrategy: Abstract base class defining the interface
    - WindowsTTSStrategy: Uses Windows SAPI (PowerShell + .NET)
    - MacOSTTSStrategy: Uses macOS 'say' command
    - LinuxTTSStrategy: Uses espeak or spd-say

Usage:
    strategy = get_tts_strategy()
    success = strategy.speak("Hello, world!", rate=1.0, pitch=1.0)
    strategy.stop()
"""

import subprocess
import platform
import re
import shutil
from abc import ABC, abstractmethod
from typing import Optional

from .security import InputValidator
from .constants import (
    TTS_MIN_RATE,
    TTS_MAX_RATE,
    TTS_MIN_PITCH,
    TTS_MAX_PITCH,
    TTS_MIN_RATE_WINDOWS,
    TTS_MAX_RATE_WINDOWS,
    MAX_TEXT_LENGTH_TTS,
)


class TTSStrategy(ABC):
    """Abstract base class for text-to-speech strategies.
    
    All platform-specific implementations must inherit from this class
    and implement the abstract methods.
    """
    
    def __init__(self):
        """Initialize the TTS strategy."""
        self.language = "en-US"
        self.is_speaking_flag = False
        self.process: Optional[subprocess.Popen] = None
    
    @abstractmethod
    def speak(self, text: str, rate: float = 1.0, pitch: float = 1.0) -> bool:
        """Speak the given text.
        
        Args:
            text: Text to speak (already sanitized)
            rate: Speech rate multiplier (0.5-2.0)
            pitch: Pitch multiplier (0.5-2.0)
            
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def stop(self) -> bool:
        """Stop any ongoing speech.
        
        Returns:
            True if successful, False otherwise
        """
        pass
    
    def _sanitize_text(self, text: str) -> str:
        """Sanitize text for TTS.
        
        Args:
            text: Raw text input
            
        Returns:
            Sanitized text safe for TTS
        """
        try:
            text = InputValidator.validate_text(
                text,
                max_length=MAX_TEXT_LENGTH_TTS,
                allow_newlines=True
            )
            # Remove problematic characters for TTS
            text = re.sub(r'[^\w\s.,!?;:\-\'\"()]', '', text, flags=re.UNICODE)
            return text
        except (TypeError, ValueError):
            return ""


class WindowsTTSStrategy(TTSStrategy):
    """Windows SAPI text-to-speech strategy using PowerShell."""
    
    def speak(self, text: str, rate: float = 1.0, pitch: float = 1.0) -> bool:
        """Speak using Windows SAPI with secure input handling."""
        # Escape text for PowerShell - use single quotes and escape single quotes
        escaped_text = text.replace("'", "''")
        
        # Convert rate to Windows SAPI range (-10 to 10)
        sapi_rate = int((rate - 1) * 10)
        sapi_rate = max(TTS_MIN_RATE_WINDOWS, min(TTS_MAX_RATE_WINDOWS, sapi_rate))
        
        # Use Base64 encoding for ultimate safety
        import base64
        text_bytes = escaped_text.encode('utf-16le')
        text_b64 = base64.b64encode(text_bytes).decode('ascii')
        
        ps_command = f'''
        Add-Type -AssemblyName System.Speech
        $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
        $synth.Rate = {sapi_rate}
        $text = [System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String('{text_b64}'))
        $synth.Speak($text)
        '''
        
        try:
            self.process = subprocess.Popen(
                ["powershell", "-Command", ps_command],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.is_speaking_flag = True
            return True
        except Exception:
            return False
    
    def stop(self) -> bool:
        """Stop Windows TTS by killing the PowerShell process."""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=1)
            except subprocess.TimeoutExpired:
                self.process.kill()
            except Exception:
                pass
            finally:
                self.process = None
                self.is_speaking_flag = False
        return True


class MacOSTTSStrategy(TTSStrategy):
    """macOS 'say' command text-to-speech strategy."""
    
    def speak(self, text: str, rate: float = 1.0, pitch: float = 1.0) -> bool:
        """Speak using macOS 'say' command."""
        # Convert rate to words per minute (macOS say default is ~175 wpm)
        from .constants import TTS_DEFAULT_WPM
        wpm = int(TTS_DEFAULT_WPM * rate)
        
        try:
            self.process = subprocess.Popen(
                ["say", "-r", str(wpm), text],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.is_speaking_flag = True
            return True
        except FileNotFoundError:
            # 'say' command not available
            return False
        except Exception:
            return False
    
    def stop(self) -> bool:
        """Stop macOS TTS by killing the say process."""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=1)
            except subprocess.TimeoutExpired:
                self.process.kill()
            except Exception:
                pass
            finally:
                self.process = None
                self.is_speaking_flag = False
        
        # Also try killall as backup (in case process reference lost)
        try:
            subprocess.run(["killall", "say"], 
                          stdout=subprocess.DEVNULL, 
                          stderr=subprocess.DEVNULL,
                          timeout=1)
        except Exception:
            pass
        
        return True


class LinuxTTSStrategy(TTSStrategy):
    """Linux text-to-speech strategy using espeak or spd-say."""
    
    def __init__(self):
        """Initialize and detect available TTS engine."""
        super().__init__()
        # Detect which TTS engine is available
        if shutil.which("spd-say"):
            self.engine = "spd-say"
        elif shutil.which("espeak"):
            self.engine = "espeak"
        else:
            self.engine = None
    
    def speak(self, text: str, rate: float = 1.0, pitch: float = 1.0) -> bool:
        """Speak using Linux TTS (espeak or spd-say)."""
        if not self.engine:
            return False
        
        try:
            if self.engine == "spd-say":
                # Convert rate to percentage (-100 to 100, default 0)
                spd_rate = int((rate - 1) * 100)
                spd_rate = max(-100, min(100, spd_rate))
                
                # Convert pitch to range (-100 to 100, default 0)
                spd_pitch = int((pitch - 1) * 100)
                spd_pitch = max(-100, min(100, spd_pitch))
                
                self.process = subprocess.Popen(
                    ["spd-say", "-r", str(spd_rate), "-i", str(spd_pitch), text],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            else:  # espeak
                # Convert rate to words per minute (espeak default is ~175 wpm)
                from .constants import TTS_DEFAULT_WPM
                wpm = int(TTS_DEFAULT_WPM * rate)
                
                # Convert pitch to range (0-99, default 50)
                espeak_pitch = int(50 * pitch)
                espeak_pitch = max(0, min(99, espeak_pitch))
                
                self.process = subprocess.Popen(
                    ["espeak", "-s", str(wpm), "-p", str(espeak_pitch), text],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            
            self.is_speaking_flag = True
            return True
        
        except Exception:
            return False
    
    def stop(self) -> bool:
        """Stop Linux TTS by killing the process."""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=1)
            except subprocess.TimeoutExpired:
                self.process.kill()
            except Exception:
                pass
            finally:
                self.process = None
                self.is_speaking_flag = False
        
        # Also try killall as backup
        if self.engine:
            try:
                subprocess.run(["killall", self.engine],
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL,
                             timeout=1)
            except Exception:
                pass
        
        return True


# Strategy registry
TTS_STRATEGY_REGISTRY = {
    "Windows": WindowsTTSStrategy,
    "Darwin": MacOSTTSStrategy,
    "Linux": LinuxTTSStrategy,
}


def get_tts_strategy() -> Optional[TTSStrategy]:
    """Get the appropriate TTS strategy for the current platform.
    
    Returns:
        TTSStrategy instance or None if platform not supported
    """
    platform_name = platform.system()
    strategy_class = TTS_STRATEGY_REGISTRY.get(platform_name)
    
    if strategy_class:
        return strategy_class()
    return None
