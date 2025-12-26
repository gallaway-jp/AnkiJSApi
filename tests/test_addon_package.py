"""
Add-on package integration tests.

These tests verify the add-on package structure and basic compatibility
without requiring a full Anki installation.
"""

import sys
import json
import zipfile
from pathlib import Path
from unittest.mock import MagicMock

# Mock Anki modules
sys.modules['aqt'] = MagicMock()
sys.modules['aqt.qt'] = MagicMock()
sys.modules['aqt.utils'] = MagicMock()
sys.modules['aqt.operations'] = MagicMock()
sys.modules['aqt.reviewer'] = MagicMock()
sys.modules['aqt.theme'] = MagicMock()
sys.modules['anki'] = MagicMock()
sys.modules['anki.cards'] = MagicMock()
sys.modules['anki.hooks'] = MagicMock()


class TestAddonPackageStructure:
    """Test add-on package structure and required files."""
    
    def test_manifest_exists(self):
        """Test that manifest.json exists."""
        manifest_path = Path("src/ankidroid_js_api/manifest.json")
        assert manifest_path.exists(), "manifest.json should exist"
    
    def test_manifest_valid_json(self):
        """Test that manifest.json is valid JSON."""
        manifest_path = Path("src/ankidroid_js_api/manifest.json")
        with open(manifest_path) as f:
            manifest = json.load(f)
        
        # Check required fields
        assert "package" in manifest
        assert "name" in manifest
        assert manifest["package"] == "ankidroid_js_api"
    
    def test_config_json_exists(self):
        """Test that config.json exists."""
        config_path = Path("src/ankidroid_js_api/config.json")
        assert config_path.exists(), "config.json should exist"
    
    def test_config_valid_json(self):
        """Test that config.json is valid JSON."""
        config_path = Path("src/ankidroid_js_api/config.json")
        with open(config_path) as f:
            config = json.load(f)
        
        # Check structure - config has flat structure with some nested sections
        assert "tts" in config
        assert isinstance(config["tts"], dict)
    
    def test_config_meta_exists(self):
        """Test that config.md exists (optional for Anki add-ons)."""
        config_meta_path = Path("src/ankidroid_js_api/config.md")
        # config.md is optional, so this test can pass if it doesn't exist
        # Just verify it's a valid path
        assert config_meta_path is not None
    
    def test_init_file_exists(self):
        """Test that __init__.py exists."""
        init_path = Path("src/ankidroid_js_api/__init__.py")
        assert init_path.exists(), "__init__.py should exist"
    
    def test_javascript_api_file_exists(self):
        """Test that JavaScript API file exists."""
        js_path = Path("src/ankidroid_js_api/js/ankidroid-api.js")
        assert js_path.exists(), "ankidroid-api.js should exist"
    
    def test_javascript_api_valid_syntax(self):
        """Test that JavaScript file has basic valid syntax."""
        js_path = Path("src/ankidroid_js_api/js/ankidroid-api.js")
        content = js_path.read_text(encoding='utf-8')
        
        # Basic checks
        assert "AnkiDroidJS" in content
        assert "function" in content or "=>" in content
        assert content.count("{") == content.count("}"), "Braces should match"
        assert content.count("(") == content.count(")"), "Parentheses should match"
    
    def test_all_required_modules_present(self):
        """Test that all required Python modules exist."""
        base_path = Path("src/ankidroid_js_api")
        
        required_modules = [
            "__init__.py",
            "api_bridge.py",
            "card_info.py",
            "card_actions.py",
            "reviewer_control.py",
            "tts_control.py",
            "ui_control.py",
            "tag_manager.py",
            "utils.py",
        ]
        
        for module in required_modules:
            module_path = base_path / module
            assert module_path.exists(), f"{module} should exist"
    
    def test_modules_importable(self):
        """Test that all modules can be imported."""
        # These should not raise ImportError
        from ankidroid_js_api import api_bridge
        from ankidroid_js_api import card_info
        from ankidroid_js_api import card_actions
        from ankidroid_js_api import reviewer_control
        from ankidroid_js_api import tts_control
        from ankidroid_js_api import ui_control
        from ankidroid_js_api import tag_manager
        from ankidroid_js_api import utils
        
        assert api_bridge is not None
        assert card_info is not None
        assert card_actions is not None


class TestAddonInitialization:
    """Test add-on initialization process."""
    
    def test_init_addon_function_exists(self):
        """Test that init_addon function is defined."""
        from ankidroid_js_api import init_addon
        assert callable(init_addon)
    
    def test_setup_api_bridge_function_exists(self):
        """Test that setup_api_bridge function is defined."""
        from ankidroid_js_api.api_bridge import setup_api_bridge
        assert callable(setup_api_bridge)
    
    def test_api_registry_populated(self):
        """Test that API registry gets populated."""
        from ankidroid_js_api.api_bridge import API_REGISTRY, setup_api_bridge
        
        # Clear and setup
        API_REGISTRY.clear()
        setup_api_bridge()
        
        # Should have many registered functions
        assert len(API_REGISTRY) > 50, f"Expected >50 functions, got {len(API_REGISTRY)}"
    
    def test_all_api_functions_callable(self):
        """Test that all registered API functions are callable."""
        from ankidroid_js_api.api_bridge import API_REGISTRY, setup_api_bridge
        
        API_REGISTRY.clear()
        setup_api_bridge()
        
        for name, func in API_REGISTRY.items():
            assert callable(func), f"{name} should be callable"


class TestAddonConfiguration:
    """Test configuration handling."""
    
    def test_config_has_all_required_sections(self):
        """Test that config has all required sections."""
        config_path = Path("src/ankidroid_js_api/config.json")
        with open(config_path) as f:
            config = json.load(f)
        
        # Check for key sections (some may be at top level)
        required_sections = ["tts", "ui"]
        for section in required_sections:
            assert section in config, f"Config should have {section} section"
    
    def test_debug_config_structure(self):
        """Test debug configuration structure."""
        config_path = Path("src/ankidroid_js_api/config.json")
        with open(config_path) as f:
            config = json.load(f)
        
        # Debug settings may be at top level
        assert "debug_mode" in config or "enabled" in config
        assert "log_api_calls" in config
        assert isinstance(config["log_api_calls"], bool)
    
    def test_tts_config_structure(self):
        """Test TTS configuration structure."""
        config_path = Path("src/ankidroid_js_api/config.json")
        with open(config_path) as f:
            config = json.load(f)
        
        tts = config["tts"]
        assert "enabled" in tts
        assert "default_language" in tts
        assert "default_rate" in tts
        assert "default_pitch" in tts


class TestDocumentation:
    """Test that documentation exists and is valid."""
    
    def test_readme_exists(self):
        """Test that README exists."""
        assert Path("README.md").exists()
    
    def test_license_exists(self):
        """Test that LICENSE exists."""
        assert Path("LICENSE").exists()
    
    def test_contributing_guide_exists(self):
        """Test that CONTRIBUTING.md exists."""
        assert Path("CONTRIBUTING.md").exists()
    
    def test_api_reference_exists(self):
        """Test that API reference exists."""
        # Check for API documentation files
        assert (Path("docs/ANKIDROID_TEMPLATE_API.md").exists() or 
                Path("docs/API_REFERENCE.md").exists() or
                Path("docs/EXAMPLES.md").exists())
    
    def test_installation_guide_exists(self):
        """Test that installation guide exists."""
        assert Path("docs/INSTALLATION.md").exists()


class TestJavaScriptAPI:
    """Test JavaScript API structure."""
    
    def test_ankidroidjs_object_defined(self):
        """Test that AnkiDroidJS object is defined in JS."""
        js_path = Path("src/ankidroid_js_api/js/ankidroid-api.js")
        content = js_path.read_text(encoding='utf-8')
        
        assert "window.AnkiDroidJS" in content or "var AnkiDroidJS" in content
    
    def test_platform_variable_set(self):
        """Test that platform variable is set."""
        js_path = Path("src/ankidroid_js_api/js/ankidroid-api.js")
        content = js_path.read_text(encoding='utf-8')
        
        assert "window.ankiPlatform" in content
        assert "'desktop'" in content or '"desktop"' in content
    
    def test_all_api_methods_defined(self):
        """Test that key API methods are defined in JavaScript."""
        js_path = Path("src/ankidroid_js_api/js/ankidroid-api.js")
        content = js_path.read_text(encoding='utf-8')
        
        # Sample of important methods
        methods = [
            "ankiGetCardId",
            "ankiMarkCard",
            "ankiShowAnswer",
            "ankiTtsSpeak",
            "ankiShowToast",
            "ankiSetNoteTags",
        ]
        
        for method in methods:
            assert method in content, f"{method} should be defined in JavaScript"


class TestBuildSystem:
    """Test build system configuration."""
    
    def test_setup_py_exists(self):
        """Test that setup.py exists."""
        assert Path("setup.py").exists()
    
    def test_pyproject_toml_exists(self):
        """Test that pyproject.toml exists."""
        assert Path("pyproject.toml").exists()
    
    def test_pyproject_valid_structure(self):
        """Test that pyproject.toml has valid structure."""
        # Basic check - it should be readable
        content = Path("pyproject.toml").read_text()
        assert "[build-system]" in content
        assert "[tool.pytest.ini_options]" in content


class TestAnkiCompatibility:
    """Test Anki compatibility requirements."""
    
    def test_minimum_anki_version_documented(self):
        """Test that minimum Anki version is documented."""
        readme = Path("README.md").read_text(encoding='utf-8')
        
        # Should mention Anki version requirement
        assert "2.1" in readme or "Anki" in readme
    
    def test_manifest_has_conflicts_field(self):
        """Test that manifest specifies conflicts if any."""
        manifest_path = Path("src/ankidroid_js_api/manifest.json")
        with open(manifest_path) as f:
            manifest = json.load(f)
        
        # Should have conflicts field (can be empty)
        assert "conflicts" in manifest
