# Mundilfari 0.1.0 Release Notes

Status: awaiting implementation pentest

## Summary

`0.1.0` establishes the repository, architecture, security, documentation, and
release foundation for a `no_std`-first time-protocol framework.

This version does not implement a time protocol, trusted clock, network client,
clock servo, hardware timestamp, or privileged clock adjustment.

## Added

- `mundilfari`, `mundilfari-core`, `mundilfari-engine`, and
  `mundilfari-platform` published crate boundaries.
- Repository-only Rust `1.97.1` task-runner boundary.
- Rust `1.90.0` MSRV through pinned stable `1.97.1` compatibility policy.
- MIT OR Apache-2.0 licensing.
- Detailed implementation and release plans through an exact `1.0.0` release
  candidate.
- Initial protocol registry spanning Internet/NTP/NTS, PTP, Navheim-derived
  GNSS observations, PPS, radio, industrial, automotive, wireless, media,
  space, formats, and trusted timestamp evidence.
- Checksum-locked local reference corpus of 67 exact RFC Editor documents,
  with reviewed roles and release assignments, offline verification,
  CODEOWNERS protection, and exclusion from crates.io packages.
- Machine-readable 56-entry external-standards source registry with a
  fail-closed ignored vault for every non-RFC document byte; seven public,
  revision-pinned sources have committed SHA-256 pins and a local-only fetcher.
- Explicit source review updates for RFC 9748, RFC 9921,
  `draft-ietf-ntp-ntpv5-09`, `draft-ietf-ntp-over-ptp-08`,
  `draft-ietf-ntp-nts-for-ptp-03`, and `draft-ietf-ntp-roughtime-19`.
- Separate revision-pinned experimental planning for
  `draft-ietf-ntp-nts-keyexchange-pool-01`.
- Explicit pre-implementation closure for transitive normative references,
  family/bundle expansion, conformance levels, and documented non-GNSS vendor
  extensions.
- Dependency-correct experimental ordering: NTPv5 remains in the NTP phase,
  while NTP-over-PTP receives a separate pass after the complete PTP
  foundations.
- Strict rule that Navheim determines GNSS time while Mundilfari decides how
  validated GNSS evidence participates in a larger clock system.
- Planned optional `mundilfari-navheim` companion crate, blocked until Navheim
  publishes its independently reviewed stable timing API.
- Dependency-last roadmap ordering: all Navheim-independent protocols,
  engines, servos, and applications precede the final Navheim integration and
  CGGTTS feature phase.
- Integrated architecture-review gaps into explicit existing versions without
  reducing the stable-protocol completeness contract, including rational
  conversion evidence, runtime capability truth, consensus fault assumptions,
  safe/sys platform isolation, deterministic embedded engines, hardened
  privilege separation, and signed reproducible release evidence.
- Follow-up architecture audit integrated through explicit versions for
  bounded fractions, split scale families, hard/statistical uncertainty,
  generic evidence withdrawal, RTC/MMIO/GPIO/counters/actuators, discipline
  authority, secure persistence, NTS/Roughtime edge cases, concurrent
  snapshots, canonical external schemas, and common error classification.
- Subsequent roadmap audit integrated with explicit early schema/crypto
  kernels, engine-owned NTP quorum/diversity, rollback capability levels,
  stable PTP security associations, consensus policy/membership generations,
  actual actuation feedback, cumulative helper limits, panic-safe facade
  handling, a defined TAI origin, mobile lifecycle tests, and a final
  post-CGGTTS Navheim security gate.
- Further lifecycle audit integrated through explicit versions for monotonic
  suspend/rate/scope identities, fork/checkpoint machine generations,
  competing discipline ownership, truthful ahead/frozen/catch-down clock
  recovery, interval certificate validity, leap-announcement admission,
  hosted time-data orchestration, no_std atomic/critical-section/ISR profiles,
  schema depth/tag budgets, and configuration/audit integrity.
- Latest dependency/trust audit integrated without replacing prior scope:
  leap candidate validation, evidence lifecycle, engine authority, and
  concurrent publication now have dependency-correct versions; remote
  time-data cannot establish the trust used to authenticate itself; TLS/NTS
  retained state follows full credential-context generations; canonical helper
  policy/audit types precede the daemon; and secret-memory protection claims
  are capability-qualified.
- Follow-up consistency audit closed stale and underspecified boundaries:
  `v0.12.0` now owns only source-neutral leap representation/conversion;
  engine admission produces an opaque generation-bound handoff that hosted
  publication revalidates at commit; smear presentation cannot change leap
  truth; credential contexts use stable policy generations and immutable
  whole-chain temporal evidence; and early time-data updates explicitly defer
  concurrent-reader publication.
- Subsequent dependency audit added `v0.7.1` so stable interval and
  hard/statistical types precede era, fractions, and EOP; added `v0.52.3` typed
  EOP/scale-offset admission so valid signatures cannot bypass configured
  authority; defined service/connection binding and worst-case monotonic
  credential-retention horizons; and corrected the remaining early activation
  and concurrent-read wording.
- Latest contract review made interval endpoints exact across open, closed,
  half-open, and algebraically unbounded forms while requiring finite trusted
  estimates and honest `HardBoundClaim` naming; expanded the `v0.75` hierarchy
  to separate service/ticket authorization from fresh connection/exporter/NTS
  association generations; fixed engine ownership of admitted conversion-data
  constructors; and moved identified EOP withdrawal into the generic lifecycle.
- Final follow-up review added `v0.7.2` for immutable, content-addressed
  hard-bound conditions through consensus; made `v0.52.3` introduce explicit
  retrieval, evidence, and admission layers; and assigned resumption PSKs/
  tickets their own
  provider-bound `ResumptionCredentialGeneration` at `v0.75.2` before the
  fresh connection/exporter/association hierarchy at `v0.75.3`, with separate
  service, ticket, connection, exporter, and association horizons.
- Final semantic hardening corrected `v0.7.2` to model intersection=`All`,
  union/hull=`Any`, conversion prerequisites, and reviewed consensus threshold/
  fault predicates; added `v0.7.3` unresolved-to-resolved type-state for
  external condition identities; and made `v0.52.3`
  `ArtifactIntegrityEvidence` independent from configured source authorization,
  with separate `ConfiguredPlatformTrustEvidence` for non-cryptographic OS
  trust.
- Overloaded PTP-profile, industrial, wireless, cellular, media, broadcast,
  timestamp, and servo milestones split into smaller independently pentested
  patch releases.
- `no_std`, dependency layering, 500-line, unsafe, standards, supply-chain,
  threat-model, and secret-handling policies.
- Machine-enforced implementation evidence covering every production source,
  its governing requirements, concrete linked tests, and exact
  source/hash/clause/errata review for protocol work.
- GitHub CI, Dependabot, CODEOWNERS, funding, issue, pull request, and manual
  release metadata.
- Release script, exact-commit pentest handoff, latest tool checks, package
  checks, SBOM controls, and local policy gates.

## Security Notes

- The published workspace has no third-party Cargo dependencies.
- All first-party Rust crates forbid unsafe code.
- No parser consumes untrusted protocol input in this release.
- No code can access or modify an OS or hardware clock in this release.
- CodeQL uses GitHub default setup; no advanced workflow is added.

## Verification

```bash
scripts/checks.sh
scripts/check_latest_tools.sh
scripts/release_0_1_gate.sh
```

The release is not tag-ready until an exact-commit pentest passes and
`scripts/validate-release-readiness.sh v0.1.0` accepts the permanent report.
