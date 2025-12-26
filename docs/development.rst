.. _development:

Development Guide
=================

This guide covers development setup, testing, and building the AnkiDroid JS API for Desktop add-on.

Prerequisites
-------------

- Python 3.9 or higher
- Git
- Anki Desktop 2.1.50+
- Text editor or IDE (VS Code recommended)

Initial Setup
-------------

1. Clone the Repository
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git clone https://github.com/gallaway-jp/AnkiJSApi.git
   cd AnkiJSApi

2. Create Virtual Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Create virtual environment
   python -m venv venv

   # Activate it
   # Windows:
   venv\Scripts\activate

   # macOS/Linux:
   source venv/bin/activate

3. Install Development Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install -r requirements-dev.txt

4. Link Add-on for Development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a symbolic link so changes are immediately reflected in Anki:

**Windows (PowerShell as Administrator):**

.. code-block:: powershell

   $source = "$PWD\src\ankidroid_js_api"
   $target = "$env:APPDATA\Anki2\addons21\ankidroid_js_api"
   New-Item -ItemType SymbolicLink -Path $target -Target $source

**macOS:**

.. code-block:: bash

   ln -s "$(pwd)/src/ankidroid_js_api" \
       "$HOME/Library/Application Support/Anki2/addons21/ankidroid_js_api"

**Linux:**

.. code-block:: bash

   ln -s "$(pwd)/src/ankidroid_js_api" \
       "$HOME/.local/share/Anki2/addons21/ankidroid_js_api"

5. Restart Anki
~~~~~~~~~~~~~~~

Close and reopen Anki to load the add-on.

Development Workflow
--------------------

Making Changes
~~~~~~~~~~~~~~

1. **Edit Python files** in ``src/ankidroid_js_api/``
2. **Edit JavaScript** in ``src/ankidroid_js_api/js/ankidroid-api.js``
3. **Restart Anki** to reload the add-on
4. **Test your changes** in card templates

Debugging
~~~~~~~~~

Enable Debug Mode
^^^^^^^^^^^^^^^^^

Edit add-on configuration (Tools → Add-ons → Config):

.. code-block:: json

   {
       "debug_mode": true,
       "log_api_calls": true
   }

View Debug Output
^^^^^^^^^^^^^^^^^

1. **Console Output**: Tools → Debug Console
2. **Add-on Errors**: Tools → Add-ons → View Add-on Errors
3. **Python Logs**: Check terminal if running Anki from command line

Debug Tips
^^^^^^^^^^

Python debugging:

.. code-block:: python

   # Add debug prints in Python code
   from .utils import log_debug
   log_debug("My debug message")

   # Or use standard print
   print("Debug:", some_variable)

JavaScript debugging:

.. code-block:: javascript

   // Add console logs in JavaScript
   console.log("Debug:", someVariable);
   console.error("Error occurred:", error);

Code Quality
~~~~~~~~~~~~

Format Code with Black
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   black src/

Run Linter
^^^^^^^^^^

.. code-block:: bash

   # PyLint
   pylint src/ankidroid_js_api/

   # Flake8
   flake8 src/

Type Checking
^^^^^^^^^^^^^

.. code-block:: bash

   mypy src/ankidroid_js_api/

Testing
-------

Run All Tests
~~~~~~~~~~~~~

.. code-block:: bash

   pytest tests/

Run with Coverage
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pytest --cov=src/ankidroid_js_api --cov-report=html tests/

Then open ``htmlcov/index.html`` to view coverage report.

Run Specific Test
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Run specific test file
   pytest tests/test_card_info.py

   # Run specific test function
   pytest tests/test_card_info.py::test_get_card_id

   # Run tests matching pattern
   pytest -k "test_card"

Project Structure
-----------------

.. code-block:: text

   ankidroid-js-api-desktop/
   ├── src/
   │   └── ankidroid_js_api/
   │       ├── __init__.py          # Add-on entry point
   │       ├── api_bridge.py        # API function registry
   │       ├── card_actions.py      # Card manipulation functions
   │       ├── card_info.py         # Card information functions
   │       ├── config.py            # Configuration management
   │       ├── fullscreen_handler.py # Fullscreen control
   │       ├── reviewer_control.py  # Reviewer state management
   │       ├── search.py            # Card search functions
   │       ├── security.py          # Security validation
   │       ├── tag_manager.py       # Tag operations
   │       ├── tts_control.py       # Text-to-speech
   │       ├── ui_control.py        # UI features
   │       └── utils.py             # Utility functions
   │       └── js/
   │           └── ankidroid-api.js # JavaScript API
   ├── tests/                       # Unit tests
   │   ├── conftest.py             # Test fixtures
   │   ├── test_card_info.py
   │   ├── test_card_actions.py
   │   └── ...
   ├── docs/                        # Documentation
   ├── requirements-dev.txt         # Development dependencies
   └── README.md

Adding New API Functions
-------------------------

See :ref:`contributing` for detailed instructions on adding new API functions.

Building and Packaging
-----------------------

Create Distribution Package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Create .ankiaddon package
   python build.py

   # Or manually create a zip:
   cd src
   zip -r ../ankidroid_js_api.ankiaddon ankidroid_js_api/

Test the Package
~~~~~~~~~~~~~~~~

1. Install the .ankiaddon file in Anki
2. Restart Anki
3. Test all functionality
4. Check for errors in debug console

Release Process
~~~~~~~~~~~~~~~

1. Update version number in ``__init__.py``
2. Update ``CHANGELOG.md`` with new version
3. Create git tag:

   .. code-block:: bash

      git tag -a v1.0.0 -m "Release version 1.0.0"
      git push origin v1.0.0

4. Build package and upload to AnkiWeb

Best Practices
--------------

Code Style
~~~~~~~~~~

- Follow PEP 8 for Python code
- Use type hints for function parameters and return values
- Write docstrings for all public functions
- Keep functions focused and single-purpose
- Use descriptive variable names

Error Handling
~~~~~~~~~~~~~~

.. code-block:: python

   def anki_some_function() -> Optional[int]:
       """Function that might fail gracefully."""
       try:
           card = get_current_card()
           if not card:
               log_error("No card available")
               return None
           return card.id
       except Exception as e:
           log_error(f"Error in anki_some_function: {e}")
           return None

Logging
~~~~~~~

.. code-block:: python

   from .utils import log_api_call, log_error, log_debug

   def anki_my_function(param: str) -> bool:
       """Always log API calls for debugging."""
       log_api_call("ankiMyFunction", {"param": param})
       
       if not validate_input(param):
           log_error(f"Invalid parameter: {param}")
           return False
       
       log_debug(f"Processing: {param}")
       # ... implementation
       return True

Testing Guidelines
~~~~~~~~~~~~~~~~~~

- Write tests for all new functions
- Test both success and failure cases
- Use mocks for Anki objects
- Aim for >80% code coverage
- Run tests before committing

Documentation
~~~~~~~~~~~~~

- Update README.md for major features
- Add examples to EXAMPLES.md
- Update API reference
- Add FAQ entries for common questions
- Keep CHANGELOG.md up to date

Next Steps
----------

- Read :ref:`contributing` for contribution guidelines
- Review :ref:`testing` for detailed testing information
- Check :ref:`architecture` to understand the codebase structure
