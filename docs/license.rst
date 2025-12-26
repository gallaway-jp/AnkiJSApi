.. _license:

License Information
===================

Project License
---------------

AnkiDroid JS API Desktop is licensed under the **MIT License**.

MIT License Text
~~~~~~~~~~~~~~~~

.. code-block:: text

   MIT License

   Copyright (c) 2025 AnkiDroid JS API Desktop Contributors

   Permission is hereby granted, free of charge, to any person obtaining a copy
   of this software and associated documentation files (the "Software"), to deal
   in the Software without restriction, including without limitation the rights
   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   copies of the Software, and to permit persons to whom the Software is
   furnished to do so, subject to the following conditions:

   The above copyright notice and this permission notice shall be included in all
   copies or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
   SOFTWARE.

What This Means
~~~~~~~~~~~~~~~

The MIT License is a permissive open-source license that allows you to:

- ✅ **Use** this software for any purpose (commercial or personal)
- ✅ **Modify** the source code to suit your needs
- ✅ **Distribute** original or modified versions
- ✅ **Sublicense** under different terms
- ✅ **Sell** copies or derivatives

**Requirements:**

- Include the copyright notice and license text in all copies
- No warranty is provided

SPDX Identifier
~~~~~~~~~~~~~~~

All source files in this project include the SPDX license identifier:

.. code-block:: python

   # SPDX-License-Identifier: MIT

This provides a standardized way to identify the license programmatically.

Third-Party Dependencies
-------------------------

Anki Desktop
~~~~~~~~~~~~

**License:** AGPL-3.0  
**Relationship:** Host application

This add-on is a plugin/extension for Anki Desktop:

- **Anki is NOT distributed with this software**
- Users must install Anki separately from `AnkiWeb <https://apps.ankiweb.net/>`_
- Per Anki's plugin policy, add-ons may use any license
- This add-on is **NOT** subject to Anki's AGPL license
- We only use Anki's public API hooks and interfaces

**Compliance Status:** ✅ **COMPLIANT**

.. note::
   Anki Desktop must be installed separately. This add-on cannot function without it.

Python Standard Library
~~~~~~~~~~~~~~~~~~~~~~~

**License:** Python Software Foundation License (PSF)  
**Compliance:** ✅ Compatible with MIT

Modules used:

- ``json`` - JSON encoding/decoding
- ``re`` - Regular expressions
- ``typing`` - Type hints
- ``subprocess`` - Process management (for TTS)
- ``platform`` - Platform detection
- ``pathlib`` - Filesystem paths
- ``functools`` - Higher-order functions
- ``time`` - Time utilities
- ``hashlib`` - Secure hashing

**No attribution required** for Python Standard Library.

Development Dependencies
------------------------

These tools are used only during development and testing. They are **NOT** included in the distributed add-on package.

Testing Framework
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Package
     - License
     - Purpose
   * - pytest
     - MIT
     - Test framework
   * - pytest-cov
     - MIT
     - Code coverage plugin
   * - pytest-mock
     - MIT
     - Mocking plugin
   * - pytest-benchmark
     - BSD-2-Clause
     - Benchmarking plugin
   * - pytest-xdist
     - MIT
     - Parallel test execution

Code Quality Tools
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Package
     - License
     - Purpose
   * - black
     - MIT
     - Code formatter
   * - mypy
     - MIT
     - Type checker
   * - pylint
     - GPL-2.0
     - Code linter
   * - flake8
     - MIT
     - Style checker

Documentation Tools
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Package
     - License
     - Purpose
   * - sphinx
     - BSD-2-Clause
     - Documentation generator
   * - sphinx-rtd-theme
     - MIT
     - Read the Docs theme

**All development dependencies are compatible with MIT License.**

License Compliance
------------------

Compliance Status
~~~~~~~~~~~~~~~~~

✅ **FULLY COMPLIANT** - All dependencies are compatible with the MIT License.

SPDX Headers
~~~~~~~~~~~~

All Python source files include SPDX license headers:

.. code-block:: python

   # SPDX-FileCopyrightText: 2025 AnkiDroid JS API Desktop Contributors
   # SPDX-License-Identifier: MIT

This follows the `REUSE <https://reuse.software/>`_ specification for license compliance.

Automated Compliance Checking
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

License compliance is verified through:

1. **CI/CD Pipeline** - Automated license header checks on every commit
2. **SPDX Validation** - All files have proper SPDX identifiers
3. **Dependency Scanning** - Development dependencies verified for compatibility

See the ``.github/workflows/license-check.yml`` for automated compliance verification.

Full Compliance Report
~~~~~~~~~~~~~~~~~~~~~~

For a detailed analysis of all third-party dependencies, see:

- `LICENSE_COMPLIANCE.md <https://github.com/gallaway-jp/AnkiJSApi/blob/main/docs/LICENSE_COMPLIANCE.md>`_
- `NOTICE <https://github.com/gallaway-jp/AnkiJSApi/blob/main/NOTICE>`_ file

Redistribution Guidelines
--------------------------

If You Redistribute This Software
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When redistributing this software (original or modified), you must:

1. **Include** the LICENSE file
2. **Include** the NOTICE file
3. **Preserve** copyright notices
4. **State** any changes you made (for modified versions)

Example Attribution
~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   This software includes AnkiDroid JS API Desktop
   Copyright (c) 2025 AnkiDroid JS API Desktop Contributors
   Licensed under the MIT License

If You Use This in Your Project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you incorporate this code into your own project:

- Include the license text in your distribution
- Provide attribution to the original authors
- You may license your derivative work under different terms
- No requirement to open-source your modifications (MIT is permissive)

Commercial Use
--------------

Is Commercial Use Allowed?
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Yes!** The MIT License explicitly permits commercial use.

You may:

- Use this software in commercial products
- Sell software that includes this code
- Offer commercial services using this software

**Requirements:**

- Include the MIT license text
- Provide attribution to original authors
- No warranty is provided

Contributing
------------

License Agreement
~~~~~~~~~~~~~~~~~

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

Contributor Rights
~~~~~~~~~~~~~~~~~~

- You retain copyright to your contributions
- You grant the project a license to use your contributions under MIT
- You certify you have the right to submit the contribution

See :ref:`contributing` for detailed contribution guidelines.

Questions?
----------

License Questions
~~~~~~~~~~~~~~~~~

If you have questions about licensing:

- Review the full `LICENSE <https://github.com/gallaway-jp/AnkiJSApi/blob/main/LICENSE>`_ file
- Read the `LICENSE_COMPLIANCE.md <https://github.com/gallaway-jp/AnkiJSApi/blob/main/docs/LICENSE_COMPLIANCE.md>`_ document
- Open an issue on `GitHub <https://github.com/gallaway-jp/AnkiJSApi/issues>`_

.. note::
   This page is for informational purposes. The LICENSE file is the authoritative source for license terms.
