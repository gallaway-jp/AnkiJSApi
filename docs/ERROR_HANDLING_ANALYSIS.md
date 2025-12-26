# Error Handling & Fault Tolerance Analysis

**Generated:** 2025-01-XX  
**Coverage:** All source modules in `src/ankidroid_js_api/`  
**Analysis Depth:** Critical issues, patterns, and recommendations

---

## Executive Summary

### Overall Assessment: **MODERATE** (60/100)

**Strengths:**
- ✅ Comprehensive error handling in `security.py` (99% coverage)
- ✅ Detailed error context in `tts_control.py` with recovery
- ✅ Validation and sanitization preventing common vulnerabilities
- ✅ Structured error responses in API bridge

**Critical Issues:**
- ❌ **BARE EXCEPT** block in `api_bridge.py:83-86` (security risk)
- ❌ **Inconsistent error handling** across modules
- ❌ **Missing error handling** in card_actions.py, card_info.py, ui_control.py
- ❌ **Silent failures** without user feedback in multiple functions
- ❌ **Generic error messages** hiding specific failures from users

### Impact Assessment
- **Security Risk:** HIGH (bare except catches system exceptions)
- **Maintainability:** MEDIUM (inconsistent patterns make debugging difficult)
- **User Experience:** LOW (silent failures, generic error messages)
- **Reliability:** MEDIUM (defensive checks but limited recovery)

---

## Detailed Findings

### 1. CRITICAL: Bare Except Block (Security Vulnerability)

**Location:** [api_bridge.py](../src/ankidroid_js_api/api_bridge.py#L83-L86)

**Issue:**
```python
try:
    template_content = str(reviewer.card.template().get('qfmt', ''))
    template_id = generate_template_hash(template_content)[:16]
except:  # ❌ CATCHES EVERYTHING including KeyboardInterrupt, SystemExit
    pass
```

**Severity:** 🔴 CRITICAL

**Problems:**
1. **Catches system exceptions:** `KeyboardInterrupt`, `SystemExit`, `MemoryError`
2. **Silently swallows errors:** No logging, no user notification
3. **Hides bugs:** Makes debugging impossible
4. **Violates PEP 8:** Never use bare except

**Impact:**
- User pressing Ctrl+C may not be able to interrupt Anki
- Out-of-memory errors silently ignored
- Template processing failures go unnoticed
- Developers cannot diagnose issues

**Recommended Fix:**
```python
try:
    template_content = str(reviewer.card.template().get('qfmt', ''))
    template_id = generate_template_hash(template_content)[:16]
except (AttributeError, KeyError, TypeError) as e:
    log_debug(f"Could not extract template ID: {e}")
    template_id = "unknown_template"
```

**Priority:** Fix immediately before next release

---

### 2. Inconsistent Error Handling Patterns

#### Pattern A: Comprehensive (security.py, tts_control.py)
```python
# security.py - BEST PRACTICE
def validate_text(text: str, ...) -> str:
    if not isinstance(text, str):
        raise TypeError("Expected string input")  # Specific exception
    
    if len(text) > max_length:
        raise ValueError(f"Text too long: {len(text)} > {max_length}")  # Detailed message
    
    # Clear contract: raises on invalid input
```

```python
# tts_control.py - EXCELLENT ERROR CONTEXT
except Exception as e:
    error_details = {
        "error": str(e),
        "system": system,
        "text_length": len(text),
        "rate": self.rate,
        "pitch": self.pitch
    }
    print(f"TTS Error: {error_details}")
    log_api_call("ankiTtsSpeak_error", error_details)
    return False
```

**Strengths:**
- ✅ Specific exception types
- ✅ Detailed error messages with context
- ✅ Proper logging
- ✅ Documented behavior (raises vs returns)

#### Pattern B: Defensive (card_actions.py, card_info.py, ui_control.py)
```python
# card_actions.py - DEFENSIVE BUT NO ERROR HANDLING
def anki_flag_card(flag: int) -> bool:
    card = get_current_card()
    if not card or not mw:  # ✅ Defensive check
        return False  # ❌ Silent failure, no logging
    
    # ... operation ...
    # ❌ No try/except, assumes all operations succeed
    
    return True
```

**Problems:**
- ❌ No exception handling (assumes operations never fail)
- ❌ Silent failures (user doesn't know why it failed)
- ❌ No logging (developers can't diagnose issues)
- ❌ No distinction between different failure modes

#### Pattern C: Generic Catch-All (api_bridge.py)
```python
# api_bridge.py - OVERLY GENERIC
except Exception as e:
    error_msg = f"Error executing {function_name}: {type(e).__name__}"
    log_debug(error_msg)  # ✅ Logging
    # Generic error message for security
    response = {"success": False, "error": f"Operation failed"}  # ❌ Not helpful
    _send_callback(reviewer, callback_id, response)
```

**Problems:**
- ❌ Hides specific error from user ("Operation failed" is not actionable)
- ❌ Only logs type, not message (loses context)
- ⚠️ "For security" justification may be misguided (users need some info)

---

### 3. Missing Error Handling by Module

#### card_actions.py (0% error handling)
**Functions without try/except:**
- `anki_flag_card()` - Card.setUserFlag() could fail
- `anki_mark_card()` - Note tag operations could fail
- `anki_bury_card()` - Scheduler operations could fail
- `anki_suspend_card()` - Scheduler operations could fail
- `anki_reset_progress()` - Card.flush() could fail
- `anki_search_card()` - Browser operations could fail
- `anki_set_card_due()` - Card operations could fail

**Potential Failures:**
- Database locked
- Invalid card state
- Permission errors
- Anki collection closed unexpectedly

**Impact:** Functions return `True` even if underlying operations fail

#### card_info.py (0% error handling)
**Functions without try/except:**
- `anki_get_new_card_count()` - Scheduler could be in invalid state
- `anki_get_eta()` - Division by zero if constants misconfigured
- All card metadata functions - Card attribute access could fail

**Potential Failures:**
- Scheduler not initialized
- Invalid deck state
- Card deleted while being accessed

**Impact:** Functions return `0` or `False`, no way to distinguish "no cards" from "error occurred"

#### ui_control.py (0% error handling)
**Functions without try/except:**
- `anki_show_options_menu()` - Dialog opening could fail
- `anki_show_toast()` - Tooltip rendering could fail
- `anki_show_navigation_drawer()` - State transition could fail

**Potential Failures:**
- GUI not initialized
- Dialog creation fails
- State transition blocked

#### tag_manager.py (0% error handling)
**Functions without try/except:**
- `anki_set_note_tags()` - Note.flush() could fail
- `anki_add_tag_to_note()` - Tag operations could fail

**Potential Failures:**
- Database write errors
- Invalid tag format after validation
- Note deleted concurrently

---

### 4. Error Response Inconsistencies

#### Current Patterns:

**Pattern 1: Boolean Returns (most functions)**
```python
def anki_flag_card(flag: int) -> bool:
    # ...
    return True  # or False
```
**Problem:** No way to communicate *why* it failed

**Pattern 2: Structured Responses (api_bridge.py)**
```python
response = {"success": False, "error": "Rate limit exceeded"}
```
**Good:** Communicates failure reason

**Pattern 3: Default Values (card_info.py)**
```python
def anki_get_new_card_count() -> int:
    if not mw or not mw.col:
        return 0  # Could mean "no cards" OR "error"
```
**Problem:** Ambiguous (0 cards vs error)

**Pattern 4: JSON Strings (tag_manager.py)**
```python
def anki_get_note_tags() -> str:
    if not card:
        return json.dumps([])  # Empty array vs error
```
**Problem:** Can't distinguish error from "no tags"

#### Recommendation: Standardize Error Responses

```python
# For functions returning data:
def anki_get_new_card_count() -> dict:
    """Returns: {"success": bool, "value": int, "error": str|None}"""
    if not mw or not mw.col:
        return {"success": False, "value": 0, "error": "Collection not available"}
    
    try:
        count = mw.col.sched.counts()[0]
        return {"success": True, "value": count, "error": None}
    except Exception as e:
        log_debug(f"Error getting new card count: {e}")
        return {"success": False, "value": 0, "error": str(e)}

# For action functions:
def anki_flag_card(flag: int) -> dict:
    """Returns: {"success": bool, "error": str|None}"""
    if not card or not mw:
        return {"success": False, "error": "No card available"}
    
    try:
        card.setUserFlag(flag)
        return {"success": True, "error": None}
    except Exception as e:
        log_debug(f"Error setting flag: {e}")
        return {"success": False, "error": f"Failed to set flag: {e}"}
```

**Benefits:**
- Consistent API across all functions
- JavaScript can distinguish errors from empty results
- Actionable error messages
- Backward compatible (can add `result_only` flag)

---

### 5. Logging Issues

#### Current State:
- ✅ `security.py`: No logging (raises exceptions appropriately)
- ✅ `tts_control.py`: Excellent logging with context
- ✅ `api_bridge.py`: Logs all calls and errors
- ❌ `card_actions.py`: Only logs API calls, not errors
- ❌ `card_info.py`: Only logs API calls, not errors
- ❌ `ui_control.py`: Only logs API calls, not errors

#### Problems:
1. **No error logging in most modules**
   - When `anki_flag_card()` fails, nothing is logged
   - Developers have no way to diagnose issues
   
2. **Inconsistent log levels**
   - Everything uses `log_debug()` (only shows if debug_mode enabled)
   - No ERROR or WARNING levels
   - Production errors go unnoticed

3. **Sanitization may hide useful info**
   - `sanitize_for_logging()` redacts text, query, tags
   - May remove context needed for debugging
   - Example: "Error in text validation" but can't see the text

#### Recommendations:

```python
# Add log levels to utils.py
def log_error(message: str, exc_info: Exception = None) -> None:
    """Always log errors, even if debug_mode is False."""
    safe_message = sanitize_for_logging(message)
    if exc_info:
        print(f"[AnkiDroid JS API ERROR] {safe_message}: {exc_info}")
    else:
        print(f"[AnkiDroid JS API ERROR] {safe_message}")

def log_warning(message: str) -> None:
    """Log warnings (always shown)."""
    safe_message = sanitize_for_logging(message)
    print(f"[AnkiDroid JS API WARNING] {safe_message}")

# Use in error handlers:
try:
    card.setUserFlag(flag)
except Exception as e:
    log_error(f"Failed to set flag {flag}", e)
    return {"success": False, "error": "Could not set flag"}
```

---

### 6. Fault Tolerance Analysis

#### What Happens When Things Go Wrong?

| **Failure Scenario** | **Current Behavior** | **Impact** | **Recommendation** |
|---------------------|---------------------|------------|-------------------|
| Database locked | Return False, no retry | ❌ User sees failure | Add retry with exponential backoff |
| Card deleted during operation | AttributeError (uncaught) | ❌ Crash or silent fail | Check card validity before operations |
| Anki collection closed | Return False/0 | ⚠️ Silent failure | Log error, show tooltip |
| Network error (future) | Not applicable | N/A | Add timeout and retry logic |
| Invalid input after validation | Assumed safe | ⚠️ May still fail | Add defensive checks |
| TTS platform error | Return False, log error | ✅ Graceful degradation | Good! Replicate pattern |
| Memory exhaustion | Bare except swallows | ❌ Silent failure | Fix bare except |
| JavaScript callback failure | No verification | ⚠️ Unknown | Add callback confirmation |

#### Recovery Strategies (Currently Missing)

**1. Retry Logic**
```python
def retry_on_db_lock(func, max_retries=3, delay=0.1):
    """Retry database operations on lock errors."""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if "database is locked" in str(e) and attempt < max_retries - 1:
                time.sleep(delay * (2 ** attempt))  # Exponential backoff
                continue
            raise
```

**2. Circuit Breaker Pattern**
```python
class CircuitBreaker:
    """Prevent repeated calls to failing operations."""
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.last_failure_time = None
    
    def call(self, func):
        if self.is_open():
            raise Exception("Circuit breaker is open")
        
        try:
            result = func()
            self.reset()
            return result
        except Exception as e:
            self.record_failure()
            raise
```

**3. Fallback Values**
```python
# Instead of returning 0 (ambiguous):
def anki_get_new_card_count() -> dict:
    try:
        count = mw.col.sched.counts()[0]
        return {"success": True, "value": count}
    except Exception:
        # Return last known good value or estimation
        return {"success": False, "value": get_cached_count(), "cached": True}
```

---

### 7. User Feedback Issues

#### Silent Failures (No User Notification)

**Examples:**
```python
# card_actions.py - User has no idea why flag wasn't set
def anki_flag_card(flag: int) -> bool:
    if not card or not mw:
        return False  # ❌ Silent failure
    # ...

# api_bridge.py - Generic "Operation failed" not helpful
response = {"success": False, "error": "Operation failed"}
```

**Impact:**
- User clicks button, nothing happens
- No explanation why
- User tries repeatedly (triggering rate limits)
- Frustration and confusion

#### Recommendations:

**Option 1: Toast Notifications (Non-Intrusive)**
```python
from .ui_control import anki_show_toast

def anki_flag_card(flag: int) -> bool:
    if not card or not mw:
        anki_show_toast("No card available to flag", short_length=True)
        return False
    
    try:
        card.setUserFlag(flag)
        return True
    except Exception as e:
        log_error(f"Failed to set flag: {e}")
        anki_show_toast("Could not set flag. See debug log.", short_length=False)
        return False
```

**Option 2: Error Details in Response (For JavaScript)**
```python
# JavaScript can show its own UI
response = {
    "success": False,
    "error": "Card not found",
    "details": {
        "reason": "no_card_available",
        "suggestion": "Please ensure a card is being reviewed"
    }
}
```

**Option 3: Configuration (User Choice)**
```python
# config.json
{
    "ui": {
        "show_error_toasts": true,  # Show errors to user
        "error_toast_duration_ms": 3000
    }
}
```

---

### 8. Input Validation Gaps

#### Areas Already Covered (Excellent)
- ✅ Text validation (security.py)
- ✅ Filename validation (path traversal prevention)
- ✅ Tag validation
- ✅ Integer/float range validation
- ✅ JSON payload size limits

#### Missing Validations

**1. Card Modification Bounds**
```python
# card_actions.py - No validation on factor
def anki_set_card_ease_factor(factor: int) -> bool:
    # Should validate: 1300 <= factor <= 5000 (Anki constraints)
    card.factor = factor  # ❌ Could set invalid values
```

**2. Flag Values**
```python
# card_actions.py - No validation
def anki_flag_card(flag: int) -> bool:
    flag = InputValidator.validate_integer(flag, 0, 7)  # Should add this
```

**3. Ease Button Values**
```python
# reviewer_control.py - Validation exists but could be in validator
if ease not in [1, 2, 3, 4]:
    return False  # Should raise ValueError for clarity
```

**4. Search Query Injection**
```python
# card_actions.py - Validates length but not for SQL injection
query = InputValidator.validate_text(query, max_length=500, allow_newlines=False)
# Anki's search is safe, but should document this assumption
```

---

## Recommendations by Priority

### 🔴 CRITICAL (Fix Immediately)

1. **Fix bare except block** in [api_bridge.py:83-86](../src/ankidroid_js_api/api_bridge.py#L83-L86)
   ```python
   except (AttributeError, KeyError, TypeError) as e:
       log_debug(f"Could not extract template ID: {e}")
       template_id = "unknown_template"
   ```

2. **Add error handling to card_actions.py** (highest impact)
   - Wrap all database/card operations in try/except
   - Log errors with context
   - Return structured responses

3. **Improve error messages in api_bridge.py**
   - Replace "Operation failed" with specific messages
   - Include enough context for user to understand issue
   - Balance security with usability

### 🟡 HIGH PRIORITY (Fix Soon)

4. **Standardize error response format**
   - Create `ErrorResponse` class or dict schema
   - Update all API functions to return structured responses
   - Document in API reference

5. **Add error logging levels**
   - Implement `log_error()`, `log_warning()`, `log_info()`
   - Always log errors (even when debug_mode=False)
   - Use appropriate levels

6. **Add try/except to card_info.py and ui_control.py**
   - Handle scheduler errors
   - Handle GUI errors
   - Return meaningful error responses

### 🟢 MEDIUM PRIORITY (Plan for Next Release)

7. **Implement retry logic for database operations**
   - Add retry decorator
   - Handle "database is locked" errors
   - Exponential backoff

8. **Add circuit breaker for failing operations**
   - Prevent repeated failures
   - Auto-recover after timeout
   - Log circuit breaker state changes

9. **Improve user feedback**
   - Add configuration for error toasts
   - Show errors in UI when appropriate
   - Provide actionable suggestions

10. **Add input validation for card constraints**
    - Validate factor ranges
    - Validate flag values
    - Document Anki's constraints

### 🔵 LOW PRIORITY (Nice to Have)

11. **Add health check API**
    ```python
    def anki_health_check() -> dict:
        return {
            "mw_available": mw is not None,
            "collection_available": mw.col is not None if mw else False,
            "reviewer_active": mw.reviewer is not None if mw else False,
            "card_available": get_current_card() is not None
        }
    ```

12. **Add error recovery documentation**
    - Document common errors
    - Provide troubleshooting steps
    - Add FAQs

13. **Create error handling tests**
    - Test all error paths
    - Test recovery mechanisms
    - Test error messages

---

## Testing Recommendations

### Error Path Testing (Currently Missing)

```python
# tests/test_error_handling.py

def test_card_action_handles_missing_card(mock_mw):
    """Test that card actions handle missing card gracefully."""
    mock_mw.reviewer.card = None
    
    result = anki_flag_card(1)
    
    assert result["success"] is False
    assert "card" in result["error"].lower()

def test_card_action_handles_db_lock(mock_mw, mock_card):
    """Test retry on database lock."""
    mock_card.setUserFlag.side_effect = [
        Exception("database is locked"),
        None  # Success on retry
    ]
    
    result = anki_flag_card(1)
    
    assert result["success"] is True
    assert mock_card.setUserFlag.call_count == 2

def test_bare_except_fix(mock_reviewer):
    """Ensure bare except is fixed and doesn't catch KeyboardInterrupt."""
    mock_reviewer.card.template.side_effect = KeyboardInterrupt()
    
    with pytest.raises(KeyboardInterrupt):
        api_call_handler(mock_reviewer, ...)
```

### Chaos Engineering Tests

```python
# Simulate failure scenarios
def test_chaos_database_lock():
    """Randomly inject database lock errors."""
    
def test_chaos_memory_pressure():
    """Test behavior under memory constraints."""
    
def test_chaos_concurrent_modifications():
    """Test concurrent card modifications."""
```

---

## Comparison with Industry Best Practices

| **Practice** | **Current State** | **Industry Standard** | **Gap** |
|-------------|------------------|---------------------|---------|
| Specific exceptions | ⚠️ Partial | ✅ Always use specific exceptions | Fix bare except, improve specificity |
| Error logging | ⚠️ Inconsistent | ✅ Always log errors | Add error logging to all modules |
| User feedback | ❌ Silent failures | ✅ Inform user of errors | Add toasts/responses |
| Retry logic | ❌ None | ✅ Retry transient failures | Implement for DB operations |
| Circuit breaker | ❌ None | ⚠️ For distributed systems | Consider for future features |
| Health checks | ❌ None | ✅ Expose system health | Add health check API |
| Error documentation | ⚠️ Partial | ✅ Document all errors | Create error catalog |
| Graceful degradation | ✅ TTS only | ✅ All features | Extend pattern |
| Structured responses | ⚠️ API bridge only | ✅ All APIs | Standardize across all functions |

---

## Code Examples: Before and After

### Example 1: card_actions.py - Flag Card

**Before (Current):**
```python
def anki_flag_card(flag: int) -> bool:
    """Set a flag on the current card."""
    log_api_call("ankiSetFlag", {"flag": flag})
    
    card = get_current_card()
    if not card or not mw:
        return False
    
    card.setUserFlag(flag)
    mw.requireReset()
    
    return True
```

**After (Recommended):**
```python
def anki_flag_card(flag: int) -> dict:
    """Set a flag on the current card.
    
    Args:
        flag: Flag value (0-7)
    
    Returns:
        {
            "success": bool,
            "error": str | None,
            "flag": int | None  # Actual flag set (for confirmation)
        }
    """
    log_api_call("ankiSetFlag", {"flag": flag})
    
    # Validate input
    try:
        flag = InputValidator.validate_integer(flag, 0, 7)
    except (TypeError, ValueError) as e:
        log_error(f"Invalid flag value: {e}")
        return {"success": False, "error": str(e), "flag": None}
    
    # Check prerequisites
    card = get_current_card()
    if not card or not mw:
        error_msg = "No card available to flag"
        log_warning(error_msg)
        if get_config().get("ui", {}).get("show_error_toasts", True):
            anki_show_toast(error_msg, short_length=True)
        return {"success": False, "error": error_msg, "flag": None}
    
    # Perform operation with error handling
    try:
        card.setUserFlag(flag)
        mw.requireReset()
        return {"success": True, "error": None, "flag": flag}
    except Exception as e:
        error_msg = f"Failed to set flag: {type(e).__name__}"
        log_error(error_msg, e)
        if get_config().get("ui", {}).get("show_error_toasts", True):
            anki_show_toast(f"Could not set flag ({type(e).__name__})", short_length=False)
        return {"success": False, "error": error_msg, "flag": None}
```

### Example 2: api_bridge.py - Fix Bare Except

**Before (Current - DANGEROUS):**
```python
try:
    template_content = str(reviewer.card.template().get('qfmt', ''))
    template_id = generate_template_hash(template_content)[:16]
except:
    pass
```

**After (Recommended):**
```python
try:
    template = reviewer.card.template()
    template_content = str(template.get('qfmt', '')) if template else ''
    template_id = generate_template_hash(template_content)[:16] if template_content else "no_template"
except (AttributeError, KeyError, TypeError) as e:
    # Card might not have template in some edge cases (e.g., deleted template)
    log_debug(f"Could not extract template ID: {type(e).__name__}: {e}")
    template_id = "unknown_template"
except Exception as e:
    # Unexpected error - log for investigation but don't crash
    log_error(f"Unexpected error getting template ID: {type(e).__name__}: {e}", e)
    template_id = "error_template"
```

### Example 3: card_info.py - Distinguish Errors from Empty Results

**Before (Current - Ambiguous):**
```python
def anki_get_new_card_count() -> int:
    """Get the count of new cards remaining in the deck."""
    log_api_call("ankiGetNewCardCount")
    
    if not mw or not mw.col:
        return 0  # Could mean "no cards" OR "error"
    
    deck_id = mw.col.decks.selected()
    return mw.col.sched.counts()[0]
```

**After (Recommended):**
```python
def anki_get_new_card_count() -> dict:
    """Get the count of new cards remaining in the deck.
    
    Returns:
        {
            "success": bool,
            "count": int,
            "error": str | None
        }
    """
    log_api_call("ankiGetNewCardCount")
    
    if not mw or not mw.col:
        error_msg = "Anki collection not available"
        log_warning(error_msg)
        return {"success": False, "count": 0, "error": error_msg}
    
    try:
        counts = mw.col.sched.counts()
        new_count = counts[0]
        return {"success": True, "count": new_count, "error": None}
    except IndexError as e:
        # Scheduler counts format unexpected
        log_error(f"Scheduler counts format error: {e}", e)
        return {"success": False, "count": 0, "error": "Invalid scheduler state"}
    except Exception as e:
        # Other scheduler errors
        log_error(f"Error getting new card count: {e}", e)
        return {"success": False, "count": 0, "error": f"Scheduler error: {type(e).__name__}"}
```

---

## Implementation Checklist

### Phase 1: Critical Fixes (Week 1)
- [ ] Fix bare except in api_bridge.py
- [ ] Add log_error() and log_warning() to utils.py
- [ ] Add error handling to anki_flag_card()
- [ ] Add error handling to anki_mark_card()
- [ ] Add error handling to anki_suspend_card()
- [ ] Test critical fixes
- [ ] Deploy hotfix release

### Phase 2: Core Improvements (Week 2-3)
- [ ] Add error handling to all card_actions.py functions
- [ ] Add error handling to all card_info.py functions
- [ ] Add error handling to all ui_control.py functions
- [ ] Add error handling to tag_manager.py
- [ ] Standardize return types (use dict responses)
- [ ] Update tests for new response format

### Phase 3: Enhanced Features (Week 4)
- [ ] Implement retry logic for DB operations
- [ ] Add configuration for error toasts
- [ ] Improve error messages in api_bridge.py
- [ ] Add input validation for all card constraints
- [ ] Create error handling tests
- [ ] Update documentation

### Phase 4: Polish (Week 5+)
- [ ] Add circuit breaker pattern
- [ ] Implement health check API
- [ ] Create error recovery documentation
- [ ] Add chaos engineering tests
- [ ] Performance test error paths
- [ ] Final review and release

---

## Metrics and Monitoring

### Current Coverage (Estimated)

| **Module** | **Functions** | **With Error Handling** | **Coverage %** |
|-----------|--------------|------------------------|---------------|
| security.py | 7 | 7 | 100% ✅ |
| tts_control.py | 3 | 3 | 100% ✅ |
| api_bridge.py | 5 | 4 | 80% ⚠️ |
| utils.py | 6 | 2 | 33% ⚠️ |
| card_actions.py | 15 | 0 | 0% ❌ |
| card_info.py | 15 | 0 | 0% ❌ |
| ui_control.py | 8 | 0 | 0% ❌ |
| tag_manager.py | 3 | 0 | 0% ❌ |
| reviewer_control.py | 6 | 0 | 0% ❌ |
| **TOTAL** | **68** | **16** | **24%** ❌ |

### Target Coverage After Improvements

| **Module** | **Target Coverage** | **ETA** |
|-----------|-------------------|---------|
| All modules | 100% | Phase 3 complete |

### Error Rate Monitoring (Recommended)

```python
# Add to utils.py
_error_counts = defaultdict(int)

def log_error(message: str, exc_info: Exception = None) -> None:
    """Log errors and track error rates."""
    _error_counts[type(exc_info).__name__] += 1
    # ... existing logging ...

def get_error_stats() -> dict:
    """Get error statistics for monitoring."""
    return dict(_error_counts)
```

---

## Conclusion

### Summary of Gaps

1. **Critical Security Issue:** Bare except block (MUST FIX)
2. **76% of functions lack error handling**
3. **Inconsistent error patterns** across modules
4. **Silent failures** without user feedback
5. **No retry logic** for transient failures
6. **Ambiguous return values** (0 could mean error or empty)

### Expected Outcomes After Implementation

- ✅ **100% error handling coverage**
- ✅ **Consistent error response format**
- ✅ **Improved debuggability** (proper logging)
- ✅ **Better user experience** (error feedback)
- ✅ **Increased reliability** (retry logic)
- ✅ **Maintainability** (standardized patterns)

### Estimated Effort

- **Phase 1 (Critical):** 4-8 hours
- **Phase 2 (Core):** 16-24 hours
- **Phase 3 (Enhanced):** 12-16 hours
- **Phase 4 (Polish):** 8-12 hours
- **Total:** 40-60 hours (~1.5-2 weeks)

### Risk Assessment

**Low Risk Changes:**
- Adding error logging (Phase 1-2)
- Improving error messages (Phase 2)
- Adding validation (Phase 2-3)

**Medium Risk Changes:**
- Changing return types to dicts (Phase 2)
  - Risk: Breaks existing JavaScript code
  - Mitigation: Add backward compatibility mode

**High Risk Changes:**
- Adding retry logic (Phase 3)
  - Risk: Could mask real issues
  - Mitigation: Add max retries, log all retries

---

## Appendices

### A. Error Taxonomy

**User Errors (Validation):**
- Invalid input (handled by security.py)
- Out of range values
- Path traversal attempts

**System Errors (Availability):**
- Anki not initialized
- Collection not available
- Card not present

**Transient Errors (Retry-able):**
- Database locked
- Temporary resource unavailability

**Permanent Errors (Not Retry-able):**
- Invalid card state
- Permission denied
- Feature not supported

### B. Error Message Templates

```python
ERROR_MESSAGES = {
    "no_card": "No card is currently being reviewed",
    "no_collection": "Anki collection is not available",
    "db_locked": "Database is temporarily locked. Retrying...",
    "invalid_input": "Invalid {param}: {details}",
    "operation_failed": "Failed to {operation}: {reason}",
    "rate_limited": "Too many requests. Please wait {seconds} seconds.",
}
```

### C. References

- [PEP 8 - Programming Recommendations](https://pep8.org/#programming-recommendations)
- [Python Exception Handling Best Practices](https://docs.python.org/3/tutorial/errors.html)
- [Google Python Style Guide - Exceptions](https://google.github.io/styleguide/pyguide.html#24-exceptions)
- [Anki Add-on Development Guide](https://addon-docs.ankiweb.net/)

---

**Next Steps:**
1. Review this analysis with the team
2. Prioritize fixes based on impact
3. Create GitHub issues for tracking
4. Begin Phase 1 implementation
5. Update test suite to cover error paths
