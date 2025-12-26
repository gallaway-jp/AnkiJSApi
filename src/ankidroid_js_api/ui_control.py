# SPDX-License-Identifier: MIT
# Copyright (c) 2025 AnkiDroid JS API Desktop Contributors

"""
UI control APIs - control the user interface.
This module provides UI control functions adapted from AnkiDroid:

Features:
    - Detect UI state (fullscreen, night mode, topbar visibility)
    - Show toast notifications with configurable duration
    - Navigate to different screens (deck browser, options)
    - Scrollbar control (placeholder for compatibility)

Desktop vs Mobile Differences:
    Some functions are placeholders for AnkiDroid API compatibility:
    - anki_enable_horizontal_scrollbar(): Placeholder (requires CSS injection)
    - anki_enable_vertical_scrollbar(): Placeholder (requires CSS injection)
    - anki_show_navigation_drawer(): Opens deck browser instead
    - anki_is_in_fullscreen(): Desktop-specific fullscreen detection
    - anki_is_topbar_shown(): Desktop-specific topbar detection

Toast Notifications:
    Configurable via config.json:
    {
        "ui": {
            "show_toast_notifications": true,
            "toast_duration_ms": 2000  // 2 seconds for short toast
        }
    }
    Long toasts multiply duration by TOAST_DURATION_MULTIPLIER_LONG (2x).

Night Mode:
    Detects Anki's native night mode (theme_manager.night_mode).
    Templates can use this to adjust styling dynamically.

Usage:
    From JavaScript in card templates:
    >>> // Show toast message
    >>> await api.ankiShowToast("Card marked!", true);
    >>> 
    >>> // Check night mode
    >>> const darkMode = await api.ankiIsInNightMode();
    >>> if (darkMode) {
    ...     document.body.style.background = "#1e1e1e";
    >>> }
    >>> 
    >>> // Open deck options
    >>> await api.ankiShowOptionsMenu();

Constants:
    UI-related constants defined in constants/ui.py:
    - DEFAULT_TOAST_DURATION_MS: 2000 (2 seconds)
    - TOAST_DURATION_MULTIPLIER_LONG: 2.0 (4 seconds for long toast)"""

from aqt.utils import tooltip
from aqt.theme import theme_manager

from .utils import log_api_call, get_config, log_warning, log_error, AnkiContext
from .constants import DEFAULT_TOAST_DURATION_MS, TOAST_DURATION_MULTIPLIER_LONG


def anki_is_in_fullscreen() -> bool:
    """Check if the reviewer is in fullscreen mode."""
    log_api_call("ankiIsInFullscreen")
    
    mw = AnkiContext.get_main_window()
    if not mw:
        return False
    
    return mw.isFullScreen()


def anki_is_topbar_shown() -> bool:
    """Check if the top bar is currently shown."""
    log_api_call("ankiIsTopbarShown")
    
    # Desktop Anki always shows the menu bar
    # Return True to indicate the toolbar is visible
    return True


def anki_is_in_night_mode() -> bool:
    """Check if night mode is currently active."""
    log_api_call("ankiIsInNightMode")
    
    mw = AnkiContext.get_main_window()
    if not mw:
        return False
    
    return theme_manager.night_mode


def anki_enable_horizontal_scrollbar(enabled: bool) -> bool:
    """Enable or disable the horizontal scrollbar.
    
    Args:
        enabled: True to enable scrollbar, False to disable.
    
    Returns:
        bool: True (command acknowledged). Currently a placeholder.
        
    Note:
        This is a placeholder for AnkiDroid compatibility. Desktop implementation
        requires CSS injection into the webview. Always returns True.
    """
    log_api_call("ankiEnableHorizontalScrollbar", {"enabled": enabled})
    
    # This would require injecting CSS into the webview
    # For now, return True to indicate the command was received
    # Implementation would modify the reviewer's webview CSS
    
    return True


def anki_enable_vertical_scrollbar(enabled: bool) -> bool:
    """Enable or disable the vertical scrollbar.
    
    Args:
        enabled: True to enable scrollbar, False to disable.
    
    Returns:
        bool: True (command acknowledged). Currently a placeholder.
        
    Note:
        This is a placeholder for AnkiDroid compatibility. Desktop implementation
        requires CSS injection into the webview. Always returns True.
    """
    log_api_call("ankiEnableVerticalScrollbar", {"enabled": enabled})
    
    # Similar to horizontal scrollbar
    # Would require CSS injection
    
    return True


def anki_show_navigation_drawer() -> bool:
    """Open the navigation drawer."""
    log_api_call("ankiShowNavigationDrawer")
    
    # Desktop doesn't have a navigation drawer
    # Instead, we could show the deck browser
    mw = AnkiContext.get_main_window()
    if mw:
        mw.moveToState("deckBrowser")
        return True
    
    return False


def anki_show_options_menu() -> bool:
    """Open the options menu."""
    log_api_call("ankiShowOptionsMenu")
    
    reviewer = AnkiContext.get_reviewer()
    if not reviewer or not reviewer.card:
        log_warning("Reviewer or card not available for options menu")
        return False
    
    try:
        # Show deck options for the current deck
        mw = AnkiContext.get_main_window()
        deck_id = reviewer.card.did
        mw.onDeckConf(deck_id)
        return True
    except Exception as e:
        log_error("Failed to open options menu", e)
        return False


def anki_show_toast(text: str, short_length: bool = True) -> bool:
    """Display a toast message."""
    log_api_call("ankiShowToast", {"text": text, "short_length": short_length})
    
    config = get_config()
    if not config.get("ui", {}).get("show_toast_notifications", True):
        return False
    
    mw = AnkiContext.get_main_window()
    if not mw:
        log_warning("Main window not available for toast")
        return False
    
    try:
        # Use Anki's tooltip function
        duration_ms = config.get("ui", {}).get("toast_duration_ms", DEFAULT_TOAST_DURATION_MS)
        if not short_length:
            duration_ms *= TOAST_DURATION_MULTIPLIER_LONG
        
        tooltip(text, period=duration_ms)
        return True
    except Exception as e:
        log_error("Failed to show toast", e)
        return False
