# SPDX-License-Identifier: MIT
# Copyright (c) 2025 AnkiDroid JS API Desktop Contributors

"""
Card action APIs - perform actions on cards.
"""

from typing import Optional
from aqt.operations import CollectionOp
from aqt.utils import tooltip

from .card_info import get_current_card
from .utils import log_api_call, log_error, log_warning, get_config, AnkiContext
from .security import InputValidator
from .constants import (
    FLAG_COLOR_MAP,
    MIN_CARD_DUE_DAYS,
    MAX_CARD_DUE_DAYS,
    DEFAULT_CARD_FACTOR,
    CARD_TYPE_NEW,
    QUEUE_NEW,
)


def anki_mark_card() -> bool:
    """Toggle the mark status of the current card.
    
    Adds or removes the 'marked' tag from the current note.
    The mark persists across all cards from the same note.
    
    Returns:
        bool: True if operation succeeded, False if no card is available.
        
    Example:
        In JavaScript:
        >>> const success = await api.ankiMarkCard();
        >>> if (success) console.log("Card marked/unmarked");
        
    Note:
        This modifies the note, not the card. All cards from the note will show the mark.
    """
    log_api_call("ankiMarkCard")
    
    card = get_current_card()
    if not card:
        return False
    
    note = card.note()
    
    if note.has_tag("marked"):
        note.remove_tag("marked")
    else:
        note.add_tag("marked")
    
    note.flush()
    
    return True


def anki_toggle_flag(flag_color: 'int | str') -> bool:
    """Toggle a flag on the current card.
    
    Args:
        flag_color: Flag color as integer (0-7) or string name:
                    0/'none', 1/'red', 2/'orange', 3/'green',
                    4/'blue', 5/'pink', 6/'turquoise', 7/'purple'
    
    Returns:
        bool: True if operation succeeded, False if no card is available.
        
    Example:
        In JavaScript:
        >>> await api.ankiToggleFlag(1);        // Red flag
        >>> await api.ankiToggleFlag("blue");  // Blue flag
        >>> await api.ankiToggleFlag(0);        // Remove flag
    """
    log_api_call("ankiToggleFlag", {"flag_color": flag_color})
    
    card = get_current_card()
    if not card:
        return False
    
    # If flag_color is already an integer, validate it
    if isinstance(flag_color, int):
        flag_value = InputValidator.validate_integer(flag_color, min_val=0, max_val=7)
    else:
        # Default to 0 (none) for invalid colors
        flag_color_str = str(flag_color).lower()
        flag_value = FLAG_COLOR_MAP.get(flag_color_str, 0)
    
    # Set the flag directly for compatibility with AnkiDroid
    card.flags = flag_value
    card.flush()
    
    return True


def anki_bury_card() -> bool:
    """Bury the current card (hide it until the next day).
    
    Returns:
        bool: True if operation succeeded, False if no card/collection is available.
        
    Example:
        In JavaScript:
        >>> await api.ankiBuryCard();
        
    Note:
        The card will automatically reappear in tomorrow's review queue.
        Other cards from the same note will still appear if scheduled.
    """
    log_api_call("ankiBuryCard")
    
    card = get_current_card()
    col = AnkiContext.get_collection()
    if not card or not col:
        log_warning("No card or collection available to bury")
        return False
    
    try:
        col.sched.bury_cards([card.id])
        
        reviewer = AnkiContext.get_reviewer()
        if reviewer:
            reviewer.nextCard()
        
        return True
    except Exception as e:
        log_error("Failed to bury card", e)
        return False


def anki_bury_note() -> bool:
    """Bury all cards from the current note.
    
    Returns:
        bool: True if operation succeeded, False if no card/collection is available.
        
    Example:
        In JavaScript:
        >>> await api.ankiBuryNote();
        
    Note:
        Buries ALL cards associated with the note (front, back, cloze deletions, etc.).
        All cards will reappear in tomorrow's review queue.
    """
    log_api_call("ankiBuryNote")
    
    card = get_current_card()
    col = AnkiContext.get_collection()
    if not card or not col:
        return False
    
    note = card.note()
    card_ids = [c.id for c in note.cards()]
    
    col.sched.bury_cards(card_ids)
    
    reviewer = AnkiContext.get_reviewer()
    if reviewer:
        reviewer.nextCard()
    
    return True


def anki_suspend_card() -> bool:
    """Suspend the current card (prevent it from appearing in reviews).
    
    Returns:
        bool: True if operation succeeded, False if no card/collection is available.
        
    Example:
        In JavaScript:
        >>> await api.ankiSuspendCard();
        
    Note:
        The card will NOT reappear automatically. You must manually unsuspend it
        in Anki's card browser to resume reviews. Other cards from the same note
        are not affected.
    """
    log_api_call("ankiSuspendCard")
    
    card = get_current_card()
    col = AnkiContext.get_collection()
    if not card or not col:
        log_warning("No card or collection available to suspend")
        return False
    
    try:
        col.sched.suspend_cards([card.id])
        
        reviewer = AnkiContext.get_reviewer()
        if reviewer:
            reviewer.nextCard()
        
        return True
    except Exception as e:
        log_error("Failed to suspend card", e)
        return False


def anki_suspend_note() -> bool:
    """Suspend all cards from the current note.
    
    Returns:
        bool: True if operation succeeded, False if no card/collection is available.
        
    Example:
        In JavaScript:
        >>> await api.ankiSuspendNote();
        
    Note:
        Suspends ALL cards associated with the note (front, back, cloze deletions, etc.).
        Cards will not reappear until manually unsuspended in the card browser.
    """
    log_api_call("ankiSuspendNote")
    
    card = get_current_card()
    col = AnkiContext.get_collection()
    if not card or not col:
        return False
    
    note = card.note()
    card_ids = [c.id for c in note.cards()]
    
    col.sched.suspend_cards(card_ids)
    
    reviewer = AnkiContext.get_reviewer()
    if reviewer:
        reviewer.nextCard()
    
    return True


def anki_reset_progress() -> bool:
    """Reset the review progress of the current card (as if it were new)."""
    log_api_call("ankiResetProgress")
    
    card = get_current_card()
    col = AnkiContext.get_collection()
    mw = AnkiContext.get_main_window()
    if not card or not col:
        log_warning("No card or collection available to reset")
        return False
    
    try:
        # Reset card to new state
        card.type = CARD_TYPE_NEW
        card.queue = QUEUE_NEW
        card.ivl = 0
        card.due = 0
        card.reps = 0
        card.lapses = 0
        card.left = 0
        card.factor = DEFAULT_CARD_FACTOR
        
        card.flush()
        if mw and hasattr(mw, 'requireReset'):
            mw.requireReset()
        
        return True
    except Exception as e:
        log_error("Failed to reset card progress", e)
        return False


def anki_search_card(query: str) -> bool:
    """Search for cards and open the Card Browser with results."""
    log_api_call("ankiSearchCard", {"query": query})
    
    # Validate query
    try:
        query = InputValidator.validate_text(query, max_length=500, allow_newlines=False)
    except (TypeError, ValueError) as e:
        log_error(f"Invalid search query: {e}")
        return False
    
    mw = AnkiContext.get_main_window()
    if not mw:
        log_warning("Main window not available for search")
        return False
    
    try:
        # Open browser with search query
        from aqt import dialogs
        browser = dialogs.open("Browser", mw)
        browser.form.searchEdit.lineEdit().setText(query)
        browser.onSearchActivated()
        
        return True
    except Exception as e:
        log_error("Failed to open browser with search", e)
        return False


def anki_set_card_due(days: int) -> bool:
    """Set the due date of the current card."""
    log_api_call("ankiSetCardDue", {"days": days})
    
    # Validate input (prevent setting dates too far in past/future)
    days = InputValidator.validate_integer(days, MIN_CARD_DUE_DAYS, MAX_CARD_DUE_DAYS)
    
    card = get_current_card()
    col = AnkiContext.get_collection()
    if not card or not col:
        return False
    
    # Set the new due date
    card.due = col.sched.today + days
    card.flush()
    
    return True
