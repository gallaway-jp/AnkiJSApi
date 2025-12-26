# Contributing to AnkiDroid JS API for Desktop

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/AnkiJSApi.git
   cd AnkiJSApi
   ```

3. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements-dev.txt
   ```

4. Create a symbolic link to test the add-on:
   ```bash
   # Windows
   mklink /D "%APPDATA%\Anki2\addons21\ankidroid_js_api" "path\to\ankidroid-js-api-desktop\src\ankidroid_js_api"
   
   # macOS/Linux
   ln -s "$(pwd)/src/ankidroid_js_api" "$HOME/.local/share/Anki2/addons21/ankidroid_js_api"
   ```

## Development Workflow

### Code Style

We follow PEP 8 for Python code. Use the provided tools:

```bash
# Format code with black
black src/

# Check with pylint
pylint src/ankidroid_js_api/

# Type checking with mypy
mypy src/ankidroid_js_api/
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=src/ankidroid_js_api tests/

# Run specific test file
python -m pytest tests/test_card_info.py
```

### Adding New Features

1. **Create a new branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Implement your feature:**
   - Add Python implementation in appropriate module
   - Update `api_bridge.py` to register new functions
   - Add JavaScript wrapper in `js/ankidroid-api.js`
   - Write unit tests in `tests/`
   - Update documentation

3. **Test your changes:**
   - Run unit tests
   - Test manually in Anki Desktop
   - Verify compatibility with existing card templates

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Add feature: description of feature"
   ```

5. **Push and create a pull request:**
   ```bash
   git push origin feature/your-feature-name
   ```

## API Implementation Guidelines

### Adding a New API Function

1. **Python implementation** (e.g., in `card_info.py`):
   ```python
   def anki_my_new_function(param1: str, param2: int) -> bool:
       """Brief description of what this function does."""
       log_api_call("ankiMyNewFunction", {"param1": param1, "param2": param2})
       
       # Implementation here
       
       return True
   ```

2. **Register in api_bridge.py**:
   ```python
   register_api_function("ankiMyNewFunction", module.anki_my_new_function)
   ```

3. **JavaScript wrapper** (in `js/ankidroid-api.js`):
   ```javascript
   ankiMyNewFunction: function(param1, param2) {
       return callPython('ankiMyNewFunction', { 
           param1: param1, 
           param2: param2 
       });
   },
   ```

4. **Add tests** (in `tests/test_module.py`):
   ```python
   def test_my_new_function(mock_mw):
       """Test the new function."""
       result = module.anki_my_new_function("test", 42)
       assert result is True
   ```

5. **Update documentation**:
   - Add to README.md if it's a major feature
   - Add example usage to EXAMPLES.md
   - Update CHANGELOG.md

## Testing Guidelines

### What to Test

- Function returns correct values
- Function handles missing/invalid input gracefully
- Function works when no card is displayed
- Function works with different card states
- Error handling and edge cases

### Mock Objects

Use the provided fixtures in `conftest.py`:

```python
def test_my_function(mock_mw, mock_card):
    """Test with mocked Anki objects."""
    with patch('module.get_current_card', return_value=mock_card):
        result = module.my_function()
        assert result == expected_value
```

## Documentation

### Code Documentation

- Use docstrings for all functions
- Include parameter types and return types
- Describe what the function does and any side effects

### User Documentation

- Update README.md for user-facing changes
- Add examples to EXAMPLES.md for new features
- Keep CHANGELOG.md up to date

## Pull Request Process

1. **Ensure tests pass:**
   ```bash
   python -m pytest tests/
   ```

2. **Update documentation:**
   - README.md
   - EXAMPLES.md
   - CHANGELOG.md

3. **Describe your changes:**
   - What does this PR do?
   - Why is this change needed?
   - How has it been tested?
   - Any breaking changes?

4. **Request review:**
   - Tag relevant maintainers
   - Respond to feedback
   - Make requested changes

## Code Review Checklist

- [ ] Code follows PEP 8 style guidelines
- [ ] All tests pass
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated
- [ ] No breaking changes (or clearly documented)
- [ ] Functions have proper error handling
- [ ] Code is well-commented

## Release Process

For maintainers:

1. Update version in:
   - `manifest.json`
   - `setup.py`
   - `__init__.py`

2. Update CHANGELOG.md with release notes

3. Create a git tag:
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

4. Build the add-on:
   ```bash
   python setup.py build_addon
   ```

5. Create GitHub release with the `.ankiaddon` file

## Questions?

- Open an issue for bugs or feature requests
- Check existing issues before creating new ones
- Be respectful and constructive

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
