# Changelog

All notable changes to Mundilfari are documented here.

The format follows Keep a Changelog and this project uses Semantic Versioning.

## [Unreleased]

### Changed

- Added a fail-closed implementation-evidence gate: every production Rust
  source maps governing requirements to concrete tests, while protocol work
  must additionally pin exact registered documents, hashes, clauses, and
  errata dispositions.
- Added a Gjallarbru-style, checksum-locked corpus of 67 RFC Editor documents
  with reviewed roles, roadmap assignments, offline integrity gates, explicit
  trust-pin updates, text-normalization protection, and CODEOWNERS coverage.
- Added a 56-entry external-standards registry and an ignored local-only vault;
  seven revision-pinned public drafts/specifications are locally downloadable
  only after committed SHA-256 verification, while restricted documents
  require legitimate manual acquisition.
- Updated protocol and release planning for RFC 9748, RFC 9921, exact current
  NTP-family draft revisions, and milestone-blocking source/errata review.
- Refreshed NTPv5 to `draft-ietf-ntp-ntpv5-09` and admitted
  `draft-ietf-ntp-nts-keyexchange-pool-01` as a separate revision-pinned
  experimental milestone.
- Added recursive normative-reference closure, exact family-document
  expansion, independent conformance levels, and requirements traceability to
  the pre-1.0 gates.
- Added a fail-closed framework milestone for documented non-GNSS vendor
  extensions and corrected the distinct NTP extension-field,
  checksum-complement, and AES-CMAC roadmap responsibilities.
- Moved NTP-over-PTP into its own post-PTP-foundation milestone so the adapter
  cannot precede the PTP wire, transport, timestamp, and correction layers it
  requires.
- Moved all GNSS message, receiver, rollover, authentication, health, and PPS
  semantic interpretation to the planned Navheim project.
- Replaced direct GNSS protocol crates with one future optional
  `mundilfari-navheim` companion adapter.
- Reordered the pre-1.0 roadmap so every Navheim-independent feature is
  implemented first and Navheim integration plus CGGTTS form the final feature
  phase.
- Incorporated the July 2026 architecture gap review into existing milestones:
  exact conversion residuals, capability truth, platform sys isolation,
  explicit consensus fault assumptions, stronger protocol and privilege
  boundaries, deterministic embedded evidence, and signed release assurance.
- Incorporated the follow-up gap audit without reducing existing scope:
  corrected dependency direction and servo ownership; added hard/statistical
  uncertainty, generic withdrawals, complete platform/device stops, discipline
  authority, secure persistence, concurrency, canonical schemas, stable
  requirement IDs, NTS/Roughtime edge cases, and source-evidence semantics.
- Integrated the subsequent sequencing and control-loop review: moved generic
  quorum/diversity ahead of NTP composition, placed schema and crypto-provider
  kernels before persistence/MAC consumers, qualified rollback protection,
  closed actuation feedback and helper cumulative limits, assigned stable PTP
  security, made the facade panic contract explicit, fixed the TAI origin, and
  moved the final Navheim security gate after CGGTTS.
- Integrated the next lifecycle and truthfulness review with typed monotonic
  suspend/rate domains, generic fork/checkpoint invalidation, competing-
  discipliner leases, honest virtual-clock ahead recovery, interval-valued
  certificate validation, leap-evidence consensus, controlled hosted
  time-data updates, explicit bare-metal concurrency profiles, bounded schema
  tag/depth governance, and atomic configuration/sequenced audit semantics.
- Split overloaded scale, PTP-profile, industrial, wireless, cellular, media,
  broadcast, timestamp, and servo milestones into independently reviewable
  patch releases while preserving the final Navheim feature phase.
- Preserved the broader pre-1.0 protocol registry commitment and Navheim-last
  ordering instead of adopting the review's narrower replacement roadmap.

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
