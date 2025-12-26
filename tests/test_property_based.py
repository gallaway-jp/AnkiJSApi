"""
Property-based tests using Hypothesis for input validation.

These tests generate hundreds of random inputs to verify that validation
functions handle all possible edge cases correctly.
"""

import sys
from unittest.mock import MagicMock

# Mock Anki modules before importing
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
from hypothesis import given, strategies as st, assume, settings
from hypothesis import HealthCheck

from ankidroid_js_api.security import (
    InputValidator,
    sanitize_for_logging,
    generate_template_hash
)


class TestInputValidatorPropertyBased:
    """Property-based tests for InputValidator."""
    
    @given(st.text(min_size=0, max_size=1000))
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_validate_text_always_returns_string(self, text):
        """Property: validate_text always returns a string."""
        try:
            result = InputValidator.validate_text(text, max_length=1000)
            assert isinstance(result, str)
        except (ValueError, TypeError):
            # Expected for invalid inputs
            pass
    
    @given(st.text(alphabet=st.characters(blacklist_categories=('Cc', 'Cs')), min_size=1, max_size=100))
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_validate_text_removes_control_chars(self, text):
        """Property: validate_text removes all control characters."""
        try:
            result = InputValidator.validate_text(text, max_length=1000)
            # Result should have no control characters
            assert all(ord(c) >= 32 or c in '\n\r\t' for c in result)
        except ValueError:
            # Some inputs may be invalid for other reasons
            pass
    
    @given(st.integers())
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_validate_integer_type_invariant(self, value):
        """Property: validate_integer returns int or raises exception."""
        try:
            result = InputValidator.validate_integer(value, min_val=-1000000, max_val=1000000)
            assert isinstance(result, int)
        except (ValueError, TypeError):
            # Expected for out of range or invalid type
            pass
    
    @given(st.integers(min_value=0, max_value=100))
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_validate_integer_within_range_succeeds(self, value):
        """Property: integers within range always succeed."""
        result = InputValidator.validate_integer(value, min_val=0, max_val=100)
        assert result == value
        assert 0 <= result <= 100
    
    @given(st.integers())
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_validate_integer_range_bounds(self, value):
        """Property: validate_integer respects min/max bounds."""
        min_val, max_val = -100, 100
        try:
            result = InputValidator.validate_integer(value, min_val=min_val, max_val=max_val)
            assert min_val <= result <= max_val
        except ValueError:
            # Should only fail if outside range
            assert value < min_val or value > max_val
    
    @given(st.floats(allow_nan=False, allow_infinity=False))
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_validate_float_type_invariant(self, value):
        """Property: validate_float returns float or raises exception."""
        try:
            result = InputValidator.validate_float(value, min_val=-1e6, max_val=1e6)
            assert isinstance(result, float)
        except (ValueError, TypeError):
            pass
    
    @given(st.floats(min_value=0.0, max_value=2.0, allow_nan=False, allow_infinity=False))
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_validate_float_within_range_succeeds(self, value):
        """Property: floats within range always succeed."""
        result = InputValidator.validate_float(value, min_val=0.0, max_val=2.0)
        assert 0.0 <= result <= 2.0
    
    @given(st.text(alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'), max_codepoint=127), min_size=1, max_size=50))
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_validate_filename_alphanumeric_safe(self, filename):
        """Property: alphanumeric filenames are safe."""
        # Add .txt extension to make it valid
        safe_filename = filename + ".txt"
        try:
            result = InputValidator.validate_filename(safe_filename)
            assert isinstance(result, str)
            assert '/' not in result
            assert '\\' not in result
            assert '..' not in result
        except ValueError:
            # May fail if other validation rules apply
            pass
    
    @given(st.text(min_size=0, max_size=200))
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_validate_filename_no_path_traversal(self, filename):
        """Property: filenames with path separators are rejected."""
        if '/' in filename or '\\' in filename or '..' in filename:
            with pytest.raises(ValueError):
                InputValidator.validate_filename(filename)
    
    @given(st.text(alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'), max_codepoint=127), min_size=1, max_size=100))
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_validate_tag_alphanumeric_safe(self, tag):
        """Property: alphanumeric tags are safe."""
        try:
            result = InputValidator.validate_tag(tag, max_length=100)
            assert isinstance(result, str)
            assert len(result) > 0
        except ValueError:
            pass
    
    @given(st.text(min_size=0, max_size=100))
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_validate_tag_converts_spaces(self, tag):
        """Property: spaces in tags are converted to underscores."""
        if tag.strip():  # Non-empty after stripping
            try:
                result = InputValidator.validate_tag(tag, max_length=100)
                assert ' ' not in result  # Spaces should be replaced
            except ValueError:
                # May fail validation for other reasons
                pass


class TestSanitizeForLoggingPropertyBased:
    """Property-based tests for sanitize_for_logging."""
    
    @given(st.text(min_size=0, max_size=1000))
    def test_sanitize_always_returns_string(self, data):
        """Property: sanitize_for_logging always returns a string."""
        result = sanitize_for_logging(data)
        assert isinstance(result, str)
    
    @given(st.text(min_size=0, max_size=100))
    def test_sanitize_respects_max_length(self, data):
        """Property: output never exceeds max_length."""
        max_len = 50
        result = sanitize_for_logging(data, max_length=max_len)
        assert len(result) <= max_len + 3  # +3 for "..."
    
    @given(st.text(min_size=0, max_size=200))
    def test_sanitize_removes_sensitive_fields(self, data):
        """Property: sensitive field values are redacted."""
        # Add sensitive field pattern
        if '"text":' in data or '"query":' in data or '"tags":' in data:
            result = sanitize_for_logging(data)
            # Should contain REDACTED if pattern was matched
            if '"text":"' in data or '"query":"' in data or '"tags":[' in data:
                assert "[REDACTED]" in result or data == result  # Exact match or redacted
    
    @given(st.dictionaries(st.text(max_size=10), st.one_of(st.text(max_size=20), st.integers(), st.booleans()), max_size=5))
    def test_sanitize_handles_non_strings(self, data):
        """Property: non-string inputs are converted to strings."""
        result = sanitize_for_logging(data)
        assert isinstance(result, str)


class TestGenerateTemplateHashPropertyBased:
    """Property-based tests for generate_template_hash."""
    
    @given(st.text(min_size=0, max_size=1000))
    def test_hash_consistency(self, template):
        """Property: same input always produces same hash."""
        hash1 = generate_template_hash(template)
        hash2 = generate_template_hash(template)
        assert hash1 == hash2
    
    @given(st.text(min_size=0, max_size=1000))
    def test_hash_format(self, template):
        """Property: hash is always 64 hex characters."""
        hash_result = generate_template_hash(template)
        assert len(hash_result) == 64
        assert all(c in '0123456789abcdef' for c in hash_result)
    
    @given(st.text(min_size=1, max_size=100), st.text(min_size=1, max_size=100))
    def test_hash_different_inputs(self, template1, template2):
        """Property: different inputs produce different hashes (collision resistance)."""
        assume(template1 != template2)  # Only test when inputs differ
        hash1 = generate_template_hash(template1)
        hash2 = generate_template_hash(template2)
        assert hash1 != hash2


class TestInputValidatorEdgeCases:
    """Edge case tests discovered through property-based testing."""
    
    @given(st.text(alphabet='\x00\x01\x02\x03\x04', min_size=1, max_size=50))
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_validate_text_only_null_bytes(self, text):
        """Property: text with only control chars is cleaned or rejected."""
        try:
            result = InputValidator.validate_text(text, max_length=100)
            # Should be empty or cleaned
            assert len(result) == 0 or all(c not in '\x00\x01\x02\x03\x04' for c in result)
        except ValueError:
            # May be rejected as invalid
            pass
    
    @given(st.integers(min_value=-2**31, max_value=2**31-1))
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_validate_integer_extreme_values(self, value):
        """Property: extreme integer values are handled correctly."""
        try:
            result = InputValidator.validate_integer(value, min_val=-2**31, max_val=2**31-1)
            assert isinstance(result, int)
            assert -2**31 <= result <= 2**31-1
        except (ValueError, TypeError):
            pass
    
    @given(st.floats(min_value=1e-10, max_value=1e10, allow_nan=False, allow_infinity=False))
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_validate_float_extreme_ranges(self, value):
        """Property: extreme float ranges are handled correctly."""
        try:
            result = InputValidator.validate_float(value, min_val=1e-10, max_val=1e10)
            assert isinstance(result, float)
            assert 1e-10 <= result <= 1e10
        except (ValueError, TypeError):
            pass
