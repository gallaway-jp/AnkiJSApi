# Third-Party Library Usage and License Compliance Review

**Date:** December 27, 2025  
**Project:** AnkiDroid JS API Desktop  
**Project License:** MIT License  
**Reviewed By:** Automated License Compliance Scan

---

## Executive Summary

This document provides a comprehensive review of all third-party dependencies used in the AnkiDroid JS API Desktop project, their licenses, and compliance requirements.

**Status:** ✅ **COMPLIANT** - All dependencies are compatible with MIT license

---

## 1. Runtime Dependencies

### 1.1 Anki Desktop (Host Application)

**Package:** `anki`, `aqt` (Anki Qt Application)  
**License:** AGPL-3.0  
**Usage:** Host application that loads this add-on  
**Compliance Status:** ✅ **COMPLIANT**

**Analysis:**
- This add-on is a plugin/extension for Anki Desktop
- Add-ons that extend Anki are NOT required to be AGPL-licensed
- As per Anki's plugin policy, add-ons can use any license
- Our MIT license is acceptable for Anki add-ons
- We do NOT distribute Anki; users install it separately
- We only use Anki's public API hooks and interfaces

**No Action Required**

---

### 1.2 Python Standard Library

**Modules Used:**
- `json` - JSON encoding/decoding
- `re` - Regular expressions
- `typing` - Type hints
- `subprocess` - Process management (for TTS)
- `platform` - Platform detection
- `shutil` - Shell utilities
- `abc` - Abstract base classes
- `collections` - Container datatypes
- `pathlib` - Object-oriented filesystem paths
- `functools` - Higher-order functions
- `time` - Time access and conversions
- `hashlib` - Secure hashes and message digests

**License:** Python Software Foundation License (PSF)  
**Compliance Status:** ✅ **COMPLIANT**

**Analysis:**
- PSF license is permissive and compatible with MIT
- No attribution requirements for standard library
- Python itself is not distributed with this project

**No Action Required**

---

## 2. Development Dependencies

All development dependencies are used only for testing, code quality, and documentation. They are NOT included in the distributed add-on package.

### 2.1 Testing Framework

#### pytest (>=7.0.0)
- **License:** MIT
- **Purpose:** Test framework
- **Compliance:** ✅ Compatible with MIT

#### pytest-cov (>=4.0.0)
- **License:** MIT
- **Purpose:** Code coverage plugin for pytest
- **Compliance:** ✅ Compatible with MIT

#### pytest-mock (>=3.10.0)
- **License:** MIT
- **Purpose:** Mocking plugin for pytest
- **Compliance:** ✅ Compatible with MIT

#### pytest-benchmark (>=5.0.0)
- **License:** BSD-2-Clause
- **Purpose:** Benchmarking plugin for pytest
- **Compliance:** ✅ Compatible with MIT

#### pytest-xdist (>=3.0.0)
- **License:** MIT
- **Purpose:** Parallel test execution
- **Compliance:** ✅ Compatible with MIT

#### hypothesis (>=6.0.0)
- **License:** Mozilla Public License 2.0 (MPL-2.0)
- **Purpose:** Property-based testing
- **Compliance:** ✅ Compatible with MIT (file-level copyleft)

---

### 2.2 Code Quality Tools

#### black (>=22.0.0)
- **License:** MIT
- **Purpose:** Code formatter
- **Compliance:** ✅ Compatible with MIT

#### mypy (>=0.990)
- **License:** MIT
- **Purpose:** Static type checker
- **Compliance:** ✅ Compatible with MIT

#### pylint (>=2.15.0)
- **License:** GPL-2.0
- **Purpose:** Code linter
- **Compliance:** ✅ Compatible (dev-only tool)
- **Note:** GPL tools used during development don't affect project license

#### flake8 (>=6.0.0)
- **License:** MIT
- **Purpose:** Style guide enforcement
- **Compliance:** ✅ Compatible with MIT

---

### 2.3 Documentation Tools

#### sphinx (>=5.0.0)
- **License:** BSD-2-Clause
- **Purpose:** Documentation generator
- **Compliance:** ✅ Compatible with MIT

#### sphinx-rtd-theme (>=1.0.0)
- **License:** MIT
- **Purpose:** Read the Docs theme for Sphinx
- **Compliance:** ✅ Compatible with MIT

---

### 2.4 Build and Distribution Tools

#### setuptools (>=65.0.0)
- **License:** MIT
- **Purpose:** Build system
- **Compliance:** ✅ Compatible with MIT

#### wheel (>=0.38.0)
- **License:** MIT
- **Purpose:** Python wheel packaging
- **Compliance:** ✅ Compatible with MIT

#### twine (>=4.0.0)
- **License:** Apache-2.0
- **Purpose:** PyPI package upload utility
- **Compliance:** ✅ Compatible with MIT

---

## 3. License Compatibility Matrix

| License Type | Compatible with MIT? | Notes |
|-------------|---------------------|-------|
| MIT | ✅ Yes | Same license |
| BSD-2-Clause | ✅ Yes | Permissive, similar to MIT |
| Apache-2.0 | ✅ Yes | Permissive, includes patent grant |
| PSF (Python) | ✅ Yes | Permissive |
| MPL-2.0 | ✅ Yes | File-level copyleft, compatible |
| GPL-2.0 | ✅ Yes* | *Only for dev tools, not distributed |
| AGPL-3.0 | ✅ Yes* | *Plugin architecture exemption |

---

## 4. Distribution Analysis

### What Gets Distributed?

The `.ankiaddon` package includes:
- ✅ Source code files (`.py`)
- ✅ JavaScript files (`.js`)
- ✅ JSON configuration files
- ✅ HTML test templates
- ❌ NO third-party libraries
- ❌ NO development dependencies
- ❌ NO test files

**Conclusion:** The distributed package contains ONLY original code licensed under MIT.

---

## 5. Compliance Requirements

### 5.1 Current Requirements ✅

As an MIT-licensed project with no bundled dependencies:

1. **Include License File** ✅
   - [LICENSE](../LICENSE) file present in repository
   - Contains full MIT license text
   - Copyright year and holder specified

2. **License Headers** ⚠️ **OPTIONAL**
   - Not currently present in source files
   - MIT license does not require headers
   - Recommended for clarity (see Section 6)

3. **Attribution** ✅
   - No third-party code requiring attribution in distributed package
   - Development tools don't require attribution

4. **Anki Add-on Compliance** ✅
   - Add-on can use any license per Anki policy
   - No AGPL infection for plugins
   - Uses only public API

---

### 5.2 Recommendations

#### Priority: MEDIUM - Add License Headers

While not legally required for MIT, adding SPDX license identifiers to source files is a best practice:

```python
# SPDX-License-Identifier: MIT
# Copyright (c) 2025 AnkiDroid JS API Desktop Contributors
```

**Benefits:**
- Clarifies licensing at file level
- Helps automated license scanners
- Industry standard practice
- Minimal overhead

#### Priority: LOW - Create NOTICE File

Consider adding a `NOTICE` file acknowledging:
- Anki Desktop as the host platform
- Development tool credits (optional)

**Example:**
```
AnkiDroid JS API Desktop
Copyright (c) 2025 AnkiDroid JS API Desktop Contributors

This software is designed as an add-on for Anki Desktop.
Anki is Copyright © Ankitects Pty Ltd and contributors.
Licensed under the AGPL-3.0 license.

For development tool credits, see requirements-dev.txt
```

#### Priority: LOW - Document Anki Compatibility

Add a section to README explaining:
- Compatible Anki versions
- That Anki must be installed separately
- Link to Anki's license

---

## 6. Risk Assessment

### License Risk Level: **LOW** ✅

**Factors:**
1. ✅ Using permissive licenses (MIT, BSD, Apache)
2. ✅ No copyleft library dependencies in distribution
3. ✅ Clear separation of dev tools from production code
4. ✅ Plugin architecture avoids AGPL concerns
5. ✅ No bundled third-party code

### Potential Future Risks: **MEDIUM** ⚠️

**Watch For:**
- ⚠️ Adding runtime dependencies with different licenses
- ⚠️ Copying code from GPL/AGPL projects
- ⚠️ Using proprietary TTS engines
- ⚠️ Incorporating third-party JavaScript libraries

**Mitigation:**
- Review license before adding any dependency
- Use tools like `pip-licenses` in CI/CD
- Document all third-party code sources
- Maintain this compliance document

---

## 7. Action Items

### Immediate (Optional but Recommended)

- [ ] Add SPDX license identifiers to Python source files
- [ ] Create NOTICE file with Anki acknowledgment
- [ ] Add "License" section to README
- [ ] Add license badge to README: `[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)`

### For Future Releases

- [ ] Run `pip-licenses` before each release
- [ ] Update this document when adding dependencies
- [ ] Scan for code copied from other sources
- [ ] Review any JavaScript libraries used

### Automated Checks (Recommended for CI/CD)

```bash
# Check licenses of all dependencies
pip install pip-licenses
pip-licenses --format=markdown --output-file=docs/dependency-licenses.md

# Scan for license headers
# (Use tools like licenseheaders or reuse)
```

---

## 8. External Resources

### License Texts
- **MIT License:** https://opensource.org/licenses/MIT
- **AGPL-3.0:** https://www.gnu.org/licenses/agpl-3.0.html
- **Apache-2.0:** https://www.apache.org/licenses/LICENSE-2.0

### Compatibility References
- **GPL Compatibility:** https://www.gnu.org/licenses/license-compatibility.html
- **MIT Compatibility:** https://opensource.stackexchange.com/questions/1640/
- **Anki Add-on License Policy:** Anki allows add-ons to use any license

### Tools
- **pip-licenses:** https://github.com/raimon49/pip-licenses
- **SPDX:** https://spdx.dev/
- **REUSE:** https://reuse.software/

---

## 9. Conclusion

**The AnkiDroid JS API Desktop project is fully compliant with all applicable license requirements.**

- ✅ Project license (MIT) is clearly specified
- ✅ No conflicting licenses in runtime dependencies
- ✅ Development dependencies properly separated
- ✅ No bundled third-party code requiring attribution
- ✅ Anki add-on architecture is compatible with MIT license

**Overall Risk Level:** LOW ✅

**Recommended Next Steps:**
1. Add SPDX identifiers to source files (optional but recommended)
2. Create NOTICE file (optional)
3. Set up automated license checking in CI/CD (recommended)
4. Keep this document updated when dependencies change

---

**Document Version:** 1.0  
**Last Updated:** December 27, 2025  
**Next Review:** When adding new dependencies or before major releases
