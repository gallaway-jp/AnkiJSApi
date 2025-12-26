# SPDX-License-Identifier: MIT
# Copyright (c) 2025 AnkiDroid JS API Desktop Contributors

"""
AnkiDroid JS API for Desktop
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Brings AnkiDroid's powerful JavaScript template API to Anki Desktop.

This add-on provides a JavaScript bridge that mimics the AnkiDroidJS API,
enabling advanced interactive card templates with programmatic control over
the reviewer, TTS, card actions, and more.

Compatibility:
    - Anki Desktop: 2.1.50+ (tested up to 25.07.5)
    - Python: 3.9+ (tested with 3.13)
    - AnkiDroidJS API Version: 0.0.3

Installation:
    1. Download .ankiaddon file from releases
    2. Tools → Add-ons → Install from file
    3. Restart Anki

Quick Start:
    In your card template:
    <script>
    const api = AnkiDroidJS.init({developer: "you@example.com", version: "0.0.3"});
    const cardId = await api.ankiGetCardId();
    </script>

Documentation:
    - Full API reference: README.md
    - Examples: test_templates/
    - Testing guide: docs/TESTING.md

:copyright: (c) 2025 by AnkiDroid JS API Contributors
:license: MIT, see LICENSE for more details.
"""

from typing import Any
from aqt import gui_hooks
from aqt.reviewer import Reviewer
from aqt.qt import QMessageBox, QAction

from .api_bridge import setup_api_bridge
from .utils import get_config, log_debug, AnkiContext

__version__ = "1.0.0"
__author__ = "AnkiDroid JS API Contributors"
__api_version__ = "0.0.3"  # AnkiDroidJS API compatibility version
__min_anki_version__ = "2.1.50"  # Minimum Anki version required


def show_error(message: str) -> None:
    """Show an error message to the user."""
    mw = AnkiContext.get_main_window()
    if mw:
        QMessageBox.critical(mw, "AnkiDroid JS API Error", message)


def show_info(message: str) -> None:
    """Show an info message to the user."""
    mw = AnkiContext.get_main_window()
    if mw:
        QMessageBox.information(mw, "AnkiDroid JS API", message)


def create_test_deck() -> None:
    """Create a test deck with all API test cards."""
    try:
        import os
        col = AnkiContext.get_collection()
        if not col:
            show_error("Collection not available")
            return
        
        # Create deck
        deck_name = "AnkiDroid JS API Tests"
        deck_id = col.decks.id(deck_name)
        
        # Create note type
        models = col.models
        model_name = "API Test Card"
        
        existing_model = models.by_name(model_name)
        if existing_model:
            model = existing_model
        else:
            model = models.new(model_name)
            models.add_field(model, models.new_field("Front"))
            models.add_field(model, models.new_field("Back"))
            
            # Read template files from add-on directory
            addon_dir = os.path.dirname(__file__)
            front_path = os.path.join(addon_dir, "test_templates", "front.html")
            back_path = os.path.join(addon_dir, "test_templates", "back.html")
            
            with open(front_path, 'r', encoding='utf-8') as f:
                front_template = f.read()
            with open(back_path, 'r', encoding='utf-8') as f:
                back_template = f.read()
            
            template = models.new_template("Card 1")
            template['qfmt'] = front_template
            template['afmt'] = back_template
            models.add_template(model, template)
            models.add(model)
        
        # Create test cards
        test_cards = [
            {"Front": "Card Information APIs", "Back": "Test all card info functions: counts, stats, IDs, etc."},
            {"Front": "Card Actions APIs", "Back": "Test mark, flag, bury, suspend, reset functions"},
            {"Front": "TTS APIs", "Back": "Test text-to-speech: speak, stop, language, pitch, rate"},
            {"Front": "UI Control APIs", "Back": "Test fullscreen, night mode, toast, scrollbar functions"},
            {"Front": "Tag Management APIs", "Back": "Test get tags, set tags, add tag functions"},
            {"Front": "Reviewer Control APIs", "Back": "Test show answer, answer buttons, display state"},
            {"Front": "Complete Integration Test", "Back": "All APIs working together in one workflow"},
        ]
        
        for card_data in test_cards:
            note = col.new_note(model)
            note['Front'] = card_data['Front']
            note['Back'] = card_data['Back']
            col.add_note(note, deck_id)
        
        col.save()
        mw = AnkiContext.get_main_window()
        if mw:
            mw.reset()
        
        show_info(f"Successfully created test deck!\n\n"
                 f"• Deck: {deck_name}\n"
                 f"• Cards: {len(test_cards)}\n\n"
                 f"Go to the deck and start reviewing to test all APIs.")
        
    except Exception as e:
        show_error(f"Failed to create test deck:\n{str(e)}")


def setup_menu() -> None:
    """Add menu items to Anki's Tools menu."""
    config = get_config()
    
    # Only show test deck creation in debug mode
    if not config.get("debug_mode", False):
        return
        
    mw = AnkiContext.get_main_window()
    if mw:
        action = QAction("Create API Test Deck", mw)
        action.triggered.connect(create_test_deck)
        mw.form.menuTools.addAction(action)


def init_addon() -> None:
    """Initialize the add-on."""
    try:
        config = get_config()
        
        if config.get("debug_mode", False):
            log_debug("Initializing AnkiDroid JS API for Desktop...")
        
        # Setup the JavaScript API bridge
        setup_api_bridge()
        
        if config.get("debug_mode", False):
            log_debug("AnkiDroid JS API initialized successfully")
            
    except Exception as e:
        show_error(f"Failed to initialize AnkiDroid JS API:\n{str(e)}")
        raise


# Initialize the add-on when Anki starts
init_addon()

# Setup menu items
setup_menu()
