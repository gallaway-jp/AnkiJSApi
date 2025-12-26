"""
Unit tests for security module - input validation and rate limiting.
"""

import sys
from unittest.mock import MagicMock

# Mock Anki modules before importing anything
sys.modules['aqt'] = MagicMock()
sys.modules['aqt.utils'] = MagicMock()
sys.modules['aqt.reviewer'] = MagicMock()
sys.modules['aqt.qt'] = MagicMock()
sys.modules['aqt.operations'] = MagicMock()
sys.modules['aqt.theme'] = MagicMock()
sys.modules['anki'] = MagicMock()
sys.modules['anki.cards'] = MagicMock()
sys.modules['anki.notes'] = MagicMock()
sys.modules['anki.collection'] = MagicMock()

import pytest
import time
from unittest.mock import patch

from ankidroid_js_api.security import (
    InputValidator,
    RateLimiter,
    sanitize_for_logging,
    generate_template_hash
)
from ankidroid_js_api.constants import (
    MAX_TEXT_LENGTH,
    MAX_TAG_LENGTH,
    MAX_LOG_MESSAGE_LENGTH
)


class TestInputValidator:
    """Test InputValidator class."""
    
    def test_validate_text_success(self):
        """Test valid text passes validation."""
        result = InputValidator.validate_text("Hello World")
        assert result == "Hello World"
    
    def test_validate_text_with_newlines(self):
        """Test text with newlines when allowed."""
        result = InputValidator.validate_text("Line 1\nLine 2", allow_newlines=True)
        assert "Line 1" in result
        assert "Line 2" in result
    
    def test_validate_text_strips_newlines_when_disabled(self):
        """Test newlines are removed when not allowed."""
        result = InputValidator.validate_text("Line 1\nLine 2", allow_newlines=False)
        assert "\n" not in result
    
    def test_validate_text_removes_null_bytes(self):
        """Test null bytes are removed."""
        result = InputValidator.validate_text("Hello\x00World")
        assert "\x00" not in result
        assert "HelloWorld" in result
    
    def test_validate_text_removes_control_characters(self):
        """Test control characters are removed."""
        result = InputValidator.validate_text("Hello\x01\x02World")
        assert "\x01" not in result
        assert "\x02" not in result
    
    def test_validate_text_max_length_enforced(self):
        """Test maximum length is enforced."""
        long_text = "A" * 1000
        with pytest.raises(ValueError, match="Text too long"):
            InputValidator.validate_text(long_text, max_length=100)
    
    def test_validate_text_type_error(self):
        """Test non-string input raises TypeError."""
        with pytest.raises(TypeError, match="Expected string input"):
            InputValidator.validate_text(12345)
    
    def test_validate_text_invalid_pattern(self):
        """Test invalid characters raise ValueError."""
        with pytest.raises(ValueError, match="invalid characters"):
            InputValidator.validate_text("<script>alert('xss')</script>")
    
    def test_validate_integer_success(self):
        """Test valid integer passes validation."""
        result = InputValidator.validate_integer(42, min_val=0, max_val=100)
        assert result == 42
    
    def test_validate_integer_from_string(self):
        """Test string can be converted to integer."""
        result = InputValidator.validate_integer("42", min_val=0, max_val=100)
        assert result == 42
    
    def test_validate_integer_out_of_range_min(self):
        """Test value below minimum raises ValueError."""
        with pytest.raises(ValueError, match="out of range"):
            InputValidator.validate_integer(-10, min_val=0, max_val=100)
    
    def test_validate_integer_out_of_range_max(self):
        """Test value above maximum raises ValueError."""
        with pytest.raises(ValueError, match="out of range"):
            InputValidator.validate_integer(200, min_val=0, max_val=100)
    
    def test_validate_integer_type_error(self):
        """Test invalid type raises TypeError."""
        with pytest.raises(TypeError, match="Expected integer"):
            InputValidator.validate_integer("not a number", min_val=0, max_val=100)
    
    def test_validate_float_success(self):
        """Test valid float passes validation."""
        result = InputValidator.validate_float(1.5, min_val=0.0, max_val=2.0)
        assert result == 1.5
    
    def test_validate_float_from_string(self):
        """Test string can be converted to float."""
        result = InputValidator.validate_float("1.5", min_val=0.0, max_val=2.0)
        assert result == 1.5
    
    def test_validate_float_out_of_range(self):
        """Test value out of range raises ValueError."""
        with pytest.raises(ValueError, match="out of range"):
            InputValidator.validate_float(5.0, min_val=0.0, max_val=2.0)
    
    def test_validate_float_type_error(self):
        """Test invalid type raises TypeError."""
        with pytest.raises(TypeError, match="Expected float"):
            InputValidator.validate_float("not a number", min_val=0.0, max_val=2.0)
    
    def test_validate_filename_success(self):
        """Test valid filename passes validation."""
        result = InputValidator.validate_filename("api-script.js")
        assert result == "api-script.js"
    
    def test_validate_filename_path_traversal_dots(self):
        """Test path traversal with .. is rejected."""
        with pytest.raises(ValueError, match="Invalid filename"):
            InputValidator.validate_filename("../../../etc/passwd")
    
    def test_validate_filename_path_traversal_slash(self):
        """Test path with forward slash is rejected."""
        with pytest.raises(ValueError, match="Invalid filename"):
            InputValidator.validate_filename("subdir/file.js")
    
    def test_validate_filename_path_traversal_backslash(self):
        """Test path with backslash is rejected."""
        with pytest.raises(ValueError, match="Invalid filename"):
            InputValidator.validate_filename("subdir\\file.js")
    
    def test_validate_filename_invalid_characters(self):
        """Test filename with invalid characters is rejected."""
        with pytest.raises(ValueError, match="Invalid filename"):
            InputValidator.validate_filename("file<script>.js")
    
    def test_validate_filename_type_error(self):
        """Test non-string filename raises TypeError."""
        with pytest.raises(TypeError, match="Filename must be a string"):
            InputValidator.validate_filename(123)
    
    def test_validate_tag_success(self):
        """Test valid tag passes validation."""
        result = InputValidator.validate_tag("my-tag")
        assert result == "my-tag"
    
    def test_validate_tag_spaces_converted_to_underscores(self):
        """Test spaces are converted to underscores."""
        result = InputValidator.validate_tag("my tag")
        assert result == "my_tag"
    
    def test_validate_tag_too_long(self):
        """Test tag longer than max is rejected."""
        with pytest.raises(ValueError, match="Tag too long"):
            InputValidator.validate_tag("A" * 200, max_length=100)
    
    def test_validate_tag_empty(self):
        """Test empty tag is rejected."""
        with pytest.raises(ValueError, match="cannot be empty"):
            InputValidator.validate_tag("   ")
    
    def test_validate_tag_invalid_characters(self):
        """Test tag with invalid characters is rejected."""
        with pytest.raises(ValueError, match="Invalid tag characters"):
            InputValidator.validate_tag("tag<script>")
    
    def test_validate_tag_type_error(self):
        """Test non-string tag raises TypeError."""
        with pytest.raises(TypeError, match="Tag must be a string"):
            InputValidator.validate_tag(123)


class TestRateLimiter:
    """Test RateLimiter class."""
    
    def setup_method(self):
        """Reset rate limiter before each test."""
        RateLimiter.reset()
    
    def test_check_first_call_allowed(self):
        """Test first call is always allowed."""
        result = RateLimiter.check("template1", "function1", max_per_second=10)
        assert result is True
    
    def test_check_within_limit(self):
        """Test calls within limit are allowed."""
        for i in range(10):
            result = RateLimiter.check("template1", "function1", max_per_second=10)
            assert result is True
            time.sleep(0.01)  # Small delay to avoid hitting limit
    
    def test_check_exceeds_limit(self):
        """Test calls exceeding limit are blocked."""
        # Mock time to prevent token refill between calls
        with patch('ankidroid_js_api.security.time.time') as mock_time:
            current = 1000.0
            mock_time.return_value = current
            
            # First call initializes bucket with 10 tokens (doesn't consume)
            # Calls 2-11 each consume 1 token (10 tokens consumed)
            for i in range(11):
                result = RateLimiter.check("template1", "function1", max_per_second=10)
                assert result is True
            
            # 12th call should be blocked (all 10 tokens consumed)
            result = RateLimiter.check("template1", "function1", max_per_second=10)
            assert result is False
    
    def test_check_tokens_refill_over_time(self):
        """Test tokens refill after time passes."""
        # Use up tokens
        for i in range(10):
            RateLimiter.check("template1", "function1", max_per_second=10)
        
        # Wait for refill
        time.sleep(0.2)
        
        # Should allow more calls
        result = RateLimiter.check("template1", "function1", max_per_second=10)
        assert result is True
    
    def test_check_different_identifiers_separate_limits(self):
        """Test different identifiers have separate limits."""
        # Use up template1's limit
        for i in range(10):
            RateLimiter.check("template1", "function1", max_per_second=10)
        
        # template2 should still have full limit
        result = RateLimiter.check("template2", "function1", max_per_second=10)
        assert result is True
    
    def test_check_different_operations_separate_limits(self):
        """Test different operations have separate limits."""
        # Use up function1's limit
        for i in range(10):
            RateLimiter.check("template1", "function1", max_per_second=10)
        
        # function2 should still have full limit
        result = RateLimiter.check("template1", "function2", max_per_second=10)
        assert result is True
    
    def test_get_call_count(self):
        """Test call count is tracked."""
        for i in range(5):
            RateLimiter.check("template1", "function1", max_per_second=10)
        
        count = RateLimiter.get_call_count("template1", "function1")
        assert count == 5
    
    def test_reset_specific_identifier(self):
        """Test resetting specific identifier."""
        RateLimiter.check("template1", "function1", max_per_second=10)
        RateLimiter.check("template2", "function1", max_per_second=10)
        
        RateLimiter.reset("template1")
        
        # template1 should be reset
        count1 = RateLimiter.get_call_count("template1", "function1")
        assert count1 == 0
        
        # template2 should still exist
        count2 = RateLimiter.get_call_count("template2", "function1")
        assert count2 == 1
    
    def test_reset_all(self):
        """Test resetting all identifiers."""
        RateLimiter.check("template1", "function1", max_per_second=10)
        RateLimiter.check("template2", "function1", max_per_second=10)
        
        RateLimiter.reset()
        
        count1 = RateLimiter.get_call_count("template1", "function1")
        count2 = RateLimiter.get_call_count("template2", "function1")
        assert count1 == 0
        assert count2 == 0
    
    def test_cleanup_removes_stale_entries(self):
        """Test cleanup removes old entries."""
        # Reset first
        RateLimiter.reset()
        
        # Mock time in the security module
        with patch('ankidroid_js_api.security.time.time') as mock_time:
            # Create entry at time 1000
            current = 1000.0
            mock_time.return_value = current
            
            # Force _last_cleanup to be current time
            RateLimiter._last_cleanup = current
            
            # Create first entry
            RateLimiter.check("template1", "function1", max_per_second=10)
            assert RateLimiter.get_call_count("template1", "function1") == 1
            
            # Advance time by more than stale threshold (3600s) + cleanup interval (300s)
            mock_time.return_value = current + 4000
            
            # Trigger cleanup with new call (cleanup runs when now - _last_cleanup > 300)
            RateLimiter.check("template2", "function2", max_per_second=10)
            
            # Old entry should be cleaned up (last_refill was 4000s ago)
            count = RateLimiter.get_call_count("template1", "function1")
            assert count == 0


class TestSanitizeForLogging:
    """Test sanitize_for_logging function."""
    
    def test_sanitize_text_field(self):
        """Test text field is redacted."""
        data = '{"text":"sensitive data"}'
        result = sanitize_for_logging(data)
        assert "sensitive data" not in result
        assert "[REDACTED]" in result
    
    def test_sanitize_query_field(self):
        """Test query field is redacted."""
        data = '{"query":"private search"}'
        result = sanitize_for_logging(data)
        assert "private search" not in result
        assert "[REDACTED]" in result
    
    def test_sanitize_tags_field(self):
        """Test tags field is redacted."""
        data = '{"tags":["secret","private"]}'
        result = sanitize_for_logging(data)
        assert "secret" not in result
        assert "private" not in result
        assert "[REDACTED]" in result
    
    def test_sanitize_file_paths(self):
        """Test file paths are stripped to filename only."""
        data = 'File "C:/Users/Name/Documents/script.py"'
        result = sanitize_for_logging(data)
        assert "C:/Users/Name/Documents/" not in result
        assert "script.py" in result
    
    def test_sanitize_truncates_long_strings(self):
        """Test long strings are truncated."""
        data = "A" * 500
        result = sanitize_for_logging(data, max_length=100)
        assert len(result) <= 103  # 100 + "..."
        assert result.endswith("...")
    
    def test_sanitize_non_string_input(self):
        """Test non-string input is converted."""
        data = {"key": "value"}
        result = sanitize_for_logging(data)
        assert isinstance(result, str)
    
    def test_sanitize_empty_string(self):
        """Test empty string is handled."""
        result = sanitize_for_logging("")
        assert result == ""
    
    def test_sanitize_preserves_safe_data(self):
        """Test safe data is preserved."""
        data = "Safe log message without PII"
        result = sanitize_for_logging(data)
        assert "Safe log message" in result


class TestGenerateTemplateHash:
    """Test generate_template_hash function."""
    
    def test_hash_is_consistent(self):
        """Test same input produces same hash."""
        template = "<div>{{Front}}</div>"
        hash1 = generate_template_hash(template)
        hash2 = generate_template_hash(template)
        assert hash1 == hash2
    
    def test_hash_is_different_for_different_inputs(self):
        """Test different inputs produce different hashes."""
        template1 = "<div>{{Front}}</div>"
        template2 = "<div>{{Back}}</div>"
        hash1 = generate_template_hash(template1)
        hash2 = generate_template_hash(template2)
        assert hash1 != hash2
    
    def test_hash_length(self):
        """Test hash is SHA-256 (64 hex characters)."""
        template = "<div>{{Front}}</div>"
        hash_result = generate_template_hash(template)
        assert len(hash_result) == 64
        assert all(c in '0123456789abcdef' for c in hash_result)
    
    def test_hash_empty_string(self):
        """Test hash of empty string."""
        hash_result = generate_template_hash("")
        assert len(hash_result) == 64
    
    def test_hash_unicode(self):
        """Test hash handles unicode correctly."""
        template = "<div>日本語</div>"
        hash_result = generate_template_hash(template)
        assert len(hash_result) == 64
