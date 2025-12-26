"""
Unit tests for card_info module
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

from ankidroid_js_api import card_info


@pytest.fixture
def mock_mw_card_info():
    """Mock the main window and collection using AnkiContext."""
    mw = Mock()
    mw.col = Mock()
    mw.reviewer = Mock()
    
    # Mock scheduler
    mw.col.sched = Mock()
    mw.col.sched.counts.return_value = (10, 5, 20)  # new, learning, review
    mw.col.sched.today = 100
    
    # Mock decks
    mw.col.decks = Mock()
    mw.col.decks.selected.return_value = 1
    mw.col.decks.name.return_value = "Test::Deck::Name"
    
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
    card.did = 1
    card.type = 2  # review
    card.queue = 2
    card.due = 105
    card.ivl = 30
    card.factor = 2500
    card.reps = 15
    card.lapses = 2
    card.flags = 1  # red flag
    card.mod = 1640000000
    
    # Mock note
    note = Mock()
    note.id = 67890
    note.tags = ["vocab", "important"]
    note.has_tag = lambda tag: tag in note.tags
    card.note.return_value = note
    
    return card


def test_get_new_card_count(mock_mw_card_info):
    """Test getting new card count."""
    count = card_info.anki_get_new_card_count()
    assert count == 10


def test_get_lrn_card_count(mock_mw_card_info):
    """Test getting learning card count."""
    count = card_info.anki_get_lrn_card_count()
    assert count == 5


def test_get_rev_card_count(mock_mw_card_info):
    """Test getting review card count."""
    count = card_info.anki_get_rev_card_count()
    assert count == 20


def test_get_eta(mock_mw_card_info):
    """Test getting ETA."""
    eta = card_info.anki_get_eta()
    # 10 new * 20s + 5 learning * 10s + 20 review * 10s = 450s = 7.5 min
    assert eta == 7


def test_get_card_mark(mock_mw_card_info, mock_card):
    """Test getting card mark status."""
    mock_mw_card_info.reviewer.card = mock_card
    
    # Test marked card
    mock_card.note().tags = ["marked"]
    assert card_info.anki_get_card_mark() is True
    
    # Test unmarked card
    mock_card.note().tags = ["other"]
    assert card_info.anki_get_card_mark() is False


def test_get_card_id(mock_mw_card_info, mock_card):
    """Test getting card ID."""
    mock_mw_card_info.reviewer.card = mock_card
    assert card_info.anki_get_card_id() == 12345


def test_get_card_reps(mock_mw_card_info, mock_card):
    """Test getting card reps."""
    mock_mw_card_info.reviewer.card = mock_card
    assert card_info.anki_get_card_reps() == 15


def test_get_deck_name(mock_mw_card_info, mock_card):
    """Test getting deck name."""
    mock_mw_card_info.reviewer.card = mock_card
    name = card_info.anki_get_deck_name()
    assert name == "Name"  # Should return only the last part


def test_no_current_card(mock_anki_context):
    """Test when no card is currently displayed."""
    mock_anki_context.reviewer.card = None
    
    assert card_info.anki_get_card_id() == 0
    assert card_info.anki_get_card_mark() is False
