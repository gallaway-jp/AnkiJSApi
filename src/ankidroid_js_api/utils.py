# SPDX-License-Identifier: MIT
# Copyright (c) 2025 AnkiDroid JS API Desktop Contributors

"""Utility functions and helpers for the AnkiDroid JS API.

This module provides core infrastructure for the add-on:

Components:
    - AnkiContext: Abstraction layer for Anki's main window, collection, and reviewer
    - Configuration management: get_config(), save_config()
    - Logging utilities: log_debug(), log_error(), log_warning(), log_api_call()
    - Decorators: require_collection(), require_card(), require_card_and_collection()
    - File I/O: get_addon_path(), read_js_file()

AnkiContext Benefits:
    The AnkiContext class serves as a dependency injection point:
    - Testability: Single point to mock for all Anki dependencies
    - Maintainability: Changes to Anki access patterns centralized
    - Clarity: Explicit about what Anki components are used
    - Isolation: Prevents direct global variable access

Decorators:
    Decorators provide automatic null-checking and default value returns:
    
    >>> @require_collection(default=0)
    ... def get_card_count() -> int:
    ...     col = AnkiContext.get_collection()
    ...     return len(col.find_cards(""))
    
    If collection is unavailable, returns 0 without raising exceptions.

Logging:
    Three log levels with configurable verbosity:
    - log_debug(): Only shown when debug_mode=True in config
    - log_warning(): Always shown
    - log_error(): Always shown, can include exception info
    - log_api_call(): Logs API calls when log_api_calls=True in config

Usage:
    >>> from .utils import AnkiContext, log_debug, require_collection
    >>> 
    >>> # Access Anki components
    >>> mw = AnkiContext.get_main_window()
    >>> col = AnkiContext.get_collection()
    >>> reviewer = AnkiContext.get_reviewer()
    >>> 
    >>> # Use decorators for safe API functions
    >>> @require_card(default=False)
    ... def mark_current_card() -> bool:
    ...     # Card existence already checked by decorator
    ...     card = get_current_card()
    ...     note = card.note()
    ...     note.add_tag("marked")
    ...     return True
"""

import json
from typing import Any, Dict, Optional, Callable, TypeVar
from pathlib import Path
from functools import wraps

T = TypeVar('T')


class AnkiContext:
    """Abstraction layer for Anki's main window and collection.
    
    Provides centralized access to Anki's global state, making the codebase
    more testable and less coupled to Anki's implementation details.
    
    Usage:
        >>> mw = AnkiContext.get_main_window()
        >>> col = AnkiContext.get_collection()
        >>> reviewer = AnkiContext.get_reviewer()
    
    Testing:
        Mock this class in tests to avoid dependency on full Anki environment:
        >>> class MockAnkiContext(AnkiContext):
        ...     @staticmethod
        ...     def get_main_window():
        ...         return Mock()
    """
    
    @staticmethod
    def get_main_window():
        """Get Anki's main window instance.
        
        Returns:
            Main window instance or None if not available.
        """
        from aqt import mw
        return mw
    
    @staticmethod
    def get_collection():
        """Get the current Anki collection.
        
        Returns:
            Collection instance or None if not available.
        """
        mw = AnkiContext.get_main_window()
        return mw.col if mw else None
    
    @staticmethod
    def get_reviewer():
        """Get the current reviewer instance.
        
        Returns:
            Reviewer instance or None if not available.
        """
        mw = AnkiContext.get_main_window()
        return mw.reviewer if mw else None
    
    @staticmethod
    def get_addon_manager():
        """Get the add-on manager instance.
        
        Returns:
            AddonManager instance or None if not available.
        """
        mw = AnkiContext.get_main_window()
        return mw.addonManager if mw else None


def get_config() -> Dict[str, Any]:
    """Get the add-on configuration."""
    addon_manager = AnkiContext.get_addon_manager()
    if addon_manager:
        return addon_manager.getConfig(__name__.split(".")[0]) or {}
    return {}


def save_config(config: Dict[str, Any]) -> None:
    """Save the add-on configuration."""
    addon_manager = AnkiContext.get_addon_manager()
    if addon_manager:
        addon_manager.writeConfig(__name__.split(".")[0], config)


def log_debug(message: str) -> None:
    """Log a debug message if debug mode is enabled."""
    from .security import sanitize_for_logging
    
    config = get_config()
    if config.get("debug_mode", False):
        # Sanitize message to remove PII
        safe_message = sanitize_for_logging(message)
        print(f"[AnkiDroid JS API] {safe_message}")

def log_error(message: str, exc_info: Exception = None) -> None:
    """Log an error message (always shown, even if debug_mode is False)."""
    from .security import sanitize_for_logging
    
    safe_message = sanitize_for_logging(message)
    if exc_info:
        print(f"[AnkiDroid JS API ERROR] {safe_message}: {exc_info}")
    else:
        print(f"[AnkiDroid JS API ERROR] {safe_message}")


def log_warning(message: str) -> None:
    """Log a warning message (always shown)."""
    from .security import sanitize_for_logging
    
    safe_message = sanitize_for_logging(message)
    print(f"[AnkiDroid JS API WARNING] {safe_message}")

def log_error(message: str, exc_info: Exception = None) -> None:
    """Log an error message (always shown, even if debug_mode is False)."""
    from .security import sanitize_for_logging
    
    safe_message = sanitize_for_logging(message)
    if exc_info:
        print(f"[AnkiDroid JS API ERROR] {safe_message}: {exc_info}")
    else:
        print(f"[AnkiDroid JS API ERROR] {safe_message}")


def log_warning(message: str) -> None:
    """Log a warning message (always shown)."""
    from .security import sanitize_for_logging
    
    safe_message = sanitize_for_logging(message)
    print(f"[AnkiDroid JS API WARNING] {safe_message}")


def require_collection(default: T = 0):
    """Decorator that ensures Anki collection is available.
    
    Args:
        default: Value to return if collection unavailable
        
    Returns:
        Decorated function that checks for collection availability
        
    Example:
        >>> @require_collection(default=0)
        ... def get_card_count() -> int:
        ...     col = AnkiContext.get_collection()
        ...     return col.sched.new_count
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            col = AnkiContext.get_collection()
            if not col:
                log_warning(f"{func.__name__} called without collection available")
                return default
            return func(*args, **kwargs)
        return wrapper
    return decorator


def require_card(default: T = 0):
    """Decorator that ensures current card is available.
    
    Args:
        default: Value to return if card unavailable
        
    Note:
        Passes the card as the first argument to the decorated function.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            from .card_info import get_current_card
            card = get_current_card()
            if not card:
                log_warning(f"No card available for {func.__name__}")
                return default
            return func(card, *args, **kwargs)
        return wrapper
    return decorator


def require_card_and_collection(default: T = False):
    """Decorator that ensures both card and collection are available.
    
    Args:
        default: Value to return if card or collection unavailable
        
    Note:
        Passes the card as the first argument to the decorated function.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            from .card_info import get_current_card
            card = get_current_card()
            col = AnkiContext.get_collection()
            if not card or not col:
                log_warning(f"Card or collection not available for {func.__name__}")
                return default
            return func(card, *args, **kwargs)
        return wrapper
    return decorator


def log_api_call(function_name: str, args: Optional[Dict[str, Any]] = None) -> None:
    """Log an API call if API call logging is enabled."""
    config = get_config()
    if config.get("log_api_calls", False):
        args_str = json.dumps(args) if args else ""
        print(f"[AnkiDroid JS API] {function_name}({args_str})")


def get_addon_path() -> Path:
    """Get the path to the add-on directory."""
    return Path(__file__).parent


# Cache for JavaScript files to avoid repeated disk I/O
_js_file_cache: Dict[str, str] = {}

def read_js_file(filename: str) -> str:
    """Read a JavaScript file from the addon's js directory with path validation."""
    from .security import InputValidator
    
    # Check cache first
    if filename in _js_file_cache:
        return _js_file_cache[filename]
    
    # Validate filename to prevent path traversal
    filename = InputValidator.validate_filename(filename)
    
    js_dir = get_addon_path() / "js"
    js_path = (js_dir / filename).resolve()
    
    # Ensure resolved path is still within js directory (prevent path traversal)
    if not str(js_path).startswith(str(js_dir.resolve())):
        raise ValueError(f"Path traversal attempt detected: {filename}")
    
    # Verify file exists and is a file (not directory)
    if not js_path.is_file():
        raise FileNotFoundError(f"JavaScript file not found: {filename}")
    
    with open(js_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Cache the content
    _js_file_cache[filename] = content
    return content
