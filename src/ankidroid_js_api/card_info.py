# SPDX-License-Identifier: MIT
# Copyright (c) 2025 AnkiDroid JS API Desktop Contributors

"""
Card information APIs - retrieve information about the current card.

This module provides read-only access to card and deck statistics:
- Card counts (new, learning, review)
- Card metadata (ID, type, interval, ease, flags)
- Review statistics (reps, lapses, due date)
- Time estimates (ETA for remaining reviews)

All functions return safe defaults (0, False, empty string) when:
- No card is currently being reviewed
- Anki collection is not available
- Reviewer is not active

Example Usage in JavaScript:
    const newCount = await api.ankiGetNewCardCount();
    const cardId = await api.ankiGetCardId();
    const isMarked = await api.ankiGetCardMark();
    const eta = await api.ankiGetETA();  // Minutes remaining

Compatibility:
    - Works with all Anki schedulers (V1, V2, V3)
    - Returns 0 for unavailable statistics
    - Thread-safe (called from main thread only)
"""

from typing import Optional, Any, Union
from anki.cards import Card

from .utils import log_api_call, log_warning, log_error, require_collection, AnkiContext
from .constants import (
    NEW_CARD_TIME_ESTIMATE_SEC,
    LEARNING_CARD_TIME_ESTIMATE_SEC,
    REVIEW_CARD_TIME_ESTIMATE_SEC,
    DEFAULT_CARD_FACTOR,
)

# Alias for clarity
CARD_DEFAULT_EASE_FACTOR = DEFAULT_CARD_FACTOR


def get_current_card() -> Optional[Card]:
    """Get the currently displayed card in the reviewer."""
    reviewer = AnkiContext.get_reviewer()
    if reviewer and reviewer.card:
        return reviewer.card
    return None


def _get_card_property(
    property_name: str,
    api_name: str,
    default: Union[int, bool, str] = 0
) -> Any:
    """Generic card property accessor.
    
    Args:
        property_name: Card attribute name (e.g., 'id', 'nid', 'type')
        api_name: API function name for logging (e.g., 'ankiGetCardId')
        default: Default value if card unavailable
        
    Returns:
        Card property value or default
    """
    log_api_call(api_name)
    
    card = get_current_card()
    if not card:
        return default
    
    return getattr(card, property_name, default)


@require_collection(default=0)
def anki_get_new_card_count() -> int:
    """Get the count of new cards remaining in the deck."""
    log_api_call("ankiGetNewCardCount")
    
    try:
        col = AnkiContext.get_collection()
        if not col:
            return 0
        deck_id = col.decks.selected()
        return col.sched.counts()[0]  # new count
    except Exception as e:
        log_error("Failed to get new card count", e)
        return 0


@require_collection(default=0)
def anki_get_lrn_card_count() -> int:
    """Get the count of learning cards."""
    log_api_call("ankiGetLrnCardCount")
    
    try:
        col = AnkiContext.get_collection()
        if not col:
            return 0
        return col.sched.counts()[1]  # learning count
    except Exception as e:
        log_error("Failed to get learning card count", e)
        return 0


@require_collection(default=0)
def anki_get_rev_card_count() -> int:
    """Get the count of review cards due today."""
    log_api_call("ankiGetRevCardCount")
    
    try:
        col = AnkiContext.get_collection()
        if not col:
            return 0
        return col.sched.counts()[2]  # review count
    except Exception as e:
        log_error("Failed to get review card count", e)
        return 0


@require_collection(default=0)
def anki_get_eta() -> int:
    """Get the estimated time (in minutes) to complete remaining reviews."""
    log_api_call("ankiGetETA")
    
    try:
        col = AnkiContext.get_collection()
        if not col:
            return 0
        # Get counts
        counts = col.sched.counts()
        new_count, lrn_count, rev_count = counts
        
        # Estimate time based on average card review times
        total_seconds = (
            (new_count * NEW_CARD_TIME_ESTIMATE_SEC) + 
            (lrn_count * LEARNING_CARD_TIME_ESTIMATE_SEC) + 
            (rev_count * REVIEW_CARD_TIME_ESTIMATE_SEC)
        )
        return int(total_seconds / 60)
    except Exception as e:
        log_error("Failed to calculate ETA", e)
        return 0


def anki_get_card_mark() -> bool:
    """Check if the current card is marked."""
    log_api_call("ankiGetCardMark")
    
    card = get_current_card()
    if not card:
        return False
    
    note = card.note()
    return note.has_tag("marked")


def anki_get_card_flag() -> int:
    """Get the flag color of the current card."""
    return _get_card_property('flags', 'ankiGetCardFlag', 0)


@require_collection(default=0)
def anki_get_card_left() -> int:
    """Get the number of reps left today (learning + review)."""
    log_api_call("ankiGetCardLeft")
    
    col = AnkiContext.get_collection()
    if not col:
        return 0
    counts = col.sched.counts()
    # Return sum of learning + review cards
    return counts[1] + counts[2]


def anki_get_card_reps() -> int:
    """Get the number of times the card has been reviewed."""
    return _get_card_property('reps', 'ankiGetCardReps', 0)


def anki_get_card_interval() -> int:
    """Get the current interval of the card in days."""
    return _get_card_property('ivl', 'ankiGetCardInterval', 0)


def anki_get_card_factor() -> int:
    """Get the ease factor of the card (as a percentage multiplied by 10)."""
    return _get_card_property('factor', 'ankiGetCardFactor', CARD_DEFAULT_EASE_FACTOR)


def anki_get_card_mod() -> int:
    """Get the modification timestamp of the card."""
    mod = _get_card_property('mod', 'ankiGetCardMod', 0)
    return int(mod) if mod else 0


def anki_get_card_id() -> int:
    """Get the unique ID of the current card."""
    return _get_card_property('id', 'ankiGetCardId', 0)


def anki_get_card_nid() -> int:
    """Get the note ID associated with the current card."""
    return _get_card_property('nid', 'ankiGetCardNid', 0)


def anki_get_card_type() -> int:
    """Get the card type (new/learning/review).
    
    Returns:
        int: Card type (0=new, 1=learning, 2=review, 3=relearning), or 0 if unavailable.
        
    Example:
        In JavaScript:
        >>> const cardType = await api.ankiGetCardType();
        >>> if (cardType === 0) console.log("This is a new card");
    """
    return _get_card_property('type', 'ankiGetCardType', 0)


def anki_get_card_did() -> int:
    """Get the deck ID containing the current card."""
    return _get_card_property('did', 'ankiGetCardDid', 0)


def anki_get_card_queue() -> int:
    """Get the queue the card is currently in.
    
    Returns:
        int: Queue type (0=new, 1=learning, 2=review, 3=day learning, -1=suspended,
             -2=sibling buried, -3=manually buried), or 0 if unavailable.
        
    Example:
        In JavaScript:
        >>> const queue = await api.ankiGetCardQueue();
        >>> if (queue === -1) console.log("Card is suspended");
    """
    return _get_card_property('queue', 'ankiGetCardQueue', 0)


def anki_get_card_lapses() -> int:
    """Get the number of times the card has been forgotten (lapsed)."""
    return _get_card_property('lapses', 'ankiGetCardLapses', 0)


def anki_get_card_due() -> int:
    """Get the due date of the card.
    
    Returns:
        int: For review cards: due day (days since collection creation).
             For new/learning cards: position in queue.
             Returns 0 if no card is available.
        
    Example:
        In JavaScript:
        >>> const due = await api.ankiGetCardDue();
        >>> console.log(`Card due value: ${due}`);
    """
    return _get_card_property('due', 'ankiGetCardDue', 0)


def anki_get_deck_name() -> str:
    """Get the name of the current deck (basename only)."""
    log_api_call("ankiGetDeckName")
    
    card = get_current_card()
    col = AnkiContext.get_collection()
    if not card or not col:
        return ""
    
    deck_name = col.decks.name(card.did)
    # Return only the basename (last part after ::)
    return deck_name.split("::")[-1] if "::" in deck_name else deck_name


def anki_get_next_time(ease: int) -> str:
    """Get the next review interval for a specific ease button."""
    log_api_call(f"ankiGetNextTime{ease}")
    
    card = get_current_card()
    col = AnkiContext.get_collection()
    reviewer = AnkiContext.get_reviewer()
    if not card or not col:
        return ""
    
    try:
        # Try the Anki 2.1.50+ approach using states()
        if hasattr(col.sched, 'states'):
            states = col.sched.states(card)
            
            # Map ease to state
            if ease == 1:  # Again
                state = states.again
            elif ease == 2:  # Hard
                state = states.hard
            elif ease == 3:  # Good
                state = states.good
            elif ease == 4:  # Easy
                state = states.easy
            else:
                return ""
            
            # Format the interval from the state
            if hasattr(state, 'interval'):
                interval_secs = state.interval
                days = interval_secs / 86400
            elif hasattr(state, 'scheduled_days'):
                days = state.scheduled_days
            else:
                return ""
            
            # Format as string
            if days < 1:
                mins = int(days * 1440)
                return f"{mins}m"
            elif days < 30:
                return f"{int(days)}d"
            else:
                months = days / 30.44
                return f"{months:.1f}mo"
        
        # Fallback: Try to access button labels from reviewer
        if reviewer and reviewer.card == card:
            # Try to get button info from reviewer's answer buttons
            # This is a simpler approach that reads what Anki itself calculated
            try:
                # Get the raw HTML or button data if available
                if hasattr(reviewer, '_answerButtonList'):
                    buttons = reviewer._answerButtonList()
                    if ease - 1 < len(buttons):
                        label = buttons[ease - 1][0]
                        # Extract time from label (format varies)
                        import re
                        match = re.search(r'(\d+(?:\.\d+)?)\s*([smhd]|mo)', label)
                        if match:
                            return f"{match.group(1)}{match.group(2)}"
            except:
                pass
        
        # Last resort: return empty string
        return ""
        
    except Exception as e:
        # Log error but don't crash
        from .utils import logger
        logger.error(f"Error getting next time for ease {ease}: {e}")
        return ""
