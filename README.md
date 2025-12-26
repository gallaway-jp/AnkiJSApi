# AnkiDroid JS API for Desktop

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/gallaway-jp/AnkiJSApi/workflows/Tests/badge.svg)](https://github.com/gallaway-jp/AnkiJSApi/actions)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

A desktop Anki add-on that brings AnkiDroid's powerful JavaScript template API to Anki Desktop, enabling advanced interactive card templates with programmatic control over the reviewer, TTS, card actions, and more.

## Features

This add-on implements the AnkiDroidJS API for desktop Anki, providing:

### Card Information APIs
- Get card counts (new, learning, review)
- Access card metadata (ID, type, interval, ease factor, etc.)
- Retrieve review statistics (reps, lapses, due date)
- Check card flags and marks

### Card Action APIs
- Mark/unmark cards
- Toggle flags (red, orange, green, blue, pink, turquoise, purple)
- Bury cards and notes
- Suspend cards and notes
- Reset card progress
- Set custom due dates
- Search for cards

### Reviewer Control APIs
- Check if displaying answer
- Programmatically show answer
- Answer cards with specific ease (Again/Hard/Good/Easy)

### Text-to-Speech APIs
- Speak text with customizable language, pitch, and rate
- Check if TTS is currently speaking
- Stop TTS playback

### UI Control APIs
- Detect night mode status
- Show toast messages
- Enable/disable scrollbars

### Tag Management APIs
- Get note tags
- Set note tags (add/remove/replace)

### Utility APIs
- Check network metered status

## Requirements

### Anki Desktop
This add-on requires **Anki Desktop** to be installed separately. It is designed to work with:

- **Anki 2.1.50+** (recommended: Anki 2.1.60 or later)
- **Python 3.9+** (included with modern Anki versions)

**Important:** This add-on extends Anki Desktop and does not include Anki itself. You must download and install Anki separately from [apps.ankiweb.net](https://apps.ankiweb.net/).

**License Note:** Anki Desktop is licensed under the [GNU Affero General Public License v3.0 (AGPL-3.0)](https://github.com/ankitects/anki/blob/main/LICENSE). However, per Anki's plugin policy, add-ons may use any license and are not subject to the AGPL requirements.

## Installation

### From AnkiWeb (Coming Soon)
1. Open Anki Desktop
2. Go to Tools → Add-ons → Get Add-ons
3. Enter code: `XXXXXXXXX`
4. Restart Anki

### Manual Installation
1. Download the latest release from [GitHub Releases](https://github.com/yourusername/ankidroid-js-api-desktop/releases)
2. Open Anki Desktop
3. Go to Tools → Add-ons → Install from file
4. Select the downloaded `.ankiaddon` file
5. Restart Anki

### From Source
1. Clone this repository:
   ```bash
   git clone https://github.com/gallaway-jp/AnkiJSApi.git
   cd AnkiJSApi
   ```

2. Create a symbolic link to your Anki addons folder:
   
   **Windows:**
   ```powershell
   mklink /D "%APPDATA%\Anki2\addons21\ankidroid_js_api" "path\to\ankidroid-js-api-desktop\src\ankidroid_js_api"
   ```
   
   **macOS/Linux:**
   ```bash
   ln -s "$(pwd)/src/ankidroid_js_api" "$HOME/.local/share/Anki2/addons21/ankidroid_js_api"
   ```

3. Restart Anki

## Usage

### In Your Card Templates

Initialize the API in your card template's script section:

```html
<script>
// Initialize the API
const api = AnkiDroidJS.init({ 
    developer: "your-email@example.com", 
    version: "0.0.3" 
});

// Use the API
async function loadCardInfo() {
    const cardId = await api.ankiGetCardId();
    const reps = await api.ankiGetCardReps();
    console.log(`Card ${cardId} has been reviewed ${reps} times`);
}

loadCardInfo();
</script>
```

### Complete Example

```html
<!-- Front Template -->
<div class="question">{{Front}}</div>

<button onclick="playTTS()">🔊 Speak</button>
<div id="stats"></div>

<script>
const api = AnkiDroidJS.init({ 
    developer: "learner@example.com", 
    version: "0.0.3" 
});

async function playTTS() {
    await api.ankiTtsSpeak("{{Front}}", 0);
}

async function showStats() {
    const newCards = await api.ankiGetNewCardCount();
    const revCards = await api.ankiGetRevCardCount();
    const eta = await api.ankiGetETA();
    
    document.getElementById('stats').innerHTML = 
        `${newCards} new, ${revCards} review, ${eta} min remaining`;
}

showStats();
</script>

<!-- Back Template -->
{{FrontSide}}
<hr>
<div class="answer">{{Back}}</div>

<button onclick="markDifficult()">Mark Difficult</button>

<script>
async function markDifficult() {
    await api.ankiToggleFlag("red");
    await api.ankiShowToast("Flagged as difficult");
}
</script>
```

## API Reference

See [TEMPLATE_API_REFERENCE.md](TEMPLATE_API_REFERENCE.md) for complete API documentation.

## Compatibility

- **Anki Desktop:** 2.1.50+
- **API Version:** 0.0.3
- **Python:** 3.9+

## Development

### Project Structure

```
ankidroid-js-api-desktop/
├── src/
│   └── ankidroid_js_api/
│       ├── __init__.py          # Add-on entry point
│       ├── api_bridge.py        # JavaScript API bridge
│       ├── card_info.py         # Card information APIs
│       ├── card_actions.py      # Card action APIs
│       ├── reviewer_control.py  # Reviewer control APIs
│       ├── tts_control.py       # Text-to-speech APIs
│       ├── ui_control.py        # UI control APIs
│       ├── tag_manager.py       # Tag management APIs
│       ├── utils.py             # Utility functions
│       ├── js/
│       │   └── ankidroid-api.js # JavaScript API implementation
│       ├── manifest.json        # Add-on manifest
│       └── config.json          # Default configuration
├── tests/                       # Unit tests
├── docs/                        # Documentation
├── LICENSE                      # MIT License
├── README.md                    # This file
├── setup.py                     # Package setup
└── requirements-dev.txt         # Development dependencies
```

### Running Tests

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=src/ankidroid_js_api tests/
```

### Building

```bash
# Build the add-on package
python setup.py build_addon

# The .ankiaddon file will be in the dist/ directory
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Third-Party Software

This add-on is designed to extend [Anki Desktop](https://apps.ankiweb.net/), which is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0). However, per Anki's plugin policy, add-ons may use any license. This add-on does NOT distribute Anki and must be used with a separately installed copy of Anki Desktop.

For detailed license compliance information, see [LICENSE_COMPLIANCE.md](docs/LICENSE_COMPLIANCE.md) and [NOTICE](NOTICE).

**Runtime Dependencies:** None (uses only Python standard library and Anki's built-in APIs)  
**Development Dependencies:** See [requirements-dev.txt](requirements-dev.txt) - MIT, BSD, Apache-2.0 licenses

## Credits

- **AnkiDroid Team** - For the original JavaScript API implementation
- **Anki Desktop** - For the extensible add-on system

## Links

- [AnkiDroid GitHub](https://github.com/ankidroid/Anki-Android)
- [Anki Desktop](https://apps.ankiweb.net/)
- [Anki Add-on Development Guide](https://addon-docs.ankiweb.net/)

## Support

If you encounter any issues or have questions:
- Open an issue on [GitHub Issues](https://github.com/yourusername/ankidroid-js-api-desktop/issues)
- Check the [documentation](docs/)
- Join the discussion on [Anki Forums](https://forums.ankiweb.net/)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.
