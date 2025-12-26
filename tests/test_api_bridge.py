"""
Unit tests for api_bridge module
"""

import sys
import json
import pytest
from unittest.mock import Mock, MagicMock, patch, call

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

from ankidroid_js_api import api_bridge


class TestAPIRegistry:
    """Test the API function registry."""
    
    def test_register_api_function(self):
        """Test registering an API function."""
        def test_func():
            return "test"
        
        api_bridge.register_api_function("testFunction", test_func)
        
        assert "testFunction" in api_bridge.API_REGISTRY
        assert api_bridge.API_REGISTRY["testFunction"] == test_func
    
    def test_registered_function_callable(self):
        """Test that registered functions can be called."""
        def test_func(x, y):
            return x + y
        
        api_bridge.register_api_function("addFunction", test_func)
        
        result = api_bridge.API_REGISTRY["addFunction"](5, 3)
        assert result == 8


class TestHandlePycmd:
    """Test the pycmd handler."""
    
    @pytest.fixture
    def mock_reviewer(self):
        """Create a mock reviewer."""
        return Mock()
    
    def test_handle_pycmd_non_ankidroidjs_command(self, mock_reviewer):
        """Test handling non-AnkiDroidJS commands."""
        result = api_bridge.handle_pycmd(mock_reviewer, "other:command")
        assert result is None
    
    def test_handle_pycmd_malformed_command(self, mock_reviewer):
        """Test handling malformed AnkiDroidJS commands."""
        result = api_bridge.handle_pycmd(mock_reviewer, "ankidroidjs:")
        assert result is None
    
    def test_handle_pycmd_valid_command_no_args(self, mock_reviewer):
        """Test handling valid command without arguments."""
        def test_func():
            return 42
        
        api_bridge.register_api_function("testFunc", test_func)
        
        # New format: ankidroidjs:callbackId:function:args
        api_bridge.handle_pycmd(mock_reviewer, "ankidroidjs:123:testFunc:{}")
        
        # Verify callback was sent
        assert mock_reviewer.web.eval.called
    
    def test_handle_pycmd_valid_command_with_args(self, mock_reviewer):
        """Test handling valid command with arguments."""
        def test_func(a, b):
            return a * b
        
        api_bridge.register_api_function("multiply", test_func)
        
        args = json.dumps({"a": 6, "b": 7})
        # New format: ankidroidjs:callbackId:function:args
        api_bridge.handle_pycmd(mock_reviewer, f"ankidroidjs:456:multiply:{args}")
        
        # Verify callback was sent
        assert mock_reviewer.web.eval.called
    
    def test_handle_pycmd_function_raises_exception(self, mock_reviewer):
        """Test handling when function raises exception."""
        def error_func():
            raise ValueError("Test error")
        
        api_bridge.register_api_function("errorFunc", error_func)
        
        # New format: ankidroidjs:callbackId:function:args
        api_bridge.handle_pycmd(mock_reviewer, "ankidroidjs:789:errorFunc:{}")
        
        # Verify callback was sent (should contain error)
        assert mock_reviewer.web.eval.called
    
    def test_handle_pycmd_unknown_function(self, mock_reviewer):
        """Test handling call to unknown function."""
        result = api_bridge.handle_pycmd(mock_reviewer, "ankidroidjs:unknownFunc")
        assert result is None


class TestInjectJSAPI:
    """Test JavaScript API injection."""
    
    @patch('ankidroid_js_api.api_bridge.read_js_file')
    def test_inject_js_api_with_head_tag(self, mock_read_js):
        """Test injecting JS API when HTML has head tag."""
        mock_read_js.return_value = "/* API code */"
        
        html = "<html><head><title>Test</title></head><body>Content</body></html>"
        result = api_bridge.inject_js_api(html, None, "question")
        
        assert "<script>/* API code */</script>" in result
        assert "</head>" in result
        # Script should be injected before </head>
        assert result.index("<script>") < result.index("</head>")
    
    @patch('ankidroid_js_api.api_bridge.read_js_file')
    def test_inject_js_api_without_head_tag(self, mock_read_js):
        """Test injecting JS API when HTML has no head tag."""
        mock_read_js.return_value = "/* API code */"
        
        html = "<div>Content</div>"
        result = api_bridge.inject_js_api(html, None, "question")
        
        assert "<script>/* API code */</script>" in result
        # Script should be at the start
        assert result.startswith("<script>")
    
    @patch('ankidroid_js_api.api_bridge.read_js_file')
    def test_inject_js_api_reads_correct_file(self, mock_read_js):
        """Test that injection reads the correct JS file."""
        mock_read_js.return_value = "test"
        
        api_bridge.inject_js_api("<html></html>", None, "question")
        
        mock_read_js.assert_called_once_with("ankidroid-api.js")


class TestSetupAPIBridge:
    """Test the API bridge setup."""
    
    @patch('ankidroid_js_api.api_bridge.gui_hooks')
    @patch('ankidroid_js_api.api_bridge.Reviewer')
    @patch('ankidroid_js_api.api_bridge.log_debug')
    def test_setup_api_bridge_registers_functions(self, mock_log, mock_reviewer, mock_hooks):
        """Test that setup registers all API functions."""
        # Clear registry first
        api_bridge.API_REGISTRY.clear()
        
        api_bridge.setup_api_bridge()
        
        # Check that functions were registered
        assert len(api_bridge.API_REGISTRY) > 0
        
        # Check some key functions are registered
        assert "ankiGetCardId" in api_bridge.API_REGISTRY
        assert "ankiMarkCard" in api_bridge.API_REGISTRY
        assert "ankiShowAnswer" in api_bridge.API_REGISTRY
        assert "ankiTtsSpeak" in api_bridge.API_REGISTRY
        assert "ankiShowToast" in api_bridge.API_REGISTRY
        assert "ankiSetNoteTags" in api_bridge.API_REGISTRY
    
    @patch('ankidroid_js_api.api_bridge.gui_hooks')
    @patch('ankidroid_js_api.api_bridge.Reviewer')
    @patch('ankidroid_js_api.api_bridge.log_debug')
    def test_setup_api_bridge_hooks_registered(self, mock_log, mock_reviewer, mock_hooks):
        """Test that setup registers GUI hooks."""
        api_bridge.setup_api_bridge()
        
        # Verify card_will_show hook was registered
        mock_hooks.card_will_show.append.assert_called_once()


class TestSpecificAPIFunctions:
    """Test specific API function registrations."""
    
    @patch('ankidroid_js_api.api_bridge.gui_hooks')
    @patch('ankidroid_js_api.api_bridge.Reviewer')
    @patch('ankidroid_js_api.api_bridge.log_debug')
    def test_card_info_functions_registered(self, mock_log, mock_reviewer, mock_hooks):
        """Test that all card info functions are registered."""
        api_bridge.API_REGISTRY.clear()
        api_bridge.setup_api_bridge()
        
        card_info_funcs = [
            "ankiGetNewCardCount",
            "ankiGetLrnCardCount",
            "ankiGetRevCardCount",
            "ankiGetETA",
            "ankiGetCardMark",
            "ankiGetCardFlag",
            "ankiGetCardReps",
            "ankiGetCardInterval",
            "ankiGetCardFactor",
            "ankiGetCardMod",
            "ankiGetCardId",
            "ankiGetCardNid",
            "ankiGetCardType",
            "ankiGetCardDid",
            "ankiGetCardQueue",
            "ankiGetCardLapses",
            "ankiGetCardDue",
            "ankiGetDeckName",
            "ankiGetNextTime1",
            "ankiGetNextTime2",
            "ankiGetNextTime3",
            "ankiGetNextTime4",
        ]
        
        for func_name in card_info_funcs:
            assert func_name in api_bridge.API_REGISTRY
    
    @patch('ankidroid_js_api.api_bridge.gui_hooks')
    @patch('ankidroid_js_api.api_bridge.Reviewer')
    @patch('ankidroid_js_api.api_bridge.log_debug')
    def test_card_action_functions_registered(self, mock_log, mock_reviewer, mock_hooks):
        """Test that all card action functions are registered."""
        api_bridge.API_REGISTRY.clear()
        api_bridge.setup_api_bridge()
        
        card_action_funcs = [
            "ankiMarkCard",
            "ankiToggleFlag",
            "ankiBuryCard",
            "ankiBuryNote",
            "ankiSuspendCard",
            "ankiSuspendNote",
            "ankiResetProgress",
            "ankiSearchCard",
            "ankiSetCardDue",
        ]
        
        for func_name in card_action_funcs:
            assert func_name in api_bridge.API_REGISTRY
    
    @patch('ankidroid_js_api.api_bridge.gui_hooks')
    @patch('ankidroid_js_api.api_bridge.Reviewer')
    @patch('ankidroid_js_api.api_bridge.log_debug')
    def test_reviewer_control_functions_registered(self, mock_log, mock_reviewer, mock_hooks):
        """Test that all reviewer control functions are registered."""
        api_bridge.API_REGISTRY.clear()
        api_bridge.setup_api_bridge()
        
        reviewer_funcs = [
            "ankiIsDisplayingAnswer",
            "ankiShowAnswer",
            "ankiAnswerEase1",
            "ankiAnswerEase2",
            "ankiAnswerEase3",
            "ankiAnswerEase4",
        ]
        
        for func_name in reviewer_funcs:
            assert func_name in api_bridge.API_REGISTRY
    
    @patch('ankidroid_js_api.api_bridge.gui_hooks')
    @patch('ankidroid_js_api.api_bridge.Reviewer')
    @patch('ankidroid_js_api.api_bridge.log_debug')
    def test_tts_functions_registered(self, mock_log, mock_reviewer, mock_hooks):
        """Test that all TTS functions are registered."""
        api_bridge.API_REGISTRY.clear()
        api_bridge.setup_api_bridge()
        
        tts_funcs = [
            "ankiTtsSpeak",
            "ankiTtsSetLanguage",
            "ankiTtsSetPitch",
            "ankiTtsSetSpeechRate",
            "ankiTtsIsSpeaking",
            "ankiTtsStop",
            "ankiTtsFieldModifierIsAvailable",
        ]
        
        for func_name in tts_funcs:
            assert func_name in api_bridge.API_REGISTRY
    
    @patch('ankidroid_js_api.api_bridge.gui_hooks')
    @patch('ankidroid_js_api.api_bridge.Reviewer')
    @patch('ankidroid_js_api.api_bridge.log_debug')
    def test_ui_control_functions_registered(self, mock_log, mock_reviewer, mock_hooks):
        """Test that all UI control functions are registered."""
        api_bridge.API_REGISTRY.clear()
        api_bridge.setup_api_bridge()
        
        ui_funcs = [
            "ankiIsInFullscreen",
            "ankiIsTopbarShown",
            "ankiIsInNightMode",
            "ankiEnableHorizontalScrollbar",
            "ankiEnableVerticalScrollbar",
            "ankiShowNavigationDrawer",
            "ankiShowOptionsMenu",
            "ankiShowToast",
        ]
        
        for func_name in ui_funcs:
            assert func_name in api_bridge.API_REGISTRY
    
    @patch('ankidroid_js_api.api_bridge.gui_hooks')
    @patch('ankidroid_js_api.api_bridge.Reviewer')
    @patch('ankidroid_js_api.api_bridge.log_debug')
    def test_tag_management_functions_registered(self, mock_log, mock_reviewer, mock_hooks):
        """Test that all tag management functions are registered."""
        api_bridge.API_REGISTRY.clear()
        api_bridge.setup_api_bridge()
        
        tag_funcs = [
            "ankiSetNoteTags",
            "ankiGetNoteTags",
            "ankiAddTagToNote",
        ]
        
        for func_name in tag_funcs:
            assert func_name in api_bridge.API_REGISTRY
    
    @patch('ankidroid_js_api.api_bridge.gui_hooks')
    @patch('ankidroid_js_api.api_bridge.Reviewer')
    @patch('ankidroid_js_api.api_bridge.log_debug')
    def test_utility_functions_registered(self, mock_log, mock_reviewer, mock_hooks):
        """Test that utility functions are registered."""
        api_bridge.API_REGISTRY.clear()
        api_bridge.setup_api_bridge()
        
        assert "ankiIsActiveNetworkMetered" in api_bridge.API_REGISTRY
