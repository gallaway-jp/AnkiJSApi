# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
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
- Unit test framework
- Build system for .ankiaddon packaging

### Known Limitations
- TTS implementation uses system TTS (not AnkiDroid's specific TTS engine)
- Speech-to-Text (STT) APIs not yet implemented
- Network metered status detection approximated for desktop
- Some mobile-specific UI controls adapted for desktop context

## [1.0.0] - TBD

### Added
- First stable release
- Full API compatibility with AnkiDroidJS v0.0.3
- Comprehensive test coverage
- Documentation and examples

[Unreleased]: https://github.com/gallaway-jp/AnkiJSApi/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/gallaway-jp/AnkiJSApi/releases/tag/v1.0.0
