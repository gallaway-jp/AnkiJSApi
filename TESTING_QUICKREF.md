# Quick Reference: Testing Commands

## 🚀 Common Commands

### Run All Tests
```bash
pytest tests/ -v
```

### Run with Coverage
```bash
pytest tests/ --cov=src/ankidroid_js_api --cov-report=html
```

### Run Specific Test Types
```bash
# Unit tests only (skip benchmarks)
pytest tests/ -k "not benchmark"

# Security tests only  
pytest tests/test_security.py -v

# Property-based tests
pytest tests/test_property_based.py --hypothesis-show-statistics

# Benchmarks only
pytest tests/test_benchmarks.py --benchmark-only
```

### Fast Execution
```bash
# Parallel execution
pytest tests/ -n auto

# Stop on first failure
pytest tests/ -x

# Quiet mode
pytest tests/ -q
```

### Coverage Reports
```bash
# HTML report
pytest tests/ --cov=src/ankidroid_js_api --cov-report=html
# Then open: htmlcov/index.html

# Terminal report with missing lines
pytest tests/ --cov=src/ankidroid_js_api --cov-report=term-missing
```

### Performance Testing
```bash
# Run benchmarks
pytest tests/test_benchmarks.py --benchmark-only

# Save benchmark baseline
pytest tests/test_benchmarks.py --benchmark-autosave

# Compare with previous
pytest tests/test_benchmarks.py --benchmark-compare
```

---

## 📊 Test Statistics

- **Total Tests**: 249
- **Unit Tests**: 206  
- **Property-Based**: 21
- **Benchmarks**: 22
- **Pass Rate**: 100%
- **Coverage**: 79%

---

## 🔍 Debugging Tests

```bash
# Show print statements
pytest tests/ -s

# Verbose output
pytest tests/ -vv

# Show local variables on failure
pytest tests/ -l

# Drop into debugger on failure
pytest tests/ --pdb
```

---

## 📁 Test Files

| File | Tests | Purpose |
|------|-------|---------|
| test_security.py | 52 | Security validation & rate limiting |
| test_property_based.py | 21 | Edge case discovery |
| test_benchmarks.py | 22 | Performance monitoring |
| test_api_bridge.py | 20 | API routing & injection |
| test_addon_package.py | 30 | Package structure |
| test_tts_control.py | 27 | Text-to-speech |
| test_card_actions.py | 13 | Card modifications |
| test_ui_control.py | 16 | UI controls |
| test_reviewer_control.py | 11 | Reviewer state |
| test_integration.py | 10 | End-to-end workflows |
| test_card_info.py | 9 | Card information |
| test_utils.py | 13 | Helper functions |
| test_tag_manager.py | 4 | Tag operations |

---

## ✅ Pre-Commit Checklist

```bash
# 1. Run all tests
pytest tests/ -v

# 2. Check coverage
pytest tests/ --cov=src/ankidroid_js_api --cov-report=term

# 3. Run benchmarks
pytest tests/test_benchmarks.py --benchmark-only

# 4. Code quality
black --check src/ tests/
isort --check-only src/ tests/
flake8 src/ tests/
```

---

**Last Updated**: December 26, 2025
