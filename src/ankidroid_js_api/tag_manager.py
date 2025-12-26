# SPDX-License-Identifier: MIT
# Copyright (c) 2025 AnkiDroid JS API Desktop Contributors

"""
Tag management APIs - manage tags associated with notes.
"""

import json

from .card_info import get_current_card
from .utils import log_api_call, AnkiContext
from .security import InputValidator


def anki_set_note_tags(tags: list) -> bool:
    """Set the tags for the current note (replaces all existing tags).
    
    Args:
        tags: List of tag strings to set. Existing tags will be replaced.
              Spaces in tags are converted to underscores automatically.
    
    Returns:
        bool: True if operation succeeded, False if no card is available.
        
    Example:
        In JavaScript:
        >>> await api.ankiSetNoteTags(["vocabulary", "chapter 1", "difficult"]);
        // Tags become: ["vocabulary", "chapter_1", "difficult"]
        
    Note:
        This REPLACES all existing tags. Use ankiAddTagToNote() to add individual tags
        without removing existing ones.
    """
    log_api_call("ankiSetNoteTags", {"tags": tags})
    
    card = get_current_card()
    if not card:
        return False
    
    note = card.note()
    
    # Process tags: convert spaces to underscores and trim
    processed_tags = []
    for tag in tags:
        tag = tag.strip()
        tag = tag.replace(" ", "_")
        if tag:
            processed_tags.append(tag)
    
    # Set the tags (this replaces all existing tags)
    note.tags = processed_tags
    note.flush()
    
    mw = AnkiContext.get_main_window()
    if mw:
        mw.requireReset()
    
    return True


def anki_get_note_tags() -> str:
    """Get all tags from the current note.
    
    Returns:
        str: JSON-encoded array of tag strings. Returns "[]" if no card is available.
        
    Example:
        In JavaScript:
        >>> const tagsJson = await api.ankiGetNoteTags();
        >>> const tags = JSON.parse(tagsJson);
        >>> console.log(tags);  // ["vocabulary", "chapter_1"]
    """
    log_api_call("ankiGetNoteTags")
    
    card = get_current_card()
    if not card:
        return json.dumps([])
    
    note = card.note()
    return json.dumps(note.tags)


def anki_add_tag_to_note(tag: str) -> bool:
    """Add a tag to the current note.
    
    Args:
        tag: Tag string to add. Validated for length and characters.
             Maximum length: 100 characters.
    
    Returns:
        bool: True if operation succeeded, False if no card is available.
        
    Example:
        In JavaScript:
        >>> await api.ankiAddTagToNote("important");
        
    Note:
        If the tag already exists on the note, it will not be duplicated.
        Preserves all existing tags on the note.
    """
    log_api_call("ankiAddTagToNote", {"tag": tag})
    
    # Validate tag
    tag = InputValidator.validate_tag(tag, max_length=100)
    
    card = get_current_card()
    if not card:
        return False
    
    note = card.note()
    
    if tag and not note.has_tag(tag):
        note.add_tag(tag)
        note.flush()
    
    return True
