.. _contributing:

Contributing Guide
==================

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

Getting Started
---------------

1. Fork the repository
2. Clone your fork:

   .. code-block:: bash

      git clone https://github.com/yourusername/AnkiJSApi.git
      cd AnkiJSApi

3. Create a virtual environment and install dependencies:

   .. code-block:: bash

      python -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate
      pip install -r requirements-dev.txt

4. Create a symbolic link to test the add-on:

   **Windows:**

   .. code-block:: bash

      mklink /D "%APPDATA%\Anki2\addons21\ankidroid_js_api" "path\to\ankidroid-js-api-desktop\src\ankidroid_js_api"
   
   **macOS/Linux:**

   .. code-block:: bash

      ln -s "$(pwd)/src/ankidroid_js_api" "$HOME/.local/share/Anki2/addons21/ankidroid_js_api"

Development Workflow
--------------------

Code Style
~~~~~~~~~~

We follow PEP 8 for Python code. Use the provided tools:

.. code-block:: bash

   # Format code with black
   black src/

   # Check with pylint
   pylint src/ankidroid_js_api/

   # Type checking with mypy
   mypy src/ankidroid_js_api/

Running Tests
~~~~~~~~~~~~~

.. code-block:: bash

   # Run all tests
   python -m pytest tests/

   # Run with coverage
   python -m pytest --cov=src/ankidroid_js_api tests/

   # Run specific test file
   python -m pytest tests/test_card_info.py

Adding New Features
-------------------

1. Create a new branch
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git checkout -b feature/your-feature-name

2. Implement your feature
~~~~~~~~~~~~~~~~~~~~~~~~~

- Add Python implementation in appropriate module
- Update ``api_bridge.py`` to register new functions
- Add JavaScript wrapper in ``js/ankidroid-api.js``
- Write unit tests in ``tests/``
- Update documentation

3. Test your changes
~~~~~~~~~~~~~~~~~~~~

- Run unit tests
- Test manually in Anki Desktop
- Verify compatibility with existing card templates

4. Commit your changes
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git add .
   git commit -m "Add feature: description of feature"

5. Push and create a pull request
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git push origin feature/your-feature-name

API Implementation Guidelines
------------------------------

Adding a New API Function
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Python implementation
^^^^^^^^^^^^^^^^^^^^^^^^

Example in ``card_info.py``:

.. code-block:: python

   def anki_my_new_function(param1: str, param2: int) -> bool:
       """
       Brief description of what this function does.
       
       Args:
           param1: Description of parameter 1
           param2: Description of parameter 2
           
       Returns:
           True if successful, False otherwise
           
       Example:
           >>> anki_my_new_function("test", 42)
           True
       """
       log_api_call("ankiMyNewFunction", {"param1": param1, "param2": param2})
       
       try:
           # Implementation here
           return True
       except Exception as e:
           log_error(f"Error in ankiMyNewFunction: {e}")
           return False

2. Register in api_bridge.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from . import card_info
   
   # In setup_api_bridge function:
   register_api_function("ankiMyNewFunction", card_info.anki_my_new_function)

3. JavaScript wrapper
^^^^^^^^^^^^^^^^^^^^^

In ``js/ankidroid-api.js``:

.. code-block:: javascript

   ankiMyNewFunction: function(param1, param2) {
       return callPython('ankiMyNewFunction', { 
           param1: param1, 
           param2: param2 
       });
   },

4. Add tests
^^^^^^^^^^^^

In ``tests/test_module.py``:

.. code-block:: python

   def test_my_new_function(mock_mw):
       """Test the new function."""
       result = module.anki_my_new_function("test", 42)
       assert result is True
       
   def test_my_new_function_error_handling(mock_mw):
       """Test error handling."""
       result = module.anki_my_new_function("", -1)
       assert result is False

5. Update documentation
^^^^^^^^^^^^^^^^^^^^^^^

- Add to README.md if it's a major feature
- Add example usage to examples.rst
- Update CHANGELOG.md

Testing Guidelines
------------------

What to Test
~~~~~~~~~~~~

- Function returns correct values
- Function handles missing/invalid input gracefully
- Function works when no card is displayed
- Function works with different card states
- Error handling and edge cases

Mock Objects
~~~~~~~~~~~~

Use the provided fixtures in ``conftest.py``:

.. code-block:: python

   def test_my_function(mock_mw, mock_card):
       """Test with mocked Anki objects."""
       with patch('module.get_current_card', return_value=mock_card):
           result = module.anki_my_function()
           assert result == expected_value

Test Coverage
~~~~~~~~~~~~~

Aim for at least 80% test coverage:

.. code-block:: bash

   pytest --cov=src/ankidroid_js_api --cov-report=term-missing tests/

Documentation Standards
-----------------------

Docstring Format
~~~~~~~~~~~~~~~~

Use Google-style docstrings with Napoleon:

.. code-block:: python

   def my_function(param1: str, param2: int) -> Optional[str]:
       """
       Brief one-line description.
       
       More detailed description if needed. This can span multiple
       lines and include examples, notes, warnings, etc.
       
       Args:
           param1: Description of param1
           param2: Description of param2
           
       Returns:
           Description of return value, or None if error
           
       Raises:
           ValueError: If param1 is empty
           TypeError: If param2 is not an integer
           
       Example:
           >>> my_function("test", 42)
           "result"
           
       Note:
           Additional notes about usage or behavior.
       """
       pass

Code Comments
~~~~~~~~~~~~~

.. code-block:: python

   # Use comments to explain WHY, not WHAT
   # Good: Normalize path to prevent directory traversal attacks
   # Bad: Convert slashes to backslashes

   # Complex logic should be explained
   if some_complex_condition:
       # This handles the edge case where...
       do_something()

Pull Request Guidelines
------------------------

Before Submitting
~~~~~~~~~~~~~~~~~

- [ ] All tests pass
- [ ] Code follows style guidelines
- [ ] New code has tests
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated
- [ ] No merge conflicts with main branch

PR Description Template
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: markdown

   ## Description
   Brief description of what this PR does.

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Performance improvement
   - [ ] Code refactoring

   ## Testing
   Describe how you tested your changes.

   ## Screenshots (if applicable)
   Add screenshots for UI changes.

   ## Checklist
   - [ ] Tests pass
   - [ ] Documentation updated
   - [ ] CHANGELOG updated

Code Review Process
~~~~~~~~~~~~~~~~~~~

1. Maintainers will review your PR
2. Address any feedback or requested changes
3. Once approved, your PR will be merged
4. Your contribution will be credited in release notes

Bug Reports
-----------

When reporting bugs, include:

- Anki version
- Add-on version
- Operating system
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages or console output
- Relevant card template code

Feature Requests
----------------

When suggesting features:

- Describe the feature clearly
- Explain the use case
- Provide examples if possible
- Consider compatibility with AnkiDroid
- Discuss implementation approach

Code of Conduct
---------------

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the project
- Show empathy towards other contributors

See our full `Code of Conduct <https://github.com/gallaway-jp/AnkiJSApi/blob/main/CODE_OF_CONDUCT.md>`_.

Getting Help
------------

- Check existing issues and discussions
- Read the :ref:`faq`
- Ask questions in GitHub Discussions
- Join the Anki community forums

Recognition
-----------

Contributors will be:

- Listed in CONTRIBUTORS.md
- Credited in release notes
- Acknowledged in documentation

Thank you for contributing! 🎉

Next Steps
----------

- Review :ref:`development` for setup details
- Check :ref:`testing` for testing guidelines
- Read :ref:`architecture` to understand the codebase
