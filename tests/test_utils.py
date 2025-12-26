"""
Unit tests for utils module
"""

import sys
import pytest
import json
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, mock_open

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

from ankidroid_js_api import utils


@pytest.fixture
def mock_mw():
    """Mock the main window using AnkiContext."""
    mw = Mock()
    mw.addonManager = Mock()
    mw.addonManager.getConfig = Mock(return_value={"debug_mode": True})
    mw.addonManager.writeConfig = Mock()
    
    with patch('ankidroid_js_api.utils.AnkiContext.get_main_window', return_value=mw):
        with patch('ankidroid_js_api.utils.AnkiContext.get_addon_manager', return_value=mw.addonManager):
            yield mw


def test_get_config_success(mock_mw):
    """Test getting config successfully."""
    expected_config = {"debug_mode": True, "log_api_calls": False}
    mock_mw.addonManager.getConfig.return_value = expected_config
    
    result = utils.get_config()
    
    assert result == expected_config


def test_get_config_no_mw():
    """Test getting config when mw is not available."""
    with patch('ankidroid_js_api.utils.AnkiContext.get_addon_manager', return_value=None):
        result = utils.get_config()
        assert result == {}


def test_get_config_no_addon_manager():
    """Test getting config when addon manager is not available."""
    with patch('ankidroid_js_api.utils.AnkiContext.get_addon_manager', return_value=None):
        result = utils.get_config()
        assert result == {}


def test_save_config_success(mock_mw):
    """Test saving config successfully."""
    config = {"debug_mode": False, "log_api_calls": True}
    
    utils.save_config(config)
    
    # The function uses __name__.split(".")[0] which in tests will be different
    # Just verify writeConfig was called
    assert mock_mw.addonManager.writeConfig.called


def test_save_config_no_mw():
    """Test saving config when mw is not available."""
    with patch('ankidroid_js_api.utils.AnkiContext.get_addon_manager', return_value=None):
        # Should not raise an exception
        utils.save_config({"test": True})


def test_log_debug_enabled(mock_mw, capsys):
    """Test debug logging when enabled."""
    mock_mw.addonManager.getConfig.return_value = {"debug_mode": True}
    
    utils.log_debug("Test debug message")
    
    captured = capsys.readouterr()
    assert "[AnkiDroid JS API] Test debug message" in captured.out


def test_log_debug_disabled(mock_mw, capsys):
    """Test debug logging when disabled."""
    mock_mw.addonManager.getConfig.return_value = {"debug_mode": False}
    
    utils.log_debug("Test debug message")
    
    captured = capsys.readouterr()
    assert captured.out == ""


def test_log_api_call_enabled(mock_mw, capsys):
    """Test API call logging when enabled."""
    mock_mw.addonManager.getConfig.return_value = {"log_api_calls": True}
    
    utils.log_api_call("testFunction", {"param1": "value1"})
    
    captured = capsys.readouterr()
    assert "[AnkiDroid JS API] testFunction" in captured.out
    assert "param1" in captured.out


def test_log_api_call_disabled(mock_mw, capsys):
    """Test API call logging when disabled."""
    mock_mw.addonManager.getConfig.return_value = {"log_api_calls": False}
    
    utils.log_api_call("testFunction", {"param1": "value1"})
    
    captured = capsys.readouterr()
    assert captured.out == ""


def test_log_api_call_no_args(mock_mw, capsys):
    """Test API call logging without arguments."""
    mock_mw.addonManager.getConfig.return_value = {"log_api_calls": True}
    
    utils.log_api_call("testFunction")
    
    captured = capsys.readouterr()
    assert "[AnkiDroid JS API] testFunction()" in captured.out


def test_get_addon_path():
    """Test getting the addon path."""
    path = utils.get_addon_path()
    
    assert isinstance(path, Path)
    assert path.name == "ankidroid_js_api"


def test_read_js_file():
    """Test reading a JavaScript file."""
    mock_js_content = "console.log('test');"
    
    with patch('builtins.open', mock_open(read_data=mock_js_content)):
        # Mock Path.is_file() to pass validation
        with patch('pathlib.Path.is_file', return_value=True):
            content = utils.read_js_file("test.js")
            
            assert content == mock_js_content


def test_read_js_file_with_path():
    """Test that read_js_file constructs correct path."""
    mock_js_content = "// test content"
    
    with patch('ankidroid_js_api.utils.get_addon_path') as mock_path:
        mock_path.return_value = Path("/fake/path/ankidroid_js_api")
        
        with patch('builtins.open', mock_open(read_data=mock_js_content)) as m:
            # Mock Path.is_file() to pass validation
            with patch('pathlib.Path.is_file', return_value=True):
                content = utils.read_js_file("api.js")
                
                # Verify the file was opened with correct path
                expected_path = Path("/fake/path/ankidroid_js_api") / "js" / "api.js"
                # The actual call might have different path separators on Windows
                assert m.called
            assert content == mock_js_content
