# Maintainability Guide

## Overview

This guide helps developers understand, maintain, and extend the AnkiDroid JS API codebase effectively.

## Quick Reference

| Aspect | Location | Update Frequency |
|--------|----------|------------------|
| API Version | `__init__.py` (`__api_version__`) | When AnkiDroidJS updates |
| Add-on Version | `__init__.py`, `manifest.json`, `setup.py` | Each release |
| Constants | `constants.py` | When adding features |
| Tests | `tests/test_*.py` | With every change |
| Documentation | `README.md`, `docs/` | With API changes |

---

## Code Organization

### Module Structure
```
src/ankidroid_js_api/
├── __init__.py          # Entry point, initialization, menu setup
├── api_bridge.py        # Core API routing and JavaScript injection
├── constants.py         # All magic numbers and configuration values
├── security.py          # Input validation, rate limiting, sanitization
├── utils.py             # Helper functions (config, logging, file I/O)
│
├── card_info.py         # Read card/deck statistics
├── card_actions.py      # Modify cards (mark, flag, bury, suspend)
├── reviewer_control.py  # Control reviewer (show answer, ease buttons)
├── tts_control.py       # Text-to-speech functionality
├── ui_control.py        # UI state (night mode, toasts, scrollbars)
├── tag_manager.py       # Tag operations
│
├── js/
│   └── ankidroid-api.js # JavaScript API injected into cards
├── test_templates/      # HTML templates for testing
└── config.json          # Default configuration
```

### Dependency Flow
```
┌─────────────┐
│ __init__.py │ ← Entry point
└──────┬──────┘
       │
       ├─→ api_bridge.py ─→ All feature modules
       │                    (card_info, card_actions, etc.)
       │
       ├─→ security.py   ─→ Used by all modules for validation
       │
       └─→ utils.py      ─→ Used by all modules for helpers
```

---

## Adding New API Functions

### Step-by-Step Process

1. **Choose the Right Module**
   - Card metadata? → `card_info.py`
   - Card modification? → `card_actions.py`
   - Reviewer control? → `reviewer_control.py`
   - New category? Create new module

2. **Implement the Function**
```python
# Example in card_actions.py
from .utils import log_api_call
from .security import InputValidator
from .constants import YOUR_CONSTANT

def anki_your_new_function(param: str) -> bool:
    """Short description.
    
    Detailed description explaining:
    - What it does
    - When to use it
    - Side effects
    
    Args:
        param: Description of parameter
        
    Returns:
        bool: True if successful, False otherwise
        
    Example:
        In JavaScript:
        >>> const result = await api.ankiYourNewFunction("value");
    """
    log_api_call("ankiYourNewFunction", {"param": param})
    
    # Validate input
    param = InputValidator.validate_text(param, max_length=YOUR_CONSTANT)
    
    # Check prerequisites
    card = get_current_card()
    if not card or not mw:
        return False
    
    try:
        # Implementation
        # ... your code ...
        return True
    except Exception as e:
        log_debug(f"Error in ankiYourNewFunction: {str(e)}")
        return False
```

3. **Register in api_bridge.py**
```python
# In setup_api_bridge()
from . import your_module

register_api_function("ankiYourNewFunction", your_module.anki_your_new_function)
```

4. **Add Tests**
```python
# In tests/test_your_module.py
def test_your_new_function(mock_mw, mock_card):
    """Test your new function."""
    result = your_module.anki_your_new_function("test")
    assert result == True
    # Add more assertions
```

5. **Update Documentation**
   - Add to `README.md` API list
   - Add example to test templates
   - Update `CHANGELOG.md`

---

## Common Patterns

### 1. Guard Clauses for Card Availability
```python
def anki_some_function() -> bool:
    card = get_current_card()
    if not card or not mw:
        return False
    # Continue with implementation
```

**Why:** Desktop Anki might not have an active reviewer.

### 2. Input Validation
```python
from .security import InputValidator

# For text
text = InputValidator.validate_text(text, max_length=MAX_TEXT_LENGTH)

# For integers
days = InputValidator.validate_integer(days, min_val=-365, max_val=3650)

# For floats
rate = InputValidator.validate_float(rate, min_val=0.5, max_val=2.0)
```

**Why:** Prevents injection attacks and invalid data.

### 3. Logging
```python
from .utils import log_api_call, log_debug

# Log API calls (configurable)
log_api_call("functionName", {"arg": value})

# Log debug info (only in debug mode)
log_debug("Detailed debug information")
```

**Why:** Helps troubleshooting without verbose production logs.

### 4. Error Handling
```python
try:
    # Operation
    result = some_operation()
    return True
except Exception as e:
    log_debug(f"Operation failed: {str(e)}")
    return False  # Never expose error details to JavaScript
```

**Why:** Security (don't leak internal details), reliability (graceful degradation).

---

## Code Quality Checklist

Before submitting changes:

- [ ] **Type Hints:** All function parameters and returns have type hints
- [ ] **Docstrings:** Function has docstring with Args, Returns, Example
- [ ] **Input Validation:** User input is validated using `InputValidator`
- [ ] **Constants:** No magic numbers (use `constants.py`)
- [ ] **Tests:** New code has corresponding tests (aim for 100% coverage)
- [ ] **Error Handling:** Exceptions caught and logged, not exposed
- [ ] **Logging:** Use `log_api_call` and `log_debug` appropriately
- [ ] **Return Values:** Consistent (bool for success, specific types for data)
- [ ] **Side Effects:** Documented in docstring
- [ ] **Thread Safety:** All code runs on main thread (Anki's requirement)

---

## Testing Strategy

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test File
```bash
pytest tests/test_card_actions.py -v
```

### Run with Coverage
```bash
pytest tests/ --cov=src/ankidroid_js_api --cov-report=html
```

### Test Categories
1. **Unit Tests** (`test_*.py`) - Test individual functions
2. **Integration Tests** (`test_integration.py`) - Test workflow combinations
3. **Manual Tests** - Use test deck (Tools → Create API Test Deck, available when `debug_mode: true`)

---

## Dependency Management

### Current Dependencies

**Runtime (included with Anki):**
- Python 3.9+
- PyQt6 (via Anki)
- Anki 2.1.50+

**Development Only:**
- pytest, pytest-cov, pytest-mock
- black, mypy, pylint, flake8

### Upgrading Anki Compatibility

When a new Anki version is released:

1. **Check Breaking Changes**
   - Review Anki changelog
   - Check for deprecated APIs

2. **Update Minimum Version**
```python
# In __init__.py
__min_anki_version__ = "2.1.XX"
```

3. **Test Thoroughly**
   - Run full test suite
   - Manual testing with test deck
   - Check private API usage (e.g., `_showAnswer`, `_answerCard`)

4. **Update Documentation**
   - README.md compatibility section
   - CHANGELOG.md

---

## Configuration Management

### Default Configuration
Location: `src/ankidroid_js_api/config.json`

**Production Settings:**
```json
{
    "debug_mode": false,
    "log_api_calls": false
}
```

**Development Settings:**
```json
{
    "debug_mode": true,
    "log_api_calls": true
}
```

### Reading Configuration
```python
from .utils import get_config

config = get_config()
enabled = config.get("tts", {}).get("enabled", True)
```

### Modifying Configuration
```python
from .utils import save_config

config = get_config()
config["debug_mode"] = True
save_config(config)
```

---

## Performance Considerations

### Optimizations Already Implemented
1. **Pre-compiled Regex** (`security.py`) - Avoid recompilation overhead
2. **JavaScript File Caching** (`utils.py`) - Reduce disk I/O
3. **Rate Limiter Cleanup** (`security.py`) - Prevent memory leak
4. **Lazy Initialization** - Only load when needed

### Performance Best Practices
- Avoid blocking operations in API functions
- Use rate limiting for expensive operations
- Cache expensive computations when appropriate
- Profile before optimizing (use `pytest --profile`)

---

## Security Best Practices

### Input Validation (ALWAYS)
```python
# BAD - No validation
def bad_function(text: str):
    os.system(text)  # Command injection!

# GOOD - Validated
def good_function(text: str):
    text = InputValidator.validate_text(text)
    # Safe to use
```

### Rate Limiting (For Expensive Operations)
```python
if not RateLimiter.check(template_id, "expensiveOp", max_per_second=1):
    return {"success": False, "error": "Rate limit exceeded"}
```

### PII Sanitization (In Logs)
```python
from .security import sanitize_for_logging

log_debug(sanitize_for_logging(user_data))
```

---

## Troubleshooting Guide

### Common Issues

**1. API functions not responding**
- Check JavaScript console (F12) for errors
- Enable `debug_mode` in config
- Check `stderr.txt` in add-on directory

**2. Tests failing after changes**
- Run tests individually to isolate issue
- Check for missing imports
- Verify mock setup in `conftest.py`

**3. Anki crashes on startup**
- Check syntax errors in Python files
- Verify imports are correct
- Review `init_addon()` for exceptions

**4. Rate limiting too aggressive**
- Adjust `DEFAULT_API_RATE_LIMIT_PER_SECOND` in `constants.py`
- Consider per-function limits

### Debug Workflow
1. Enable debug mode in config
2. Restart Anki
3. Check console output
4. Review `stderr.txt` and `stdout.txt` in add-on folder
5. Use test deck to isolate issue

---

## Release Process

### Version Numbering
Follow [Semantic Versioning](https://semver.org/):
- MAJOR.MINOR.PATCH (e.g., 1.2.3)
- MAJOR: Breaking API changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

### Release Checklist
1. [ ] Update version in:
   - `__init__.py` (`__version__`)
   - `manifest.json` (`human_version`)
   - `setup.py` (`version`)
2. [ ] Update `CHANGELOG.md` with release notes
3. [ ] Run full test suite: `pytest tests/ -v`
4. [ ] Build add-on: `python setup.py build_addon`
5. [ ] Test .ankiaddon installation manually
6. [ ] Create git tag: `git tag v1.2.3`
7. [ ] Push to GitHub: `git push && git push --tags`
8. [ ] Create GitHub release with .ankiaddon file
9. [ ] (Future) Submit to AnkiWeb

---

## Long-Term Sustainability

### Technical Debt Tracking
Current known issues (see `docs/CODE_REVIEW_BEST_PRACTICES.md`):
- Split `api_bridge.py` into smaller modules
- Implement dependency injection for testability
- Add Result type for consistent error handling
- Create facade layer for Anki internals

### Migration Path
When Anki updates break compatibility:
1. Create compatibility layer in `utils.py`
2. Use feature detection instead of version checks
3. Maintain backward compatibility for one version
4. Document migration in CHANGELOG

### Documentation Maintenance
- Update README.md when API changes
- Keep examples in `test_templates/` current
- Review docs/ quarterly for accuracy
- Add new troubleshooting entries as issues arise

---

## Getting Help

- **Issues:** Check existing GitHub issues
- **Questions:** Open a discussion on GitHub
- **Contributing:** See CONTRIBUTING.md (to be created)
- **Testing:** See `docs/TESTING.md`

---

## Key Takeaways

1. **Use existing patterns** - Follow the structure in similar modules
2. **Validate everything** - Never trust user input
3. **Test thoroughly** - Unit tests + integration tests + manual tests
4. **Document clearly** - Future you will thank you
5. **Keep it simple** - YAGNI (You Aren't Gonna Need It)
6. **Security first** - Input validation, rate limiting, PII sanitization
7. **Performance second** - Profile before optimizing

---

*Last updated: December 26, 2025*
*Review this guide quarterly and update as the codebase evolves.*
