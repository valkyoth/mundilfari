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
- External condition identifiers decode only to unresolved core type-state;
  exact content or an immutable trusted registry generation must resolve them
  before any hard claim, engine, persistence, IPC, C, or WASM consumer.
- Canonical condition resolution grants no runtime trust. Engine alone owns
  bounded `VerifiedBoundDerivation` construction, snapshot-consistent current
  evidence assessment, and `PolicyAcceptedHardBound` construction. Exact
  per-atom support basis remains visible; derivation/condition/assessment loss
  invalidates all downstream consumers through the generic lifecycle and
  generation graph.
- Consensus, servo, and holdover live in `mundilfari-engine`.
- Safe OS, transport, timestamp, PHC, PPS, and device wrappers live in
  `mundilfari-platform`.
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
  reads enforce the exact monotonic-domain deadline even without a writer.
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
