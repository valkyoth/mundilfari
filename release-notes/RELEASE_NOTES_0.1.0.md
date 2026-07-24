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
  estimates and honest hard-bound-claim naming; expanded the `v0.75` hierarchy
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
- Runtime trust hardening added `v0.60.1`: canonical conditions remain
  conditional until current evidence is assessed and accepted by engine policy.
  An opaque `PolicyAcceptedHardBound` gates consensus, leap admission, servo/
  estimator/holdover state, proposals, synchronized publication, and strict
  facade operations, while diagnostics expose status, reasons, assurance,
  deadline, and non-claims without an `is_trusted` boolean.
- The same milestone now requires an opaque engine-verified derivation binding
  exact claim endpoints to root observations or every derived operation,
  rounding rule, model generation, condition, and input digest. Atom assessment
  preserves structured support basis, and assessment/acceptance issuance uses
  one snapshot-consistent generation transaction.
- `v0.137.0`–`v0.137.1` now require every strict virtual-clock read to enforce
  the accepted deadline in its exact monotonic domain, including idle expiry,
  timer starvation, suspend/resume, reset, and domain-failure cases.
- Derivation inputs are now retained from their true owners: `v0.7.1` creates
  bounded non-authoritative root recipes, `v0.7.2` composes them, and every
  claim-transforming era/fraction/scale/UTC/POSIX/uncertainty/observation
  milestone through `v0.15.0` preserves them for later engine verification.
  Serialized and persisted recipes remain explicit unverified records.
- Support basis is now a structured set of independent evidence-origin,
  integrity, authority, and direct/derived-lineage axes; derived results retain
  their complete bounded transitive bases. Deadline issuance and strict reads
  sample after evaluator work and compare conservative monotonic upper edges
  including resolution, latency, and rate uncertainty.
- `v0.6.1` now defines one domain-separated canonical identity profile before
  claims exist. `BorrowedHardBoundClaim` carries a mandatory typed handle into
  bounded caller-owned or fallible derivation arenas, with canonical shared
  DAGs and complete-record serialization rather than detachable tuples or local
  handles.
- Those handles now use invariant generative lifetime brands and nonwrapping
  generations, while traversal uses read leases/frozen snapshots and releases
  all arena access before callbacks. Geometry, conditional-claim, and fallible
  complete-derivation comparisons are separate, and `v0.17.0` audits identity,
  SHA-256, arena ABA/concurrency, equality, stack, and reduced-state evidence
  before protocols consume them.
- New `v0.7.4` separates zero-allocation borrowed claims from fallible bounded
  frozen owned claims. Promotion canonically reinterns the complete DAG;
  multi-root promotion preserves sharing with bounded retention/compaction.
  Verified proofs/tokens become source-arena-independent while no_std engine
  storage remains explicit and checked. Returned clocks, `'static` tasks, and
  C/JNI/Swift contexts receive explicit non-self-referential ownership and
  destruction tests.
- `v0.60.1` now defines deterministic multi-root verification rather than
  leaving partial failure to implementations. Canonical member order, one
  bounded snapshot, shared-node failure fan-out, root-local evidence isolation,
  complete accounting, and a typed complete-membership witness prevent
  attacker-selected successful prefixes. Global aborts mint no proof/token,
  and the no_std proof/accepted references share one kind-safe checked engine-
  handle abstraction.
- Failed batch members now remain in configured membership/original `n` while
  contributing no interval or vote; they cannot be filtered to weaken a
  threshold, and shortage is explicitly insufficient/unsafe. Aborted refreshes
  report whether prior authority was retained, invalidated, or absent, while
  complete replacement and prior retirement share one linearization point.
- Complete and aborted batches now use disjoint member types:
  `Unprocessed` exists only in abort diagnostics and cannot reach a complete
  witness or quorum. Prior-authority reports bind fixed-size identity,
  generation, monotonic interval, deadline/invalidation, and publication data
  to their refresh linearization point; delayed return never makes `Retained`
  a current-authority claim.
- Complete membership, aggregate batch state, exact-support consensus, and
  published snapshots now have distinct non-substitutable authority
  identities. Validity is the conservative minimum of all required deadlines
  in one monotonic domain; mixed domains require admitted correlation evidence
  or fail. Losing any contributor actually used by a proof invalidates that
  authority even if a different quorum could be formed.
- Commit-covered refresh timing has an implementable contract: after callbacks
  and fallible work, commit serialization protects a pre-commit interval
  expanded by a reviewed bound for all remaining work through physical commit.
  Fixed-size measured/unavailable stamps make capability, sampling, and domain
  failure explicit; unavailable observations never retain or create authority.
- Refresh now has two explicit strength profiles. General hosted systems use a
  nonwrapping reservation/version and the monotonic sample as the logical
  `LinearizationRefresh` point, allowing unbounded later preemption while
  strict readers revalidate installed historical state. Only optional
  `CommitCoveredRefresh` requires a reviewed remaining-work/WCET capability.
- Pre-consensus state is now accurately named `BatchAdmissionState` and has no
  servo, discipline, publication, or trusted-time authority. Monotonic-domain
  correlation now has a complete owner chain: core defines directed untrusted
  candidates and outward-rounded earliest-edge deadline translation, platforms
  measure candidates, and engine alone admits opaque correlations with full
  reset/suspend/rate/migration/provider/lifecycle invalidation.
- `v0.24.0` and hosted, PHC, architectural, embedded, and browser adapters now
  own conservative `read_interval()` production. Default strict reads report
  linearization-time `observed_at`/`valid_until`; a type-distinct
  through-completion result exists only with reviewed current WCET capability.
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
