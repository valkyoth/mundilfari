# Mundilfari Release Plan To 1.0

Status: planning document

This plan is intentionally granular. Time bugs can invalidate certificates,
leases, logs, databases, authentication, distributed ordering, and physical
control, so each milestone must be small enough to review, test, pentest, and
stop cleanly before tagging.

The list is not a maximum. Split a milestone or add patch versions whenever
work exceeds one safe review pass. Every stable-baseline registry entry must be
implemented or carry a documented impossible/unavailable status before
`1.0.0`.

The machine-enforced review ceiling is 16 top-level deliverable groups and 180
lines from one milestone heading to the next. These are hard ceilings, not
targets: a smaller milestone is still split when it contains independently
reviewable state machines, trust boundaries, or conformance decisions.
Integration and audit gates may spend their budget primarily on verification,
but receive no numerical exemption.

Tags use:

```text
v0.N.0       milestone release
v0.N.P       scoped subdivision or correction for milestone N
v1.0.0-rc.N exact production candidate
v1.0.0       first serious production-ready release
```

## Release Principles

Every release requires:

- one clear definition of done;
- one independently standardized protocol/profile family or one algorithmic
  control unit per implementation stop; a tightly coupled exception names its
  normative coupling and is split again if its state/security/conformance
  evidence can be reviewed independently;
- official specification revisions and verified errata for changed protocols;
- bounded positive, negative, malformed, state, rollover, and resource tests;
- documented security impact, limitations, and platform/no_std capability;
- current dependency and tool review;
- release notes and exact SBOM evidence;
- exact-commit pentest, remediation, and clean retest before tagging;
- no hidden dependency on one machine, private path, or inaccessible fixture.

Mundilfari implements generic time semantics and every Mundilfari-owned
time-protocol behavior itself. Reviewed external crates may provide generic
TLS, cryptography, or OS bindings; they do not own NTP, NTS, PTP, generic time
scales, clock algorithms, or protocol security policy. Navheim is the explicit
exception for GNSS interpretation and is used only through
`mundilfari-navheim`; Mundilfari never duplicates its decoders or GNSS trust
decisions.

## Required Milestone Format

Every release below has:

- `Status`;
- one `Goal`;
- bounded `Deliverables`;
- release-specific `Verification`;
- observable `Exit criteria` ending with the exact implementation-stop and
  pentest handoff sentence.

Release-specific verification is additive to the common gate:

```bash
scripts/checks.sh
cargo deny check
cargo audit
scripts/generate-sbom.sh --check
```

The version release gate also runs the live latest-Rust, latest-tool, and
latest-GitHub-Action checks.

## Pentest Before Tags

Every tag, including patches and release candidates, requires:

1. implementation stops on a committed candidate;
2. common and version-specific gates pass;
3. temporary findings are recorded in root `PENTEST.md`;
4. findings are fixed, documented, and retested;
5. temporary `PENTEST.md` is removed;
6. GitHub CI and CodeQL default setup pass on the reviewed commit;
7. permanent `security/pentest/vX.Y.Z.md` records `Status: PASS`, the exact
   40-character `Reviewed-Commit`, tester, scope, and date;
8. only that permanent report is committed as the direct child of the reviewed
   commit;
9. `scripts/validate-release-readiness.sh vX.Y.Z` passes;
10. tagging and publishing occur only when explicitly requested.

No milestone may mark its own pentest complete during implementation.

## Crates.io And Repository-Only Packages

Published libraries use independent semantic versions after the foundation,
and `release-crates.toml` records exactly which crates changed. Publish order
is always dependency order. The facade is published last.

Crates.io packages include:

- the `mundilfari` facade;
- shared library crates needed by downstream users;
- independently useful protocol, format, profile, and platform crates;
- a downstream testkit only if it has a stable public use case.

Repository-only `publish = false` packages include:

- `xtask`, release validators, and fixture importers;
- fuzz, simulator, differential, benchmark, and hardware-lab drivers;
- CLI/daemon packaging helpers until their public release milestone;
- internal compliance reports and licensed-standard tooling.

The root README and facade-crate README remain byte-identical.

## Phase 0: Repository And Governance

### v0.1.0 - Repository Foundation

Status: implementation candidate; pentest not yet performed.

Goal: establish the serious Rust workspace and policy baseline.

Deliverables:

- pinned Rust `1.97.1`, published-crate MSRV `1.90.0`, and compatibility table;
- `no_std` facade, core, engine, and platform crate boundaries;
- MIT OR Apache-2.0 licensing, CI, dependency policy, security policy, and
  release tooling;
- implementation, protocol, standards, threat, modularity, unsafe, toolchain,
  supply-chain, release-note, and pentest documentation;
- checksum-locked RFC source corpus, external-source registry, and ignored
  local-only standards vault with offline validation;
- Linux, Windows, BSD, macOS, Android, iOS, and future Aesynx architecture.

Verification:

- common gate, README identity, package dry-runs, and the full Rust-version
  compatibility matrix;
- repository metadata and script self-tests.

Exit criteria:

- a contributor can identify scope, non-claims, crate publishing rules,
  security posture, and release process from repository documentation;
- `v0.1.0 implementation stop reached. Run pentest for this exact commit.`

### v0.2.0 - Registry And Provenance

Status: planned.

Goal: make protocol completeness and standards provenance machine-auditable.

Deliverables:

- versioned protocol, standard, errata, license, and document-hash registries;
- promote the `v0.1.0` RFC and external-source acquisition baseline into
  clause-level requirement and errata disposition ledgers;
- stable domain-qualified requirement IDs with bidirectional links among
  normative clauses/architecture decisions, owning crate/module,
  implementation items, positive/negative/property/fuzz/conformance/HIL
  evidence, and explicit exclusions/non-claims;
- recursively inventory every normative reference from each admitted source
  and classify it as implemented, provider-owned, registry/procedure-only,
  syntax/transport support, superseded, not applicable, or blocked;
- require every normative-reference disposition to name its consumer,
  reviewed revision/hash, owning crate or provider boundary, milestone, and
  rationale; unclassified transitive references block implementation;
- retain exact RFC Editor bytes in `rfc/`, keep every non-RFC document byte in
  ignored `standards/private/`, and prohibit network access from normal gates;
- exact per-document records for every family entry, including amendments,
  corrigenda, interpretation documents, profiles, registries, and official
  errata; a family or bundle name is never sufficient for implementation;
- status classes including stable, historic, active draft, monitored proposal,
  licensed, partially documented, historical-evidence-only,
  implementation-blocked, unavailable, and proprietary-undocumented;
- separate `WireComplete`, `BehavioralComplete`, `OperationalComplete`, and
  `ConformanceValidated` evidence levels without upward inference;
- separate access, redistribution, implementation, and conformance states so
  possession of a document cannot be mistaken for protocol completion;
- schema validation and duplicate identifier/revision rejection;
- public completeness and legitimate-access policy.

Verification:

- registry round trips, malformed schema corpus, duplicate/conflict tests, and
  comparison with `PROTOCOLS.md`;
- orphan requirement, implementation, test, proof/fuzz/HIL evidence, and
  non-claim mutations in both trace directions;
- generated transitive-reference closure fixtures covering cycles, updates,
  obsoletes, provider boundaries, and a newly introduced unclassified
  normative reference;
- corrupt/missing/extra RFC files, unauthorized URLs, checksum changes,
  duplicate roles, unassigned milestones, local-vault tracking attempts, and
  restricted-document publication tests.

Exit criteria:

- every initial registry entry and transitive normative dependency has an
  exact status, disposition, consumer, and roadmap assignment;
- every implementation-bound requirement has a stable ID and no orphaned
  source, implementation, test/evidence, exclusion, or non-claim edge;
- every source needed through the next implementation pass has an exact
  legitimate artifact, reviewed errata state, and clause dispositions;
- `v0.2.0 implementation stop reached. Run pentest for this exact commit.`

### v0.3.0 - Security And Engineering Policy

Status: planned.

Goal: turn the threat model and coding rules into enforced repository policy.

Deliverables:

- parser, panic, arithmetic, allocation, logging, secret, unsafe, and
  discipline-authority policies;
- manifest/metadata-driven dependency-layer, feature-authority, unsafe, and
  500-line validators that automatically cover future workspace crates;
- protocol claim, accuracy claim, and conformance claim checks;
- fail-closed per-source implementation evidence: reviewed implementation
  hashes, governing documents, requirement locators, exact normative
  hashes/clauses/errata for protocol work, and concrete tests linked from
  every requirement;
- security-review templates for standards and dependencies.

Verification:

- policy validator unit fixtures covering every accepted and rejected case;
- mutation tests for unregistered implementation files, missing requirements,
  unknown or changed standards, unreviewed clauses/errata, nonexistent tests,
  and requirements without linked tests;
- deliberate layer, file-size, feature, and unsafe violations fail closed.

Exit criteria:

- no published implementation source can enter the workspace without
  requirement/specification review and linked test evidence;
- `v0.3.0 implementation stop reached. Run pentest for this exact commit.`

## Phase 1: Exact Time Foundations

### v0.4.0 - Checked Integer Domains

Status: planned.

Goal: establish checked signed/unsigned arithmetic for time work.

Deliverables:

- explicit checked add, subtract, multiply, divide, negate, and conversion
  APIs;
- overflow and division-by-zero errors without panics;
- construction invariants and redacted structured errors.

Verification:

- exhaustive small-domain tests, integer boundaries, property invariants, and
  debug/release equivalence.

Exit criteria:

- no foundational time arithmetic relies on wrapping or ambient overflow mode;
- `v0.4.0 implementation stop reached. Run pentest for this exact commit.`

### v0.5.0 - Wide Intermediate Arithmetic

Status: planned.

Goal: provide audited wide intermediates for exact conversion.

Deliverables:

- internal `U256` and `I256` limbs, comparison, shifts, multiply, and division;
- canonical conversion and checked narrowing;
- wide fraction, interval, and rate intermediates without flattening a full
  instant into total `i128` attoseconds;
- no secret-dependent use claim.

Verification:

- differential big-integer oracle tests outside the runtime graph, exhaustive
  reduced-width models, and boundary vectors.

Exit criteria:

- fraction and interval math can avoid premature truncation or overflow;
- `v0.5.0 implementation stop reached. Run pentest for this exact commit.`

### v0.6.0 - Duration And Frequency

Status: planned.

Goal: define normalized signed duration and frequency-ratio domains.

Deliverables:

- attosecond-resolution duration with checked normalization;
- fixed-point frequency ratio and parts-per-billion adjustment;
- explicit rounding direction and quantization loss.

Verification:

- normalization, sign, zero, extreme, reciprocal, and round-trip properties.

Exit criteria:

- servo and conversion code can use typed values instead of raw integers;
- `v0.6.0 implementation stop reached. Run pentest for this exact commit.`

### v0.6.1 - Canonical Identity Kernel

Status: planned.

Goal: define one allocation-free structural identity and content-addressing
contract before claims, recipes, conditions, models, or origins depend on
digests.

Deliverables:

- core-owned `CanonicalIdentityV1` preimage encoder with domain-separated tags
  for claim, recipe, condition, model, and origin identities; every preimage
  binds identity-profile and semantic-schema generation, exact type/domain,
  units, scale, sign/normalization, endpoint inclusion/unbounded state,
  operation/proof rule, condition/model/origin references, and bounded
  length-delimited content;
- canonical signed/integer/enum/sequence encoding and canonical ordering for
  commutative operations using digest plus full structural-byte tie-breaker;
  input permutation cannot alter identity and equal digests never decide an
  ambiguous order without structural comparison;
- fixed `IdentityDigestV1 = SHA-256` profile with an explicit algorithm
  identifier, domain prefix, and first-party no_std public-data-only
  implementation reviewed against the exact `v0.2.0`-admitted
  `nist-fips-180-4-upd1` source. The announced future NIST revision is monitored
  and refreshed at `v0.165.0`; no unreleased draft silently changes V1;
  this is stable content addressing, not MAC/authentication, secret handling,
  collision-resistance assurance for hostile authority, or a substitute for
  `v0.24.1` generic cryptographic providers;
- identity equality, registry lookup, interning, and cache use require digest
  match plus canonical structural comparison; a digest collision returns a
  typed collision/conflict result and never aliases, overwrites, selects, or
  grants authority to different content;
- caller-buffer/streaming encoding with fixed byte/item/depth/work limits,
  required-length reporting, and atomic short-buffer failure;
- Rust `Hash`, `TypeId`, memory layout/padding, pointer/address, serde output,
  debug/display formatting, locale, platform endianness, or randomized process
  state are forbidden identity inputs;
- `v0.7.1`–`v0.7.3` reuse this exact identity profile, while `v0.22.1`
  wraps its canonical value encoding without creating a second representation
  and `v0.24.1` cannot silently change an existing identity algorithm/profile.

Verification:

- SHA-256 official/KAT and incremental/one-shot tests; golden preimages and
  identities across Rust `1.90.0..=1.97.1`, endian/word-width targets, no_std,
  and independent reference encoders;
- exhaustive type/unit/scale/sign/normalization/open-closed-unbounded/operation/
  condition/schema separation, commutative permutations and equal-digest
  structural tie-breaks, forced-collision mock paths, noncanonical aliases,
  every byte/item/depth/work limit, and short-buffer atomicity;
- compile/static tests forbid Rust layout/hash/serde/debug identity shortcuts
  and prove generic crypto-provider selection cannot mutate V1 identities.

Exit criteria:

- every later identity/digest has one stable canonical preimage and collision
  rule before a hard claim can be constructed;
- `v0.6.1 implementation stop reached. Run pentest for this exact commit.`

### v0.7.0 - Atomic Instant

Status: planned.

Goal: implement the continuous canonical instant.

Deliverables:

- private signed seconds plus normalized attoseconds where seconds is the
  mathematical floor, including negative fractional instants;
- exact zero at `1958-01-01 00:00:00 TAI`, with every represented second an
  SI second on the continuous TAI coordinate; the type is not scale-neutral,
  UTC, POSIX, monotonic, or a realization identifier;
- checked instant/duration arithmetic and ordering;
- coordinate equality separated from realization/source/model/uncertainty
  evidence, and no implicit `SystemTime` conversion.

Verification:

- origin/epoch vectors, invariant, negative one-half representation,
  normalization, subtraction, negation, ordering, coordinate-equality versus
  evidence cases, extreme-range, and arithmetic tests.

Exit criteria:

- one continuous internal timeline exists without erasing native wire values;
- `v0.7.0 implementation stop reached. Run pentest for this exact commit.`

### v0.7.1 - Fundamental Intervals And Uncertainty Classes

Status: planned.

Goal: provide stable source-neutral interval and uncertainty-class types before
era resolution, fractions, EOP, or other conversion models require them.

Deliverables:

- generic instant and duration interval algebra with explicit
  `Endpoint<T> { Included(T), Excluded(T), Unbounded }` semantics; every open,
  closed, and half-open combination is represented directly without adding or
  subtracting a domain quantum;
- canonical empty and finite interval forms: `(t,t)`, `[t,t)`, and `(t,t]`
  are empty, `[t,t]` is a singleton, and adjacent excluded/included endpoints
  retain exact set meaning across discrete attosecond and rational domains;
- checked metric width is endpoint subtraction and never cardinality or an
  endpoint-adjustment trick; containment and intersection preserve endpoint
  inclusion exactly at numeric extremes;
- unbounded endpoints exist for algebra and coverage calculations, but
  `FiniteInterval<T>` is required in trusted-time estimates, observations,
  era contexts, and admission expiries;
- non-interchangeable `BorrowedHardBoundClaim<'arena, T>` and
  `StatisticalRange<T>` wrappers; the borrowed claim states mathematical
  containment under a source-neutral `BoundAssumptionsId`, not proof that a
  source is honest or authoritative, while an early `StatisticalRange` is
  non-guaranteed and cannot be promoted; the identifier is an opaque reference
  to immutable assumption content, not a caller-selected label, and its
  complete composition algebra follows in `v0.7.2`;
- every root `BorrowedHardBoundClaim<'arena, T>` constructor stores a paired,
  core-owned,
  immutable `UnverifiedBoundDerivation<T>` recipe in its admitted derivation
  arena, binding a bounded
  `ClaimOriginId`, the exact included/excluded output endpoints, claim digest,
  operation=`Root`, and condition identity. The recipe is material for later
  engine verification, not proof, source provenance, authentication, honesty,
  authority, or current support, and construction succeeds only when the
  recipe is stored and its mandatory handle is attached;
- every claim/origin/recipe digest is computed only from the exact `v0.6.1`
  canonical identity profile; canonical claim comparison and arena interning
  compare full structure after digest match and surface collisions explicitly;
- `BorrowedHardBoundClaim<'arena, T>` contains a mandatory private typed
  `DerivationHandle<'arena, T>` rather than returning a droppable
  `(claim, recipe)` pair. Arena construction introduces a fresh invariant
  generative lifetime brand that cannot be named by callers or escape its
  scoped owner; the handle binds that brand, store generation, node
  generation/index, output domain/type, and recipe digest. An address, pointer,
  storage-buffer location, caller label, randomized hash seed, or wrapping
  counter is never arena identity;
- no_std uses a caller-owned fixed-capacity `DerivationArena` over supplied
  slots/buffers; alloc-enabled use has a fallible explicitly bounded arena and
  never unconditional growth. Canonically interned immutable DAG nodes share
  common inputs to avoid exponential copying, and all mutation/eviction rotates
  checked nonwrapping store/node generations without making a live handle refer
  to different content. Generation exhaustion permanently faults that arena or
  requires construction under a completely new generative brand; destruction
  and same-address reinitialization cannot validate an old branded handle;
- mutable arenas require exclusive write access and are not `Sync`; traversal
  resolves under an immutable read lease or frozen pinned snapshot that blocks
  eviction/reinterning until release. Read-only/frozen views are `Send`/`Sync`
  only when their backing storage/node types and type-level synchronization
  strategy prove those properties; later target concurrency profiles must
  preserve this boundary. Handles confer no storage access by themselves and
  inherit the brand/view transfer restrictions;
- comparison APIs deliberately separate `same_geometry()` for endpoints,
  `same_conditional_claim()` for the canonical interval/condition/claim
  preimage carried by the value, and fallible
  `try_same_derivation(left_lease, right_lease)` for complete recipe-DAG
  equivalence across arenas. Arena-dependent representations do not implement
  infallible semantic `Eq`/`Hash`; digest-keyed interning/caches retain
  canonical collision buckets and return typed stale-handle/collision/
  capacity failures. Cross-store equivalence uses the fallible operation or
  explicit bounded canonical import/reinterning;
- heterogeneous recipe nodes and edges explicitly tag input/output domains
  (instant, duration, rational, scale-specific, model, and condition) and
  validate operation-specific edge signatures. Geometry-only
  `FiniteInterval<T>` remains available, but it cannot enter hard-claim
  transformation, verification, policy-acceptance, or strict-time APIs;
- serialization exports the complete reachable bounded canonical derivation
  record, never the process-local arena handle/store identity; external decode
  remains the unverified `v0.7.3` type-state;
- typed saturated/invalid outcomes rather than sentinel endpoints;
- no source authority, authentication, observation provenance, covariance,
  confidence, error-budget composition, midpoint preference, or implicit
  statistical-to-hard conversion;
- `v0.14.0` extends these stable primitives with asymmetric uncertainty,
  covariance/confidence/model evidence, richer algebra, and observation use
  without replacing the foundational interval representation.

Verification:

- all open/closed/half-open/unbounded combinations, adjacent-but-disjoint
  intervals, `(t,t)`/`[t,t)`/`(t,t]` empty normalization, `[t,t]` singleton,
  discrete-attosecond versus exact-rational domains, numeric extremes, checked
  width without plus/minus-quantum adjustment, containment/intersection
  properties, finite-estimate enforcement, instant-versus-duration
  non-substitution, compile-fail hard/statistical mixing/promotion, no_std/MSRV,
  paired root-recipe creation, endpoint/condition/origin/digest substitution,
  recipe-drop/detachment refusal, canonical-identity collision handling,
  API/type size and stack-use reports, zero/full arena and allocation failure,
  interning/DAG sharing, destruction/recreation in the same storage/address,
  stale-brand and near-generation-exhaustion refusal, eviction during leased
  traversal, concurrent import versus read/write leases, mutable/frozen/
  read-only `Send`/`Sync` compile tests, stale/cross-store/cross-generation
  handles, heterogeneous/wrong-domain edges, long shared chains, identical
  geometry with different conditions/derivations, identical recipes in
  different arenas, stale handles during fallible comparison, forced digest
  collisions and collision-bucket cache lookup, complete-record export without
  handle leakage, and dependency tests proving the opaque origin identity does
  not introduce later provenance/observation coupling.

Exit criteria:

- every earlier era, fraction, and conversion model can use one stable bounded
  interval vocabulary without inventing provisional uncertainty types;
- every root hard claim retains the bounded non-authoritative material required
  for later exact derivation verification through an enforceable typed handle
  and bounded caller-controlled storage model;
- `v0.7.1 implementation stop reached. Run pentest for this exact commit.`

### v0.7.2 - Bounded Hard-Bound Condition Algebra

Status: planned.

Goal: express the exact logical condition under which every hard containment
claim holds, without flattening intersection, union, conversion, or Byzantine
fault guarantees into one incorrect conjunction.

Deliverables:

- bounded immutable atoms and a canonical `BoundCondition` expression language
  with `Atom(AssumptionId)`, `All`, `Any`, `AtLeast`, `AtMostFaulty`, and
  `Derived { rule: ProofRuleId, inputs }` forms; every collection, integer, and
  proof-rule reference has a fixed bound;
- `BoundAssumptionsId` is the content-addressed identity of the complete
  canonical condition, binding digest algorithm, namespace, semantic-schema
  generation, proof-rule-registry generation, and canonical content; callers
  cannot select an identifier that aliases a different expression;
- exact condition identity is part of borrowed-claim evidence, serialization
  contracts, and cache keys under the `v0.7.1` `same_conditional_claim()`
  semantics, while geometric interval comparison remains separately queryable
  and complete derivation equivalence remains fallible and lease-backed;
- interval intersection constructs `All(A, B)`; union or convex hull constructs
  `Any(A, B)`; widening that adds no new dependency retains the input
  condition; conversion/projection constructs `All(input, model, rounding)`;
- quorum and consensus use reviewed `AtLeast`, `AtMostFaulty`, or `Derived`
  rules tied to exact policy, membership, diversity/correlation, and fault-model
  generations; they never claim that every contributing source assumption must
  hold when the proved guarantee is an `n`/`f` threshold;
- simplification, deduplication, normalization, and contradiction detection
  use only versioned reviewed sound rewrite/proof rules; an implementation
  cannot replace `Any` with `All`, discard a branch, invent an implication, or
  reduce a threshold from geometry alone;
- maximum expression depth, node count, fan-out, atom count, proof-rule inputs,
  and evaluation/rewrite work, with typed capacity, incompatibility, unknown-
  rule, generation/schema, and digest-collision failures rather than silent
  strengthening, weakening, truncation, or fallback;
- every claim-transforming interval operation automatically composes the
  `v0.7.1` `UnverifiedBoundDerivation<T>` recipe with exact ordered input claim
  and recipe digests, input/output endpoints, operation/proof rule, rounding
  direction/policy, model identity/generation where applicable, input and
  canonical output conditions, and rewrites; no API returns a transformed hard
  claim while omitting its recipe;
- transformation resolves every typed handle in one explicitly selected arena,
  under the required read/write lease, validates heterogeneous edge signatures,
  computes condition/claim/recipe identities with `v0.6.1`, interns the
  canonical output DAG node, and only then returns a new handle-bearing claim.
  Cross-store composition requires explicit bounded canonical
  import/reinterning and never trusts a foreign handle;
- recipes have independent fixed depth, node, fan-out, input, byte/storage,
  traversal, cycle-detection, and later verification-work bounds. Internal
  construction is acyclic; overflow, attempted cycles, unavailable inputs, or
  capacity exhaustion returns a typed failure rather than truncating,
  flattening, or replacing the recipe with a digest-only claim;
- the protocol-neutral derivation report projects this complete
  non-authoritative recipe plus policy and membership generations where
  applicable and explicit non-claims for later uncertainty, quorum, and
  consensus evidence;
- `v0.14.0` may enrich assumption content and statistical conversion policy,
  but it reuses this condition algebra rather than reconstructing assumptions.

Verification:

- truth-table/property tests for intersection=`All`, union/hull=`Any`,
  conversion requirements, `AtLeast`, `AtMostFaulty`, and reviewed derived
  rules; canonical ordering/deduplication, identifier stability/collision,
  caller-selected/substituted identifiers, incompatible atoms, unknown rules,
  conflicting policy/membership/correlation/schema generations, and every
  depth/node/fan-out/work exhaustion boundary;
- adversarial rewrite tests prove no simplifier strengthens or weakens a
  formula, and engine fixtures prove `n`/`f` results do not conjunct every
  source claim or collapse a threshold to an unaudited boolean;
- recipe property tests cover every root/intersection/union/hull/widening/
  conversion/projection path, exact endpoint and digest binding, canonical
  input order, rounding/model/condition substitution, cycle attempts, and
  every independent depth/node/fan-out/storage/traversal/work boundary;
- arena tests cover canonical DAG reuse, cross-store import/reinterning,
  eviction/generation/read-lease races, concurrent imports, heterogeneous edge
  signatures, long diamond DAGs, and failure atomicity when output identity/
  interning exhausts capacity.

Exit criteria:

- no hard-bound operation can produce a geometrically plausible claim while
  misstating the logical condition required for containment or discarding the
  complete bounded recipe for its exact endpoint derivation;
- `v0.7.2 implementation stop reached. Run pentest for this exact commit.`

### v0.7.3 - Untrusted Bound-Condition Resolution

Status: planned.

Goal: prevent serialized, persisted, IPC, C, WASM, or network-derived
assumption identifiers or derivation records from bypassing canonical
condition/recipe construction or later engine verification.

Deliverables:

- external decoding produces only `UnresolvedAssumptionReference` and
  `UnresolvedBoundCondition` values and, for derivation material, only a
  bounded `UnverifiedBoundDerivationRecord`;
  no deserializer may directly create `AssumptionId`, admitted
  `BoundAssumptionsId`,
  `ResolvedBoundCondition`, `BorrowedHardBoundClaim`,
  `OwnedHardBoundClaim`, or any engine-verified derivation;
- explicit resolution checks digest algorithm, namespace, semantic-schema and
  proof-rule-registry generations, canonical content, identifier/content
  equality, collision handling, rule availability, expression canonicality,
  depth/node/fan-out/capacity/work bounds, and registry rollback/freshness;
- successful resolution returns an opaque `ResolvedBoundCondition` carrying
  the exact canonical condition and immutable registry generation used; cache
  entries key the complete resolution context and cannot upgrade unresolved
  references;
- derivation-record resolution checks complete referenced claims/inputs,
  endpoints, digests, operations, rounding, models, conditions, canonical
  ordering, acyclicity, and every recipe bound, then returns only the
  non-authoritative core `UnverifiedBoundDerivation<T>`; resolution never
  asserts mathematical correctness or runtime authority;
- every record carries complete `v0.6.1` canonical structural preimages and
  identities for the reachable DAG, not arena/store handles or digest-only
  references. Decode/import recomputes identities, performs structural
  collision comparison, validates heterogeneous edges, and atomically interns
  into the caller-selected bounded arena or fails without a partial claim;
- identifier-only encodings are accepted only when the receiver already holds
  and verifies the exact immutable registry generation and canonical content;
  otherwise the complete bounded canonical condition and required rule
  references accompany the identifier;
- trusted immutable registries have explicit authority, integrity, generation,
  rollback-capability, replacement, and withdrawal behavior; a registry name
  or caller-supplied generation is not authority;
- this early core resolver accepts caller-supplied already-admitted immutable
  registry evidence and owns no storage, cryptography, platform, or engine
  authority; production provider assurance/persistence arrives through
  `v0.24.1` and `v0.39.1` without changing the resolution type-state;
- `v0.22.1` canonical schema, `v0.39.1` persistence, `v0.140.1` external
  bindings, and every later IPC/C/WASM/network consumer reuse this type-state
  boundary without adding direct identifier deserialization.

Verification:

- forged identifiers, valid identifiers paired with different content,
  digest-algorithm/namespace/schema/rule-generation substitution, registry
  rollback/replacement/withdrawal, unknown proof rules, noncanonical and
  over-deep expressions, collision handling, identifier-only missing-registry
  cases, cache poisoning/cross-generation reuse, and compile-fail direct
  deserialization/construction tests, plus dependency tests proving no early
  crypto/storage/platform/engine coupling;
- canonical schema, persistence, IPC, C, and WASM fixtures prove decoding
  remains unresolved until the complete bounded resolution succeeds;
- malformed/truncated/spliced derivation records, cycles, missing inputs,
  endpoint/operation/rounding/model/condition substitution, and all recipe
  depth/node/fan-out/storage/work limits; handle/store injection,
  digest-without-structure, forced collisions, heterogeneous edge confusion,
  arena import exhaustion, and partial-intern rollback.

Exit criteria:

- no external identifier or serialized hard claim obtains trusted condition
  semantics without exact content and registry resolution, and no serialized
  derivation becomes proof or authority before complete engine verification;
- `v0.7.3 implementation stop reached. Run pentest for this exact commit.`

### v0.7.4 - Borrowed And Owned Hard-Claim Ownership

Status: planned.

Goal: preserve zero-allocation lifetime safety while giving hosted engines,
returned clocks, async tasks, and foreign-language contexts a non-self-
referential ownership boundary.

Deliverables:

- “hard-bound claim” is documentation-only shorthand for
  `BorrowedHardBoundClaim<'arena, T>`, `OwnedHardBoundClaim<T>`, or
  `HardBoundClaimView<'view, T>`; no third public `HardBoundClaim` type, alias,
  trait, or enum is introduced;
- `BorrowedHardBoundClaim<'arena, T>` remains the zero-allocation no_std form
  and cannot outlive its invariant generative arena brand; compile-time
  lifetimes, not runtime checks or leaked storage, enforce this boundary;
- fallible alloc-enabled `OwnedHardBoundClaim<T>` owns an opaque bounded frozen
  derivation arena or shares it through an Arc-style owner when the target has
  the required pointer-atomic capability. Targets without that capability use
  unique ownership or an explicit caller synchronization profile; no hidden
  global allocator, unbounded growth, unconditional `Arc`, or `Box::leak`
  fallback is permitted;
- borrowed-to-owned `try_promote()` canonically exports and atomically
  imports/reinterns the complete reachable derivation DAG into fresh owned
  bounded storage, recomputes `v0.6.1` identities, performs full structural
  collision checks and heterogeneous-edge validation, and returns failure
  without a partial owner. It never copies, trusts, transmutes, or lifetime-
  extends a process-local handle/brand;
- bounded `try_promote_set(roots, capacity)` canonically interns multiple
  borrowed roots into one `OwnedHardBoundClaimSet<T>` and one frozen owner,
  preserving common condition/model/recipe nodes across roots. Root count,
  input bytes, unique nodes/edges/canonical bytes, depth, and total work are
  bounded before/through admission, and allocation/collision/capacity failure
  is atomic with no partially promoted root;
- the owned set exposes stable per-root claim views/identities, per-root
  reachable-resource reports, and one deduplicated total-owner resource report.
  Duplicate roots alias the same canonical root entry without duplicating DAG
  storage, and dropping a root view cannot invalidate another root;
- frozen sets expose no in-place root removal or compaction. Dropping or no
  longer retaining one root view leaves the owner and its nodes unchanged until
  the last owner is destroyed; producing a subset and reclaiming space requires
  fallible bounded `try_compact_roots(retained_roots, capacity)` into a new
  canonical frozen owner with atomic rollback. Batch root/node/byte/work limits
  prevent one untrusted window/queue from forcing unbounded retention;
- both forms expose a lease-scoped `HardBoundClaimView<'view, T>` for common
  core algorithms; owned-to-view borrowing does not manufacture a new arena
  identity, and promotion does not add evidence, verification, authority,
  acceptance, or stronger containment semantics;
- owned frozen arenas cannot evict or reintern; thaw/edit requires a new
  bounded arena and canonical promotion, so an `OwnedHardBoundClaim` never
  observes mutable backing content. Clone/share, drop, and last-owner
  destruction semantics are explicit and preserve bounded resource reports;
- the ownership contract reserves engine promotion: `v0.60.3` verification
  produces source-arena-independent `VerifiedBoundDerivation<T>`, and
  `v0.60.6` policy admission produces `PolicyAcceptedHardBound<T>` carrying the
  required canonical identities and lifecycle/generation dependencies, never a
  borrow or handle into the unverified source arena;
- “source-arena-independent” is exact: hosted forms own all bounded engine
  state; no_std forms either contain it inline or use the one checked storage
  reference `EngineProofHandle<'engine, K, T>`, where sealed `K` distinguishes
  verified-derivation from policy-accepted storage. The public semantic
  projections `VerifiedBoundDerivationRef<'engine, T>` and
  `PolicyAcceptedHardBoundRef<'engine, T>` each contain the corresponding
  kind-specific handle and resolve it only through the matching checked engine
  store/read lease. They allocate no parallel store, identity, generation, or
  ownership mechanism. Engine-storage lifetime, brand, nonwrapping generation,
  destruction, kind mismatch, and stale-handle rules are public; none of these
  names means undocumented `'static` or a hidden pointer into caller storage;
- dropping a borrowed or owned source arena after successful engine promotion
  does not itself invalidate the engine-owned proof/token; evidence, model,
  policy, source, lifecycle, assessment, and deadline generation changes still
  invalidate it. Dropping before completed promotion leaves no verified or
  accepted value;
- no_std engines explicitly borrow caller-provided arena and engine storage and
  expose those lifetimes. The std/alloc facade owns only frozen promoted claim
  state and engine-owned proof/token state, avoiding self-referential structs;
- external schemas continue to carry complete unverified canonical records,
  never either Rust ownership wrapper. FFI context ownership and language-
  handle destruction rules are completed at `v0.140.1`/`v0.144.0`.

Verification:

- compile-fail borrowed-claim escape, locally branded return, self-referential
  owner construction, lifetime transmute, and use-after-source-drop cases;
- successful/failing borrowed-to-owned promotion, source drop after promotion,
  drop before promotion, forced digest collision, cross-store import,
  zero/full capacity, allocation/import exhaustion, rollback atomicity, unique
  versus shared owner targets, cross-thread frozen ownership, clone/drop/last-
  owner destruction, and no_std no-alloc dependency tests;
- multi-root long shared chains/diamonds, duplicate/permuted roots, individual-
  versus-batch canonical identity equivalence, cross-root DAG sharing, per-root
  and deduplicated-total accounting, every root/node/byte/work limit, failure
  at each root with atomic rollback, root-view drop independence, retained
  unreachable nodes, bounded compaction, and compaction failure rollback;
- returned self-contained owned-state builder and `'static` closure/thread
  fixtures, plus placeholder async/ABI ownership fixtures consumed by the later
  facade/async/binding milestones.

Exit criteria:

- callers can choose an explicit borrowed or fallible owned storage model
  without self-reference, lifetime forgery, hidden leaking, or loss of the
  canonical derivation required for later engine verification;
- `v0.7.4 implementation stop reached. Run pentest for this exact commit.`

### v0.8.0 - Epoch And Era Framework

Status: planned.

Goal: make epoch identity and rollover resolution explicit.

Deliverables:

- typed epochs, custom epoch identifiers, and bounded `EraContext` carrying an
  admissible finite `v0.7.4`
  `HardBoundClaimView<'_, AtomicInstant>` with explicit endpoint semantics, the
  `v0.7.2` canonical condition identity, resolved through `v0.7.3` for any
  external context, and maximum-distance policy;
- every successful era-resolution hard claim preserves and extends the input
  `UnverifiedBoundDerivation` with the exact era context, raw/truncated value,
  resolver operation, selected era, output endpoints, and claim digest;
- resolver traits for RFC 868, NTP, PTP, broadcast, and device counters;
- a resolved-external-instant boundary for Navheim and other providers;
- ambiguity and missing-context errors.

Verification:

- before/at/after rollover vectors, ambiguous windows, negative epochs, and
  multiple-wrap rejection, plus recipe preservation and context/raw-value/
  selected-era/output substitution tests.

Exit criteria:

- no truncated timestamp silently chooses a nearest era;
- `v0.8.0 implementation stop reached. Run pentest for this exact commit.`

### v0.9.0 - Exact Fractions

Status: planned.

Goal: preserve and convert protocol-native fractions exactly.

Deliverables:

- binary, decimal, scaled-nanosecond, and bounded exact-fraction adapters;
- caller-selected rounding, exact rational quantum, and lower/upper residual
  `v0.7.4` `HardBoundClaimView<'_, Duration>` whose open/closed endpoints follow
  directed rounding without quantum adjustment and whose `v0.7.2`
  `All(input, model, rounding)` condition preserves every conversion and
  rounding precondition;
- every hard residual/conversion result extends the bounded
  `UnverifiedBoundDerivation` with exact rational input, output endpoints,
  quantum, directed-rounding policy, model generation, and claim digest;
- fixed maximum limb width, canonical sign location, positive nonzero
  denominator, and explicit reduced/unreduced invariants;
- bounded comparison, reduction, and conversion algorithms without
  cross-product overflow, attacker-selected arbitrary precision, or
  attacker-sized allocation;
- raw representation retention.

Verification:

- exhaustive reduced-width fractions, zero/maximum denominators, worst-case
  reduction work, comparison-overflow cases, official protocol examples,
  halfway rounding, maximum precision, monotonicity, and recipe quantum/
  rounding/model/endpoint substitution tests.

Exit criteria:

- NTP/PTP/media fractions convert without hidden precision claims;
- `v0.9.0 implementation stop reached. Run pentest for this exact commit.`

### v0.10.0 - Calendar Core

Status: planned.

Goal: implement calendar conversion needed by time protocols.

Deliverables:

- proleptic Gregorian, Julian, ordinal, and ISO-week dates;
- checked year ranges, leap-year rules, and weekday conversion;
- no time-zone or locale assumptions.

Verification:

- published calendar vectors, century/400-year boundaries, negative years,
  exhaustive cycles, and round trips.

Exit criteria:

- calendar conversion is first-party, bounded, and independent of `std`;
- `v0.10.0 implementation stop reached. Run pentest for this exact commit.`

### v0.11.0 - Scale Identity And Conversion Context

Status: planned.

Goal: establish stable scale identity and immutable conversion context without
implementing every scale family in one review pass.

Deliverables:

- stable identifiers for continuous, civil, protocol-encoding, and named
  externally resolved scales;
- the SI second and unit foundations reviewed from
  `bipm-si-brochure-9-v4.01`, with the exact locally locked revision recorded
  in the requirement ledger;
- one immutable versioned `ConversionContext`, never a general path-search
  graph, with explicit model generations and admissible data;
- every conversion API that returns or transforms a hard claim must consume
  and extend its `UnverifiedBoundDerivation` with the exact context/model
  generation, operation, rounding, endpoints, and output condition/digest;
- typed missing, stale, mixed-generation, unavailable, and unsupported
  conversion outcomes;
- no GNSS signal, navigation-message, receiver, or UTC-model interpretation.

Verification:

- scale-identity non-substitution, context generation replacement,
  mixed-generation rejection, missing/stale data, forbidden implicit
  conversion, and claim-recipe loss/context/model/rounding substitution tests.

Exit criteria:

- scale identity and model identity are explicit before any family conversion;
- `v0.11.0 implementation stop reached. Run pentest for this exact commit.`

### v0.11.1 - UT1 And Earth Orientation

Status: planned.

Goal: implement the EOP/UT1 model foundation needed for later UTC conversion
with source-neutral model metadata and classified uncertainty.

Deliverables:

- the official `iers-conventions-2010-tn36` model baseline, its official
  corrections register, and the distinction between the official release and
  non-definitive working updates reviewed and recorded;
- versioned Earth-orientation records and source-neutral `EopModelMetadata`
  carrying model/document identity, exact revision/content hash, validity,
  interpolation policy, and model generation without asserting source
  authority, authentication, retrieval history, or observation provenance;
- `v0.7.1` hard/statistical interval classification for EOP validity and
  uncertainty; richer covariance/confidence and observation provenance remain
  owned by `v0.14.0` and `v0.15.0`;
- checked UT1-offset evaluation and application to continuous instants through
  `ConversionContext`; UTC civil conversion completes with `v0.12.0`;
- hard-bound UT1 evaluation/application preserves a complete
  `UnverifiedBoundDerivation` binding the EOP content/model generation,
  interpolation/extrapolation decision, rounding, and exact endpoints;
- stale, extrapolated, missing, caller-removed, replaced, and unavailable
  structural model outcomes; identified withdrawal events and propagation
  begin only at `v0.15.1` and the `v0.52.x` orchestration milestones.

Verification:

- official EOP examples, interpolation boundaries, stale/extrapolated data,
  caller removal/replacement/unavailability, mixed generations, classified
  uncertainty propagation, and compile tests preventing source-neutral
  metadata from satisfying later provenance/authority or generic-withdrawal
  contracts; recipe tests replace EOP content, generation, interpolation
  decision, rounding, and endpoints independently.

Exit criteria:

- the UT1 model is never represented as a fixed offset or silently
  extrapolated;
- `v0.11.1 implementation stop reached. Run pentest for this exact commit.`

### v0.11.2 - Relativistic Coordinate Scales

Status: planned.

Goal: add only admitted relativistic-coordinate scales and conversion models
required by registered protocols.

Deliverables:

- the applicable clauses of `iau-2000-resolutions`,
  `iau-2006-resolution-b3`, and `bipm-si-brochure-9-v4.01` reviewed and mapped
  to exact constants and equations;
- exact identifiers, epochs, rates, model constants, validity, and references
  for each admitted scale;
- checked conversions under an explicit model/context generation;
- every hard-bound coordinate-scale conversion extends the
  `UnverifiedBoundDerivation` with exact constants, equation/operation,
  context/model generation, rounding, and endpoints;
- explicit out-of-scope scales and accuracy non-claims.

Verification:

- official published examples, epoch/rate extremes, rounding, reverse
  conversion residuals, wrong model, unsupported scales, and complete recipe
  preservation/substitution tests.

Exit criteria:

- no relativistic conversion is inferred from a name or approximate
  floating-point offset;
- `v0.11.2 implementation stop reached. Run pentest for this exact commit.`

### v0.11.3 - NTP And PTP Scale Semantics

Status: planned.

Goal: distinguish protocol timestamp encodings from underlying time scales.

Deliverables:

- NTP-as-UTC-encoding and era context separated from a standalone scale;
- PTP timescale, arbitrary-timescale, epoch, and UTC-offset semantics;
- exact conversion-context/model generation attached to normalized results;
- hard normalized results retain an `UnverifiedBoundDerivation` binding the
  protocol-native value/identity, era/offset input, conversion operation,
  context/model generation, rounding, condition, and endpoints;
- protocol identity retained through conversion.

Verification:

- NTP era/UTC examples, PTP timescale/arbitrary-timescale cases, stale offset,
  mixed model generations, cross-protocol non-substitution, and native-input/
  era/offset/context/recipe substitution.

Exit criteria:

- a wire encoding cannot masquerade as an independent physical time scale;
- `v0.11.3 implementation stop reached. Run pentest for this exact commit.`

### v0.11.4 - Externally Resolved GNSS Scale Identities

Status: planned.

Goal: represent named GNSS scales for generic externally resolved
observations without performing Navheim-owned interpretation.

Deliverables:

- identifiers and externally supplied scale-offset/model evidence for GPS,
  Galileo, BeiDou, GLONASS, QZSS, and NavIC observations;
- non-fixed-offset GLONASS distinction and typed unknown/custom identities;
- cross-check-only adapters under `ConversionContext`;
- any hard cross-check result preserves an `UnverifiedBoundDerivation`
  containing the external observation identity, supplied offset/model
  generation, operation, rounding, condition, and exact endpoints;
- no week resolution, navigation UTC model, receiver, health, or
  authentication logic.

Verification:

- externally resolved examples, missing/stale offset evidence, GLONASS
  non-fixed behavior, unknown identities, mixed generations, and compile-time
  Navheim-boundary checks, plus external-observation/model/recipe substitution.

Exit criteria:

- Mundilfari can name an externally resolved GNSS scale without determining
  time from GNSS;
- `v0.11.4 implementation stop reached. Run pentest for this exact commit.`

### v0.11.5 - Time-Scale Family Security Gate

Status: planned.

Goal: audit scale identity, conversion models, and family boundaries before
UTC/leap implementation builds on them.

Deliverables:

- clause/model maps and cross-family non-substitution review;
- resolved critical/high generation, stale-data, rounding, and boundary
  findings;
- explicit Navheim ownership confirmation.

Verification:

- full scale corpus, differential published examples, arbitrary conversion
  requests, caller removal/replacement/unavailability, no_std/MSRV, and focused
  pentest; generic identified withdrawal remains deferred to `v0.15.1`.

Exit criteria:

- all admitted scale families preserve identity, model generation, and
  uncertainty semantics;
- `v0.11.5 implementation stop reached. Run pentest for this exact commit.`

### v0.12.0 - UTC And Leap Seconds

Status: planned.

Goal: model UTC including positive and possible negative leaps.

Deliverables:

- UTC civil values capable of representing second 60;
- immutable versioned leap-table representation with content hash,
  source-neutral metadata, and structural positive/negative leap entries;
- explicit generic TAI-to-UTC and UTC-to-TAI conversion against the canonical
  `AtomicInstant` origin, including realization metadata and typed ambiguous,
  missing-table, stale-table, and out-of-coverage outcomes;
- every hard UTC/TAI/UT1 conversion result extends its
  `UnverifiedBoundDerivation` with the immutable leap/EOP content hash and
  generation, selected branch, operation, rounding, condition, and exact
  input/output endpoints;
- checked UTC/UT1 conversion using the admitted EOP model and matching
  conversion-context generations;
- this milestone does not own evidence provenance, announcement lifecycle,
  admission policy, active-model replacement, or concurrent publication;
- explicit UTC-before-1972 non-claim until a historical frequency-offset model
  is separately admitted.

Verification:

- canonical TAI/UTC origin and published offset vectors, every historical leap
  boundary, second 60, invalid leap dates, immutable table/hash/source-neutral
  metadata, outside-coverage behavior, realization-evidence non-equivalence,
  negative-leap synthetic tests, and recipe table/EOP/branch/rounding/endpoint
  substitution; compile/dependency tests prove the deferred provenance/
  admission/publication layers are absent.

Exit criteria:

- leap handling is explicit and no UTC value is forced through POSIX rules;
- `v0.12.0 implementation stop reached. Run pentest for this exact commit.`

### v0.12.1 - Leap Model Candidate Validation

Status: planned.

Goal: define immutable leap-model candidates, pure validation, conflict
detection, and transactional generation replacement without depending on
later provenance, lifecycle, engine quorum, or concurrent-publication types.

Deliverables:

- immutable `LeapModelCandidate` with complete entries, source-independent
  candidate identifier, proposed generation, effective interval, hash, and
  structural/model constraints but no authentication/diversity authority;
- pure bounded validation for ordering, duplicate/conflicting transitions,
  lead-time representation, positive/negative leap shape, UTC/TAI continuity,
  and model compatibility;
- deterministic candidate-to-current comparison with unchanged, extension,
  conflict, rollback, replacement, and unsupported outcomes;
- single-thread transactional stage/commit/abort semantics for an isolated
  caller-owned conversion model, replacing one model generation indivisibly
  and invalidating stale conversion contexts;
- “atomic activation” at this stage means one indivisible model-generation
  transaction, not lock-free or concurrent-reader publication;
- raw validated-candidate replacement remains an explicit expert operation;
  it cannot update `TrustedClock`, the default facade, or manufacture later
  engine admission;
- no protocol type, provenance policy, generic lifecycle event, authentication
  class, source quorum, or engine dependency.

Verification:

- immutable candidate/model properties, malformed ordering, duplicates,
  conflicting entries, false positive/negative and synthetic negative leaps,
  extension/rollback/replacement comparisons, stage/abort/commit failure
  injection, stale conversion generation, and explicit compile/dependency
  tests proving no provenance/lifecycle/engine/concurrency coupling.

Exit criteria:

- core can validate and transactionally replace an isolated caller-owned model
  without claiming source admission or default-clock publication;
- `v0.12.1 implementation stop reached. Run pentest for this exact commit.`

### v0.13.0 - POSIX And Smear Policy

Status: planned.

Goal: define honest POSIX/UTC conversion behavior.

Deliverables:

- `PosixInstant` and typed `Unique`, `Ambiguous`, or `Nonexistent` conversion
  outcomes before policy;
- repeat/clamp/reject policies and typed smear profiles carrying provider,
  window, function, model generation, and inverse limitations;
- hard POSIX/UTC/smear results extend the `UnverifiedBoundDerivation` with the
  exact policy/profile, model generation, branch/invertibility outcome,
  rounding, condition, and input/output endpoints;
- labels preventing smeared time from being reported as UTC.

Verification:

- leap boundaries, each policy, noninvertible cases, and smear endpoint
  continuity tests, including complete policy/profile/branch/model/recipe
  preservation and substitution.

Exit criteria:

- every POSIX conversion states its leap policy;
- `v0.13.0 implementation stop reached. Run pentest for this exact commit.`

### v0.14.0 - Intervals And Uncertainty

Status: planned.

Goal: extend the `v0.7.1` interval foundation and `v0.7.2` hard-bound
condition contract into complete uncertainty algebra and evidence for
observations and algorithms.

Deliverables:

- asymmetric uncertainty and error-budget composition over the stable
  `v0.7.1` instant/duration interval representation;
- statistical estimates carrying covariance, confidence level, model identity,
  and model generation while preserving the foundational hard/statistical
  non-substitution;
- explicit, policy-named statistical-to-hard-bound conversion only where its
  assumptions and confidence are supplied; the conversion adds them to the
  immutable `v0.7.2` condition with `All` and never replaces the prior
  containment formula, with no implicit covariance promotion;
- richer checked union, expansion, error-budget composition, projection, and
  midpoint policy reusing the foundational containment/intersection and
  logical-condition semantics;
- every operation producing a hard bound, including explicit statistical-to-
  hard conversion and uncertainty expansion, composes the complete bounded
  `UnverifiedBoundDerivation`; covariance/statistical-only operations cannot
  manufacture a hard-claim recipe without the named conversion policy and its
  condition/model evidence;
- empty/disjoint/saturated results.

Verification:

- interval algebra properties, extremes, asymmetry, empty sets, rounding,
  covariance units/symmetry, confidence/model substitution, and compile-fail
  hard/statistical mixing; recipe composition, statistical-only recipe refusal,
  expansion/conversion policy/model/condition substitution, and recipe-bound
  exhaustion.

Exit criteria:

- network and physical observations need not pretend to be exact instants;
- `v0.14.0 implementation stop reached. Run pentest for this exact commit.`

### v0.15.0 - Quality Authentication And Provenance

Status: planned.

Goal: define the complete protocol-neutral observation model.

Deliverables:

- earliest/latest interval, policy-permitted preferred estimate, scale,
  realization, resolution, precision, age, stability, traceability, leap, and
  holdover;
- authentication class separate from advertised/measured/verified accuracy;
- source generation, protocol, authority, path, optional typed
  `EvidenceDigest { algorithm, value, assurance }`, monotonic capture,
  warnings, integrity, and reading;
- observation earliest/latest and duration-error bounds reuse `v0.7.1`
  interval/hard-bound types, `v0.7.2` condition identities, and `v0.7.3`
  external resolution; statistical fields use the enriched `v0.14.0` evidence
  without a parallel interval representation;
- each observation root hard claim binds its `UnverifiedBoundDerivation` origin
  to the exact observation/source/provider identity, evidence digest,
  generations, raw reading/capture identity, and claimed endpoints; derived
  observation bounds retain the complete transitive recipe rather than only
  the final claim digest;
- bounded error-budget components separating systematic/random,
  measured/asserted, correlation identity, calibration, quantization, path,
  capture, scale-model, and oscillator contributions;
- diversity assertions carrying provenance, assurance class, validity,
  generation, and conservative unknown-correlation behavior.

Verification:

- construction invariants, redacted debug output, non-substitution type tests,
  forged diversity, correlation conflicts, digest assurance, error-budget
  composition, observation/source/evidence/raw-reading recipe substitution,
  transitive-recipe preservation, and no trusted-boolean API.

Exit criteria:

- callers can distinguish authentic, accurate, traceable, and merely formatted;
- `v0.15.0 implementation stop reached. Run pentest for this exact commit.`

### v0.15.1 - Generic Observation Lifecycle

Status: planned.

Goal: make insertion, withdrawal, and discontinuity generic for every time
source before any protocol or Navheim adapter exists.

Deliverables:

- unique observation/artifact identity, source identity, generation,
  monotonic sequence, capture time, and `valid_until`;
- protocol-neutral `Upsert`, `Withdraw`, and `Discontinuity` events with typed
  reasons and affected correlation generations;
- adapters may map an identified EOP/time-data source's earlier structural
  caller-removed, replaced, or unavailable state into these events only once
  source/artifact identity and generation exist; `v0.11.1` itself has no
  generic withdrawal event;
- monotonic ordering, duplicate/idempotence policy, and bounded event queues;
- reserved withdrawal capacity/backpressure so an invalidation cannot be
  silently dropped behind ordinary observations;
- withdrawal propagation contract for filters, consensus, servos, virtual
  clocks, persistence, and audit records.

Verification:

- duplicate/out-of-order events, generation rollover, withdrawal before/after
  upsert, EOP caller-removal/replacement mapping with/without source identity,
  expiry, queue saturation, reserved-capacity exhaustion, discontinuity
  fan-out, restart, and deterministic replay.

Exit criteria:

- every source can retract evidence without relying on a source-specific
  mechanism;
- `v0.15.1 implementation stop reached. Run pentest for this exact commit.`

### v0.15.2 - Leap Evidence Provenance And Lifecycle

Status: planned.

Goal: represent identified leap evidence and its lifecycle using the completed
generic observation/provenance foundations without deciding source quorum.

Deliverables:

- evidence classes for authoritative table assertions, authenticated protocol
  announcements, corroborating observations, and unauthenticated hints;
- candidate identifier/hash, source/authority identity, protocol, provenance,
  authentication/integrity class, capture/validity, uncertainty, generation,
  sequence, and correlation assertions;
- generic upsert/withdraw/discontinuity mapping for pending, corrected,
  cancelled, expired, conflicted, and rejected leap evidence;
- bounded reserved invalidation behavior and deterministic projection from
  identified evidence sets into one or more `LeapModelCandidate` values;
- unauthenticated hints may warn or increase uncertainty but carry no
  activation authority;
- no diversity/quorum decision or concurrent publication implementation.

Verification:

- exhaustive evidence-class construction, forged/unknown provenance,
  authentication-without-authority, duplicate/reordered generations,
  cancellation/withdrawal, expiry, conflict, queue pressure, correlated
  assertions, candidate-hash mismatch, and no-engine dependency tests.

Exit criteria:

- leap assertions have complete generic provenance and retraction semantics
  before engine policy can admit a candidate;
- `v0.15.2 implementation stop reached. Run pentest for this exact commit.`

### v0.16.0 - Monotonic Clock Correlation

Status: planned.

Goal: relate fast monotonic readings to continuous/civil time safely.

Deliverables:

- `MonotonicClockId`/domain token on every instant, deadline, elapsed duration,
  expiry, and correlation;
- explicit suspend semantics (`StopsDuringSuspend` or `IncludesSuspend`),
  raw-oscillator versus frequency-adjusted rate semantics, process-local
  versus system-wide scope, boot/session, namespace, process generation,
  machine-instance generation, clock generation, rate, and uncertainty;
- bounded `MonotonicReadInterval { earliest, latest }` in one exact domain;
  `latest` conservatively includes clock resolution/quantization, sampling
  latency, and rate uncertainty/drift through the provider's documented
  observation/linearization point. An operation-supplied completion margin is
  applied separately only by a consumer with a reviewed bound; the measured
  interval alone makes no caller-return guarantee. A scalar hardware/API
  counter reading cannot by itself prove that a deadline has not passed;
- checked same-domain arithmetic only, with typed domain/suspend/generation
  mismatch errors;
- a public `UntrustedMonotonicCorrelationCandidate` is structurally separate
  from the opaque engine-only `AdmittedMonotonicDomainCorrelation`. Core owns
  only the bounded candidate, canonical identity/preimage, translation
  arithmetic, and diagnostic views; it has no constructor for admitted state;
- every candidate is directed from one exact source `MonotonicClockId`/
  generation to one exact target domain/generation. Its offset interval,
  bounded rate ratio, and drift bound are typed
  `BorrowedHardBoundClaim`/`OwnedHardBoundClaim` values with mandatory
  `UnverifiedBoundDerivation` recipes and canonical `BoundCondition`/
  `BoundAssumptionsId`, never privileged scalar fields. The candidate also
  binds observation method, uncertainty provenance, suspend/reset/migration
  compatibility, provider identity/generation, and lifecycle generation;
- each numerical claim binds exact paired capture anchors: conservative source
  and target `MonotonicReadInterval` values, capture ordering/bracketing method,
  pairing generation, and elapsed origin. Translation grows rate/drift
  uncertainty outward from the worst-case elapsed distance to those anchors;
  a provider cannot reset the growth origin by repackaging the same evidence;
- structural `CorrelationValidityCandidate` is non-circular and initially has
  only `IndependentEndpointDeadlines { source, target }`. Each deadline is
  checked by reading its own exact endpoint domain without using the
  correlation under admission or any value derived from it. A separate
  supervision-domain form is deferred until a reviewed dependency-DAG proof
  can exclude self/indirect cycles; one translated aggregate deadline cannot
  validate the correlation that performs the translation;
- the initial candidate recipe/condition contract exposes every transitive
  input and support reference needed for later admission. It grants no way to
  treat an opaque or historical `AdmittedMonotonicDomainCorrelation` reference
  as a root observation, proof input, condition atom, or authority. Initial
  engine admission therefore can enforce an acyclic-by-construction leaf set
  rather than trusting “direct translation only” to prevent semantic cycles;
- translating a source instant or deadline produces an outward-rounded target
  interval with accumulated offset/rate/drift/elapsed/quantization uncertainty.
  For a source `valid_until` mapped to target `[earliest, latest]`, the only
  safe target deadline is the conservative `earliest` edge;
- the initial kernel permits direct translation only. No caller-controlled
  graph search or implicit chaining exists. A later bounded-composition
  extension would require a separately reviewed maximum depth, deterministic
  canonical path selection, cycle prevention, uncertainty growth, complete
  dependency retention, and an independently pentested milestone;
- candidate lifecycle invalidates on either domain reset/generation change,
  incompatible suspend, rate-semantics change, migration outside declared
  scope, provider withdrawal/loss, validity expiry, or uncertainty exceeding
  the consuming policy's bound;
- stale/rollback/restart detection;
- virtual trusted-clock read model.

Verification:

- compile-time/runtime cross-domain rejection, each suspend/rate/scope
  combination, restart, suspend, rollback, drift, stale generation/
  correlation, persisted-anchor mismatch, helper-expiry mismatch, and
  uncertainty-growth simulations; coarse resolution, delayed sampling,
  latency spikes, rate-uncertainty growth, completion margins, and exact
  upper-edge deadline comparisons;
- candidate/admitted type-confusion compile tests; reversed direction,
  wrong/stale domain generation, reset/suspend/rate/migration/provider-loss
  invalidation, forged provider identity, high/overflowing uncertainty, exact
  outward-rounding vectors, and source-deadline-to-target-earliest-edge
  properties. Attempts to chain, cycle, choose a path, self-assert admission,
  or use a candidate where admitted state is required fail typed;
- missing/truncated/substituted offset/rate/drift recipes, forged narrow
  endpoints, changed capture anchors/pairing generation, elapsed-growth reset,
  missing/circular/same-correlation-translated validity, and source/target
  endpoint deadline/reset cases fail. Property tests grow uncertainty
  monotonically from both anchors and independently check each endpoint
  deadline. Structural fixtures attempting to hide current or historical
  admitted-correlation references in a recipe, condition, or derived support
  leaf remain untrusted and cannot become an admitted candidate dependency.

Exit criteria:

- monotonic values cannot cross domains or become civil time without an exact
  directed correlation, and core candidates carry no engine authority;
- `v0.16.0 implementation stop reached. Run pentest for this exact commit.`

### v0.16.1 - Core No-Allocation Formatting

Status: planned.

Goal: format foundational time values in `no_std` without allocation, locale,
or partial semantic output.

Deliverables:

- unambiguous `core::fmt::Display` implementations and caller-buffer
  `format_into` APIs with required-length reporting;
- atomic write-or-error behavior for insufficient output;
- explicit `ConversionContext` for UTC/civil forms, preserved fractional
  precision, leap-second formatting, and no locale dependence;
- no formatting path that silently selects an era, scale, zone, or smear.

Verification:

- exact/minus-one buffer sizes, extremes, negative years, second 60,
  fractional precision, stale/missing context, writer failure, no allocation,
  and round-trip cases where a parser exists.

Exit criteria:

- core values have bounded human-readable output without hiding conversion
  policy;
- `v0.16.1 implementation stop reached. Run pentest for this exact commit.`

### v0.16.2 - Common Error Taxonomy

Status: planned.

Goal: give callers stable error classification without flattening detailed
protocol or platform causes.

Deliverables:

- stable classes for malformed, unsupported, ambiguous, stale,
  unauthenticated, integrity failure, policy rejection, resource exhaustion,
  unavailable, unauthorized, discontinuous, out of range, transport, and
  platform failures;
- structured source chains and redacted details in `no_std` and `std`;
- peer invalidity, local exhaustion, transport failure, and authorization
  failure kept distinct;
- exhaustive classification required for every public error.

Verification:

- one fixture per class, protocol/platform wrapper mappings, redaction,
  unknown future detail, source chaining, and compile-time exhaustive internal
  mapping checks.

Exit criteria:

- applications never need to parse error strings to make safe policy choices;
- `v0.16.2 implementation stop reached. Run pentest for this exact commit.`

### v0.17.0 - Foundation Security Gate

Status: planned.

Goal: audit the complete time model before protocols depend on it.

Deliverables:

- arithmetic and conversion audit;
- `CanonicalIdentityV1` preimage/domain-separation/schema-reuse audit plus
  differential/KAT review of the first-party SHA-256 implementation; structural
  collision, commutative ordering, collision-bucket cache/interning behavior,
  and the prohibition on unstable Rust identity inputs are release blockers;
- foundational instant/duration interval and hard/statistical type-separation
  audit proving every era, fraction, EOP, and later uncertainty consumer uses
  the `v0.7.1`/`v0.7.4` types without provisional duplicates;
- derivation-arena audit covering capacity, canonical DAG sharing,
  lifetime-brand generativity, same-address ABA resistance, nonwrapping
  generation exhaustion, destruction/reinitialization, eviction/read leases,
  concurrent import, mutable/frozen/read-only `Send`/`Sync`, heterogeneous edge
  safety, and geometry/conditional-claim/fallible-derivation equality
  semantics;
- `v0.7.4` ownership/promotion audit proving borrowed claims cannot escape,
  owned frozen arenas avoid self-reference, promotion is fallible/atomic/
  canonical and does not grant authority, target-dependent unique versus
  Arc-style sharing is honest, and no lifetime extension, handle copying, or
  storage leak bypasses the boundary;
- multi-root promotion audit proving cross-root canonical sharing, duplicate
  root coalescing, per-root versus unique-total accounting, immutable retention,
  bounded new-owner compaction, atomic batch failure, and individual/batch
  identity equivalence;
- leap-candidate validation/transaction and evidence-provenance/lifecycle
  boundary plus monotonic-domain suspend/rate/scope/generation audit; engine
  authority/diversity admission remains deferred to `v0.61.1`;
- monotonic-correlation candidate audit proving offset/rate/drift claims carry
  complete bounded recipes/conditions and immutable paired capture anchors,
  uncertainty grows outward from those anchors, endpoint validity is
  independently checkable without self-translation, and no core/platform value
  can construct engine-admitted correlation state or use an admitted/
  historical correlation as transitive numerical proof or condition support;
- hard/statistical uncertainty, error-budget, observation-lifecycle,
  formatting, and error-taxonomy audit;
- Kani-style reduced-state proofs for handle resolution, brand/generation
  transitions, eviction exclusion, and collision buckets, plus other bounded
  proofs where useful;
- no_std stack/code-size and arena/handle layout evidence for every supported
  capacity/profile;
- API and serialization stability review proving no raw Rust layout, `repr(C)`,
  or implicit serialization freezes the internal instant representation;
- resolved critical/high findings.

Verification:

- full foundation corpus, independent differential oracles, fuzzing, MSRV, and
  no_std target matrix; SHA-256 KAT/differential corpus, identity-schema golden
  vectors, arena ABA/wraparound/concurrency state machines, equality/collision
  cases, borrowed/owned promotion and source-drop/owner-drop state machines,
  compile-fail lifetime-escape corpus, multi-root shared-DAG/retention/
  compaction state machines, forged correlation bounds/anchors, circular
  validity cases, two-node/longer/replacement/restored-reference correlation
  proof cycles, and reduced-state proof artifacts are mandatory.

Exit criteria:

- exact time foundations are approved for protocol use;
- `v0.17.0 implementation stop reached. Run pentest for this exact commit.`

## Phase 2: Bounded Wire And State Foundations

### v0.18.0 - Read And Write Cursors

Status: planned.

Goal: implement allocation-free bounded wire cursors.

Deliverables:

- exact read/write, remaining length, subcursor, and finish APIs;
- no unchecked slicing or partial success;
- byte-offset structured errors.

Verification:

- every length boundary, truncation point, zero-sized field, and arbitrary-byte
  no-panic corpus.

Exit criteria:

- protocol parsers share one reviewed bounds discipline;
- `v0.18.0 implementation stop reached. Run pentest for this exact commit.`

### v0.19.0 - Primitive Wire Codecs

Status: planned.

Goal: implement protocol-neutral integer and field codecs.

Deliverables:

- endian integers, bit fields, BCD, signed fixed point, and length prefixes;
- canonical/minimal checks where applicable;
- reserved-value preservation.

Verification:

- exhaustive widths, endian cross-tests, malformed BCD, sign boundaries, and
  round trips.

Exit criteria:

- protocols do not add ad hoc unchecked byte arithmetic;
- `v0.19.0 implementation stop reached. Run pentest for this exact commit.`

### v0.20.0 - Checksums And CRC

Status: planned.

Goal: provide reviewed checksum/CRC building blocks.

Deliverables:

- parameterized CRC engine and protocol-specific fixed profiles;
- XOR, additive, Fletcher, and parity helpers where required;
- streaming and one-shot equivalence.

Verification:

- catalogue check values, bit-by-bit oracle comparison, corruption, empty, and
  chunk-boundary tests.

Exit criteria:

- later protocols use named reviewed profiles rather than magic polynomials;
- `v0.20.0 implementation stop reached. Run pentest for this exact commit.`

### v0.21.0 - Fixed-Capacity Collections

Status: planned.

Goal: support bounded no-allocation state.

Deliverables:

- fixed vector, queue, map, set, string, and byte buffer;
- explicit capacity errors and deterministic iteration;
- no hidden heap use;
- an explicit `unsafe_code = "forbid"` representation decision for each
  collection: safe `[Option<T>; N]`/equivalent storage or a separately audited
  dependency, with initialized/drop-state, layout, stack-cost, and destructor
  evidence.

Alloc-enabled companions use fallible `try_*` construction and
`try_reserve`-style growth, or caller-supplied storage. APIs that cannot
recover from allocator failure carry an explicit process-abort-on-OOM
non-claim and are never the only network-facing path.

Verification:

- zero/full capacity, reuse, order, duplicate, removal, drop exactly once,
  panic-during-drop containment where applicable, stack-limit/layout reports,
  dependency feature audit where selected, and model comparison.

Exit criteria:

- untrusted lengths cannot create attacker-sized allocations;
- `v0.21.0 implementation stop reached. Run pentest for this exact commit.`

### v0.22.0 - Borrowed Packet Pattern

Status: planned.

Goal: standardize lossless parse/validate/encode APIs.

Deliverables:

- borrowed packet references, unknown-field iterators, owned opt-in forms;
- unknown preservation for inspection separated from semantic acceptance,
  forwarding, response echo, authentication, and re-encoding authority;
- unknown fields echoed only when the exact protocol revision requires it and
  response/work budgets permit it;
- strict/compatible/forensic modes;
- type-state transitions from parsed through semantic, association, and
  authenticated validity where applicable;
- caller-owned encoder contract.

Verification:

- unknown preservation, forbidden reflection/forwarding, required-echo
  fixtures, compile-fail forensic/compatibility non-authority, exact round
  trips, and insufficient-output atomicity.

Exit criteria:

- protocol crates share one security-reviewed API shape;
- `v0.22.0 implementation stop reached. Run pentest for this exact commit.`

### v0.22.1 - Canonical Schema Kernel

Status: planned.

Goal: define the allocation-free canonical encoding kernel before any
persistent or external state consumer exists.

Deliverables:

- one `no_std`, caller-buffer schema envelope with schema identity, version,
  criticality, canonical field order, duplicate/unknown-field rules, and
  explicit maximum record/message size;
- schema primitive/value encoding wraps and reuses the exact `v0.6.1`
  `CanonicalIdentityV1` integers, enums, sequences, type/domain tags,
  normalization, and length framing for identity-bearing fields; it does not
  introduce a parallel serde-shaped or schema-only canonical representation,
  and compatibility extensions cannot reinterpret an existing identity
  preimage;
- fixed maximum nesting depth and total field/item count, with iterative
  parsing or recursion whose stack depth is statically bounded;
- canonical bounded integers including signed high/low wide limbs, byte
  strings, sequences, identifiers, generations, and nested values;
- stable type/tag allocation registry with reserved core, protocol,
  experimental, and vendor ranges, collision rejection, and a permanent rule
  that a field/tag identifier is never reused with new meaning;
- required-length and atomic encode-or-error behavior with no Rust-layout,
  serde-data-model, filesystem, IPC, or language-runtime dependency;
- import/export value traits for protocol, engine, and platform consumers;
- bound-condition fields decode only into the `v0.7.3`
  `UnresolvedAssumptionReference`/`UnresolvedBoundCondition` type-state;
  canonical schema decoding cannot directly construct a
  `BoundAssumptionsId`, `ResolvedBoundCondition`,
  `BorrowedHardBoundClaim`, `OwnedHardBoundClaim`, or
  `OwnedHardBoundClaimSet`; ownership arises only through core promotion;
- derivation fields decode only into bounded
  `UnverifiedBoundDerivationRecord`; canonical schema has no tag or decode
  trait for the opaque engine `VerifiedBoundDerivation`, and recipe resolution
  remains non-authoritative;
- budget-consumption hooks completed by `v0.25.0` for bytes, items, nesting,
  and work;
- compatibility rules that later schema work may extend but never silently
  reinterpret.

Verification:

- golden bytes, every truncation, duplicate/noncanonical/unknown critical
  field, maximum/over-depth and item-count inputs, tag/range collisions,
  identifier-reuse fixture, integer extremes, required-length/short-buffer
  atomicity, deterministic re-encoding, version skew, stack bounds,
  unverified-derivation-record encoding and direct verified-tag/decode absence,
  byte-for-byte identity-kernel reuse/no-second-encoding fixtures,
  no-allocation, and arbitrary-byte fuzz/property tests.

Exit criteria:

- persistence and IPC can share one reviewed encoding kernel without freezing
  Rust memory layout;
- `v0.22.1 implementation stop reached. Run pentest for this exact commit.`

### v0.23.0 - Poll And Timer State Machines

Status: planned.

Goal: define runtime-neutral bounded protocol execution.

Deliverables:

- explicit poll context, actions, timers, deadlines, cancellation, and budgets;
- generation tokens on timers, requests, transmit timestamps, crypto work, and
  hardware callbacks;
- no executor or wall-clock assumption;
- deterministic state transition tracing.

Verification:

- exhaustive small state machines, cancellation races, timer wrap, duplicate
  wake, stale-generation completion, and budget exhaustion.

Exit criteria:

- protocol engines can run in embedded, simulator, and hosted environments;
- `v0.23.0 implementation stop reached. Run pentest for this exact commit.`

### v0.23.1 - Execution Lifecycle Generations

Status: planned.

Goal: make fork, clone, VM restore, and container checkpoint/restore generic
lifecycle discontinuities before protocol associations exist.

Deliverables:

- typed `ProcessGeneration`, `MachineInstanceGeneration`, and lifecycle events
  for fork child, process replacement, VM snapshot/restore, container
  checkpoint/restore, clone, and explicit reinitialization;
- one invalidation fan-out contract covering outstanding requests/transmit
  identities, entropy/nonces, sockets, timers/deadlines, rate limits, helper
  sessions, persistent bootstrap anchors, refresh reservations/fencing
  generations/tombstones, and TrustedClock publication state;
- inherited state is unusable until explicit child/restored-instance
  reinitialization establishes new generations;
- hosted handle policy for non-inheritance, close-on-exec, pre-opened helper
  handles, and safe closure/reopen; platform-specific detection stays in
  platform adapters;
- lifecycle events compose with generic discontinuity and withdrawal queues
  without silent loss.

Verification:

- fork-before/after request, multithreaded fork boundary, exec, duplicate
  entropy/request state, VM snapshot replay, container checkpoint restore,
  inherited sockets/timers/rate limits/helper session, CLOEXEC/non-inherited
  handles, inherited live/tombstoned refresh reservations, stale delayed-writer
  install attempts, queue saturation, child reinitialization, and deterministic
  simulator schedules.

Exit criteria:

- cloned execution cannot silently continue security or timing state under the
  old process/machine generation;
- `v0.23.1 implementation stop reached. Run pentest for this exact commit.`

### v0.24.0 - Transport And Clock Traits

Status: planned.

Goal: freeze platform-neutral I/O and clock contracts.

Deliverables:

- datagram, stream, raw-link, serial, edge, sample, CAN, and clock traits;
- receive/send metadata and timestamp quality;
- monotonic providers return the full `MonotonicClockId` descriptor and reject
  deadlines/elapsed values from another suspend/rate/scope/generation domain;
- every monotonic provider implements bounded
  `read_interval() -> Result<MonotonicReadInterval, ClockReadError>` carrying
  exact domain identity, earliest/latest, native resolution/quantization,
  measurement method, sample/call latency bound or observation, rate-
  uncertainty provenance, capture generation, and capability/non-claims;
  scalar native counters are conservatively inflated and never mapped to
  `[t,t]` unless the provider proves zero uncertainty;
- separate `LinearizationReadCapability` and optional
  `ThroughCompletionCapability { wcet }` contracts: interval measurement may
  support authority at its documented observation/linearization point without
  claiming a hard caller-return bound; through-completion is exposed only when
  the platform/runtime provides a reviewed maximum completion/WCET guarantee;
- platform-neutral correlation providers may emit only
  `UntrustedMonotonicCorrelationCandidate` values using the complete `v0.16.0`
  directed-domain, method, uncertainty, validity, suspend/reset, provider, and
  lifecycle contract. Provider methods must supply the exact paired capture
  anchors plus bounded derivation recipes/conditions for offset, rate, and
  drift claims; registration or a narrow numeric assertion is not evidence.
  The trait has no admission method and no provider may construct or claim
  `AdmittedMonotonicDomainCorrelation`;
- unavailable interval bounds, migration/frequency/suspend/virtualization/
  reset ambiguity, and unavailable completion bounds are explicit capability
  or typed error states, never scalar fallback;
- HAL-like device traits without Unix file descriptors in core signatures;
- compiled/available/authorized/healthy capability discovery contracts;
- entropy and hardware-clock traits without fallback implementations.

Verification:

- in-memory transports, error propagation, timestamp identity, short I/O, and
  capability compile tests; interval-provider contract tests cover scalar
  inflation, zero/nonzero resolution, latency/rate uncertainty, exact domain,
  missing provenance, migration/frequency/suspend/reset/virtualization
  ambiguity, and linearization-only versus through-completion capability;
  correlation-provider tests cover complete candidate metadata, withdrawal,
  provider generation changes, root-recipe/condition/anchor preservation,
  forged narrow scalar output, and compile-time refusal of engine admission.

Exit criteria:

- protocol crates do not expose OS socket or file types;
- every platform monotonic implementation must provide a conservative interval
  or explicitly report that strict authority is unavailable;
- `v0.24.0 implementation stop reached. Run pentest for this exact commit.`

### v0.24.1 - Generic Cryptographic Provider Contracts

Status: planned.

Goal: establish protocol-neutral cryptographic capability boundaries before
any persistence or wire consumer requests cryptographic work.

Deliverables:

- `no_std` caller-buffer contracts for MAC, AEAD, digest, entropy, secret
  containers, opaque key identifiers, and key generation;
- explicit algorithm/provider identity, assurance class, failure behavior,
  nonce requirements, per-key operation/byte limits, atomic exhaustion
  accounting, and fail-closed generation rollover;
- capability-qualified `SecretMemoryProtection` report separating redaction
  only, best-effort zeroization, page locking, core-dump exclusion,
  hardware-backed/non-exportable keys, and externally held key operations;
  capabilities are combinable and never inferred from a secret-container type;
- test-only versus production-approved provider provenance and constructors;
- no protocol field semantics, TLS, certificate, storage, or clock policy in
  provider traits;
- provider digest APIs may verify or reproduce the fixed public-data
  `v0.6.1` identity profile but cannot replace its preimage, algorithm,
  structural collision checks, or existing identities; configurable provider
  algorithms are for later security/integrity protocols, not identity drift;
- redacted diagnostics and common error-taxonomy mapping.

Verification:

- deterministic mock/KAT providers, wrong algorithm/key/generation/direction,
  short output, entropy/nonce failure, usage-limit races and exhaustion,
  redaction, claimed/unavailable/failing zeroization/page-lock/core-dump/
  hardware/external-key capabilities, feature/no_std/MSRV matrices, and
  identity-profile reproduction plus attempted provider-driven identity
  algorithm/preimage substitution, and compile-time protocol-type isolation.

Exit criteria:

- every later crypto consumer depends on one bounded provider contract while
  no test provider can be mistaken for production assurance;
- `v0.24.1 implementation stop reached. Run pentest for this exact commit.`

### v0.25.0 - Work And Resource Budgets

Status: planned.

Goal: enforce operation-wide resource accounting.

Deliverables:

- non-copyable byte, item, nesting, work, allocation, and response budgets;
- child reservations without reset or double release;
- canonical-schema decode/encode charges bytes, total items/fields, nesting,
  and parsing work through the same non-resettable budget before descent or
  allocation;
- deterministic per-poll work ceilings and reported remaining work;
- local exhaustion distinct from protocol invalidity.
- pre-allocation validation of every network-controlled size and explicit
  fallible-allocation outcomes for alloc-enabled paths.

Verification:

- conservation properties, nested operations, cancellation, adversarial
  complexity, deep-small schema inputs, field/item floods, budget-before-
  descent checks, allocator failure injection, oversized pre-allocation
  rejection, and exhaustion outcome tests.

Exit criteria:

- nested parsers and state machines cannot reset attacker work;
- `v0.25.0 implementation stop reached. Run pentest for this exact commit.`

### v0.26.0 - Testkit Property Engine

Status: planned.

Goal: provide deterministic first-party generative testing.

Deliverables:

- test-only PRNG, generators, shrinking, seed recording, and corpus replay;
- clear separation from cryptographic entropy;
- invariant runner and failure minimizer.

Verification:

- deterministic seeds, shrink minimality fixtures, replay, and production API
  non-exposure.

Exit criteria:

- every protocol can add dependency-free property tests;
- `v0.26.0 implementation stop reached. Run pentest for this exact commit.`

### v0.27.0 - Mutation And State Fuzzer

Status: planned.

Goal: build protocol-aware deterministic fuzz infrastructure.

Deliverables:

- bit/byte/length/TLV/checksum mutation;
- state-sequence and timer-event mutation;
- corpus minimization and regression promotion.

Verification:

- seeded reproducibility, mutation coverage, minimizer tests, and crash corpus
  replay.

Exit criteria:

- malformed-input and state fuzzing is available before the first protocol;
- `v0.27.0 implementation stop reached. Run pentest for this exact commit.`

### v0.28.0 - Network And Clock Simulator

Status: planned.

Goal: simulate hostile timing conditions deterministically.

Deliverables:

- delay, jitter, loss, duplication, reorder, fragmentation, and asymmetry;
- drift, steps, oscillator noise, leap, rollover, restart, and holdover;
- malicious, correlated, and Byzantine sources.

Verification:

- deterministic scenario snapshots, conservation/order properties, and known
  analytical scenarios.

Exit criteria:

- protocol algorithms can be tested without live networks or hardware;
- `v0.28.0 implementation stop reached. Run pentest for this exact commit.`

### v0.29.0 - Wire Foundation Security Gate

Status: planned.

Goal: audit the shared parser, state, budget, test, and simulator foundation.

Deliverables:

- parser/resource audit and unsafe-free confirmation;
- canonical-schema kernel and generic crypto-provider contract audit,
  including canonicality, assurance, redaction, entropy, usage accounting,
  exhaustion, and proof that test providers are not production constructors;
- execution-lifecycle generation/invalidation and schema budget/depth/tag
  governance audit;
- API stability and code-size review;
- fuzz corpus and complexity-oracle report.

Verification:

- full arbitrary-input campaign, MSRV/no_std matrix, and independent review.

Exit criteria:

- shared wire, schema, state, and provider-contract foundations are approved
  for untrusted protocol input and later security consumers;
- `v0.29.0 implementation stop reached. Run pentest for this exact commit.`

## Phase 3: Platform Foundations

### v0.30.0 - Standard Clock Adapters

Status: planned.

Goal: expose safe monotonic and realtime clocks on supported hosted platforms.

Deliverables:

- Linux, Windows, BSD, and macOS adapters;
- generated capability report distinguishing compiled, available, authorized,
  and healthy states with resolution and explicit platform errors;
- exact native mapping for each monotonic clock's suspend behavior,
  raw/frequency-adjusted rate semantics, process/system scope, boot/session,
  namespace, process/machine instance generation, and clock generation;
- hosted `read_interval()` implementations use reviewed target-specific
  bracketing/cross-read strategies around Linux/Android clocks, Windows
  performance/interrupt-time counters, and BSD/macOS/iOS monotonic clocks;
  intervals include native resolution, observed bracket/call latency, rate
  uncertainty, migration/frequency/virtualization state, and generation.
  General-purpose hosted adapters advertise linearization-time capability and
  do not claim `ThroughCompletionCapability` merely from benchmarks or typical
  scheduler latency;
- hosted cross-clock methods emit untrusted directed correlation candidates,
  never admitted correlations. Candidate validity ends on reset, suspend/
  resume incompatibility, rate-semantics or namespace/process/machine
  generation change, migration beyond the measured scope, or provider loss.
  The candidate preserves exact cross-read anchors and measured/configured/
  asserted condition/recipe evidence for every offset/rate/drift bound;
- process/container/time-namespace identity and clock generation in every
  hosted clock report;
- fork/exec and VM/container checkpoint/restore detection where the platform
  exposes it, explicit fallback/non-claim otherwise, plus close-on-exec and
  child reinitialization for affected handles;
- checked native time conversion that returns `OutOfRange` rather than
  narrowing, saturating, or panicking;
- Android/iOS library-safe support.

Verification:

- host matrix, monotonic nondecrease, conversion bounds, suspend documentation,
  capability-state transitions, denied authorization, unavailable devices, and
  mock fault tests; target-specific interval containment against instrumented
  brackets, coarse clocks, preemption/latency spikes, CPU migration, frequency
  change, virtualization, reset, and explicit no-through-completion capability;
- directed correlation-candidate offset/rate/uncertainty containment,
  anchor-based uncertainty growth, lifecycle withdrawal, missing/forged
  derivation evidence, reversed-domain and provider-forgery refusal;
- cross-clock/domain arithmetic refusal, suspend/no-suspend elapsed behavior,
  raw/adjusted drift, fork/exec, VM/container restore, inherited handle, and
  process/machine generation tests;
- Android/iOS application lifecycle tests for background suspension/resume,
  network roaming and path changes, captive-network transitions, and
  battery-budgeted resynchronization.

Exit criteria:

- platform clocks implement core traits without entering protocol code;
- `v0.30.0 implementation stop reached. Run pentest for this exact commit.`

### v0.31.0 - TCP UDP And Resolver Adapters

Status: planned.

Goal: implement bounded standard network transports.

Deliverables:

- TCP/UDP client/server adapters, timeout/cancellation, address policy;
- OS resolver adapter and explicit custom resolver boundary;
- no automatic authenticated-to-legacy fallback.

Verification:

- Linux/Windows/BSD/macOS loopback, short I/O, DNS rebinding fixtures, timeout,
  cancellation, and descriptor exhaustion.

Exit criteria:

- standard transports are portable and protocol-neutral;
- `v0.31.0 implementation stop reached. Run pentest for this exact commit.`

### v0.32.0 - Software Socket Timestamps

Status: planned.

Goal: capture and classify software receive/transmit timestamps.

Deliverables:

- supported OS timestamp APIs and metadata quality;
- packet association and truncation/drop reporting;
- safe fallback to ordinary capture explicitly labeled.

Verification:

- loopback association, multiple queued packets, truncated metadata, reorder,
  and unsupported-platform tests.

Exit criteria:

- timestamps cannot be mistaken for hardware capture;
- `v0.32.0 implementation stop reached. Run pentest for this exact commit.`

### v0.33.0 - Platform Binding Admission

Status: planned.

Goal: admit minimal maintained OS-binding crates where safer than handwritten ABI.

Deliverables:

- current `libc`/`windows-sys` or narrower alternative reviews;
- feature/transitive/native/MSRV/license inventory;
- safe `mundilfari-platform` facade plus narrowly scoped OS-family
  `mundilfari-platform-*-sys` crates for necessary unsafe;
- safe capability adapters for platform page locking and core-dump exclusion,
  with OS-specific failure/revocation reporting and no implicit guarantee;
- isolated safe wrappers and replacement boundaries with no protocol policy.

Verification:

- ABI size/alignment checks, supported target builds, cargo-deny/audit, and
  forbidden dependency leakage tests; page-lock/core-dump capability,
  permission/resource failure, fork/exec/restore, and unsupported-platform
  tests.

Exit criteria:

- generic ABI code is reviewed without entering safe platform, core, or wire
  crate unsafe surfaces;
- `v0.33.0 implementation stop reached. Run pentest for this exact commit.`

### v0.34.0 - Linux Raw Transports

Status: planned.

Goal: implement raw ICMP and Ethernet transport foundations.

Deliverables:

- bounded raw socket configuration and link metadata;
- separately reported raw-link, interface-configuration, and timestamp
  capability/permission errors with interface binding;
- no packet validation policy.

Verification:

- namespace tests, permission denial, malformed link metadata, interface
  removal, and packet capture comparison.

Exit criteria:

- raw transports are isolated and cannot issue arbitrary syscalls;
- `v0.34.0 implementation stop reached. Run pentest for this exact commit.`

### v0.35.0 - Linux Ancillary Timestamp Parsing

Status: planned.

Goal: safely parse `SO_TIMESTAMPING` control messages.

Deliverables:

- alignment/length checked control-message traversal;
- software, transformed hardware, and raw hardware classification;
- explicit Linux old/new timestamp ABI handling, preferring Y2038-safe
  interfaces and labeling or rejecting legacy range limits;
- transmit error-queue association and kernel drop indicators.

Verification:

- synthetic every-byte truncation, alignment variants, multiple messages,
  unknown controls, 32-bit Y2038 boundaries, reorder, and live loopback tests.

Exit criteria:

- no truncated or mismatched ancillary record becomes a valid timestamp;
- `v0.35.0 implementation stop reached. Run pentest for this exact commit.`

### v0.36.0 - Hardware Timestamp Configuration

Status: planned.

Goal: configure and inspect NIC timestamp capabilities safely.

Deliverables:

- reviewed Linux ioctl/netlink adapter;
- separately feature-gated timestamp configuration, capability discovery, and
  exact applied-policy/runtime-authorization reporting;
- restoration and concurrent-change policy.

Verification:

- mock ABI, supported NIC lab, denied permission, hot unplug, rollback, and
  invalid configuration tests.

Exit criteria:

- configuration success is evidence-based and never implies accuracy;
- `v0.36.0 implementation stop reached. Run pentest for this exact commit.`

### v0.37.0 - PHC And Cross Timestamp

Status: planned.

Goal: support Linux PTP hardware clocks.

Deliverables:

- raw PHC timestamp, device identity/generation/reset state, timestamp origin,
  resolution, advertised precision, and supported cross-timestamp methods;
- PHC and system/monotonic methods return bounded `MonotonicReadInterval`
  values and `UntrustedMonotonicCorrelationCandidate` records with exact
  directed device/domain identity and generation, method provenance,
  bracketing/cross-timestamp latency, quantization, driver/device uncertainty,
  and migration/reset/hotplug generation; unsupported methods never collapse a
  raw scalar PHC sample to a zero-width monotonic interval;
- system/monotonic correlation candidates with measured cross-timestamp error,
  exact paired capture anchors, bounded offset/rate/drift derivation roots and
  conditions, calibration, and asymmetry inputs; platform never admits a
  candidate or assigns clock authority;
- Linux PTP character-device/standard-ioctl implementation separated from
  embedded device-specific MMIO;
- device identity and hotplug handling.

Verification:

- mock ioctl corpus, live PHC tests, overflow, stale device, concurrency,
  time-namespace mismatch, cross-timestamp uncertainty and maximum-latency
  benchmarks covering reset and clock-ID lifetime; interval containment,
  scalar-inflation, bracketing order, preemption, hotplug, and method-fallback
  refusal; outward-rounded directed-candidate fixtures, stale provider/device
  generation, anchor substitution, forged narrow bound/recipe, excessive
  uncertainty, and candidate/admitted type separation.

Exit criteria:

- PHC operations are typed, bounded, and separately authorized;
- `v0.37.0 implementation stop reached. Run pentest for this exact commit.`

### v0.38.0 - PPS And Edge Capture

Status: planned.

Goal: capture kernel PPS and generic timing edges.

Deliverables:

- `/dev/ppsN` capabilities, sequence, assert/clear edge, timeout, and quality;
- generic caller-supplied edge capture trait;
- device identity and loss reporting.
- explicit distinction between kernel/device capture and caller-supplied
  already captured edges.

Verification:

- synthetic sequence wrap, missed edge, timeout, live PPS, hot unplug, and
  timestamp correlation tests.

Exit criteria:

- physical edges become observations without inventing civil time;
- `v0.38.0 implementation stop reached. Run pentest for this exact commit.`

### v0.38.1 - RTC And Architectural Counters

Status: planned.

Goal: expose bounded real-time-clock and architectural counter observations
without treating either as automatically valid civil time.

Deliverables:

- RTC read, set-backend boundary, validity, battery/power-loss, oscillator,
  resolution, update-in-progress, device identity, generation, and uncertainty;
- architectural monotonic/cycle counter identity, width, wrap extension,
  frequency generation, invariance, suspend/reset, and untrusted directed
  cross-correlation candidates;
- architectural counter `read_interval()` strategies bind CPU/core/package,
  migration detection, serialization/barrier method, frequency/invariance
  generation, wrap/reset state, resolution, calibration/rate uncertainty, and
  earliest/latest bounds; an un-serialized or migration-ambiguous scalar read
  is diagnostic rather than `[t,t]`;
- read-only safe APIs separated from later discipline authorization;
- platform-specific capability and non-claim reports.

Verification:

- invalid/battery-low RTC, torn register reads, BCD/range faults, century
  ambiguity, counter wrap, frequency change, reset, suspend, CPU migration,
  namespace mismatch, serialization/barrier variants, interval containment,
  scalar inflation, uncertainty provenance, and mock/live platform tests.
  Cross-correlation tests cover direction, outward rounding, frequency/rate
  drift, provider loss, and reset/suspend/migration withdrawal without engine
  admission.

Exit criteria:

- RTCs and cycle counters are typed observations with validity and generation,
  never implicit UTC authorities;
- `v0.38.1 implementation stop reached. Run pentest for this exact commit.`

### v0.38.2 - Embedded MMIO GPIO And Frequency Capture

Status: planned.

Goal: implement deterministic embedded clock/register, GPIO edge, and
frequency-counter backends behind safe capability traits.

Deliverables:

- uniquely owned register/capture tokens and narrowly scoped sys/device crates;
- volatile access, alignment, endianness, memory ordering/barriers, reset and
  power-domain generations, and documented register invariants;
- counter wrap extension, frequency changes, interrupt-versus-poll capture,
  GPIO edge identity/sequence/loss, and frequency-counter gate/calibration
  evidence;
- caller-provided embedded monotonic clocks and MMIO/cycle counters implement
  `read_interval()` with target-declared resolution, capture/interrupt/poll
  latency, calibration/rate uncertainty, domain/reset generation, and optional
  reviewed WCET-backed through-completion capability; missing bounds disable
  strict authority without preventing diagnostic sampling;
- target-specific mock register blocks and no Unix descriptor assumptions.

Verification:

- mock MMIO/register models, misalignment/endian faults, stale ownership,
  reorder/barrier cases, reset/power cycle, counter wrap/frequency change,
  interrupt races, GPIO bounce/loss, frequency calibration, interval
  containment/scalar inflation/missing-bound refusal, claimed WCET violation,
  and representative embedded targets.

Exit criteria:

- embedded hardware access is bounded, generation-aware, and isolated from
  protocol and engine policy;
- `v0.38.2 implementation stop reached. Run pentest for this exact commit.`

### v0.39.0 - Discipline API And Clock Adjustment Backends

Status: planned.

Goal: separate discipline proposals and authorization from internal
platform/device adjustment backends.

Deliverables:

- a separate `mundilfari-discipline` API owning typed discipline proposals,
  target identity/generation, authorization, bounds, and applied results;
- Linux, Windows, BSD, and macOS supported slew/step/frequency operations;
- internal platform and RTC/PHC/oscillator/DAC/DCO adjustment backends not
  re-exported by the ordinary facade;
- `AppliedAdjustment` reporting requested, actually applied, residual, and
  target generation rather than success alone;
- separate read/configure/adjust capabilities and a short-lived
  policy-generated authorization handle rechecked at operation time to close
  discovery/TOCTOU gaps;
- separately named expert in-process embedded API with identical numerical,
  generation, authority, and audit safeguards;
- every step, rate change, PHC/RTC reset, suspend, or device replacement
  publishes a discontinuity and increments affected generations;
- no default backward or post-startup step.

Verification:

- mock kernel/device faults, partial/applied/residual adjustment, saturation,
  stale target generation, authorization revocation between discovery and
  operation, discontinuity publication, isolated VM/embedded tests, rollback
  refusal, and degraded capability.

Exit criteria:

- no protocol parser or client can directly modify a system clock;
- `v0.39.0 implementation stop reached. Run pentest for this exact commit.`

### v0.39.1 - Secure Bounded Persistence Foundation

Status: planned.

Goal: provide one reviewed persistence contract for cookies, bootstrap,
calibration, holdover, policies, and trusted-clock snapshots.

Deliverables:

- state values encoded exclusively through the completed `v0.22.1` canonical
  schema kernel, with explicit maximum record size and unknown-version
  behavior; persistence adds no second envelope or serializer model;
- restored bound-condition references remain unresolved until `v0.7.3`
  resolution verifies exact canonical content or the immutable registry
  generation; persistence integrity never upgrades an assumption reference;
- persisted `ConditionAssessment` or `PolicyAcceptedHardBound` data is
  historical evidence only after restore and must pass fresh `v0.60.6`
  lifecycle/policy/evidence/deadline revalidation before regaining authority;
- serialized or persisted derivation material decodes only as
  `UnverifiedBoundDerivationRecord`; the opaque `VerifiedBoundDerivation<T>`
  has no direct `Deserialize`, canonical-schema decode, or restore path.
  Persistence exports the complete bounded reachable canonical DAG and never a
  process-local derivation handle, arena address, store identity, or generation.
  Restoration must resolve the complete bounded recipe and the later
  `v0.60.3` engine must reverify it against current input claims/observations,
  proof-rule registry, conversion models, source/provider generations, and
  lifecycle state before constructing new authority;
- crash-consistent atomic replacement, partial/torn-write detection, explicit
  durability semantics, and bounded schema migration;
- checksum separated from authenticated integrity and confidentiality;
- secret-bearing snapshot provider boundary, redaction, and best-effort
  clearing without overstated guarantees, plus the exact
  `SecretMemoryProtection` capability retained in snapshot/persistence reports;
- authenticated integrity/confidentiality requested only through the
  `v0.24.1` provider contracts, with unavailable production provider reported
  as a capability limitation;
- typed `RollbackProtection` capabilities: `None`, `BestEffortLocal`,
  `BootSessionBound`, `TrustedMonotonicCounter`, `HardwareSealed`, and
  `RemoteWitnessed`; no mutable local state/key is described as strong
  rollback protection;
- restored state carries its rollback capability and freshness evidence,
  separately from authentication, confidentiality, and corruption detection;
- monotonic generation where the selected trust root supports it,
  boot/session/process/machine-instance and monotonic-domain binding,
  corruption, replay, and lifecycle-discontinuity handling;
- caller-supplied storage/no_std backend traits plus reviewed hosted file
  adapter; protocols import/export bounded values and perform no file I/O.

Verification:

- failure injection at every write/rename/sync boundary, partial/torn records,
  corruption, wrong key, rollback under every capability, attacker-restored
  state plus ordinary local key, copied boot/session state, restored accepted-
  bound token refusal/reassessment, trusted-counter/sealed/remote-witness
  faults, unknown schema, migration chains, size exhaustion, concurrent
  readers, and recovery;
- derivation replay/rollback, cross-engine copy, direct verified-type decode,
  missing or substituted input, stale rule/model/source generation, lifecycle
  withdrawal, handle/store/address leakage, incomplete reachable DAG,
  malformed recipe, and complete bounded re-verification tests.

Exit criteria:

- no protocol or engine invents an unaudited private state-file format;
- `v0.39.1 implementation stop reached. Run pentest for this exact commit.`

### v0.39.2 - Discipline Ownership And Competing Adjusters

Status: planned.

Goal: detect and contain external clock changes by other daemons,
administrators, hypervisors, kernels, or device controllers.

Deliverables:

- typed `ClockDisciplineLease` carrying `DisciplineOwnership` capability
  (`Exclusive`, `Cooperative`, `ObservedOnly`, or `Unmanaged`), holder/target
  identity, lease generation, expiry clock domain, renewal, loss, and platform
  assurance;
- acquisition/release adapters where an OS/device offers enforceable
  ownership, cooperative observation otherwise, and no false exclusivity
  claim;
- independent observation of target phase/rate/configuration and detection of
  changes not correlated to an accepted Mundilfari `AppliedAdjustment`;
- every competing/external change rotates target/lease generation, publishes a
  discontinuity, invalidates proposals/feedback/correlations, and requires
  servo reacquisition;
- helper authorization binds the current ownership mode/generation and cannot
  convert `ObservedOnly` or `Unmanaged` into adjustment authority.

Verification:

- simultaneous Mundilfari/chrony/PTP-style writers, administrator step,
  hypervisor correction, kernel/device autonomous rate change, lease loss/
  expiry/renewal, false exclusivity, cooperative changes, stale proposal/
  feedback, helper race, generation rollover, and VM/platform fault tests.

Exit criteria:

- Mundilfari never continues a servo as though it exclusively controlled a
  target after evidence of competing adjustment;
- `v0.39.2 implementation stop reached. Run pentest for this exact commit.`

### v0.39.3 - Helper Policy And Minimal Discipline Audit Contract

Status: planned.

Goal: freeze the minimal helper policy ceiling and canonical discipline audit
types before any daemon/helper implementation can invent private formats.

Deliverables:

- stable typed `HelperPolicyCeiling` with policy identity/generation,
  provenance, integrity/rollback capability, target/ownership scope,
  per-request and cumulative phase/frequency limits, rate/settling limits,
  expiry monotonic domain, permitted operation classes/handles, fault-latch
  thresholds, and recovery authority;
- verify/stage/semantic-and-capability-validate/atomic-activate policy
  transaction; workers may select only within the active ceiling and cannot
  widen it;
- minimal canonical `DisciplineAuditRecord` carrying strict sequence,
  monotonic domain, TAI interval/model generation, process/machine/session,
  policy/authorization/target/proposal identities and generations, requested/
  applied/residual result, accepted/rejected/fault decision, and reason;
- canonical explicit audit gap/loss record with first/last affected sequence,
  count/range, cause, storage generation, and recovery evidence;
- audit capacity is reserved before an adjustment is authorized; audit-full
  rejects new requests, while an unexpected post-operation audit failure
  latches the helper and must emit a gap/recovery record before reauthorization;
- minimal types use the `v0.22.1` schema and `v0.39.1` persistence foundation;
  later configuration syntax, exporters, retention, chaining, sealing, and
  witnessing may extend but never replace or reinterpret them.

Verification:

- policy identity/provenance/integrity/rollback/generation changes,
  stage/activation races, attempted worker widening, ownership/target mismatch,
  every numerical/rate/settling boundary, exact canonical vectors, audit
  sequence/reorder/duplicate, full storage before authorization, write failure
  after application, reserved gap record exhaustion, fault latch/recovery, and
  later-compatible unknown fields.

Exit criteria:

- the daemon can only consume a pre-reviewed helper ceiling and audit contract,
  never create an implementation-private authority or evidence format;
- `v0.39.3 implementation stop reached. Run pentest for this exact commit.`

### v0.40.0 - Platform And Privilege Security Gate

Status: planned.

Goal: audit platform FFI, raw I/O, timestamps, hardware clocks, and adjustment.

Deliverables:

- machine-readable unsafe inventory, per-block invariants, safe-wrapper/ABI
  review, granular permission model, and privilege-separation plan;
- RTC/counter/MMIO/GPIO/frequency/actuator, namespace identity, discipline,
  ownership/competing-adjuster, lifecycle discontinuity, early canonical-
  schema/crypto-provider, persistence, helper-policy-ceiling, and minimal
  discipline-audit boundary review;
- proof that core, engine, facade, protocol, crypto-state, IPC-schema, and safe
  platform crates still forbid unsafe code;
- resolved critical/high platform findings;
- supported-target capability matrix.

Verification:

- host CI, sanitizers/Miri where applicable, syscall fault injection, live
  hardware subset, ABI/layout assertions, mock-wrapper fuzzing, and focused
  pentest.

Exit criteria:

- platform foundations are approved for protocol integration;
- `v0.40.0 implementation stop reached. Run pentest for this exact commit.`

## Phase 4: Legacy Services And Representations

### v0.41.0 - RFC 867 Daytime

Status: planned.

Goal: implement lossless Daytime client/server behavior.

Deliverables:

- bounded TCP/UDP port 13 transport state;
- raw response bytes and optional explicitly labeled parse candidates;
- no silent authoritative civil-time guess.

Verification:

- arbitrary text/binary, maximum response, truncation, timeout, candidate
  ambiguity, client/server loopback, and RFC examples.

Exit criteria:

- Daytime is inspectable but disabled for secure clock discipline;
- `v0.41.0 implementation stop reached. Run pentest for this exact commit.`

### v0.42.0 - RFC 868 TIME

Status: planned.

Goal: implement TCP/UDP TIME with explicit era resolution.

Deliverables:

- exact 32-bit big-endian codec, client, and server;
- RFC 868 epoch and rollover context;
- unsolicited/trailing/truncated reply rejection.

Verification:

- epoch, maximum counter, 2036 rollover windows, ambiguity, every truncation,
  and loopback interoperability.

Exit criteria:

- TIME observations preserve insecurity and era warnings;
- `v0.42.0 implementation stop reached. Run pentest for this exact commit.`

### v0.43.0 - ICMP Timestamp

Status: planned.

Goal: implement ICMP Timestamp Request/Reply inspection and client/server logic.

Deliverables:

- type 13/14 codec, checksum, identifiers, and milliseconds-since-midnight;
- raw transport adapter and day/context ambiguity;
- rate-limited server disabled by default.

Verification:

- checksum vectors, identifier mismatch, nonstandard values, midnight wrap,
  permission denial, packet captures, and amplification tests.

Exit criteria:

- ICMP timing cannot enter discipline under strict or balanced policy;
- `v0.43.0 implementation stop reached. Run pentest for this exact commit.`

### v0.44.0 - Historic Internet Clock Services

Status: planned.

Goal: implement documented DCNET and NIST ACTS timing.

Deliverables:

- separate focused crates and exact historical revision records;
- serial/modem framing, quality/health, and propagation fields where specified;
- historical-only feature gates.

Verification:

- authoritative examples/captures, malformed framing, timeout, line noise,
  rollover, and simulator interoperability.

Exit criteria:

- historical support is lossless, isolated, and never a secure default;
- `v0.44.0 implementation stop reached. Run pentest for this exact commit.`

### v0.45.0 - BSD timed And DCE DTS

Status: planned.

Goal: implement documented timing portions of BSD TSP and DCE DTS.

Deliverables:

- message codecs, state transitions, sequence/election/time fields;
- exact accessible specification scope and explicit blocked clauses;
- compatibility-only policy.

Verification:

- reference captures, malformed messages, state-sequence mutation, replay,
  election conflict, and independent implementation tests.

Exit criteria:

- no guessed DCE or vendor behavior is claimed;
- `v0.45.0 implementation stop reached. Run pentest for this exact commit.`

### v0.46.0 - XMPP Entity Time And MS-SNTP

Status: planned.

Goal: implement modern XMPP time and documented Microsoft SNTP extensions.

Deliverables:

- bounded XMPP entity-time values/state integration;
- MS-SNTP-specific fields and validation isolated from base NTP;
- explicit surrounding-transport application boundaries.

Verification:

- official examples, namespace/version errors, extension round trips,
  malformed input, and interoperability.

Exit criteria:

- extensions cannot weaken shared NTP validation silently;
- `v0.46.0 implementation stop reached. Run pentest for this exact commit.`

### v0.47.0 - HTTP Mail And ASN.1 Time

Status: planned.

Goal: implement security-relevant Internet and certificate time formats.

Deliverables:

- HTTP-date and mail-date variants under explicit compatibility mode;
- strict ASN.1 UTCTime and GeneralizedTime;
- canonical encoding, year-window, offset, and leap policy.

Verification:

- RFC/DER vectors, invalid dates/zones, noncanonical DER, year boundaries,
  whitespace, every truncation, and round trips.

Exit criteria:

- strict and legacy text forms cannot be confused;
- `v0.47.0 implementation stop reached. Run pentest for this exact commit.`

### v0.48.0 - RFC 3339 And IXDTF

Status: planned.

Goal: implement complete bounded RFC 3339 and RFC 9557 IXDTF.

Deliverables:

- borrowed parse and canonical encode;
- offsets, fractional precision, unknown-offset and IXDTF annotations;
- duplicate/critical annotation policy and raw preservation.

Verification:

- official vectors, annotation nesting/work limits, invalid calendars, leap
  values, differential tests, and exact round trips.

Exit criteria:

- Internet date strings retain all standardized semantics;
- `v0.48.0 implementation stop reached. Run pentest for this exact commit.`

### v0.49.0 - ISO 8601 Profiles

Status: planned.

Goal: implement only legitimately licensed ISO 8601 profiles in the registry.

Deliverables:

- exact revision/clause record and bounded codecs;
- reduced precision, ordinal/week, duration, interval, and recurrence scope as
  assigned by the licensed specification;
- explicit exclusions.

Verification:

- licensed vectors, boundary/ambiguity/malformed corpus, clause map, and
  independent review.

Exit criteria:

- no generic “ISO date” claim exceeds implemented licensed clauses;
- `v0.49.0 implementation stop reached. Run pentest for this exact commit.`

### v0.50.0 - TZif POSIX TZ And iCalendar

Status: planned.

Goal: implement bounded local-time rule representations.

Deliverables:

- RFC 9636 TZif, POSIX TZ strings, and iCalendar VTIMEZONE components;
- transition/resource limits, unknown field handling, and version preservation;
- no bundled silently stale zone database.

Verification:

- RFC/IANA vectors, hostile counts/offsets, transition extremes, differential
  zone conversions, and fuzzing.

Exit criteria:

- local civil conversion uses explicit versioned rule data;
- `v0.50.0 implementation stop reached. Run pentest for this exact commit.`

### v0.51.0 - TZDIST

Status: planned.

Goal: implement RFC 7808 TZDIST client/server state machines.

Deliverables:

- discovery, capabilities, list/get/expand/change flows;
- bounded HTTP/application transport boundary and cache validators;
- response trust/provenance policy.

Verification:

- RFC examples, pagination/resource bounds, stale caches, redirects, malformed
  zones, client/server interoperability, and SSRF policy tests.

Exit criteria:

- downloaded zone rules never become trusted without explicit source policy;
- `v0.51.0 implementation stop reached. Run pentest for this exact commit.`

### v0.52.0 - Time Data Loaders

Status: planned.

Goal: load leap, IERS/EOP, and external scale-offset data with provenance.

Deliverables:

- strict bounded loaders and canonical internal snapshots;
- signature/checksum hooks plus candidate activation metadata, expiry,
  rollback, and conflict inputs; caller-owned commit belongs to `v0.52.1`;
- no automatic network download in core.

Verification:

- official datasets, truncation/corruption, stale/future data, rollback,
  conflicting authorities, and deterministic hashes.

Exit criteria:

- scale conversion data is versioned, inspectable, and replaceable;
- `v0.52.0 implementation stop reached. Run pentest for this exact commit.`

### v0.52.1 - Hosted Time-Data Update Orchestration

Status: planned.

Goal: update leap, EOP, and scale-offset snapshots through explicit
application policy without adding automatic network behavior to core.

Deliverables:

- bounded `TimeDataProvider` values for embedded/static snapshots,
  application-supplied files, OS-managed data, and optional explicitly
  caller-authorized remote retrieval;
- source identity, provenance, integrity, rollback capability, validity,
  expiry, model generation, retrieval authorization, network action, and
  resource limits in every candidate/report;
- caller-serialized verify → stage → compare → commit transaction using the
  generic loader, persistence, lifecycle, and conversion-generation
  boundaries; the update guard rejects or serializes competing writers;
- caller-owned commit is indivisible but provides no concurrent-reader or
  `TrustedClock` publication guarantee before
  `v0.137.3`;
- failed refresh leaves the current caller-owned snapshot untouched and reports
  stale/expired/degraded/faulted state; withdrawal and rollback invalidate
  dependent conversions;
- no remote retrieval in core, protocol crates, builds, tests, or default
  constructors;
- `TrustedClock::system_defaults(...)` reports the selected provider, source,
  network behavior, refresh policy, fallback, and current capability.

Verification:

- embedded/file/OS/authorized-remote providers, authorization refusal, SSRF/
  redirect/size/work limits, signature/checksum failure, older/conflicting
  snapshots, competing-writer rejection/serialization, stage/compare/commit
  failure and crash injection, withdrawal, expiry, failed refresh, offline
  restart, explicit absence of a concurrent-reader guarantee, and
  capability/system-default reports.

Exit criteria:

- hosted applications can maintain time data without hidden download,
  rollback, or partial-activation behavior;
- `v0.52.1 implementation stop reached. Run pentest for this exact commit.`

### v0.52.2 - Remote Time-Data Trust Bootstrap

Status: planned.

Goal: require an independently established trust path for remotely obtained
leap, EOP, and scale-offset artifacts without circularly trusting the
candidate data.

Deliverables:

- candidate data is never used to validate the transport session, certificate,
  signature time, or credential context that delivered that same candidate;
- every remote artifact requires at least one explicitly admitted independent
  path: signed artifact identity under a pinned/admitted verification key,
  pinned transport SPKI/key, or HTTPS whose complete credential context was
  validated using an already admitted trusted-time interval/model generation;
- typed transport and artifact authorities, signing/transport identities,
  source URI, redirect chain, retrieval generation, and evidence carried into
  the common candidate pipeline;
- redirects cannot silently change artifact authority, signer, pinned
  identity, scheme, host policy, or retrieval authorization;
- signing/transport key activation, overlap, expiry, compromise, revocation,
  rollback, emergency replacement, and offline trust-root update policy;
- offline/manual and OS-managed ingestion use the identical bounded
  verify → stage → compare → commit caller-owned snapshot pipeline and cannot
  bypass artifact identity/provenance checks; concurrent publication remains
  deferred to `v0.137.3`;
- the early milestone accepts caller-supplied authenticated fetch evidence;
  no built-in production TLS claim exists before `v0.72.0`/`v0.75.1`.

Verification:

- circular bootstrap attempt where candidate time would validate its own TLS
  chain, pinned signer/SPKI success/failure, already-admitted-time HTTPS,
  wrong/expired/revoked/rotated signer, compromised/rolled-back key, redirect
  authority/scheme/host/signature changes, replayed/older artifact, offline
  and OS-managed parity, partial download, transport success with artifact
  failure, and current-model retention.

Exit criteria:

- no remotely or manually obtained time-data candidate can establish the trust
  used to authenticate itself;
- `v0.52.2 implementation stop reached. Run pentest for this exact commit.`

### v0.52.3 - EOP And Scale-Offset Admission Proofs

Status: planned.

Goal: require non-forgeable typed admission for every non-leap data component
that can alter trusted conversions.

Deliverables:

- three non-substitutable trust levels:
  `RetrievalClaim` contains the retrieved bytes/content digest, claimed source
  and provider identity, provider generation, platform metadata, claimed
  capability, and supplied signature/attestation material but is explicitly
  untrusted; opaque `ArtifactIntegrityEvidence` records verification of the
  applicable signature, digest, attestation, freshness, registered verifier
  provider identity/generation/capability, and rollback evidence without
  granting source authority; only an admitted snapshot applies configured
  data-family authority/role and admission policy;
- platform implementations may return only `RetrievalClaim`; neither a custom
  adapter, a claimed privileged evidence variant, cloned provider identity, nor
  an `integrity: true`-style field can construct `ArtifactIntegrityEvidence` or
  obtain admission;
- OS-managed data without cryptographic verification uses a distinct opaque
  `ConfiguredPlatformTrustEvidence` assurance result binding the configured
  platform provider identity/generation/capability and explicit non-claims; it
  is never named artifact verification or treated as cryptographic proof;
- platform-specific attestation verification may use an admitted verifier
  provider, but evidence retains that verifier's identity, generation,
  assurance capability, verification inputs, and non-claims; callback output
  is a bounded structured result and never a trusted boolean;
- opaque, engine-policy-constructed `AdmittedEopSnapshot` and
  `AdmittedScaleOffsetSnapshot`, plus bounded `AdmittedTimeDataSnapshot`
  aggregation for coherent non-leap conversion-data candidates; component
  types cannot be substituted;
- crate ownership and dependency direction are fixed:
  `mundilfari-core` owns raw/structurally validated EOP and offset snapshots
  plus the protocol-neutral untrusted `RetrievalClaim` contract,
  `mundilfari-platform` owns platform retrieval/attestation implementations
  that emit those claims,
  `mundilfari-engine` owns verifier-provider admission, provider-neutral
  integrity/attestation verification, private `ArtifactIntegrityEvidence` and
  `ConfiguredPlatformTrustEvidence` constructors, separate configured source-
  authority/role admission policy, admitted constructors/wrappers, and
  revalidation, while the `mundilfari` facade owns ergonomic policy builders/
  default orchestration and consumes engine-issued proofs for `TrustedClock`
  publication;
- core and platform never depend on engine/facade admission authority; engine
  consumes only protocol-neutral core snapshots/claims and never depends on
  platform, while facade composes the layers without adding a second
  verification or admission implementation;
- each proof binds content hash and model generation, artifact/source
  identity and configured authority, the exact retrieval claim and opaque
  integrity or configured-platform-trust evidence identity/assurance basis,
  verifier/provider generation, separate source-authority/role decision,
  admission-policy generation, validity and expiry with monotonic domain,
  rollback evidence/capability, applicable conversion-context generation, and
  current withdrawal state;
- artifact authentication and admission authority remain independent: a
  correctly signed artifact from an unconfigured or wrong-role signer is
  represented by valid `ArtifactIntegrityEvidence` but is not admitted;
- admission revalidation detects withdrawal, expiry, rollback, authority/
  policy change, artifact replacement, and conversion-generation mismatch;
- raw EOP and scale-offset snapshots remain available only to isolated
  caller-owned expert conversion contexts and cannot update `TrustedClock` or
  the default facade;
- no leap authority duplication: leap evidence still requires the engine-owned
  `AdmittedLeapCandidate` at `v0.61.1`; concurrent publication of every
  admitted component remains deferred to `v0.137.3`.

Verification:

- forged/private construction, forged custom adapters, claimed privileged
  variants or integrity booleans, cloned/unregistered provider identities,
  stale attestations, unsupported verification capabilities, valid integrity
  from an unauthorized/wrong-role source, `ArtifactIntegrityEvidence` survival
  across failed authorization, configured-platform-trust versus cryptographic
  assurance separation, forged verifier callbacks/booleans, correct signature
  with absent/wrong authority,
  hash/model/source/retrieval/policy/context mismatch, expiry/withdrawal/
  rollback/replacement between verification, admission, and revalidation,
  mixed EOP/offset generations, raw-snapshot default publication compile
  failures, bounded aggregate capacity, caller-owned expert-context behavior,
  crate dependency/feature matrices, and compile-fail tests proving core,
  platform, protocol, and custom adapter crates cannot construct integrity,
  configured-platform-trust, or admitted values.

Exit criteria:

- every conversion-data update crosses untrusted retrieval, independent
  verification, configured-authority admission, and later revalidation; no raw
  or merely authenticated EOP/scale-offset artifact can change the default
  trusted conversion context;
- `v0.52.3 implementation stop reached. Run pentest for this exact commit.`

### v0.53.0 - Documented Vendor Extension Framework

Status: planned.

Goal: admit documented non-GNSS vendor extensions without guessing proprietary
behavior or weakening base-protocol validation.

Deliverables:

- revision-qualified vendor and extension identifiers with exact source,
  affected base protocol, criticality, trust, and conflict metadata;
- bounded opaque preservation for unknown non-critical extensions and
  fail-closed rejection for unknown critical extensions;
- separate codecs/modules or focused crates when an extension has independent
  state or security behavior;
- no GNSS receiver, navigation, NMEA, RTCM, RINEX, gpsd, OSNMA/QZNMA, or
  satellite-PPS interpretation, all of which remains Navheim-owned;
- undocumented and partially documented behavior retained as explicit
  non-claims and disabled by default.

Verification:

- documented extension vectors, identifier collisions, wrong base revision,
  malformed/oversized values, unknown criticality, downgrade, feature
  combinations, round trips, and opaque-forwarding limits.

Exit criteria:

- vendor support is traceable to exact public or legitimately held normative
  material and never inferred from captures or another implementation;
- `v0.53.0 implementation stop reached. Run pentest for this exact commit.`

### v0.53.1 - Legacy Format And Extension Security Gate

Status: planned.

Goal: audit legacy protocols, time representations, and vendor extensions.

Deliverables:

- downgrade/non-authority review and complete format/extension clause maps;
- parser/resource fuzz reports;
- resolved critical/high findings and compatibility non-claims.

Verification:

- full legacy/format/extension corpus, differential implementations,
  no_std/MSRV matrix, and focused pentest.

Exit criteria:

- legacy or vendor-extension support cannot silently authorize clock changes;
- `v0.53.1 implementation stop reached. Run pentest for this exact commit.`

## Phase 5: NTP And SNTP

### v0.54.0 - NTP Base Wire

Status: planned.

Goal: implement historical/current NTP base headers losslessly.

Deliverables:

- leap, version, mode, stratum, poll, precision, delay/dispersion, identifiers,
  and four timestamps;
- borrowed decode and caller-owned encode;
- reserved/version-aware values.

Verification:

- RFC vectors, every field boundary/truncation, arbitrary bytes, round trips,
  and packet capture comparison.

Exit criteria:

- shared NTP wire code is usable without a network client;
- `v0.54.0 implementation stop reached. Run pentest for this exact commit.`

### v0.55.0 - NTP Timestamp Era And Fixed Point

Status: planned.

Goal: implement exact NTP timestamps and signed fixed-point fields.

Deliverables:

- raw fractions, eras, era context, short formats, distance components;
- explicit rounding and quantization;
- ordered arithmetic without overflow.

Verification:

- RFC era examples, 2036 boundaries, negative deltas, maximum fractions,
  fixed-point extremes, and oracle comparison.

Exit criteria:

- NTP timestamps cannot be confused with POSIX or era-zero time;
- `v0.55.0 implementation stop reached. Run pentest for this exact commit.`

### v0.56.0 - NTP Extension Fields Checksum Complement And MAC

Status: planned.

Goal: implement the distinct updated extension-field, UDP checksum-complement,
and legacy MAC behaviors.

Deliverables:

- RFC 7821 UDP checksum-complement behavior;
- RFC 7822 extension-field framing and RFC 9748 registry updates;
- RFC 8573 AES-CMAC update requesting MAC operations only through the
  `v0.24.1` provider contract and recording algorithm/key/provider assurance
  and usage generation;
- unknown extension preservation and criticality;
- ambiguity resolution between extensions and legacy MACs.

Verification:

- official examples, length/alignment/padding, duplicate fields, ambiguous
  tails, every truncation, and round trips.

Exit criteria:

- extension parsing follows all incorporated NTP updates; AES-CMAC behavior is
  provider-neutral and has no production-assurance claim until `v0.72.0`;
- `v0.56.0 implementation stop reached. Run pentest for this exact commit.`

### v0.57.0 - SNTP Client

Status: planned.

Goal: deliver a strict single-shot SNTP client engine.

Deliverables:

- request construction, origin matching, four-timestamp delay/offset;
- unpredictable request/transmit identity and endpoint, version, mode,
  association, origin, stratum, leap, root-distance, loop, KoD, and era
  validation;
- duplicate/replay rejection, explicit response/extension budgets, and no
  discipline authority or authenticated-to-legacy downgrade;
- fixed-storage polling API.

Verification:

- simulator exchange vectors, replay/origin mismatch, KoD, negative delay,
  rollover, malformed responses, and independent server interoperability.

Exit criteria:

- one-shot results are bounded observations, not automatic clock changes;
- `v0.57.0 implementation stop reached. Run pentest for this exact commit.`

### v0.58.0 - SNTP Server

Status: planned.

Goal: implement a bounded amplification-resistant SNTP server.

Deliverables:

- valid client admission, server timestamps, root/quality fields;
- per-source/global rate limits and controlled KoD;
- response-size accounting before encode, bounded extension work, and no
  response policy for malformed or suspicious requests.

Verification:

- client/server interoperability, reflection ratio, spoofed sources, floods,
  malformed packets, time-source fault, and rate-limit recovery.

Exit criteria:

- default server behavior cannot be used as an avoidable amplifier;
- `v0.58.0 implementation stop reached. Run pentest for this exact commit.`

### v0.59.0 - NTP Association And Clock Filter

Status: planned.

Goal: implement long-running source association and clock filtering.

Deliverables:

- reach register, poll state, sample window, root distance, dispersion, jitter;
- stale/restart/KoD state and bounded sample storage;
- monotonic timers;
- NTP association-local filtering only: no multi-source quorum, falseticker
  rejection, clustering, combining, diversity, or discipline authority.

Verification:

- RFC examples, reach transitions, loss/reorder, clock steps, poll boundaries,
  stale samples, and simulator traces.

Exit criteria:

- source state is deterministic and restart-safe;
- `v0.59.0 implementation stop reached. Run pentest for this exact commit.`

### v0.60.0 - Generic Interval Quorum And Falseticker Rejection

Status: planned.

Goal: implement protocol-neutral interval intersection and candidate admission
inside `mundilfari-engine` before any multi-source NTP composition.

Deliverables:

- engine-owned correctness interval construction, intersection, survivor
  count, and
  falseticker evidence under explicit `n`, maximum faulty diversity groups
  `f`, required overlap, freshness, and path-delay assumptions;
- every candidate and result carries the exact immutable `v0.7.2`
  `BoundAssumptionsId` for its canonical condition; raw interval intersection
  uses `All`, while the quorum guarantee uses a reviewed `AtLeast`,
  `AtMostFaulty`, or `Derived` rule binding exact `n`, `f`, policy, membership,
  diversity/correlation, freshness, and path-delay generations rather than
  conjuncting every contributing source claim;
- incompatible, unknown-rule, stale-generation, or capacity-exhausted
  condition construction returns explicit unsafe/insufficient status rather
  than a narrower interval or stronger/weaker formula;
- generic validated-observation inputs with no NTP packet, association,
  transport, poll, or wire type dependency;
- bounded source cardinality and tie behavior;
- no source weighting yet.

Verification:

- published algorithm examples, Byzantine groups, disjoint/split intervals,
  malicious majorities, impossible-guarantee cases, identical endpoints,
  permutations, assumption loss/substitution/incompatibility/capacity,
  threshold truth tables, conjunct-all regression cases, and property tests.

Exit criteria:

- malicious outliers cannot enter the survivor set by simple averaging and no
  protocol crate owns a copy of the quorum algorithm;
- `v0.60.0 implementation stop reached. Run pentest for this exact commit.`

### v0.60.1 - Runtime Bound-Condition Assessment

Status: planned.

Goal: assess whether the assumptions of a canonical conditional hard-bound
claim are currently supported without yet granting policy acceptance.

Deliverables:

- `ResolvedBoundCondition` proves only canonical structure/content and a
  `v0.7.4` borrowed or owned `HardBoundClaimView<'_, T>` remains usable for
  conditional, diagnostic, or untrusted data; neither representation implies
  that any atom currently holds;
- bounded `ConditionAssessment` with explicit `Supported`, `Contradicted`,
  `Indeterminate`, `Expired`, and `Withdrawn` status, exact
  `BoundAssumptionsId`, policy/membership/source/correlation/evidence
  generations, evidence identities or bounded digest, evaluation instant and
  full `MonotonicClockId`, conservative `valid_until`/re-evaluation deadline,
  reasons, assurance, and non-claims;
- every assessed atom carries a bounded structured `SupportBasis` with
  independent `EvidenceOrigin` (measurement, external assertion, or configured
  assumption), `IntegrityBasis` (none/digest/cryptographically verified),
  `AuthorityBasis` (none, asserted identity, or policy-recognized authority),
  and direct-versus-derived lineage. These are orthogonal axes: one measurement
  may also be cryptographically protected and authority-issued without losing
  any fact;
- derived support binds its rule and complete bounded transitive leaf-basis
  set/digest; it never replaces that set with a bare `Derived` label.
  Condition composition preserves every atom's axes/provenance rather than
  upgrading to the strongest input, and an `AtMostFaulty`/Byzantine-budget
  configuration can be accepted only with its configured-assumption origin
  still visible, never reported as measured evidence merely because another
  axis is cryptographically verified or authority-recognized;
- reviewed multi-valued truth tables for `Atom`, `All`, `Any`, `AtLeast`,
  `AtMostFaulty`, and every admitted `Derived` proof rule; indeterminate,
  expired, withdrawn, and contradictory members are preserved in the
  derivation report and never coerced to a trusted boolean;
- atom assessors are engine-admitted, typed, bounded providers tied to exact
  source, calibration, oscillator/model, freshness/path-delay, authority,
  diversity/correlation, policy, membership, and lifecycle generations;
  provider callbacks return structured evidence, not `is_true`;

Verification:

- unknown, contradicted, indeterminate, expired, withdrawn, and restored atoms;
  exhaustive `Atom`/`All`/`Any`/threshold/fault-rule tables; structured support-
  axis preservation, transitive-leaf retention, configured-assumption honesty,
  callback re-entry, generation change, and bounded assessment exhaustion.

Exit criteria:

- canonical condition structure and current runtime support are distinct typed
  states, and no assessment alone grants a hard bound;
- `v0.60.1 implementation stop reached. Run pentest for this exact commit.`

### v0.60.2 - Proof-Bearing Monotonic Correlation Admission

Status: planned.

Goal: admit directed monotonic-domain correlations only from current,
non-circular numerical proofs and independently valid endpoint domains.

Deliverables:

- engine is the sole owner of
  `AdmittedMonotonicDomainCorrelation` construction. Admission verifies the
  complete `v0.16.0` untrusted candidate, but provider registration is only an
  identity/authorization input and never proves its numerical claims. The
  existing bounded derivation verifier must independently produce current
  `VerifiedBoundDerivation` and `PolicyAcceptedHardBound` values for the exact
  offset, rate-ratio, and drift claims/anchors. Their canonical conditions are
  composed with `All`; snapshot-consistent `ConditionAssessment` preserves
  every atom's measured/configured/asserted `EvidenceOrigin`,
  `IntegrityBasis`, `AuthorityBasis`, direct/derived lineage, and complete
  transitive `SupportBasis`;
- correlation admission captures and rechecks one generation vector spanning
  provider registration/identity, directed endpoint domains, exact paired
  anchors/pairing generation, observation method, all derivation/condition/
  assessment/evidence/policy/model generations, suspend/reset/migration
  compatibility, lifecycle, and uncertainty ceiling. The admitted value binds
  those verified derivations, accepted tokens, assessments/support bases, and
  anchors; rate/drift uncertainty grows outward from the anchors at every
  translation rather than trusting a provider-supplied final number;
- initial correlation numerical derivation and condition-assessment admission
  is acyclic by construction: the verifier walks the complete bounded
  transitive recipe, condition, and `SupportBasis` leaves and rejects any
  dependency on any current, stale, replaced, or historical
  `AdmittedMonotonicDomainCorrelation` identity or a claim/assessment derived
  through one. This applies to both endpoints and every intermediate derived
  claim. A future correlation-on-correlation proof model requires its own
  versioned bounded dependency DAG, atomic cycle check, canonical ordering,
  replacement semantics, resource limits, and pentest; it is not implied by
  direct translation;
- admitted `CorrelationValidity` initially accepts only independently checked
  source and target endpoint deadlines. Admission and every strict use read
  both exact domains independently and require each conservative latest edge
  to precede its own deadline. Neither deadline may be translated by the
  candidate/correlation under admission, by a dependent authority, or by an
  indirect cycle. No single aggregate deadline substitutes for this pair;
- the opaque result exposes only direct outward-rounded translation. Missing/
  invalid derivation, unsupported/expired/withdrawn assumptions, provider
  registration without adequate evidence, forged narrow bounds or anchors,
  circular validity, two-node or longer proof-support cycles, replaced/restored
  correlation references, excessive uncertainty, reverse use, implicit
  composition, and stale candidates fail closed;
- either domain/provider reset, suspend incompatibility, rate-semantics or
  scope/migration change, expiry, withdrawal, or generation change invalidates
  the admitted correlation through reserved lifecycle propagation and every
  dependent admission/consensus/publication state before later strict use;

Verification:

- candidate/admitted confusion, provider registration without evidence, forged
  offset/rate/drift bounds or anchors, missing/substituted proof material,
  assumption withdrawal, independent endpoint expiry/reset, circular validity,
  A→B/B→A and longer proof-support cycles, replacement generations, historical
  restore references, outward rounding, and lifecycle invalidation.

Exit criteria:

- only engine-issued, proof-bearing, acyclic-by-construction directed
  correlations can translate monotonic values;
- `v0.60.2 implementation stop reached. Run pentest for this exact commit.`

### v0.60.3 - Verified Bound Derivation And Engine Proof Ownership

Status: planned.

Goal: verify complete hard-bound derivations into source-arena-independent,
non-forgeable engine proof state.

Deliverables:

- a non-forgeable `VerifiedBoundDerivation<T>` proves that the exact claimed
  endpoints follow from admitted inputs before policy can accept the bound. It
  is created only by engine verification of the complete `v0.7.1`–`v0.15.0`
  `UnverifiedBoundDerivation<T>`; missing, truncated, digest-only, over-budget,
  or externally unresolved recipes fail closed. A root derivation binds the
  observation identity, source/provider/evidence identities and generations,
  original finite interval, and output claim digest. A derived proof binds
  every ordered input claim and derivation digest, the bounded interval/
  conversion operation, exact input and output endpoints, rounding direction
  and policy, conversion-model identity and generation, canonical output
  condition, and output claim digest;
- successful verification materializes a source-arena-independent
  `VerifiedBoundDerivation<T>` containing the canonical proof/claim identities,
  verified operation/model/rule inputs, and every lifecycle/generation
  dependency needed for revalidation. Hosted forms own the bounded state;
  no_std forms store it inline or return the semantic
  `VerifiedBoundDerivationRef<'engine, T>` projection over
  `EngineProofHandle<'engine, VerifiedDerivationKind, T>` from `v0.7.4`.
  Resolution uses the checked branded, nonwrapping-generation engine store;
  neither form contains an undocumented pointer or owner reference to
  caller/source-arena storage;
- engine verification resolves the claim's mandatory typed
  `DerivationHandle<'arena, T>` against the exact admitted arena brand/
  generation. It obtains an immutable read lease or frozen pinned snapshot,
  walks the complete reachable canonical DAG under budget, materializes the
  bounded verification input, and releases all arena locks/leases before any
  atom assessor or other external callback. Reacquisition rechecks brand,
  store/node/eviction generations before issuance; concurrent eviction,
  reinterning, or import requires exclusive write access and causes bounded
  retry or indeterminate failure rather than use-after-reuse. Stale/evicted/
  foreign/cross-domain handles and geometry-only intervals fail closed. Import
  from persistence/IPC must first atomically reintern the complete unverified
  record into a bounded current arena;

Verification:

- root and derived recomputation, adversarial narrowing, every operation/model/
  endpoint/rounding substitution, missing/truncated/over-budget DAGs, stale or
  foreign handles, eviction/import races, source-arena drop before/during/after
  promotion, no_std engine-store generation faults, and proof identity
  equivalence.

Exit criteria:

- verified engine proofs are complete, bounded, source-arena-independent, and
  impossible to construct from geometry, digests, or unresolved records alone;
- `v0.60.3 implementation stop reached. Run pentest for this exact commit.`

### v0.60.4 - Atomic Multi-Root Batch Verification

Status: planned.

Goal: verify several policy-visible roots under one bounded generation snapshot
without order-selected authority or a successful prefix on global abort.

Deliverables:

- one owned multi-root set may supply several verification inputs through
  independent root views while sharing immutable source DAG storage. A bounded
  admission list maps each policy-visible `BatchMemberId` to a canonical root
  identity. Duplicate canonical roots share structural computation but retain
  distinct source/lifecycle memberships only when the membership and
  correlation/diversity policy explicitly admits them as distinct. Otherwise
  admission rejects or coalesces them for quorum counting. Computation sharing
  never implies independence, and distinct members never alias accepted-token
  identity;
- multi-root verification returns a bounded `BatchVerificationOutcome<T>`.
  Before verification work it canonicalizes admitted membership and processes
  roots by canonical root identity then `BatchMemberId`, never caller order.
  Results bind the complete admitted membership identity/generation and use
  stable ordering, so input permutations have identical outcome identities,
  result order, and resource-accounting rules;
- one batch transaction captures a single global policy/membership/evidence/
  provider/rule/model/lifecycle generation snapshot plus bounded root-specific
  evidence vectors. Each shared derivation node is verified once under that
  snapshot. Structural failure propagates to every transitively dependent root,
  while root-specific evidence or condition failure affects only that
  membership; independent roots continue so a completed batch reports every
  member;
- `BatchVerificationOutcome<T>` is explicitly `Complete` or `Aborted` with
  disjoint member types. `Complete` contains exactly one processed
  `CompleteMemberStatus<T>`—accepted, failed, contradicted, expired,
  indeterminate, or withdrawn—for every admitted member and may convert to
  non-forgeable `CompleteBatchVerification<T>`. `CompleteMemberStatus` has no
  `Unprocessed` variant. Successful per-root proof/token identities equal
  independent verification under the same snapshot. Consensus or any API
  claiming the full admitted membership set requires that complete witness,
  never an iterator or prefix of successes;
- cancellation, shared work-budget exhaustion, snapshot invalidation, or
  internal invariant failure globally aborts the transaction and mints no
  externally consumable `VerifiedBoundDerivation` or
  `PolicyAcceptedHardBound`, including work completed before the abort.
  `Aborted` uses only `AbortMemberDiagnostic`: already visited affected members
  report diagnostic `Indeterminate` state and unvisited members report
  `Unprocessed`; snapshot invalidation may deterministically mark every member
  indeterminate. Thus `Unprocessed` exists only inside
  `BatchVerificationOutcome::Aborted`. The aborted outcome still reports
  complete membership accounting, abort reason, canonical stopping checkpoint,
  unique shared work, per-root work, and consumed/unused budget, but cannot
  construct or convert to `CompleteBatchVerification`;
- resource accounting is complete and stable: shared-node work is charged once
  to the unique total and attributed to reachable roots by one documented
  deterministic rule; root/evidence work remains per member. Capacity checks
  cover result slots and accounting metadata as well as DAG work, and no
  partial outcome can be consumed as the full admitted membership set;
- a complete witness preserves every configured member, its terminal status,
  and the original policy-defined `n`. Only a member with a current
  `PolicyAcceptedHardBound` is an eligible interval contributor. Failed,
  contradicted, expired, indeterminate, or withdrawn processed members
  contribute no interval and no vote, but cannot be filtered out to reduce
  `n`, `f`, the required overlap, or any threshold. `Unprocessed` cannot appear
  in this witness, and quorum entry has no API accepting
  `BatchVerificationOutcome::Aborted` or `AbortMemberDiagnostic`. Too few
  remaining eligible contributors yields explicit `Insufficient` or `Unsafe`,
  never a quorum recomputed over a smaller denominator;
- removing, merging, or reclassifying a member requires atomic installation of
  a new membership generation and complete reassessment under that generation.
  A caller-side filtered result list, duplicate-root optimization, or failed
  refresh cannot mutate the membership embodied by
  `CompleteBatchVerification`;

Verification:

- canonical root/member permutations, shared DAGs, duplicate roots, shared-node
  failure fan-out, root-specific evidence isolation, cancellation and global
  exhaustion after every node/root, snapshot invalidation after every prefix,
  complete versus aborted type-state, full accounting, original-`n`
  preservation, and compile-fail `Unprocessed`/complete-witness mixing.

Exit criteria:

- global abort mints no proof/token prefix, and only a fully processed
  complete-membership witness can leave batch verification;
- `v0.60.4 implementation stop reached. Run pentest for this exact commit.`

### v0.60.5 - Batch Admission Validity And Refresh Transactions

Status: planned.

Goal: install non-authoritative admitted membership and report prior-state
refresh outcomes with fenced, bounded, linearizable transactions.

Deliverables:

- `CompleteBatchVerification` is processed membership/verification state. A
  separate `BatchAdmissionState<T>` binds the exact witness identity/
  generation, every currently accepted member on which that admission-state
  claim depends, policy/membership/correlation generations, and a conservative
  `AdmissionValidity` in one explicit `MonotonicClockId`. It is explicitly not
  time authority and has no conversion into a servo observation, discipline
  proposal, synchronized publication, trusted-time result, or later
  `ConsensusAuthority`; only the `v0.61.0` consensus constructor may consume it
  with the complete witness and produce time authority under a proof rule;
- admission validity never chooses an arbitrary member deadline. When all
  required dependencies use the admission-validity domain, `valid_until` is the
  conservative minimum of every accepted-token, policy, membership, evidence,
  model, admitted correlation, and lifecycle deadline needed by that admission
  state. A mixed-domain aggregate is either rejected as
  `IncompatibleMonotonicDomains` or each deadline is conservatively translated
  into the selected domain through a current engine-issued
  `AdmittedMonotonicDomainCorrelation`; its identity/generation, uncertainty
  bound, proof/condition/assessment/support/anchor generations, provider, and
  lifecycle become dependencies. Its independently checked source/target
  `CorrelationValidity` deadlines remain mandatory side conditions and are
  never translated through that same correlation. Mundilfari does not compare
  raw mixed-domain deadlines or silently discard a vector entry;
- every refresh result carries a fixed-size `PriorStateObservation` sampled for
  one explicit tagged `PriorStateSubject`—`BatchAdmissionState`,
  `ConsensusAuthority`, or
  `PublishedAuthoritySnapshot`—at the refresh linearization point, not caller
  receipt. A batch refresh always names the first; later milestones may wrap it
  with their own subject without reusing its identity. Its tagged
  `PriorStateDisposition::{Retained, Invalidated, Absent}` binds the prior
  state identity/generation when present, its exact-domain admission/authority
  validity, observed engine-state generation, and optional concurrent-
  publication generation. `Retained` additionally carries the unchanged prior
  domain/`valid_until`; `Invalidated` carries a
  fixed-size invalidation generation and typed reason; `Absent` carries the
  engine/publication generation in which absence was observed;
- every prior observation contains a fixed-size
  `LinearizationObservationStamp::{Measured, Unavailable}`. `Measured` binds
  the observation `MonotonicClockId`, a conservative
  `MonotonicReadInterval`, and one explicit
  `RefreshCoverageProfile::{LinearizationRefresh, CommitCoveredRefresh}`.
  Commit-covered evidence additionally binds the reviewed remaining-work bound
  and capability generation. `Unavailable` binds a typed reason plus attempted
  domain when known and observed engine/publication generations; it contains no
  fabricated instant or deadline;
- `LinearizationRefresh` is the portable default and requires no WCET. After
  callbacks/fallible work, the engine acquires a nonwrapping versioned
  transaction reservation, rechecks the complete generation vector, and
  samples the exact-domain `MonotonicReadInterval`; that provider observation
  point is the logical refresh linearization point. Readers encountering the
  reserved generation never observe an in-progress or mixed update: they
  boundedly retry or return typed `RefreshInProgress`, and cannot return the
  superseded state after the sample. Arbitrary preemption may follow. The
  immutable historically linearized record installs only if its exact
  reservation/version and invalidation watermark remain current; abandoned or
  superseded reservations are tombstoned and a delayed writer cannot overwrite
  a newer generation. Every later strict use independently revalidates all
  dependencies and `observed_at.latest < valid_until`. This profile grants no
  validity through physical commit, publication, completion, or caller return;
- reservation ownership is concrete: engine alone creates a non-forgeable
  `RefreshReservationGuard` binding reservation ID, owner operation, process/
  session/machine generations, captured `RefreshInvalidationWatermark`, and a
  nonwrapping `RefreshFencingGeneration`. Every dependency mutation capable of
  invalidating staged state—evidence/assessment/accepted-token, policy,
  membership, source, correlation/proof/model/anchor/validity, lifecycle,
  clock-domain/reset, publication, or configuration change—atomically advances
  the watermark before exposing that mutation;
- `RefreshReservationGuard` tombstones its reservation on explicit
  cancellation, unwind/panic where supported, normal early return, and `Drop`;
  the already-owned fixed reservation slot atomically transitions in place
  from `Live` to `Tombstone` and therefore requires no allocation, separate
  tombstone capacity, callback, blocking operation, fallible operation, or
  panic-capable cleanup. This bounded transition is valid during unwinding and
  `Drop` cannot return an error. If a higher fence already changed the slot to
  `SupersededTombstone`, cleanup is a successful fenced no-op. An impossible
  owner/fence/state transition atomically latches an engine invariant fault and
  permanently removes the old writer's install capability; it never panics or
  permits installation. No external callback or fallible/Pending-producing
  work is permitted after acquisition. A leaked/stalled live guard cannot be
  stolen because a timeout elapsed. Engine cancellation, owner/process/session
  invalidation, or an already published tombstone may authorize a new writer
  to atomically supersede it with a strictly higher fencing generation; the
  delayed old writer then returns typed `SupersededNoInstall`;
- process/session restart invalidates every inherited reservation before state
  use. `Vacant`/`Live`/`Tombstone`/`SupersededTombstone` share the same
  preallocated bounded slot; tombstones are reclaimed to `Vacant` only after
  the reader generation floor proves no observer can accept the old fence.
  Slot saturation may reject new acquisition but can never prevent guard
  cleanup. Fencing generations are never reused, and counter or reclamation
  exhaustion faults closed rather than risking ABA. Readers remain bounded:
  they return a current revalidated state, `RefreshInProgress`, or a typed
  fault and never wait for a leaked/stalled writer;
- `CommitCoveredRefresh` is optional. It uses the same reservation and sample,
  then expands the conservative latest edge by a current reviewed bound
  covering every remaining generation comparison, write, atomic swap,
  preemption/critical-section allowance, and observation-record write through
  physical commit. It commits only within that bound and before `valid_until`.
  Only this profile claims coverage through commit; it still grants no
  through-return authority;
- missing/stale remaining-work capability makes only
  `CommitCoveredRefresh` unavailable; ordinary hosted targets continue with
  `LinearizationRefresh`. Sampling failure, no comparable domain, reservation
  exhaustion, or inability to exclude mixed/in-progress reader state returns
  `Unavailable` and cannot report `Retained` or install a new admission/
  authority record. A known invalidation may still publish a diagnostic
  tombstone carrying the unavailable reason and exact invalidation generation;
- `Absent` uses `Measured` in the configured engine refresh domain when one is
  available; if no prior state/deadline domain and no configured refresh
  domain exists, it returns `Unavailable(NoAuthorityObservationDomain)` while
  still binding the observed engine/publication generations. Known invalidation
  may return `Invalidated` with an unavailable stamp and exact invalidation
  generation/reason, but sampling failure alone never permits `Retained`;
- `Retained` means only that the prior token revalidated with
  `Measured.cover.latest < valid_until` at that linearization point. It grants
  no authority through caller receipt, and any later use must perform the
  normal current-token/deadline/generation check. Cancellation,
  local result-capacity exhaustion, or transient work exhaustion leaves an
  older batch unchanged only if its exact policy/membership/evidence/
  lifecycle/deadline generations still revalidate; retention never extends its
  deadline or counts as a successful refresh. Evidence withdrawal, expiry,
  policy/membership generation change, source/lifecycle invalidation, or any
  other genuine dependency change invalidates affected prior authority through
  the normal generation graph even when the replacement aborts. An internal
  invariant failure faults the engine and reports prior authority invalidated,
  never retained;
- a failed refresh never replaces any prefix of current state. Committing a
  new complete batch and retiring the prior batch occur at one documented
  engine linearization point after both the new and prior generation vectors
  are rechecked; `PriorStateObservation.stamp` identifies which coverage
  profile applies. `v0.137.2` implements the
  corresponding concurrent publication transition and fills its publication
  subject/generation without changing these engine semantics;

Verification:

- admission/batch/consensus identity separation, same- and mixed-domain
  validity, retained/invalidated/absent observations, exact expiry and
  unavailable sampling, abort and genuine invalidation, unbounded post-sample
  preemption, every watermark dependency, in-place non-failing cleanup,
  supersession, restart, slot/fence/reclamation exhaustion, reader bounds, and
  `CommitCoveredRefresh` margin edges.

Exit criteria:

- batch admission remains non-authoritative, refresh failure cannot create or
  extend authority, and guard cleanup cannot fail or permit a stale install;
- `v0.60.5 implementation stop reached. Run pentest for this exact commit.`

### v0.60.6 - Policy-Accepted Hard Bounds And Lifecycle

Status: planned.

Goal: construct policy-accepted hard bounds from verified proofs and current
assessments, then invalidate every downstream consumer when support changes.

Deliverables:

- engine construction either recomputes a root/derived claim or verifies the
  complete bounded derivation with reviewed operation-specific rules and work
  limits; a condition assessment, caller-supplied digest, geometrically
  plausible interval, or previously verified different claim cannot justify
  narrower/substituted endpoints. Derivation inputs, proof rules, and model
  generations participate in lifecycle invalidation;
- assessment/admission uses one snapshot-consistent transaction: capture a
  bounded generation vector containing every condition, evidence, lifecycle,
  policy, membership, source, correlation, assessor/provider identity and
  generation, assessor-registry generation, proof-rule-registry generation,
  monotonic-domain generation, and verified-derivation dependency before
  evaluation; invoke assessors without engine locks; then atomically compare
  the complete vector immediately before issuance;
- a changed vector causes a bounded retry or an `Indeterminate` assessment,
  never a partial or mixed-generation result. The final
  `ConditionAssessment` and, only when derivation verification and policy
  permit it, optional `PolicyAcceptedHardBound<T>` are minted together at one
  documented engine linearization point; callback re-entry cannot observe or
  publish an in-progress assessment;
- the final issuance comparison resamples a `v0.16.0`
  `MonotonicReadInterval` in the assessment deadline's exact domain at that
  linearization point after evaluator/verification work, then compares its
  conservative `latest` edge including resolution, sampling latency, rate
  uncertainty, plus only a reviewed bound for internal work that remains before
  the issuance linearization point. It never claims coverage through caller
  receipt. If the required upper edge reaches `valid_until`, the engine emits
  expired/indeterminate diagnostics and never mints a current assessment or
  accepted token;
- opaque, non-forgeable `PolicyAcceptedHardBound<T>` is constructed only when
  a finite borrowed/owned `HardBoundClaimView<'_, T>`, its exact
  `VerifiedBoundDerivation<T>` and resolved condition, a snapshot-consistent
  current `Supported` assessment, and the selected engine policy all agree; it
  binds the interval/claim and
  verified-derivation identities/digests/generations, condition and assessment
  identity/generation, policy/membership/source/correlation generations,
  per-atom support basis, assurance/non-claims, evaluation domain, and
  conservative expiry/re-evaluation deadline;
- `PolicyAcceptedHardBound<T>` is likewise source-arena-independent. Hosted
  forms own their bounded state; no_std forms store bounded state inline or
  return the semantic `PolicyAcceptedHardBoundRef<'engine, T>` projection over
  `EngineProofHandle<'engine, PolicyAcceptedKind, T>` through that same checked
  branded, nonwrapping-generation engine store. This is not a second handle or
  storage abstraction. Completed promotion permits the
  unverified source arena/owner to drop without revoking the token, while every
  bound evidence/model/policy/source/lifecycle/assessment/deadline generation
  remains revalidated and can revoke it; failed or interrupted promotion mints
  neither verified proof nor accepted token;
- accepted-token identity/equivalence includes the exact conditional claim,
  verified-derivation identity and generation, condition/assessment identity
  and generation, policy/membership/source/correlation generations, and
  deadline; equal geometry, claim digest, or recipe digest alone cannot make
  tokens interchangeable or satisfy a cache lookup;
- policy may reject a `Supported` assessment because its assurance, evidence
  class, lifetime, fault scope, or non-claims are inadequate; no public
  constructor, deserializer, provider, or boolean can manufacture acceptance;
- assessment and accepted-bound revalidation consumes the generic
  `v0.15.1` upsert/withdraw/discontinuity lifecycle with reserved invalidation
  capacity; atom/evidence change, source loss, correlation reclassification,
  policy/membership reload, expiry, withdrawal, or monotonic-domain change
  rotates assessment generation and invalidates every dependent accepted token;
- downstream invalidation graph is explicit and bounded: consensus survivors/
  results, leap admission, servo and estimator inputs/accumulated state,
  holdover models, discipline proposals, `TrustedClock` publication, and
  synchronized status all reject stale accepted-bound generations before use;
- `v0.137.1` later linearizes assessment revalidation with concurrent
  publication; this milestone owns engine assessment/admission but no clock
  publication or discipline authority.

Verification:

- snapshot changes at every capture/evaluate/recheck/issue boundary, upper-edge
  expiry, callback re-entry, supported-but-policy-rejected inputs, forged/stale/
  cross-condition tokens, accepted-token cache non-substitution, source-arena
  independence, verification work crossing expiry, and proof that no mixed or
  partial assessment/token can issue; withdrawal propagates through consensus,
  leap, servo, estimator, holdover, proposal, publication, and synchronized
  status.

Exit criteria:

- only an opaque engine token binding the exact verified derivation, current
  assessment, policy, support, generations, and deadline can represent an
  accepted hard bound;
- `v0.60.6 implementation stop reached. Run pentest for this exact commit.`

### v0.60.7 - Engine Admission And Refresh Security Gate

Status: planned.

Goal: integrate and adversarially verify runtime assessment, proof ownership,
batch verification, correlation admission, policy acceptance, and refresh
transactions before clustering consumes them.

Deliverables:

- one bounded integration surface covering `v0.60.1` through `v0.60.6`,
  preserving every type-state, identity, dependency, resource, concurrency,
  and invalidation boundary without a convenience bypass.

Verification:

- unknown, contradicted, expired, withdrawn, and restored atoms; exhaustive
  `All`/`Any`/threshold/fault-rule evaluation with indeterminate members;
  all origin/integrity/authority/lineage axis combinations, mixed-basis
  composition, complete transitive leaf-basis preservation, and proof that
  `AtMostFaulty`/Byzantine-budget configured assumptions can never emerge as
  measured origin or disappear behind derived/cryptographic/authority labels;
- root and derived claim recomputation plus adversarial interval narrowing,
  supported-condition reuse with different endpoints, spliced input
  derivations, reordered/substituted input or observation digests, wrong
  rounding direction/policy, stale or substituted conversion-model/proof-rule
  generation, output-condition mismatch, and verification-work exhaustion;
- missing/dropped handle construction attempts, stale/evicted/foreign-store/
  cross-generation/cross-domain handles, stale lifetime brands, same-address
  arena recreation, near-generation exhaustion, geometry-only acceptance
  attempts, eviction/import during leased traversal, arena mutation during
  unlocked assessment work, proof that no arena lock/lease crosses external
  callbacks, imported-record partial reinterning, cross-thread profile
  enforcement, and DAG node/edge/work exhaustion;
- borrowed and owned claim inputs, source-arena drop after successful engine
  promotion, source drop before/during promotion, proof/token inspection after
  source drop, canonical-identity/generation dependency preservation, and
  proof that engine-owned results contain no source brand/handle/owner;
- shared-set roots verified in permutation, duplicate-root coalescing without
  token aliasing, canonical root/member ordering, one-root evidence failure
  independence, shared-node failure fan-out, one-snapshot generation capture,
  bounded batch work, complete-member witness enforcement, and batch-versus-
  individual proof/token identity equivalence;
- cancellation and global work exhaustion after every unique DAG node and
  member, generation change after every verified prefix, result/accounting
  capacity exhaustion, and internal-invariant abort injection prove global
  aborts mint no authoritative artifact, classify every member as
  `Indeterminate` or `Unprocessed`, return stable complete accounting, and
  cannot convert to `CompleteBatchVerification`; every root permutation
  produces the same canonical outcome. Compile-fail/type-state tests prove
  `AbortMemberDiagnostic`/`Unprocessed` cannot construct
  `CompleteMemberStatus`, `CompleteBatchVerification`, or a quorum input;
- for every admitted quorum/threshold rule, failures leave eligible
  contributors exactly one below, at, and one above the boundary; each failed,
  contradicted, expired, indeterminate, and withdrawn
  `CompleteMemberStatus` contributes no interval/vote yet remains in
  original-`n` accounting.
  Caller-side failure filtering, denominator reduction, threshold
  recomputation, and duplicate-root independence forgery fail, while each
  explicitly admitted duplicate/correlation policy is covered. `Unprocessed`
  appears only in separate aborted-outcome refusal tests, never this threshold
  matrix;
- refresh state machines inject cancellation, each capacity/work failure,
  internal-invariant failure, withdrawal, expiry, and every policy/membership/
  evidence/lifecycle generation change before and after each work/commit step.
  They prove exact
  `Retained`/`Invalidated`/`Absent` reporting, no retained-deadline extension,
  no partial replacement, invalidation despite replacement failure, and one
  linearization point for complete replacement plus prior retirement;
- admission-state tests prove `CompleteBatchVerification` alone has no
  authority identity, `BatchAdmissionState` cannot be confused with consensus
  or publication or enter servo/discipline/trusted-time APIs, and same-domain
  `AdmissionValidity.valid_until` is the
  minimum of all accepted-member and transitive policy/membership/evidence/
  model/lifecycle deadlines. Every dependency expires or withdraws in turn;
  mixed-domain inputs are rejected unless an
  `AdmittedMonotonicDomainCorrelation` translates them conservatively.
  Candidate/admitted confusion, platform/provider self-admission, registration
  without evidence, wrong direction, forged identity/narrow offset/rate/drift
  claim or capture anchor, missing/substituted derivation/condition/assessment/
  support basis, stale/expired/high-uncertainty candidates, assumption
  withdrawal, reset/suspend/rate/migration/provider withdrawal, anchor-based
  uncertainty growth, exact earliest-edge deadline translation, and attempted
  composition all fail closed. Endpoint validity tests independently sample
  both domains and reject self/indirect translation, circular supervision,
  either deadline expiry, and either domain reset. Numerical-proof cycle tests
  reject A→B supported by B→A, longer cycles, cycles introduced by replacement
  generations, and restored historical correlation references used as current
  recipe/condition/support inputs;
- prior-observation tests bind identity/generation, exact-domain
  `PriorStateSubject`, `LinearizationObservationStamp`, unchanged
  `valid_until`, invalidation generation/reason, and engine/publication
  generation to the same refresh boundary. Exact expiry, straddling reads,
  monotonic failure/domain mismatch, invalidation immediately after
  linearization, delayed synchronous return, and delayed async polling prove
  `Retained` is historical-at-its measured coverage, never authority through
  receipt;
- `LinearizationRefresh` schedules inject unbounded preemption after
  reservation, immediately after the logical sample, and before every physical
  install step. Readers never observe mixed/in-progress state, boundedly return
  `RefreshInProgress`, and later accept an installed historical record only
  after their own generation/deadline revalidation. A result may be expired on
  receipt without retroactively changing its measured disposition. Reservation
  abandonment/supersession, invalidation watermark changes, delayed-writer ABA,
  generation exhaustion, and newer-writer ordering cannot overwrite newer
  state. Every invalidating dependency class advances the watermark before
  visibility. State-machine tests cover in-place `Live` to `Tombstone`,
  already-superseded cleanup as a fenced no-op, impossible-transition engine-
  fault latching with no install, and cleanup under reservation-slot saturation;
  allocator/callback/panic/blocking instrumentation proves cleanup is bounded,
  allocation-free, callback-free, nonblocking, and non-panicking. Panic/unwind,
  explicit cancellation, guard drop/early return, future drop, leaked/stalled
  owner, engine cancellation, process/session
  restart, timeout-only steal attempts, higher-fence supersession,
  `SupersededNoInstall`, bounded tombstone reclamation, reader-generation
  floors, acquisition-capacity exhaustion, and bounded reader availability are
  covered;
- `CommitCoveredRefresh` injects preemption after the sample and each remaining
  generation comparison, write, swap, critical-section edge, and observation-
  record step. Tests hit one tick below/at/above the reviewed remaining-work
  bound and deadline; absent/stale/violated capability disables this profile
  while hosted `LinearizationRefresh` remains functional. Sample failure, no
  comparable domain, or broken reservation exclusion yields
  `LinearizationObservationStamp::Unavailable`, never retained or newly
  installed state. Prior absence with and without a configured refresh domain
  covers `Measured` and `Unavailable(NoAuthorityObservationDomain)`;
- provider replacement/withdrawal, assessor- or proof-rule-registry reload,
  policy reload, callback re-entry, and evidence/generation changes at every
  point between vector capture, unlocked evaluation, verification, final
  comparison, and issuance; bounded retry exhaustion returns `Indeterminate`
  and no mixed or partial assessment/token;
- coarse monotonic resolution, final reads straddling expiry, callbacks or
  verification work crossing expiry, latency spikes, rate uncertainty,
  completion-margin exhaustion, and exact `latest == valid_until` refusal;
- source and threshold lifecycle cases include
  source loss changing a threshold, correlation-group reclassification,
  calibration/oscillator/path-delay expiry, policy/membership/source/evidence
  reload, monotonic-domain change, and assessment deadline boundaries;
- forged/stale/cross-condition accepted tokens, supported-but-policy-rejected
  assurance, provider boolean/privileged-variant attempts, assessment-to-use
  and assessment-to-publication races, withdrawal under queue pressure,
  equal-geometry/equal-claim tokens with different verified-derivation or
  assessment generations and accepted-token cache non-substitution,
  servo/estimator/holdover/proposal invalidation, deterministic replay, and
  compile-fail private construction/deserialization tests.

Exit criteria:

- no canonical or mathematically conditional hard-bound claim view is labeled
  currently trusted without a verified exact derivation and fresh,
  snapshot-consistent engine-issued policy-accepted assessment whose support
  bases remain visible;
- no attacker-controlled root order or global abort can select an authoritative
  prefix, and no full-membership consumer accepts anything except the exact
  complete batch witness;
- failed members never vote or contribute intervals, never silently reduce the
  configured quorum, and an aborted refresh neither preserves invalid prior
  authority nor partially replaces still-current prior authority;
- `Unprocessed` is unrepresentable in a complete witness or quorum input, and
  prior-state disposition is an interval-valued linearization observation
  rather than a through-receipt authority claim;
- batch, consensus, and publication authority identities cannot substitute for
  one another; pre-consensus admission state has no time authority, aggregate
  deadlines are conservative in one domain, and no unavailable observation can
  retain or mint state;
- `v0.60.7 implementation stop reached. Run pentest for this exact commit.`

### v0.61.0 - Generic Clustering Combining And Diversity

Status: planned.

Goal: select and combine validated survivors under protocol-neutral engine
diversity policy.

Deliverables:

- engine-owned clustering, combining, preferred-source choice, and uncertainty
  output over generic observations, preserving the exact canonical condition
  and reviewed derivation report from `v0.60.0`;
- trusted survivor/combined hard-bound paths consume only current
  `v0.60.6` `PolicyAcceptedHardBound` values and propagate the accepted
  derivation identity, condition/assessment generation, and support-basis
  report; conditional claims remain available only through explicit diagnostic
  results;
- when inputs come from multi-root admission, an operation claiming the full
  configured membership consumes the matching `CompleteBatchVerification` and
  `BatchAdmissionState`, checks their exact identity/membership generation, and
  preserves every terminal failed member in
  membership accounting and the original `n`. Only members carrying current
  accepted bounds are eligible interval contributors; failed members cast no
  vote, cannot reduce the required threshold, and force `Insufficient` or
  `Unsafe` when too few eligible contributors remain. A successful prefix or
  aborted diagnostic outcome is never treated as the admitted set; the quorum
  API accepts `CompleteMemberStatus` through the witness and has no
  `AbortMemberDiagnostic`/`Unprocessed` input path;
- `BatchAdmissionState` has no time-claim endpoints or authority conversion.
  Only this consensus constructor selects proof support, applies the reviewed
  quorum/combining rule, derives the exact time claim, and may construct
  `ConsensusAuthority`;
- engine constructs a distinct `ConsensusAuthority<T>` with a non-substitutable
  `ConsensusAuthorityId`. Its bounded canonical `ProofSupportSet` contains
  exactly the accepted tokens and condition/derivation/correlation dependencies
  actually used by the selected quorum proof, while the complete witness
  separately preserves every configured member and original `n`. Unused
  eligible alternatives are not silently added to or substituted into an
  already-issued proof;
- every consensus authority has one explicit monotonic authority domain.
  Same-domain validity is the conservative minimum of every deadline in its
  exact proof-support set plus the policy, membership, evidence, model,
  correlation, and lifecycle dependencies required by the decision. Mixed
  domains fail as `IncompatibleMonotonicDomains` unless each deadline is
  conservatively translated through a current
  `AdmittedMonotonicDomainCorrelation`; each correlation identity/generation,
  verified offset/rate/drift derivations, canonical condition/assessment,
  transitive support bases, capture anchors, provider/lifecycle, and uncertainty
  then enter the proof-support set. The authority retains and independently
  checks both endpoint `CorrelationValidity` deadlines; neither is translated
  through the correlation itself. Raw cross-domain deadline comparison is
  forbidden. Consensus also rechecks the admission's no-transitive-correlation
  proof-support invariant; it cannot introduce correlation-backed claims or
  assessments into an existing correlation dependency after admission;
- expiry, withdrawal, replacement, or generation change of any used
  contributor or correlation invalidates that exact consensus authority even
  when unused members could form another quorum. Alternative support requires
  a new complete verification and consensus decision with a new identity and
  generation; implementations never mutate the old proof-support set in place;
- operator, network, path, geography, protocol, authority, and upstream
  correlation attributes;
- operator/upstream/ASN/path/grandmaster/receiver/oscillator/site diversity
  groups and a rule that weights never override the fault quorum;
- split-brain result;
- reusable bounded APIs that NTP and later cross-protocol consensus compose
  without either reimplementing the algorithms.

Verification:

- correlated hostnames, tie/order invariance, malicious majority, source loss,
  diversity thresholds, stale/lost assessment, conditional-claim rejection,
  complete batches with eligible contributors one below/at/above every
  threshold and each terminal failure status, aborted/prefix/filter outcome
  refusal including every `Unprocessed` position, original-`n` preservation,
  duplicate-root correlation policy, membership-generation substitution, and
  simulator campaigns;
- same-domain aggregate-minimum tests expire each required dependency in turn;
  mixed-domain tests cover rejection, conservative correlation translation,
  forged narrow correlation proof/anchor, correlation assumption/support/
  endpoint-validity expiry or withdrawal, generation change, circular
  validation, and prohibit raw numeric comparison. Exact-support tests
  distinguish used from unused eligible
  members and prove that loss of one used member invalidates the old authority
  even when an unused alternative quorum exists, requiring a new identity.

Exit criteria:

- multiple names are never assumed to be independent sources;
- `v0.61.0 implementation stop reached. Run pentest for this exact commit.`

### v0.61.1 - Leap Evidence Authority And Diversity Admission

Status: planned.

Goal: admit leap-model candidates through protocol-neutral engine authority,
correlation, diversity, and conflict policy after provenance/lifecycle and
generic quorum foundations exist.

Deliverables:

- engine policy consuming `v0.15.2` leap evidence and producing an admitted,
  rejected, pending, split, or insufficient decision for a validated
  `v0.12.1` candidate;
- explicit authority, authentication/integrity, freshness, lead-time,
  correlation, diversity/quorum, and minimum-evidence requirements;
  authentication alone never grants leap authority;
- source smear behavior remains evidence about presentation/transport;
  local smear-versus-step presentation policy never decides whether the
  underlying UTC model contains a leap;
- policy-defined treatment of authoritative pinned tables, authenticated
  announcements, corroborated evidence, unauthenticated hints, cancellations,
  withdrawals, and conflicting candidate hashes/generations;
- generic evidence adapters allow future NTP/PTP/radio/external sources
  without adding protocol types or duplicate quorum logic to core/engine;
- opaque, engine-constructed `AdmittedLeapCandidate` binds candidate
  identifier/hash, exact evidence set or digest, authority, policy and
  membership generations, evidence and decision generations, the exact
  `v0.7.2` canonical condition/`BoundAssumptionsId` and derivation report,
  current `v0.60.1` condition-assessment, `v0.60.3` verified-bound-derivation,
  and `v0.60.6` accepted-bound identities and generations, support-basis report,
  non-claims, expiry, and the expiry's full `MonotonicClockId`;
- the handoff exposes bounded activation revalidation but no raw constructor;
  no model installation or concurrent publication occurs here, and
  `v0.137.3` is the only default-clock consumer.

Verification:

- one authenticated malicious server, correlated aliases, diverse agreement,
  authoritative-table versus NTP/PTP/radio fixture conflict, false leap,
  late/withdrawn/cancelled evidence, source churn, smear/step disagreement,
  policy/membership reload, malicious majority, impossible quorum, and
  candidate/decision generation mismatch; compile tests prevent external
  `AdmittedLeapCandidate` construction or raw-candidate default publication;
  contradicted/indeterminate/expired/withdrawn conditions and stale accepted-
  bound tokens invalidate leap admission before use.

Exit criteria:

- no single protocol packet or authenticated endpoint can admit a leap outside
  explicit authority and diversity policy, and no duplicate selection
  algorithm exists outside the engine;
- `v0.61.1 implementation stop reached. Run pentest for this exact commit.`

### v0.62.0 - Poll Control And Full NTP Client

Status: planned.

Goal: integrate complete NTPv4 client operation.

Deliverables:

- NTP source lifecycle, burst, poll adaptation, reachability, and normalized
  NTP observation/filter metadata;
- facade/application composition of NTP associations through the
  `v0.60.0`–`v0.61.0` engine primitives, producing the combined reading
  without a protocol-to-engine dependency edge;
- random source ports/identifiers through supplied entropy;
- bounded multi-source orchestration.

Verification:

- long simulator runs, chrony/ntpd/ntpsec interoperability, restart, KoD,
  rate changes, source churn, entropy failure, and packet loss.

Exit criteria:

- the complete client can produce a validated reading without discipline;
- `v0.62.0 implementation stop reached. Run pentest for this exact commit.`

### v0.63.0 - Full NTP Server

Status: planned.

Goal: deliver secure bounded NTPv4 server operation.

Deliverables:

- client/server mode, reference state, KoD, rate/work limits, and quality;
- amplification, replay, malformed, and expensive-extension protections;
- authenticated control excluded until its milestone.

Verification:

- multiple independent clients, reflection/flood tests, source transitions,
  malformed corpus, interleaved compatibility, and long soak.

Exit criteria:

- server operation is interoperable and fail-closed under resource pressure;
- `v0.63.0 implementation stop reached. Run pentest for this exact commit.`

### v0.64.0 - NTP Legacy Modes

Status: planned.

Goal: implement symmetric, broadcast, multicast, and NTPv0-v3 compatibility.

Deliverables:

- exact revision state machines and separate insecure feature gates;
- association loop/duplicate protection;
- explicit trust and deployment warnings.

Verification:

- historical implementation interop, mode-confusion, loop, replay, broadcast
  spoof, state mutation, and downgrade tests.

Exit criteria:

- legacy modes are never enabled by secure defaults;
- `v0.64.0 implementation stop reached. Run pentest for this exact commit.`

### v0.65.0 - KoD Port Randomization And Interleaved Modes

Status: planned.

Goal: implement incorporated operational/security NTP updates.

Deliverables:

- complete KoD policy, RFC 9109 source-port behavior, and RFC 9769 interleaved
  operation;
- request identity and transmit timestamp history;
- resource/rate interactions.

Verification:

- update RFC vectors, interleaved reorder/loss, port entropy failure, replay,
  spoof, KoD abuse, and interoperability.

Exit criteria:

- NTPv4 behavior reflects current incorporated updates, not RFC 5905 alone;
- `v0.65.0 implementation stop reached. Run pentest for this exact commit.`

### v0.66.0 - Mode 6 And Management

Status: planned.

Goal: implement bounded NTP control and management mappings.

Deliverables:

- RFC 9327 mode 6 codec/state, RFC 5907 MIB, and RFC 9249 YANG mappings;
- authentication/authorization boundary and remote-disabled default;
- response fragmentation and work limits.

Verification:

- official/reference vectors, unauthenticated mutation refusal, fragment
  reorder/duplication, amplification, and management interop.

Exit criteria:

- control traffic cannot change server state without explicit authority;
- `v0.66.0 implementation stop reached. Run pentest for this exact commit.`

### v0.67.0 - Autokey Inspection

Status: planned.

Goal: support safe forensic/historical Autokey parsing.

Deliverables:

- documented packet/extension forms and validation evidence;
- no trust or signing implementation claim beyond accessible specification;
- historical-only API and warnings.

Verification:

- archived captures/vectors, malformed crypto fields, resource limits, replay,
  and forensic non-authority tests.

Exit criteria:

- Autokey compatibility cannot masquerade as modern secure time;
- `v0.67.0 implementation stop reached. Run pentest for this exact commit.`

### v0.68.0 - Khronos Watchdog

Status: planned.

Goal: implement RFC 9523 secure client selection watchdog behavior.

Deliverables:

- random subset policy, rounds, thresholds, fallback/alert state, and evidence;
- integration without replacing normal NTP selection;
- bounded query and source diversity budgets.

Verification:

- RFC scenarios, time-shifting adversaries, partial compromise, entropy
  failure, correlated sources, network partitions, and long simulation.

Exit criteria:

- Khronos can detect/limit attacks without silently weakening normal policy;
- `v0.68.0 implementation stop reached. Run pentest for this exact commit.`

### v0.69.0 - NTP Discovery

Status: planned.

Goal: implement DHCPv4/DHCPv6 and configured pool discovery.

Deliverables:

- exact option codecs, source provenance, deduplication, lifetime, and policy;
- resolver and pool expansion boundaries;
- discovered endpoints remain untrusted until protocol authentication.

Verification:

- RFC options, malformed DHCP, duplicate/correlated endpoints, rebinding,
  expiry, network changes, and resolver fault tests.

Exit criteria:

- discovery never grants identity or clock authority;
- `v0.69.0 implementation stop reached. Run pentest for this exact commit.`

### v0.70.0 - Experimental NTPv5

Status: planned.

Goal: implement the exact pinned NTPv5 draft experimentally.

Deliverables:

- `draft-ietf-ntp-ntpv5-09` exact source hash, with a final-RFC/new-revision
  migration check immediately before implementation;
- revision-named codecs/state, feature gates, and wire identity;
- client/server scope only where the exact draft defines it;
- no stable type leakage or automatic negotiation.

Verification:

- draft vectors, revision mismatch, unknown fields, migration fixtures,
  malformed corpus, and available draft implementation interop.

Exit criteria:

- NTPv5 remains revision-isolated and cannot change stable NTP semantics;
- `v0.70.0 implementation stop reached. Run pentest for this exact commit.`

### v0.71.0 - NTP Family Security Gate

Status: planned.

Goal: complete NTP-family conformance, interoperability, and security review.

Deliverables:

- RFC/update/errata clause maps and protocol capability matrix;
- differential simulator and implementation report;
- proof that NTP association/filter code emits normalized observations while
  interval quorum, falseticker rejection, clustering, combining, and
  correlation-aware diversity exist only in `mundilfari-engine`;
- conservative delay/asymmetry policy with maximum root distance/RTT,
  interval expansion, minimum-delay history labeled as an assumption, and no
  NTS-to-NTP fallback;
- resolved critical/high parser, state, selection, server, and downgrade issues.

Verification:

- official vectors, chrony/ntpd/ntpsec matrix, fuzz/soak/Byzantine campaigns,
  host/no_std/MSRV matrix, and focused pentest.

Exit criteria:

- unauthenticated NTP is feature-complete but never mislabeled secure, and NTS
  authentication is never claimed to remove delay attacks;
- `v0.71.0 implementation stop reached. Run pentest for this exact commit.`

## Phase 6: NTS Roughtime And Secure Bootstrap

### v0.72.0 - Production Crypto TLS And Dependency Admission

Status: planned.

Goal: admit production implementations for the already frozen generic crypto
contracts and the TLS/X.509 boundary needed by secure time.

Deliverables:

- current Rustls, production crypto-provider, MAC, AEAD, digest, entropy,
  secret-container, certificate, and X.509 reviews;
- production `SecretMemoryProtection` capability mapping for redaction,
  zeroization, page locking, core-dump exclusion, hardware/non-exportable, and
  externally held keys, with unsupported protections explicit non-claims;
- exact feature/transitive/native/MSRV/license inventories;
- conformance to the `v0.24.1` provider traits without widening them or
  exposing time-protocol semantics;
- sealed audited production constructors or explicit provider-assurance
  provenance that discipline policy may reject;
- TLS/Rustls/certificate admission remains here and cannot be inferred from
  the earlier generic provider contract.

Verification:

- cargo-deny/audit/SBOM, feature-power-set checks, forbidden dependency
  leakage, provider failure mocks, and public type audit.

Exit criteria:

- generic dependencies are replaceable and time logic remains first-party;
- `v0.72.0 implementation stop reached. Run pentest for this exact commit.`

### v0.73.0 - NTS-KE Record Codec

Status: planned.

Goal: implement complete RFC 8915 NTS-KE records.

Deliverables:

- critical bit, record types, lengths, protocol/AEAD negotiation, endpoint,
  cookies, warnings, errors, and end record;
- unknown critical rejection and unknown noncritical preservation;
- borrowed and bounded owned forms.

Verification:

- RFC vectors, duplicate/order rules, every truncation, length overflow,
  critical unknowns, malformed negotiation, and round trips.

Exit criteria:

- NTS-KE wire behavior is independent of any TLS implementation;
- `v0.73.0 implementation stop reached. Run pentest for this exact commit.`

### v0.74.0 - NTS-KE State And Exporter Context

Status: planned.

Goal: implement TLS-neutral NTS key establishment state.

Deliverables:

- ALPN `ntske/1` verification, TLS 1.3 minimum, request/response state;
- TLS 1.3 early data/0-RTT forbidden for NTS-KE;
- exact exporter label/context and directional key derivation requests;
- session-resumption, ticket, exporter-context, connection, and process
  generation lifecycle through the generic `v0.23.1` process/machine events,
  with no key reuse across an invalid generation;
- TLS-neutral state keeps ticket, connection, exporter, and NTS association
  identities distinct; the concrete typed hierarchy and resumption transition
  are completed at `v0.75.2`–`v0.75.3`;
- endpoint, algorithm, cookie, shutdown, transcript, and TLS-channel evidence
  policy without an arbitrary authenticated boolean.

Verification:

- RFC transcript cases, wrong/missing ALPN, TLS downgrade, rejected 0-RTT,
  resumed sessions, ticket/exporter/process generation changes, exporter
  context bytes, partial records, duplicate negotiation, and mock failures.

Exit criteria:

- the state machine cannot accept an unauthenticated or wrong-protocol session;
- `v0.74.0 implementation stop reached. Run pentest for this exact commit.`

### v0.75.0 - Rustls NTS-KE Adapter

Status: planned.

Goal: integrate reviewed Rustls TLS 1.3 for NTS-KE.

Deliverables:

- client/server adapter behind `std` and `rustls` features;
- application-provided crypto provider and trust configuration;
- secret-memory/provider capability report propagated without upgrading
  Rustls or platform guarantees;
- RFC 9325 deployment policy and RFC 9525 service-identity verification;
- explicit certificate-revocation capability report and deployment non-claim
  where the selected provider/configuration supplies no live revocation;
- typed interval-valued certificate outcome `TemporalValidity`:
  `DefinitelyValid` only when the entire trusted time interval lies within
  the admitted whole-chain certificate-validity intersection and every
  supported revocation-freshness constraint, `DefinitelyInvalid` when it is
  disjoint on an invalid side, and `Indeterminate` for partial overlap or
  insufficient time/revocation evidence;
- all certificate, CRL/OCSP, and trusted-time boundaries use the exact
  open/closed/half-open `v0.7.1` semantics; `notAfter`, `nextUpdate`, and
  equivalent endpoints are never emulated by subtracting a quantum;
- strict mode accepts only `DefinitelyValid`; no midpoint, preferred estimate,
  or monotonic projection substitutes for the trusted interval;
- concrete bounded `CredentialVerifier` contract returns immutable
  whole-chain `TemporalValidationEvidence`: exact trusted interval used,
  validation instant, chain and supported revocation evidence digests,
  per-member outcomes, capability/non-claims, validity horizon, and optional
  revalidation deadline with its full `MonotonicClockId`;
- a conventional verifier accepting one scalar `UnixTime` cannot by itself
  produce `DefinitelyValid` or satisfy the strict `CredentialVerifier`
  contract; adapters must preserve whole-interval and whole-chain evidence;
- certificate-time bootstrap policy without disabling validity checks.

Verification:

- Rustls interop, wrong identity, expired/not-yet-valid/revoked-policy chain,
  unavailable revocation, trust anchor, ALPN, TLS version, resumption, rejected
  early data, wholly-valid/disjoint/partial-overlap time intervals, boundary
  precision and every open/closed combination, absent preferred estimate,
  scalar-`UnixTime` midpoint rejection, incomplete chain/revocation evidence,
  close, fragmentation, and provider matrix tests.

Exit criteria:

- Rustls supplies TLS only; all NTS behavior remains Mundilfari-owned;
- `v0.75.0 implementation stop reached. Run pentest for this exact commit.`

### v0.75.1 - Service Credential Context And Retention Horizon

Status: planned.

Goal: bind retained TLS/NTS security state to stable credential policy and
immutable temporal evidence without rotating identity on normal clock
refinement.

Deliverables:

- typed `CredentialPolicyGeneration` covering trust-anchor set,
  service-identity policy, certificate-validation policy, provider/algorithm
  configuration, and revocation policy;
- immutable `TemporalValidationEvidence` from `v0.75.0` carries the exact
  interval used for validation, validation instant, whole-chain/revocation
  evidence digest and outcomes, capability/non-claims, validity horizon, and
  revalidation deadline;
- stable `ServiceCredentialContextId` binds the concrete verified reference
  identity, endpoint authority, SNI where applicable, ALPN policy,
  credential-policy generation, presented-chain and temporal/revocation
  evidence identity/digest, service-level conservative horizon, relevant
  conversion/leap-model generation, and process/machine generation, never a
  resumption credential, TLS connection, exporter, NTS association, or
  continuously refined live clock interval;
- the service-context horizon covers only the certificate chain, supported
  revocation evidence/freshness, reference identity, configured trust/policy,
  relevant time-model validity, and lifecycle validity; ticket/PSK,
  connection, exporter/key-usage, association, and cookie horizons belong to
  their later typed layers;
- each context change has an explicit action:
  `InvalidateImmediately`, `RevalidateBeforeUse`, or policy-bounded
  `ContinueUntil`, with strict defaults for trust removal, revocation,
  identity-policy tightening, time-model rollback, or definite expiry;
- service-context `ContinueUntil` never exceeds the earliest conservative
  certificate-chain, revocation-freshness, reference-identity, trust/policy,
  time-model, lifecycle, or other service-level security horizon;
- civil horizons convert to a monotonic revalidation deadline using the
  worst-case upper trusted-time bound, correlation uncertainty, conservative
  oscillator/holdover growth, and exact suspend semantics; holdover growth may
  move the effective deadline earlier;
- inability to establish or maintain a conservative monotonic deadline
  requires revalidation before every use or rejection; clock discontinuity,
  correlation loss, suspend-domain mismatch, or `MonotonicClockId`
  invalidation cancels the deadline;
- ordinary clock refinement within the same admitted time/model generation
  does not rotate the context; definite expiry, trust removal, confirmed
  revocation, rollback, execution-generation change, or relevant time-model
  discontinuity does;
- `TemporalValidity` evaluates the whole validated chain and all supported
  time-bearing revocation evidence, including CRL/OCSP `thisUpdate`,
  `nextUpdate`, produced/validity times, and freshness policy;
- partial overlap anywhere in the chain/revocation intervals is
  `Indeterminate`; strict mode requires every admitted interval wholly valid;
- revocation checking remains a reported capability/non-claim when the
  provider/configuration cannot supply it.

Verification:

- trust-root add/remove/rotation, service-identity policy change, validation-
  policy tightening/loosening, revocation configuration change and newly
  received revocation, CRL/OCSP before/inside/partial/expired/future intervals,
  chain member expiry, service context change before later resumption,
  certificate expiry during retained-state use, time/leap-model rollback/
  replacement, process/
  machine generation change, repeated normal clock refinements without
  context churn, reference identity/endpoint/SNI/ALPN/chain substitution,
  every competing chain/revocation/identity/trust/policy/time-model/lifecycle
  horizon and proof that ticket/connection/exporter/association limits do not
  alter service-context identity,
  upper-bound/correlation/oscillator/holdover/suspend deadline calculations,
  earlier deadline movement, missing conservative deadline, discontinuity,
  revalidation-horizon expiry, and every invalidation/revalidation/continued-
  use action.

Exit criteria:

- no service credential context outlives, changes identity from, or bypasses
  the service-level policy and temporal/revocation evidence that authorized it;
- `v0.75.1 implementation stop reached. Run pentest for this exact commit.`

### v0.75.2 - TLS Resumption Credential Generation

Status: planned.

Goal: model every TLS 1.3 resumption ticket/PSK as a bounded cryptographic
credential between its originating service context and a resumed connection.

Deliverables:

- opaque `ResumptionCredentialGeneration` binds exactly one
  `ServiceCredentialContextId`, opaque provider-held PSK/ticket handle and
  provider generation, TLS version and cipher-suite/hash compatibility, ticket
  nonce/identity, and server ticket-key generation where the provider exposes
  it; Mundilfari never requires exporting provider-held secret bytes;
- issuance, monotonic age basis, use count, expiry, single-use/replay policy,
  endpoint/SNI/ALPN constraints, process/machine generation, and server/client
  role are carried as credential state rather than service-context or
  connection state;
- secret-memory and persistence capabilities remain independent explicit
  claims for the opaque handle, ticket bytes, provider state, and any stored
  metadata; persistence never implies rollback protection, non-exportability,
  page locking, or secure deletion;
- the resumption-credential horizon is the earliest still-valid service
  context horizon plus ticket/PSK age, usage, expiry, provider generation,
  ticket-key generation, replay, lifecycle, and persistence constraints; it
  includes no future connection, exporter, key-usage, association, or cookie
  lifetime;
- creation and every attempted use revalidate all bound fields and the
  originating service context. If the TLS/provider adapter cannot expose or
  enforce a policy-required identity, generation, compatibility, replay,
  lifetime, or secret/persistence binding, resumption is disabled rather than
  reported as fully verified;
- private constructors and one-way state transitions prevent caller-forged
  credentials, service/role/provider substitution, use after consumption or
  expiry, and conversion of an opaque ticket into reusable connection/exporter
  authority.

Verification:

- full-handshake ticket issuance, opaque provider handles, wrong service/
  endpoint/SNI/ALPN/role/provider/TLS/cipher-suite/hash/ticket-key generation,
  nonce/identity collision, stale/rotated provider, age/usage/expiry/replay,
  process/machine restore, persistence rollback, unavailable secret-memory
  capability, adapter omission of each required binding, strict resumption
  disablement, and compile-fail construction/substitution tests;
- horizon tests prove the result is the earliest service-plus-credential
  limit, never includes later exporter/association objects, and moves earlier
  or invalidates when any constituent becomes unsafe.

Exit criteria:

- no resumed handshake can treat an opaque ticket/PSK as an unmodeled copy of
  service authorization or as reusable connection/exporter authority;
- `v0.75.2 implementation stop reached. Run pentest for this exact commit.`

### v0.75.3 - TLS Connection Exporter And NTS Association Generations

Status: planned.

Goal: separate reusable service/resumption-credential authorization from
per-handshake, per-exporter, and per-NTS-association lifetimes.

Deliverables:

- `TlsConnectionGeneration` is fresh for every full or resumed handshake and
  binds `ServiceCredentialContextId` directly for a full handshake or both it
  and the consumed `ResumptionCredentialGeneration` for a resumed handshake,
  plus transcript digest, negotiated TLS/cipher suite/ALPN, endpoint/SNI,
  connection state, peer-evidence disposition, process/machine generation,
  and an explicit connection-lifetime horizon;
- `ExporterGeneration` is unique to and cannot outlive one
  `TlsConnectionGeneration`; exporter material, direction, label/context, and
  key-usage accounting never cross connections, and its horizon is the earlier
  of connection lifetime and exporter/key-usage limits;
- `NtsAssociationGeneration` derives from exactly one exporter generation and
  binds the negotiated NTS algorithms, endpoints, directional key identities,
  cookies, and association lifecycle, with a horizon no later than its exporter
  plus association/cookie policy;
- resumption first revalidates and consumes the `v0.75.2` credential, including
  its service context, ticket/PSK identity, endpoint/SNI/ALPN policy,
  compatibility, age/usage/replay, provider/ticket-key/trust-policy
  generations, temporal/revocation horizon, and lifecycle generation; it then
  creates a fresh connection, exporter, and NTS association generation in that
  order;
- TLS 1.3 resumption without a resent certificate chain uses the retained
  immutable service-context evidence only under its conservative horizon and
  revalidation policy; absence of a new chain never becomes fresh evidence;
- private constructors and type relationships prevent tickets from carrying
  exporter material, exporters from crossing connections, associations from
  changing exporters, or cookies from losing their service/association
  bindings.

Verification:

- full versus resumed handshake generation trees, ticket from wrong service/
  identity/endpoint/SNI/ALPN/policy/horizon/lifecycle, absent certificate on
  resumption, stale/removed trust or revocation update, missing or substituted
  `ResumptionCredentialGeneration`, replayed ticket,
  connection generation reuse, old exporter reuse after resumption, exporter
  label/context/direction mismatch, association/cookie rebinding, each layered
  horizon expiring before/after its parent, process/machine restore,
  exhaustion/rekey, and compile-fail cross-generation substitution/
  construction tests.

Exit criteria:

- every handshake creates fresh connection/exporter/association generations,
  while a typed resumption credential authorizes only one policy-permitted
  transition from its bounded service context;
- `v0.75.3 implementation stop reached. Run pentest for this exact commit.`

### v0.76.0 - NTS AEAD And Extension Protection

Status: planned.

Goal: implement NTS-protected NTP extension construction.

Deliverables:

- provider-backed mandatory AES-SIV-CMAC-256;
- unique identifier, cookie, placeholders, authenticator/encrypted extension;
- associated data, nonce, padding, directional key, and NAK policy;
- per-direction/key-generation operation and byte limits with atomic
  accounting, exhaustion-before-use checks, and fail-closed rekey;
- entropy/nonce/provider failure is terminal for the attempted construction
  and never falls back to reuse or a weaker algorithm;
- request/response sizing through placeholders and bounded amplification/work
  accounting before encryption or allocation.

Verification:

- RFC and AEAD vectors, tamper at every region, nonce/padding boundaries,
  wrong direction/key, unknown encrypted fields, operation/byte limit races,
  exact exhaustion, entropy/nonce failure, failed rekey, and constant-time
  failure review.

Exit criteria:

- generic AEAD code never decides NTS field meaning or ordering;
- `v0.76.0 implementation stop reached. Run pentest for this exact commit.`

### v0.77.0 - NTS Client And Cookie Jar

Status: planned.

Goal: deliver a complete bounded NTS client.

Deliverables:

- NTS-KE plus protected NTP orchestration;
- fixed-capacity cookie jar, generation, endpoint, local discard policy, use,
  replenish, `ServiceCredentialContextId`,
  `ResumptionCredentialGeneration` where applicable, and
  `NtsAssociationGeneration`;
- local discard deadline/policy age clearly distinguished from any
  authenticated server expiration supplied by a future protocol revision;
- non-`Copy`, redacted-debug, non-automatic-serialization secret types;
- prohibition on logging unique identifiers, cookies, exporter material, or
  stable client correlators;
- generic `v0.23.1` fork/checkpoint/restore-generation-aware entropy and
  request identity;
- one-use/replenishment, replay/failure/rekey state, common secure persistence
  with capability-qualified rollback evidence, atomic per-key exhaustion,
  fail-closed rekey, key-rotation overlap, and best-effort clearing boundary
  without overstated guarantees;
- service-context invalidation/revalidation propagates to tickets and retained
  cookie state; connection/exporter/association generation invalidation follows
  the `v0.75.2`–`v0.75.3` hierarchy before further use.

Verification:

- public server interop, cookie exhaustion/reuse prevention, local age expiry,
  replay, server restart, key rotation, endpoint migration, process fork,
  VM/container restore, service-context rotation/revocation/time rollback,
  ticket resumption with fresh connection/exporter/association generations,
  cross-generation rejection, log-capture redaction, tamper, and long
  simulation.

Exit criteria:

- an authenticated observation retains separate delay/accuracy uncertainty;
- `v0.77.0 implementation stop reached. Run pentest for this exact commit.`

### v0.78.0 - NTS Server

Status: planned.

Goal: deliver NTS-KE and protected NTP server operation.

Deliverables:

- cookie construction/key rotation, stateless validation where applicable;
- cluster/server cookie-key provider with explicit key IDs, generation,
  distribution boundary, per-key operation/byte limits, atomic exhaustion,
  overlap, fail-closed rekey, compromise recovery, and rollback refusal
  qualified by the selected persistence capability;
- cookie plaintext/privacy/unlinkability review and minimum correlator policy;
- bounded expensive-work admission and rate limits;
- rekey overlap, NAK, algorithm, endpoint, and certificate policy.

Verification:

- independent client interop, placeholder response sizing, flood/amplification,
  invalid-cookie CPU budget, cluster key distribution, key rollback/compromise,
  rotation/restart, certificate rotation, privacy/linkability, replay, and
  malformed records.

Exit criteria:

- unauthenticated traffic cannot force unbounded crypto or response work;
- `v0.78.0 implementation stop reached. Run pentest for this exact commit.`

### v0.78.1 - Experimental NTS Pool Key Establishment

Status: planned.

Goal: implement the exact pinned NTS pool key-establishment draft without
changing stable RFC 8915 endpoint semantics.

Deliverables:

- `draft-ietf-ntp-nts-keyexchange-pool-01` exact source hash and
  final-RFC/new-revision migration check immediately before implementation;
- revision-named records, endpoint selection, identity, retry, and failure
  policy behind an experimental feature;
- preservation of pool provenance and separation of discovery, TLS service
  identity, negotiated NTS server identity, cookies, and clock authority;
- bounded fan-out, retry, DNS, connection, and expensive-work budgets with no
  unauthenticated downgrade to ordinary NTP.

Verification:

- exact draft examples, revision mismatch, pool/member churn, malicious DNS,
  wrong certificate/service identity, redirect/confusion, replay, exhaustion,
  malformed records, bounded retry, and available implementation interop.

Exit criteria:

- pool key establishment remains revision-pinned and cannot silently alter
  stable NTS trust or endpoint policy;
- `v0.78.1 implementation stop reached. Run pentest for this exact commit.`

### v0.79.0 - Roughtime Client And Verifier

Status: planned.

Goal: implement client, response verification, and chain evidence for the
exact pinned Roughtime revision.

Deliverables:

- `draft-ietf-ntp-roughtime-19` exact source hash and final-RFC migration
  check immediately before implementation;
- request/response codecs, nonce linkage, Merkle path, delegation, signature,
  midpoint/radius interval, and chain evidence;
- provider-backed signature verification and pinned server identities;
- revision-specific experimental namespace until finalized.

Verification:

- official/reference vectors, tag/length/duplicate errors, nonce mismatch,
  Merkle/signature/delegation failure, radius bounds, chain inconsistency,
  replay, and independent server interop.

Exit criteria:

- Roughtime yields authenticated intervals and never steps a clock directly;
- `v0.79.0 implementation stop reached. Run pentest for this exact commit.`

### v0.79.1 - Bounded Roughtime Server

Status: planned.

Goal: complete the pinned Roughtime revision with explicit bounded server
behavior rather than treating a codec as server completeness.

Deliverables:

- request admission, nonce batching/tree construction, response construction,
  delegation/signing keys, validity, and generation;
- online/offline signing boundary, delegation rotation, overlap, rollback,
  compromise, and restart policy;
- per-source/global rate and work limits, response-size/amplification budget,
  malformed-request no-response policy, and entropy failure handling;
- revision-specific experimental server API and audit events.

Verification:

- independent client interop, official/reference vectors, malformed/flooded
  requests, nonce batching, key/delegation rotation, rollback/compromise,
  restart, entropy failure, amplification ratio, and long server simulation.

Exit criteria:

- the Roughtime server is explicitly implemented, bounded, and separately
  reviewable from client verification;
- `v0.79.1 implementation stop reached. Run pentest for this exact commit.`

### v0.80.0 - Secure Time Bootstrap

Status: planned.

Goal: resolve certificate validation when civil time is initially untrusted.

Deliverables:

- pinned Roughtime/NTS key, provisioned interval, hardware clock, persisted
  interval through the common secure persistence boundary plus monotonic
  elapsed, and SPKI-pin policies;
- state transitions from unknown to rough to certificate-validatable time,
  with `TemporalValidity` propagated rather than collapsed to a boolean;
- strict certificate validation requires the complete trusted interval inside
  the whole-chain temporal intersection and all supported revocation-freshness
  constraints; partial overlap remains `Indeterminate`, exact endpoint
  inclusion follows `v0.7.1`, and no midpoint/preferred estimate is substituted;
- persisted monotonic elapsed is admissible only when the
  `MonotonicClockId`, process/machine generation, and suspend semantics prove
  the elapsed interval remained meaningful; otherwise the anchor is rejected
  or uncertainty grows from separately admitted evidence;
- rollback/restart/expiry and uncertainty growth.

Verification:

- no clock, wildly wrong clock, stale snapshot, restart, rollback, key
  mismatch, interval wholly inside/outside/partially overlapping the whole-
  chain temporal intersection and revocation-freshness constraints, every
  open/closed validity boundary, missing preferred estimate, mismatched
  monotonic domain, suspend/restore/fork, and recovery simulations.

Exit criteria:

- bootstrap never silently disables certificate validity or identity checks;
- `v0.80.0 implementation stop reached. Run pentest for this exact commit.`

### v0.81.0 - Secure Time Security Gate

Status: planned.

Goal: audit dependency, NTS, Roughtime, cookie, and bootstrap boundaries.

Deliverables:

- complete RFC/draft clause maps and dependency admission reports;
- NTS early-data, resumption-credential/provider/ticket-key and exporter
  generation, cookie
  privacy/unlinkability, logging, cluster-key rollback/compromise, certificate
  revocation capability, interval-valued temporal validity, and generic
  process/machine lifecycle-generation audit;
- service credential context binding across trust anchors, identity policy,
  chain/revocation intervals, conservative horizon, and trusted-time/leap-model
  generations, plus distinct resumption credential, TLS connection, exporter,
  NTS association, and cookie generation lifetimes and layer-owned horizons;
- provider assurance and secret lifecycle/redaction/rollback/clearing review;
- fixed-capacity codec, machine, AEAD provider, cookie jar, and Rustls adapter
  boundary audit;
- resolved critical/high TLS, AEAD, replay, downgrade, and bootstrap findings.

Verification:

- independent interop, fuzzing, malformed TLS/application records, long
  rotation/restart simulations, full/resumed generation-tree and chainless-
  resumption campaigns, unavailable provider bindings with resumption disabled,
  old-exporter/cross-association reuse attempts, cargo evidence, and focused
  pentest.

Exit criteria:

- secure network time is approved without false accuracy claims;
- `v0.81.0 implementation stop reached. Run pentest for this exact commit.`

## Phase 7: Physical Timecodes And Generic External Sources

### v0.82.0 - Generic External Satellite Observation Contract

Status: planned.

Goal: accept non-Navheim validated satellite-time providers without claiming
GNSS decoding conformance.

Deliverables:

- protocol-neutral source builder for appliances, vendor SDKs, embedded
  receivers, and recorded laboratory observations;
- mandatory scale, uncertainty, capture, freshness, health, integrity,
  authentication, and provenance policy;
- mandatory observation identity, source generation/sequence, `valid_until`,
  and generic upsert/withdraw/discontinuity events from `v0.15.1`;
- explicit provider and conformance non-claims.

Verification:

- missing/contradictory evidence, stale provider, unknown scale, malicious
  uncertainty, source replacement, retroactive withdrawal, discontinuity,
  saturated event queue, and custom no_std provider fixtures.

Exit criteria:

- Navheim is preferred for full GNSS interpretation but not mandatory for
  already validated generic observations;
- `v0.82.0 implementation stop reached. Run pentest for this exact commit.`

### v0.83.0 - TWSTFT

Status: planned.

Goal: implement two-way communication-satellite time and frequency transfer
as a non-GNSS Mundilfari protocol.

Deliverables:

- legitimately available TWSTFT records, sessions, station/equipment/path
  identities, calibration, delay, and uncertainty provenance;
- explicit separation from Navheim GNSS common-view/all-in-view evidence;
- bounded file/stream and state behavior.

Verification:

- official/laboratory files, malformed records, path and calibration changes,
  day rollover, asymmetric delay, replay, and reference-tool comparison.

Exit criteria:

- communication-satellite transfer is supported without importing GNSS
  navigation semantics;
- `v0.83.0 implementation stop reached. Run pentest for this exact commit.`

### v0.84.0 - IRIG

Status: planned.

Goal: implement the complete selected licensed IRIG revision.

Deliverables:

- all assigned code rates/modulations/control functions, frame sync, BCD,
  quality, year, leap, and straight-binary seconds;
- edge/sample decoder and encoder;
- profile/revision identity.

Verification:

- licensed vectors, every code/control layout, pulse tolerance boundaries,
  missing/extra pulses, noise, year ambiguity, and hardware generator captures.

Exit criteria:

- support is not limited to one hardcoded IRIG-B example;
- `v0.84.0 implementation stop reached. Run pentest for this exact commit.`

### v0.85.0 - IEEE 1344 And Power IRIG

Status: planned.

Goal: implement IEEE 1344 and power-system IRIG extensions.

Deliverables:

- extension/control fields, time quality, local offset, leap/DST indicators;
- exact profile/revision validation;
- compatibility/conflict handling with base IRIG.

Verification:

- licensed vectors, reserved/conflicting fields, parity, transition
  announcements, malformed frames, and power equipment captures.

Exit criteria:

- extension meaning is profile-bound and never inferred from bit position alone;
- `v0.85.0 implementation stop reached. Run pentest for this exact commit.`

### v0.86.0 - WWVB WWV WWVH And CHU

Status: planned.

Goal: implement North American national radio time observations.

Deliverables:

- published amplitude/phase/time codes, frame synchronization, parity/quality,
  announcements, propagation metadata, and decoders;
- acquisition separated from civil decode;
- signal source provenance.

Verification:

- official vectors, recorded signals, noise/fading, wrong station, propagation
  delay, leap/DST announcements, spoof scenarios, and hardware receiver tests.

Exit criteria:

- decoded radio time includes path uncertainty and spoofability;
- `v0.86.0 implementation stop reached. Run pentest for this exact commit.`

### v0.87.0 - DCF77 MSF JJY And Other National Radio

Status: planned.

Goal: implement remaining registry national radio timecodes.

Deliverables:

- separate DCF77, MSF, JJY, BPC, ALS162, RWM, and BPM crates where official
  specifications are accessible;
- station-specific modulation, parity, announcements, and time zone/UTC rules;
- unavailable entries retained as explicit non-claims.

Verification:

- official vectors/recordings per station, noise, propagation, parity,
  transition, spoof, and cross-source comparisons.

Exit criteria:

- each claimed station has authoritative provenance and evidence;
- `v0.87.0 implementation stop reached. Run pentest for this exact commit.`

### v0.88.0 - eLoran And Frequency References

Status: planned.

Goal: implement eLoran time observations and generic frequency references.

Deliverables:

- accessible eLoran timing fields/path/correction models;
- frequency observation, calibration, stability, and traceability types;
- no unsupported positioning claims.

Verification:

- official/lab vectors, propagation/correction faults, chain identity, signal
  loss, oscillator measurements, and captured hardware.

Exit criteria:

- frequency and time-of-arrival observations retain calibration uncertainty;
- `v0.88.0 implementation stop reached. Run pentest for this exact commit.`

### v0.89.0 - Physical Evidence And Spoof Monitoring

Status: planned.

Goal: extract and preserve physical-source risk evidence without duplicating
the generic source fusion owned by `v0.133.0`.

Deliverables:

- inconsistency, propagation, delay, health, authentication, and common-mode
  evidence and correlation metadata;
- preserved provider health, spoof/meaconing evidence, and invalidations;
- protocol-neutral events for later consensus, with no survivor selection,
  source weighting, fusion, servo, or clock change;
- no automatic trust solely from physical origin.

Verification:

- per-source and paired comparison fixtures, common antenna/reference, delayed
  authenticated external evidence, radio spoof, oscillator fault, withdrawal,
  and proof that no local fusion result is emitted.

Exit criteria:

- physical evidence remains source-local and feeds only the later generic
  consensus engine;
- `v0.89.0 implementation stop reached. Run pentest for this exact commit.`

### v0.90.0 - Physical Timing Security Gate

Status: planned.

Goal: complete generic physical timing, conformance, hardware, and security
review without a GNSS implementation dependency.

Deliverables:

- exact physical-source ownership and generic-provider API audit;
- hardware-lab evidence for PPS, IRIG, frequency references, and radio corpora;
- resolved critical/high capture, parser, spoof-evidence preservation,
  invalidation, correlation, and quality findings.

Verification:

- full corpus/fuzz/simulator runs, source and generator matrix, no_std/MSRV,
  long-duration timing measurements, and focused pentest.

Exit criteria:

- generic external and physical timing claims are evidence-backed without a
  Navheim dependency;
- `v0.90.0 implementation stop reached. Run pentest for this exact commit.`

## Phase 8: PTP gPTP Profiles And White Rabbit

### v0.91.0 - PTP Standards Admission And Wire Formats

Status: planned.

Goal: admit exact published PTP revisions and implement IEEE 1588-2008/2019
wire formats and shared TLVs.

Deliverables:

- all event/general messages, headers, timestamp fields, correction, ports,
  sequence, flags, and required TLVs;
- unknown TLV preservation and exact revision identity;
- standards/errata/amendment registry proving that no unpublished
  “PTPv3”/PTPvNext work is presented as a stable standard;
- borrowed decode/caller-owned encode.

Verification:

- licensed vectors, every message/TLV/truncation/alignment, reserved fields,
  maximum correction, arbitrary input, round trips, and publisher-status
  review. Future revision work remains revision-pinned experimental until a
  normative release exists.

Exit criteria:

- packet inspection is complete without claiming clock synchronization;
- `v0.91.0 implementation stop reached. Run pentest for this exact commit.`

### v0.92.0 - PTPv1 Compatibility

Status: planned.

Goal: implement IEEE 1588-2002 compatibility separately.

Deliverables:

- exact v1 messages, datasets, state differences, and conversion boundaries;
- no v1/v2 structure confusion;
- explicit historical/compatibility policy.

Verification:

- licensed vectors/captures, version confusion, malformed fields, replay,
  state transitions, and legacy implementation interop.

Exit criteria:

- PTPv1 remains isolated from modern default operation;
- `v0.92.0 implementation stop reached. Run pentest for this exact commit.`

### v0.93.0 - PTP Datasets And BMCA

Status: planned.

Goal: implement PTP datasets and best-master selection.

Deliverables:

- default/current/parent/time-properties/port datasets;
- foreign-master qualification, BMCA, tie-breaking, and identity;
- explicit evidence that advertised priority is selection input rather than
  authenticated truth;
- bounded candidate storage.

Verification:

- licensed decision vectors, permutations/ties, duplicate identities, timeout,
  malicious priorities, dataset changes, and model checking.

Exit criteria:

- master selection is deterministic and profile-aware;
- `v0.93.0 implementation stop reached. Run pentest for this exact commit.`

### v0.94.0 - End-To-End Delay

Status: planned.

Goal: implement Sync/Follow_Up and Delay_Req/Delay_Resp operation.

Deliverables:

- one/two-step event association, residence/correction, delay, offset, and
  timeout state;
- software/hardware timestamp quality plus binding of event/general message,
  sequence, source port, domain, transport, and callback generation to one
  exchange;
- asymmetry/negative-delay warnings.

Verification:

- licensed examples, reorder/loss/duplicate, 16-bit sequence-ID wrap, wrong
  sequence/source, correction overflow, delayed transmit timestamp, asymmetry,
  and simulator runs.

Exit criteria:

- event timestamps cannot associate with the wrong exchange;
- `v0.94.0 implementation stop reached. Run pentest for this exact commit.`

### v0.95.0 - Peer-To-Peer Delay

Status: planned.

Goal: implement Pdelay exchanges and neighbor rate ratio.

Deliverables:

- request/response/follow-up association, peer mean path delay, rate ratio;
- neighbor identity, multiport state, and lost-response policy;
- delay attack signals.

Verification:

- licensed vectors, reordered peers, source changes, asymmetry, loss, duplicate,
  rate drift, transparent peers, and simulator traces.

Exit criteria:

- peer delay state is bounded and cannot cross port identities;
- `v0.95.0 implementation stop reached. Run pentest for this exact commit.`

### v0.96.0 - Ordinary Clock State Machine

Status: planned.

Goal: implement complete ordinary-clock port behavior.

Deliverables:

- all required states, timers, qualification, announce timeout, role changes;
- E2E/P2P and one/two-step integration;
- state transition evidence and fault recovery.

Verification:

- transition coverage, timer boundaries, grandmaster change, port fault,
  message mutation, 16-bit sequence-ID wrap across every active exchange,
  stale pre-wrap messages, and independent PTP implementation interop.

Exit criteria:

- ordinary-clock behavior satisfies the selected revision clause map;
- `v0.96.0 implementation stop reached. Run pentest for this exact commit.`

### v0.97.0 - Boundary Clock

Status: planned.

Goal: implement bounded multiport boundary-clock behavior.

Deliverables:

- per-port datasets/state, one selected parent, downstream master behavior;
- topology loop and domain protection;
- cross-port timestamp/correction association and validated observation
  outputs, with no generic servo implementation.

Verification:

- multiport simulator, topology changes, loops, simultaneous masters, port
  failure, source quality changes, and linuxptp interop.

Exit criteria:

- state cannot leak across domains or ports incorrectly;
- `v0.97.0 implementation stop reached. Run pentest for this exact commit.`

### v0.98.0 - Transparent Clocks

Status: planned.

Goal: implement E2E and P2P transparent-clock correction behavior.

Deliverables:

- ingress/egress residence time, correction updates, peer delay, forwarding;
- one/two-step handling and overflow policy;
- monitor-only mode.

Verification:

- hardware/simulator residence paths, correction overflow, negative/late
  timestamps, duplicates, multi-hop composition, and independent switch interop.

Exit criteria:

- correction evidence remains traceable through each clock;
- `v0.98.0 implementation stop reached. Run pentest for this exact commit.`

### v0.99.0 - PTP Transports

Status: planned.

Goal: implement raw Ethernet, UDPv4, and UDPv6 PTP mappings.

Deliverables:

- multicast/unicast addresses, ports, EtherType, domain/interface policy;
- event/general socket separation and timestamp metadata;
- VLAN/link metadata hooks where specified.

Verification:

- packet captures, IPv4/IPv6/raw interop, multicast membership, interface
  changes, wrong domain/port, MTU, and timestamp association.

Exit criteria:

- transport choice does not alter base PTP semantic validation;
- `v0.99.0 implementation stop reached. Run pentest for this exact commit.`

### v0.100.0 - Signaling Management And YANG

Status: planned.

Goal: implement PTP signaling, management, and management mappings.

Deliverables:

- complete accessible actions/TLVs, target identities, errors, and response;
- bounded management datasets and RFC 8575 YANG mapping;
- remote mutation authorization disabled by default.

Verification:

- licensed vectors, unknown/critical TLVs, targeting, fragmentation, access
  denial, amplification/work limits, and management interop.

Exit criteria:

- unauthenticated management cannot alter live clock state;
- `v0.100.0 implementation stop reached. Run pentest for this exact commit.`

### v0.101.0 - PTP Hardware Measurement Integration

Status: planned.

Goal: admit and correlate PTP hardware measurements without implementing a
second servo or holdover engine.

Deliverables:

- timestamp quality admission, PHC/system target choice, cross timestamps;
- calibration, quantization, path/asymmetry, correction, capture, and
  cross-timestamp error-budget inputs;
- validated interval observations, discontinuities, withdrawals, and target
  capability evidence for later `mundilfari-engine` servos;
- no source fusion, servo, holdover, or discipline decision.

Verification:

- hardware NIC/PHC lab, timestamp loss/reorder, sequence wrap, oscillator
  drift evidence, grandmaster changes/withdrawal, PHC reset, cable asymmetry,
  cross-timestamp latency, and fault injection;
- dependency tests proving PTP/platform crates do not depend on engine and
  contain no servo/holdover algorithm.

Exit criteria:

- accuracy reports derive from measured paths rather than packet decode;
- `v0.101.0 implementation stop reached. Run pentest for this exact commit.`

### v0.102.0 - gPTP

Status: planned.

Goal: implement IEEE 802.1AS-2011 and 802.1AS-2020 profiles.

Deliverables:

- profile-specific datasets, BMCA differences, domains, intervals, roles,
  transport, time-aware system, and quality;
- revision isolation and legacy interoperability;
- TSN clock correlation outputs.

Verification:

- licensed vectors, conformance suite where available, multi-hop TSN
  simulation, automotive/media peers, revision mismatch, and hardware interop.

Exit criteria:

- gPTP local/network time is not labeled UTC without correlation;
- `v0.102.0 implementation stop reached. Run pentest for this exact commit.`

### v0.103.0 - Enterprise And Telecom Profiles

Status: planned.

Goal: implement IETF Enterprise and ITU-T telecom PTP profiles.

Deliverables:

- RFC 9760 and licensed G.8265.1/G.8275.1/G.8275.2 parameters;
- profile-specific BMCA, transport, unicast, timing, quality, and topology;
- profile negotiation/config validation.

Verification:

- RFC/licensed vectors, telecom lab/simulator, wrong profile/domain, source
  quality transitions, holdover, and vendor interop.

Exit criteria:

- profile rules remain outside and cannot weaken the base engine;
- `v0.103.0 implementation stop reached. Run pentest for this exact commit.`

### v0.104.0 - Power PTP Profiles

Status: planned.

Goal: implement power-system PTP profiles as one independently reviewed
licensed family.

Deliverables:

- IEEE C37.238 and IEC/IEEE 61850-9-3 exact admitted revisions;
- exact licensed parameters, identities, TLVs, intervals, and quality;
- no power-control functionality outside timing.

Verification:

- licensed vectors/conformance, power equipment interoperability, wrong
  profile, domain collision, topology, grandmaster switch, and long soak.

Exit criteria:

- every profile claim names its exact revision and evidence;
- `v0.104.0 implementation stop reached. Run pentest for this exact commit.`

### v0.104.1 - Media PTP And AES67 Profiles

Status: planned.

Goal: implement broadcast/media PTP and AES67 timing profiles separately from
power and fronthaul.

Deliverables:

- SMPTE ST 2059-2 and AES67 exact admitted revisions and their required base
  profiles;
- profile identities, domains, intervals, datasets, quality, and media-clock
  correlation boundaries;
- no media payload or uncorrelated UTC claim.

Verification:

- licensed vectors/conformance, studio/audio equipment interop, wrong profile,
  epoch/rate correlation, domain collision, grandmaster switch, and long soak.

Exit criteria:

- media profile time remains distinct from media counters and names exact
  revision/evidence;
- `v0.104.1 implementation stop reached. Run pentest for this exact commit.`

### v0.104.2 - Fronthaul And O-RAN Timing Profiles

Status: planned.

Goal: implement IEEE 802.1CM and applicable O-RAN timing profiles as a
separate topology/security domain.

Deliverables:

- exact admitted IEEE 802.1CM and O-RAN WG4 revisions;
- fronthaul profile parameters, topology, quality, timing chain, SyncE/PTP
  interaction, identities, and failure evidence;
- no radio/access-network functionality outside timing.

Verification:

- licensed vectors/conformance, fronthaul lab/simulator, wrong profile/domain,
  topology/path changes, source/SyncE quality changes, holdover evidence, and
  multi-vendor interop.

Exit criteria:

- fronthaul timing claims are revision-, topology-, and evidence-specific;
- `v0.104.2 implementation stop reached. Run pentest for this exact commit.`

### v0.105.0 - Synchronous Ethernet

Status: planned.

Goal: implement SyncE timing messaging and quality-level integration.

Deliverables:

- accessible ESMC/SSM messages, quality levels, selection, failure, and
  frequency-source provenance;
- frequency transfer distinct from phase/time;
- PTP profile integration hooks.

Verification:

- licensed vectors, quality transitions, loops, source loss, mismatched
  frequency/time sources, and lab equipment interop.

Exit criteria:

- frequency lock never implies phase or UTC synchronization;
- `v0.105.0 implementation stop reached. Run pentest for this exact commit.`

### v0.106.0 - White Rabbit

Status: planned.

Goal: implement White Rabbit/high-accuracy software and hardware boundaries.

Deliverables:

- compatible PTP high-accuracy profile, WR TLVs/state, frequency/phase, link
  delay, calibration, fixed-delay compensation, and hardware capability;
- monitor/codec operation without compatible hardware;
- calibrated fiber asymmetry, compatible topology, servo-evidence boundary,
  and explicit accuracy non-claims.

Verification:

- legitimate specification vectors, WR hardware lab, fiber/link changes,
  calibration corruption, asymmetric delay, holdover, and multi-device interop.

Exit criteria:

- White Rabbit accuracy is claimed only for measured compatible hardware;
- `v0.106.0 implementation stop reached. Run pentest for this exact commit.`

### v0.107.0 - Experimental NTS4PTP

Status: planned.

Goal: implement the exact pinned NTS-for-PTP draft experimentally.

Deliverables:

- `draft-ietf-ntp-nts-for-ptp-03` exact source hash and
  final-RFC/new-revision migration check immediately before implementation;
- revision-specific messages/state/security associations;
- integration with NTS provider boundaries and PTP identities;
- no stable profile leakage or silent activation.

Verification:

- draft vectors, revision mismatch, replay, key rotation, delay attack
  residuals, malformed security TLVs, and available interop.

Exit criteria:

- experimental authentication never implies delay-attack immunity;
- `v0.107.0 implementation stop reached. Run pentest for this exact commit.`

### v0.107.1 - Experimental NTP Over PTP

Status: planned.

Goal: integrate the exact pinned NTP-over-PTP transport only after both NTP
and PTP wire, timestamp, correction, and transport foundations exist.

Deliverables:

- `draft-ietf-ntp-over-ptp-08` exact source hash and final-RFC/new-revision
  migration check immediately before implementation;
- revision-named PTP encapsulation, NTP network-correction extension field,
  client/server and draft-defined symmetric transport behavior;
- explicit reuse of reviewed NTP validation and PTP framing/timestamp
  boundaries without a second NTP or PTP state engine;
- transparent-clock correction provenance, overflow, trust, and accuracy
  policy with experimental-only negotiation.

Verification:

- exact draft vectors, revision mismatch, malformed encapsulation, wrong PTP
  message/domain, correction overflow/tamper, NTP extension conflicts,
  one/two-step timestamp failures, transparent-clock paths, hardware captures,
  and chrony/available implementation interop.

Exit criteria:

- NTP-over-PTP cannot be enabled before both protocol foundations exist and
  never converts unauthenticated correction data into an accuracy claim;
- `v0.107.1 implementation stop reached. Run pentest for this exact commit.`

### v0.107.2 - Stable PTP Authentication And Security Associations

Status: planned.

Goal: implement only the stable PTP authentication and security-association
behavior admitted from the exact locked IEEE 1588 revision.

Deliverables:

- clause-mapped Security TLV and integrity/authentication semantics from the
  admitted stable revision, with unknown revision/profile behavior rejected;
- security-association identity isolated by PTP domain, port, peer,
  direction, algorithm, key, and generation;
- replay windows and sequence-ID wrap behavior;
- key activation, overlap, rollover, usage exhaustion, revocation, and
  fail-closed association replacement through the generic provider boundary;
- explicit multiport/domain isolation and downgrade policy;
- authenticated-but-delayable residual-risk evidence: authentication never
  claims bounded network delay, truthful BMCA data, or delay-attack immunity;
- explicit external-security-only non-claim for any PTP revision/profile whose
  stable internal mechanism is not admitted.

Verification:

- exact licensed vectors and independent implementation interop, malformed/
  duplicate/wrong-order Security TLVs, replay at and across sequence wrap,
  wrong domain/port/direction/association, key overlap/revocation/exhaustion,
  multiport isolation, downgrade, delayed authenticated messages, provider
  failure, fuzzing, and long rotation soak.

Exit criteria:

- stable internal PTP authentication is implemented and named precisely, or
  the affected mode remains explicitly external-security-only;
- `v0.107.2 implementation stop reached. Run pentest for this exact commit.`

### v0.108.0 - PTP Family Security And Hardware Gate

Status: planned.

Goal: complete PTP profile conformance, hardware evidence, and security review.

Deliverables:

- revision/profile clause maps and support matrix;
- stable PTP authentication/security-association, NTS4PTP, and NTP-over-PTP
  revision, downgrade, correction, key-lifecycle, and trust review;
- delay/topology/threat and accuracy evidence report;
- strict-discipline admission requiring an admitted PTP security mechanism,
  MACsec/IPsec-equivalent trusted boundary, statically trusted isolated timing
  domain, or independent corroboration with bounded correction authority;
- explicit residual-risk statement for malicious on-link grandmasters and
  untruthful BMCA priority;
- resolved critical/high parser, state, FFI, timestamp, correction,
  observation, and profile issues.

Verification:

- linuxptp/vendor matrix, official suites, multi-NIC/grandmaster/switch lab,
  fuzz/simulator/soak, target matrix, and focused pentest.

Exit criteria:

- precision claims are bounded by actual measured configurations;
- `v0.108.0 implementation stop reached. Run pentest for this exact commit.`

## Phase 9: Industrial Automotive Wireless Media And Space

### v0.109.0 - BACnet Time

Status: planned.

Goal: implement only the timing services of the admitted BACnet revision.

Deliverables:

- BACnet time/date, synchronization, and timestamped-event objects assigned by
  the exact licensed revision;
- surrounding BACnet transport/application trait boundary;
- no complete BACnet stack claim.

Verification:

- licensed vectors, malformed objects, rollover, event order, simulator, and
  independent BACnet stack interop.

Exit criteria:

- the BACnet crate exposes timing only and preserves application context;
- `v0.109.0 implementation stop reached. Run pentest for this exact commit.`

### v0.109.1 - DNP3 Time

Status: planned.

Goal: implement only the timing services of the admitted DNP3 revision.

Deliverables:

- DNP3 synchronization, delay measurement, timestamped-event objects, quality,
  and source/session identity from the exact licensed revision;
- surrounding DNP3 transport/application trait boundary;
- no complete DNP3 stack claim.

Verification:

- licensed vectors, malformed objects, sequence/delay, rollover, event order,
  replay, simulator, and independent DNP3 stack interop.

Exit criteria:

- the DNP3 crate exposes timing only and preserves application context;
- `v0.109.1 implementation stop reached. Run pentest for this exact commit.`

### v0.110.0 - IEC Power Time

Status: planned.

Goal: implement IEC 60870 and IEC 61850 time mappings.

Deliverables:

- relevant timestamp formats, quality flags, sync/control timing, and event
  semantics;
- power profile correlation with PTP where specified;
- exact licensed scope.

Verification:

- licensed vectors, invalid/reserved quality, leap/DST, rollover, stale event,
  device interop, and fault simulations.

Exit criteria:

- time quality flags are never discarded during normalization;
- `v0.110.0 implementation stop reached. Run pentest for this exact commit.`

### v0.111.0 - CANopen And J1939 Time

Status: planned.

Goal: implement CANopen and J1939 time services.

Deliverables:

- time/date messages, epoch/rollover, node/source identity, and CAN transport
  boundary;
- bus load/resource policy;
- no general vehicle/fieldbus stack.

Verification:

- licensed vectors/captures, arbitration reorder, duplicate source, rollover,
  malformed frames, bus saturation, and device interop.

Exit criteria:

- CAN timing state is source-bound and bounded;
- `v0.111.0 implementation stop reached. Run pentest for this exact commit.`

### v0.112.0 - EtherCAT Distributed Clocks

Status: planned.

Goal: implement EtherCAT distributed-clock timing as one licensed family.

Deliverables:

- exact distributed-clock registers/messages/state, cycle/time correlation,
  delay, quality, and topology from the admitted revision;
- bounded timing-only transport/device boundary;
- no general EtherCAT motion/control stack.

Verification:

- licensed vectors, simulator/equipment, cycle wrap, source loss, jitter,
  topology changes, and independent stack interop.

Exit criteria:

- EtherCAT timing is independently reviewable and scope-limited;
- `v0.112.0 implementation stop reached. Run pentest for this exact commit.`

### v0.112.1 - PROFINET Time Synchronization

Status: planned.

Goal: implement the admitted PROFINET timing profile independently.

Deliverables:

- exact timing messages/state, cycle/time correlation, quality, domains, and
  normative PTP integration;
- bounded timing-only transport/profile boundary;
- no general PROFINET stack.

Verification:

- licensed vectors, simulator/equipment, cycle wrap, loss/jitter, wrong
  profile/domain, topology changes, and independent interop.

Exit criteria:

- PROFINET timing claims name their exact revision and profile;
- `v0.112.1 implementation stop reached. Run pentest for this exact commit.`

### v0.112.2 - CIP Sync

Status: planned.

Goal: implement CIP Sync timing independently of other industrial Ethernet
families.

Deliverables:

- exact admitted profile objects/messages, identities, PTP mapping, quality,
  and cycle/time correlation;
- bounded timing-only application/transport boundary;
- no general CIP/EtherNet-IP stack.

Verification:

- licensed vectors, simulator/equipment, object faults, source/profile
  changes, cycle wrap, PTP mismatch, and independent interop.

Exit criteria:

- CIP Sync behavior cannot leak assumptions into other industrial profiles;
- `v0.112.2 implementation stop reached. Run pentest for this exact commit.`

### v0.112.3 - Sercos Timing

Status: planned.

Goal: implement the admitted Sercos timing mechanisms separately.

Deliverables:

- exact cycle, phase, time correlation, quality, synchronization, and topology
  behavior from the licensed revision;
- bounded timing-only transport/device boundary;
- no motion/control completeness claim.

Verification:

- licensed vectors, simulator/equipment, cycle/phase wrap, jitter, loss,
  topology/source changes, malformed timing data, and interop.

Exit criteria:

- Sercos timing is independently tested and revision-bound;
- `v0.112.3 implementation stop reached. Run pentest for this exact commit.`

### v0.112.4 - POWERLINK Timing

Status: planned.

Goal: implement the admitted POWERLINK timing mechanisms separately.

Deliverables:

- exact cycle, synchronization, time correlation, quality, source, and
  topology behavior from the licensed revision;
- bounded timing-only transport/device boundary;
- no general POWERLINK stack.

Verification:

- licensed vectors, simulator/equipment, cycle wrap, jitter/loss, source and
  topology change, malformed timing data, and interop.

Exit criteria:

- POWERLINK timing is independently tested and revision-bound;
- `v0.112.4 implementation stop reached. Run pentest for this exact commit.`

### v0.113.0 - KNX And OPC UA Time

Status: planned.

Goal: implement KNX and OPC UA time-related services.

Deliverables:

- exact date/time/zone/status/timestamp mappings;
- surrounding application/transport boundary and trust provenance;
- local/UTC ambiguity handling.

Verification:

- licensed vectors, invalid civil values, zone/DST, stale server, malformed
  payload, and independent stack interop.

Exit criteria:

- formatted application time is not treated as synchronized automatically;
- `v0.113.0 implementation stop reached. Run pentest for this exact commit.`

### v0.114.0 - AUTOSAR Time

Status: planned.

Goal: implement AUTOSAR Ethernet, CAN, and FlexRay time synchronization.

Deliverables:

- separate transport profiles, message/state/sequence/CRC, domains, rate
  correction, gateway behavior, and quality;
- fixed-capacity Sans-I/O engine with caller-owned buffers, const-generic
  association/source bounds, explicit monotonic input, deterministic work
  budget, and bounded send/timer/observation actions;
- explicit CAN, FlexRay, serial-edge, and IRIG capture-domain identities;
- exact licensed revisions;
- automotive safety non-claims.

Verification:

- licensed vectors, sequence/replay, gateway paths, bus loss, rate drift,
  malformed messages, capacity extremes, target stack/WCET measurement, and
  automotive simulator interop.

Exit criteria:

- each AUTOSAR transport retains profile-specific semantics;
- `v0.114.0 implementation stop reached. Run pentest for this exact commit.`

### v0.115.0 - FlexRay And TTEthernet

Status: planned.

Goal: implement native FlexRay and SAE AS6802/TTEthernet timing.

Deliverables:

- cycle/macrotick timing, fault-tolerant synchronization, clique/fault state,
  and network-time correlation;
- transport traits and exact licensed scope;
- no general bus scheduler.

Verification:

- licensed vectors, clique split, malicious clocks, cycle rollover, frame
  loss, rate fault, and deterministic network simulation.

Exit criteria:

- fault-tolerant claims match the exact modeled assumptions;
- `v0.115.0 implementation stop reached. Run pentest for this exact commit.`

### v0.116.0 - Bluetooth Time

Status: planned.

Goal: implement Bluetooth time services and Mesh Time.

Deliverables:

- Current Time, Reference Time Update, Device Time, Time Profile, Elapsed Time,
  and Mesh timing assigned by accessible specifications;
- GATT/mesh transport traits, authority, zone/DST, accuracy, and update state;
- permission and bonding policy hooks.

Verification:

- licensed vectors, malformed characteristics, replay, unauthorized update,
  zone/leap transitions, mesh propagation, and device interop.

Exit criteria:

- local wireless time cannot silently authorize system-clock changes;
- `v0.116.0 implementation stop reached. Run pentest for this exact commit.`

### v0.117.0 - Zigbee Time

Status: planned.

Goal: implement the admitted Zigbee time cluster independently.

Deliverables:

- exact time attributes/commands, authority, validity, zone/DST, and transport
  boundary;
- replay/age, sleep/rejoin, and unauthorized-writer policy;
- no general Zigbee stack.

Verification:

- licensed vectors, invalid civil values, replay, unauthorized updates,
  sleep/rejoin, malformed payloads, and ecosystem interop.

Exit criteria:

- Zigbee time retains authority, validity, and civil-time provenance;
- `v0.117.0 implementation stop reached. Run pentest for this exact commit.`

### v0.117.1 - Matter Time

Status: planned.

Goal: implement the admitted Matter time-synchronization service independently.

Deliverables:

- exact cluster/service fields, trust, granularity, source, failure, and
  transport boundary;
- fabric/node identity, replay/age, and administrator policy;
- no general Matter stack.

Verification:

- licensed vectors, fabric/node changes, unauthorized writer, stale/replayed
  data, malformed payloads, failover, and ecosystem interop.

Exit criteria:

- Matter time is source- and fabric-bound with explicit trust;
- `v0.117.1 implementation stop reached. Run pentest for this exact commit.`

### v0.117.2 - LoRaWAN DeviceTime

Status: planned.

Goal: implement the admitted LoRaWAN DeviceTime exchange independently.

Deliverables:

- exact request/answer fields, scale/epoch, fraction, network/session identity,
  frame-counter binding, delay, and uncertainty;
- replay, join/rejoin, rollover, and age policy;
- no general LoRaWAN stack.

Verification:

- licensed vectors, frame-counter/replay, rollover, delay/asymmetry,
  join/rejoin, malformed answers, and network-server interop.

Exit criteria:

- LoRaWAN time retains scale, session, delay, and security provenance;
- `v0.117.2 implementation stop reached. Run pentest for this exact commit.`

### v0.118.0 - Wi-Fi TSF And FTM Correlation

Status: planned.

Goal: implement Wi-Fi TSF/FTM clock correlations without ranging or position.

Deliverables:

- exact TSF/FTM timing fields, clock/AP identity, counter wrap, capture, and
  correlation quality;
- association/roam/generation and delay evidence;
- no ranging-distance or position calculation.

Verification:

- licensed vectors, counter wrap, AP/association changes, delayed/replayed
  frames, capture quality, malicious peer, and device captures.

Exit criteria:

- Wi-Fi local clocks are not mislabeled civil UTC or distance;
- `v0.118.0 implementation stop reached. Run pentest for this exact commit.`

### v0.118.1 - TSCH And 6TiSCH Timing

Status: planned.

Goal: implement the tightly coupled IEEE 802.15.4 TSCH and 6TiSCH timing
profiles separately from Wi-Fi.

Deliverables:

- slot/ASN timing, coordinator/source identity, synchronization updates,
  rollover, quality, and loss state;
- exact 6TiSCH profile behavior over the admitted TSCH revision;
- no general 802.15.4/6LoWPAN stack.

Verification:

- licensed/RFC vectors, slot/counter wrap, coordinator change, drift,
  delayed/replayed updates, partition/merge, malformed frames, and simulation.

Exit criteria:

- deterministic slot timing retains profile, source, and partition state;
- `v0.118.1 implementation stop reached. Run pentest for this exact commit.`

### v0.119.0 - WirelessHART Time

Status: planned.

Goal: implement only the timing portion of WirelessHART.

Deliverables:

- exact network time, slots, synchronization updates, source/quality, and loss
  behavior;
- timing-only transport boundary and revision identity;
- no general WirelessHART stack.

Verification:

- licensed vectors, manager loss, slot/counter wrap, replay/delay, partition,
  malformed frames, and simulator/equipment interop.

Exit criteria:

- WirelessHART timing remains independently revision-bound;
- `v0.119.0 implementation stop reached. Run pentest for this exact commit.`

### v0.119.1 - ISA100 Time

Status: planned.

Goal: implement only the timing portion of ISA100.

Deliverables:

- exact network time, slots, updates, source/quality, and loss behavior;
- timing-only transport boundary and revision identity;
- no general ISA100 stack.

Verification:

- licensed vectors, manager loss, slot/counter wrap, replay/delay, partition,
  malformed frames, and simulator/equipment interop.

Exit criteria:

- ISA100 timing remains independently revision-bound;
- `v0.119.1 implementation stop reached. Run pentest for this exact commit.`

### v0.119.2 - Thread Time

Status: planned.

Goal: implement only the admitted Thread time services.

Deliverables:

- exact network-time fields/state, leader/source identity, quality, age, and
  partition behavior;
- timing-only Thread transport/application boundary;
- no general Thread stack.

Verification:

- licensed vectors, leader change, partition/merge, replay/delay, counter
  wrap, malformed data, and ecosystem interop.

Exit criteria:

- Thread time retains partition, leader, and trust provenance;
- `v0.119.2 implementation stop reached. Run pentest for this exact commit.`

### v0.120.0 - Cellular NITZ

Status: planned.

Goal: implement NITZ civil/zone information as low-trust network evidence.

Deliverables:

- exact civil, zone, DST, network identity, age, and receipt metadata;
- roaming/change/replay and correction policy;
- no modem or radio-access stack.

Verification:

- public/licensed vectors, zone/DST, stale network, roaming, replay, malformed
  fields, leap boundaries, and modem captures.

Exit criteria:

- unauthenticated NITZ civil time remains visibly low trust;
- `v0.120.0 implementation stop reached. Run pentest for this exact commit.`

### v0.120.1 - 5G Reference Time

Status: planned.

Goal: implement applicable 5G reference-time mappings independently of NITZ.

Deliverables:

- exact reference-time information, scale, network/source identity, quality,
  uncertainty, age, and correction semantics;
- generation, replay, roaming/handover, and withdrawal behavior;
- no radio-access stack.

Verification:

- licensed vectors, scale/leap cases, stale/replayed data, roaming/handover,
  source generation, malformed fields, and modem/network fixtures.

Exit criteria:

- 5G reference time retains scale, uncertainty, and network provenance;
- `v0.120.1 implementation stop reached. Run pentest for this exact commit.`

### v0.121.0 - SMPTE Timecode

Status: planned.

Goal: implement the exact admitted SMPTE timecode revision.

Deliverables:

- frame/drop-frame values, rates, user/control data, discontinuity, source, and
  clock-correlation types;
- exact transport/profile boundaries;
- no uncorrelated UTC claim.

Verification:

- licensed vectors, every frame rate/drop-frame boundary, day wrap,
  discontinuity, malformed codes, and equipment/file interop.

Exit criteria:

- SMPTE frame position becomes civil time only through explicit correlation;
- `v0.121.0 implementation stop reached. Run pentest for this exact commit.`

### v0.121.1 - MIDI Timecode

Status: planned.

Goal: implement the exact admitted MIDI timecode revision.

Deliverables:

- full-frame/quarter-frame forms, rates, direction, source, reconstruction,
  discontinuity, and correlation;
- exact MIDI transport boundary;
- no general MIDI stack.

Verification:

- licensed vectors, frame assembly/reorder/loss, rate changes, reverse
  direction, wrap, malformed messages, and equipment interop.

Exit criteria:

- MIDI position remains a media timeline until explicitly correlated;
- `v0.121.1 implementation stop reached. Run pentest for this exact commit.`

### v0.121.2 - AES Audio Timing

Status: planned.

Goal: implement the exact admitted AES audio timing mechanisms independently.

Deliverables:

- sample/frame counters, rates, source/clock identity, quality,
  discontinuities, and wall-clock correlation where specified;
- exact licensed transport/profile scope;
- no audio codec/processing stack.

Verification:

- licensed vectors, sample wrap, rate/source changes, discontinuity, malformed
  timing data, and equipment/file interop.

Exit criteria:

- AES sample position never becomes UTC without normative correlation;
- `v0.121.2 implementation stop reached. Run pentest for this exact commit.`

### v0.121.3 - RDS Time

Status: planned.

Goal: implement the admitted RDS civil-time signaling independently.

Deliverables:

- exact date/time/offset/quality fields, station identity, acquisition age,
  propagation uncertainty, and trust;
- no general radio-data decoder claim beyond required timing framing.

Verification:

- licensed vectors/captures, offset/date boundaries, stale/repeated groups,
  signal loss, malformed fields, propagation, and receiver interop.

Exit criteria:

- RDS civil time remains station/path-bound evidence;
- `v0.121.3 implementation stop reached. Run pentest for this exact commit.`

### v0.121.4 - DVB Time

Status: planned.

Goal: implement the admitted DVB time tables independently.

Deliverables:

- exact UTC/local-offset tables, descriptors, service/network identity,
  versioning, validity, and update behavior;
- bounded section/transport boundary and no general broadcast stack.

Verification:

- licensed vectors/captures, table version/change, offset transitions,
  malformed sections, replay/staleness, and receiver interop.

Exit criteria:

- DVB time retains table version, service identity, and validity;
- `v0.121.4 implementation stop reached. Run pentest for this exact commit.`

### v0.121.5 - ATSC Time

Status: planned.

Goal: implement the admitted ATSC time signaling independently.

Deliverables:

- exact system-time, offset/daylight, source/service identity, version, and
  validity behavior;
- bounded table/transport boundary and no general broadcast stack.

Verification:

- licensed vectors/captures, GPS/UTC/leap mapping, version changes, malformed
  tables, replay/staleness, and receiver interop.

Exit criteria:

- ATSC time retains scale/model, table version, and service provenance;
- `v0.121.5 implementation stop reached. Run pentest for this exact commit.`

### v0.121.6 - ISDB Time

Status: planned.

Goal: implement the admitted ISDB time signaling independently.

Deliverables:

- exact civil/time-offset tables, service/network identity, version, validity,
  and update behavior;
- bounded table/transport boundary and no general broadcast stack.

Verification:

- licensed vectors/captures, table version/change, offset transitions,
  malformed sections, replay/staleness, and receiver interop.

Exit criteria:

- ISDB time retains table version, service identity, and validity;
- `v0.121.6 implementation stop reached. Run pentest for this exact commit.`

### v0.122.0 - RTP And RTCP Clock Correlation

Status: planned.

Goal: implement RTP/RTCP media-clock correlation independently.

Deliverables:

- RTP counters, RTCP sender mappings, clock/source identity, wrap,
  discontinuity, capture, and synchronization metadata;
- RFC updates and no media codec/session stack.

Verification:

- RFC vectors, counter wrap, jitter/reorder, wrong sender mapping, source
  change, discontinuity, malicious mappings, and independent interop.

Exit criteria:

- RTP media and civil timelines remain type-distinct;
- `v0.122.0 implementation stop reached. Run pentest for this exact commit.`

### v0.122.1 - MPEG Timing

Status: planned.

Goal: implement MPEG PTS/DTS/PCR timing independently.

Deliverables:

- exact counters/rates, wrap, discontinuity, program/source identity, capture,
  and clock-correlation types;
- licensed systems timing scope and no codec implementation.

Verification:

- licensed vectors, counter wrap, discontinuity, jitter, program/source
  changes, malformed fields, and reference-tool interop.

Exit criteria:

- MPEG timestamps remain program-clock values until explicitly correlated;
- `v0.122.1 implementation stop reached. Run pentest for this exact commit.`

### v0.122.2 - DASH Timing

Status: planned.

Goal: implement DASH presentation and wall-clock timing independently.

Deliverables:

- exact manifest timeline, availability, UTC-timing, periods, discontinuities,
  source identity, and uncertainty;
- bounded manifest timing boundary and no player implementation.

Verification:

- licensed vectors, manifest extremes, period/discontinuity changes, stale or
  malicious wall-clock source, overflow, and reference-tool interop.

Exit criteria:

- DASH presentation and wall-clock timelines remain explicitly correlated;
- `v0.122.2 implementation stop reached. Run pentest for this exact commit.`

### v0.122.3 - HLS Timing

Status: planned.

Goal: implement RFC 8216 HLS timing independently.

Deliverables:

- media sequence, durations, discontinuities, program-date-time, source, and
  wall-clock correlation;
- bounded playlist timing boundary and no player implementation.

Verification:

- RFC vectors, sequence/wrap, discontinuity, malformed/extreme playlists,
  conflicting program dates, stale sources, and reference-tool interop.

Exit criteria:

- HLS media and civil timelines remain explicitly correlated;
- `v0.122.3 implementation stop reached. Run pentest for this exact commit.`

### v0.122.4 - SCTE Timing

Status: planned.

Goal: implement the exact admitted SCTE timing constructs independently.

Deliverables:

- exact splice/event timing, clock/source identity, wrap, discontinuity, and
  wall-clock correlation from licensed revisions;
- bounded signaling boundary and no broadcast automation stack.

Verification:

- licensed vectors, event/counter wrap, discontinuity, source change,
  malformed signaling, conflicting correlations, and equipment interop.

Exit criteria:

- SCTE event time retains exact source and clock correlation;
- `v0.122.4 implementation stop reached. Run pentest for this exact commit.`

### v0.123.0 - CCSDS Time

Status: planned.

Goal: implement selected complete CCSDS time-code families.

Deliverables:

- unsegmented, day-segmented, calendar-segmented, ASCII, P-field, fine-time,
  agency epoch, and mission registry support;
- exact Blue Book revision and legal vector provenance;
- mission epoch context.

Verification:

- official vectors, P-field combinations, epoch ambiguity, fine-time extremes,
  truncation, malformed codes, and reference tool comparison.

Exit criteria:

- CCSDS support is complete for the claimed revision/families;
- `v0.123.0 implementation stop reached. Run pentest for this exact commit.`

### v0.124.0 - SpaceWire SpaceFibre And ECSS Time

Status: planned.

Goal: implement space link timecodes and ECSS timing profiles.

Deliverables:

- accessible SpaceWire/SpaceFibre time distribution and ECSS mappings;
- control/data correlation, mission epoch, quality, and loss state;
- no complete spacecraft bus stack.

Verification:

- licensed vectors, counter wrap, lost/reordered codes, link reset, epoch
  mismatch, malformed controls, and hardware/simulator interop.

Exit criteria:

- link-local and mission civil time remain explicitly correlated;
- `v0.124.0 implementation stop reached. Run pentest for this exact commit.`

### v0.125.0 - Domain Protocol Security Gate

Status: planned.

Goal: audit industrial, automotive, wireless, media, and space timing.

Deliverables:

- exact licensed revision/clause/completeness matrix;
- timing-only and no-surrounding-stack API audit;
- fixed-capacity work-budget, stack-use, and target-specific WCET evidence;
- explicit ISO 26262/IEC 61508 and other functional-safety non-claims unless
  separate traceability, tool qualification, safety manuals, and integration
  assessment exist;
- resolved critical/high parser, state, replay, resource, and trust findings.

Verification:

- all official vectors, cross-domain fuzzing, simulators/equipment subsets,
  target/MSRV matrix, and focused pentest.

Exit criteria:

- every domain claim is narrow, source-bound, and evidence-backed;
- `v0.125.0 implementation stop reached. Run pentest for this exact commit.`

## Phase 10: Trusted Timestamp Evidence

### v0.126.0 - RFC 3161 Codec And Client

Status: planned.

Goal: implement bounded Time-Stamp Protocol requests/responses and client state.

Deliverables:

- message imprint, algorithms, policy, nonce, certificates, status, token, and
  transport boundary;
- strict ASN.1/DER through reviewed generic or first-party bounded components;
- evidence distinct from current-time observation.

Verification:

- RFC vectors, malformed DER, algorithm/policy mismatch, nonce replay, imprint
  mismatch, huge chains, client/server captures, and independent TSA interop.

Exit criteria:

- a token cannot verify for the wrong data, policy, nonce, or authority;
- `v0.126.0 implementation stop reached. Run pentest for this exact commit.`

### v0.127.0 - RFC 3161 TSA Server And RFC 5816

Status: planned.

Goal: implement a bounded TSA server and updated algorithm behavior.

Deliverables:

- request admission, clock/evidence source policy, serials, signing provider,
  certificates, failure statuses, and RFC 5816 updates;
- rate/work limits and audited issuance records;
- no claim beyond configured authority/time source.

Verification:

- independent clients, algorithm transitions, duplicate nonce, clock fault,
  signing failure, floods, malformed requests, and token verification.

Exit criteria:

- issuance fails closed when trusted time or signing authority is unavailable;
- `v0.127.0 implementation stop reached. Run pentest for this exact commit.`

### v0.128.0 - Evidence Record Syntax

Status: planned.

Goal: implement ERS and XMLERS archival evidence.

Deliverables:

- hash trees, timestamps, chains, renewal, algorithms, policies, and XML
  canonicalization boundary;
- bounded depth/count/work and original-byte signature semantics;
- versioned validation report.

Verification:

- RFC/standard vectors, tree/path substitution, renewal order, algorithm
  migration, malformed ASN.1/XML, canonicalization attacks, and huge records.

Exit criteria:

- archival evidence renewal is complete for the claimed revisions;
- `v0.128.0 implementation stop reached. Run pentest for this exact commit.`

### v0.129.0 - Timestamped Data COSE And ETSI

Status: planned.

Goal: implement timestamped-data bindings, COSE headers, and applicable ETSI profiles.

Deliverables:

- RFC 5544 timestamped-data and RFC 9921 COSE/RFC 3161 binding semantics;
- protected/unprotected header policy and token chains using RFC 9052/9053;
- exact licensed ETSI scope and algorithm policy;
- unknown critical field handling.

Verification:

- RFC/licensed vectors, coverage substitution, duplicate headers, wrong
  countersignature, malformed chains, algorithm downgrade, and interop.

Exit criteria:

- evidence is cryptographically bound to the intended object and context;
- `v0.129.0 implementation stop reached. Run pentest for this exact commit.`

### v0.130.0 - ANSI X9.95 Timestamp Profile

Status: planned.

Goal: implement the legitimately licensed ANSI X9.95 timestamp profile
independently.

Deliverables:

- exact profile revision, messages, policies, algorithms, identities, and
  RFC 3161/CMS relationships;
- profile-specific validation and renewal evidence;
- no Authenticode or OpenTimestamps semantics.

Verification:

- licensed vectors, cross-protocol confusion, digest/nonce/policy mismatch,
  algorithm/revision errors, malformed evidence, and profile interop.

Exit criteria:

- X9.95 retains its exact profile, trust, and renewal semantics;
- `v0.130.0 implementation stop reached. Run pentest for this exact commit.`

### v0.130.1 - Authenticode Timestamp Compatibility

Status: planned.

Goal: implement Authenticode timestamp compatibility independently.

Deliverables:

- exact admitted Authenticode timestamp forms, content binding, signer,
  countersignature, certificate, algorithm, and validation policy;
- legacy/modern form distinction and compatibility-only boundaries;
- no X9.95 or OpenTimestamps semantic reuse.

Verification:

- official/ecosystem vectors, wrong content/signer, countersignature
  substitution, algorithm downgrade, malformed CMS, certificate-time cases,
  and tool interop.

Exit criteria:

- Authenticode compatibility has its own trust and validation report;
- `v0.130.1 implementation stop reached. Run pentest for this exact commit.`

### v0.130.2 - OpenTimestamps

Status: planned.

Goal: implement OpenTimestamps generation and verification independently.

Deliverables:

- exact proof operations, calendar attestations, digest algorithms, upgrade,
  verification, and bounded proof graph;
- calendar identity/equivocation, network, caching, and trust policy;
- no RFC 3161/X9.95/Authenticode authority inference.

Verification:

- public vectors, malformed/deep proofs, digest mismatch, calendar
  equivocation, unavailable/malicious calendars, upgrade/replay, resource
  limits, and ecosystem interop.

Exit criteria:

- OpenTimestamps proofs retain calendar, operation, and trust provenance;
- `v0.130.2 implementation stop reached. Run pentest for this exact commit.`

### v0.131.0 - Evidence Chain Policy

Status: planned.

Goal: unify verification and archival-renewal policy without erasing formats.

Deliverables:

- authority/time/algorithm/revocation/renewal policy;
- evidence interval, provenance, validation level, and non-forgeable result;
- mixed-chain and long-term algorithm migration.

Verification:

- mixed authorities/formats, expired/revoked chains, weak algorithm cutoffs,
  renewal gaps, conflicting tokens, and deterministic reports.

Exit criteria:

- “valid evidence” always names policy, time interval, and trust basis;
- `v0.131.0 implementation stop reached. Run pentest for this exact commit.`

### v0.132.0 - Timestamp Evidence Security Gate

Status: planned.

Goal: audit timestamp authorities, evidence chains, dependencies, and formats.

Deliverables:

- complete clause/conformance matrix and algorithm inventory;
- signature/DER/XML/resource/renewal security review;
- resolved critical/high findings and interoperability report.

Verification:

- official vectors, independent TSAs/tools, fuzzing, adversarial chains,
  cargo evidence, and focused pentest.

Exit criteria:

- trusted evidence is production-candidate quality independently of clock sync;
- `v0.132.0 implementation stop reached. Run pentest for this exact commit.`

## Phase 11: Consensus Servos Facade And Applications

### v0.133.0 - Cross-Protocol Consensus Orchestration

Status: planned.

Goal: orchestrate validated observations from different protocol families
through the already reviewed generic quorum and diversity algorithms.

Deliverables:

- normalization and uncertainty expansion feeding the existing
  `v0.60.0`–`v0.61.0` engine quorum/condition-assessment/clustering/combining
  primitives, including `v0.60.6` policy acceptance, with no second
  intersection, assessment/admission, falseticker, clustering, or combining
  implementation;
- cross-protocol correlation groups, supported interval,
  authentication/diversity policy, split-brain, and evidence;
- exact conversion-context/model generation on every normalized input;
  mixed generations are rejected or explicitly re-normalized before quorum;
- generic upsert/withdraw/discontinuity consumption with withdrawal
  propagation, condition reassessment, accepted-bound invalidation, and
  recomputation before any later servo action;
- hard bounds remain distinct from statistical estimates/covariance and may
  mix only through an explicit reviewed conversion policy;
- explicit `n` admitted sources, maximum faulty diversity groups `f`, required
  overlap, freshness/path-delay bounds, network-adversary scope, and
  the exact `v0.7.2` threshold/fault condition, contributing atom/condition
  identities, proof rule, and canonical `BoundAssumptionsId` in every result;
  orchestration consumes the engine derivation report and never reconstructs
  assumptions from prose or source metadata;
- synchronized/servo-eligible consensus output carries a current
  `PolicyAcceptedHardBound`, exact verified-derivation and assessment
  generations, and unmodified per-atom `SupportBasis`; conditional,
  indeterminate, expired, withdrawn, policy-rejected, or unverified-derivation
  results remain diagnostic and have no servo or clock-publication authority;
- orchestration preserves the exact `ConsensusAuthorityId`, canonical bounded
  `ProofSupportSet`, single `AuthorityValidity` domain, and every admitted
  monotonic-correlation dependency produced by the generic engine, including
  verified offset/rate/drift derivations, conditions/assessments/support bases,
  capture anchors, and independently checked endpoint validity. It cannot
  replace used contributors with unused survivors or recompute only a deadline
  while retaining the old authority identity;
- multi-root orchestration claiming one admitted source set consumes the exact
  `v0.60.4` `CompleteBatchVerification` membership witness. Aborted batches,
  successful prefixes, and caller-filtered result iterators cannot silently
  shrink `n`, remove a failed member, or enter consensus as a complete set.
  Only current accepted-bound members contribute intervals/votes; all other
  processed `CompleteMemberStatus` values remain visible non-contributors, and
  shortage returns `Insufficient`/`Unsafe` until an atomic new membership
  generation is fully reassessed. `AbortMemberDiagnostic`, including
  `Unprocessed`, is refused before orchestration;
- operator/upstream/ASN/path/grandmaster/receiver/oscillator/site correlation
  claims with assertion provenance, configured/measured/authenticated/inferred/
  unknown assurance, expiry, and generation;
- conservative correlation for unknown/untrusted diversity and policy that
  prevents custom providers from self-declaring arbitrary independence;
- typed `ConsensusPolicyId`/`ConsensusPolicyGeneration` and source-membership
  generation covering `n`, `f`, admitted sources, correlation, weighting,
  freshness, path-delay, and authentication rules;
- atomic policy/membership replacement, invalidation of pending or completed
  results from stale generations, and exact policy/membership generations in
  every result and downstream proposal;
- weights that cannot override the fault quorum;
- bounded sources and stable result ordering;
- no clock change authority.

Verification:

- NTP/NTS/Roughtime/PTP/generic-external/radio mixed simulations, Byzantine
  coalitions and malicious majorities, Sybil/correlation cases, impossible
  guarantees, forged diversity, unknown correlation, common upstreams,
  partitions, stale/mixed-generation sources, withdrawal under queue pressure,
  hard/statistical mixing attempts, assumption loss/substitution/conflicting
  generations/expression exhaustion, incorrect conjunct-all/threshold formulas,
  assessment status/deadline changes and stale accepted-bound tokens,
  policy/membership reload during
  withdrawals, in-flight crypto, pending servo proposals, and helper
  authorization, stale-result rejection, atomic replacement, and interval
  properties; aborted-batch and caller-filtered successful-prefix attempts
  cannot shrink the admitted source set. One-below/at/above threshold matrices
  cover every non-contributor status, duplicate/correlated memberships, and
  atomic membership-generation replacement; separate type-state tests reject
  every aborted/unprocessed outcome. Cross-family cases also cover same-domain
  minimum validity, mixed-domain rejection/translation, forged correlation
  proof/anchor, either endpoint-validity expiry/reset, circular validity,
  used-support withdrawal while an alternative quorum remains, and mandatory
  new-authority recomputation. Navheim is represented only by protocol-neutral
  fixtures here.

Exit criteria:

- cross-protocol consensus reports synchronized, rough, split, insufficient,
  or unsafe explicitly;
- `v0.133.0 implementation stop reached. Run pentest for this exact commit.`

### v0.134.0 - Bounded PLL Servo

Status: planned.

Goal: implement one bounded fixed-point phase-locked-loop servo.

Deliverables:

- PLL phase/frequency state and proposal output;
- interval-valued input, saturating anti-windup control, phase/frequency
  limits, panic thresholds, startup/recovery, and generation-aware reset;
- hard-bound servo input requires the current `v0.60.6`
  `PolicyAcceptedHardBound`; verified-derivation or assessment
  loss/expiry/withdrawal invalidates the input and resets or faults accumulated
  state before another proposal;
- hard/statistical uncertainty kept distinct and explicit target capability;
- withdrawals and discontinuities reset or invalidate state before new output.

Verification:

- analytical PLL traces, drift/noise/step/loss simulations, saturation,
  numerical stability, mixed uncertainty, assessment loss/stale accepted
  token, withdrawal/discontinuity,
  reference implementation comparison, and property tests.

Exit criteria:

- servos cannot issue out-of-policy adjustments;
- `v0.134.0 implementation stop reached. Run pentest for this exact commit.`

### v0.134.1 - Bounded FLL Servo

Status: planned.

Goal: implement one bounded fixed-point frequency-locked-loop servo.

Deliverables:

- FLL frequency estimation and proposal output over explicit sample intervals;
- saturation, frequency/aging limits, startup/recovery, target generation,
  accepted-bound verified-derivation/assessment generations, withdrawal, and
  discontinuity behavior;
- error-budget and hard/statistical uncertainty preservation.

Verification:

- analytical frequency traces, irregular/lost samples, drift, steps,
  saturation, numerical extremes, generation changes, withdrawal,
  assessment expiry/stale token, reference comparison, and properties.

Exit criteria:

- FLL behavior is independently reviewable and cannot bypass adjustment
  policy;
- `v0.134.1 implementation stop reached. Run pentest for this exact commit.`

### v0.134.2 - Hybrid Servo Selection

Status: planned.

Goal: combine admitted PLL and FLL behavior through an explicit bounded mode
policy rather than a second hidden implementation.

Deliverables:

- typed PLL/FLL/hybrid modes, transition conditions, hysteresis, state
  transfer, and evidence;
- startup, recovery, source-quality, holdover-entry, generation, and
  discontinuity transitions;
- no implicit statistical-to-hard uncertainty conversion.

Verification:

- every transition edge, chatter resistance, delayed/lost samples, source
  replacement, withdrawal, discontinuity, numerical boundaries, and long
  simulator/reference traces.

Exit criteria:

- hybrid behavior is a visible policy over reviewed PLL/FLL engines;
- `v0.134.2 implementation stop reached. Run pentest for this exact commit.`

### v0.134.3 - Step Slew And Discipline Proposal Policy

Status: planned.

Goal: convert servo estimates into bounded discipline proposals without
granting adjustment authority.

Deliverables:

- typed step/slew/rate proposals, thresholds, maximum correction, backward and
  post-startup step policy, target identity/generation, and expiry;
- each proposal binds the exact current `PolicyAcceptedHardBound` and condition-
  assessment and verified-derivation generations; derivation or assessment
  loss invalidates the proposal before authorization or actuation;
- requested versus predicted applied/residual values and saturation evidence,
  clearly labeled as prediction until actual feedback arrives;
- proposal-only engine output consumed by `mundilfari-discipline`;
- invalidation when input, target, authorization, or correlation generations
  change.

Verification:

- threshold boundaries, backward/post-startup refusal, saturation, stale
  generation/accepted-bound token, revoked authority, condition-assessment
  loss, impossible target capability, withdrawal, discontinuity, and proposal
  replay.

Exit criteria:

- engine policy can propose but never directly apply a clock change;
- `v0.134.3 implementation stop reached. Run pentest for this exact commit.`

### v0.134.4 - Actuation Feedback And Servo Anti-Windup

Status: planned.

Goal: close the protocol-neutral control loop using what the target actually
applied rather than continuing from proposal predictions.

Deliverables:

- an `ActuationFeedback` event carrying proposal identity/generation,
  requested and actually applied correction, quantization, clamping, partial
  application, rejection, residual, actuation/observation timestamps, target
  generation, and discontinuity state;
- authenticated correlation of `AppliedAdjustment` to exactly one proposal
  and target generation, with duplicate/stale/forged feedback rejected;
- PLL, FLL, hybrid, and discipline-proposal state consuming feedback before
  further integration, with anti-windup/reset behavior for saturation,
  rejection, partial application, delayed feedback, and discontinuity;
- `v0.39.2` ownership loss or externally observed phase/rate change treated as
  discontinuous competing actuation, invalidating feedback correlation and
  forcing reacquisition rather than being integrated as oscillator error;
- bounded missing-feedback timeout and degraded/faulted outcomes;
- persistence/audit representation through the common schema without granting
  the engine adjustment authority.

Verification:

- exact, quantized, clamped, partial, rejected, delayed, duplicate, missing,
  reordered, wrong-proposal, wrong-target-generation, and discontinuous
  feedback traces; external/competing adjustment and lease-loss schedules,
  repeated saturation, integrator-windup adversarial cases, actuator mock
  faults, and closed-loop analytical/simulator comparison.

Exit criteria:

- no servo integrates an assumed adjustment after actual actuation evidence is
  available or required;
- `v0.134.4 implementation stop reached. Run pentest for this exact commit.`

### v0.135.0 - Precision Kalman-Style Estimator

Status: planned.

Goal: implement high-rate phase/frequency estimation for precision clocks.

Deliverables:

- bounded fixed-point estimator consuming generic precision observations,
  including but not coupled to PTP;
- actuation feedback, saturation, residual, and target-generation changes
  consumed before prediction/update continues;
- covariance as model-derived statistical uncertainty carrying confidence,
  units, model identity/generation, outlier, delay/asymmetry, and reset
  behavior;
- no conversion of covariance into hard earliest/latest bounds without a
  named policy and documented assumptions;
- any policy conversion to a hard bound must obtain a fresh
  `PolicyAcceptedHardBound`; derivation or assessment loss resets or downgrades
  estimator output before it can feed a servo;
- no floating-point requirement in no_std core.

Verification:

- recorded PHC traces, simulated oscillator/noise models, numerical extremes,
  covariance/confidence semantics, hard-bound conversion rejection/policies,
  accepted-condition expiry/rejection, convergence, withdrawal/discontinuity,
  malicious delay, and independent estimator comparison.

Exit criteria:

- estimator uncertainty grows honestly when assumptions fail;
- `v0.135.0 implementation stop reached. Run pentest for this exact commit.`

### v0.136.0 - Holdover Models

Status: planned.

Goal: implement oscillator holdover and uncertainty growth.

Deliverables:

- age/frequency/stability/temperature/aging observation model with measured
  Allan-deviation and calibration-age inputs;
- configurable oscillator classes and conservative fallback;
- source loss/recovery/withdrawal/discontinuity state and persisted calibration
  provenance through the common secure persistence boundary;
- calibration, oscillator, temperature, aging, and source-availability
  condition atoms are reassessed during holdover; expired/withdrawn/
  indeterminate assumptions or invalidated observation/model derivations
  invalidate any accepted hard bound and force conservative conditional/
  statistical output or fault according to policy;
- systematic/random and measured/asserted error components retained; model
  prediction covariance never presented as a guaranteed bound.

Verification:

- long synthetic/hardware traces, temperature ramps, restart, stale model,
  assumption expiry during holdover, stale accepted token, source recovery,
  underreported stability attacks, and saturation.

Exit criteria:

- holdover never reports frozen uncertainty or hidden source loss;
- `v0.136.0 implementation stop reached. Run pentest for this exact commit.`

### v0.137.0 - Trusted Virtual Clock

Status: planned.

Goal: provide a monotonic application clock with civil correlation.

Deliverables:

- synchronized/rough/holdover/ahead/frozen/catching-down/faulted state model,
  with detailed ahead recovery completed at `v0.137.7`;
- `TimeEstimate` with earliest/latest, optional policy-approved preferred
  estimate, scale/realization, resolution, uncertainty, monotonic correlation,
  freshness/holdover age, separate authentication/integrity/traceability,
  leap policy, source generation, canonical `BoundAssumptionsId`/condition,
  current `ConditionAssessment`, optional `PolicyAcceptedHardBound` identity/
  generation/verified-derivation identity/deadline, per-atom `SupportBasis`,
  reasons/non-claims, and warnings;
- synchronized hard-bound status exists only while the accepted-bound token
  revalidates under the current policy/evidence/lifecycle generations;
  conditional or diagnostic estimates remain available without synchronized
  labeling;
- default strict `TrustedClock::now()` is an explicit linearization-time
  contract returning `LinearizedTrustedTime { estimate, observed_at:
  MonotonicReadInterval, valid_until }`. It samples the exact
  `MonotonicClockId` carried by the accepted-bound deadline and requires the
  conservative `observed_at.latest < valid_until`; resolution/quantization,
  measurement latency, and rate uncertainty are included. Authority is claimed
  for that sampled interval/linearization point and the returned deadline, not
  for an unknowably delayed caller-receipt instant;
- optional `TrustedClock::now_through_completion()` requires a current
  `ThroughCompletionCapability { wcet }`, adds the reviewed completion/WCET
  margin to the interval's conservative upper edge, and returns a distinct
  `CompletionBoundTrustedTime`. General-purpose platforms without a hard bound
  report the capability unavailable; they retain linearization-time reads
  rather than overstating scheduler guarantees;
- either strict contract returns typed expired/diagnostic state when its
  required upper edge reaches the deadline, even when no writer, timer,
  invalidation event, or republish operation has run. If the provider cannot
  bound the measurement interval itself, no strict contract compares a scalar
  best-case reading;
- strict authority requires a suspend-inclusive monotonic domain or a platform
  resume signal that invalidates the token before another strict read.
  Monotonic read failure, pause without reliable resume invalidation, domain
  change/reset, or incomparable identity fails closed to diagnostics rather
  than trusting the cached synchronized label;
- monotonic nonrollback preferred application projection with no network I/O,
  distinct truth-seeking interval semantics, plus explicit UTC/POSIX
  conversion context and policy;
- common secure persistence and restart bootstrap boundary;
- one logically consistent instant/uncertainty/scale-model/source-set/
  generation snapshot contract, with the concurrent publication mechanism
  completed in `v0.137.5`.

Verification:

- single-reader logical snapshot/state-model tests, clock rollback, system
  step, suspend/restart, leap/smear, holdover, split-brain, accepted-assessment
  expiry/withdrawal/stale token, conditional-not-synchronized refusal, and
  monotonicity properties; exact-deadline refusal, idle expiry without a
  writer, timer starvation, suspend/resume for both monotonic-domain profiles,
  coarse resolution, read interval straddling expiry, sampling latency spikes,
  rate uncertainty, `observed_at`/`valid_until` reporting, delayed caller
  receipt without a false through-return claim, unavailable/expired/violated
  WCET capability, completion-margin boundaries, monotonic read failure/reset/
  domain mismatch, and fail-closed diagnostics;
  multi-reader publication/interleavings remain `v0.137.5`.

Exit criteria:

- applications can read trusted time without a network request per event;
- `v0.137.0 implementation stop reached. Run pentest for this exact commit.`

### v0.137.1 - Trusted Snapshot Identity And Atomic Publication

Status: planned.

Goal: define the immutable trusted-snapshot identity and atomic publication
preconditions before adding concurrent refresh machinery.

Deliverables:

- documented memory-ordering/publication model for one internally consistent
  snapshot across instant, hard/statistical uncertainty, scale/context model,
  source set, canonical bound condition, current assessment, accepted-bound
  identity/deadline, synchronized status, validity, and generation;
- synchronized hard-bound publication accepts only a current
  `PolicyAcceptedHardBound`; immediately before commit it atomically rechecks
  the verified derivation, condition/assessment identity, evidence, policy,
  membership, source, correlation, lifecycle and monotonic-domain generations,
  per-atom support basis, status, and conservative deadline. Conditional
  estimates publish only with explicit diagnostic/non-synchronized state;
- a synchronized snapshot has a distinct
  `PublishedAuthoritySnapshotId` and binds the exact current
  `ConsensusAuthorityId`, its complete `ProofSupportSet`, and every transitive
  validity/correlation generation. Publication never upgrades the batch
  witness itself into authority and never substitutes an unused contributor
  into the consensus proof;
- published validity remains in one explicit strict-read monotonic domain. If
  the consensus authority domain differs, commit requires a current
  `AdmittedMonotonicDomainCorrelation`, conservatively translates the deadline
  to the target interval's earliest edge with outward rounding, takes the
  minimum of all publication dependencies, and binds that correlation
  identity/generation, verified numerical derivations, condition/assessment/
  support bases, capture anchors, independent endpoint validity, provider/
  lifecycle/expiry into the snapshot. Publication independently rechecks both
  endpoint deadlines and never uses the correlation to validate itself.
  Publication also rejects any numerical derivation, condition assessment, or
  support leaf transitively backed by an admitted or historical correlation,
  including a reference restored after replacement. Otherwise publication
  fails typed; raw cross-domain comparison is forbidden;

Verification:

- accepted/raw type confusion, snapshot/consensus/batch identity substitution,
  proof-support replacement, same- and mixed-domain validity, exact earliest-
  edge translation, correlation proof/condition/anchor/endpoint substitution,
  and atomic precommit generation/deadline recheck.

Exit criteria:

- one immutable published snapshot binds a complete current authority and
  cannot mix fields or dependencies from distinct logical generations;
- `v0.137.1 implementation stop reached. Run pentest for this exact commit.`

### v0.137.2 - Concurrent Refresh Publication Linearization

Status: planned.

Goal: publish complete refresh replacements with bounded readers and fenced
writers under arbitrary post-sample preemption.

Deliverables:

- concurrent batch refresh publishes a new `CompleteBatchVerification` and
  retires the prior batch/snapshot at one linearization point after rechecking
  both generation vectors. A non-invalidating cancellation, capacity, or
  transient-work abort retains an older still-current snapshot unchanged and
  reports `Retained`; genuine withdrawal, expiry, or policy/membership/
  evidence/lifecycle change publishes its invalidation even when replacement
  fails and reports `Invalidated`. No prior state reports `Absent` as retained,
  and no reader observes a replacement prefix. The published
  `PriorStateObservation` names the exact tagged
  `PublishedAuthoritySnapshot` subject, prior identity/generation,
  `LinearizationObservationStamp`, unchanged exact-domain deadline or
  invalidation generation/reason, engine generation, and this commit's
  publication generation. A batch or consensus subject cannot substitute for
  the published subject;
- concurrent publication implements both `v0.60.5` refresh profiles.
  `LinearizationRefresh` is required on general hosted platforms: a versioned
  reservation hides the in-progress generation, the exact-domain monotonic
  sample is the logical publication point, and arbitrary post-sample
  preemption is permitted. Readers encountering the reservation boundedly
  retry or return `RefreshInProgress`; after immutable physical installation
  they revalidate the snapshot's complete dependency vector and deadline at
  their own strict-read point. Thus an already-expired historical snapshot may
  be delivered but can never return synchronized authority. Reservation
  generation and invalidation watermark prevent a delayed writer from
  overwriting any newer publication/invalidation;
- concurrent publication owns the atomic `RefreshInvalidationWatermark` and
  `RefreshFencingGeneration` storage plus `RefreshReservationGuard` install/
  tombstone/supersession operations. Every invalidating dependency update
  advances the watermark in the same ordered mutation that makes its new
  generation visible. Only explicit cancellation/guard tombstone or owner/
  process/session invalidation permits a higher-fence writer to supersede;
  elapsed time alone never does. Superseded writers publish nothing and return
  `SupersededNoInstall`;
- each guard owns one preallocated reservation slot whose
  `Vacant`/`Live`/`Tombstone`/`SupersededTombstone` transition occurs in place.
  Cleanup consumes no secondary tombstone capacity and is bounded,
  allocation-free, callback-free, nonblocking, and non-panicking, including
  during unwind. Cleanup after higher-fence supersession is a successful fenced
  no-op; an impossible transition latches the engine fault and irrevocably
  disables old-writer installation. Slot saturation rejects acquisition, never
  cleanup;
- optional `CommitCoveredRefresh` expands the sample's latest edge by a current
  reviewed remaining-work capability covering checks, writes, swap,
  preemption/critical-section allowance, and observation-record publication,
  then physically commits within that bound and before `valid_until`. Missing/
  stale capability disables only this stronger profile. Sample/domain/
  reservation failure produces `Unavailable`; no unavailable profile reports
  `Retained` or installs an admission/authority record, while ordered
  invalidation tombstones remain fail-safe;
- every concurrent linearization-time strict read obtains one logical snapshot
  and exact-domain `MonotonicReadInterval`, validates
  `observed_at.latest < valid_until`, and returns both values from the same
  logical generation. Through-completion reads additionally snapshot/recheck
  the exact current WCET capability/generation and require
  `latest + wcet < valid_until`; unavailable or stale capability cannot affect
  the linearization-time API;
- a sample that may straddle expiry, reset/domain mismatch, unavailable suspend
  coverage/resume invalidation, unbounded measurement interval, or monotonic
  failure returns expired/diagnostic state without waiting for a writer.
  The documented read linearization/order prevents a cached pre-expiry label
  from surviving expiry or being paired with another publication generation;

Verification:

- retained/invalidated/absent replacement interleavings, every watermark
  mutation, arbitrary post-sample preemption, in-place guard cleanup and fault
  fallback, supersession/restart/reclamation/fence exhaustion, bounded reader
  retry, exact deadline straddling, and `CommitCoveredRefresh` capability and
  margin edges.

Exit criteria:

- readers see current, in-progress, or typed-fault state within a bound, and no
  delayed or failed writer can overwrite a newer publication or invalidation;
- `v0.137.2 implementation stop reached. Run pentest for this exact commit.`

### v0.137.3 - Multi-Component Admitted State Publication

Status: planned.

Goal: atomically publish leap, EOP, scale-offset, conversion-context, and clock
state only from their matching current engine admission proofs.

Deliverables:

- concurrent publication consumes only an engine-issued
  `AdmittedLeapCandidate`; immediately before commit it atomically rechecks
  candidate/evidence/authority/policy/membership/decision generations, expiry
  in its exact monotonic domain, replacement/withdrawal state, and its bound
  condition's current `v0.60.6` policy acceptance;
- EOP and external scale-offset publication accepts only the matching
  `v0.52.3` opaque `AdmittedEopSnapshot` or
  `AdmittedScaleOffsetSnapshot` proof and atomically rechecks every bound
  content/source/configured-authority/retrieval-claim/artifact-integrity-or-
  configured-platform-trust/assurance-basis/verifier-provider/policy/validity/
  expiry/rollback/conversion-generation/withdrawal field at the same commit
  boundary;
- withdrawal, expiry, policy or membership reload, evidence-generation change,
  condition-assessment loss, source/correlation change, accepted-bound expiry,
  or candidate replacement between admission and commit invalidates the
  transaction; generation comparison and commit share one linearized
  publication boundary rather than a caller-controlled check-then-act gap;
- assessment invalidation uses the reserved generic lifecycle path and removes
  synchronized authority from consensus, servo/estimator/holdover state,
  pending discipline proposals, and the clock snapshot in the same ordered
  dependency update; stale accepted tokens cannot survive queue pressure;
- leap tables, EOP, external scale-offset data, conversion-context generation,
  UTC result, and dependent clock snapshot become visible as one internally
  consistent transition; no reader observes mixed component generations;
- raw `LeapModelCandidate` or expert core replacement can never update
  `TrustedClock` or the default facade without `AdmittedLeapCandidate`; raw EOP
  or scale-offset data is likewise rejected without its typed admitted proof;
- clarifies that `v0.12.1` atomicity was only a single-thread transactional
  generation replacement, while this milestone supplies concurrent-reader
  visibility and ordering;

Verification:

- old/new/raw/admitted leap, EOP, and scale-offset proofs; retrieval, integrity,
  platform-trust, authority, policy, rollback, withdrawal, expiry, conversion-
  context, and clock-snapshot substitutions at every precommit boundary; no
  reader observes mixed component generations.

Exit criteria:

- concurrent publication cannot bypass an engine admission proof or expose a
  partially replaced time-data and clock state;
- `v0.137.3 implementation stop reached. Run pentest for this exact commit.`

### v0.137.4 - Hosted Publication Concurrency Engineering

Status: planned.

Goal: bound hosted publication synchronization, callbacks, queues, memory
ordering, retries, placement assumptions, and reader latency.

Deliverables:

- explicit `Send`/`Sync` policy for every public engine/provider type;
- bounded queues and cancellation/invalidation ordering with withdrawals
  reserved from silent loss;
- no lock held while calling user transport, crypto, persistence, provider, or
  audit callbacks;
- documented read guarantee: lock-free, wait-free, or bounded locking, with
  maximum read-latency and PHC cross-timestamp benchmark targets;
- documented cache-line layout/false-sharing controls, bounded reader retry
  count and failure outcome, CPU migration assumptions/detection, and
  per-core/socket/NUMA placement conditions for every HFT-oriented claim.

Verification:

- Loom/Shuttle models for ordering, queue/cancellation/invalidation, callback
  re-entry, bounded retry, migration, false sharing, contention, starvation,
  and per-core/cross-core/cross-NUMA latency limits.

Exit criteria:

- hosted concurrency has explicit memory-ordering, callback, progress, and
  latency contracts with bounded failure outcomes;
- `v0.137.4 implementation stop reached. Run pentest for this exact commit.`

### v0.137.5 - Concurrent Publication Security Gate

Status: planned.

Goal: integrate the trusted snapshot, refresh linearization, admitted component
publication, and hosted concurrency contracts under adversarial schedules.

Deliverables:

- one bounded integration surface covering `v0.137.1` through `v0.137.4`
  without weakening any identity, admission, validity, progress, or
  invalidation rule.

Verification:

- Loom/Shuttle-style repository-only model tests for publication,
  invalidation, fencing/watermarks/reservation guards/tombstone reclamation,
  queues, cancellation, persistence swap, and helper IPC state;
- old/new admitted/raw leap candidate, EOP and scale-offset component proof,
  evidence/policy/membership/conversion generation, retrieval claim, artifact-
  integrity or configured-platform-trust assurance, verifier/provider versus
  source authority, expiry, rollback, withdrawal, conversion context, UTC
  result, and clock snapshot interleavings across verification/admission/
  recheck/commit/publication;
- supported-to-contradicted/indeterminate/expired/withdrawn assessment,
  source/correlation/policy/membership generation, assessment deadline, stale
  `PolicyAcceptedHardBound`, servo/proposal invalidation, and synchronized-to-
  diagnostic snapshot interleavings across assessment/recheck/commit;
- old/new complete-batch refresh interleavings cover cancellation, capacity/
  work abort, genuine invalidation, prior absence, deadline crossing, commit,
  and retirement. Readers observe exactly retained-old, invalidated/diagnostic,
  or complete-new state with the matching
  `PriorStateObservation`, never a mixed or partial replacement;
- snapshot-subject tests reject batch/consensus identity confusion; support-
  dependency schedules expire or withdraw every used contributor and
  correlation in turn, including the case where an unused alternative quorum
  remains. Mixed-domain publication either translates through the exact
  admitted correlation or fails without publication;
- admitted-correlation publication schedules substitute numerical proofs,
  conditions, assessments, support bases, capture anchors, endpoint deadlines,
  and provider/lifecycle generations one at a time; either endpoint reset/
  expiry or circular self-validation prevents synchronized publication.
  Two-node and longer numerical-proof/support cycles, replacement-generation
  cycles, and restored historical references likewise prevent publication;
- preemption is injected after every post-sample step and at the exact
  remaining-work/deadline margin for `CommitCoveredRefresh`. Separate
  `LinearizationRefresh` schedules inject unbounded preemption immediately
  after the logical sample, guard cancellation/drop/unwind, reservation
  abandonment, every watermark-advancing invalidation and newer
  publication during delay, delayed historical install/receipt, reader retry
  exhaustion, higher-fence supersession/`SupersededNoInstall`, process/session
  restart, in-place tombstoning at full slot capacity, already-superseded
  cleanup, impossible-transition fault latching, bounded tombstone reclamation/
  exhaustion, and strict-read expiry/revalidation. Cleanup instrumentation
  rejects allocation, callbacks, blocking, or panic. Timeout-only theft is
  refused. Capability absence leaves
  this hosted profile functional. Monotonic sample failure, no comparable
  domain, or reservation failure proves
  `LinearizationObservationStamp::Unavailable` can accompany absence or known
  invalidation but never retention or a new admission/authority record;
- delayed-reader and delayed-return schedules prove the disposition describes
  only its recorded publication linearization interval: a retained prior may
  expire or invalidate immediately afterward, and no caller may use the report
  itself as current or through-receipt authority;
- verified-derivation replacement/invalidation and exact-deadline, idle-expiry,
  timer-starvation, suspend/resume, coarse/straddling monotonic intervals,
  latency/rate-uncertainty spikes, observed-at/deadline pairing, delayed caller
  receipt, WCET-capability issue/reload/withdrawal/violation and completion-
  margin boundaries, monotonic failure/reset/domain-change interleavings across
  snapshot selection, monotonic sampling, deadline check, writer commit, and
  both strict return contracts;
- stress tests for readers/writers, generation consistency, callback reentry,
  starvation, suspend/reset, forced CPU migration, cache-line contention,
  retry exhaustion, and per-core/cross-core/cross-NUMA HFT-oriented maximum/
  p99 latency benchmarks.

Exit criteria:

- no reader can observe fields from different logical clock generations;
- `v0.137.5 implementation stop reached. Run pentest for this exact commit.`

### v0.137.6 - no_std Concurrency Profiles

Status: planned.

Goal: publish observations and trusted-clock state on bare-metal targets
without assuming hosted atomics or hiding unbounded locks.

Deliverables:

- explicit mutually exclusive profiles: single-thread-only, target-atomic,
  caller-supplied critical section, and ISR-safe producer/consumer where
  supported;
- `target_has_atomic` width/capability gating and compile-time refusal when a
  selected atomic profile cannot represent required publication state;
- typed caller critical-section contract with maximum hold/disable time,
  nesting/reentrancy, memory-ordering, and priority rules;
- caller-provided monotonic `read_interval()` is mandatory for strict reads;
  optional through-completion capability binds the profile, critical-section/
  ISR path, target/build identity, WCET evidence, and generation and is absent
  unless the complete read path has a reviewed bound;
- each concurrency profile documents whether and how it supplies the
  nonwrapping reservation/version, invalidation watermark, bounded reader
  retry/failure, and abandoned-reservation recovery required by
  `LinearizationRefresh`. `CommitCoveredRefresh` is exposed only when that
  profile additionally proves the complete remaining path; inability to make
  this stronger claim never disables a sound linearization-only profile;
- bounded ISR queues, producer/consumer ownership, overflow/invalidation
  behavior, and prohibition on allocation/blocking/user callbacks in ISR
  paths;
- no silent emulation of unavailable atomics by an unbounded spinlock, mutex,
  interrupt mask, or critical section;
- capability report and `Send`/`Sync` policy per profile.

Verification:

- representative no-atomic and atomic-width targets, compile-fail feature
  combinations, interrupt/preemption schedules, nested/reentrant critical
  sections, queue saturation with reserved withdrawal capacity, priority
  inversion, memory-order model tests, interrupt-latency/stack/WCET
  measurement, monotonic interval provider absence/refusal, WCET-capability
  generation/withdrawal/violation, unbounded post-sample preemption,
  reservation abandonment/ABA/supersession, bounded reader retry, delayed
  historical install and strict revalidation, and target hardware/simulator
  fixtures.

Exit criteria:

- every `no_std` concurrency claim names its atomic/critical-section/ISR model
  and bounded timing behavior;
- `v0.137.6 implementation stop reached. Run pentest for this exact commit.`

### v0.137.7 - Honest Virtual Clock Ahead Recovery

Status: planned.

Goal: recover when a previously accepted application-clock projection is
discovered to be too far ahead without labeling known-false time synchronized.

Deliverables:

- nondecreasing semantics apply only to the preferred application projection;
  hard earliest/latest truth bounds may revise backward with evidence;
- explicit `Ahead`, `Frozen`, `CatchingDown`, and `Faulted` states plus
  configured maximum divergence, catch-down rate/duration, and transition
  evidence;
- preferred estimate removed whenever it lies outside the current honest
  interval; synchronized status is unavailable during unresolved divergence;
- condition-assessment loss or accepted-bound invalidation removes synchronized
  status independently of preferred-projection monotonicity and exposes the
  conditional diagnostic estimate;
- separate `estimate_now()` truth-seeking interval API with no monotonic
  projection promise;
- policy for freeze versus bounded catch-down versus fault, with no hidden
  backward application projection and no discipline authority;
- generation/withdrawal/persistence/audit handling for detection and recovery.

Verification:

- accepted source far in the future then withdrawn/corrected, hard bounds
  revising backward, preferred estimate outside interval, every state edge,
  assessment contradiction/expiry during ahead recovery, maximum divergence/
  catch-down duration, restart during recovery, repeated corrections, leap/
  smear interaction, concurrent readers, and property tests proving monotonic
  projection never implies false synchronized status.

Exit criteria:

- monotonic application behavior never forces the truth-seeking estimate or
  synchronization label to preserve a known-false future value;
- `v0.137.7 implementation stop reached. Run pentest for this exact commit.`

### v0.138.0 - Easy Blocking APIs

Status: planned.

Goal: expose safe one-shot application APIs.

Deliverables:

- `query_once()` acquisition distinct from `TrustedClock::now()` virtual-clock
  reads, plus strict `TrustedClock::system_defaults(...)`;
- std/alloc builders return a self-contained `TrustedClock` owning engine-
  promoted/frozen claim state and source-arena-independent verified/accepted
  state;
  the returned clock never borrows a locally created derivation arena or uses a
  self-referential/leaked owner. no_std builders instead expose the exact
  caller-storage lifetime in the clock type;
- blocking strict facade keeps the two `v0.137.0` contracts type-distinct:
  `now()` returns linearization-time authority with `observed_at` and
  `valid_until`, while `now_through_completion()` exists/succeeds only with a
  reported current WCET capability and returns the distinct completion-bound
  result; no convenience wrapper relabels one as the other;
- separate explicit result paths:
  strict trusted-time operations return a synchronized hard bound only with a
  current `PolicyAcceptedHardBound`, while conditional/diagnostic operations
  expose the interval, canonical condition, unresolved/unsupported atoms,
  `ConditionAssessment`, expiry/re-evaluation deadline, reasons, assurance,
  exact per-atom `SupportBasis`, verified-derivation status, and non-claims
  without synchronized authority;
- no `is_trusted` boolean, convenience conversion, default unwrap, or preferred
  estimate erases why, under which policy/generations, or until when a bound is
  accepted;
- blocking refresh APIs return `PriorStateObservation` rather than a
  current-authority boolean. The facade exposes its tagged batch/consensus/
  publication subject, `LinearizationObservationStamp::{Measured,
  Unavailable}` plus
  `RefreshCoverageProfile::{LinearizationRefresh, CommitCoveredRefresh}`,
  unchanged exact-domain deadline/invalidation data, and
  engine/publication generation, and requires ordinary current-token
  validation before later use; delayed blocking return cannot upgrade
  historical `Retained` into through-receipt authority, and unavailable
  observation never appears as retained;
- a named, versioned system-defaults policy profile whose report enumerates
  selected sources, trust roots, time-data provider/source/refresh state,
  network actions, fallbacks, platform assumptions, and rejected alternatives;
- local clock, SNTP, NTP, NTS, Roughtime, TIME, and selected source builders;
- facade capability report replacing repository-foundation booleans with
  compiled, available, authorized, and healthy states;
- explicit protocol/security defaults, timeout, endpoint, and report;
- no silent fallback or automatic system-clock change;
- a safe-facade contract returning structured errors rather than panicking for
  malformed caller input, unsupported ranges, insufficient storage,
  unavailable devices, denied privileges, cancellation, or resource
  exhaustion;
- allocator-abort-on-OOM non-claims and internal invariant-bug scope separated
  from recoverable public failures.

Verification:

- compile examples, error ergonomics, feature combinations, local simulators,
  public interop, timeout/cancel, system-policy snapshot/diff, hidden-network/
  fallback refusal, strict refusal for contradicted/indeterminate/expired/
  withdrawn/stale accepted bounds, conditional diagnostic preservation,
  return-from-builder and source-arena-drop self-contained clock tests,
  compile-fail no_std clock lifetime escape,
  delayed hosted return with valid linearization metadata, unavailable/stale/
  violated WCET capability and contract non-substitution,
  refresh observation followed by immediate expiry/invalidation and delayed
  blocking receipt, subject-confusion and unavailable-observation refusal,
  no-trusted-boolean misuse compile tests, and iterator/builder/callback/
  formatting/state-transition panic tests plus whole-facade fuzzing.

Exit criteria:

- common tasks are easy while trust and uncertainty remain visible;
- `v0.138.0 implementation stop reached. Run pentest for this exact commit.`

### v0.139.0 - Poll Future And Async Adapters

Status: planned.

Goal: support runtime-neutral asynchronous use.

Deliverables:

- canonical poll APIs, `core::future` adapters, cancellation, deadlines, and
  user-executor integration;
- optional owned buffers and `v0.7.4` `OwnedHardBoundClaim<T>` state under
  `alloc`; adapters intended for `'static` spawning own every promoted claim,
  engine proof/token, buffer, cancellation, and transport dependency rather
  than extending a borrowed arena lifetime;
- bounded async windows/queues may use `OwnedHardBoundClaimSet<T>` so common
  derivation nodes are shared; queue/root count, retained unique bytes/nodes,
  and work remain explicit, and removal compacts only through the fallible new-
  owner operation;
- cancelling a queued `v0.60.4` verification batch uses its global-abort
  contract: no authoritative prefix escapes through an already-ready future or
  wake race, every member remains diagnosable as `Indeterminate` or
  `Unprocessed`, and only `CompleteBatchVerification` may enter
  full-membership consensus. The future returns the exact prior-state
  disposition; cancellation does not clear a still-current prior batch and
  cannot preserve one invalidated concurrently. Its
  `PriorStateObservation` is historical at its measured linearization
  coverage, preserves the exact tagged subject and unavailable reason, and
  delayed waking/polling/return never turns `Retained` into authority through
  receipt;
- async acquisition performs every transport/provider/callback/fallible action
  before requesting `RefreshReservationGuard`. The final poll that acquires the
  guard contains no await, wake registration, external callback, or operation
  that can return `Poll::Pending`; it must complete with `Poll::Ready` after
  install, typed no-install, or tombstone. Async state cannot store a live guard
  across polls. Future drop before acquisition owns no reservation; unwind/drop
  during the final poll runs the bounded in-place guard tombstone path without
  allocation, callback, blocking, or panic;
- no Tokio or runtime dependency.

Verification:

- custom executor, embedded-style polling, Tokio adapter example outside the
  graph, `'static` spawn with owned claims, compile-fail borrowed-claim spawn,
  multi-root shared queue equivalence/retention/exhaustion, cancellation/drop
  races at pending/wake/ready boundaries with no proof/token or complete-
  witness escape, retained-versus-concurrently-invalidated prior-batch
  outcomes, expiry/invalidation immediately after the observation point,
  unavailable sampling/capability/domain outcomes, arbitrarily delayed result
  polling/receipt, compile/model checks that no `Poll::Pending` or wake
  registration occurs with a live reservation, future drop before acquisition,
  panic/unwind/drop during the final poll, superseded no-install, wake
  discipline, and feature matrix.

Exit criteria:

- async use does not make an executor part of protocol semantics;
- `v0.139.0 implementation stop reached. Run pentest for this exact commit.`

### v0.140.0 - Fixed-Storage Builders

Status: planned.

Goal: complete allocation-free user-facing client/server construction.

Deliverables:

- const capacities, caller buffers, deterministic resource reports, and
  compile-time/runtime capacity errors;
- first-class sizing/builders for the `v0.7.1` derivation arena: node/edge/
  canonical-byte/work capacity, store identity/generation, eviction policy,
  scoped generative-brand creation, mutable/frozen/read-only state, read/write
  lease policy, worst-case claim/handle size, stack usage, generation-
  exhaustion behavior, and fallible bounded alloc-backed alternatives are
  visible rather than hidden inside a client builder;
- explicit borrowed builder families carry caller arena/engine-storage
  lifetimes, while fallible owned builders accept frozen-arena capacity/share
  policy, atomically promote through `v0.7.4`, and return self-contained owners;
- multi-root builders expose maximum roots plus unique/per-root node, edge,
  canonical-byte, and work budgets and report deduplicated storage; individual
  promotion is the one-root specialization of the same canonical path;
- batch-verification builders additionally size membership/result slots,
  canonical-order scratch state, global/per-root generation snapshots,
  unique/per-root work accounting, cancellation checkpoints, and the
  `CompleteMemberStatus`/`AbortMemberDiagnostic` disjoint result buffers,
  `CompleteBatchVerification` witness, and fixed-size
  `PriorStateObservation`; insufficient capacity aborts without a
  proof/token prefix or prior-state mutation;
- engine/fusion builders separately size bounded `BatchAdmissionState`,
  canonical `ProofSupportSet`, correlation numerical derivations/conditions/
  assessments/transitive support bases/capture anchors/independent endpoint
  validity, admitted monotonic-domain correlations, and authority dependency
  vectors. Observation storage always reserves the fixed-size measured/
  unavailable stamp plus refresh-profile evidence. Hosted builders size
  reservation slots whose in-place state includes live/tombstone/superseded
  forms, fencing/watermark generations, owner/cancellation state,
  reader-generation tracking, and reclamation metadata for
  `LinearizationRefresh`; a remaining-work capability is required only when
  enabling `CommitCoveredRefresh`. No separate tombstone capacity is consumed
  by guard cleanup; zero/full capacity affects acquisition only;
- documented allocation behavior per operation for every `alloc` builder;
- representative SNTP/NTP/PTP/generic-external/IRIG examples;
- embedded transport integration guide.

Verification:

- zero/minimum/maximum capacity, stack-size reports, no allocator link,
  derivation-arena DAG sharing/exhaustion/eviction reports, same-storage brand
  recreation, read/write lease and `Send`/`Sync` compile tests, embedded
  targets, examples, and compile-fail overflow cases; allocation/import
  exhaustion, partial-promotion rollback, returned-owner drop order, and
  compile-fail borrowed-result escape; multi-root sharing, duplicate roots,
  removal retention, bounded re-compaction, batch/individual equivalence, and
  zero/minimum/exact/short capacity for every batch membership, result,
  canonical-order, snapshot, accounting, and cancellation-checkpoint buffer;
  compile-fail cross-status construction plus exact size/stack evidence for
  proof-support/correlation proof/anchor/endpoint-validity capacities, zero/
  exact/short reservation-slot/reader-floor capacity, full-slot in-place
  cleanup, already-superseded no-op, impossible-transition fault latch,
  generation exhaustion and bounded reclamation, and both observation-stamp
  variants;
  every prior-observation variant.

Exit criteria:

- Core-tier protocol use is practical and documented;
- `v0.140.0 implementation stop reached. Run pentest for this exact commit.`

### v0.140.1 - Schema Compatibility Freeze And Binding Expansion

Status: planned.

Goal: freeze compatibility for the `v0.22.1` canonical kernel and expand it
across IPC, persistence, bindings, logs, and evidence exchange.

Deliverables:

- compatible extensions for atomic instants, durations,
  hard/statistical uncertainty, scales/models/generations, provenance,
  capability reports, observation events, `CompleteMemberStatus`,
  `AbortMemberDiagnostic`, `AdmissionValidity`, `AuthorityValidity`,
  `PriorStateSubject`, `BatchAdmissionState`, `ConsensusAuthorityId`,
  `UntrustedMonotonicCorrelationCandidate`,
  `AdmittedMonotonicDomainCorrelation` historical-reference metadata,
  canonical bounded
  `ProofSupportSet`, `PublishedAuthoritySnapshotId`, fixed-size
  `PriorStateObservation`/`LinearizationObservationStamp`, refresh coverage
  profile/reservation metadata, and discontinuities;
- schema tags for processed complete-member status and abort-only diagnostics
  are disjoint. `Unprocessed` has no complete-witness encoding, and decode can
  never convert an aborted diagnostic into a quorum-capable value;
- prior-state observations encode an exact tagged admission/authority subject,
  identity/generation, measured interval/domain, exact refresh profile and its
  reservation/version or remaining-work capability generation as applicable,
  or typed unavailable reason, unchanged deadline or typed invalidation
  generation/reason, and engine/optional publication generation as historical
  evidence only; subject tags are non-substitutable and they never deserialize
  as a current accepted token or through-receipt authority claim;
- authority encodings preserve one explicit monotonic domain, the complete
  canonical dependency/support set, conservative aggregate deadline, and any
  admitted correlation identities/generations/uncertainty/expiry. Decoders
  reject mixed-domain raw deadlines, omitted support, and batch/consensus/
  publication identity substitution;
- correlation candidates encode directed domain/generation identities,
  typed offset/rate/drift claim/condition identities and bounded unverified
  derivation records, exact paired capture anchors/pairing generation,
  independent endpoint-validity deadlines, method/provenance, suspend/reset/
  migration/provider/lifecycle metadata, and canonical identity. External
  boundaries can decode only the untrusted candidate or a historical admitted-
  correlation reference with historical assessment/support metadata; no schema
  directly constructs verified correlation derivations, accepted numerical
  claims, or the opaque current engine-admitted type;
- decoded recipe, condition, assessment, and support records cannot regain
  current correlation-proof authority when they contain an admitted/
  historical correlation reference. They remain unresolved historical input,
  and fresh admission rejects every transitive correlation dependency,
  including replacement-generation and longer-cycle attempts;
- reservation/fencing/watermark/tombstone encodings are diagnostic historical
  records only. No persisted/IPC/schema value recreates a live
  `RefreshReservationGuard`, authorizes supersession, or survives process/
  session generation change as a current reservation. Decoding cannot create
  a live/tombstone slot transition or bypass the in-place cleanup state machine;
- every IPC, persistence, C, WASM, log/evidence, and language-binding encoding
  of a bound condition preserves the `v0.7.3` unresolved/resolved type-state;
  identifier-only forms require the exact verified registry generation and no
  binding directly constructs admitted condition identities or hard claims;
- serialized derivations decode only as bounded
  `UnverifiedBoundDerivationRecord`, while assessments/accepted-bound tokens
  decode as historical evidence or unresolved references only; receiving
  engines resolve and completely reverify recipes against current inputs,
  rule registries, models, source/lifecycle generations, and exact `v0.60.6`
  policy/evidence/generation/deadline state before granting authority.
  C/WASM/language bindings cannot construct verified derivations or accepted
  tokens, and the opaque verified type has no direct deserialize path;
- compatibility/freeze ledger proving deterministic field order/encoding,
  bounds, version negotiation, unknown field/criticality rules, canonicality,
  and maximum message sizes retain the early kernel semantics;
- schema owns no serde/Rust-memory-layout semantics and works in `no_std`
  caller buffers;
- explicit compatibility contracts for daemon IPC, secure persistence, C,
  WASM, logs/evidence, and language bindings;
- Java/Kotlin and Swift either use tested JNI/Swift shims or the documented C
  ABI with platform integration/range fixtures;
- external-language opaque contexts own any bounded promoted/frozen arena and
  engine state. Language claim/clock handles retain or borrow that context by
  documented ABI ownership rules, can never contain a Rust arena borrow, and
  cannot outlive or be used after context destruction; schemas never encode
  Rust owner/refcount/brand state.

Verification:

- golden cross-language vectors, noncanonical/duplicate/unknown fields,
  version skew, truncation, integer/range extremes, schema migration,
  deterministic re-encoding, forged/cross-generation assumption identifiers,
  missing/rolled-back registries, forged/stale serialized assessments and
  accepted-bound tokens, derivation replay/rollback/cross-engine copy,
  missing-input/stale-rule-or-model substitution, direct verified-type decode
  refusal, complete-versus-abort tag substitution and forged `Unprocessed`
  complete witness, prior-observation field/variant substitution and
  current-authority misuse, measured/unavailable stamp substitution,
  authority-subject confusion, omitted/reordered support dependencies,
  mixed-domain deadline forgery, forged correlation derivation/anchor/endpoint-
  validity records, live-reservation decode/supersession attempts,
  C/WASM/JNI-or-C/Swift-or-C fixtures, context-first/child-first/
  arbitrary destruction order, double release, use after context close, shared
  frozen-owner threads, allocation/promotion failure without leaked or
  partially initialized handles, and fuzzing.

Exit criteria:

- no external boundary depends on Rust layout or an implicit serializer data
  model;
- `v0.140.1 implementation stop reached. Run pentest for this exact commit.`

### v0.141.0 - Multi-Protocol Server Framework

Status: planned.

Goal: provide bounded shared server orchestration.

Deliverables:

- listener/source/quality/rate/work policy across applicable protocols;
- per-protocol amplification and authentication controls;
- coordinated shutdown and audit events.

Verification:

- mixed-client simulation, global/per-source quotas, slow clients, flood,
  source fault, shutdown/restart, and protocol-isolation tests.

Exit criteria:

- one overloaded protocol cannot starve or weaken another silently;
- `v0.141.0 implementation stop reached. Run pentest for this exact commit.`

### v0.142.0 - Privilege-Separated Daemon

Status: planned.

Goal: implement `mundilfarid` with least-privilege clock discipline.

Deliverables:

- unprivileged workers/consensus, bounded `DisciplineProposal`, policy-issued
  authorization, and a dedicated minimal helper with no protocol dependencies;
- exact consumption of the frozen `v0.39.3` `HelperPolicyCeiling` and
  `DisciplineAuditRecord`/gap types, with no daemon-private policy or audit
  schema;
- pre-opened socketpair/fixed endpoint, OS peer credentials, fixed-version
  maximum-length canonical-schema messages, sequence/typed-monotonic-domain
  expiry/source-generation replay defense, and pre-opened allowlisted clock
  handles;
- proposal authorization binds the current `PolicyAcceptedHardBound`,
  verified-derivation and condition-assessment generations, and conservative
  deadline; the helper tracks the independently authorized minimum current
  generations and rejects stale tokens, while derivation/assessment-loss
  revocation uses reserved ordered control capacity before any later actuation;
- helper-enforced phase/frequency/slew/step bounds, privilege reduction,
  syscall sandboxing, separated raw-capture authority where possible, and an
  append-only accepted/rejected request audit;
- helper-local cumulative phase and frequency budgets per named time window,
  maximum request rate, minimum settling interval, and an independent policy
  ceiling that worker configuration cannot expand;
- helper-generated session nonce, boot/session generation, clock-domain
  identity for monotonic expiries, generic process/machine-instance
  generation, and newly authorized generations for recovery;
- fork/exec/VM/container restore invalidates the helper session and all
  outstanding authorization; inherited/pre-opened handles follow the
  `v0.23.1` lifecycle and close-on-exec/non-inheritance policy;
- fault latching after configured repeated rejected, saturated,
  contradictory, or feedback-missing requests, with bounded fail-closed audit
  behavior when storage is unavailable/full: reserve audit capacity before
  authorization, reject when full, and latch on unexpected post-operation
  audit loss until an explicit gap/recovery record is admitted;
- Linux reference plus supported platform service designs.

Verification:

- IPC fuzzing, peer-credential spoofing, replay/expiry/generation schedules,
  arbitrary path/clock-ID/ioctl/FD refusal, compromised-worker simulation,
  repeated individually valid maximum adjustments, cumulative budget and rate
  boundaries, settling violations, worker policy-expansion attempts, wrong
  session/domain/process/machine generation, fork/checkpoint restore,
  condition-assessment loss before/during authorization, stale accepted-bound
  generation, revocation queue pressure/order, fault-latch/re-authorize
  recovery, audit-full/unavailable, socket/file permissions, restart,
  downgrade, service sandbox, VM clock tests, and soak.

Exit criteria:

- a compromised worker cannot exceed the independently configured discipline
  envelope or issue arbitrary privileged calls;
- `v0.142.0 implementation stop reached. Run pentest for this exact commit.`

### v0.143.0 - CLI

Status: planned.

Goal: deliver query, inspect, compare, decode, convert, serve, and monitor tools.

Deliverables:

- bounded stdin/file/network inputs and machine/human output;
- explicit trust labels, secret redaction, exit codes, and offline modes;
- no clock discipline without an explicit privileged command/policy.

Verification:

- command snapshots, hostile files/terminals, output redaction, pipe failures,
  every protocol sample, platform behavior, and shell completion.

Exit criteria:

- CLI output cannot imply trust or precision absent from the reading;
- `v0.143.0 implementation stop reached. Run pentest for this exact commit.`

### v0.144.0 - C ABI

Status: planned.

Goal: expose stable bounded C interfaces for selected core/protocol APIs.

Deliverables:

- versioned opaque handles, caller buffers, error codes, ownership, threading,
  and panic containment;
- one explicit context owns bounded promoted/frozen claim arenas and engine
  state; child claim/clock handles are reference-counted or context-borrowed by
  the documented ABI contract, Rust arena borrows exist only during individual
  calls, and context close invalidates children before freeing backing storage;
- canonical external-schema values/events with explicit high/low limbs for
  wide instants and
  `OutOfRange` on every narrowing conversion;
- generated header and ABI compatibility policy;
- no unbounded allocation or Rust layout exposure.

Verification:

- C/C++ consumers on Linux/Windows/macOS, canonical golden vectors,
  null/length/alias misuse, ABI layout, symbol version, sanitizer, and fuzz
  tests;
- context/child destruction in every order, double close, concurrent close/use,
  child use after context close, last-owner release, allocation/import
  exhaustion, and no partially returned handle;
- Java/Kotlin JNI-or-C and Swift-or-C ownership/range/platform fixtures for the
  documented binding route.

Exit criteria:

- invalid foreign input cannot unwind across or corrupt the ABI;
- `v0.144.0 implementation stop reached. Run pentest for this exact commit.`

### v0.145.0 - WASM And Browser-Safe APIs

Status: planned.

Goal: expose safe browser-compatible time parsing and evidence verification.

Deliverables:

- core conversions, RFC 3339/IXDTF/TZif, packet inspection, Roughtime and
  timestamp-evidence verification;
- caller-provided fetch/WebSocket/backend transport hooks and a trusted
  application-clock API;
- browser/Node monotonic adapters or caller-provided clocks expose the
  `v0.24.0` interval contract with timer-resolution reduction, event-loop/
  worker delay, background suspension/throttling, navigation/process
  generation, and rate uncertainty; they default to linearization-time or
  diagnostic capability and never claim through-completion WCET from typical
  event-loop latency;
- checked JavaScript integer/date conversion with `OutOfRange` rather than
  truncation, saturation, or panic;
- canonical external-schema encoding/decoding, version, bounds, and
  unknown-field behavior;
- explicit lack of UDP/raw/hardware/clock-control browser capabilities.

Verification:

- wasm32 build, browser/node tests, hostile buffers, JS exception/cancel,
  feature size, coarse/privacy-reduced timers, background throttle/suspend,
  event-loop starvation, worker/process reset, scalar inflation, missing-bound
  diagnostics, and no native dependency leakage.

Exit criteria:

- no proprietary web time protocol is invented for convenience;
- `v0.145.0 implementation stop reached. Run pentest for this exact commit.`

### v0.146.0 - Metrics Health And Audit Records

Status: planned.

Goal: provide bounded operational observability without leaking secrets.

Deliverables:

- source/consensus/servo/holdover/daemon health;
- bounded labels, cardinality, audit schema, redaction, retention, and export
  traits;
- exporters, retention, chaining, sealing, and witnessing extend the frozen
  `v0.39.3` discipline record/gap contract without replacing or reinterpreting
  its fields;
- every audit record carries strict record sequence, explicit gap/loss events,
  monotonic clock identity/domain, TAI estimate interval, scale/model/policy/
  membership/configuration generations, and process/machine instance;
- optional bounded hash/MAC chaining, hardware sealing, or external witnessing
  with exact provider and verification capability;
- `AppendOnly` and `TamperEvident` are distinct capabilities: append-only
  storage is never described as tamper-evident without a verified chain,
  sealed root, or witness;
- append-only discipline-request outcomes and capability states separated into
  compiled, available, authorized, and healthy;
- accuracy/authentication/traceability fields kept separate.

Verification:

- cardinality attacks, secret/cookie/certificate redaction, malformed exporter,
  backpressure, record reorder/duplicate/drop and explicit gap generation,
  monotonic/TAI/model mismatch, chain truncation/fork/rollback/key rotation,
  unavailable witness/storage, append-only versus tamper-evident capability,
  schema compatibility, and incident replay.

Exit criteria:

- observability cannot alter protocol validity or exhaust core state;
- `v0.146.0 implementation stop reached. Run pentest for this exact commit.`

### v0.147.0 - Configuration And Policy Language

Status: planned.

Goal: implement explicit, validated deployment policy.

Deliverables:

- bounded configuration for sources, trust, diversity, protocols, clocks,
  steps/slew, holdover, resources, platform privileges, and logging;
- configuration syntax maps to the existing typed `v0.39.3`
  `HelperPolicyCeiling`; it does not introduce a second helper-policy model;
- configuration identity, provenance, integrity, rollback capability,
  generation, applicable process/machine/target identity, and audit linkage;
- verify/parse → stage → semantic/capability/resource/helper-ceiling validate
  → atomic activate, with old configuration retained on any failure;
- opaque secret-provider/key references only; no inline secret material in the
  canonical configuration value, diagnostics, audit, or dry-run output;
- independent helper-policy ceiling validation that worker configuration
  cannot widen, including cumulative discipline envelope and ownership mode;
- secure defaults, unknown-field rejection, versioning, migration, dry-run,
  withdrawal, and rollback behavior;
- no generic deserialization dependency in protocol cores.

Verification:

- valid/invalid fixtures, unknown/duplicate/conflicting fields, resource
  extremes, identity/provenance/integrity/rollback/generation changes,
  stage-versus-activation races, partial activation refusal, inline-secret
  rejection/redaction, stale secret reference, helper-ceiling expansion,
  downgrade attempts, migration, withdrawal, and property fuzzing.

Exit criteria:

- deployed behavior is reviewable before the daemon changes a clock;
- `v0.147.0 implementation stop reached. Run pentest for this exact commit.`

### v0.148.0 - Navheim-Independent Product Security Gate

Status: planned.

Goal: audit all generic and non-Navheim consensus, servo, facade, daemon,
interface, and operational behavior.

Deliverables:

- API/feature/capability truth review proving Cargo features do not assert
  runtime permission, device presence, source health, or discipline authority;
- privilege, IPC, config, C/WASM, observability, and cross-protocol threat
  reports;
- generic withdrawal, hard/statistical uncertainty, secure persistence,
  exact open/closed/unbounded interval and finite-estimate semantics,
  `CanonicalIdentityV1` domain separation/fixed profile/structural collision
  handling and schema reuse, non-authoritative `BorrowedHardBoundClaim`/
  `OwnedHardBoundClaim` forms with mandatory typed arena handles, bounded
  shared heterogeneous derivation DAG,
  canonical fallible promotion into frozen ownership, no self-reference/
  lifetime extension/storage leaking, multi-root shared-DAG promotion with
  bounded retention/compaction, and source-arena-independent engine proof/token
  state with explicit hosted-owned or no_std inline/checked-engine-store
  representation, one kind-parameterized handle backing its two semantic
  views, complete invalidation generations, and deterministic
  `BatchVerificationOutcome` complete/abort semantics with no authoritative
  prefix, original-`n` membership accounting with accepted-bound-only interval
  contributors, disjoint complete-member versus abort-diagnostic type-state,
  and atomic retained/invalidated/absent prior-state replacement bound to a
  fixed-size measured/unavailable linearization observation rather than caller
  receipt; distinct batch/consensus/publication authority identities,
  exact bounded proof-support sets, one-domain conservative minimum validity,
  untrusted-versus-engine-admitted directed correlation lifecycle and outward-
  rounded earliest-edge deadline translation, proof-bearing offset/rate/drift
  claims with exact anchors/conditions/assessments/transitive support bases and
  independently checked non-circular endpoint validity, initial prohibition of
  all transitive admitted/historical-correlation numerical-proof or condition
  support, admitted dependencies for every translation, used-support
  invalidation despite an available
  alternative quorum, portable version-reserved `LinearizationRefresh` with
  RAII guard/watermark/fencing/in-place non-failing tombstone/restart recovery,
  and optional
  remaining-work-bounded `CommitCoveredRefresh`,
  content-addressed
  `BoundAssumptionsId` bounded `All`/`Any`/threshold/fault-rule semantics
  through consensus, bounded core `UnverifiedBoundDerivation` preservation
  across every root/transforming milestone,
  unresolved-to-resolved external condition type-state plus
  `UnverifiedBoundDerivationRecord`, complete engine
  `VerifiedBoundDerivation`, structured per-atom `SupportBasis` origin/
  integrity/authority/transitive-lineage axes,
  snapshot-consistent runtime `ConditionAssessment` versus opaque
  `PolicyAcceptedHardBound`, reserved derivation/assessment-loss propagation
  through every consensus/control/publication consumer, provider-owned
  monotonic interval contracts across hosted/PHC/architectural/embedded/browser
  adapters, conservative upper-edge issuance/read expiry enforcement,
  linearization-time `observed_at`/`valid_until` authority versus type-distinct
  reviewed-WCET through-completion capability,
  strict-versus-diagnostic facade behavior,
  process/machine lifecycle, monotonic domains, dependency-correct layered
  leap admission with `AdmittedLeapCandidate` precommit revalidation,
  caller-serialized independently trusted time-data ingestion,
  untrusted `RetrievalClaim`, verifier-issued `ArtifactIntegrityEvidence`
  versus distinct `ConfiguredPlatformTrustEvidence`, configured-role
  `AdmittedEopSnapshot`/`AdmittedScaleOffsetSnapshot` proofs, and
  all-component concurrent publication,
  competing discipline ownership, honest ahead recovery, embedded concurrency,
  stable `ServiceCredentialContextId` invalidation without live-clock churn,
  bounded `ResumptionCredentialGeneration`, fresh TLS connection/exporter/NTS
  association generation hierarchy, and layer-correct conservative retention-
  horizon derivation,
  capability-qualified secret memory, concurrent snapshot, canonical external
  schema, frozen helper-policy/discipline-audit semantics, and language-binding
  review;
- resolved critical/high product findings.

Verification:

- full system simulation, platform VM matrix, live sources/hardware subset,
  long holdover/restart/fault tests, and focused pentest.

Exit criteria:

- every Navheim-independent feature is complete and the frozen generic source
  boundary is ready for the final companion phase;
- `v0.148.0 implementation stop reached. Run pentest for this exact commit.`

## Phase 12: Navheim Integration As Final Feature Work

This is the last feature phase. It starts only after Navheim has published and
independently reviewed its complete stable GNSS timing observation/event API.
All generic clocks, source traits, consensus, servos, applications, and
non-Navheim protocols are already implemented before this dependency enters
the workspace.

### v0.149.0 - Navheim Upstream Admission

Status: planned; blocked until Navheim's stable timing release.

Goal: admit one exact stable Navheim release without creating a second GNSS
implementation.

Deliverables:

- license, MSRV, feature, unsafe, maintenance, security, SBOM, and transitive
  dependency review;
- frozen ownership and dependency-direction contract;
- exact mapping inventory for every observation, absence, invalidation,
  discontinuity, health, authentication, integrity, and provenance state.

Verification:

- independently inspect Navheim's stable API and release evidence;
- prove no Mundilfari crate is present in Navheim's graph and no existing
  Mundilfari default graph gains Navheim.

Exit criteria:

- one reviewed Navheim release is approved as the sole GNSS interpretation
  upstream;
- `v0.149.0 implementation stop reached. Run pentest for this exact commit.`

### v0.150.0 - mundilfari-navheim Crate Boundary

Status: planned; blocked on `v0.149.0`.

Goal: establish the optional companion crate and enforce dependency direction.

Deliverables:

- published `mundilfari-navheim` crate with Navheim, core, and engine
  dependencies;
- no default feature from `mundilfari` enables the companion;
- compile-time layer rules preventing Navheim dependencies elsewhere.

Verification:

- default/all-feature Cargo graphs, package dry-run, no_std capability matrix,
  forbidden-edge fixtures, and downstream minimal examples.

Exit criteria:

- users not selecting GNSS carry no Navheim code or transitive dependency;
- `v0.150.0 implementation stop reached. Run pentest for this exact commit.`

### v0.151.0 - Exact GNSS Instant And Scale Mapping

Status: planned.

Goal: map resolved Navheim instants into Mundilfari without truncation or
implicit context.

Deliverables:

- exact native-scale mapping into the already defined canonical TAI
  `AtomicInstant` and generic `v0.12.0` TAI/UTC conversion model, with no
  adapter-local epoch or TAI arithmetic;
- explicit UTC realization, leap-model, rounding, and quantization evidence;
- fail-closed Navheim/Mundilfari scale-model disagreement.

Verification:

- every upstream scale, extreme, leap, rollover result, unknown identifier,
  conversion disagreement, overflow, and round-trip property.

Exit criteria:

- the adapter never decodes or resolves a GNSS week and never invents a UTC
  mapping;
- `v0.151.0 implementation stop reached. Run pentest for this exact commit.`

### v0.152.0 - GNSS Evidence And Observation Mapping

Status: planned.

Goal: preserve complete Navheim evidence in generic Mundilfari observations.

Deliverables:

- asymmetric uncertainty, capture-domain, receiver/source, freshness, and
  provenance mapping;
- separate message correctness, navigation authentication, signal
  authenticity, solution integrity, and clock-authority properties;
- reason-bearing handling for pending, unsupported, ambiguous, stale,
  rejected, and failed values.

Verification:

- exhaustive upstream-state mapping, unknown future states, delayed
  authentication, false-precision attempts, and serialization round trips.

Exit criteria:

- no upstream security state is collapsed into a trusted boolean;
- `v0.152.0 implementation stop reached. Run pentest for this exact commit.`

### v0.153.0 - GNSS Event Lifecycle And Withdrawal

Status: planned.

Goal: map Navheim invalidation and discontinuity into the already complete
generic observation lifecycle from `v0.15.1`.

Deliverables:

- exact artifact/generation/sequence identity mapping into generic
  upsert/withdraw/discontinuity events;
- stale-model, receiver-reset, outage, backward-step, security-transition, and
  replacement handling;
- bounded backpressure that cannot silently drop invalidation.
- no Navheim-specific lifecycle queue, filter, consensus, servo, or virtual
  clock mechanism.

Verification:

- reorder, duplication, omission, queue saturation, delayed invalidation,
  restart, replacement, and stale-consumer adversarial schedules.

Exit criteria:

- formerly accepted GNSS evidence cannot remain usable after Navheim withdraws
  it;
- `v0.153.0 implementation stop reached. Run pentest for this exact commit.`

### v0.154.0 - Generic PPS To Navheim Correlation Bridge

Status: planned.

Goal: combine Mundilfari physical PPS capture with Navheim GNSS semantics.

Deliverables:

- capture-domain/generation, edge, sequence, device error, and capture
  uncertainty handoff;
- mapping of Navheim's represented instant, receiver time mark, convention,
  calibrated delay, and correlation uncertainty;
- pulse-without-time and time-without-pulse states.

Verification:

- reorder/loss/duplication, receiver reset, edge polarity, leap/rollover,
  cable delay, quantization, Linux PPS hardware, and logic-analyzer fixtures.

Exit criteria:

- Mundilfari captures edges but only Navheim assigns their GNSS meaning;
- `v0.154.0 implementation stop reached. Run pentest for this exact commit.`

### v0.155.0 - Navheim Frequency And Time-Transfer Evidence

Status: planned.

Goal: map receiver frequency outputs and GNSS time-transfer evidence.

Deliverables:

- nominal frequency, lock, receiver error, correction, delay, uncertainty, and
  provenance mapping without capture or steering ownership;
- Navheim common-view/all-in-view result mapping;
- generic counter and oscillator interfaces remain Mundilfari-owned.

Verification:

- lock loss, discontinuity, calibration changes, correlated uncertainty,
  missing evidence, replay, and independent laboratory comparison.

Exit criteria:

- receiver frequency evidence never grants oscillator-control authority;
- `v0.155.0 implementation stop reached. Run pentest for this exact commit.`

### v0.156.0 - CGGTTS Interchange

Status: planned.

Goal: implement CGGTTS exchange records over already validated GNSS
time-transfer evidence.

Deliverables:

- exact selected CGGTTS revision, station/equipment identifiers, tracks,
  calibration, delays, uncertainty, and provenance;
- input boundary accepting Navheim common-view/all-in-view results or
  equivalently validated generic evidence;
- no satellite solution, receiver-message, week-resolution, or health
  interpretation.

Verification:

- official/laboratory records, malformed and oversized files, revision
  differences, day rollover, calibration changes, precision retention, and
  independent-tool comparison.

Exit criteria:

- Mundilfari owns only CGGTTS interchange while Navheim owns the GNSS solution
  behind it;
- `v0.156.0 implementation stop reached. Run pentest for this exact commit.`

### v0.157.0 - Navheim Interoperability And Security Gate

Status: planned.

Goal: approve the complete companion and CGGTTS boundary before GNSS may
influence a clock.

Deliverables:

- full stable Navheim event and CGGTTS coverage plus version-compatibility
  report;
- independent scale/leap model disagreement evidence;
- resolved critical/high conversion, invalidation, PPS, CGGTTS, downgrade,
  and dependency-direction findings.

Verification:

- Navheim replay/simulator/receiver and CGGTTS laboratory matrix, all
  companion/CGGTTS fuzz/property suites, no_std/MSRV/feature graphs,
  long-duration timing, hardware PPS, and focused pentest.

Exit criteria:

- GNSS and CGGTTS clock use is evidence-backed without any duplicated GNSS
  decoder;
- `v0.157.0 implementation stop reached. Run pentest for this exact commit.`

## Phase 13: Final Conformance Hardening And Production Admission

No new feature or protocol scope is introduced after `v0.157.0`. Newly
discovered missing stable-baseline work is inserted before this phase.

### v0.158.0 - Official Vector Closure

Status: planned.

Goal: close all official positive/negative vector gaps.

Deliverables:

- registry-to-vector coverage report and legal provenance;
- missing official vectors or documented unavailable status;
- zero unexplained failures.

Verification:

- reproducible complete vector suite and mutation around every official case.

Exit criteria:

- every implemented stable protocol has vector evidence;
- `v0.158.0 implementation stop reached. Run pentest for this exact commit.`

### v0.159.0 - Differential Interoperability Closure

Status: planned.

Goal: complete the independent implementation matrix.

Deliverables:

- NTP/NTS/PTP/Navheim-adapter/timestamp/domain peer versions and exact
  scenarios;
- packet/result comparison and divergence classification;
- remediated security-relevant divergence.

Verification:

- reproducible matrix across supported hosts and hardware where applicable.

Exit criteria:

- no unexplained stable-protocol interoperability divergence remains;
- `v0.159.0 implementation stop reached. Run pentest for this exact commit.`

### v0.160.0 - Parser And Resource Exhaustion Review

Status: planned.

Goal: re-audit every untrusted parser and operation-wide budget.

Deliverables:

- parser inventory, complexity oracle, allocation/work/response limits,
  canonical-schema maximum depth/item counts, iterative/bounded recursion, and
  stable tag/range collision review;
- allocator-failure behavior and abort-on-OOM non-claims for every alloc path,
  proving untrusted sizes are bounded before allocation;
- borrowed-to-owned claim promotion allocation/import/canonicalization limits,
  atomic rollback, unique/shared frozen-owner accounting, clone/drop/last-owner
  behavior, and proof that promotion failure leaks no arena or partial handle;
- multi-root count/per-root/unique-total budgets, shared-DAG worst cases,
  retained unreachable-node bounds, new-owner compaction failure, and proof
  that an untrusted batch cannot pin unbounded memory or work;
- batch-verification membership/result/snapshot/accounting capacities,
  canonical ordering cost, shared-node-once charging, deterministic per-root
  attribution, and abort at every work/cancellation checkpoint with no
  proof/token prefix or prior-state mutation; retained prior state remains
  bounded by its existing owner/deadline and cannot accumulate failed refresh
  state. Complete/abort member buffers are separately bounded, and every
  fixed-size prior-observation variant has explicit size/stack/accounting
  evidence;
- admission/authority dependency, proof-support, correlation, reservation, and
  publication
  capacities are independently bounded. Exhaustion, mixed-domain input,
  unavailable sampling, or missing/stale remaining-work capability cannot
  truncate a support set, retain old authority, mint new authority, or
  accumulate failed-refresh state; hosted linearization refresh remains
  available without a commit-coverage capability;
- correlation claim/recipe/condition/assessment/support/anchor/endpoint-
  validity storage and verification/uncertainty-growth work are included in
  operation-wide limits. Because initial correlation proofs forbid every
  transitive correlation input, no hidden correlation-DAG capacity or traversal
  exists. Refresh reservation-slot/reader-generation tables have fixed
  capacities and bounded reclamation; each slot contains its tombstone states
  in place, so full capacity may refuse acquisition but never cleanup. Leaked/
  stalled writers, slot saturation, and fencing exhaustion return bounded typed
  failure and cannot trigger timeout-based stealing, unbounded scanning, or ABA
  reuse;
- full corpus minimization and panic/timeout triage;
- whole-safe-facade fuzzing across iterators, builders, callbacks, formatting,
  cancellation, state transitions, capacity/resource failure, unavailable
  devices, and denied privileges;
- Kani-style bounded proofs for selected normalization, parser, replay-window,
  budget, and state-transition properties with explicit model limits;
- remediated superlinear or unbounded paths.

Verification:

- continuous structure-aware fuzzing, allocation-failure injection, worst-case
  benchmarks, correlation proof/anchor worst cases, reservation/tombstone
  saturation and reclamation schedules, memory limits, and arbitrary-input
  runs.

Exit criteria:

- no known attacker-controlled unbounded work or memory remains;
- `v0.160.0 implementation stop reached. Run pentest for this exact commit.`

### v0.161.0 - Unsafe FFI And Platform Review

Status: planned.

Goal: complete full-workspace unsafe and platform audit.

Deliverables:

- machine-readable inventory and audit of every unsafe block, invariant,
  caller obligation, and owning `mundilfari-platform-*-sys` crate;
- ABI drift, ancillary parsing, PHC/PPS/RTC/counters, GPIO/frequency capture,
  oscillator/DAC/DCO, raw socket, namespace identity, and discipline-backend
  review;
- monotonic suspend/rate/scope/domain identity, fork/checkpoint lifecycle,
  handle inheritance, discipline ownership lease, and competing-adjuster
  review;
- platform correlation audit proving PHC/hosted/architectural/embedded
  providers emit only complete directed
  `UntrustedMonotonicCorrelationCandidate` values with exact capture anchors
  and bounded numerical claim recipes/conditions, withdraw on every declared
  reset/suspend/rate/migration/provider transition, and have no constructor,
  numerical-proof bypass, or dependency path to engine-admitted correlation
  state; platform output cannot smuggle a current/historical admitted
  correlation into a numerical recipe, condition, or support leaf;
- safe-wrapper length/alignment/discriminant/ownership/lifetime/kernel-size
  validation;
- C/JNI/Swift context/child ownership, retain/close/destruction order,
  concurrent close/use, per-call Rust arena borrows, and proof that no foreign
  handle embeds or outlives a borrowed branded claim;
- sanitizer/Miri coverage, MMIO volatile/alignment/order/endian/reset review,
  and remediated findings.

Verification:

- supported host/architecture matrix, fault injection, kernel ABI checks,
  correlation candidate/admission boundary tests, and focused platform pentest.

Exit criteria:

- no undocumented unsafe or unchecked privileged boundary remains, and no
  safe platform/core/engine/facade/protocol/crypto-state/IPC-schema crate
  admits unsafe;
- `v0.161.0 implementation stop reached. Run pentest for this exact commit.`

### v0.162.0 - Crypto TLS And Side-Channel Review

Status: planned.

Goal: independently audit every generic crypto/TLS consumer and secret path.

Deliverables:

- dependency/provider/algorithm inventory and update check;
- transcript, exporter, AEAD, signature, certificate, entropy, cookie, and
  secret lifecycle review;
- independent verification of every claimed `SecretMemoryProtection`
  capability and explicit unsupported/non-composable protection non-claims;
- `ServiceCredentialContextId`, `ResumptionCredentialGeneration`,
  `TlsConnectionGeneration`, `ExporterGeneration`, and
  `NtsAssociationGeneration` coverage across tickets/PSKs, full/resumed
  handshakes, NTS associations, cookies, trust/identity/revocation/provider/
  ticket-key/time/leap/lifecycle changes, reference identity/endpoint/SNI/ALPN/
  TLS/cipher-suite/hash/chain binding, conservative per-layer revalidation-
  horizon calculation, full validated chain, CRL/OCSP temporal evidence, and
  invalidate/revalidate/continue/disable-resumption action;
- stable `CredentialPolicyGeneration` and immutable
  `TemporalValidationEvidence` remain service-level inputs and never absorb a
  per-connection/exporter/association lifetime;
- proof that resumption without a resent chain reuses only still-valid immutable
  service evidence through a revalidated, consumed resumption credential while
  creating fresh connection/exporter/association generations and never reusing
  exporter material;
- interval-valued certificate temporal-validity and bootstrap review proving
  strict validation never uses a scalar `UnixTime`, midpoint/preferred
  projection, endpoint quantum adjustment, or a candidate artifact to
  authenticate its own retrieval, and always applies the whole-chain temporal
  intersection plus supported revocation-freshness constraints;
- generic provider-boundary assurance, per-key atomic usage/exhaustion,
  fail-closed rekey, and proof that persistence/protocol consumers bypass no
  admitted provider contract;
- resolved critical/high findings and timing evidence.

Verification:

- KATs, differential providers, malformed/tamper corpus, side-channel tests,
  cargo evidence, and independent cryptographic audit.

Exit criteria:

- all security primitives are current, bounded, and correctly composed;
- `v0.162.0 implementation stop reached. Run pentest for this exact commit.`

### v0.163.0 - Fault Long-Run And Hardware Review

Status: planned.

Goal: validate weeks-long operation, holdover, faults, and accuracy claims.

Deliverables:

- long-run source/servo/daemon/rotation/restart results;
- hardware lab for PTP/White Rabbit/Navheim-derived GNSS/PPS/IRIG/oscillators;
- persistence crash/rollback/migration campaigns and concurrent snapshot/
  withdrawal/cancellation stress;
- fork/exec/VM/container restore invalidation, competing clock discipliners,
  stable service-context invalidation without refinement churn, resumed-
  credential/provider/ticket-key/horizon revalidation and handshake connection/
  exporter/association rotation, independent time-data retrieval/verification/
  authority trust and caller-serialized-to-concurrent publication, forged
  adapters and raw/authenticated-but-unauthorized EOP/scale-offset rejection,
  leap and time-data admission-to-commit withdrawal/expiry/policy/authority/
  candidate races,
  retention-deadline upper-bound/correlation/holdover/suspend campaigns,
  every interval endpoint combination at certificate/revocation/EOP/era/replay/
  poll/leap/smear boundaries, hard-bound assumption loss/substitution/
  incorrect `All`/`Any`/threshold rewrite, incompatible-generation/capacity,
  untrusted-reference/registry-rollback/cache-poisoning campaigns through
  consensus and every external schema/binding, runtime condition
  contradiction/indeterminacy/expiry/withdrawal, stale accepted-bound tokens,
  canonical-identity cross-type/unit/scale/endpoint/operation/schema confusion,
  forced digest collisions and schema second-representation drift,
  derivation-arena exhaustion/eviction/stale/cross-store/wrong-domain handles,
  borrowed-claim lifetime escape/self-reference/leak attempts, owned-promotion
  allocation/import exhaustion and rollback, source drop before/during/after
  engine promotion, `'static` owned-task cancellation/drop, returned-clock
  ownership, and FFI arbitrary/concurrent context-child destruction,
  multi-root long-chain/diamond/duplicate-root sharing, root-removal retention,
  compaction rollback, canonical root/member permutation invariance,
  shared-node failure fan-out versus root-specific evidence independence,
  cancellation/work exhaustion after every node/root, snapshot invalidation
  after every verified prefix, no-token global abort, complete
  aborted-membership `Indeterminate`/`Unprocessed` diagnostic accounting,
  compile-fail complete/abort status mixing, stable unique/per-root accounting,
  complete-membership witness enforcement, and batch/individual proof/token
  identity equivalence; processed failed/contradicted/expired/indeterminate/
  withdrawn complete-member matrices one below/at/above every threshold,
  original-`n`/no-vote enforcement, duplicate-root correlation admission,
  failed-refresh prior retained/invalidated/absent outcomes, and atomic
  complete-new/prior-retirement races; non-authoritative batch admission versus
  consensus/publication subject identity, exact used `ProofSupportSet`, same-
  domain minimum deadline, untrusted/admitted correlation type confusion,
  provider registration without evidence/self-admission, forged narrow
  offset/rate/drift proof or capture anchor, condition/assessment/support-basis
  substitution/withdrawal, elapsed uncertainty growth, directed outward-
  rounded earliest-edge translation, independently checked endpoint deadlines,
  circular self/indirect validity, A→B/B→A and longer proof-support cycles,
  replacement-generation cycles, restored historical-reference support,
  mixed-domain rejection, each domain/
  provider/lifecycle reset/suspend/rate/migration/expiry/change,
  used-contributor withdrawal while an unused alternative quorum remains, and
  mandatory new-authority identity; prior identity/generation,
  measured/unavailable stamp, deadline, invalidation generation/reason,
  engine/publication generation, unbounded post-sample hosted preemption,
  guard panic/unwind/drop/cancellation, in-place non-failing tombstone cleanup,
  full-slot cleanup, superseded-cleanup no-op, impossible-transition fault
  latch/no-install, allocation/callback/blocking/panic cleanup instrumentation,
  reservation abandonment/leak/stall/ABA/
  higher-fence supersession, every invalidation-watermark dependency class,
  process/session restart, delayed old-writer `SupersededNoInstall`, bounded
  tombstone/reader-floor reclamation and exhaustion, timeout-steal refusal,
  delayed historical install, bounded reader retry/`RefreshInProgress`, strict
  revalidation after receipt, plus commit-covered preemption after every
  bounded step, exact remaining-work margin, missing/stale capability,
  sample/domain failure, immediate post-linearization expiry/invalidation, and
  delayed receipt,
  missing/truncated/over-budget early recipes, narrowed/spliced/substituted
  derivations, serialized-record replay/rollback/cross-engine restore and stale
  input/rule/model/lifecycle reverification, mixed-generation assessment
  issuance, origin/integrity/authority/transitive-basis laundering,
  assessment-to-publication races, hosted/PHC/architectural/embedded/browser
  interval containment and missing-bound refusal, coarse/straddling/latency/
  rate monotonic upper-edge expiry, suspend/reset/domain failures,
  linearization metadata under delayed caller return, and WCET-capability
  issue/reload/withdrawal/violation,
  servo/holdover/proposal invalidation, and strict-facade synchronized-label
  refusal,
  audit/configuration rollback, helper audit-full/latch/gap recovery, and
  virtual-clock ahead/freeze/catch-down/fault recovery campaigns;
- maximum/p99 TrustedClock read and PHC cross-timestamp latency evidence for
  claimed HFT-oriented configurations, including cache-line layout, bounded
  retry behavior, CPU migration, and per-core/socket/NUMA placement;
- documented measured accuracy envelopes and failures.

Verification:

- environmental drift, network partitions, grandmaster/source withdrawals,
  disk/torn-write/rollback faults, concurrent publication, queue pressure,
  suspend/reboot, leap/rollover simulation, and hardware measurements.

Exit criteria:

- every precision/holdover claim has reproducible evidence;
- `v0.163.0 implementation stop reached. Run pentest for this exact commit.`

### v0.164.0 - Supported Target And no_std Closure

Status: planned.

Goal: close the advertised compiler, platform, and feature matrix.

Deliverables:

- Rust `1.90.0..=1.97.1`, Linux, Windows, BSD, macOS, Android, iOS, embedded,
  WASM, and future-Aesynx readiness report;
- Android/iOS lifecycle evidence for background suspension/resume, path
  roaming, captive networks, and battery-budgeted resynchronization;
- representative allocator-free `*-unknown-none` and browser-WASM evidence,
  not only hosted cross-target compilation;
- owned-claim unique versus Arc-style frozen sharing is compiled/tested only
  where pointer atomics and the declared synchronization profile support it;
  other targets expose unique ownership or an explicit non-claim;
- single-thread, `target_has_atomic`, caller critical-section, and claimed
  ISR-safe no_std concurrency profiles with priority-inversion,
  interrupt-latency, stack, and WCET evidence;
- every target's monotonic provider has interval-containment/resolution/
  latency/rate/suspend/reset/migration evidence or an explicit strict-authority
  non-claim; through-completion is advertised only where target/profile WCET
  evidence closes the complete return path;
- every supported hosted target demonstrates version-reserved
  `LinearizationRefresh` without claiming WCET, including unbounded post-sample
  preemption and later strict-reader revalidation. Targets advertising
  `CommitCoveredRefresh` separately provide and test the complete remaining-
  work capability;
- every supported feature combination and published crate package check;
- documented unsupported privileged capabilities.

Verification:

- CI/cross builds, host tests, no allocator/no_std links, package dry-runs,
  semver feature checks, monotonic interval/capability and both refresh-profile
  fixtures, and docs.rs configurations.

Exit criteria:

- every advertised target/capability has build evidence or an explicit non-claim;
- `v0.164.0 implementation stop reached. Run pentest for this exact commit.`

### v0.165.0 - Standards Registry Closure

Status: planned.

Goal: refresh standards, drafts, errata, licenses, and completeness.

Deliverables:

- final pre-1.0 protocol registry audit;
- draft-to-final migrations or revision pins;
- live RFC Editor errata comparison and official-publisher revision refresh;
- RFC source/checksum reconciliation and local-vault inventory/lock review;
- recursive normative-reference closure with no unclassified dependency;
- complete implementation-evidence coverage with every production source,
  requirement, clause/erratum disposition, and test link independently
  reviewed;
- bidirectional stable requirement-ID closure across normative/architecture
  sources, crates/modules/items, positive/negative/property/fuzz/conformance/
  HIL evidence, exclusions, and non-claims with no orphan edge;
- exact-document expansion of every remaining family/bundle record, including
  current amendments, corrigenda, interpretations, profiles, and registries;
- refreshed non-WG proposal watchlist with explicit admitted, monitored, or
  rejected-out-of-scope dispositions;
- independently checked wire, behavioral, operational, and conformance claims;
- all accessible stable entries complete and blocked entries justified.

Verification:

- official publisher/source comparison, hashes, clause maps, transitive
  dependency graph, registry diff, and independent completeness review;
- deliberate stale revision, missing amendment, unresolved erratum,
  unclassified normative reference, family-only record, and overstated
  conformance claim all fail closed.

Exit criteria:

- no known accessible stable-baseline protocol, normative dependency,
  amendment, or erratum is silently omitted, and every non-claim is explicit;
- `v0.165.0 implementation stop reached. Run pentest for this exact commit.`

### v0.166.0 - API Documentation And Semver Freeze

Status: planned.

Goal: freeze production public APIs and documentation.

Deliverables:

- all public items documented with security invariants and examples;
- explicit safe-facade panic contract: caller input, supported-range,
  capacity, platform, authorization, cancellation, and resource failures
  return structured errors, with allocator-abort and internal-invariant
  non-claims documented separately;
- semver/feature/public dependency review;
- generated facade capability report replacing foundation-ready booleans and
  distinguishing compiled, available, authorized, and healthy states;
- `query_once()` versus `TrustedClock::now()` acquisition semantics and
  `estimate_now()` truth-seeking semantics, ahead-recovery states, monotonic
  domain identity, and cross-language range behavior documented;
- secret-memory capability/non-claim, service credential/resumption credential/
  connection/exporter/NTS-association hierarchy, immutable temporal-validation
  evidence/scalar-time non-claim and layer-correct conservative retention
  horizons, independent time-data retrieval/verification/authority-admission/
  publication phases, opaque leap/EOP/scale-offset admission and precommit
  revalidation, smear-presentation separation, and helper-policy/audit-full
  behavior documented without stronger implied claims;
- interval examples cover open/closed/half-open sets, unbounded algebra,
  finite trusted estimates, empty/singleton/adjacent cases, rational domains,
  hard-bound claim umbrella/non-authority semantics with no third public claim
  type, bounded logical conditions for
  intersection/union/conversion/consensus, unresolved external-reference
  resolution, canonical identity preimages/algorithm/structural collision
  checks/schema reuse, mandatory typed derivation handles and bounded no_std/
  alloc arena sizing/DAG behavior, borrowed versus owned claim lifetimes,
  fallible canonical promotion/frozen unique-or-shared ownership, no self-
  reference/leak/lifetime-extension boundary, early non-authoritative
  derivation recipes and complete-record export/unverified restore type-state,
  source-arena-independent verified root/derived claim proofs and accepted
  tokens with explicit no_std engine-storage lifetime/generation rules and
  source-drop versus evidence-generation invalidation semantics, runtime
  assessment
  statuses and issuance linearization, structured independent origin/
  integrity/authority/lineage support axes with transitive configured
  assumptions, policy-accepted-bound lifetime, provider-owned monotonic
  interval provenance, conservative upper-edge deadline/domain enforcement,
  untrusted directed versus opaque engine-admitted monotonic correlation,
  proof-bearing offset/rate/drift claims, exact capture anchors/uncertainty
  growth, condition/assessment/transitive support basis, independently checked
  non-circular endpoint validity, no transitive admitted/historical-correlation
  proof or condition support, outward-rounded earliest-edge deadline mapping
  and lifecycle invalidation,
  non-authoritative `BatchAdmissionState`,
  version-reserved `LinearizationRefresh` versus remaining-work-bounded
  `CommitCoveredRefresh`, `RefreshReservationGuard` ownership/drop/cancel/
  unwind, allocation-free/non-panicking in-place cleanup with superseded no-op
  and engine-fault fallback, watermark mutation rules, fencing supersession/no-
  install, process/session invalidation, bounded tombstone reclamation, timeout-
  steal refusal, and async no-`Poll::Pending` rule after reservation,
  linearization-time `observed_at`/`valid_until` versus WCET-backed
  through-completion contracts, strict versus conditional facade results,
  incompatibility, and no quantum adjustment;
- single-root and `OwnedHardBoundClaimSet` multi-root promotion examples cover
  shared DAGs, per-root/unique-total accounting, duplicate roots, immutable
  retention, bounded compaction, atomic failure, and untrusted batch limits;
- multi-root engine examples distinguish promotion atomicity from
  `BatchVerificationOutcome`, show canonical member ordering, shared-node
  failure fan-out, root-specific failure isolation, duplicate policy
  memberships, cancellation/work/snapshot aborts with no token prefix, and the
  `CompleteBatchVerification` requirement for full-membership consensus. They
  distinguish configured membership accounting from accepted-bound interval
  contributors, show that `Unprocessed` belongs only to
  `AbortMemberDiagnostic` and cannot reach a complete witness/quorum, cover
  unchanged thresholds and `Insufficient`/`Unsafe`, and document atomic refresh
  replacement plus fixed-size `PriorStateObservation` payloads for
  `PriorStateDisposition::{Retained, Invalidated, Absent}`. Examples state the
  exact tagged admission/authority subject, explain measured versus unavailable
  stamps, version-reserved hosted `LinearizationRefresh`, and optional
  remaining-work-bounded `CommitCoveredRefresh`, and warn that `Retained` is
  not authority through caller receipt. Consensus/publication examples show
  exact proof-support dependencies, conservative one-domain validity,
  correlation-bound translation or rejection, and new-authority recomputation
  after any used support is lost;
- no_std examples define `EngineProofHandle<'engine, K, T>` as the sole
  checked engine-store reference and
  `VerifiedBoundDerivationRef`/`PolicyAcceptedHardBoundRef` as its two
  kind-safe semantic projections, not parallel storage abstractions;
- `TimeEstimate` and facade documentation expose condition, assessment,
  verified-derivation identity, atom support basis, evidence/policy
  generations, deadline, reasons, assurance, and non-claims; no trusted boolean
  or cached synchronized label hides missing current acceptance or expiry;
- platform/provider documentation names each interval measurement strategy,
  uncertainty provenance, scalar inflation, migration/frequency/suspend/reset
  behavior, and completion capability/non-claim for every supported target;
- task, protocol, deployment, migration, incident, and hardware guides.
- returned-clock, `'static` async, no_std caller-storage, and C/JNI/Swift
  context/child ownership and destruction-order guides.

Verification:

- rustdoc with warnings denied, doctests, examples, link checks, semver tools,
  downstream fixtures, and usability review.

Exit criteria:

- APIs distinguish raw, parsed, validated, authenticated, and discipline-ready;
- `v0.166.0 implementation stop reached. Run pentest for this exact commit.`

### v0.167.0 - Independent Full-Workspace Audit

Status: planned.

Goal: complete independent protocol, daemon, platform, and application audit.

Deliverables:

- externally reviewed full workspace and deployment model;
- verified independent reviewer identity and signed exact-commit attestation;
- repository security-setting, protected-ref, CI identity, and release
  authority evidence obtained independently of documentation assertions;
- all critical/high findings fixed and medium findings resolved or explicitly
  accepted with owners/deadlines;
- complete retest report.

Verification:

- common gates plus independent audit methodology, regression suite, and
  evidence review.

Exit criteria:

- independent reviewers approve progression to beta;
- `v0.167.0 implementation stop reached. Run pentest for this exact commit.`

### v0.168.0 - Beta 1

Status: planned.

Goal: publish the first feature-complete beta with no new scope.

Deliverables:

- production packaging candidates, migration notes, known limitations;
- public feedback and incident intake;
- reproducible archives, signed provenance, protected release refs, and
  archive/SBOM/hash reproduction instructions;
- compatibility promise for the beta line.

Verification:

- exact archives/checksums/SBOM/provenance, install/upgrade/rollback tests, full
  regression and deployment smokes.

Exit criteria:

- beta artifacts are reproducible and no critical/high finding is open;
- `v0.168.0 implementation stop reached. Run pentest for this exact commit.`

### v0.169.0 - Beta 2 Remediation

Status: planned.

Goal: resolve beta findings without adding features.

Deliverables:

- compatibility, documentation, performance, and security fixes;
- public feedback disposition and regression tests;
- updated audit evidence.

Verification:

- upgrade from beta 1, full regression/hardware matrix, and changed-scope audit.

Exit criteria:

- known beta blockers are closed;
- `v0.169.0 implementation stop reached. Run pentest for this exact commit.`

### v0.170.0 - Release Candidate Tooling Rehearsal

Status: planned.

Goal: rehearse exact 1.0-versioned archives and publication without release.

Deliverables:

- RC-aware semantic version parsing and publish order;
- exact package contents, checksums, SBOM, provenance, and signatures;
- protected tag/branch and independent attestation verification;
- registry index wait/resume and failure recovery.

Verification:

- offline/local registry rehearsal, dirty/tag/version guards, archive byte
  comparison, interrupted publish simulation, and tool self-tests.

Exit criteria:

- tooling can reproduce and validate the exact candidate artifacts;
- `v0.170.0 implementation stop reached. Run pentest for this exact commit.`

### v1.0.0-rc.1 - Exact Production Candidate

Status: planned.

Goal: create the exact `1.0.0`-versioned candidate for final admission.

Deliverables:

- packages use final `1.0.0` versions with `-rc.1` repository tag semantics;
- no feature, dependency, source, generated artifact, or package-content
  difference may occur during final promotion;
- complete signed audit/pentest attestation, conformance, hardware,
  reproducible-build provenance, and SBOM bundle.

Verification:

- all common/final gates, exact artifact hashes, supported target matrix,
  independent audit review, and clean install/upgrade/rollback.

Exit criteria:

- the exact candidate has no known critical/high issue and is approved for
  unchanged promotion;
- `v1.0.0-rc.1 implementation stop reached. Run pentest for this exact commit.`

## v1.0.0 - Serious Production Release

Status: planned.

Goal: promote the unchanged approved release candidate.

Deliverables:

- final signed tags, crates, checksums, SBOM, provenance, release notes, and
  audit/pentest evidence;
- published long-term support and security response policy;
- post-1.0 standards and draft migration process.

Verification:

- candidate/tag/package/archive hashes are identical;
- all release readiness, registry publication, docs.rs, install, and provenance
  checks pass without rebuilding different sources.

Exit criteria:

- every accessible stable-baseline registry entry is complete;
- every default protocol and privileged path has independent security evidence;
- no known critical/high vulnerability remains;
- no claimed no_std/platform/precision/conformance property lacks evidence;
- experimental drafts remain isolated from stable APIs;
- `v1.0.0 implementation stop reached. Run final pentest for this exact commit.`

## Post-1.0 Policy

New stable standards published after the baseline enter `1.x` minor releases.
Security fixes receive patch releases and supported-line backports.

Draft-to-final migration:

- retains the exact draft decoder behind an explicit compatibility feature;
- introduces the final standard as a distinct revision;
- never silently changes wire, transcript, signature, or stored-packet meaning;
- includes migration notes, interoperability evidence, and a full release
  pentest.
