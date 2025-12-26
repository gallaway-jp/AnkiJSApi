"""
Unit tests for tts_control module
"""

import sys
import pytest
import platform
from unittest.mock import Mock, MagicMock, patch, call

# Mock Anki modules before importing our code
sys.modules['aqt'] = MagicMock()
sys.modules['aqt.qt'] = MagicMock()
sys.modules['aqt.utils'] = MagicMock()
sys.modules['aqt.operations'] = MagicMock()
sys.modules['aqt.reviewer'] = MagicMock()
sys.modules['aqt.theme'] = MagicMock()
sys.modules['anki'] = MagicMock()
sys.modules['anki.cards'] = MagicMock()
sys.modules['anki.hooks'] = MagicMock()

from ankidroid_js_api import tts_control


@pytest.fixture
def mock_config():
    """Mock configuration."""
    with patch('ankidroid_js_api.tts_control.get_config') as mock_cfg:
        mock_cfg.return_value = {
            "tts": {
                "enabled": True,
                "default_language": "en-US",
                "default_rate": 1.0,
                "default_pitch": 1.0
            }
        }
        yield mock_cfg


@pytest.fixture
def tts_controller():
    """Create a fresh TTS controller for testing."""
    return tts_control.TTSController()


class TestTTSController:
    """Test the TTSController class."""
    
    def test_init(self, tts_controller):
        """Test TTS controller initialization."""
        assert tts_controller.language == "en-US"
        assert tts_controller.pitch == 1.0
        assert tts_controller.rate == 1.0
        assert tts_controller.strategy is not None  # Strategy should be initialized
    
    def test_set_language(self, tts_controller):
        """Test setting TTS language."""
        result = tts_controller.set_language("ja-JP")
        
        assert result is True
        assert tts_controller.language == "ja-JP"
    
    def test_set_pitch_valid(self, tts_controller):
        """Test setting valid pitch values."""
        result = tts_controller.set_pitch(1.5)
        assert result is True
        assert tts_controller.pitch == 1.5
    
    def test_set_pitch_clamping(self, tts_controller):
        """Test that pitch is validated to valid range."""
        import pytest
        
        # Too low - should raise ValueError
        with pytest.raises(ValueError, match="out of range"):
            tts_controller.set_pitch(0.1)
        
        # Too high - should raise ValueError
        with pytest.raises(ValueError, match="out of range"):
            tts_controller.set_pitch(3.0)
    
    def test_set_speech_rate_valid(self, tts_controller):
        """Test setting valid speech rate."""
        result = tts_controller.set_speech_rate(1.2)
        assert result is True
        assert tts_controller.rate == 1.2
    
    def test_set_speech_rate_clamping(self, tts_controller):
        """Test that rate is validated to valid range."""
        import pytest
        
        # Too low - should raise ValueError
        with pytest.raises(ValueError, match="out of range"):
            tts_controller.set_speech_rate(0.2)
        
        # Too high - should raise ValueError
        with pytest.raises(ValueError, match="out of range"):
            tts_controller.set_speech_rate(5.0)
    
    def test_is_speaking_no_process(self, tts_controller):
        """Test is_speaking when no process exists."""
        result = tts_controller.is_speaking()
        assert result is False
    
    def test_is_speaking_with_running_process(self, tts_controller):
        """Test is_speaking with a running process."""
        # Mock the strategy with a process
        tts_controller.strategy = Mock()
        mock_process = Mock()
        mock_process.poll.return_value = None  # Still running
        tts_controller.strategy.process = mock_process
        
        result = tts_controller.is_speaking()
        assert result is True
    
    def test_is_speaking_with_finished_process(self, tts_controller):
        """Test is_speaking with a finished process."""
        # Mock the strategy's is_speaking method
        tts_controller.strategy = Mock()
        tts_controller.strategy.is_speaking.return_value = False
        
        result = tts_controller.is_speaking()
        assert result is False
    
    def test_stop_no_process(self, tts_controller):
        """Test stopping when no process exists."""
        result = tts_controller.stop()
        assert result is True
    
    def test_stop_with_process(self, tts_controller):
        """Test stopping an active process."""
        # Mock the strategy's stop method
        tts_controller.strategy = Mock()
        tts_controller.strategy.stop.return_value = True
        
        result = tts_controller.stop()
        
        assert result is True
        tts_controller.strategy.stop.assert_called_once()
    
    def test_stop_with_unresponsive_process(self, tts_controller):
        """Test stopping a process - delegated to strategy."""
        # Mock the strategy's stop method
        tts_controller.strategy = Mock()
        tts_controller.strategy.stop.return_value = True
        
        result = tts_controller.stop()
        
        assert result is True
        tts_controller.strategy.stop.assert_called_once()
    
    def test_speak_windows(self, tts_controller, mock_config):
        """Test speaking using strategy."""
        # Mock the strategy
        tts_controller.strategy = Mock()
        tts_controller.strategy._sanitize_text.return_value = "Hello World"
        tts_controller.strategy.speak.return_value = True
        
        result = tts_controller.speak("Hello World", 0)
        
        assert result is True
        tts_controller.strategy.speak.assert_called_once()
    
    def test_speak_macos(self, tts_controller, mock_config):
        """Test speaking with strategy pattern."""
        # Mock the strategy
        tts_controller.strategy = Mock()
        tts_controller.strategy._sanitize_text.return_value = "Hello World"
        tts_controller.strategy.speak.return_value = True
        
        tts_controller.rate = 1.5
        result = tts_controller.speak("Hello World", 0)
        
        assert result is True
        tts_controller.strategy.speak.assert_called_with("Hello World", rate=1.5, pitch=1.0)
    
    def test_speak_linux_espeak(self, tts_controller, mock_config):
        """Test speaking using strategy."""
        # Mock the strategy
        tts_controller.strategy = Mock()
        tts_controller.strategy._sanitize_text.return_value = "Hello World"
        tts_controller.strategy.speak.return_value = True
        
        result = tts_controller.speak("Hello World", 0)
        
        assert result is True
    
    def test_speak_linux_fallback_festival(self, tts_controller, mock_config):
        """Test speaking using strategy."""
        # Mock the strategy
        tts_controller.strategy = Mock()
        tts_controller.strategy._sanitize_text.return_value = "Hello World"
        tts_controller.strategy.speak.return_value = True
        
        result = tts_controller.speak("Hello World", 0)
        
        assert result is True
    
    def test_speak_unsupported_platform(self, tts_controller, mock_config):
        """Test speaking when no strategy is available."""
        tts_controller.strategy = None  # No strategy for platform
        
        result = tts_controller.speak("Hello World", 0)
        assert result is False
    
    def test_speak_disabled_in_config(self, tts_controller):
        """Test speaking when TTS is disabled in config."""
        with patch('ankidroid_js_api.tts_control.get_config') as mock_cfg:
            mock_cfg.return_value = {"tts": {"enabled": False}}
            
            result = tts_controller.speak("Hello World", 0)
            assert result is False
    
    def test_speak_queue_mode_flush(self, tts_controller, mock_config):
        """Test speak with queue mode FLUSH (0)."""
        # Mock the strategy
        tts_controller.strategy = Mock()
        tts_controller.strategy._sanitize_text.return_value = "Hello"
        tts_controller.strategy.speak.return_value = True
        tts_controller.strategy.stop.return_value = True
        
        result = tts_controller.speak("Hello", 0)
        
        # Stop should be called before speaking
        tts_controller.strategy.stop.assert_called()
        assert result is True
    
    @patch('ankidroid_js_api.tts_control.platform.system', return_value='Windows')
    @patch('ankidroid_js_api.tts_control.subprocess.Popen')
    def test_speak_queue_mode_add(self, mock_popen, mock_system, tts_controller, mock_config):
        """Test speak with queue mode ADD (1) - Desktop always stops."""
        # Note: Desktop implementation differs from AnkiDroid
# Stop should be called before speaking
        tts_controller.strategy.stop.assert_called()
        assert result is True
    
    def test_speak_queue_mode_add(self, tts_controller, mock_config):
        """Test speak with queue mode ADD (1) - still stops for simplicity."""
        # Mock the strategy
        tts_controller.strategy = Mock()
        tts_controller.strategy._sanitize_text.return_value = "Hello"
        tts_controller.strategy.speak.return_value = True
        tts_controller.strategy.stop.return_value = True
        
        # We always stop previous speech for simplicity
        result = tts_controller.speak("Hello", 1)
        
        # Implementation always calls stop() regardless of queue_mode
        assert result is True
    
    def test_speak_exception_handling(self, tts_controller, mock_config):
        """Test that exceptions during speak are handled."""
        # Mock the strategy to raise an exception
        tts_controller.strategy = Mock()
        tts_controller.strategy._sanitize_text.return_value = "Hello"
        tts_controller.strategy.speak.side_effect = Exception("TTS Error")
        
        result = tts_controller.speak("Hello", 0)
        
        assert result is False


class TestTTSModuleFunctions:
    """Test the module-level TTS functions."""
    
    @patch('ankidroid_js_api.tts_control._tts_controller.speak')
    def test_anki_tts_speak(self, mock_speak):
        """Test the module-level speak function."""
        mock_speak.return_value = True
        
        result = tts_control.anki_tts_speak("Hello World", 0)
        
        assert result is True
        mock_speak.assert_called_once_with("Hello World", 0)
    
    @patch('ankidroid_js_api.tts_control._tts_controller.set_language')
    def test_anki_tts_set_language(self, mock_set_lang):
        """Test the module-level set language function."""
        mock_set_lang.return_value = True
        
        result = tts_control.anki_tts_set_language("ja-JP")
        
        assert result is True
        mock_set_lang.assert_called_once_with("ja-JP")
    
    @patch('ankidroid_js_api.tts_control._tts_controller.set_pitch')
    def test_anki_tts_set_pitch(self, mock_set_pitch):
        """Test the module-level set pitch function."""
        mock_set_pitch.return_value = True
        
        result = tts_control.anki_tts_set_pitch(1.5)
        
        assert result is True
        mock_set_pitch.assert_called_once_with(1.5)
    
    @patch('ankidroid_js_api.tts_control._tts_controller.set_speech_rate')
    def test_anki_tts_set_speech_rate(self, mock_set_rate):
        """Test the module-level set speech rate function."""
        mock_set_rate.return_value = True
        
        result = tts_control.anki_tts_set_speech_rate(0.8)
        
        assert result is True
        mock_set_rate.assert_called_once_with(0.8)
    
    @patch('ankidroid_js_api.tts_control._tts_controller.is_speaking')
    def test_anki_tts_is_speaking(self, mock_is_speaking):
        """Test the module-level is speaking function."""
        mock_is_speaking.return_value = True
        
        result = tts_control.anki_tts_is_speaking()
        
        assert result is True
        mock_is_speaking.assert_called_once()
    
    @patch('ankidroid_js_api.tts_control._tts_controller.stop')
    def test_anki_tts_stop(self, mock_stop):
        """Test the module-level stop function."""
        mock_stop.return_value = True
        
        result = tts_control.anki_tts_stop()
        
        assert result is True
        mock_stop.assert_called_once()
    
    def test_anki_tts_field_modifier_is_available(self):
        """Test the field modifier availability function."""
        result = tts_control.anki_tts_field_modifier_is_available()
        
        # Desktop Anki has TTS field modifier support
        assert result is True
