"""
Unit tests for tag_manager module
"""

import sys
import pytest
import json
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

from ankidroid_js_api import tag_manager


@pytest.fixture
def mock_mw():
    """Mock the main window using AnkiContext."""
    mw = Mock()
    mw.requireReset = Mock()
    mw.col = Mock()
    
    with patch('ankidroid_js_api.utils.AnkiContext.get_main_window', return_value=mw):
        with patch('ankidroid_js_api.utils.AnkiContext.get_collection', return_value=mw.col):
            yield mw


@pytest.fixture
def mock_card():
    """Mock a card with a note."""
    card = Mock()
    note = Mock()
    note.tags = ["tag1", "tag2"]
    note.flush = Mock()
    card.note.return_value = note
    return card


def test_set_note_tags(mock_mw, mock_card):
    """Test setting note tags."""
    with patch('ankidroid_js_api.tag_manager.get_current_card', return_value=mock_card):
        result = tag_manager.anki_set_note_tags(["new_tag", "another tag"])
        
        assert result is True
        assert mock_card.note().tags == ["new_tag", "another_tag"]
        mock_card.note().flush.assert_called_once()
        mock_mw.requireReset.assert_called_once()


def test_set_note_tags_with_spaces(mock_mw, mock_card):
    """Test that spaces in tags are converted to underscores."""
    with patch('ankidroid_js_api.tag_manager.get_current_card', return_value=mock_card):
        result = tag_manager.anki_set_note_tags(["multi word tag"])
        
        assert result is True
        assert mock_card.note().tags == ["multi_word_tag"]


def test_get_note_tags(mock_mw, mock_card):
    """Test getting note tags."""
    with patch('ankidroid_js_api.tag_manager.get_current_card', return_value=mock_card):
        result = tag_manager.anki_get_note_tags()
        
        tags = json.loads(result)
        assert tags == ["tag1", "tag2"]


def test_get_note_tags_no_card():
    """Test getting tags when no card is present."""
    with patch('ankidroid_js_api.tag_manager.get_current_card', return_value=None):
        result = tag_manager.anki_get_note_tags()
        
        tags = json.loads(result)
        assert tags == []
