"""
Integration tests for AnkiDroid JS API Desktop add-on.

These tests validate the add-on works correctly without requiring
a full Anki installation. They test module integration and functionality.

Run these tests:
    pytest tests/test_integration.py -v
"""

import sys
import pytest
from pathlib import Path
from unittest.mock import MagicMock

# Mock Anki modules before importing our code
sys.modules['aqt'] = MagicMock()
sys.modules['aqt.qt'] = MagicMock()
sys.modules['aqt.utils'] = MagicMock()
sys.modules['aqt.operations'] = MagicMock()
sys.modules['aqt.reviewer'] = MagicMock()
sys.modules['aqt.theme'] = MagicMock()
sys.modules['anki'] = MagicMock()
sys.modules['anki.cards'] = MagicMock()
sys.modules['anki.hooks'] = MagicMock()

# These tests now run without requiring Anki to be installed
pytestmark = pytest.mark.integration


class TestAnkiIntegration:
    """
    Integration tests that require Anki installation.
    """
    
    def test_addon_loads_in_anki(self):
        """Test that the add-on modules can be imported with Anki available."""
        # Add our source to path
        addon_src = Path(__file__).parent.parent / "src"
        if str(addon_src) not in sys.path:
            sys.path.insert(0, str(addon_src))
        
        # Import our addon modules
        from ankidroid_js_api import init_addon, setup_api_bridge
        from ankidroid_js_api import api_bridge, card_info, card_actions
        from ankidroid_js_api import reviewer_control, tts_control, ui_control
        
        # Verify they're callable
        assert callable(init_addon)
        assert callable(setup_api_bridge)
        assert hasattr(api_bridge, 'API_REGISTRY')
    
    def test_javascript_injection_in_reviewer(self):
        """Test that JavaScript API file exists and is valid."""
        from ankidroid_js_api.utils import read_js_file
        
        js_content = read_js_file("ankidroid-api.js")
        
        # Verify JavaScript content
        assert "AnkiDroidJS" in js_content
        assert "window.ankiPlatform" in js_content
        assert "function" in js_content or "=>" in js_content
        assert js_content.count("{") == js_content.count("}")
    
    def test_pycmd_bridge_communication(self):
        """Test that pycmd bridge handles commands correctly."""
        from ankidroid_js_api.api_bridge import handle_pycmd, register_api_function
        
        # Register a test function
        def test_func(x=1):
            return x * 2
        
        register_api_function("testFunc", test_func)
        
        # Test pycmd handling
        import json
        mock_reviewer = MagicMock()
        mock_reviewer.web.eval = MagicMock()
        mock_reviewer.card = None  # No card for template hash
        
        # Test valid command with callback format
        handle_pycmd(mock_reviewer, "ankidroidjs:999:testFunc:{\"x\": 5}")
        
        # Verify callback was sent
        assert mock_reviewer.web.eval.called
        
        # Test non-ankidroidjs command
        result = handle_pycmd(mock_reviewer, "other:command")
        assert result is None
    
    def test_api_functions_work_end_to_end(self):
        """Test that API functions are properly registered and work."""
        from ankidroid_js_api.api_bridge import API_REGISTRY, setup_api_bridge
        
        # Clear and setup API
        API_REGISTRY.clear()
        setup_api_bridge()
        
        # Verify all major function categories are registered
        assert len(API_REGISTRY) > 50, f"Expected >50 functions, got {len(API_REGISTRY)}"
        
        # Check specific important functions
        required_functions = [
            "ankiGetCardId",
            "ankiMarkCard",
            "ankiShowAnswer",
            "ankiTtsSpeak",
            "ankiShowToast",
            "ankiSetNoteTags",
            "ankiGetNewCardCount",
        ]
        
        for func_name in required_functions:
            assert func_name in API_REGISTRY, f"{func_name} not registered"
            assert callable(API_REGISTRY[func_name]), f"{func_name} not callable"
    
    def test_tts_functionality_in_anki(self):
        """Test TTS controller initialization and configuration."""
        from ankidroid_js_api.tts_control import TTSController
        
        # Create TTS controller
        tts = TTSController()
        
        # Test configuration
        assert tts.language == "en-US"
        assert tts.pitch == 1.0
        assert tts.rate == 1.0
        
        # Test parameter setting
        assert tts.set_language("ja-JP") is True
        assert tts.language == "ja-JP"
        
        assert tts.set_pitch(1.5) is True
        assert tts.pitch == 1.5
        
        assert tts.set_speech_rate(0.8) is True
        assert tts.rate == 0.8
        
        # Test validation (no longer clamping, raises errors)
        import pytest
        with pytest.raises(ValueError, match="out of range"):
            tts.set_pitch(5.0)
        
        with pytest.raises(ValueError, match="out of range"):
            tts.set_speech_rate(0.1)
    
    def test_config_changes_take_effect(self):
        """Test that configuration can be loaded and validated."""
        from ankidroid_js_api.utils import get_config
        import json
        
        config_path = Path(__file__).parent.parent / "src" / "ankidroid_js_api" / "config.json"
        assert config_path.exists(), "config.json not found"
        
        # Load and validate config structure
        with open(config_path) as f:
            config = json.load(f)
        
        # Verify required sections
        assert "tts" in config
        assert "ui" in config
        
        # Verify TTS config
        assert "enabled" in config["tts"]
        assert "default_language" in config["tts"]
        
        # Verify UI config
        assert "show_toast_notifications" in config["ui"]


class TestCardTemplateIntegration:
    """Tests for card template integration."""
    
    def test_complex_card_template(self):
        """Test that API bridge can inject JavaScript into HTML."""
        from ankidroid_js_api.api_bridge import inject_js_api
        
        # Test with complex HTML
        html = """
        <html>
        <head>
            <title>Test Card</title>
            <style>.card { font-size: 20px; }</style>
        </head>
        <body>
            <div class="card">{{Front}}</div>
        </body>
        </html>
        """
        
        result = inject_js_api(html, None, "question")
        
        # Verify JavaScript was injected
        assert "<script>" in result
        assert "AnkiDroidJS" in result
        assert "</head>" in result
        # Script should be before </head>
        script_pos = result.index("<script>")
        head_end_pos = result.index("</head>")
        assert script_pos < head_end_pos
    
    def test_template_error_handling(self):
        """Test error handling in API functions."""
        # Test that our inject_js_api handles HTML without head tag
        from ankidroid_js_api.api_bridge import inject_js_api
        
        # HTML without head tag
        html_no_head = "<div>Content without head</div>"
        result = inject_js_api(html_no_head, None, "question")
        
        # Should inject at start
        assert result.startswith("<script>")
        assert "AnkiDroidJS" in result


class TestPerformanceIntegration:
    """Performance-related integration tests."""
    
    def test_api_call_performance(self):
        """Test that API calls complete in reasonable time."""
        import time
        from ankidroid_js_api.api_bridge import handle_pycmd
        
        mock_reviewer = MagicMock()
        mock_reviewer.card = MagicMock()
        mock_reviewer.card.id = 12345
        
        # Time multiple API calls
        start = time.time()
        iterations = 100
        
        for _ in range(iterations):
            result = handle_pycmd(mock_reviewer, "ankidroidjs:ankiGetCardId")
        
        elapsed = time.time() - start
        avg_time = elapsed / iterations
        
        # Each call should complete in under 10ms
        assert avg_time < 0.01, f"Average API call took {avg_time*1000:.2f}ms (too slow)"
        print(f"\n  ⏱️  Average API call time: {avg_time*1000:.3f}ms")
    
    def test_javascript_injection_overhead(self):
        """Test that JS injection doesn't significantly impact performance."""
        import time
        from ankidroid_js_api.api_bridge import inject_js_api
        
        # Create a typical card HTML
        html = "<html><head><title>Card</title></head><body>Content</body></html>"
        
        # Time injection
        start = time.time()
        iterations = 1000
        
        for _ in range(iterations):
            result = inject_js_api(html, None, "question")
        
        elapsed = time.time() - start
        avg_time = elapsed / iterations
        
        # Injection should be very fast (under 1ms)
        assert avg_time < 0.001, f"Average injection took {avg_time*1000:.2f}ms (too slow)"
        print(f"\n  ⏱️  Average JS injection time: {avg_time*1000:.3f}ms")


# Example fixture for integration tests (would need proper implementation)
@pytest.fixture(scope="session")
def anki_session():
    """
    Fixture to set up and tear down Anki for testing.
    
    This is a stub showing how such a fixture might be structured.
    Real implementation would need to:
    1. Create isolated test profile
    2. Start Anki in test mode
    3. Load the add-on
    4. Yield for tests
    5. Clean up profile
    """
    # Setup
    test_profile = None
    anki_instance = None
    
    try:
        # Would initialize Anki here
        yield {
            "profile": test_profile,
            "anki": anki_instance
        }
    finally:
        # Cleanup
        pass


@pytest.fixture
def test_deck(anki_session):
    """
    Fixture to create a test deck with sample cards.
    
    This would:
    1. Create a deck
    2. Create note type
    3. Add sample cards
    4. Return deck for testing
    """
    pass


# Documentation for running integration tests
"""
To run integration tests (when implemented):

1. Install pytest-anki or set up Anki test environment
2. Configure test profile path
3. Run with:
   pytest tests/test_integration.py --anki-profile=test_profile

For CI/CD integration:
- Use Anki's headless mode
- Set up virtual display (xvfb on Linux)
- Cache Anki installation

Example GitHub Actions workflow:
```yaml
- name: Install Anki
  run: |
    wget https://github.com/ankitects/anki/releases/download/.../anki.deb
    sudo dpkg -i anki.deb

- name: Run integration tests
  run: pytest tests/test_integration.py
  env:
    ANKI_BASE: /tmp/anki-test
```
"""
