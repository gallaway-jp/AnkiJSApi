"""
Unit tests for reviewer_control module
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

from ankidroid_js_api import reviewer_control


@pytest.fixture
def mock_mw():
    """Mock the main window and reviewer using AnkiContext."""
    mw = Mock()
    mw.reviewer = Mock()
    mw.reviewer.state = "question"
    mw.reviewer._showAnswer = Mock()
    mw.reviewer._answerCard = Mock()
    
    with patch('ankidroid_js_api.utils.AnkiContext.get_main_window', return_value=mw):
        with patch('ankidroid_js_api.utils.AnkiContext.get_reviewer', return_value=mw.reviewer):
            yield mw


@pytest.fixture
def mock_card():
    """Mock a card object."""
    card = Mock()
    card.id = 12345
    return card


def test_is_displaying_answer_question_side(mock_mw):
    """Test checking if displaying answer on question side."""
    mock_mw.reviewer.state = "question"
    
    result = reviewer_control.anki_is_displaying_answer()
    
    assert result is False


def test_is_displaying_answer_answer_side(mock_mw):
    """Test checking if displaying answer on answer side."""
    mock_mw.reviewer.state = "answer"
    
    result = reviewer_control.anki_is_displaying_answer()
    
    assert result is True


def test_is_displaying_answer_no_reviewer():
    """Test when reviewer is not available."""
    with patch('ankidroid_js_api.utils.AnkiContext.get_reviewer', return_value=None):
        result = reviewer_control.anki_is_displaying_answer()
        assert result is False


def test_show_answer_success(mock_mw):
    """Test showing answer from question side."""
    mock_mw.reviewer.state = "question"
    
    result = reviewer_control.anki_show_answer()
    
    assert result is True
    mock_mw.reviewer._showAnswer.assert_called_once()


def test_show_answer_already_showing(mock_mw):
    """Test showing answer when already on answer side."""
    mock_mw.reviewer.state = "answer"
    
    result = reviewer_control.anki_show_answer()
    
    # Changed behavior: returns True even if already showing
    assert result is True


def test_show_answer_no_reviewer():
    """Test showing answer when reviewer is not available."""
    with patch('ankidroid_js_api.utils.AnkiContext.get_reviewer', return_value=None):
        result = reviewer_control.anki_show_answer()
        assert result is False


def test_answer_ease_valid(mock_mw, mock_card):
    """Test answering card with valid ease."""
    mock_mw.reviewer.state = "answer"
    
    with patch('ankidroid_js_api.reviewer_control.get_current_card', return_value=mock_card):
        for ease in [1, 2, 3, 4]:
            result = reviewer_control.anki_answer_ease(ease)
            assert result is True
            mock_mw.reviewer._answerCard.assert_called_with(ease)


def test_answer_ease_invalid(mock_mw, mock_card):
    """Test answering card with invalid ease."""
    mock_mw.reviewer.state = "answer"
    
    with patch('ankidroid_js_api.reviewer_control.get_current_card', return_value=mock_card):
        result = reviewer_control.anki_answer_ease(5)
        assert result is False
        
        result = reviewer_control.anki_answer_ease(0)
        assert result is False


def test_answer_ease_on_question(mock_mw, mock_card):
    """Test answering card while on question side."""
    mock_mw.reviewer.state = "question"
    
    with patch('ankidroid_js_api.reviewer_control.get_current_card', return_value=mock_card):
        result = reviewer_control.anki_answer_ease(3)
        assert result is False


def test_answer_ease_no_card(mock_mw):
    """Test answering when no card is present."""
    mock_mw.reviewer.state = "answer"
    
    with patch('ankidroid_js_api.reviewer_control.get_current_card', return_value=None):
        result = reviewer_control.anki_answer_ease(3)
        assert result is False


def test_answer_ease_shortcuts(mock_mw, mock_card):
    """Test the ease shortcut functions."""
    mock_mw.reviewer.state = "answer"
    
    with patch('ankidroid_js_api.reviewer_control.get_current_card', return_value=mock_card):
        # Test ease 1 (Again)
        result = reviewer_control.anki_answer_ease1()
        assert result is True
        mock_mw.reviewer._answerCard.assert_called_with(1)
        
        # Test ease 2 (Hard)
        result = reviewer_control.anki_answer_ease2()
        assert result is True
        mock_mw.reviewer._answerCard.assert_called_with(2)
        
        # Test ease 3 (Good)
        result = reviewer_control.anki_answer_ease3()
        assert result is True
        mock_mw.reviewer._answerCard.assert_called_with(3)
        
        # Test ease 4 (Easy)
        result = reviewer_control.anki_answer_ease4()
        assert result is True
        mock_mw.reviewer._answerCard.assert_called_with(4)
