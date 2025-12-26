.. _changelog:

Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

Unreleased
----------

Added
~~~~~

- Initial implementation of AnkiDroidJS API for Anki Desktop
- Card information APIs (counts, stats, metadata)
- Card action APIs (mark, flag, bury, suspend, reset)
- Reviewer control APIs (show answer, answer with ease)
- Text-to-Speech (TTS) control APIs
- UI control APIs (night mode, toasts, scrollbars)
- Tag management APIs
- Utility APIs (network status)
- Comprehensive documentation and examples
- MIT License
- Unit test framework (258 tests)
- Build system for .ankiaddon packaging
- Sphinx HTML documentation
- License compliance documentation
- Security validation and rate limiting
- Input sanitization

Known Limitations
~~~~~~~~~~~~~~~~~

- TTS implementation uses system TTS (not AnkiDroid's specific TTS engine)
- Speech-to-Text (STT) APIs not yet implemented
- Network metered status detection approximated for desktop
- Some mobile-specific UI controls adapted for desktop context

Version 1.0.0
-------------

*To be determined*

Added
~~~~~

- First stable release
- Full API compatibility with AnkiDroidJS v0.0.3
- Comprehensive test coverage (>95%)
- Documentation and examples
- AnkiWeb publication

Fixed
~~~~~

- All known issues from unreleased version

Documentation
~~~~~~~~~~~~~

- Complete API reference
- Installation guide
- Quick start guide
- Usage guide with examples
- FAQ
- Contributing guide
- Development guide
- Architecture documentation
- Testing guide

Security
~~~~~~~~

- Input validation for all API functions
- Rate limiting to prevent abuse
- Sanitization of user-provided content
- SPDX license headers

Future Versions
---------------

Version 1.1.0 (Planned)
~~~~~~~~~~~~~~~~~~~~~~~

Planned Features
^^^^^^^^^^^^^^^^

- Custom TTS voice selection
- Enhanced STT support
- Additional card statistics APIs
- Performance optimizations
- Extended error reporting

Version 2.0.0 (Planned)
~~~~~~~~~~~~~~~~~~~~~~~

Breaking Changes
^^^^^^^^^^^^^^^^

- Potential API refinements based on user feedback
- Updated minimum Anki version requirement
- Enhanced security features

New Features
^^^^^^^^^^^^

- Advanced card manipulation APIs
- Custom JavaScript events
- Plugin system for extensions
- Enhanced debugging tools

Version History
---------------

.. list-table::
   :header-rows: 1
   :widths: 15 15 70

   * - Version
     - Date
     - Summary
   * - Unreleased
     - In Progress
     - Initial development with full API implementation
   * - 1.0.0
     - TBD
     - First stable release

Development Milestones
----------------------

Phase 1: Core Implementation ✅
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- API bridge implementation
- Core API functions
- Security layer
- Basic testing

Phase 2: Documentation ✅
~~~~~~~~~~~~~~~~~~~~~~~~~

- API reference
- User guides
- Examples
- Sphinx documentation

Phase 3: Testing & Quality ✅
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Unit tests (258 tests)
- Integration tests
- Code coverage >95%
- License compliance

Phase 4: Release Preparation 🔄
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- AnkiWeb packaging
- Final testing
- Release notes
- Community feedback

How to Contribute
-----------------

See :ref:`contributing` for guidelines on:

- Reporting bugs
- Suggesting features
- Submitting pull requests
- Development setup

Links
-----

- `GitHub Repository <https://github.com/RisingOrange/anki-smart-templates>`_
- `Issue Tracker <https://github.com/RisingOrange/anki-smart-templates/issues>`_
- `AnkiWeb Page <https://ankiweb.net/shared/info/XXXXXXX>`_ (TBD)
- `Documentation <https://ankidroid-js-api.readthedocs.io/>`_ (TBD)

.. note::
   This project follows semantic versioning. Version numbers indicate:
   
   - **MAJOR**: Incompatible API changes
   - **MINOR**: New functionality (backwards-compatible)
   - **PATCH**: Bug fixes (backwards-compatible)
