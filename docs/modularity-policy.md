# Mundilfari Modularity Policy

Mundilfari must not become a monolithic source tree.

Rules:

- `mundilfari` is a facade, not an implementation home.
- Shared time domains live in `mundilfari-core`.
- Foundational instant/duration interval algebra with exact open/closed/
  unbounded endpoints, finite trusted estimates, and hard-claim/statistical
  non-substitution lives in core before era, fraction, or EOP consumers; later
  uncertainty algebra extends rather than duplicates these types.
- Hard-bound conditions are immutable, bounded, content-addressed logical
  expressions owned by core: intersection uses `All`, union/hull uses `Any`,
  conversion preserves prerequisites, and engine consensus emits reviewed
  threshold/fault predicates rather than conjuncting every source.
- The core `CanonicalIdentityV1` kernel exclusively defines domain-separated
  claim/recipe/condition/model/origin preimages and fixed identity hashing;
  schema wraps it, crypto providers may reproduce it, and neither may create a
  second identity representation or algorithm.
- Core hard-claim constructors and transformations own bounded, acyclic,
  non-authoritative `UnverifiedBoundDerivation` recipes. Every hard claim has a
  mandatory generative lifetime-branded arena handle; no_std caller-owned and
  fallible bounded alloc arenas own canonical heterogeneous DAG nodes.
  Generations never wrap, mutable access is exclusive, and derivation traversal
  uses a read lease/frozen snapshot that excludes eviction or reinterning.
  Geometry, conditional-claim, and fallible complete-derivation comparisons
  remain distinct; arena-dependent values expose no infallible semantic
  `Eq`/`Hash`. Every interval, era, fraction, scale, civil, uncertainty, and
  observation layer preserves the exact inputs/outputs/operation/rounding/
  model/condition/origin needed by the later engine verifier.
- Core owns `BorrowedHardBoundClaim`, fallible alloc-enabled
  `OwnedHardBoundClaim`, bounded `OwnedHardBoundClaimSet`, frozen owners,
  canonical single/multi-root promotion, bounded new-owner compaction, and the
  common lease-scoped claim view. Promotion adds no authority. Engine alone
  converts verified material into source-arena-independent
  `VerifiedBoundDerivation`/`PolicyAcceptedHardBound` state; facade/async/FFI
  layers only own or borrow these contracts and cannot extend arena lifetimes.
  no_std engine-backed forms expose their exact engine-storage lifetime,
  brand, and nonwrapping generation rather than hiding a caller pointer. One
  kind-parameterized engine handle backs the verified-derivation and accepted-
  bound semantic reference views; neither view creates another storage model.
- External condition identifiers decode only to unresolved core type-state;
  exact content or an immutable trusted registry generation must resolve them
  before any hard claim, engine, persistence, IPC, C, or WASM consumer.
- External or persisted derivation bytes decode only to
  `UnverifiedBoundDerivationRecord`; no schema, persistence, IPC, or binding
  directly decodes the opaque verified engine type.
- Canonical condition resolution grants no runtime trust. Engine alone owns
  bounded `VerifiedBoundDerivation` construction, snapshot-consistent current
  evidence assessment, and `PolicyAcceptedHardBound` construction. Exact
  per-atom evidence-origin, integrity, authority, and direct/derived-lineage
  axes—including derived transitive leaves—remain visible; derivation/
  condition/assessment loss invalidates all downstream consumers through the
  generic lifecycle and generation graph.
- Engine alone owns canonical multi-root verification order, shared-node work,
  batch generation snapshots, complete/aborted outcomes, and the non-forgeable
  complete-membership witness. Facade, async, and consensus layers cannot
  extract an authoritative successful prefix from an aborted batch.
  `CompleteMemberStatus` and `AbortMemberDiagnostic` are disjoint; only the
  latter can represent `Unprocessed`, and it cannot enter quorum. Engine also
  owns the distinction between original configured membership and current
  accepted-bound interval contributors, unchanged quorum thresholds, and the
  retained/invalidated/absent prior-state refresh transaction. A complete
  witness is not aggregate authority: engine separately owns non-authoritative
  `BatchAdmissionState`, exact-support `ConsensusAuthority`, one-domain
  conservative validity, and proof-bearing admitted monotonic-correlation
  dependencies. Correlation admission reuses the canonical hard-bound
  derivation and condition machinery: engine verifies every offset/rate/drift
  recipe, snapshot-consistently assesses it, preserves structured support
  axes and immutable paired capture anchors, and independently checks both
  endpoint validity domains. Initial admission walks every transitive recipe,
  condition, assessment, and support leaf and forbids all current/stale/
  replaced/historical admitted-correlation dependencies or claims derived
  through them, so proof support is acyclic by construction. Provider
  registration alone grants no proof.
  Batch admission cannot enter servo, discipline, publication, or trusted-time
  APIs; only consensus constructs time authority.
  Losing used proof support invalidates that authority; an unused alternative
  requires a new decision/identity. The fixed-size observation tags batch
  admission, consensus, or published authority and records measured coverage
  profile or typed unavailability. Portable `LinearizationRefresh` uses an
  engine-owned RAII `RefreshReservationGuard`, invalidation watermark, and
  nonwrapping fencing generation plus strict-reader revalidation without WCET.
  Engine owns cancellation/drop tombstoning, timeout-independent supersession,
  `SupersededNoInstall`, restart invalidation, bounded reader generation floors,
  tombstone reclamation, and capacity/fencing exhaustion. Each preallocated
  reservation slot holds `Live` and tombstone states in place; cleanup is
  bounded, allocation-free, callback-free, nonblocking, and non-panicking,
  cannot exhaust, treats prior supersession as success, and latches an engine
  fault/no-install on an impossible transition. Async wrappers finish
  all pending/fallible/external work before acquisition and cannot retain the
  guard across `Poll::Pending`. Optional `CommitCoveredRefresh` adds the
  reviewed remaining-work bound. Concurrent
  publication owns `PublishedAuthoritySnapshotId`, its generation, and
  replacement ordering, but cannot redefine admission/consensus identities or
  the observation as authority through receipt.
- Consensus, servo, and holdover live in `mundilfari-engine`.
- Safe OS, transport, timestamp, PHC, PPS, and device wrappers live in
  `mundilfari-platform`.
- Platform clock traits own `read_interval()` and capability provenance;
  hosted, PHC, architectural, browser, and embedded implementations inflate
  scalar counters conservatively or report strict authority unavailable.
- Core owns directed `UntrustedMonotonicCorrelationCandidate` structure,
  offset/rate/drift hard-bound claim and recipe/condition fields, immutable
  paired capture anchors, independently sourced endpoint-validity fields, and
  outward-rounded direct translation only. Platform may measure/withdraw
  candidates but cannot admit them or turn registration into proof. Engine
  alone verifies the numerical derivations, snapshot-consistently assesses
  their conditions/support, independently checks both endpoint domains, and
  constructs opaque `AdmittedMonotonicDomainCorrelation`; facade and protocol
  crates cannot bypass or duplicate admission.
- `mundilfari-platform` remains safe; necessary unsafe/FFI lives only in small
  OS-family or device-specific `mundilfari-platform-*-sys` crates.
- Clock discipline uses a separate authorization boundary and a minimal
  protocol-free helper process.
- GNSS interpretation lives in Navheim, never in a Mundilfari core, protocol,
  platform, engine, or facade crate.
- Only the optional `mundilfari-navheim` companion may depend on Navheim.
- Generic PPS capture remains platform-owned; GNSS pulse semantics arrive from
  Navheim through the companion.
- Every independently useful protocol or tightly coupled family receives a
  focused crate.
- Wire parsing, validation, I/O, source policy, and clock discipline remain
  separate modules and dependency layers.
- Protocol crates depend only on core/shared protocol prerequisites, never
  platform or engine.
- Engine depends on core and protocol-neutral observations, never protocol or
  platform crates.
- Safe platform depends on core and narrowly scoped sys crates, never protocol
  or engine policy.
- Facade/application crates compose protocol, engine, and platform.
- Facade strict APIs require an engine-issued current accepted bound;
  diagnostic APIs expose the conditional claim, condition, assessment,
  verified-derivation status, per-atom support basis, deadline, reasons,
  assurance, and non-claims without a trusted boolean. Strict virtual-clock
  reads enforce the exact monotonic-domain deadline using conservative
  intervals even without a writer. Linearization-time results expose
  `observed_at`/`valid_until`; type-distinct through-completion results require
  current reviewed WCET capability.
- All generic source fusion, servo, and holdover algorithms live only in
  engine.
- Leap-candidate structure and pure validation live in core; generic evidence
  lifecycle/provenance uses shared source types; leap authority, correlation,
  diversity, and quorum live only in engine; hosted concurrent publication
  lives only in the composition layer.
- Core raw leap-model replacement is isolated and cannot publish
  `TrustedClock` or default-facade state; only an opaque engine-issued admitted
  handoff reaches composition, where its bindings are rechecked with commit.
- Raw EOP and scale-offset snapshots are likewise isolated; only their opaque
  policy-issued admitted proofs reach concurrent default-clock publication.
- Core owns raw EOP/offset structures and the protocol-neutral untrusted
  `RetrievalClaim`; platform implementations emit only those claims. Engine's
  provider-neutral verifier alone creates opaque `ArtifactIntegrityEvidence`
  without granting source authority, or distinct
  `ConfiguredPlatformTrustEvidence` for non-cryptographic OS trust. Engine
  applies configured source authority/role only when constructing admitted
  values and never depends on platform; facade composes policy/default
  publication without recreating verification or admission.
- Generic interval quorum, falseticker rejection, clustering, combining, and
  diversity are engine primitives implemented before NTP composition; NTP
  crates own association/filter metadata but no copy of those algorithms.
- Protocol crate feature sets contain no clock-adjustment or privileged
  authority feature.
- The helper and daemon share the canonical pre-daemon policy-ceiling and
  discipline-audit types; neither may introduce a private replacement schema,
  and daemon configuration may only narrow the helper ceiling.
- Monotonic values and lifecycle events use shared core domain/generation
  types; protocol crates do not invent private fork/checkpoint handling.
- `no_std` concurrency selects single-thread, target-atomic, caller critical-
  section, or explicitly supported ISR profiles; unavailable atomics are not
  hidden behind an unbounded lock.
- Navheim never depends on Mundilfari, preventing an integration cycle.
- Stable crates do not expose experimental-draft types.
- Non-generated Rust files may not exceed 500 lines.
- Review for a split begins near 300 lines.
- Every production Rust source file in a published crate has exactly one
  machine-checked implementation-evidence record with governing requirements
  and linked tests.
- Feature flags do not silently enable networking, insecure legacy behavior,
  a runtime, privileged operations, or system-clock modification.
- Capability APIs distinguish code compiled, resource available, caller
  authorized, and component healthy; a Cargo feature proves only the first.
- Secret-memory APIs report redaction, zeroization, page locking, core-dump
  exclusion, hardware/non-exportable keys, and external-key operations as
  separate provider/platform capabilities; container types imply none of them.

The local gate is:

```bash
scripts/validate-modularity-policy.sh check
```
