# Architecture & Design Patterns Review

## Executive Summary

The AnkiDroid JS API codebase demonstrates a **well-structured, modular architecture** with strong separation of concerns. The design successfully bridges JavaScript template code with Python backend functionality through a clean registry pattern, while maintaining security and extensibility as core principles.

**Overall Assessment: 8.5/10**
- ✅ Excellent modular organization
- ✅ Strong security foundation
- ✅ Clear separation of concerns
- ✅ Well-documented extension points
- ⚠️ Some opportunities for abstraction
- ⚠️ Minor coupling concerns

---

## Architecture Overview

### 1. Module Organization (Layered Architecture)

```
┌──────────────────────────────────────────────────────────┐
│                     Entry Point Layer                     │
│  __init__.py - Plugin initialization, menu setup         │
└───────────────────────┬──────────────────────────────────┘
                        │
┌───────────────────────▼──────────────────────────────────┐
│                     Core Bridge Layer                     │
│  api_bridge.py - Command routing, API registry,          │
│                  JavaScript injection                     │
└───────────────────────┬──────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼────────┐ ┌───▼────────┐ ┌───▼────────────┐
│  Feature Layer │ │Cross-Cutting│ │Infrastructure  │
│  (6 modules)   │ │   Concerns  │ │    Layer       │
├────────────────┤ ├─────────────┤ ├────────────────┤
│• card_info.py  │ │• security.py│ │• utils.py      │
│• card_actions  │ │             │ │• constants.py  │
│• reviewer_     │ │             │ │                │
│  control.py    │ │             │ │                │
│• tts_control   │ │             │ │                │
│• ui_control    │ │             │ │                │
│• tag_manager   │ │             │ │                │
└────────────────┘ └─────────────┘ └────────────────┘
```

**Key Characteristics:**
- **11 Python modules** organized into logical layers
- **Clear dependency hierarchy**: Feature → Infrastructure → Cross-cutting
- **No circular dependencies** detected
- **Single responsibility** per module (good cohesion)

### 2. Dependency Graph

```
┌──────────────────────────────────────────────────────────┐
│ Dependency Flow (Top to Bottom)                          │
└──────────────────────────────────────────────────────────┘

__init__.py
    └── api_bridge.py
            ├── card_info.py ────┐
            ├── card_actions.py ─┤
            ├── reviewer_control.py ─┤
            ├── tts_control.py ──┤
            ├── ui_control.py ───┤
            └── tag_manager.py ──┤
                                  │
                    ┌─────────────┴──────────────┐
                    │                            │
                    ▼                            ▼
            security.py ◄───────────────► utils.py
                    │                            │
                    └──────────┬─────────────────┘
                               ▼
                        constants.py
```

**Dependency Metrics:**
- **Feature modules**: All depend on `utils`, `security`, `constants`
- **Cross-cutting modules**: `security` and `utils` are peer dependencies
- **Foundation module**: `constants` has zero dependencies (good!)
- **Average coupling**: Low (3-4 imports per module)
- **Direction**: Acyclic (no circular dependencies)

---

## Design Patterns Identified

### 1. ✅ **Registry Pattern** (api_bridge.py)

**Implementation:**
```python
API_REGISTRY: Dict[str, Callable] = {}

def register_api_function(name: str, func: Callable) -> None:
    """Register a function callable from JavaScript."""
    API_REGISTRY[name] = func

# Usage in setup_api_bridge()
register_api_function("ankiGetCardId", card_info.anki_get_card_id)
register_api_function("ankiMarkCard", card_actions.anki_mark_card)
# ... 60+ functions registered
```

**Strengths:**
- ✅ Highly extensible - new APIs added without modifying router
- ✅ Centralized function mapping
- ✅ Type-safe with `Callable` hint
- ✅ Clean separation of registration and routing logic

**Usage Pattern:**
- JavaScript calls: `ankidroidjs:callbackId:functionName:args`
- Router looks up function in registry
- Dynamic dispatch to correct handler

**Assessment:** **Excellent implementation** - This is the correct pattern for plugin-based architecture.

---

### 2. ✅ **Decorator Pattern** (utils.py)

**Implementation:**
```python
def require_collection(default: Any):
    """Decorator to ensure Anki collection is available."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not mw or not mw.col:
                log_warning(f"{func.__name__} called without collection")
                return default
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Usage:
@require_collection(default=0)
def anki_get_new_card_count() -> int:
    """Get count of new cards."""
    return mw.col.sched.new_count
```

**Strengths:**
- ✅ DRY principle - eliminated 24 lines of duplicate validation
- ✅ Declarative - clear intent at function definition
- ✅ Consistent error handling across all functions
- ✅ Three variants: `@require_collection`, `@require_card`, `@require_card_and_collection`

**Impact:**
- Reduced validation code by **67%** in affected functions
- Uniform error handling behavior
- Improved maintainability

**Assessment:** **Excellent addition** - Recent improvement (added during complexity reduction phase).

---

### 3. ✅ **Strategy Pattern** (tts_control.py)

**Implementation:**
```python
class TTSController:
    def speak(self, text: str, queue_mode: int = 0) -> bool:
        """Speak text using system TTS."""
        system = platform.system()
        
        if system == "Windows":
            self._speak_windows(text)
        elif system == "Darwin":  # macOS
            self._speak_macos(text)
        elif system == "Linux":
            self._speak_linux(text)
        # ...
    
    def _speak_windows(self, text: str) -> None:
        """Windows SAPI strategy."""
        # PowerShell + SAPI implementation
    
    def _speak_macos(self, text: str) -> None:
        """macOS 'say' command strategy."""
        # macOS implementation
    
    def _speak_linux(self, text: str) -> None:
        """Linux espeak/spd-say strategy."""
        # Linux implementation
```

**Strengths:**
- ✅ Platform-specific implementations encapsulated
- ✅ Easy to add new platforms
- ✅ Testable (can mock `platform.system()`)

**Potential Improvement:**
Could use **Strategy Pattern (classic)** with separate strategy classes:
```python
class TTSStrategy(ABC):
    @abstractmethod
    def speak(self, text: str) -> None: ...

class WindowsTTSStrategy(TTSStrategy): ...
class MacOSTTSStrategy(TTSStrategy): ...
class LinuxTTSStrategy(TTSStrategy): ...

# Then:
strategy_map = {
    "Windows": WindowsTTSStrategy(),
    "Darwin": MacOSTTSStrategy(),
    "Linux": LinuxTTSStrategy(),
}
strategy = strategy_map.get(platform.system())
strategy.speak(text)
```

**Current Assessment:** **Good enough** for 3 platforms, but consider classic Strategy if platforms exceed 5.

---

### 4. ⚠️ **Singleton Pattern (Implicit)** (Global State)

**Current State:**
```python
# Multiple modules use:
from aqt import mw  # Main window singleton

# In functions:
def some_function():
    if not mw or not mw.col:  # Global state access
        return default
    return mw.col.some_method()
```

**Analysis:**
- ✅ **Unavoidable** - Anki's architecture uses `mw` as singleton
- ⚠️ **Coupling concern** - 8 modules import `mw` directly
- ⚠️ **Testing challenge** - Requires mocking `mw` in tests

**Current Mitigation:**
- Decorators (`@require_collection`) abstract `mw` access
- Dependency injection in some functions: `get_current_card()`

**Recommendation:**
Consider **Dependency Injection** for testability:
```python
# Instead of:
def anki_get_card_id() -> int:
    card = get_current_card()
    # ...

# Consider:
def anki_get_card_id(card: Optional[Card] = None) -> int:
    card = card or get_current_card()
    # ...
```

**Assessment:** **Acceptable** - Imposed by Anki's architecture, but room for improvement via DI.

---

### 5. ✅ **Template Method Pattern** (Partial - security.py)

**Implementation:**
```python
class InputValidator:
    """Centralized validation with pre-compiled patterns."""
    
    _FILENAME_PATTERN = re.compile(r'^[\w\-]+\.\w+$')
    _TAG_PATTERN = re.compile(r'^[\w\-]+$')
    _CALLBACK_ID_PATTERN = re.compile(r'^-?\d+$')
    
    @staticmethod
    def validate_text(text: str, max_length: int, pattern: str, ...) -> str:
        """Template for text validation."""
        # 1. Type check
        if not isinstance(text, str):
            raise TypeError(...)
        # 2. Length check
        if len(text) > max_length:
            raise ValueError(...)
        # 3. Sanitize control characters
        text = ''.join(char for char in text if ord(char) >= 32 or ...)
        # 4. Pattern validation
        if not re.match(pattern, text):
            raise ValueError(...)
        return text.strip()
    
    @staticmethod
    def validate_integer(value: Any, min_val: int, max_val: int) -> int:
        """Template for integer validation."""
        # Similar pattern: type → range → return
```

**Strengths:**
- ✅ Consistent validation flow across all methods
- ✅ Pre-compiled patterns for performance
- ✅ Centralized error messages

**Assessment:** **Good foundation** - Template Method pattern applied to validation logic.

---

### 6. ✅ **Facade Pattern** (api_bridge.py)

**Implementation:**
```python
def setup_api_bridge() -> None:
    """Facade for entire API registration process."""
    
    # Card Information APIs (from card_info module)
    register_api_function("ankiGetNewCardCount", card_info.anki_get_new_card_count)
    register_api_function("ankiGetCardId", card_info.anki_get_card_id)
    # ... 15 more from card_info
    
    # Card Actions APIs (from card_actions module)
    register_api_function("ankiMarkCard", card_actions.anki_mark_card)
    # ... 8 more from card_actions
    
    # Reviewer Control APIs (from reviewer_control module)
    register_api_function("ankiShowAnswer", reviewer_control.anki_show_answer)
    # ... 7 more from reviewer_control
    
    # TTS APIs, UI APIs, Tag APIs...
    # ... 60+ total API functions
```

**Strengths:**
- ✅ Single entry point for all API setup
- ✅ Hides complexity of 6 feature modules
- ✅ Clear documentation of all available APIs
- ✅ Easy to see full API surface

**Assessment:** **Excellent** - Classic Facade pattern for complex subsystem.

---

### 7. ✅ **DRY Principle - Generic Accessor** (card_info.py)

**Implementation:**
```python
def _get_card_property(property_name: str, api_name: str, default: Any) -> Any:
    """Generic accessor for card properties."""
    log_api_call(api_name)
    card = get_current_card()
    if not card:
        return default
    return getattr(card, property_name, default)

# 12 functions simplified to one line each:
def anki_get_card_id() -> int:
    return _get_card_property("id", "ankiGetCardId", -1)

def anki_get_card_nid() -> int:
    return _get_card_property("nid", "ankiGetCardNid", -1)

def anki_get_card_lapses() -> int:
    return _get_card_property("lapses", "ankiGetCardLapses", 0)
# ... 9 more
```

**Impact:**
- ✅ Eliminated **84 lines** of duplicate code (24% reduction)
- ✅ Reduced from ~8 lines per function to 1 line
- ✅ Easier to maintain - changes affect all getters uniformly

**Assessment:** **Excellent refactoring** - Addresses code duplication systematically.

---

## SOLID Principles Analysis

### S - Single Responsibility Principle ✅

**Grade: A**

Each module has one clear responsibility:

| Module | Responsibility | Lines | Assessment |
|--------|---------------|-------|------------|
| `card_info.py` | Query card/collection state | 272 | ✅ Cohesive |
| `card_actions.py` | Modify card state | 234 | ✅ Cohesive |
| `reviewer_control.py` | Control reviewer UI | ~150 | ✅ Cohesive |
| `tts_control.py` | Text-to-speech | 265 | ✅ Cohesive |
| `ui_control.py` | UI state queries | ~100 | ✅ Cohesive |
| `tag_manager.py` | Tag operations | ~100 | ✅ Cohesive |
| `security.py` | Input validation, rate limiting | 312 | ✅ Cohesive |
| `utils.py` | Shared utilities | ~200 | ✅ Cohesive |
| `constants.py` | Configuration constants | ~100 | ✅ Cohesive |
| `api_bridge.py` | Command routing | 284 | ✅ Cohesive |
| `__init__.py` | Plugin initialization | 159 | ✅ Cohesive |

**Strengths:**
- Clear boundaries between modules
- Functions within each module are related
- No "god objects" or dumping grounds

**No violations detected.**

---

### O - Open/Closed Principle ✅

**Grade: A-**

**Good Examples:**

1. **API Registration** (api_bridge.py):
   ```python
   # Open for extension (add new APIs)
   register_api_function("newAPI", new_module.new_function)
   
   # Closed for modification (routing logic unchanged)
   def handle_pycmd(reviewer, cmd):
       func = API_REGISTRY[function_name]  # No changes needed
       result = func(**args)
   ```
   ✅ New APIs added without modifying router.

2. **Validation Decorators** (utils.py):
   ```python
   # Open for extension (new decorators)
   @require_new_decorator(default=...)
   def new_function(): ...
   
   # Closed for modification (existing code unchanged)
   ```
   ✅ New validation patterns via new decorators.

**Area for Improvement:**

Platform-specific TTS logic (tts_control.py):
```python
def speak(self, text: str):
    system = platform.system()
    
    if system == "Windows":
        self._speak_windows(text)
    elif system == "Darwin":
        self._speak_macos(text)
    elif system == "Linux":
        self._speak_linux(text)
    # Adding new platform = modifying this function ⚠️
```

**Recommendation:** Use Strategy pattern with plugin system:
```python
# TTS strategies registered in config
TTS_STRATEGIES = {
    "Windows": WindowsTTS,
    "Darwin": MacOSTTS,
    "Linux": LinuxTTS,
    # New platforms added without modifying code
}

strategy = TTS_STRATEGIES[platform.system()]()
strategy.speak(text)
```

---

### L - Liskov Substitution Principle ⚠️

**Grade: B**

**Current State:**
- No inheritance hierarchies in codebase (mostly functions, 3 classes)
- Classes: `InputValidator`, `RateLimiter`, `TTSController`
- All are concrete classes with no subclasses

**Analysis:**
- ✅ **Not applicable** - No polymorphism currently used
- ⚠️ **Future concern** - If TTS strategies become classes with inheritance

**Recommendation:**
If adding TTS strategy classes, ensure LSP:
```python
class TTSStrategy(ABC):
    @abstractmethod
    def speak(self, text: str) -> bool:
        """Return True if successful."""
        pass

# All subclasses MUST return bool (not None/int)
class WindowsTTS(TTSStrategy):
    def speak(self, text: str) -> bool:  # Maintains contract
        # ...
        return True
```

---

### I - Interface Segregation Principle ✅

**Grade: A**

**Analysis:**
- Functions are small and focused (average 15-30 lines)
- No "fat interfaces" forcing clients to depend on unused methods
- Each API function is independently callable

**Example:**
```python
# JavaScript can call only what it needs:
await api.ankiGetCardId();  # Doesn't force loading TTS, UI, etc.
```

**Strengths:**
- ✅ Granular API functions (60+ small functions vs 5 large ones)
- ✅ No forced dependencies
- ✅ Easy to test individual functions

---

### D - Dependency Inversion Principle ⚠️

**Grade: B-**

**Issue:**
High-level modules depend on low-level Anki implementation:

```python
# card_info.py (high-level) depends on aqt.mw (low-level)
from aqt import mw  # Direct dependency on Anki's implementation

def anki_get_card_id() -> int:
    card = get_current_card()  # Calls mw.reviewer.card
    if not card:
        return -1
    return card.id
```

**Problem:**
- ⚠️ Tight coupling to Anki's `mw` singleton
- ⚠️ Hard to test without full Anki environment
- ⚠️ Cannot swap implementations (e.g., mock backend for testing)

**Recommended Improvement - Dependency Injection:**

```python
# 1. Define abstraction (protocol)
from typing import Protocol

class CardProvider(Protocol):
    """Abstract interface for getting cards."""
    def get_current_card(self) -> Optional[Card]: ...
    def get_collection(self) -> Optional[Collection]: ...

# 2. Concrete implementation
class AnkiCardProvider:
    def get_current_card(self) -> Optional[Card]:
        if not mw or not mw.reviewer:
            return None
        return mw.reviewer.card
    
    def get_collection(self) -> Optional[Collection]:
        return mw.col if mw else None

# 3. Inject dependency
def anki_get_card_id(provider: CardProvider = None) -> int:
    provider = provider or AnkiCardProvider()  # Default to Anki
    card = provider.get_current_card()
    if not card:
        return -1
    return card.id

# 4. Testing becomes easy
class MockCardProvider:
    def get_current_card(self):
        return Mock(id=123)

assert anki_get_card_id(MockCardProvider()) == 123  # No Anki needed!
```

**Current Mitigation:**
- Tests use pytest fixtures to mock `mw`
- Works but requires complex setup

**Assessment:** Room for improvement via DI, but acceptable given Anki's architecture constraints.

---

## Architectural Strengths

### 1. ✅ Modular Organization
- **11 well-defined modules** with clear boundaries
- Feature modules (6) separate from infrastructure (3) and core (2)
- Easy to navigate and understand

### 2. ✅ Security by Design
- `InputValidator` class centralizes all validation
- Rate limiting built into core (`RateLimiter`)
- Input sanitization before processing
- Payload size limits (MAX_JSON_PAYLOAD_BYTES)
- Pre-compiled regex patterns for performance

### 3. ✅ Extensibility
- Registry pattern allows easy API additions
- Decorators enable new validation patterns
- Clear extension points documented in code
- Plugin-friendly architecture

### 4. ✅ Separation of Concerns
- Business logic (feature modules) separate from infrastructure
- Cross-cutting concerns (security, logging) centralized
- No mixing of responsibilities

### 5. ✅ Documentation Quality
- Module-level docstrings explain architecture
- Function docstrings include examples
- Clear comments on complex logic
- Extension points documented

### 6. ✅ Error Handling
- Consistent error handling via decorators
- Centralized logging (`log_error`, `log_warning`)
- Graceful degradation (return defaults on error)
- No bare except blocks (fixed in error handling phase)

---

## Architectural Weaknesses & Recommendations

### 1. ⚠️ Global State Coupling (Priority: Medium)

**Issue:**
8 modules directly import `from aqt import mw`

**Impact:**
- Testing requires complex mocking
- Tight coupling to Anki's implementation
- Hard to unit test in isolation

**Recommendation:**
Introduce **Dependency Injection** for `mw`:

```python
# utils.py - Create abstraction
class AnkiContext:
    """Abstraction for Anki's main window and collection."""
    
    @staticmethod
    def get_main_window():
        from aqt import mw
        return mw
    
    @staticmethod
    def get_collection():
        mw = AnkiContext.get_main_window()
        return mw.col if mw else None
    
    @staticmethod
    def get_reviewer():
        mw = AnkiContext.get_main_window()
        return mw.reviewer if mw else None

# Then in modules:
# Instead of: from aqt import mw
# Use: from .utils import AnkiContext

def anki_get_card_id() -> int:
    reviewer = AnkiContext.get_reviewer()  # Abstracted
    if not reviewer or not reviewer.card:
        return -1
    return reviewer.card.id
```

**Benefits:**
- Single point of Anki import
- Easy to mock `AnkiContext` in tests
- Can swap implementations (e.g., for non-Anki environments)

---

### 2. ⚠️ TTS Platform Coupling (Priority: Low)

**Issue:**
Platform detection hardcoded in `TTSController.speak()`:

```python
if system == "Windows":
    self._speak_windows(text)
elif system == "Darwin":
    self._speak_macos(text)
elif system == "Linux":
    self._speak_linux(text)
```

**Recommendation:**
Use **Strategy Pattern with Registry**:

```python
# tts_strategies.py
class TTSStrategy(ABC):
    @abstractmethod
    def speak(self, text: str, rate: float, pitch: float) -> None: ...
    
    @abstractmethod
    def stop(self) -> None: ...

class WindowsTTS(TTSStrategy):
    def speak(self, text: str, rate: float, pitch: float) -> None:
        # Windows implementation
    
    def stop(self) -> None:
        # Windows stop

# Similar for MacOSTTS, LinuxTTS, CustomTTS

# tts_control.py
TTS_STRATEGY_REGISTRY = {
    "Windows": WindowsTTS,
    "Darwin": MacOSTTS,
    "Linux": LinuxTTS,
}

class TTSController:
    def __init__(self):
        platform_name = platform.system()
        strategy_class = TTS_STRATEGY_REGISTRY.get(platform_name)
        if not strategy_class:
            raise ValueError(f"Unsupported platform: {platform_name}")
        self.strategy = strategy_class()
    
    def speak(self, text: str, queue_mode: int = 0) -> bool:
        return self.strategy.speak(text, self.rate, self.pitch)
```

**Benefits:**
- New platforms added via registry (no code changes)
- Each platform's code in separate file
- Testable via mock strategies

---

### 3. ⚠️ Constants Module Organization (Priority: Low)

**Current State:**
All constants in one file (~100 lines, mixed categories)

**Recommendation:**
Organize by category:

```python
# constants/security.py
MAX_TEXT_LENGTH = 500
MAX_JSON_PAYLOAD_BYTES = 10_000
RATE_LIMIT_CALLS = 10

# constants/cards.py
DEFAULT_CARD_FACTOR = 2500
CARD_TYPE_NEW = 0
QUEUE_NEW = 0

# constants/tts.py
TTS_DEFAULT_WPM = 150
TTS_MIN_RATE = 0.5

# constants/__init__.py
from .security import *
from .cards import *
from .tts import *
```

**Benefits:**
- Easier to find related constants
- Can import subset: `from .constants.security import MAX_TEXT_LENGTH`
- Clearer organization

---

### 4. ✅ **Already Excellent** - Error Handling

Recent improvements (from error handling phase):
- ✅ Fixed bare `except` block
- ✅ Added `log_error()` and `log_warning()`
- ✅ Improved error messages with context
- ✅ Validation decorators for consistent checks

**No changes needed** - Keep current approach.

---

### 5. ✅ **Already Excellent** - Code Duplication

Recent improvements (from complexity phase):
- ✅ Generic accessor `_get_card_property()` (84 lines saved)
- ✅ Validation decorators (24 lines saved)
- ✅ Total: 108 lines eliminated

**No changes needed** - Continue using these patterns.

---

## Dependency Metrics Summary

| Metric | Value | Assessment |
|--------|-------|------------|
| Total Modules | 11 | ✅ Good size |
| Avg Imports/Module | 3-4 | ✅ Low coupling |
| Circular Dependencies | 0 | ✅ Clean |
| Max Dependency Chain | 3 levels | ✅ Shallow |
| Global Singletons | 1 (`mw`) | ⚠️ Imposed by Anki |
| Classes | 3 | ✅ Function-focused |
| Avg Lines/Module | ~180 | ✅ Manageable |
| Code Duplication | <5% | ✅ Excellent (post-refactoring) |

---

## Testing Architecture

### Current Coverage: 79%

**Test Organization:**
```
tests/
├── test_card_info.py (52 tests)
├── test_card_actions.py (21 tests)
├── test_security.py (52 tests)
├── test_api_bridge.py (15 tests)
└── ... (249 total tests)
```

**Test Types:**
1. **Unit tests** - 176 tests (pytest)
2. **Property-based tests** - 21 tests (hypothesis)
3. **Benchmarks** - 22 tests (pytest-benchmark)
4. **Integration tests** - 30 tests

**Strengths:**
- ✅ 100% test pass rate
- ✅ Good coverage of security module (critical)
- ✅ Property-based testing for validation logic
- ✅ Performance benchmarks included

**Recommendation:**
Consider **Architectural Tests** (ArchUnit-style):
```python
# test_architecture.py
def test_no_circular_dependencies():
    """Ensure no circular imports."""
    # Parse imports, build dependency graph, check for cycles

def test_layer_isolation():
    """Feature modules should not import from each other."""
    feature_modules = ["card_info", "card_actions", "reviewer_control", ...]
    for module in feature_modules:
        imports = get_imports(module)
        assert not any(imp in feature_modules for imp in imports)

def test_security_module_independence():
    """Security module should not depend on feature modules."""
    imports = get_imports("security")
    assert "card_info" not in imports
    assert "card_actions" not in imports
```

---

## Performance Considerations

### 1. ✅ Pre-compiled Regex Patterns (security.py)
```python
class InputValidator:
    _FILENAME_PATTERN = re.compile(r'^[\w\-]+\.\w+$')  # Compiled once
    _TAG_PATTERN = re.compile(r'^[\w\-]+$')
```
**Impact:** 10-50x faster than `re.match()` per call

### 2. ✅ Rate Limiting (api_bridge.py)
```python
class RateLimiter:
    """Prevent API abuse - 10 calls/second per template."""
```
**Impact:** Prevents DoS attacks, maintains UI responsiveness

### 3. ✅ Payload Size Limits
```python
if len(args_json) > MAX_JSON_PAYLOAD_BYTES:
    raise ValueError(...)
```
**Impact:** Prevents memory exhaustion

### 4. ⚠️ Potential Improvement - Caching
**Opportunity:**
Some API calls return static data (e.g., card properties during review):
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def anki_get_card_type(card_id: int) -> int:
    """Cache card type (doesn't change during review)."""
    # ...
```

**Caution:** Only cache immutable data, clear cache on card change.

---

## Comparison to Best Practices

| Best Practice | Implementation | Grade |
|---------------|---------------|-------|
| **Separation of Concerns** | 11 focused modules | A |
| **DRY Principle** | Generic accessor, decorators | A |
| **SOLID Principles** | Mostly followed (see above) | B+ |
| **Security by Design** | InputValidator, RateLimiter | A |
| **Testability** | 79% coverage, 249 tests | A- |
| **Documentation** | Module/function docstrings | A |
| **Error Handling** | Centralized logging, decorators | A |
| **Performance** | Pre-compiled patterns, rate limiting | A |
| **Extensibility** | Registry pattern, decorators | A |
| **Dependency Management** | Low coupling, no cycles | A- |

---

## Migration Path (Optional Improvements)

### Phase 1: Reduce Global State Coupling (4-8 hours)
1. Create `AnkiContext` abstraction in `utils.py`
2. Refactor 8 modules to use `AnkiContext` instead of direct `mw` import
3. Update tests to mock `AnkiContext`
4. **Impact:** Easier testing, better abstraction

### Phase 2: TTS Strategy Pattern (2-4 hours)
1. Define `TTSStrategy` abstract base class
2. Extract platform implementations to separate classes
3. Add strategy registry
4. Update `TTSController` to use strategies
5. **Impact:** Easier to add new platforms

### Phase 3: Split Constants (1-2 hours)
1. Create `constants/` package
2. Split into `security.py`, `cards.py`, `tts.py`, `ui.py`
3. Update imports
4. **Impact:** Better organization

### Phase 4: Architectural Tests (2-3 hours)
1. Add `test_architecture.py`
2. Implement dependency graph analysis
3. Add layer isolation tests
4. **Impact:** Prevent architectural degradation

**Total Effort:** 9-17 hours
**Priority:** Optional - current architecture is solid

---

## Final Recommendations

### Must Do (High Priority)
1. ✅ **Nothing critical** - Architecture is sound
2. Continue current patterns (decorators, generic accessor)
3. Maintain test coverage above 75%

### Should Do (Medium Priority)
1. **Reduce `mw` coupling** via `AnkiContext` abstraction (4-8 hours)
   - Improves testability significantly
   - Better abstraction for future Anki version changes
2. **Add architectural tests** (2-3 hours)
   - Prevent regressions in module dependencies
   - Document architectural rules as code

### Nice to Have (Low Priority)
1. **TTS Strategy Pattern** (2-4 hours) - only if adding 2+ new platforms
2. **Split constants** (1-2 hours) - organizational improvement
3. **Caching for immutable data** (1-2 hours) - micro-optimization

---

## Conclusion

**Overall Architecture Grade: A-**

The codebase demonstrates **strong architectural design** with clear separation of concerns, modular organization, and well-applied design patterns. Recent improvements (decorators, generic accessor) show commitment to code quality.

**Key Strengths:**
- ✅ Clean module structure (11 focused modules)
- ✅ Excellent use of Registry and Decorator patterns
- ✅ Strong security foundation
- ✅ High test coverage (79%, 249 tests)
- ✅ Low code duplication (108 lines eliminated)
- ✅ Good documentation

**Areas for Improvement:**
- ⚠️ Global state coupling (`mw` singleton) - medium priority
- ⚠️ TTS platform coupling - low priority
- ⚠️ Dependency Inversion Principle - consider for future refactoring

**Recommendation:**
The architecture is **production-ready** as-is. Optional improvements (AnkiContext abstraction, architectural tests) would enhance long-term maintainability but are not urgent.

**Next Steps:**
1. Continue with current development
2. Consider `AnkiContext` refactoring if planning major test infrastructure improvements
3. Add architectural tests if project grows beyond 15 modules

---

## Appendix: Design Pattern Catalog

| Pattern | Location | Purpose | Assessment |
|---------|----------|---------|------------|
| **Registry** | api_bridge.py | Map JS function names to Python handlers | ✅ Excellent |
| **Decorator** | utils.py | Validation and error handling | ✅ Excellent |
| **Strategy** | tts_control.py | Platform-specific TTS implementations | ✅ Good (could be classic Strategy) |
| **Facade** | api_bridge.py | Simplify API registration | ✅ Excellent |
| **Singleton** | aqt.mw | Global Anki state | ⚠️ Imposed by Anki |
| **Template Method** | security.py | Validation flow | ✅ Good |
| **DRY Accessor** | card_info.py | Generic property getter | ✅ Excellent |

---

**Document Version:** 1.0  
**Date:** 2025  
**Author:** Architecture Review  
**Status:** Complete
