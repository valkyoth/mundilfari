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
  consumers. Open/closed endpoints are exact and never simulated by adjusting
  one quantum; trusted estimates are finite. A hard-bound claim states
  mathematical containment, not source honesty. Its immutable content-
  addressed bounded condition uses `All` for intersection, `Any` for union/
  hull, added model/rounding prerequisites for conversion, and a reviewed
  threshold/fault predicate for consensus; simplification cannot silently
  strengthen or weaken it. External identifiers remain unresolved until exact
  canonical content or a trusted immutable registry generation is verified.
  Claim/recipe/condition/model/origin identities use one early domain-separated
  canonical preimage and fixed versioned identity-digest profile; exact type,
  units, scale, normalization, endpoint inclusion, operation, condition, and
  schema generation are bound. Structural comparison follows digest match,
  collisions fail typed, and Rust hash/layout/serde/debug output is forbidden.
  Every root and transforming hard-claim operation preserves a bounded,
  acyclic, non-authoritative `UnverifiedBoundDerivation` with exact endpoints,
  inputs, operation, rounding, models, condition, and origin/observation
  identity; absence or truncation prevents later acceptance. A hard claim
  contains a mandatory lifetime-branded typed handle into a bounded arena.
  Brands are generative rather than addresses/caller labels; store/node
  generations never wrap, and exhaustion faults or requires a fresh brand.
  Mutable arenas require exclusive writes while traversal uses an immutable
  read lease/frozen snapshot that excludes eviction. Stale/evicted/foreign/
  wrong-domain handles and geometry-only intervals cannot enter verification,
  and serialization exports the complete DAG rather than the process-local
  handle. Geometry, canonical conditional-claim equality, and fallible
  lease-backed derivation equality are distinct; arena-dependent values have no
  infallible semantic `Eq`/`Hash`.
  Borrowed claims cannot escape the arena brand. alloc callers may fallibly
  promote a complete canonical DAG into a bounded frozen
  `OwnedHardBoundClaim`; promotion reinterns structurally and cannot copy a
  handle, extend a lifetime, leak storage, or grant authority. Engine-verified
  proofs and accepted tokens are lifetime-independent from that unverified
  source arena and retain all invalidating generation dependencies.
  Canonical resolution does not prove current truth: engine assessment reports
  supported, contradicted, indeterminate, expired, or withdrawn with exact
  evidence/generations/deadline and preserves independent evidence-origin,
  integrity, authority, and direct/derived-lineage axes for every atom.
  Derived basis retains all bounded transitive leaves, so configured assumptions
  cannot hide behind cryptographic, authority, or derived labels. Engine
  acceptance additionally requires complete current verification of the early
  recipe into an opaque `VerifiedBoundDerivation` binding the exact
  observations, endpoints, operation, rounding, models, condition, and claim
  digest; a supported condition cannot justify a substituted narrower
  interval. Statistical estimates require explicit policy before contributing
  a bound.
- Assessment issuance captures and rechecks one complete generation vector
  around unlocked provider callbacks. It publishes no mixed-generation result:
  arena traversal first materializes bounded input under a read lease/frozen
  snapshot and releases every arena lock/lease before those callbacks.
  Successful verification owns the proof/token material before the source may
  drop; failure creates nothing. Change, eviction, or concurrent import causes
  bounded retry or indeterminate status, and any accepted token is minted with
  its assessment at the same engine linearization point. A fresh bounded
  monotonic interval is sampled there; its
  conservative upper edge, including resolution, latency, rate uncertainty,
  and only a reviewed margin for internal work remaining before that
  linearization point, must remain before the deadline. This is not
  caller-return authority.
- Derivation or condition-assessment loss invalidates consensus, leap decisions,
  servo/estimator/holdover state, discipline proposals, synchronized
  publication, and strict facade results through reserved lifecycle/generation
  propagation; stale accepted tokens and trusted booleans are rejected.
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
- Persisted derivations decode only as `UnverifiedBoundDerivationRecord`;
  verified derivations have no deserialize/restore path. Replay, restore, or
  migration requires bounded reverification against current inputs, rules,
  models, source/provider generations, and lifecycle state.
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
  interval lies within the whole-chain validity intersection and supported
  revocation-freshness constraints; exact endpoint inclusion is preserved,
  midpoint/preferred estimates cannot turn partial overlap into validity, and
  scalar-time verifier success cannot substitute for immutable evidence.
- Retained TLS/NTS state uses separate lifetimes: a stable service credential
  context binds policy/identity/chain/revocation/time evidence; each ticket/PSK
  becomes a bounded `ResumptionCredentialGeneration` that also binds its
  provider handle/generation, cryptographic compatibility, ticket identity/key
  generation where available, age/use/expiry/replay policy, and secret/
  persistence capabilities. Every handshake gets a fresh TLS connection
  generation, every connection gets a unique exporter generation, and every
  exporter derives a distinct NTS association generation. Exporter material
  never crosses full or resumed connections. Missing adapter enforcement
  disables resumption. Normal clock refinement does not rotate the service
  context; relevant policy, expiry, revocation, model, or lifecycle change
  still invalidates or requires revalidation.
- Temporal evidence also binds the concrete reference identity, endpoint,
  SNI/ALPN policy, and chain evidence. Each layer owns its horizon: service
  chain/revocation/identity/trust/time-model, then ticket/PSK/provider limits,
  connection lifetime, exporter/key usage, and association/cookie policy;
  every child ends no later than its parent. Worst-case time/correlation/
  holdover/suspend semantics derive the monotonic
  deadline, and failure or domain discontinuity requires per-use revalidation
  or rejection.
- TLS 1.3 resumption revalidates and consumes the typed resumption credential
  before creating fresh connection/exporter/association generations even when
  the peer does not resend its certificate chain; absence of a chain is never
  fresh evidence.
- `TrustedClock::now()` monotonicity applies to a preferred application
  projection, never to hard truth bounds or a false synchronization label.
- Every platform monotonic provider returns a conservative interval with exact
  domain, resolution, measurement method, latency/rate-uncertainty provenance,
  and generation or reports strict authority unavailable; scalar counters are
  never silently singleton intervals.
- Default strict clock reads return linearization-time authority with explicit
  `observed_at` and `valid_until`. A distinct through-completion result requires
  current reviewed WCET capability and adds that margin; ordinary hosted
  scheduling latency is never claimed bounded. A straddling/unbounded
  measurement, idle expiry without a writer, monotonic failure/reset/domain
  mismatch, or suspend without inclusive time or reliable resume invalidation
  fails closed to diagnostics.
- Early hosted time-data updates use a caller-serialized verify/stage/compare/
  commit transaction and make no concurrent-reader claim; later publication
  accepts only opaque admitted leap, EOP, and scale-offset forms and exposes
  conversion/clock state consistently. Raw or merely authenticated artifacts
  remain expert-only; platform/custom adapters emit untrusted retrieval claims,
  engine verification produces opaque artifact-integrity evidence without
  source authority, and configured source role/authority is applied only at
  admission. Correctly verified wrong-role artifacts remain unauthorized.
  Non-cryptographic configured platform trust uses distinct evidence and is
  never named verification or proof; attestation callbacks retain provider
  generation/capability and cannot return a trusted boolean. A candidate never
  authenticates the transport or signature that delivered itself, redirects
  preserve admitted authority, remote retrieval is explicit, and offline/
  manual ingestion uses the same candidate pipeline.
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
