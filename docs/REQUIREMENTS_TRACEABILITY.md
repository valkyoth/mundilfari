# Mundilfari Requirements Traceability

Status: repository-baseline audit and bidirectional-traceability contract

Reviewed: 2026-07-24

This document maps the project requirements to present evidence and to the
release milestone that must close the production claim. It is an audit index,
not a substitute for the detailed implementation or release plans.

## Bidirectional Traceability Contract

Before implementation, `v0.2.0` assigns stable domain-qualified IDs such as
`TIME-ATOM-001`, `WIRE-BOUND-002`, `NTP-REPLAY-003`, or
`DISC-HELPER-006`. Each requirement maps in both directions among:

- its exact normative clause/hash/errata disposition or architecture decision;
- owning crate, module, release milestone, and implementation source hash;
- positive, negative, boundary, property, fuzz, simulation, conformance, and
  hardware evidence as applicable;
- explicit exclusions, non-claims, and inapplicability rationales.

The active [implementation-evidence registry](../compliance/IMPLEMENTATION_EVIDENCE.json)
already enforces this shape for foundation source. `v0.2.0` completes the
protocol/standard ledger and stable ID namespace before core feature
implementation begins. The common gate rejects orphan edges in either
direction; a source change invalidates its reviewed hash until the documents
and tests are rechecked.

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
| implementation cannot bypass document/test review | reviewed implementation hash plus machine-readable requirement, exact-standard, clause, errata, and test linkage | `v0.3.0`; every common gate |
| exact interval and hard/statistical semantics | exact borrowed/owned/view types with no third public generic claim type; one canonical identity profile; borrowed generative handles; fallible single/multi-root promotion into bounded frozen shared DAGs with atomic failure, per-root/unique-total accounting, immutable retention and bounded new-owner compaction; nonwrapping generations, lease traversal, explicit equality, and no arena-dependent infallible semantic `Eq`/`Hash`; engine proofs/tokens become source-arena-independent through one kind-safe checked engine handle and semantic views; canonical-order batch verification uses one bounded snapshot, shared-node failure fan-out, root-local evidence isolation, no authoritative global-abort prefix, complete accounting, processed-only complete member status, abort-only unprocessed diagnostics, and a typed complete-membership witness; original configured membership remains distinct from current accepted-bound contributors, failed members cannot vote or reduce thresholds, and refresh atomically reports retained/invalidated/absent prior authority through a fixed-size interval-valued linearization observation that grants no through-receipt authority; external/persisted recipes remain unverified records | identity `v0.6.1`; claims/recipes/ownership `v0.7.1`–`v0.15.0`; foundation audit `v0.17.0`; schema/persistence/builders `v0.22.1`, `v0.39.1`, `v0.140.0`–`v0.140.1`; engine `v0.60.0`–`v0.61.0`; downstream/publication `v0.133.0`–`v0.144.0`; product/resource/fault/API gates `v0.148.0`, `v0.160.0`, `v0.163.0`, `v0.166.0` |
| unambiguous canonical atomic timeline | TAI origin/SI-second semantics, generic TAI/UTC mapping, realization evidence separation | `v0.7.0`, `v0.12.0`; gate `v0.17.0` |
| leap evidence cannot unilaterally change UTC | source-neutral representation; pure isolated candidate transaction; evidence lifecycle; opaque engine admission handoff; atomic precommit generation/expiry recheck and consistent publication | `v0.12.0`–`v0.12.1`, `v0.15.2`, `v0.61.1`, `v0.137.1`; audit `v0.148.0` |
| monotonic values are domain typed | suspend/rate/scope/process/machine/namespace/generation identity | `v0.16.0`, `v0.24.0`, `v0.30.0` |
| generic evidence withdrawal | source-neutral upsert/withdraw/discontinuity lifecycle | `v0.15.1`; every source and engine milestone |
| cloned execution invalidates inherited state | generic fork/exec/checkpoint/restore process and machine generations | `v0.23.1`; consumers and final fault review |
| canonical schema precedes persistence | no_std bounded kernel before storage, later compatibility/binding freeze | `v0.22.1`, `v0.39.1`, `v0.140.1` |
| crypto provider precedes security consumers | MAC/AEAD/digest/entropy/key contracts, assurance and usage accounting; providers cannot mutate the earlier fixed public content-identity profile | identity `v0.6.1`; provider `v0.24.1`; production admission `v0.72.0`; audit `v0.162.0` |
| complete platform foundations | provider-owned monotonic read intervals/capabilities, hosted clocks, PHC, RTC, architectural/embedded counters, MMIO, GPIO, frequency capture, actuators, namespace identity | traits `v0.24.0`; adapters `v0.30.0`, `v0.37.0`–`v0.40.0`; `v0.161.0` |
| one discipline authority boundary | proposal/policy API, actual-actuation feedback, cumulative helper envelope | `v0.39.0`, `v0.134.4`, helper `v0.142.0` |
| competing discipliners are detected | ownership capability, external-change discontinuity, proposal invalidation and reacquisition | `v0.39.2`, `v0.134.4`, `v0.161.0` |
| common secure persistence | bounded versioned state with capability-qualified rollback freshness; derivations restore only as unverified records requiring complete current-engine reverification | `v0.39.1`, `v0.140.1`; consumers and final audits |
| helper policy and audit types precede the daemon | stable policy ceiling, canonical discipline/audit-gap records, reserve-before-actuation full-store behavior | `v0.39.3`; consumers `v0.142.0`, `v0.146.0`, `v0.147.0` |
| controlled hosted time-data updates | explicit provider, caller-serialized transaction, non-circular artifact trust, untrusted retrieval separated from artifact-integrity or configured-platform-trust evidence and separately configured source role/authority, opaque EOP/scale-offset admission proofs, and later all-component concurrent publication | `v0.52.1`–`v0.52.3`, `v0.137.1`, `v0.148.0` |
| one generic fusion implementation | early engine quorum/diversity, later cross-protocol orchestration only | `v0.60.0`–`v0.61.0`, `v0.133.0` |
| stable PTP security ownership | stable Security TLV/association/replay/key lifecycle or external-only non-claim | `v0.107.2`, gate `v0.108.0` |
| consensus configuration identity | atomic policy/membership generations carried into results/proposals; original `n` is preserved across processed member failure, only current accepted bounds contribute, abort/unprocessed diagnostics cannot enter quorum, removal requires a fully reassessed new generation, and refresh disposition is bound to its observation interval/generation | `v0.60.1`–`v0.61.0`, `v0.133.0`, concurrent refresh `v0.137.1` |
| safe facade panic contract | recoverable caller/environment/resource failures return structured errors | `v0.138.0`, `v0.160.0`, `v0.166.0` |
| interval-valued certificate validation | concrete verifier applies exact endpoint semantics to immutable whole-chain temporal/revocation evidence; scalar-time success cannot satisfy strict full-interval validity | `v0.7.1`, `v0.75.0`, `v0.80.0`, `v0.162.0` |
| retained TLS/NTS state has correct lifetimes without live-clock churn | stable service context, typed provider-bound resumption credential, fresh per-handshake connection, per-connection exporter, and per-exporter NTS association generations have distinct bindings and layer-owned horizons; missing resumption enforcement disables it | `v0.75.1`–`v0.75.3`, consumers `v0.77.0`–`v0.81.0`; audit `v0.162.0` |
| secret-memory claims are capability-qualified | redaction, zeroization, page locking, core-dump exclusion, hardware/non-exportable, and external-key protections remain separate capabilities and non-claims | `v0.24.1`, `v0.33.0`, `v0.72.0`; audit `v0.162.0` |
| consistent concurrent reads | provider-owned conservative monotonic intervals; explicit linearization-time `observed_at`/`valid_until` authority versus WCET-capability-backed through-completion authority; generation-consistent publication and no_std profiles | primitive `v0.16.0`; traits/platform `v0.24.0`, `v0.30.0`, `v0.37.0`–`v0.38.2`; issuance `v0.60.1`; reads `v0.137.0`–`v0.138.0` |
| honest monotonic application-clock recovery | truth bounds may revise, preferred projection cannot retain false synchronized status | `v0.137.3`, `v0.166.0` |
| configuration and audit integrity | atomic generated configuration; domain/model-sequenced audit with honest tamper-evidence capability | `v0.146.0`–`v0.148.0` |
| canonical external representation | early bounded kernel plus compatibility freeze for IPC/persistence/C/WASM/logs/bindings | `v0.22.1`, `v0.140.1` |
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
