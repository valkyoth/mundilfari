# Mundilfari Requirements Traceability

Status: repository-baseline audit

Reviewed: 2026-07-24

This document maps the project requirements to present evidence and to the
release milestone that must close the production claim. It is an audit index,
not a substitute for the detailed implementation or release plans.

## Repository And Language

| Requirement | Present evidence | Production closure |
| --- | --- | --- |
| Mundilfari workspace and crate naming | workspace manifests, package metadata, crate READMEs | `v0.166.0` API/metadata freeze |
| MIT OR Apache-2.0 | root license files and workspace metadata | every package/release gate |
| latest stable Rust with published-crate MSRV 1.90.0 | pinned 1.97.1 toolchain, full patch matrix, live stable check | `v0.164.0` |
| repository-only tools may use 1.97.1 | `xtask` excluded from published workspace | `v0.164.0` |
| `no_std`-first published libraries | empty default features and portable-target checks | `v0.164.0` |
| Linux, Windows, BSD, macOS, Android, and iOS | platform-neutral APIs and current CI/cross targets | platform work `v0.30.0`–`v0.40.0`; closure `v0.164.0` |
| future Aesynx compatibility | no Unix types in protocol/core contracts | `v0.164.0` readiness non-claim or evidence |

## Architecture And Dependencies

| Requirement | Present evidence | Production closure |
| --- | --- | --- |
| focused crates, no monolith | facade/core/engine/platform boundaries and dependency validator | every protocol milestone; `v0.166.0` |
| no code file above 500 lines | local manifest-driven line gate for Rust, Python, and shell | every common gate |
| first-party core time protocols | dependency direction and supply-chain policy | protocol gates and `v0.167.0` |
| narrow generic third-party use only when safer/necessary | explicit TLS, crypto, X.509, OS-binding admission policy | `v0.72.0`, `v0.162.0` |
| current crates and tooling | live crates.io, Rust distribution, and GitHub Action checks | every release gate |
| crates.io versus repository-only separation | version matrix, release manifest, package-content checks | `v0.166.0`, `v0.170.0` |
| identical root/facade README | byte-identity common gate | every common gate |
| separate published-crate READMEs | modularity and package checks | each crate introduction |

## Security And Verification

| Requirement | Present evidence | Production closure |
| --- | --- | --- |
| security paramount from the first commit | threat model, unsafe/secret/dependency policy, deny/audit/SBOM gates | per-version pentest plus `v0.158.0`–`v0.167.0` |
| every behavior testable | deterministic polling, bounded providers, fixtures, simulation, fuzz and hardware plan | owning milestone plus final closure |
| exact-commit pentest before every tag | release-plan exit sentences and readiness validator | every tag |
| GitHub CodeQL default setup only | documented repository setting; no advanced workflow | every release review |
| no unsafe in safe crates | workspace lint and unsafe inventory policy | `v0.161.0` |
| no inaccessible fixture/build dependency | tracked hashes plus ignored local standards vault | `v0.2.0`, `v0.165.0` |

## Specifications And Completeness

| Requirement | Present evidence | Production closure |
| --- | --- | --- |
| official RFC/source corpus | checksum-locked RFCs and external-source registry | `v0.2.0`, `v0.165.0` |
| exact revisions, amendments, corrigenda, registries, and errata | fail-closed source policy; family records block implementation | `v0.2.0`, owning milestone, `v0.165.0` |
| recursive normative dependencies | required consumer/disposition/hash/provider ledger | `v0.2.0`, `v0.165.0` |
| honest conformance claims | independent wire, behavioral, operational, and validated levels | owning milestone, `v0.165.0` |
| active drafts revision-pinned and experimental | exact local-only hashes and revision-specific APIs | owning milestone, `v0.165.0` |
| documented vendor extensions without guessing | dedicated fail-closed extension framework | `v0.53.0`–`v0.53.1` |
| complete pre-1.0 feature scope | protocol registry and granular release plan | `v0.165.0` then feature freeze |

## Navheim Boundary

Navheim owns every GNSS navigation message, receiver protocol, constellation
model, transmitted UTC model, GNSS authentication/health decision, receiver
clock correction, week/era resolution, and assignment of GNSS meaning to PPS.
Mundilfari owns generic time domains, scales, uncertainty, source comparison,
consensus, servo, holdover, discipline, and policy.

All Navheim-independent protocol and product work ends at `v0.148.0`.
`v0.149.0` through `v0.157.0` are the final feature phase and add only the
reviewed upstream admission, companion mapping, generic PPS correlation, and
CGGTTS interchange. No feature or protocol scope follows that phase.

## Audit Rule

This index is reviewed whenever a requirement, protocol registry entry,
compiler window, supported target, dependency rule, or standards baseline
changes. A green repository check proves the present foundation only; it does
not advance any planned protocol or production conformance claim.
