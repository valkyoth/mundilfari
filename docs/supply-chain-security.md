# Mundilfari Supply-Chain Security

Mundilfari uses overlapping controls because no single tool covers source,
license, advisory, feature, native-code, release, and provenance risk.

## Required Checks

- `cargo deny check` for license, source, advisory, and duplicate policy;
- `cargo audit` for RustSec advisories;
- `scripts/generate-sbom.sh --check` for committed SPDX evidence;
- Dependabot for Cargo and GitHub Actions;
- immutable GitHub Action SHA pins;
- live stable Rust, Cargo tool, and Action release checks before tags;
- manual dependency admission and update review.

## First-Party Boundary

Mundilfari implements generic time semantics and every Mundilfari-owned time
protocol itself. Dependencies must not supply NTP, PTP, clock selection,
generic leap semantics, time-zone semantics, or another part of that purpose.

Navheim is the deliberate exception for GNSS interpretation. Only the optional
`mundilfari-navheim` companion may depend on it. Navheim supplies resolved GNSS
timing evidence; it cannot supply cross-family consensus, servos, holdover,
clock authority, or privileged discipline. Navheim is admitted only after its
stable timing release and a full dependency/security review.

Generic TLS, X.509, cryptographic primitives, mandatory AEADs, and OS bindings
may be admitted when mature third-party code is safer than a new local
implementation.

## Admission Record

Every dependency review records:

- exact latest release checked and date;
- official repository and crates.io package;
- license and MSRV;
- maintainer and security status;
- default and enabled features;
- complete transitive and native-code graph;
- `no_std`, allocation, and `std` impact;
- public API/type exposure;
- reason, alternatives, responsibility boundary, and replacement plan;
- protocol-specific tests and failure behavior.

Git dependencies are denied. An exceptional git source requires an immutable
`rev`, documented emergency reason, and release-blocking replacement plan.

## Current Inventory

The `v0.1.0` published workspace has no third-party runtime, development, or
build dependencies.

| Dependency | Version | Scope | Status |
| --- | --- | --- | --- |
| None | — | Published workspace | No external Cargo dependencies admitted |

Cargo security tools are release tooling, not shipped dependencies:

| Tool | Pinned version |
| --- | --- |
| `cargo-deny` | `0.20.2` |
| `cargo-audit` | `0.22.2` |
| `cargo-sbom` | `0.10.0` |
