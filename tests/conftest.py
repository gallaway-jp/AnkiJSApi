"""
Pytest configuration and shared fixtures.
"""

import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Mock Anki modules before any imports
sys.modules['aqt'] = MagicMock()
sys.modules['aqt.utils'] = MagicMock()
sys.modules['aqt.qt'] = MagicMock()
sys.modules['anki'] = MagicMock()
sys.modules['anki.cards'] = MagicMock()
sys.modules['anki.notes'] = MagicMock()
sys.modules['anki.collection'] = MagicMock()


@pytest.fixture
def mock_mw():
    """Create a mock Anki main window (mw).
    
    This fixture provides a fully configured mock of Anki's main window
    with common attributes and methods used throughout the codebase.
    """
    mw = Mock()
    mw.col = Mock()
    mw.reviewer = Mock()
    mw.reviewer.web = Mock()
    mw.reviewer.card = None
    mw.reviewer.state = "question"
    mw.state = "review"
    
    # Reset method
    def reset():
        mw.reset.called = True
    mw.reset = Mock(side_effect=reset)
    
    return mw


@pytest.fixture
def mock_card():
    """Create a mock Anki card with typical attributes.
    
    This fixture provides a card with default values that can be
    overridden in individual tests as needed.
    """
    card = Mock()
    card.id = 1234567890
    card.nid = 9876543210
    card.did = 1
    card.ord = 0
    card.mod = 1234567890
    card.usn = -1
    card.type = 0
    card.queue = 0
    card.due = 0
    card.ivl = 0
    card.factor = 2500
    card.reps = 0
    card.lapses = 0
    card.left = 1001
    card.odue = 0
    card.odid = 0
    card.flags = 0
    card.data = ""
    
    # Mock note
    note = Mock()
    note.tags = []
    note.add_tag = Mock()
    note.remove_tag = Mock()
    note.flush = Mock()
    card.note = Mock(return_value=note)
    
    # Mock collection methods
    card.col = Mock()
    card.col.update_card = Mock()
    card.col.flush = Mock()
    
    return card


@pytest.fixture
def mock_reviewer(mock_mw):
    """Create a mock Anki reviewer.
    
    This fixture provides a reviewer instance with web interface
    for testing JavaScript interaction.
    """
    reviewer = Mock()
    reviewer.web = Mock()
    reviewer.web.eval = Mock()
    reviewer.card = None
    reviewer.state = "question"
    reviewer.mw = mock_mw
    
    return reviewer


@pytest.fixture
def mock_collection():
    """Create a mock Anki collection.
    
    This fixture provides a collection with common methods
    for card and note operations.
    """
    col = Mock()
    col.findCards = Mock(return_value=[])
    col.findNotes = Mock(return_value=[])
    col.getCard = Mock()
    col.getNote = Mock()
    col.update_card = Mock()
    col.update_note = Mock()
    col.flush = Mock()
    col.tags = Mock()
    col.tags.all = Mock(return_value=["tag1", "tag2"])
    
    return col


@pytest.fixture
def mock_anki_context(mock_mw):
    """Mock AnkiContext to return test mocks.
    
    This fixture patches AnkiContext.get_* methods to return our mocks,
    allowing tests to work without a real Anki instance.
    
    Usage:
        def test_something(mock_anki_context):
            # AnkiContext.get_main_window() now returns mock_mw
            result = some_function_using_anki_context()
            assert result == expected
    """
    with patch('ankidroid_js_api.utils.AnkiContext.get_main_window', return_value=mock_mw):
        with patch('ankidroid_js_api.utils.AnkiContext.get_collection', return_value=mock_mw.col):
            with patch('ankidroid_js_api.utils.AnkiContext.get_reviewer', return_value=mock_mw.reviewer):
                with patch('ankidroid_js_api.utils.AnkiContext.get_addon_manager', return_value=mock_mw.addonManager if hasattr(mock_mw, 'addonManager') else None):
                    yield mock_mw
