# SPDX-License-Identifier: MIT
# Copyright (c) 2025 AnkiDroid JS API Desktop Contributors

"""
Reviewer control APIs - control the card reviewer interface.
This module provides programmatic control over Anki's card reviewer:

Features:
    - Check reviewer state (question vs answer side)
    - Flip cards programmatically (show answer)
    - Answer cards with specific ease buttons (1-4)
    - Debug reviewer state for troubleshooting

Reviewer States:
    - "question": Showing the front of the card
    - "answer": Showing the back of the card
    - None: No card is being reviewed

Ease Buttons:
    When answering cards, use these ease values:
    - 1: Again (card failed, will reappear soon)
    - 2: Hard (difficult, shorter interval)
    - 3: Good (standard interval)
    - 4: Easy (confident, longer interval)

Safety:
    - All functions check for reviewer availability
    - Answer functions only work when on answer side
    - Graceful degradation (return False if unavailable)

Usage:
    From JavaScript in card templates:
    >>> // Check if answer is showing
    >>> const onAnswer = await api.ankiIsDisplayingAnswer();
    >>> 
    >>> // Flip to answer side
    >>> if (!onAnswer) {
    ...     await api.ankiShowAnswer();
    >>> }
    >>> 
    >>> // Answer with "Good" (ease 3)
    >>> await api.ankiAnswerEase3();
    >>> 
    >>> // Or use specific ease
    >>> await api.ankiAnswerEase(2);  // Hard

Compatibility:
    - Works with Anki 2.1.50+ (uses internal _showAnswer and _answerCard methods)
    - Tested with all Anki schedulers (V1, V2, V3)

Warning:
    These functions use Anki's internal methods (_showAnswer, _answerCard).
    While stable, they may change in future Anki versions."""

from .card_info import get_current_card
from .utils import log_api_call, AnkiContext


def anki_get_debug_info() -> dict:
    """Get debug information about the reviewer state."""
    reviewer = AnkiContext.get_reviewer()
    if not reviewer:
        return {"error": "No reviewer available"}
    info = {
        "state": reviewer.state,
        "card_id": reviewer.card.id if reviewer.card else None,
        "available_methods": {
            "has_on_show_answer": hasattr(reviewer, 'on_show_answer'),
            "has__showAnswer": hasattr(reviewer, '_showAnswer'),
            "has__linkHandler": hasattr(reviewer, '_linkHandler'),
            "has_on_answer_button": hasattr(reviewer, 'on_answer_button'),
            "has__answerCard": hasattr(reviewer, '_answerCard'),
        }
    }
    return info


def anki_is_displaying_answer() -> bool:
    """Check if the answer side is currently displayed."""
    log_api_call("ankiIsDisplayingAnswer")
    
    reviewer = AnkiContext.get_reviewer()
    if not reviewer:
        return False
    
    return reviewer.state == "answer"


def anki_show_answer() -> bool:
    """Flip the card to show the answer."""
    log_api_call("ankiShowAnswer")
    
    reviewer = AnkiContext.get_reviewer()
    if not reviewer:
        return False
    
    if reviewer.state == "question":
        # Use _showAnswer which we confirmed exists
        reviewer._showAnswer()
        return True
    elif reviewer.state == "answer":
        # Already showing answer
        return True
    
    return False


def anki_answer_ease(ease: int) -> bool:
    """Answer the card with a specific ease button (1-4)."""
    log_api_call(f"ankiAnswerEase{ease}")
    
    reviewer = AnkiContext.get_reviewer()
    if not reviewer:
        return False
    
    card = get_current_card()
    if not card:
        return False
    
    # Validate ease
    if ease not in [1, 2, 3, 4]:
        return False
    
    # Make sure we're on the answer side
    if reviewer.state != "answer":
        # If on question side, don't auto-flip - let the template handle it
        return False
    
    # Answer the card using _answerCard which we confirmed exists
    reviewer._answerCard(ease)
    return True


def anki_answer_ease1() -> bool:
    """Answer the card with 'Again' (ease 1)."""
    return anki_answer_ease(1)


def anki_answer_ease2() -> bool:
    """Answer the card with 'Hard' (ease 2)."""
    return anki_answer_ease(2)


def anki_answer_ease3() -> bool:
    """Answer the card with 'Good' (ease 3)."""
    return anki_answer_ease(3)


def anki_answer_ease4() -> bool:
    """Answer the card with 'Easy' (ease 4)."""
    return anki_answer_ease(4)
