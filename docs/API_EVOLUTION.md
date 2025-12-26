# API Evolution and Deprecation Policy

## Overview

This document defines how the AnkiDroid JS API evolves over time while maintaining backward compatibility and providing a smooth upgrade path for users.

---

## Versioning Strategy

### Version Format
We use [Semantic Versioning 2.0.0](https://semver.org/):

```
MAJOR.MINOR.PATCH
```

- **MAJOR**: Incompatible API changes (breaking changes)
- **MINOR**: New functionality (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Examples
- `1.0.0` → `1.0.1`: Bug fix (safe to upgrade)
- `1.0.0` → `1.1.0`: New API function (safe to upgrade)
- `1.0.0` → `2.0.0`: Breaking change (review changelog before upgrading)

---

## Compatibility Guarantees

### Within Same MAJOR Version
✅ **Guaranteed:**
- Existing API functions continue to work
- Function signatures remain unchanged
- Return value types remain consistent
- Configuration format remains compatible

❌ **Not Guaranteed:**
- Internal implementation details
- Undocumented behavior
- Performance characteristics
- Log message format

### Example
```javascript
// This will ALWAYS work in v1.x.x
const cardId = await api.ankiGetCardId();

// This might change (internal implementation)
// Don't depend on: log message format, error text, timing, etc.
```

---

## Adding New Features

### Process for New API Functions

1. **Design Phase**
   - Document function purpose and use cases
   - Choose appropriate module (card_info, card_actions, etc.)
   - Define function signature with types
   - Consider future extensibility

2. **Implementation Phase**
   ```python
   # New function in appropriate module
   def anki_new_feature(param: str) -> dict:
       """Complete docstring with examples."""
       # Implementation with validation and error handling
       pass
   ```

3. **Testing Phase**
   - Unit tests for all code paths
   - Integration tests with other functions
   - Manual testing with test deck

4. **Documentation Phase**
   - Add to README.md API list
   - Add example to test templates
   - Update CHANGELOG.md under "Added"

5. **Release**
   - Increment MINOR version (1.0.0 → 1.1.0)
   - Tag release in git
   - Publish to AnkiWeb/GitHub

### Example: Adding `ankiGetCardHistory()`

**Before (v1.2.0):**
```python
# card_info.py - Function doesn't exist
```

**After (v1.3.0):**
```python
# card_info.py
def anki_get_card_history(limit: int = 10) -> list:
    """Get review history for current card.
    
    Added in: v1.3.0
    
    Args:
        limit: Maximum number of reviews to return (default: 10)
        
    Returns:
        list: Review history entries [{id, ease, time, ...}]
    """
    # Implementation
```

**CHANGELOG.md:**
```markdown
## [1.3.0] - 2025-XX-XX
### Added
- New API function: `ankiGetCardHistory()` - retrieve review history
```

---

## Deprecation Process

### When to Deprecate
- Function has better alternative
- Security vulnerability cannot be fixed without breaking change
- Anki internals changed, making function obsolete

### Deprecation Timeline

```
Version N: Announce deprecation
  ↓ (maintain for at least 6 months or 2 minor versions)
Version N+2: Mark as deprecated in code
  ↓ (maintain for at least 6 months or 2 minor versions)
Version N+4 (or MAJOR): Remove function
```

### Example Timeline

**v1.5.0 (Announce):**
```markdown
## [1.5.0] - 2025-03-01
### Deprecated
- `ankiGetCardLeft()`: Use `ankiGetLrnCardCount() + ankiGetRevCardCount()` instead
  - Will be removed in v2.0.0 (estimated: 2025-09-01)
  - Reason: Confusing name, better alternatives exist
```

**v1.7.0 (Mark in Code):**
```python
def anki_get_card_left() -> int:
    """Get the number of reps left today.
    
    .. deprecated:: 1.5.0
        Use `ankiGetLrnCardCount() + ankiGetRevCardCount()` instead.
        This function will be removed in v2.0.0.
    """
    log_debug("WARNING: ankiGetCardLeft is deprecated, use ankiGetLrnCardCount + ankiGetRevCardCount")
    # Original implementation
```

**v2.0.0 (Remove):**
```python
# Function removed entirely
# Users must migrate to new API
```

---

## Breaking Changes

### When Breaking Changes Are Acceptable
- MAJOR version increment only (1.x.x → 2.0.0)
- After deprecation period (minimum 6 months)
- When security requires it (emergency exception)

### Communicating Breaking Changes

**CHANGELOG.md:**
```markdown
## [2.0.0] - 2025-09-01

### BREAKING CHANGES
- **Removed**: `ankiGetCardLeft()` - Use `ankiGetLrnCardCount() + ankiGetRevCardCount()`
- **Changed**: `ankiToggleFlag()` now returns `{success: bool, flag: int}` instead of `bool`
  - Migration: Check `result.success` instead of `result`
  
### Migration Guide
See docs/MIGRATION_v1_to_v2.md for detailed upgrade instructions.
```

**Migration Document:**
```markdown
# Migrating from v1.x to v2.0

## Removed Functions
| Old Function | Replacement |
|--------------|-------------|
| `ankiGetCardLeft()` | `ankiGetLrnCardCount() + ankiGetRevCardCount()` |

## Changed Return Values
| Function | Old Return | New Return |
|----------|-----------|------------|
| `ankiToggleFlag()` | `bool` | `{success: bool, flag: int}` |

## Code Examples
### Before (v1.x)
```javascript
const left = await api.ankiGetCardLeft();
const success = await api.ankiToggleFlag("red");
```

### After (v2.0)
```javascript
const lrnCount = await api.ankiGetLrnCardCount();
const revCount = await api.ankiGetRevCardCount();
const left = lrnCount + revCount;

const result = await api.ankiToggleFlag("red");
if (result.success) {
    console.log(`Flag set to: ${result.flag}`);
}
```
```

---

## Configuration Evolution

### Adding New Configuration Options

**Backward Compatible (MINOR version):**
```json
{
    "existing_option": true,
    "new_option": {
        "_comment": "Added in v1.4.0",
        "enabled": true
    }
}
```

**Code handles missing option gracefully:**
```python
config = get_config()
new_feature_enabled = config.get("new_option", {}).get("enabled", True)  # Default if missing
```

### Changing Configuration Format (MAJOR version)

**Before (v1.x):**
```json
{
    "debug": true,
    "logging": true
}
```

**After (v2.0):**
```json
{
    "debug": {
        "enabled": true,
        "level": "INFO"
    },
    "logging": {
        "api_calls": true,
        "performance": false
    }
}
```

**Migration code:**
```python
def migrate_config_v1_to_v2(old_config: dict) -> dict:
    """Migrate v1 config to v2 format."""
    new_config = {
        "debug": {
            "enabled": old_config.get("debug", False),
            "level": "INFO"
        },
        "logging": {
            "api_calls": old_config.get("logging", False),
            "performance": False
        }
    }
    return new_config
```

---

## Anki Compatibility

### Supporting Multiple Anki Versions

**Feature Detection (Preferred):**
```python
def show_answer_safe():
    """Show answer with compatibility across Anki versions."""
    if hasattr(mw.reviewer, 'on_show_answer'):
        mw.reviewer.on_show_answer()  # Anki 2.1.55+
    elif hasattr(mw.reviewer, '_showAnswer'):
        mw.reviewer._showAnswer()  # Anki 2.1.50-2.1.54
    else:
        raise RuntimeError("Unsupported Anki version")
```

**Version Checking (Avoid if possible):**
```python
from aqt.utils import pointVersion

def get_anki_version() -> tuple:
    """Get Anki version as (major, minor, patch)."""
    version = pointVersion()
    return tuple(map(int, version.split('.')))

# Only use for major incompatibilities
if get_anki_version() >= (2, 1, 55):
    # New API
else:
    # Legacy API
```

### Dropping Support for Old Anki Versions

**Timeline:**
- Support Anki versions for at least 1 year after release
- Announce in CHANGELOG before dropping support
- Only drop in MAJOR version increment

**Example:**
```markdown
## [2.0.0] - 2025-09-01
### BREAKING CHANGES
- **Dropped support**: Anki < 2.1.50
  - Last version supporting Anki 2.1.49: v1.9.0
  - Upgrade to Anki 2.1.50+ or stay on add-on v1.9.0
```

---

## API Stability Levels

### Stable APIs
- Listed in README.md
- Guaranteed backward compatibility within MAJOR version
- Follow deprecation process before removal

**Example:** `ankiGetCardId()`, `ankiMarkCard()`, `ankiTtsSpeak()`

### Experimental APIs
- Prefixed with `experimental_` or marked in docs
- May change without notice
- Not recommended for production use

**Example:**
```python
def experimental_get_card_stats_v2() -> dict:
    """Experimental API - may change without notice.
    
    .. warning::
        This API is experimental and may change in any version.
        Do not use in production card templates.
    """
    pass
```

### Internal APIs
- Prefixed with `_` (underscore)
- Not documented in README.md
- No compatibility guarantees

**Example:** `_send_callback()`, `_cleanup_stale_entries()`

---

## User Communication

### Where to Announce Changes

1. **CHANGELOG.md** - Required for all changes
2. **GitHub Releases** - Tag releases with notes
3. **AnkiWeb Description** - Highlight major changes
4. **In-App Notifications** - For critical updates (if applicable)

### Release Notes Template

```markdown
## [1.4.0] - 2025-06-15

### Added
- New API: `ankiGetCardHistory()` - retrieve review history (#42)
- Configuration option: `cache_enabled` for performance (#45)

### Changed
- Improved error messages in TTS functions (#43)
- Updated default toast duration to 3000ms (#44)

### Deprecated
- `ankiGetCardLeft()` - use `ankiGetLrnCardCount() + ankiGetRevCardCount()` instead
  - Will be removed in v2.0.0 (estimated: 2025-12-01)

### Fixed
- Rate limiter memory leak on long sessions (#41)
- TTS crash on empty text (#40)

### Security
- Added stricter input validation for search queries (#46)

---

**Full Changelog**: https://github.com/user/repo/compare/v1.3.0...v1.4.0
```

---

## Testing Strategy for Evolution

### Compatibility Tests

**Test with multiple Anki versions:**
```python
# tests/test_compatibility.py
@pytest.mark.parametrize("anki_version", ["2.1.50", "2.1.55", "25.07.5"])
def test_show_answer_compatibility(anki_version, mock_mw):
    """Test show_answer works across Anki versions."""
    # Mock appropriate method for version
    # Test function still works
```

### Deprecation Tests

**Ensure deprecated functions still work:**
```python
def test_deprecated_function_still_works():
    """Deprecated function should work but log warning."""
    with pytest.warns(DeprecationWarning):
        result = anki_get_card_left()
        assert isinstance(result, int)
```

### Migration Tests

**Test v1 → v2 migrations:**
```python
def test_config_migration_v1_to_v2():
    """Test config migration from v1 to v2."""
    v1_config = {"debug": True, "logging": False}
    v2_config = migrate_config_v1_to_v2(v1_config)
    
    assert v2_config["debug"]["enabled"] == True
    assert v2_config["logging"]["api_calls"] == False
```

---

## FAQ

**Q: How long should we support deprecated features?**
A: Minimum 6 months or 2 minor versions, whichever is longer.

**Q: Can we fix bugs in deprecated functions?**
A: Yes, security fixes always. Other bugs: evaluate case-by-case.

**Q: What if Anki makes a breaking change?**
A: Create compatibility layer if possible. If not, increment MAJOR version.

**Q: How to handle AnkiDroidJS API updates?**
A: Review changes, update `__api_version__`, test thoroughly, document differences.

**Q: Should we version the JavaScript API separately?**
A: No, keep in sync with Python add-on version for simplicity.

---

*Last updated: December 26, 2025*
*Review this policy annually and update based on lessons learned.*
