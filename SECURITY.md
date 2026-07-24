# Security Policy

Mundilfari is security-sensitive protocol and clock software. Treat time
arithmetic, parsing, state machines, source selection, authentication,
uncertainty, clock discipline, platform timestamps, privileged helpers,
release scripts, standards, CI, and dependencies as high risk until reviewed
and tested.

## Current Security Status

Version `0.1.0` is a repository foundation. It contains no protocol parsers,
network clients, cryptography, TLS, platform FFI, privileged clock control, or
production time source. Do not use it to make security or clock-discipline
decisions.

## Routine Checks

Run these regularly and before releases:

```bash
scripts/checks.sh
scripts/check_latest_tools.sh
scripts/release_0_1_gate.sh
cargo deny check
cargo audit
scripts/generate-sbom.sh --check
```

GitHub Actions run CI. GitHub CodeQL default setup must be enabled in repository
security settings. Do not add an advanced CodeQL workflow while default setup
is active. The required review is documented in
[GitHub Security Settings](docs/github-security-settings.md).

## Release Gate

Every release tag must point at a final pentest-report commit. The matching
`security/pentest/vX.Y.Z.md` report must have `Status: PASS`, and
`scripts/validate-release-readiness.sh vX.Y.Z` must pass before the tag is
created.

The report commit must be the direct linear child of the reviewed
implementation commit and may change only the permanent report. Do not rewrite
the release branch between review and tagging.

## Protocol Security Rules

- Parsing does not grant semantic validity or clock authority.
- Authentication, accuracy, uncertainty, freshness, and traceability are
  independent properties.
- `AtomicInstant` is the canonical TAI coordinate; realization and trust
  evidence are separate and equality never manufactures either.
- Monotonic instants, deadlines, elapsed durations, correlations, and expiries
  carry suspend/rate/scope/process/machine/namespace/generation identity and
  cannot cross domains implicitly.
- Guaranteed hard bounds and statistical covariance/confidence are distinct;
  stable non-interchangeable interval classes exist before EOP or era
  consumers, and statistical estimates require explicit policy before
  contributing a bound.
- Every source can withdraw evidence or publish a discontinuity, and that
  invalidation propagates through consensus, servo, clock, persistence, and
  audit state.
- Fork, exec, VM snapshot/restore, and container checkpoint/restore rotate
  generic lifecycle generations and invalidate inherited security/time state.
- Leap handling remains layered: core validates immutable candidates, lifecycle
  preserves and withdraws evidence, engine policy alone constructs an opaque
  admitted handoff, and hosted publication rechecks all bound generations,
  expiry, withdrawal, and replacement state immediately before one consistent
  UTC-model change. Raw expert replacement cannot update the default clock.
- Source smear behavior is evidence; local smear-versus-step presentation
  policy never decides whether the underlying UTC model contains a leap.
- No silent downgrade from authenticated to unauthenticated time.
- Legacy and historical protocols are disabled in secure defaults.
- GNSS interpretation comes only from admitted Navheim timing evidence;
  Mundilfari preserves invalidation, health, authentication, integrity,
  freshness, uncertainty, and provenance without re-decoding it.
- Navheim evidence never grants clock authority without independent
  Mundilfari source and discipline policy.
- Large, backward, or post-startup clock steps require explicit policy.
- The privileged helper independently limits cumulative adjustment and request
  rate, binds authorization to a session/clock domain, and latches repeated
  faults; per-request bounds alone are insufficient.
- Discipline ownership is capability-qualified; externally observed
  phase/rate changes invalidate proposals and force servo reacquisition.
- Servo state consumes correlated actual-actuation feedback and cannot assume
  that a proposal was applied exactly.
- Persisted authentication, confidentiality, corruption detection, and
  rollback freshness are separate capabilities; ordinary mutable local state
  never receives a strong rollback-protection claim.
- Protocol and persistence consumers use the shared bounded crypto-provider
  contract with per-key usage limits and fail-closed entropy/rekey behavior.
- Secret-memory protection is capability-qualified: redaction, zeroization,
  page locking, core-dump exclusion, hardware/non-exportable keys, and external
  key operations are separate claims, and unsupported protections remain
  explicit non-claims.
- Safe facade APIs return structured errors for caller, capacity, platform,
  authorization, cancellation, and resource failures; allocator aborts and
  internal invariant bugs are documented non-claims, not recoverable errors.
- Strict certificate validation accepts only when the full trusted-time
  interval lies within certificate validity; midpoint or preferred estimates
  cannot turn partial overlap into validity, and scalar-time verifier success
  cannot substitute for immutable whole-chain temporal/revocation evidence.
- Retained TLS/NTS tickets, exporters, associations, cookies, and peer evidence
  bind a stable policy generation, immutable temporal-validation evidence, and
  relevant time/leap-model and lifecycle generations. Normal clock refinement
  does not churn identity; expiry, rollback, trust removal, revocation, or a
  relevant discontinuity explicitly invalidates or requires revalidation.
- Temporal evidence also binds the concrete reference identity, endpoint,
  SNI/ALPN, chain, connection, and exporter generation. Retention never exceeds
  the earliest conservative chain/revocation/policy/session/key horizon;
  worst-case time/correlation/holdover/suspend semantics derive the monotonic
  deadline, and failure or domain discontinuity requires per-use revalidation
  or rejection.
- `TrustedClock::now()` monotonicity applies to a preferred application
  projection, never to hard truth bounds or a false synchronization label.
- Early hosted time-data updates use a caller-serialized verify/stage/compare/
  commit transaction and make no concurrent-reader claim; later publication
  accepts only opaque admitted leap, EOP, and scale-offset forms and exposes
  conversion/clock state consistently. Raw or merely authenticated artifacts
  remain expert-only; configured authority is independently required. A
  candidate never authenticates the transport or signature that delivered
  itself, redirects preserve admitted authority, remote retrieval is explicit,
  and offline/manual ingestion uses the same candidate pipeline.
- The helper consumes one canonical pre-daemon policy ceiling and discipline
  audit/gap schema; later daemon configuration and exporters may extend those
  types but cannot replace, reinterpret, or widen them.
- Append-only audit storage is not called tamper-evident without a verified
  chain, sealed root, or external witness.
- Delay attacks remain in scope even when a protocol is authenticated.
- Official specifications, revisions, and verified errata precede protocol
  claims.
- Every production source hash, governing requirement, and concrete test is
  registered in the implementation-evidence gate; protocol work additionally
  pins exact normative hashes, clauses, and errata dispositions.
- Precision claims require end-to-end hardware and measurement evidence.

## Dependency Policy

The dependency policy lives in `deny.toml`. Unknown registries and git sources
are denied. Mundilfari implements time semantics and time protocols itself;
reviewed generic TLS, cryptographic, or OS-binding crates may be admitted only
at documented optional boundaries.

Every new or updated third-party crate requires:

- current-version verification;
- license, maintenance, MSRV, feature, transitive, and native-code review;
- no hidden `std`, network, filesystem, entropy, or privileged expansion in
  core crates;
- behavior and failure tests;
- threat-model, SBOM, and release-note updates;
- `cargo deny check` and `cargo audit` evidence.

## Reporting

Do not publish exploitable security details before a fix is available. Use a
private GitHub security advisory or contact the maintainers through the
repository's configured private security channel.
