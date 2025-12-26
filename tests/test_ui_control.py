"""
Unit tests for ui_control module
"""

import sys
import pytest
from unittest.mock import Mock, MagicMock, patch

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

from ankidroid_js_api import ui_control


@pytest.fixture
def mock_mw():
    """Mock the main window using AnkiContext."""
    mw = Mock()
    mw.isFullScreen = Mock(return_value=False)
    mw.moveToState = Mock()
    mw.onDeckConf = Mock()
    mw.reviewer = Mock()
    mw.reviewer.card = Mock()
    mw.reviewer.card.did = 1
    
    with patch('ankidroid_js_api.utils.AnkiContext.get_main_window', return_value=mw):
        with patch('ankidroid_js_api.utils.AnkiContext.get_reviewer', return_value=mw.reviewer):
            yield mw


@pytest.fixture
def mock_theme_manager():
    """Mock the theme manager."""
    with patch('ankidroid_js_api.ui_control.theme_manager') as tm:
        tm.night_mode = False
        yield tm


@pytest.fixture
def mock_tooltip():
    """Mock the tooltip function."""
    with patch('ankidroid_js_api.ui_control.tooltip') as tooltip_mock:
        yield tooltip_mock


def test_is_in_fullscreen_true(mock_mw):
    """Test checking fullscreen when in fullscreen."""
    mock_mw.isFullScreen.return_value = True
    
    result = ui_control.anki_is_in_fullscreen()
    
    assert result is True
    mock_mw.isFullScreen.assert_called_once()


def test_is_in_fullscreen_false(mock_mw):
    """Test checking fullscreen when not in fullscreen."""
    mock_mw.isFullScreen.return_value = False
    
    result = ui_control.anki_is_in_fullscreen()
    
    assert result is False


def test_is_in_fullscreen_no_mw():
    """Test checking fullscreen when mw is not available."""
    with patch('ankidroid_js_api.utils.AnkiContext.get_main_window', return_value=None):
        result = ui_control.anki_is_in_fullscreen()
        assert result is False


def test_is_topbar_shown(mock_mw):
    """Test checking if topbar is shown."""
    # Desktop always shows topbar
    result = ui_control.anki_is_topbar_shown()
    assert result is True


def test_is_in_night_mode_true(mock_mw, mock_theme_manager):
    """Test checking night mode when enabled."""
    mock_theme_manager.night_mode = True
    
    result = ui_control.anki_is_in_night_mode()
    
    assert result is True


def test_is_in_night_mode_false(mock_mw, mock_theme_manager):
    """Test checking night mode when disabled."""
    mock_theme_manager.night_mode = False
    
    result = ui_control.anki_is_in_night_mode()
    
    assert result is False


def test_enable_horizontal_scrollbar(mock_mw):
    """Test enabling horizontal scrollbar."""
    result = ui_control.anki_enable_horizontal_scrollbar(True)
    assert result is True
    
    result = ui_control.anki_enable_horizontal_scrollbar(False)
    assert result is True


def test_enable_vertical_scrollbar(mock_mw):
    """Test enabling vertical scrollbar."""
    result = ui_control.anki_enable_vertical_scrollbar(True)
    assert result is True
    
    result = ui_control.anki_enable_vertical_scrollbar(False)
    assert result is True


def test_show_navigation_drawer(mock_mw):
    """Test showing navigation drawer (opens deck browser on desktop)."""
    result = ui_control.anki_show_navigation_drawer()
    
    assert result is True
    mock_mw.moveToState.assert_called_once_with("deckBrowser")


def test_show_navigation_drawer_no_mw():
    """Test showing navigation drawer when mw is not available."""
    with patch('ankidroid_js_api.utils.AnkiContext.get_main_window', return_value=None):
        result = ui_control.anki_show_navigation_drawer()
        assert result is False


def test_show_options_menu(mock_mw):
    """Test showing options menu."""
    result = ui_control.anki_show_options_menu()
    
    assert result is True
    mock_mw.onDeckConf.assert_called_once_with(1)


def test_show_options_menu_no_card(mock_mw):
    """Test showing options menu when no card is present."""
    mock_mw.reviewer.card = None
    
    result = ui_control.anki_show_options_menu()
    
    assert result is False


def test_show_toast_enabled(mock_mw, mock_tooltip):
    """Test showing toast when enabled."""
    with patch('ankidroid_js_api.ui_control.get_config') as mock_config:
        mock_config.return_value = {
            "ui": {
                "show_toast_notifications": True,
                "toast_duration_ms": 2000
            }
        }
        
        result = ui_control.anki_show_toast("Hello!", True)
        
        assert result is True
        mock_tooltip.assert_called_once_with("Hello!", period=2000)


def test_show_toast_long_duration(mock_mw, mock_tooltip):
    """Test showing toast with long duration."""
    with patch('ankidroid_js_api.ui_control.get_config') as mock_config:
        mock_config.return_value = {
            "ui": {
                "show_toast_notifications": True,
                "toast_duration_ms": 2000
            }
        }
        
        result = ui_control.anki_show_toast("Important!", False)
        
        assert result is True
        mock_tooltip.assert_called_once_with("Important!", period=4000)


def test_show_toast_disabled(mock_mw, mock_tooltip):
    """Test showing toast when disabled in config."""
    with patch('ankidroid_js_api.ui_control.get_config') as mock_config:
        mock_config.return_value = {
            "ui": {
                "show_toast_notifications": False
            }
        }
        
        result = ui_control.anki_show_toast("Hello!", True)
        
        assert result is False
        mock_tooltip.assert_not_called()


def test_show_toast_no_mw(mock_tooltip):
    """Test showing toast when mw is not available."""
    with patch('ankidroid_js_api.utils.AnkiContext.get_main_window', return_value=None):
        with patch('ankidroid_js_api.ui_control.get_config') as mock_config:
            mock_config.return_value = {
                "ui": {"show_toast_notifications": True}
            }
            
            result = ui_control.anki_show_toast("Hello!", True)
            assert result is False
