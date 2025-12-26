# SPDX-License-Identifier: MIT
# Copyright (c) 2025 AnkiDroid JS API Desktop Contributors

"""
API Bridge - connects JavaScript in card templates to Python backend.

This module provides the core infrastructure for the AnkiDroid JS API:

Architecture:
    - API_REGISTRY: Dictionary mapping JavaScript function names to Python implementations
    - handle_pycmd: Parses ankidroidjs: commands from JavaScript and routes to functions
    - inject_js_api: Injects JavaScript API code into card templates
    - Rate limiting: Prevents API abuse (10 calls/second per template)
    - Security: Input validation, payload size limits, callback ID validation

Extension Points:
    To add a new API function:
    1. Create the implementation in the appropriate module (card_info, card_actions, etc.)
    2. Register it in setup_api_bridge(): register_api_function("apiName", function)
    3. Add tests in tests/test_*.py
    4. Update documentation in README.md

Example:
    >>> # In your new module (e.g., my_features.py)
    >>> def my_custom_function(param: str) -> bool:
    ...     # Implementation here
    ...     return True
    >>>
    >>> # In api_bridge.py setup_api_bridge()
    >>> register_api_function("myCustomFunction", my_features.my_custom_function)

Compatibility:
    - Anki Desktop: 2.1.50+ (PyQt6)
    - Python: 3.9+
    - AnkiDroid JS API: v0.0.3

Thread Safety:
    All functions are called from Anki's main thread. Do not use threading without proper synchronization.
"""

import json
import re
from typing import Any, Callable, Dict

from aqt import gui_hooks
from aqt.reviewer import Reviewer

from .utils import AnkiContext
from . import card_info
from . import card_actions
from . import reviewer_control
from . import tts_control
from . import ui_control
from . import tag_manager
from .utils import read_js_file, log_debug
from .security import RateLimiter, generate_template_hash
from .constants import MAX_JSON_PAYLOAD_BYTES, DEFAULT_API_RATE_LIMIT_PER_SECOND


# Registry of Python functions callable from JavaScript
API_REGISTRY: Dict[str, Callable] = {}


def register_api_function(name: str, func: Callable) -> None:
    """Register a Python function to be callable from JavaScript."""
    API_REGISTRY[name] = func


def handle_pycmd(reviewer: Reviewer, cmd: str) -> None:
    """Handle pycmd calls from JavaScript with rate limiting and validation."""
    if not cmd.startswith("ankidroidjs:"):
        return
    
    # Parse the command: ankidroidjs:callbackId:function_name:json_args
    parts = cmd.split(":", 3)
    if len(parts) < 3:
        log_debug(f"Malformed command (expected 'ankidroidjs:callbackId:function:args', got '{cmd[:100]}')")
        return
    
    callback_id = parts[1]
    function_name = parts[2]
    args_json = parts[3] if len(parts) > 3 else "{}"
    
    # Generate template identifier for rate limiting
    template_id = "unknown"
    if reviewer and reviewer.card:
        try:
            template_content = str(reviewer.card.template().get('qfmt', ''))
            template_id = generate_template_hash(template_content)[:16]
        except:
            pass
    
    # Check rate limit
    if not RateLimiter.check(template_id, function_name, max_per_second=DEFAULT_API_RATE_LIMIT_PER_SECOND):
        error_msg = f"Rate limit exceeded for {function_name}"
        log_debug(error_msg)
        response = {"success": False, "error": "Rate limit exceeded"}
        _send_callback(reviewer, callback_id, response)
        return
    
    log_debug(f"Processing API call: {function_name} (callback {callback_id})")
    
    # Look up the function
    if function_name not in API_REGISTRY:
        error_msg = f"Unknown API function: {function_name}"
        log_debug(error_msg)
        response = {"success": False, "error": error_msg}
        _send_callback(reviewer, callback_id, response)
        return
    
    try:
        # Validate JSON size to prevent DoS attacks
        if len(args_json) > MAX_JSON_PAYLOAD_BYTES:
            raise ValueError(f"JSON payload too large: {len(args_json)} bytes")
        
        # Parse arguments
        args = json.loads(args_json) if args_json else {}
        
        # Call the function
        func = API_REGISTRY[function_name]
        result = func(**args) if isinstance(args, dict) else func(args)
        
        log_debug(f"API call {function_name} completed")
        
        # Send success response via callback
        response = {"success": True, "result": result}
        _send_callback(reviewer, callback_id, response)
    
    except Exception as e:
        error_msg = f"Error executing {function_name}: {type(e).__name__}: {str(e)}"
        log_debug(error_msg)
        # Provide specific error type while avoiding sensitive details
        error_type = type(e).__name__
        user_msg = f"Operation failed: {error_type}"
        response = {"success": False, "error": user_msg}
        _send_callback(reviewer, callback_id, response)


def _send_callback(reviewer: Reviewer, callback_id: str, response: dict) -> None:
    """Send a response back to JavaScript via callback with validation."""
    from .security import InputValidator
    
    # Validate callback_id is numeric or -1 (for fire-and-forget)
    if not InputValidator._CALLBACK_ID_PATTERN.match(str(callback_id)):
        log_debug(f"Invalid callback ID: {callback_id}")
        return
    
    # json.dumps provides safe escaping
    response_json = json.dumps(response, ensure_ascii=True)
    js_code = f"window._ankidroidJsCallback({callback_id}, {response_json});"
    log_debug(f"Sending callback {callback_id}")
    
    if reviewer and reviewer.web:
        reviewer.web.eval(js_code)


def inject_js_api(html: str, card: Any, kind: str) -> str:
    """Inject the JavaScript API into card templates.
    
    Args:
        html: The card HTML content
        card: The card being reviewed (can be None)
        kind: The kind of content ("reviewQuestion", "reviewAnswer", etc.)
    
    Returns:
        Modified HTML with JavaScript API injected
    """
    log_debug(f"Injecting JS API for card type: {kind}")
    
    # Read the JavaScript API file
    js_api = read_js_file("ankidroid-api.js")
    
    # Inject it into the HTML
    injection = f"<script>{js_api}</script>"
    
    # Insert before </head> if present, otherwise at the start
    if "</head>" in html:
        html = html.replace("</head>", f"{injection}</head>")
    else:
        html = injection + html
    
    log_debug("JS API injected successfully")
    return html


def setup_api_bridge() -> None:
    """Setup the API bridge between JavaScript and Python."""
    
    # Register all API functions
    
    # Card Information APIs
    register_api_function("ankiGetNewCardCount", card_info.anki_get_new_card_count)
    register_api_function("ankiGetLrnCardCount", card_info.anki_get_lrn_card_count)
    register_api_function("ankiGetRevCardCount", card_info.anki_get_rev_card_count)
    register_api_function("ankiGetETA", card_info.anki_get_eta)
    register_api_function("ankiGetCardMark", card_info.anki_get_card_mark)
    register_api_function("ankiGetCardFlag", card_info.anki_get_card_flag)
    register_api_function("ankiGetCardLeft", card_info.anki_get_card_left)
    register_api_function("ankiGetCardReps", card_info.anki_get_card_reps)
    register_api_function("ankiGetCardInterval", card_info.anki_get_card_interval)
    register_api_function("ankiGetCardFactor", card_info.anki_get_card_factor)
    register_api_function("ankiGetCardMod", card_info.anki_get_card_mod)
    register_api_function("ankiGetCardId", card_info.anki_get_card_id)
    register_api_function("ankiGetCardNid", card_info.anki_get_card_nid)
    register_api_function("ankiGetCardType", card_info.anki_get_card_type)
    register_api_function("ankiGetCardDid", card_info.anki_get_card_did)
    register_api_function("ankiGetCardQueue", card_info.anki_get_card_queue)
    register_api_function("ankiGetCardLapses", card_info.anki_get_card_lapses)
    register_api_function("ankiGetCardDue", card_info.anki_get_card_due)
    register_api_function("ankiGetDeckName", card_info.anki_get_deck_name)
    register_api_function("ankiGetNextTime1", lambda: card_info.anki_get_next_time(1))
    register_api_function("ankiGetNextTime2", lambda: card_info.anki_get_next_time(2))
    register_api_function("ankiGetNextTime3", lambda: card_info.anki_get_next_time(3))
    register_api_function("ankiGetNextTime4", lambda: card_info.anki_get_next_time(4))
    
    # Card Action APIs
    register_api_function("ankiMarkCard", card_actions.anki_mark_card)
    register_api_function("ankiToggleFlag", card_actions.anki_toggle_flag)
    register_api_function("ankiBuryCard", card_actions.anki_bury_card)
    register_api_function("ankiBuryNote", card_actions.anki_bury_note)
    register_api_function("ankiSuspendCard", card_actions.anki_suspend_card)
    register_api_function("ankiSuspendNote", card_actions.anki_suspend_note)
    register_api_function("ankiResetProgress", card_actions.anki_reset_progress)
    register_api_function("ankiSearchCard", card_actions.anki_search_card)
    register_api_function("ankiSetCardDue", card_actions.anki_set_card_due)
    
    # Reviewer Control APIs
    register_api_function("ankiGetDebugInfo", reviewer_control.anki_get_debug_info)
    register_api_function("ankiIsDisplayingAnswer", reviewer_control.anki_is_displaying_answer)
    register_api_function("ankiShowAnswer", reviewer_control.anki_show_answer)
    register_api_function("ankiAnswerEase1", reviewer_control.anki_answer_ease1)
    register_api_function("ankiAnswerEase2", reviewer_control.anki_answer_ease2)
    register_api_function("ankiAnswerEase3", reviewer_control.anki_answer_ease3)
    register_api_function("ankiAnswerEase4", reviewer_control.anki_answer_ease4)
    
    # Also register with buttonAnswer prefix for compatibility
    register_api_function("buttonAnswerEase1", reviewer_control.anki_answer_ease1)
    register_api_function("buttonAnswerEase2", reviewer_control.anki_answer_ease2)
    register_api_function("buttonAnswerEase3", reviewer_control.anki_answer_ease3)
    register_api_function("buttonAnswerEase4", reviewer_control.anki_answer_ease4)
    
    # TTS Control APIs
    register_api_function("ankiTtsSpeak", tts_control.anki_tts_speak)
    register_api_function("ankiTtsSetLanguage", tts_control.anki_tts_set_language)
    register_api_function("ankiTtsSetPitch", tts_control.anki_tts_set_pitch)
    register_api_function("ankiTtsSetSpeechRate", tts_control.anki_tts_set_speech_rate)
    register_api_function("ankiTtsIsSpeaking", tts_control.anki_tts_is_speaking)
    register_api_function("ankiTtsStop", tts_control.anki_tts_stop)
    register_api_function("ankiTtsFieldModifierIsAvailable", tts_control.anki_tts_field_modifier_is_available)
    
    # UI Control APIs
    register_api_function("ankiIsInFullscreen", ui_control.anki_is_in_fullscreen)
    register_api_function("ankiIsTopbarShown", ui_control.anki_is_topbar_shown)
    register_api_function("ankiIsInNightMode", ui_control.anki_is_in_night_mode)
    register_api_function("ankiEnableHorizontalScrollbar", ui_control.anki_enable_horizontal_scrollbar)
    register_api_function("ankiEnableVerticalScrollbar", ui_control.anki_enable_vertical_scrollbar)
    register_api_function("ankiShowNavigationDrawer", ui_control.anki_show_navigation_drawer)
    register_api_function("ankiShowOptionsMenu", ui_control.anki_show_options_menu)
    register_api_function("ankiShowToast", ui_control.anki_show_toast)
    
    # Tag Management APIs
    register_api_function("ankiSetNoteTags", tag_manager.anki_set_note_tags)
    register_api_function("ankiGetNoteTags", tag_manager.anki_get_note_tags)
    register_api_function("ankiAddTagToNote", tag_manager.anki_add_tag_to_note)
    
    # Utility APIs
    register_api_function("ankiIsActiveNetworkMetered", lambda: False)  # Desktop is typically not metered
    
    # Hook into the reviewer to inject JavaScript
    gui_hooks.card_will_show.append(inject_js_api)
    
    # Patch Reviewer._linkHandler to intercept our commands
    from aqt.reviewer import Reviewer
    _original_link_handler = Reviewer._linkHandler
    
    def custom_link_handler(reviewer_self, url: str) -> Any:
        """Custom link handler that intercepts ankidroidjs commands."""
        if isinstance(url, str) and url.startswith("ankidroidjs:"):
            log_debug(f"_linkHandler received: {url}")
            handle_pycmd(reviewer_self, url)
            return False  # Don't pass to original handler
        
        return _original_link_handler(reviewer_self, url)
    
    Reviewer._linkHandler = custom_link_handler
    
    log_debug(f"API bridge setup complete with {len(API_REGISTRY)} functions registered")
