# Code Review: Best Practices & SOLID Principles

## Executive Summary

This review evaluates the AnkiDroid JS API codebase against clean code principles and SOLID design patterns. The code demonstrates good security practices and solid testing coverage, but there are opportunities for improvement in architecture, maintainability, and adherence to SOLID principles.

**Overall Grade: B+**
- Security: A
- Testing: A
- SOLID Principles: C+
- Clean Code: B
- Performance: A

---

## SOLID Principles Analysis

### ❌ **S - Single Responsibility Principle (Violations Found)**

#### Issue 1: `api_bridge.py` Has Multiple Responsibilities
**Current State:**
- Handles command parsing
- Manages API registration  
- Performs rate limiting
- Injects JavaScript
- Patches Anki internals
- Sends callbacks

**Impact:** Changes to any of these concerns require modifying the same file, increasing risk of bugs.

**Recommendation:**
```python
# Separate into distinct modules:
- api_registry.py      # API function registration
- command_parser.py    # Parse ankidroidjs: commands
- js_injector.py       # Handle JavaScript injection
- callback_sender.py   # Send responses to JavaScript
```

#### Issue 2: `TTSController` Mixes Business Logic and Platform-Specific Code
**Current State:** Single class contains both TTS state management AND platform-specific implementations.

**Recommendation:**
```python
# Use Strategy pattern
class TTSController:
    def __init__(self, speaker: TTSSpeaker):
        self._speaker = speaker  # Platform-specific implementation
        
class WindowsTTSSpeaker(TTSSpeaker):
    def speak(self, text: str) -> bool: ...

class MacOSTTSSpeaker(TTSSpeaker):
    def speak(self, text: str) -> bool: ...
```

---

### ✅ **O - Open/Closed Principle (Mostly Compliant)**

**Good:** API registration system is open for extension:
```python
register_api_function("ankiNewFunction", new_function)  # Easy to add
```

**Issue:** Adding new validation types requires modifying `InputValidator` class.

**Recommendation:**
```python
# Use validator registry pattern
class InputValidator:
    _validators: Dict[str, Callable] = {}
    
    @classmethod
    def register(cls, name: str, validator: Callable):
        cls._validators[name] = validator
    
    @classmethod
    def validate(cls, name: str, value: Any) -> Any:
        return cls._validators[name](value)
```

---

### ❌ **L - Liskov Substitution Principle (N/A)**

No inheritance hierarchies present, so LSP doesn't apply. However, lack of abstraction is itself a design issue (see below).

---

### ❌ **I - Interface Segregation Principle (Violations Found)**

#### Issue: `mw` (MainWindow) Is a God Object
**Current State:** Every module depends on the monolithic `mw` object from Anki:
```python
if not mw or not mw.col or not mw.reviewer:  # Coupled to everything
    return False
```

**Impact:** Modules depend on interfaces they don't use, making testing difficult.

**Recommendation:**
```python
# Define minimal interfaces
class ReviewerInterface(Protocol):
    def get_current_card(self) -> Optional[Card]: ...

class CollectionInterface(Protocol):
    def get_scheduler(self) -> Scheduler: ...

# Inject dependencies
def anki_mark_card(reviewer: ReviewerInterface) -> bool:
    card = reviewer.get_current_card()
    ...
```

---

### ❌ **D - Dependency Inversion Principle (Violations Found)**

#### Issue 1: High-Level Modules Depend on Low-Level Details
**Current State:** API functions directly import and use `mw`, `aqt.utils`, concrete Anki classes:
```python
from aqt import mw  # Direct dependency on concrete implementation
from aqt.utils import tooltip

def anki_show_toast(text: str):
    if mw:  # Tightly coupled
        tooltip(text)
```

**Recommendation:**
```python
# Depend on abstractions
class UIService(ABC):
    @abstractmethod
    def show_message(self, text: str, duration: int) -> None: ...

class AnkiUIService(UIService):
    def show_message(self, text: str, duration: int) -> None:
        tooltip(text, duration)

# Inject dependency
def anki_show_toast(text: str, ui_service: UIService = None):
    service = ui_service or get_ui_service()
    service.show_message(text, 2000)
```

#### Issue 2: Global State Throughout
**Current State:**
- `API_REGISTRY` is module-level dict
- `_tts_controller` is global singleton
- `RateLimiter` uses class variables as global state

**Problems:**
- Makes testing difficult (must reset globals)
- Thread-safety concerns
- Hidden dependencies

**Recommendation:**
```python
# Use dependency injection
class APIBridge:
    def __init__(self, rate_limiter: RateLimiter, registry: APIRegistry):
        self._rate_limiter = rate_limiter
        self._registry = registry
```

---

## Clean Code Issues

### 🔴 **CRITICAL: Dead Code in `security.py`**

**Location:** [security.py](../src/ankidroid_js_api/security.py#L281-L290)

```python
def sanitize_for_logging(data: str, max_length: int = 100) -> str:
    # ... actual code ...
    return data[:max_length] + "..." if len(data) > max_length else data
    
    # Dead code below this line (unreachable)
    data = re.sub(r'"text":\s*"[^"]*"', '"text":"[REDACTED]"', data)
    data = re.sub(r'"query":\s*"[^"]*"', '"query":"[REDACTED]"', data)
    # ... more unreachable code ...
```

**Impact:** Confusing, suggests code was copy-pasted during refactoring.

**Action:** MUST be removed immediately.

---

### ⚠️ **Magic Numbers**

**Issue:** Numerous hardcoded values without explanation:

```python
# api_bridge.py
MAX_JSON_SIZE = 10 * 1024  # Why 10KB?

# card_info.py
total_seconds = (new_count * 20) + (lrn_count * 10) + (rev_count * 10)
# Why 20 and 10 seconds?

# tts_control.py
wpm = int(175 * self.rate)  # Why 175 WPM?

# security.py
_CLEANUP_INTERVAL: float = 300.0  # Why 5 minutes?
```

**Recommendation:**
```python
class Constants:
    MAX_JSON_PAYLOAD_BYTES = 10 * 1024  # Prevent DoS attacks
    NEW_CARD_TIME_ESTIMATE_SEC = 20  # Average time per new card
    REVIEW_CARD_TIME_ESTIMATE_SEC = 10  # Average time per review
    TTS_DEFAULT_WPM = 175  # Standard English speaking rate
    RATE_LIMITER_CLEANUP_INTERVAL_SEC = 300  # Balance memory vs performance
```

---

### ⚠️ **Function Length**

**Issue:** `handle_pycmd()` in [api_bridge.py](../src/ankidroid_js_api/api_bridge.py#L31-L96) is 65 lines long.

**Recommendation:** Extract smaller functions:
```python
def handle_pycmd(reviewer: Reviewer, cmd: str) -> None:
    if not cmd.startswith("ankidroidjs:"):
        return
    
    parts = _parse_command(cmd)
    if not parts:
        return
    
    template_id = _get_template_id(reviewer)
    
    if not _check_rate_limit(template_id, parts.function_name):
        _send_rate_limit_error(reviewer, parts.callback_id)
        return
    
    _execute_api_call(reviewer, parts)

def _parse_command(cmd: str) -> Optional[CommandParts]:
    """Extract callback_id, function_name, and args from command."""
    ...

def _check_rate_limit(template_id: str, function_name: str) -> bool:
    """Check if API call is within rate limit."""
    ...
```

---

### ⚠️ **Inconsistent Error Handling**

**Issue:** Some functions return `False`, others raise exceptions, some do both:

```python
# Pattern 1: Return False
def anki_mark_card() -> bool:
    if not card or not mw:
        return False  # Silent failure

# Pattern 2: Raise exception
def validate_text(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("Expected string input")  # Explicit failure

# Pattern 3: Try/catch with return False
def speak(self, text: str) -> bool:
    try:
        self._speak_windows(text)
        return True
    except Exception as e:
        print(f"TTS Error: {e}")
        return False  # Exception converted to False
```

**Recommendation:** Be consistent:
```python
# For API functions (called from JavaScript):
# Return Result object with success/error details
@dataclass
class Result:
    success: bool
    data: Any = None
    error: Optional[str] = None

def anki_mark_card() -> Result:
    if not card:
        return Result(success=False, error="No card available")
    ...
    return Result(success=True, data={"marked": True})

# For internal functions:
# Raise exceptions, let caller handle
def validate_text(text: str) -> str:
    if not isinstance(text, str):
        raise ValidationError("Expected string")
    return text
```

---

### ⚠️ **Duplicate Code**

#### Issue 1: Repeated Guard Clauses
**Found in:** `card_actions.py`, `card_info.py`, `reviewer_control.py`

```python
# Repeated in 20+ functions
if not mw or not mw.col or not mw.reviewer:
    return False

card = get_current_card()
if not card:
    return False
```

**Recommendation:**
```python
def requires_card(func):
    """Decorator to ensure card availability."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        card = get_current_card()
        if not card or not mw or not mw.col:
            return Result(success=False, error="No card available")
        return func(card, *args, **kwargs)
    return wrapper

@requires_card
def anki_mark_card(card: Card) -> Result:
    """Card is guaranteed to exist."""
    note = card.note()
    ...
```

#### Issue 2: Duplicated Button Registrations
**Location:** [api_bridge.py](../src/ankidroid_js_api/api_bridge.py#L193-L201)

```python
register_api_function("ankiAnswerEase1", reviewer_control.anki_answer_ease1)
# ...
register_api_function("buttonAnswerEase1", reviewer_control.anki_answer_ease1)
# Same functions registered twice
```

**Recommendation:**
```python
# Use aliases
ALIASES = {
    "buttonAnswerEase1": "ankiAnswerEase1",
    "buttonAnswerEase2": "ankiAnswerEase2",
    ...
}

def register_api_function(name: str, func: Callable, aliases: List[str] = None):
    API_REGISTRY[name] = func
    if aliases:
        for alias in aliases:
            API_REGISTRY[alias] = func
```

---

### ⚠️ **Naming Inconsistencies**

**Issue:** Mix of naming conventions:

```python
# Inconsistent prefixes
anki_get_new_card_count()  # anki_ prefix
get_current_card()  # No prefix

# Inconsistent abbreviations
anki_get_lrn_card_count()  # "lrn" abbreviated
anki_get_rev_card_count()  # "rev" abbreviated  
anki_get_new_card_count()  # "new" NOT abbreviated

# Private method inconsistency
def _send_callback()  # Snake case with underscore
class RateLimiter:
    def _cleanup_stale_entries()  # Snake case with underscore
    _buckets  # Class attribute with underscore (but public interface)
```

**Recommendation:**
- Public API functions: `anki_` prefix (for JavaScript calls)
- Internal helpers: descriptive names without prefix
- Abbreviations: Use full words (`learning`, `review`)
- Private: `_` prefix consistently for private methods/attributes

---

### ⚠️ **Comments Explain "What" Instead of "Why"**

**Issue:**
```python
# Get counts
counts = mw.col.sched.counts()  # Comment repeats code

# Set the flag directly for compatibility with AnkiDroid
card.flags = flag_value  # Good - explains WHY
```

**Recommendation:**
```python
# Remove redundant comments
counts = mw.col.sched.counts()  # No comment needed, code is clear

# Keep comments that explain reasoning
card.flags = flag_value  # Desktop Anki requires direct attribute modification (bypasses undo system)
```

---

### ✅ **GOOD: Type Hints**

Code uses type hints extensively:
```python
def validate_text(text: str, max_length: int = 500) -> str:
    ...

def get_current_card() -> Optional[Card]:
    ...
```

**Suggestion:** Add `from __future__ import annotations` for forward references:
```python
from __future__ import annotations  # PEP 563

def process_card(card: Card) -> Card:  # No quotes needed
    ...
```

---

## Architecture Issues

### 🔴 **No Dependency Injection**

**Current:** Modules directly access global `mw` object:
```python
from aqt import mw

def anki_mark_card():
    if not mw:  # Global dependency
        return False
```

**Problems:**
- Impossible to test without full Anki environment
- Tight coupling to Anki implementation
- Cannot mock for unit tests

**Solution:**
```python
class CardService:
    def __init__(self, collection: Collection, reviewer: Reviewer):
        self._collection = collection
        self._reviewer = reviewer
    
    def mark_card(self) -> bool:
        card = self._reviewer.get_current_card()
        ...

# In tests
def test_mark_card():
    mock_collection = Mock(spec=Collection)
    mock_reviewer = Mock(spec=Reviewer)
    service = CardService(mock_collection, mock_reviewer)
    
    result = service.mark_card()
    assert result == True
```

---

### 🔴 **Tight Coupling to Anki Internals**

**Issue:** Code reaches deep into Anki's internal structure:
```python
# Direct access to private methods
mw.reviewer._showAnswer()
mw.reviewer._answerCard(ease)

# Deep property chains
template_content = str(reviewer.card.template().get('qfmt', ''))
```

**Risk:** Anki updates could break the add-on.

**Recommendation:**
- Create facade/adapter layer
- Abstract Anki specifics behind interfaces
- Use only public APIs when available

---

### ⚠️ **No Error Boundaries**

**Issue:** Exceptions in API calls can crash the reviewer:
```python
def handle_pycmd(reviewer: Reviewer, cmd: str) -> None:
    try:
        # ... code ...
    except Exception as e:
        # Catches exceptions, but what about before this?
        log_debug(error_msg)
```

**Recommendation:**
```python
def safe_api_call(func):
    """Decorator to wrap API calls in error boundary."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            return Result(success=False, error=str(e))
        except Exception as e:
            # Log error with stack trace
            log_error(f"{func.__name__} failed", exc_info=True)
            return Result(success=False, error="Internal error")
    return wrapper
```

---

## Testing Gaps

**Current:** 154 passing tests (excellent coverage!)

**Missing:**
1. **Integration tests for error paths**
   - What happens when Anki internals change?
   - How do race conditions behave?

2. **Property-based tests**
   - Validate InputValidator with random inputs
   - Test rate limiter under concurrent load

3. **Performance tests**
   - Ensure rate limiter cleanup doesn't block
   - Verify JavaScript injection doesn't slow card rendering

---

## Priority Recommendations

### 🔴 **CRITICAL (Fix Immediately)**

1. **Remove dead code** in [security.py](../src/ankidroid_js_api/security.py#L281-L290)
2. **Extract magic numbers** to named constants
3. **Add error boundaries** around all API calls

### 🟡 **HIGH PRIORITY (Fix in Next Iteration)**

4. **Split `api_bridge.py`** into smaller, focused modules
5. **Implement decorator** for repeated guard clauses
6. **Add Result type** for consistent error handling
7. **Use dependency injection** for testability

### 🟢 **MEDIUM PRIORITY (Continuous Improvement)**

8. **Create facade layer** for Anki internals
9. **Implement Strategy pattern** for TTS
10. **Add integration tests** for error scenarios
11. **Use validator registry** for extensibility

---

## Positive Highlights

✅ **Excellent:**
- Comprehensive security validation
- Pre-compiled regex patterns for performance
- Rate limiting to prevent abuse
- Extensive test coverage (154 tests)
- PII sanitization in logging
- Type hints throughout

✅ **Good:**
- Clear module organization by feature
- Consistent API naming (anki_ prefix)
- Detailed docstrings
- Configuration system

---

## Conclusion

The codebase demonstrates strong security practices and good test coverage, but has room for improvement in:
1. **SOLID adherence** - particularly SRP, ISP, and DIP
2. **Dependency management** - too much global state
3. **Clean code** - dead code, magic numbers, function length
4. **Architecture** - tight coupling to Anki internals

**Recommended First Steps:**
1. Remove dead code (5 minutes)
2. Extract constants (30 minutes)  
3. Add error boundaries (1 hour)
4. Refactor api_bridge.py (3 hours)

These changes will significantly improve maintainability and testability.
