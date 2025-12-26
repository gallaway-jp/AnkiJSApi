# Testing Guide

This document explains all the tests in the AnkiDroid JS API project and how to run them.

## Test Overview

The project includes comprehensive test coverage across multiple categories:

### 1. Unit Tests (117 tests)
Unit tests for all Python modules using pytest and mocking.

### 2. Add-on Package Integration Tests (30 tests)
Integration tests validating package structure, API completeness, and configuration.

### 3. Anki Integration Tests (10 test stubs)
Integration tests that would run against actual Anki (currently skipped).

### 4. JavaScript Tests (HTML-based)
Browser-based tests for the JavaScript API client.

---

## Running the Tests

### All Unit Tests

Run all unit tests (excludes integration tests):

```bash
pytest tests/ -v
```

### Specific Test Files

Run tests for a specific module:

```bash
# Test TTS functionality
pytest tests/test_tts_control.py -v

# Test API bridge
pytest tests/test_api_bridge.py -v

# Test card information functions
pytest tests/test_card_info.py -v

# Test card actions
pytest tests/test_card_actions.py -v

# Test reviewer controls
pytest tests/test_reviewer_control.py -v

# Test UI controls
pytest tests/test_ui_control.py -v

# Test tag management
pytest tests/test_tag_manager.py -v

# Test utilities
pytest tests/test_utils.py -v
```

### With Coverage Report

To generate a coverage report (requires pytest-cov):

```bash
pip install pytest-cov
pytest tests/ --cov=src/ankidroid_js_api --cov-report=html
```

View the report by opening `htmlcov/index.html` in a browser.

---

## Test Categories

### 1. TTS Control Tests (`test_tts_control.py`)

**28 tests** covering text-to-speech functionality:

- **TTSController Class Tests:**
  - Initialization and configuration
  - Language, pitch, and rate settings
  - Parameter clamping (0.5-2.0 range)
  - Process management (speaking, stopping)
  - Platform-specific speech synthesis (Windows/macOS/Linux)
  - Queue modes (FLUSH vs ADD)
  - Error handling

- **Module Function Tests:**
  - All public TTS API functions
  - Field modifier availability

**Key Features Tested:**
- Cross-platform TTS (PowerShell/say/espeak/festival)
- Subprocess management
- Configuration handling
- Queue mode behavior

---

### 2. API Bridge Tests (`test_api_bridge.py`)

**23 tests** covering JavaScript-Python bridge:

- **API Registry:**
  - Function registration
  - Callable verification

- **Pycmd Handler:**
  - Command parsing
  - Argument handling
  - Error responses
  - Unknown function handling

- **JavaScript Injection:**
  - HTML parsing (with/without `<head>`)
  - Script insertion
  - File reading

- **Setup and Integration:**
  - API function registration (60+ functions)
  - GUI hooks registration
  - Link handler wrapping

- **Function Coverage Verification:**
  - Card info functions (22)
  - Card action functions (9)
  - Reviewer control functions (6)
  - TTS functions (7)
  - UI control functions (8)
  - Tag management functions (3)
  - Utility functions (1)

**Key Features Tested:**
- Complete API surface verification
- Bridge communication protocol
- Error handling and edge cases

---

### 3. Card Info Tests (`test_card_info.py`)

**9 tests** covering card information retrieval:

- New/learning/review card counts
- Card statistics (reps, marks, ETA)
- Card metadata (ID, deck name)
- Error handling (no current card)

---

### 4. Card Actions Tests (`test_card_actions.py`)

**13 tests** covering card manipulation:

- Mark/unmark cards
- Flag operations (all colors)
- Bury card/note
- Suspend card/note
- Reset progress
- Search and navigate
- Set due date (with clamping)

---

### 5. Reviewer Control Tests (`test_reviewer_control.py`)

**11 tests** covering reviewer state and control:

- Answer display detection
- Show answer functionality
- Answer ease buttons (1-4)
- Error handling (invalid ease, no card)

---

### 6. UI Control Tests (`test_ui_control.py`)

**13 tests** covering UI state and notifications:

- Fullscreen detection
- Night mode detection
- Scrollbar controls
- Navigation drawer
- Options menu
- Toast notifications

---

### 7. Tag Manager Tests (`test_tag_manager.py`)

**4 tests** covering tag operations:

- Get note tags
- Set note tags
- Tag normalization (spaces)
- Error handling

---

### 8. Utilities Tests (`test_utils.py`)

**16 tests** covering utility functions:

- Configuration (get/save)
- Logging (debug, API calls)
- Path management
- File I/O (JavaScript files)

---

## Add-on Package Integration Tests

### Overview

Package integration tests (`test_addon_package.py`) validate the complete add-on structure without requiring Anki installation.

**Status:** All 30 tests passing ✅

### Test Categories:

1. **Package Structure (10 tests)**
   - Manifest validation
   - Configuration files
   - Module existence and importability
   - JavaScript syntax validation

2. **Add-on Initialization (4 tests)**
   - Init function availability
   - API bridge setup
   - Function registration (60+ functions)
   - Callable verification

3. **Configuration (3 tests)**
   - Required sections present
   - Debug config structure
   - TTS config structure

4. **Documentation (5 tests)**
   - README existence
   - License file
   - Contributing guide
   - API reference
   - Installation guide

5. **JavaScript API (3 tests)**
   - AnkiDroidJS object definition
   - Platform variable setting
   - All API methods defined

6. **Build System (3 tests)**
   - setup.py presence
   - pyproject.toml validity
   - Configuration structure

7. **Anki Compatibility (2 tests)**
   - Version documentation
   - Manifest conflicts field

### Running Package Integration Tests

```bash
pytest tests/test_addon_package.py -v
```

### What These Tests Validate

✅ **Package Integrity:** All required files present and valid  
✅ **API Completeness:** All 60+ functions registered  
✅ **Configuration:** Valid JSON and proper structure  
✅ **Documentation:** Complete and accessible  
✅ **Build System:** Ready for packaging  
✅ **Module Integration:** All components work together  

---

## Anki Integration Tests

### Overview

Integration tests (`test_integration.py`) provide a framework for testing against actual Anki.

**Status:** Currently all skipped (require Anki installation)

### Test Categories:

1. **Anki Integration (6 tests)**
   - Add-on loading
   - JavaScript injection in reviewer
   - Pycmd bridge communication
   - End-to-end API functions
   - TTS functionality
   - Configuration changes

2. **Card Template Integration (2 tests)**
   - Complex template testing
   - Error handling

3. **Performance Integration (2 tests)**
   - API call performance
   - JavaScript injection overhead

### Running Integration Tests

To run integration tests when Anki is installed:

```bash
pytest tests/test_integration.py -v -m integration
```

### Setting Up Integration Tests

To implement these tests:

1. Install Anki Desktop
2. Set up a test profile
3. Install pytest-anki or create custom fixtures
4. Update test marks in `pytest.ini`

---

## JavaScript Tests

### Overview

Browser-based tests for the JavaScript client library.

**File:** `tests/test_javascript_api.html`

### Running JavaScript Tests

1. Open `tests/test_javascript_api.html` in a web browser
2. Click "Run All Tests"
3. View results on the page

### What's Tested (17 tests)

- API initialization
- Card information APIs
- Card action APIs
- Reviewer control APIs
- UI control APIs
- Tag management APIs
- Promise-based async behavior
- Error handling
- Platform detection
- Deprecated API warnings

### Features

- **Mock Backend:** Uses mock `pycmd` function to simulate Python responses
- **Visual Results:** Color-coded pass/fail display
- **No Dependencies:** Runs entirely in the browser

---

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install pytest
    
    - name: Run tests
      run: pytest tests/ -v
```

---

## Test Statistics

### Current Coverage

- **Total Tests:** 157 (147 passing, 10 skipped)
- **Execution Time:** ~0.33 seconds
- **Test Files:** 10
- **Lines of Test Code:** ~2500+

### Module Coverage

| Module | Tests | Coverage |
|--------|-------|----------|
| Package Integration | 30 | ✅ Complete structure validation |
| api_bridge.py | 23 | ✅ Complete API surface |
| tts_control.py | 28 | ✅ All platforms & modes |
| card_info.py | 9 | ✅ All info functions |
| card_actions.py | 13 | ✅ All actions |
| reviewer_control.py | 11 | ✅ All controls |
| ui_control.py | 16 | ✅ All UI functions |
| tag_manager.py | 4 | ✅ Complete |
| utils.py | 13 | ✅ All utilities |
| Anki Integration | 10 | ⏭️ Skipped (framework ready) |

---

## Writing New Tests

### Unit Test Template

```python
import sys
from unittest.mock import Mock, patch
import pytest

# Mock Anki modules BEFORE importing our code
sys.modules['aqt'] = MagicMock()
sys.modules['anki'] = MagicMock()

from ankidroid_js_api import your_module

def test_your_function():
    """Test description."""
    # Setup
    mock_obj = Mock()
    
    # Execute
    result = your_module.your_function(mock_obj)
    
    # Assert
    assert result == expected_value
```

### Integration Test Template

```python
import pytest

@pytest.mark.integration
@pytest.mark.skip(reason="Requires Anki installation")
def test_with_actual_anki(anki_session):
    """Test description."""
    # Test with actual Anki instance
    pass
```

---

## Troubleshooting

### Common Issues

**Issue:** `ModuleNotFoundError: No module named 'aqt'`
- **Solution:** Tests should mock Anki modules before imports. Check that mocking is done at the top of the test file.

**Issue:** Tests pass individually but fail when run together
- **Solution:** Clear module-level state between tests or use fixtures.

**Issue:** Integration tests not running
- **Solution:** Integration tests are skipped by default. Install Anki and remove `@pytest.mark.skip` decorators.

---

## Best Practices

1. **Mock External Dependencies:** Always mock Anki modules in unit tests
2. **Test Edge Cases:** Include tests for error conditions and boundary values
3. **Use Descriptive Names:** Test names should clearly describe what they test
4. **Keep Tests Isolated:** Each test should be independent
5. **Test One Thing:** Each test should verify one specific behavior
6. **Use Fixtures:** Share common setup code via pytest fixtures

---

## Future Enhancements

Potential test improvements:

1. **Code Coverage:** Achieve 100% code coverage
2. **Integration Tests:** Implement full integration test suite with Anki
3. **Performance Tests:** Add benchmarks for API calls
4. **Stress Tests:** Test with large decks and many cards
5. **Browser Tests:** Automated JavaScript testing with Selenium/Puppeteer
6. **Property-Based Tests:** Use Hypothesis for property-based testing
7. **Mutation Testing:** Use mutmut to verify test quality

---

## Contributing

When adding new features:

1. Write tests first (TDD)
2. Ensure all tests pass
3. Add integration tests for complex features
4. Update this documentation

For questions, see [CONTRIBUTING.md](../CONTRIBUTING.md).
