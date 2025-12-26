"""
Unit tests for card_actions module
"""

import sys
import pytest
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

from ankidroid_js_api import card_actions


@pytest.fixture
def mock_mw():
    """Mock the main window using AnkiContext."""
    mw = Mock()
    mw.requireReset = Mock()
    mw.col = Mock()
    mw.col.sched = Mock()
    mw.reviewer = Mock()
    
    with patch('ankidroid_js_api.utils.AnkiContext.get_main_window', return_value=mw):
        with patch('ankidroid_js_api.utils.AnkiContext.get_collection', return_value=mw.col):
            with patch('ankidroid_js_api.utils.AnkiContext.get_reviewer', return_value=mw.reviewer):
                yield mw


@pytest.fixture
def mock_card():
    """Mock a card object."""
    card = Mock()
    card.id = 12345
    card.nid = 67890
    card.flags = 0
    card.set_user_flag = Mock()
    card.flush = Mock()
    
    # Mock note
    note = Mock()
    note.id = 67890
    note.tags = ["vocab"]
    note.has_tag = lambda tag: tag in note.tags
    note.add_tag = Mock(side_effect=lambda tag: note.tags.append(tag))
    note.remove_tag = Mock(side_effect=lambda tag: note.tags.remove(tag) if tag in note.tags else None)
    note.flush = Mock()
    note.cards = Mock(return_value=[card])
    card.note.return_value = note
    
    return card


def test_mark_card_add_mark(mock_mw, mock_card):
    """Test marking an unmarked card."""
    with patch('ankidroid_js_api.card_actions.get_current_card', return_value=mock_card):
        mock_card.note().tags = []
        
        result = card_actions.anki_mark_card()
        
        assert result is True
        mock_card.note().add_tag.assert_called_once_with("marked")
        mock_card.note().flush.assert_called_once()
        # requireReset removed for compatibility


def test_mark_card_remove_mark(mock_mw, mock_card):
    """Test unmarking a marked card."""
    with patch('ankidroid_js_api.card_actions.get_current_card', return_value=mock_card):
        mock_card.note().tags = ["marked"]
        
        result = card_actions.anki_mark_card()
        
        assert result is True
        mock_card.note().remove_tag.assert_called_once_with("marked")


def test_mark_card_no_card(mock_mw):
    """Test marking when no card is present."""
    with patch('ankidroid_js_api.card_actions.get_current_card', return_value=None):
        result = card_actions.anki_mark_card()
        assert result is False


def test_toggle_flag_colors(mock_mw, mock_card):
    """Test toggling different flag colors."""
    with patch('ankidroid_js_api.card_actions.get_current_card', return_value=mock_card):
        # Test each flag color
        flag_tests = [
            ("red", 1),
            ("orange", 2),
            ("green", 3),
            ("blue", 4),
            ("pink", 5),
            ("turquoise", 6),
            ("purple", 7),
            ("none", 0),
        ]
        
        for color, expected_value in flag_tests:
            result = card_actions.anki_toggle_flag(color)
            assert result is True
            # Now uses flags property directly instead of set_user_flag
            assert mock_card.flags == expected_value
            mock_card.flush.assert_called()


def test_toggle_flag_invalid_color(mock_mw, mock_card):
    """Test toggling with invalid color defaults to none."""
    with patch('ankidroid_js_api.card_actions.get_current_card', return_value=mock_card):
        result = card_actions.anki_toggle_flag("invalid")
        assert result is True
        # Now uses flags property, defaults to 0 for invalid
        assert mock_card.flags == 0
        mock_card.flush.assert_called()


def test_bury_card(mock_mw, mock_card):
    """Test burying a card."""
    with patch('ankidroid_js_api.card_actions.get_current_card', return_value=mock_card):
        result = card_actions.anki_bury_card()
        
        assert result is True
        mock_mw.col.sched.bury_cards.assert_called_once_with([12345])
        mock_mw.reviewer.nextCard.assert_called_once()


def test_bury_note(mock_mw, mock_card):
    """Test burying all cards in a note."""
    card2 = Mock()
    card2.id = 12346
    mock_card.note().cards.return_value = [mock_card, card2]
    
    with patch('ankidroid_js_api.card_actions.get_current_card', return_value=mock_card):
        result = card_actions.anki_bury_note()
        
        assert result is True
        mock_mw.col.sched.bury_cards.assert_called_once_with([12345, 12346])


def test_suspend_card(mock_mw, mock_card):
    """Test suspending a card."""
    with patch('ankidroid_js_api.card_actions.get_current_card', return_value=mock_card):
        result = card_actions.anki_suspend_card()
        
        assert result is True
        mock_mw.col.sched.suspend_cards.assert_called_once_with([12345])


def test_suspend_note(mock_mw, mock_card):
    """Test suspending all cards in a note."""
    card2 = Mock()
    card2.id = 12346
    mock_card.note().cards.return_value = [mock_card, card2]
    
    with patch('ankidroid_js_api.card_actions.get_current_card', return_value=mock_card):
        result = card_actions.anki_suspend_note()
        
        assert result is True
        mock_mw.col.sched.suspend_cards.assert_called_once_with([12345, 12346])


def test_reset_progress(mock_mw, mock_card):
    """Test resetting card progress."""
    with patch('ankidroid_js_api.card_actions.get_current_card', return_value=mock_card):
        result = card_actions.anki_reset_progress()
        
        assert result is True
        assert mock_card.type == 0
        assert mock_card.queue == 0
        assert mock_card.ivl == 0
        assert mock_card.due == 0
        assert mock_card.reps == 0
        assert mock_card.lapses == 0
        assert mock_card.left == 0
        assert mock_card.factor == 2500
        mock_card.flush.assert_called_once()


def test_search_card(mock_mw):
    """Test searching for cards."""
    with patch('aqt.dialogs') as mock_dialogs:
        mock_browser = Mock()
        mock_browser.form.searchEdit.lineEdit.return_value.setText = Mock()
        mock_browser.onSearchActivated = Mock()
        mock_dialogs.open.return_value = mock_browser
        
        result = card_actions.anki_search_card("tag:difficult")
        
        assert result is True
        mock_dialogs.open.assert_called_once_with("Browser", mock_mw)
        mock_browser.form.searchEdit.lineEdit().setText.assert_called_once_with("tag:difficult")
        mock_browser.onSearchActivated.assert_called_once()


def test_set_card_due(mock_mw, mock_card):
    """Test setting card due date."""
    mock_mw.col.sched.today = 100
    
    with patch('ankidroid_js_api.card_actions.get_current_card', return_value=mock_card):
        result = card_actions.anki_set_card_due(7)
        
        assert result is True
        assert mock_card.due == 107
        mock_card.flush.assert_called_once()


def test_set_card_due_clamps_values(mock_mw, mock_card):
    """Test that due date is validated to valid range."""
    mock_mw.col.sched.today = 100
    
    with patch('ankidroid_js_api.card_actions.get_current_card', return_value=mock_card):
        # Test negative value (within valid range -365 to 3650)
        result = card_actions.anki_set_card_due(-5)
        assert result is True
        assert mock_card.due == 95  # today (100) + days (-5)
        
        # Test large value within range
        result = card_actions.anki_set_card_due(100)
        assert result is True
        assert mock_card.due == 200  # today (100) + days (100)
