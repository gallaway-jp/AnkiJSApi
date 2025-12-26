.. _testing:

Testing Guide
=============

This guide helps you understand the testing strategy, write effective tests, and maintain high test quality for the AnkiDroid JS API codebase.

**Current Test Coverage**: 258 tests across 12 test files

Test Organization
-----------------

Test Structure
~~~~~~~~~~~~~~

.. code-block:: text

   tests/
   ├── conftest.py                 # Shared fixtures and configuration
   ├── test_security.py           # Security validation and rate limiting
   ├── test_api_bridge.py         # Core API routing and JavaScript injection
   ├── test_card_info.py          # Card information retrieval
   ├── test_card_actions.py       # Card modification operations
   ├── test_reviewer_control.py   # Reviewer state and control
   ├── test_tts_control.py        # Text-to-speech functionality
   ├── test_ui_control.py         # UI state and notifications
   ├── test_tag_manager.py        # Tag operations
   ├── test_utils.py              # Helper functions
   ├── test_integration.py        # End-to-end workflow tests
   └── test_addon_package.py      # Package structure and metadata

Test Categories
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 30 30 20

   * - Category
     - Purpose
     - Test Files
     - Count
   * - Unit Tests
     - Test individual functions
     - test_*.py (except integration)
     - ~200
   * - Integration Tests
     - Test workflows and interactions
     - test_integration.py
     - ~10
   * - Package Tests
     - Test structure and configuration
     - test_addon_package.py
     - ~30
   * - Security Tests
     - Test validation and rate limiting
     - test_security.py
     - ~50+

Running Tests
-------------

All Tests
~~~~~~~~~

.. code-block:: bash

   pytest tests/ -v

Specific Test File
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pytest tests/test_security.py -v
   pytest tests/test_card_actions.py -v

Specific Test Function
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pytest tests/test_security.py::TestInputValidator::test_validate_text_success -v

Specific Test Class
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pytest tests/test_security.py::TestRateLimiter -v

With Coverage
~~~~~~~~~~~~~

.. code-block:: bash

   pip install pytest-cov
   pytest tests/ --cov=src/ankidroid_js_api --cov-report=html
   # Open htmlcov/index.html to view report

Fast Subset (unit tests only)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pytest tests/ -v -m "not integration"

Verbose Output
~~~~~~~~~~~~~~

.. code-block:: bash

   pytest tests/ -vv  # Extra verbose
   pytest tests/ -s   # Show print statements

Stop on First Failure
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pytest tests/ -x

Writing Tests
-------------

Test Naming Convention
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Good test names (descriptive, action-oriented)
   def test_validate_text_removes_null_bytes():
   def test_rate_limiter_blocks_after_limit_exceeded():
   def test_mark_card_adds_tag_when_unmarked():

   # Bad test names (vague)
   def test_validation():
   def test_limiter():
   def test_mark():

Test Structure (AAA Pattern)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def test_validate_text_removes_null_bytes():
       # Arrange - Set up test data
       input_text = "Hello\x00World"
       
       # Act - Execute the function
       result = InputValidator.validate_text(input_text)
       
       # Assert - Verify the outcome
       assert "\x00" not in result
       assert "HelloWorld" in result

Fixtures for Setup
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   @pytest.fixture
   def mock_card():
       """Create a mock card for testing."""
       card = Mock()
       card.id = 12345
       card.flags = 0
       # ... setup ...
       return card

   def test_mark_card_success(mock_card):
       """Test can use the fixture."""
       # mock_card is automatically passed
       assert mock_card.id == 12345

Parametrized Tests (DRY)
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   @pytest.mark.parametrize("color,expected_value", [
       ("red", 1),
       ("orange", 2),
       ("green", 3),
       ("blue", 4),
   ])
   def test_flag_color_mapping(color, expected_value):
       """Test flag color maps to correct value."""
       result = get_flag_value(color)
       assert result == expected_value

Testing Best Practices
-----------------------

1. Test One Thing Per Test
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Good - Tests one behavior
   def test_validate_text_removes_null_bytes():
       result = InputValidator.validate_text("Hello\x00World")
       assert "\x00" not in result

   # Bad - Tests multiple behaviors
   def test_validation():
       result1 = InputValidator.validate_text("Hello\x00World")
       assert "\x00" not in result1
       result2 = InputValidator.validate_integer("42", 0, 100)
       assert result2 == 42
       # Too much in one test

2. Test Edge Cases
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def test_validate_integer_boundary_conditions():
       """Test boundary values."""
       # Minimum boundary
       assert InputValidator.validate_integer(0, 0, 100) == 0
       
       # Maximum boundary
       assert InputValidator.validate_integer(100, 0, 100) == 100
       
       # Just below minimum (should fail)
       with pytest.raises(ValueError):
           InputValidator.validate_integer(-1, 0, 100)
       
       # Just above maximum (should fail)
       with pytest.raises(ValueError):
           InputValidator.validate_integer(101, 0, 100)

3. Test Error Conditions
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def test_validate_text_raises_on_invalid_type():
       """Test that invalid type raises TypeError."""
       with pytest.raises(TypeError, match="Expected string"):
           InputValidator.validate_text(12345)

4. Use Mocks Appropriately
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from unittest.mock import Mock, patch

   def test_get_card_id(mock_mw, mock_card):
       """Test card ID retrieval with mocked dependencies."""
       with patch('module.get_current_card', return_value=mock_card):
           result = anki_get_card_id()
           assert result == 12345

5. Test Happy Path and Sad Path
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Happy path - normal operation
   def test_mark_card_success(mock_card):
       """Test marking card successfully."""
       result = anki_mark_card(True)
       assert result is True

   # Sad path - error conditions
   def test_mark_card_no_card_available():
       """Test marking card when no card available."""
       with patch('module.get_current_card', return_value=None):
           result = anki_mark_card(True)
           assert result is False

Test Coverage Goals
-------------------

Coverage Targets
~~~~~~~~~~~~~~~~

- **Overall**: Aim for >80% line coverage
- **Critical modules**: security.py, api_bridge.py should be >90%
- **Feature modules**: >75% coverage each
- **Utilities**: >85% coverage

Measuring Coverage
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Generate HTML coverage report
   pytest --cov=src/ankidroid_js_api --cov-report=html tests/
   
   # View in browser
   open htmlcov/index.html  # macOS
   xdg-open htmlcov/index.html  # Linux
   start htmlcov/index.html  # Windows

Coverage Report Analysis
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Name                                 Stmts   Miss  Cover
   --------------------------------------------------------
   src/ankidroid_js_api/__init__.py        45      2    96%
   src/ankidroid_js_api/api_bridge.py      89      5    94%
   src/ankidroid_js_api/card_actions.py    67      8    88%
   src/ankidroid_js_api/card_info.py       52      3    94%
   src/ankidroid_js_api/security.py        98      4    96%
   --------------------------------------------------------
   TOTAL                                  800     45    94%

Common Testing Scenarios
------------------------

Testing API Functions
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def test_api_function_with_valid_input(mock_mw, mock_card):
       """Test API function with valid input."""
       with patch('module.get_current_card', return_value=mock_card):
           result = api_function("valid_input")
           assert result == expected_output

Testing Error Handling
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def test_api_function_handles_exception():
       """Test error handling."""
       with patch('module.some_operation', side_effect=Exception("Error")):
           result = api_function("input")
           assert result is None  # or default value

Testing Security Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def test_input_validator_rejects_malicious_input():
       """Test security validation."""
       malicious_input = "<script>alert('xss')</script>"
       result = InputValidator.validate_text(malicious_input)
       assert "<script>" not in result

Testing TTS Across Platforms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   @pytest.mark.parametrize("platform,expected_command", [
       ("Windows", "powershell"),
       ("Darwin", "say"),
       ("Linux", "espeak"),
   ])
   def test_tts_platform_specific(platform, expected_command):
       """Test TTS uses correct command per platform."""
       with patch('platform.system', return_value=platform):
           controller = TTSController()
           # Verify correct command is used

Continuous Integration
----------------------

GitHub Actions
~~~~~~~~~~~~~~

Example workflow:

.. code-block:: yaml

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
             pip install -r requirements-dev.txt
         - name: Run tests
           run: |
             pytest tests/ --cov=src/ankidroid_js_api
         - name: Upload coverage
           uses: codecov/codecov-action@v2

Troubleshooting Tests
----------------------

Tests Failing Locally
~~~~~~~~~~~~~~~~~~~~~

1. Check Python version (3.9+ required)
2. Reinstall dependencies: ``pip install -r requirements-dev.txt``
3. Clear pytest cache: ``pytest --cache-clear``
4. Run single test to isolate: ``pytest tests/test_file.py::test_name -v``

Mock Issues
~~~~~~~~~~~

If mocks aren't working:

- Verify patch path matches import path
- Use ``patch.object()`` for class methods
- Check mock is returned/applied before test runs

Import Errors
~~~~~~~~~~~~~

.. code-block:: bash

   # Add src to Python path
   export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
   pytest tests/

Next Steps
----------

- See :ref:`development` for development setup
- Check :ref:`contributing` for contribution guidelines
- Review :ref:`architecture` to understand code structure
