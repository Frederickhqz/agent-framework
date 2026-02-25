# Changelog

All notable changes to the OpenClaw Agent Framework.

## [Unreleased]

### Added
- Curiosity diary system for agent self-reflection
- Voice pipeline documentation (TTS/STT)
- Automated voice message cleanup at 4 AM
- Preserve voice message functionality
- **INSTALL.md** - Complete installation guide
- **CHANGELOG.md** - Version tracking
- **CONTRIBUTING.md** - Contribution guidelines
- `scripts/archive-old-diaries.sh` - Archive diaries >30 days
- `scripts/verify.sh` - Installation verification script

### Changed
- Updated diary INDEX with Feb 24-25 entries
- Improved memory retention policy documentation
- All documentation files now linked in README

## [0.2.0] - 2026-02-25

### Added
- Complete MEMORY_FRAMEWORK.md documentation
- Task inference rules in HEARTBEAT.md
- Memory tier system (P0/P1/P2)
- Fluff compaction during operations
- Nightly janitor (2-3 AM conditional)
- Session boundary detection
- QMD integration for semantic search

### Changed
- Restructured memory/ directory layout
- Improved retention policy
- Updated scripts for better logging

### Fixed
- Archive folder creation on first run
- QMD collection initialization

## [0.1.0] - 2026-02-22

### Added
- Initial framework release
- README.md with quick start
- HEARTBEAT.md task inference rules
- Basic memory structure:
  - CORE_SYSTEM.md
  - PROJECTS.md
  - RETENTION_POLICY.md
- Janitor scripts:
  - memory-janitor.sh
  - compact-fluff.sh
  - session-flush.sh
- QMD skill integration
- Curiosity diary template

---

## Version Format

[MAJOR.MINOR.PATCH] - YYYY-MM-DD

- **MAJOR**: Breaking changes to framework structure
- **MINOR**: New features, improvements
- **PATCH**: Bug fixes, documentation updates

## Categories

- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Now removed features
- **Fixed**: Bug fixes
- **Security**: Security improvements
