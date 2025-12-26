# Project Structure

```
ankidroid-js-api-desktop/
│
├── src/
│   └── ankidroid_js_api/              # Main add-on package
│       ├── __init__.py                # Add-on initialization and entry point
│       ├── api_bridge.py              # JavaScript-Python bridge and function registry
│       ├── card_info.py               # Card information APIs
│       ├── card_actions.py            # Card action APIs (mark, flag, bury, etc.)
│       ├── reviewer_control.py        # Reviewer control APIs (show answer, answer cards)
│       ├── tts_control.py             # Text-to-speech control APIs
│       ├── ui_control.py              # UI control APIs (toasts, night mode, etc.)
│       ├── tag_manager.py             # Tag management APIs
│       ├── utils.py                   # Utility functions
│       ├── config.json                # Default add-on configuration
│       ├── manifest.json              # Anki add-on manifest
│       └── js/
│           └── ankidroid-api.js       # JavaScript API implementation
│
├── tests/                             # Unit tests
│   ├── __init__.py
│   ├── conftest.py                    # Pytest configuration
│   ├── test_card_info.py              # Tests for card_info module
│   └── test_tag_manager.py            # Tests for tag_manager module
│
├── docs/                              # Documentation
│   ├── EXAMPLES.md                    # Example card templates
│   ├── INSTALLATION.md                # Detailed installation guide
│   └── FAQ.md                         # Frequently asked questions
│
├── .gitignore                         # Git ignore file
├── CHANGELOG.md                       # Version history
├── CONTRIBUTING.md                    # Contribution guidelines
├── LICENSE                            # MIT License
├── README.md                          # Main documentation
├── QUICKSTART.md                      # Quick start guide
├── pyproject.toml                     # Modern Python project configuration
├── requirements-dev.txt               # Development dependencies
├── setup.py                           # Package setup and build script
├── card-template-api.md               # Anki desktop API reference (for comparison)
└── TEMPLATE_API_REFERENCE.md          # AnkiDroid API reference (for comparison)
```

## Module Overview

### Core Modules

#### `__init__.py`
- Entry point for the add-on
- Initializes the API bridge
- Sets up error handling
- Registers hooks

#### `api_bridge.py`
- Creates the bridge between JavaScript and Python
- Registers all API functions
- Handles pycmd communication
- Injects JavaScript into card templates

#### `utils.py`
- Configuration management
- Logging utilities
- File I/O helpers
- Common utility functions

### API Implementation Modules

#### `card_info.py`
Card information retrieval functions:
- `anki_get_new_card_count()` - Get count of new cards
- `anki_get_lrn_card_count()` - Get count of learning cards
- `anki_get_rev_card_count()` - Get count of review cards
- `anki_get_eta()` - Get estimated time remaining
- `anki_get_card_mark()` - Check if card is marked
- `anki_get_card_flag()` - Get card flag color
- `anki_get_card_reps()` - Get review count
- `anki_get_card_interval()` - Get current interval
- `anki_get_card_factor()` - Get ease factor
- `anki_get_card_id()` - Get card ID
- And more...

#### `card_actions.py`
Card action functions:
- `anki_mark_card()` - Toggle mark status
- `anki_toggle_flag()` - Set/remove flag
- `anki_bury_card()` - Bury card
- `anki_bury_note()` - Bury all cards in note
- `anki_suspend_card()` - Suspend card
- `anki_suspend_note()` - Suspend all cards in note
- `anki_reset_progress()` - Reset card progress
- `anki_search_card()` - Search for cards
- `anki_set_card_due()` - Set due date

#### `reviewer_control.py`
Reviewer control functions:
- `anki_is_displaying_answer()` - Check if showing answer
- `anki_show_answer()` - Show the answer
- `anki_answer_ease1()` - Answer "Again"
- `anki_answer_ease2()` - Answer "Hard"
- `anki_answer_ease3()` - Answer "Good"
- `anki_answer_ease4()` - Answer "Easy"

#### `tts_control.py`
Text-to-speech functions:
- `anki_tts_speak()` - Speak text
- `anki_tts_set_language()` - Set TTS language
- `anki_tts_set_pitch()` - Set voice pitch
- `anki_tts_set_speech_rate()` - Set speech rate
- `anki_tts_is_speaking()` - Check if speaking
- `anki_tts_stop()` - Stop TTS

#### `ui_control.py`
UI control functions:
- `anki_is_in_fullscreen()` - Check fullscreen status
- `anki_is_in_night_mode()` - Check night mode
- `anki_show_toast()` - Show toast notification
- `anki_enable_horizontal_scrollbar()` - Control scrollbars
- `anki_show_options_menu()` - Show options

#### `tag_manager.py`
Tag management functions:
- `anki_set_note_tags()` - Set note tags
- `anki_get_note_tags()` - Get note tags
- `anki_add_tag_to_note()` - Add tag to note (deprecated)

### JavaScript API

#### `js/ankidroid-api.js`
- Implements the AnkiDroidJS API in JavaScript
- Provides Promise-based interface
- Communicates with Python via pycmd
- Matches AnkiDroid's API signature

## Testing

### Test Structure

Tests use pytest and mocking to test functionality without requiring Anki to be running.

#### `conftest.py`
- Sets up test environment
- Adds src to Python path
- Provides shared fixtures

#### `test_card_info.py`
- Tests for card information functions
- Mocks Anki's collection and cards
- Verifies correct data retrieval

#### `test_tag_manager.py`
- Tests for tag management
- Verifies tag setting and retrieval
- Tests edge cases

## Documentation

### User Documentation

- **README.md** - Overview, features, basic usage
- **QUICKSTART.md** - 5-minute getting started guide
- **INSTALLATION.md** - Detailed installation instructions
- **EXAMPLES.md** - Example card templates
- **FAQ.md** - Common questions and troubleshooting

### Developer Documentation

- **CONTRIBUTING.md** - How to contribute
- **CHANGELOG.md** - Version history
- **setup.py** - Build and packaging info
- **pyproject.toml** - Modern Python configuration

## Configuration

### `config.json`
Default configuration options:
```json
{
    "enabled": true,
    "debug_mode": false,
    "log_api_calls": false,
    "tts": {...},
    "ui": {...}
}
```

### `manifest.json`
Anki add-on metadata:
```json
{
    "package": "ankidroid_js_api",
    "name": "AnkiDroid JS API for Desktop",
    "human_version": "1.0.0",
    ...
}
```

## Build and Packaging

### Building the Add-on

```bash
python setup.py build_addon
```

Creates a `.ankiaddon` file in the `dist/` directory.

### Development Installation

Create a symbolic link to test changes without rebuilding:

```bash
# Windows
mklink /D "%APPDATA%\Anki2\addons21\ankidroid_js_api" "src\ankidroid_js_api"

# macOS/Linux
ln -s "$(pwd)/src/ankidroid_js_api" "$HOME/.local/share/Anki2/addons21/ankidroid_js_api"
```

## Workflow

1. **User creates card template** with JavaScript using AnkiDroidJS API
2. **User reviews card** in Anki Desktop
3. **add-on injects** `ankidroid-api.js` into the card HTML
4. **JavaScript calls API function** (e.g., `api.ankiGetCardId()`)
5. **JavaScript sends pycmd** to Python backend
6. **Python function executes** and returns result
7. **Result returned to JavaScript** via Promise
8. **Template updates UI** with the result

## API Compatibility

The add-on implements AnkiDroid JS API version **0.0.3**, providing compatibility with AnkiDroid card templates.

### Supported Features

✅ Card information APIs  
✅ Card action APIs  
✅ Reviewer control APIs  
✅ Text-to-speech APIs  
✅ UI control APIs  
✅ Tag management APIs  

### Known Limitations

❌ Speech-to-text (STT) not implemented  
⚠️ TTS uses system TTS (different from AnkiDroid)  
⚠️ Some mobile-specific UI features adapted for desktop  

## Future Enhancements

Potential future additions:
- Speech-to-text support
- Additional card scheduling APIs
- Custom filter support
- Performance optimizations
- More comprehensive testing
- Integration with other add-ons
