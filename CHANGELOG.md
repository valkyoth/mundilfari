# Changelog

All notable changes to Mundilfari are documented here.

The format follows Keep a Changelog and this project uses Semantic Versioning.

## [Unreleased]

### Changed

- Moved all GNSS message, receiver, rollover, authentication, health, and PPS
  semantic interpretation to the planned Navheim project.
- Replaced direct GNSS protocol crates with one future optional
  `mundilfari-navheim` companion adapter.
- Reordered the pre-1.0 roadmap so every Navheim-independent feature is
  implemented first and Navheim integration plus CGGTTS form the final feature
  phase.

## [0.1.0] - Unreleased

### Added

- Security-first Rust workspace foundation.
- `no_std` facade, core, engine, and platform crate boundaries.
- Rust `1.90.0` MSRV and Rust `1.97.1` pinned stable toolchain policy.
- Repository security, dependency, documentation, CI, release, and pentest
  controls.
- Detailed implementation and release plans for all pre-1.0 protocol work.

[Unreleased]: https://github.com/valkyoth/mundilfari/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/valkyoth/mundilfari/releases/tag/v0.1.0
