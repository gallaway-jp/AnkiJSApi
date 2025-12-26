# Development & Build Guide

This guide covers development setup, testing, and building the AnkiDroid JS API for Desktop add-on.

## Prerequisites

- Python 3.9 or higher
- Git
- Anki Desktop 2.1.50+
- Text editor or IDE (VS Code recommended)

## Initial Setup

### 1. Clone the Repository

```bash
git clone https://github.com/gallaway-jp/AnkiJSApi.git
cd AnkiJSApi
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### 3. Install Development Dependencies

```bash
pip install -r requirements-dev.txt
```

### 4. Link Add-on for Development

Create a symbolic link so changes are immediately reflected in Anki:

**Windows (PowerShell as Administrator):**
```powershell
$source = "$PWD\src\ankidroid_js_api"
$target = "$env:APPDATA\Anki2\addons21\ankidroid_js_api"
New-Item -ItemType SymbolicLink -Path $target -Target $source
```

**macOS:**
```bash
ln -s "$(pwd)/src/ankidroid_js_api" "$HOME/Library/Application Support/Anki2/addons21/ankidroid_js_api"
```

**Linux:**
```bash
ln -s "$(pwd)/src/ankidroid_js_api" "$HOME/.local/share/Anki2/addons21/ankidroid_js_api"
```

### 5. Restart Anki

Close and reopen Anki to load the add-on.

## Development Workflow

### Making Changes

1. **Edit Python files** in `src/ankidroid_js_api/`
2. **Edit JavaScript** in `src/ankidroid_js_api/js/ankidroid-api.js`
3. **Restart Anki** to reload the add-on
4. **Test your changes** in card templates

### Debugging

#### Enable Debug Mode

Edit add-on configuration (Tools → Add-ons → Config):
```json
{
    "debug_mode": true,
    "log_api_calls": true
}
```

#### View Debug Output

1. **Console Output**: Tools → Debug Console
2. **Add-on Errors**: Tools → Add-ons → View Add-on Errors
3. **Python Logs**: Check terminal if running Anki from command line

#### Debug Tips

```python
# Add debug prints in Python code
from .utils import log_debug
log_debug("My debug message")

# Or use standard print
print("Debug:", some_variable)
```

```javascript
// Add console logs in JavaScript
console.log("Debug:", someVariable);
console.error("Error occurred:", error);
```

### Code Quality

#### Format Code with Black

```bash
black src/
```

#### Run Linter

```bash
# PyLint
pylint src/ankidroid_js_api/

# Flake8
flake8 src/
```

#### Type Checking

```bash
mypy src/ankidroid_js_api/
```

## Testing

### Run All Tests

```bash
pytest tests/
```

### Run with Coverage

```bash
pytest --cov=src/ankidroid_js_api --cov-report=html tests/
```

Then open `htmlcov/index.html` to view coverage report.

### Run Specific Test

```bash
# Test file
pytest tests/test_card_info.py

# Specific test function
pytest tests/test_card_info.py::test_get_card_id

# With verbose output
pytest -v tests/test_card_info.py
```

### Writing Tests

Example test:

```python
import pytest
from unittest.mock import Mock, patch

def test_new_feature(mock_mw):
    """Test description."""
    # Arrange
    with patch('module.function', return_value=Mock()):
        # Act
        result = my_function()
        
        # Assert
        assert result == expected_value
```

### Testing in Anki

1. Create test cards with various templates
2. Enable debug mode
3. Review cards and check console output
4. Test all API functions
5. Test edge cases (no card, suspended cards, etc.)

## Building

### Build the Add-on Package

```bash
python setup.py build_addon
```

This creates `dist/ankidroid_js_api_desktop-1.0.0.ankiaddon`

### Build Process

The build command:
1. Reads version from `manifest.json`
2. Creates a `.ankiaddon` file (zip format)
3. Includes all Python files
4. Includes JavaScript files
5. Includes config and manifest
6. Excludes `__pycache__` and `.pyc` files

### Manual Build

You can also manually create the package:

```bash
cd src/ankidroid_js_api
zip -r ../../dist/ankidroid_js_api.ankiaddon . -x "*.pyc" -x "__pycache__/*"
```

## Version Management

### Updating Version

Update version in these files:
1. `src/ankidroid_js_api/manifest.json` - `human_version`
2. `setup.py` - `version`
3. `pyproject.toml` - `version`
4. `src/ankidroid_js_api/__init__.py` - `__version__`

### Creating a Release

1. **Update version numbers** (as above)

2. **Update CHANGELOG.md**:
   ```markdown
   ## [1.1.0] - 2025-01-15
   
   ### Added
   - New feature X
   
   ### Fixed
   - Bug Y
   ```

3. **Commit changes**:
   ```bash
   git add .
   git commit -m "Release v1.1.0"
   ```

4. **Create tag**:
   ```bash
   git tag -a v1.1.0 -m "Release version 1.1.0"
   git push origin v1.1.0
   ```

5. **Build package**:
   ```bash
   python setup.py build_addon
   ```

6. **Create GitHub release**:
   - Go to GitHub → Releases → New Release
   - Select the tag
   - Upload the `.ankiaddon` file
   - Add release notes from CHANGELOG

## Project Structure

```
ankidroid-js-api-desktop/
├── src/ankidroid_js_api/    # Main add-on code
├── tests/                   # Unit tests
├── docs/                    # Documentation
├── dist/                    # Built packages (created by build)
└── venv/                    # Virtual environment (created by you)
```

## Common Tasks

### Add a New API Function

1. **Implement in Python** (e.g., `card_info.py`):
   ```python
   def anki_my_function(param: str) -> bool:
       log_api_call("ankiMyFunction", {"param": param})
       # Implementation
       return True
   ```

2. **Register in `api_bridge.py`**:
   ```python
   register_api_function("ankiMyFunction", card_info.anki_my_function)
   ```

3. **Add JavaScript wrapper** (`js/ankidroid-api.js`):
   ```javascript
   ankiMyFunction: function(param) {
       return callPython('ankiMyFunction', { param: param });
   },
   ```

4. **Write tests** (`tests/test_card_info.py`):
   ```python
   def test_my_function():
       result = card_info.anki_my_function("test")
       assert result is True
   ```

5. **Update documentation** (README.md, EXAMPLES.md)

### Update JavaScript API

Edit `src/ankidroid_js_api/js/ankidroid-api.js` and restart Anki.

### Modify Configuration

Edit `src/ankidroid_js_api/config.json` for default settings.

Users can override in Tools → Add-ons → Config.

## Troubleshooting

### Add-on Not Loading

1. Check symbolic link exists and points to correct directory
2. Look for errors in Tools → Add-ons → View Add-on Errors
3. Ensure no syntax errors in Python files
4. Try removing and recreating the symbolic link

### Tests Failing

1. Ensure virtual environment is activated
2. Install all dev dependencies
3. Check Python version (3.9+)
4. Run with `-v` for verbose output

### Build Fails

1. Check all version numbers match
2. Ensure manifest.json is valid JSON
3. Verify setup.py has no syntax errors
4. Try manually creating zip file

### Changes Not Reflected in Anki

1. Restart Anki after code changes
2. Check symbolic link is correct
3. Clear Anki's web cache (Tools → Preferences → Network → Clear)
4. Disable and re-enable the add-on

## Best Practices

### Code Style

- Follow PEP 8 for Python
- Use type hints where possible
- Write descriptive docstrings
- Keep functions focused and small

### Testing

- Write tests for new features
- Test edge cases
- Mock Anki objects appropriately
- Aim for >80% code coverage

### Documentation

- Update README for user-facing changes
- Add examples for new features
- Keep CHANGELOG up to date
- Comment complex code

### Git Workflow

1. Create feature branch
2. Make changes
3. Write tests
4. Update docs
5. Commit with descriptive message
6. Push and create PR

## Resources

- [Anki Add-on Development Guide](https://addon-docs.ankiweb.net/)
- [Anki Source Code](https://github.com/ankitects/anki)
- [AnkiDroid Source](https://github.com/ankidroid/Anki-Android)
- [Python Packaging Guide](https://packaging.python.org/)

## Getting Help

- Check existing issues on GitHub
- Review the FAQ
- Ask in Anki forums
- Contact maintainers

---

Happy coding! 🚀
