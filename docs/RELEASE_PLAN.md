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

### v0.8.0 - Epoch And Era Framework

Status: planned.

Goal: make epoch identity and rollover resolution explicit.

Deliverables:

- typed epochs, custom epoch identifiers, and bounded `EraContext` carrying an
  admissible interval and maximum-distance policy;
- resolver traits for RFC 868, NTP, PTP, broadcast, and device counters;
- a resolved-external-instant boundary for Navheim and other providers;
- ambiguity and missing-context errors.

Verification:

- before/at/after rollover vectors, ambiguous windows, negative epochs, and
  multiple-wrap rejection.

Exit criteria:

- no truncated timestamp silently chooses a nearest era;
- `v0.8.0 implementation stop reached. Run pentest for this exact commit.`

### v0.9.0 - Exact Fractions

Status: planned.

Goal: preserve and convert protocol-native fractions exactly.

Deliverables:

- binary, decimal, scaled-nanosecond, and bounded exact-fraction adapters;
- caller-selected rounding, exact rational quantum, and lower/upper residual
  interval;
- fixed maximum limb width, canonical sign location, positive nonzero
  denominator, and explicit reduced/unreduced invariants;
- bounded comparison, reduction, and conversion algorithms without
  cross-product overflow, attacker-selected arbitrary precision, or
  attacker-sized allocation;
- raw representation retention.

Verification:

- exhaustive reduced-width fractions, zero/maximum denominators, worst-case
  reduction work, comparison-overflow cases, official protocol examples,
  halfway rounding, maximum precision, and monotonicity tests.

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
- typed missing, stale, mixed-generation, unavailable, and unsupported
  conversion outcomes;
- no GNSS signal, navigation-message, receiver, or UTC-model interpretation.

Verification:

- scale-identity non-substitution, context generation replacement,
  mixed-generation rejection, missing/stale data, and forbidden implicit
  conversion tests.

Exit criteria:

- scale identity and model identity are explicit before any family conversion;
- `v0.11.0 implementation stop reached. Run pentest for this exact commit.`

### v0.11.1 - UT1 And Earth Orientation

Status: planned.

Goal: implement the EOP/UT1 model foundation needed for later UTC conversion
with explicit provenance and uncertainty.

Deliverables:

- the official `iers-conventions-2010-tn36` model baseline, its official
  corrections register, and the distinction between the official release and
  non-definitive working updates reviewed and recorded;
- versioned Earth-orientation records, source, validity, interpolation policy,
  model generation, and hard/statistical uncertainty separation;
- checked UT1-offset evaluation and application to continuous instants through
  `ConversionContext`; UTC civil conversion completes with `v0.12.0`;
- stale, extrapolated, missing, and withdrawn model outcomes.

Verification:

- official EOP examples, interpolation boundaries, stale/extrapolated data,
  model replacement/withdrawal, mixed generations, and uncertainty
  propagation.

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
- explicit out-of-scope scales and accuracy non-claims.

Verification:

- official published examples, epoch/rate extremes, rounding, reverse
  conversion residuals, wrong model, and unsupported-scale tests.

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
- protocol identity retained through conversion.

Verification:

- NTP era/UTC examples, PTP timescale/arbitrary-timescale cases, stale offset,
  mixed model generations, and cross-protocol non-substitution.

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
- no week resolution, navigation UTC model, receiver, health, or
  authentication logic.

Verification:

- externally resolved examples, missing/stale offset evidence, GLONASS
  non-fixed behavior, unknown identities, mixed generations, and compile-time
  Navheim-boundary checks.

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
  requests, model replacement/withdrawal, no_std/MSRV, and focused pentest.

Exit criteria:

- all admitted scale families preserve identity, model generation, and
  uncertainty semantics;
- `v0.11.5 implementation stop reached. Run pentest for this exact commit.`

### v0.12.0 - UTC And Leap Seconds

Status: planned.

Goal: model UTC including positive and possible negative leaps.

Deliverables:

- UTC civil values capable of representing second 60;
- versioned leap table, provenance, activation, and hash;
- leap announcement and conflict model;
- explicit generic TAI-to-UTC and UTC-to-TAI conversion against the canonical
  `AtomicInstant` origin, including realization metadata and typed ambiguous,
  missing-table, stale-table, and out-of-coverage outcomes;
- checked UTC/UT1 conversion using the admitted EOP model and matching
  conversion-context generations;
- explicit UTC-before-1972 non-claim until a historical frequency-offset model
  is separately admitted.

Verification:

- canonical TAI/UTC origin and published offset vectors, every historical leap
  boundary, second 60, invalid leap dates, table replacement, rollback,
  outside-coverage behavior, realization-evidence non-equivalence, and
  negative-leap synthetic tests.

Exit criteria:

- leap handling is explicit and no UTC value is forced through POSIX rules;
- `v0.12.0 implementation stop reached. Run pentest for this exact commit.`

### v0.13.0 - POSIX And Smear Policy

Status: planned.

Goal: define honest POSIX/UTC conversion behavior.

Deliverables:

- `PosixInstant` and typed `Unique`, `Ambiguous`, or `Nonexistent` conversion
  outcomes before policy;
- repeat/clamp/reject policies and typed smear profiles carrying provider,
  window, function, model generation, and inverse limitations;
- labels preventing smeared time from being reported as UTC.

Verification:

- leap boundaries, each policy, noninvertible cases, and smear endpoint
  continuity tests.

Exit criteria:

- every POSIX conversion states its leap policy;
- `v0.13.0 implementation stop reached. Run pentest for this exact commit.`

### v0.14.0 - Intervals And Uncertainty

Status: planned.

Goal: make uncertain time a first-class interval.

Deliverables:

- earliest/latest intervals and asymmetric uncertainty;
- a typed distinction between guaranteed hard bounds and statistical
  estimates carrying covariance, confidence level, model identity, and model
  generation;
- explicit, policy-named statistical-to-hard-bound conversion only where its
  assumptions and confidence are supplied; no implicit covariance promotion;
- checked intersection, union, expansion, containment, and midpoint policy;
- empty/disjoint/saturated results.

Verification:

- interval algebra properties, extremes, asymmetry, empty sets, rounding,
  covariance units/symmetry, confidence/model substitution, and compile-fail
  hard/statistical mixing.

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
- bounded error-budget components separating systematic/random,
  measured/asserted, correlation identity, calibration, quantization, path,
  capture, scale-model, and oscillator contributions;
- diversity assertions carrying provenance, assurance class, validity,
  generation, and conservative unknown-correlation behavior.

Verification:

- construction invariants, redacted debug output, non-substitution type tests,
  forged diversity, correlation conflicts, digest assurance, error-budget
  composition, and no trusted-boolean API.

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
- monotonic ordering, duplicate/idempotence policy, and bounded event queues;
- reserved withdrawal capacity/backpressure so an invalidation cannot be
  silently dropped behind ordinary observations;
- withdrawal propagation contract for filters, consensus, servos, virtual
  clocks, persistence, and audit records.

Verification:

- duplicate/out-of-order events, generation rollover, withdrawal before/after
  upsert, expiry, queue saturation, reserved-capacity exhaustion,
  discontinuity fan-out, restart, and deterministic replay.

Exit criteria:

- every source can retract evidence without relying on a source-specific
  mechanism;
- `v0.15.1 implementation stop reached. Run pentest for this exact commit.`

### v0.16.0 - Monotonic Clock Correlation

Status: planned.

Goal: relate fast monotonic readings to continuous/civil time safely.

Deliverables:

- monotonic instant, boot/session identity, correlation, rate, and uncertainty;
- stale/rollback/restart detection;
- virtual trusted-clock read model.

Verification:

- restart, suspend, rollback, drift, stale correlation, and uncertainty-growth
  simulations.

Exit criteria:

- monotonic values cannot become civil time without an explicit correlation;
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
- hard/statistical uncertainty, error-budget, observation-lifecycle,
  formatting, and error-taxonomy audit;
- Kani-style bounded proofs where useful;
- API and serialization stability review proving no raw Rust layout, `repr(C)`,
  or implicit serialization freezes the internal instant representation;
- resolved critical/high findings.

Verification:

- full foundation corpus, independent differential oracles, fuzzing, MSRV, and
  no_std target matrix.

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
- canonical bounded integers including signed high/low wide limbs, byte
  strings, sequences, identifiers, generations, and nested values;
- required-length and atomic encode-or-error behavior with no Rust-layout,
  serde-data-model, filesystem, IPC, or language-runtime dependency;
- import/export value traits for protocol, engine, and platform consumers;
- compatibility rules that later schema work may extend but never silently
  reinterpret.

Verification:

- golden bytes, every truncation, duplicate/noncanonical/unknown critical
  field, integer extremes, required-length/short-buffer atomicity,
  deterministic re-encoding, version skew, no-allocation, and arbitrary-byte
  fuzz/property tests.

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

### v0.24.0 - Transport And Clock Traits

Status: planned.

Goal: freeze platform-neutral I/O and clock contracts.

Deliverables:

- datagram, stream, raw-link, serial, edge, sample, CAN, and clock traits;
- receive/send metadata and timestamp quality;
- HAL-like device traits without Unix file descriptors in core signatures;
- compiled/available/authorized/healthy capability discovery contracts;
- entropy and hardware-clock traits without fallback implementations.

Verification:

- in-memory transports, error propagation, timestamp identity, short I/O, and
  capability compile tests.

Exit criteria:

- protocol crates do not expose OS socket or file types;
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
- test-only versus production-approved provider provenance and constructors;
- no protocol field semantics, TLS, certificate, storage, or clock policy in
  provider traits;
- redacted diagnostics and common error-taxonomy mapping.

Verification:

- deterministic mock/KAT providers, wrong algorithm/key/generation/direction,
  short output, entropy/nonce failure, usage-limit races and exhaustion,
  redaction, feature/no_std/MSRV matrices, and compile-time protocol-type
  isolation.

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
- deterministic per-poll work ceilings and reported remaining work;
- local exhaustion distinct from protocol invalidity.
- pre-allocation validation of every network-controlled size and explicit
  fallible-allocation outcomes for alloc-enabled paths.

Verification:

- conservation properties, nested operations, cancellation, adversarial
  complexity, allocator failure injection, oversized pre-allocation rejection,
  and exhaustion outcome tests.

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
- process/container/time-namespace identity and clock generation in every
  hosted clock report;
- checked native time conversion that returns `OutOfRange` rather than
  narrowing, saturating, or panicking;
- Android/iOS library-safe support.

Verification:

- host matrix, monotonic nondecrease, conversion bounds, suspend documentation,
  capability-state transitions, denied authorization, unavailable devices, and
  mock fault tests;
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
- isolated safe wrappers and replacement boundaries with no protocol policy.

Verification:

- ABI size/alignment checks, supported target builds, cargo-deny/audit, and
  forbidden dependency leakage tests.

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
- system/monotonic correlation with measured cross-timestamp error,
  calibration, and asymmetry inputs;
- Linux PTP character-device/standard-ioctl implementation separated from
  embedded device-specific MMIO;
- device identity and hotplug handling.

Verification:

- mock ioctl corpus, live PHC tests, overflow, stale device, concurrency,
  time-namespace mismatch, cross-timestamp uncertainty and maximum-latency
  benchmarks covering reset and clock-ID lifetime.

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
  frequency generation, invariance, suspend/reset, and cross-correlation;
- read-only safe APIs separated from later discipline authorization;
- platform-specific capability and non-claim reports.

Verification:

- invalid/battery-low RTC, torn register reads, BCD/range faults, century
  ambiguity, counter wrap, frequency change, reset, suspend, CPU migration,
  namespace mismatch, and mock/live platform tests.

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
- target-specific mock register blocks and no Unix descriptor assumptions.

Verification:

- mock MMIO/register models, misalignment/endian faults, stale ownership,
  reorder/barrier cases, reset/power cycle, counter wrap/frequency change,
  interrupt races, GPIO bounce/loss, frequency calibration, WCET, and
  representative embedded targets.

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
- crash-consistent atomic replacement, partial/torn-write detection, explicit
  durability semantics, and bounded schema migration;
- checksum separated from authenticated integrity and confidentiality;
- secret-bearing snapshot provider boundary, redaction, and best-effort
  clearing without overstated guarantees;
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
  boot/session binding, corruption, replay, and discontinuity handling;
- caller-supplied storage/no_std backend traits plus reviewed hosted file
  adapter; protocols import/export bounded values and perform no file I/O.

Verification:

- failure injection at every write/rename/sync boundary, partial/torn records,
  corruption, wrong key, rollback under every capability, attacker-restored
  state plus ordinary local key, copied boot/session state, trusted-counter/
  sealed/remote-witness faults, unknown schema, migration chains, size
  exhaustion, concurrent readers, and recovery.

Exit criteria:

- no protocol or engine invents an unaudited private state-file format;
- `v0.39.1 implementation stop reached. Run pentest for this exact commit.`

### v0.40.0 - Platform And Privilege Security Gate

Status: planned.

Goal: audit platform FFI, raw I/O, timestamps, hardware clocks, and adjustment.

Deliverables:

- machine-readable unsafe inventory, per-block invariants, safe-wrapper/ABI
  review, granular permission model, and privilege-separation plan;
- RTC/counter/MMIO/GPIO/frequency/actuator, namespace identity, discipline,
  discontinuity, early canonical-schema/crypto-provider, and persistence
  boundary review;
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
- signature/checksum hooks, activation, expiry, rollback, and conflict policy;
- no automatic network download in core.

Verification:

- official datasets, truncation/corruption, stale/future data, rollback,
  conflicting authorities, and deterministic hashes.

Exit criteria:

- scale conversion data is versioned, inspectable, and replaceable;
- `v0.52.0 implementation stop reached. Run pentest for this exact commit.`

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
- generic validated-observation inputs with no NTP packet, association,
  transport, poll, or wire type dependency;
- bounded source cardinality and tie behavior;
- no source weighting yet.

Verification:

- published algorithm examples, Byzantine groups, disjoint/split intervals,
  malicious majorities, impossible-guarantee cases, identical endpoints,
  permutations, and property tests.

Exit criteria:

- malicious outliers cannot enter the survivor set by simple averaging and no
  protocol crate owns a copy of the quorum algorithm;
- `v0.60.0 implementation stop reached. Run pentest for this exact commit.`

### v0.61.0 - Generic Clustering Combining And Diversity

Status: planned.

Goal: select and combine validated survivors under protocol-neutral engine
diversity policy.

Deliverables:

- engine-owned clustering, combining, preferred-source choice, and uncertainty
  output over generic observations;
- operator, network, path, geography, protocol, authority, and upstream
  correlation attributes;
- operator/upstream/ASN/path/grandmaster/receiver/oscillator/site diversity
  groups and a rule that weights never override the fault quorum;
- split-brain result;
- reusable bounded APIs that NTP and later cross-protocol consensus compose
  without either reimplementing the algorithms.

Verification:

- correlated hostnames, tie/order invariance, malicious majority, source loss,
  diversity thresholds, and simulator campaigns.

Exit criteria:

- multiple names are never assumed to be independent sources;
- `v0.61.0 implementation stop reached. Run pentest for this exact commit.`

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
  generation lifecycle with no key reuse across an invalid generation;
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
- RFC 9325 deployment policy and RFC 9525 service-identity verification;
- explicit certificate-revocation capability report and deployment non-claim
  where the selected provider/configuration supplies no live revocation;
- certificate-time bootstrap policy without disabling validity checks.

Verification:

- Rustls interop, wrong identity, expired/not-yet-valid/revoked-policy chain,
  unavailable revocation, trust anchor, ALPN, TLS version, resumption, rejected
  early data, close, fragmentation, and provider matrix tests.

Exit criteria:

- Rustls supplies TLS only; all NTS behavior remains Mundilfari-owned;
- `v0.75.0 implementation stop reached. Run pentest for this exact commit.`

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
  and replenish;
- local discard deadline/policy age clearly distinguished from any
  authenticated server expiration supplied by a future protocol revision;
- non-`Copy`, redacted-debug, non-automatic-serialization secret types;
- prohibition on logging unique identifiers, cookies, exporter material, or
  stable client correlators;
- fork/process-generation-aware entropy and request identity;
- one-use/replenishment, replay/failure/rekey state, common secure persistence
  with capability-qualified rollback evidence, atomic per-key exhaustion,
  fail-closed rekey, key-rotation overlap, and best-effort clearing boundary
  without overstated guarantees.

Verification:

- public server interop, cookie exhaustion/reuse prevention, local age expiry,
  replay, server restart, key rotation, endpoint migration, process fork,
  log-capture redaction, tamper, and long simulation.

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
- state transitions from unknown to rough to certificate-validatable time;
- rollback/restart/expiry and uncertainty growth.

Verification:

- no clock, wildly wrong clock, stale snapshot, restart, rollback, key
  mismatch, interval outside certificate, and recovery simulations.

Exit criteria:

- bootstrap never silently disables certificate validity or identity checks;
- `v0.80.0 implementation stop reached. Run pentest for this exact commit.`

### v0.81.0 - Secure Time Security Gate

Status: planned.

Goal: audit dependency, NTS, Roughtime, cookie, and bootstrap boundaries.

Deliverables:

- complete RFC/draft clause maps and dependency admission reports;
- NTS early-data, resumption/exporter generation, cookie
  privacy/unlinkability, logging, cluster-key rollback/compromise, certificate
  revocation capability, and fork-generation audit;
- provider assurance and secret lifecycle/redaction/rollback/clearing review;
- fixed-capacity codec, machine, AEAD provider, cookie jar, and Rustls adapter
  boundary audit;
- resolved critical/high TLS, AEAD, replay, downgrade, and bootstrap findings.

Verification:

- independent interop, fuzzing, malformed TLS/application records, long
  rotation/restart simulations, cargo evidence, and focused pentest.

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
  `v0.60.0`–`v0.61.0` engine quorum/clustering/combining primitives, with no
  second intersection, falseticker, clustering, or combining implementation;
- cross-protocol correlation groups, supported interval,
  authentication/diversity policy, split-brain, and evidence;
- exact conversion-context/model generation on every normalized input;
  mixed generations are rejected or explicitly re-normalized before quorum;
- generic upsert/withdraw/discontinuity consumption with withdrawal
  propagation and recomputation before any later servo action;
- hard bounds remain distinct from statistical estimates/covariance and may
  mix only through an explicit reviewed conversion policy;
- explicit `n` admitted sources, maximum faulty diversity groups `f`, required
  overlap, freshness/path-delay bounds, network-adversary scope, and
  correct-interval assumptions in every result;
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
  hard/statistical mixing attempts, policy/membership reload during
  withdrawals, in-flight crypto, pending servo proposals, and helper
  authorization, stale-result rejection, atomic replacement, and interval
  properties. Navheim is represented only by protocol-neutral fixtures here.

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
- hard/statistical uncertainty kept distinct and explicit target capability;
- withdrawals and discontinuities reset or invalidate state before new output.

Verification:

- analytical PLL traces, drift/noise/step/loss simulations, saturation,
  numerical stability, mixed uncertainty, withdrawal/discontinuity,
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
  withdrawal, and discontinuity behavior;
- error-budget and hard/statistical uncertainty preservation.

Verification:

- analytical frequency traces, irregular/lost samples, drift, steps,
  saturation, numerical extremes, generation changes, withdrawal,
  reference comparison, and properties.

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
- requested versus predicted applied/residual values and saturation evidence,
  clearly labeled as prediction until actual feedback arrives;
- proposal-only engine output consumed by `mundilfari-discipline`;
- invalidation when input, target, authorization, or correlation generations
  change.

Verification:

- threshold boundaries, backward/post-startup refusal, saturation, stale
  generation, revoked authority, impossible target capability, withdrawal,
  discontinuity, and proposal replay.

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
- bounded missing-feedback timeout and degraded/faulted outcomes;
- persistence/audit representation through the common schema without granting
  the engine adjustment authority.

Verification:

- exact, quantized, clamped, partial, rejected, delayed, duplicate, missing,
  reordered, wrong-proposal, wrong-target-generation, and discontinuous
  feedback traces; repeated saturation, integrator-windup adversarial cases,
  actuator mock faults, and closed-loop analytical/simulator comparison.

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
- no floating-point requirement in no_std core.

Verification:

- recorded PHC traces, simulated oscillator/noise models, numerical extremes,
  covariance/confidence semantics, hard-bound conversion rejection/policies,
  convergence, withdrawal/discontinuity, malicious delay, and independent
  estimator comparison.

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
- systematic/random and measured/asserted error components retained; model
  prediction covariance never presented as a guaranteed bound.

Verification:

- long synthetic/hardware traces, temperature ramps, restart, stale model,
  source recovery, underreported stability attacks, and saturation.

Exit criteria:

- holdover never reports frozen uncertainty or hidden source loss;
- `v0.136.0 implementation stop reached. Run pentest for this exact commit.`

### v0.137.0 - Trusted Virtual Clock

Status: planned.

Goal: provide a monotonic application clock with civil correlation.

Deliverables:

- synchronized/rough/holdover/faulted states;
- `TimeEstimate` with earliest/latest, optional policy-approved preferred
  estimate, scale/realization, resolution, uncertainty, monotonic correlation,
  freshness/holdover age, separate authentication/integrity/traceability,
  leap policy, source generation, and warnings;
- monotonic nonrollback reads with no network I/O, plus explicit UTC/POSIX
  conversion context and policy;
- common secure persistence and restart bootstrap boundary;
- one logically consistent instant/uncertainty/scale-model/source-set/
  generation snapshot contract, with the concurrent publication mechanism
  completed in `v0.137.1`.

Verification:

- concurrent reads, clock rollback, system step, suspend/restart, leap/smear,
  holdover, split-brain, and monotonicity properties.

Exit criteria:

- applications can read trusted time without a network request per event;
- `v0.137.0 implementation stop reached. Run pentest for this exact commit.`

### v0.137.1 - Concurrent Snapshot Publication

Status: planned.

Goal: publish TrustedClock estimates and observation lifecycle changes without
torn logical snapshots or unbounded reader latency.

Deliverables:

- documented memory-ordering/publication model for one internally consistent
  snapshot across instant, hard/statistical uncertainty, scale/context model,
  source set, validity, and generation;
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

- Loom/Shuttle-style repository-only model tests for publication,
  invalidation, queues, cancellation, persistence swap, and helper IPC state;
- stress tests for readers/writers, generation consistency, callback reentry,
  starvation, suspend/reset, forced CPU migration, cache-line contention,
  retry exhaustion, and per-core/cross-core/cross-NUMA HFT-oriented maximum/
  p99 latency benchmarks.

Exit criteria:

- no reader can observe fields from different logical clock generations;
- `v0.137.1 implementation stop reached. Run pentest for this exact commit.`

### v0.138.0 - Easy Blocking APIs

Status: planned.

Goal: expose safe one-shot application APIs.

Deliverables:

- `query_once()` acquisition distinct from `TrustedClock::now()` virtual-clock
  reads, plus strict `TrustedClock::system_defaults(...)`;
- a named, versioned system-defaults policy profile whose report enumerates
  selected sources, trust roots, network actions, fallbacks, platform
  assumptions, and rejected alternatives;
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
  fallback refusal, misuse compile tests, and iterator/builder/callback/
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
- optional owned buffers under `alloc`;
- no Tokio or runtime dependency.

Verification:

- custom executor, embedded-style polling, Tokio adapter example outside the
  graph, cancellation races, wake discipline, and feature matrix.

Exit criteria:

- async use does not make an executor part of protocol semantics;
- `v0.139.0 implementation stop reached. Run pentest for this exact commit.`

### v0.140.0 - Fixed-Storage Builders

Status: planned.

Goal: complete allocation-free user-facing client/server construction.

Deliverables:

- const capacities, caller buffers, deterministic resource reports, and
  compile-time/runtime capacity errors;
- documented allocation behavior per operation for every `alloc` builder;
- representative SNTP/NTP/PTP/generic-external/IRIG examples;
- embedded transport integration guide.

Verification:

- zero/minimum/maximum capacity, stack-size reports, no allocator link,
  embedded targets, examples, and compile-fail overflow cases.

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
  capability reports, observation events, and discontinuities;
- compatibility/freeze ledger proving deterministic field order/encoding,
  bounds, version negotiation, unknown field/criticality rules, canonicality,
  and maximum message sizes retain the early kernel semantics;
- schema owns no serde/Rust-memory-layout semantics and works in `no_std`
  caller buffers;
- explicit compatibility contracts for daemon IPC, secure persistence, C,
  WASM, logs/evidence, and language bindings;
- Java/Kotlin and Swift either use tested JNI/Swift shims or the documented C
  ABI with platform integration/range fixtures.

Verification:

- golden cross-language vectors, noncanonical/duplicate/unknown fields,
  version skew, truncation, integer/range extremes, schema migration,
  deterministic re-encoding, C/WASM/JNI-or-C/Swift-or-C fixtures, and fuzzing.

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
- pre-opened socketpair/fixed endpoint, OS peer credentials, fixed-version
  maximum-length canonical-schema messages, sequence/monotonic
  expiry/source-generation replay defense, and pre-opened allowlisted clock
  handles;
- helper-enforced phase/frequency/slew/step bounds, privilege reduction,
  syscall sandboxing, separated raw-capture authority where possible, and an
  append-only accepted/rejected request audit;
- helper-local cumulative phase and frequency budgets per named time window,
  maximum request rate, minimum settling interval, and an independent policy
  ceiling that worker configuration cannot expand;
- helper-generated session nonce, boot/session generation, clock-domain
  identity for monotonic expiries, and newly authorized generations for
  recovery;
- fault latching after configured repeated rejected, saturated,
  contradictory, or feedback-missing requests, with bounded fail-closed audit
  behavior when storage is unavailable/full;
- Linux reference plus supported platform service designs.

Verification:

- IPC fuzzing, peer-credential spoofing, replay/expiry/generation schedules,
  arbitrary path/clock-ID/ioctl/FD refusal, compromised-worker simulation,
  repeated individually valid maximum adjustments, cumulative budget and rate
  boundaries, settling violations, worker policy-expansion attempts, wrong
  session/domain, fault-latch/re-authorize recovery, audit-full/unavailable,
  socket/file permissions, restart, downgrade, service sandbox, VM clock
  tests, and soak.

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
- canonical external-schema values/events with explicit high/low limbs for
  wide instants and
  `OutOfRange` on every narrowing conversion;
- generated header and ABI compatibility policy;
- no unbounded allocation or Rust layout exposure.

Verification:

- C/C++ consumers on Linux/Windows/macOS, canonical golden vectors,
  null/length/alias misuse, ABI layout, symbol version, sanitizer, and fuzz
  tests;
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
- checked JavaScript integer/date conversion with `OutOfRange` rather than
  truncation, saturation, or panic;
- canonical external-schema encoding/decoding, version, bounds, and
  unknown-field behavior;
- explicit lack of UDP/raw/hardware/clock-control browser capabilities.

Verification:

- wasm32 build, browser/node tests, hostile buffers, JS exception/cancel,
  feature size, and no native dependency leakage.

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
- append-only discipline-request outcomes and capability states separated into
  compiled, available, authorized, and healthy;
- accuracy/authentication/traceability fields kept separate.

Verification:

- cardinality attacks, secret/cookie/certificate redaction, malformed exporter,
  backpressure, schema compatibility, and incident replay.

Exit criteria:

- observability cannot alter protocol validity or exhaust core state;
- `v0.146.0 implementation stop reached. Run pentest for this exact commit.`

### v0.147.0 - Configuration And Policy Language

Status: planned.

Goal: implement explicit, validated deployment policy.

Deliverables:

- bounded configuration for sources, trust, diversity, protocols, clocks,
  steps/slew, holdover, resources, platform privileges, and logging;
- secure defaults, unknown-field rejection, versioning, and dry-run;
- no generic deserialization dependency in protocol cores.

Verification:

- valid/invalid fixtures, unknown/duplicate/conflicting fields, resource
  extremes, downgrade attempts, migration, and property fuzzing.

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
  concurrent snapshot, canonical external-schema, and language-binding review;
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

- parser inventory, complexity oracle, allocation/work/response limits;
- allocator-failure behavior and abort-on-OOM non-claims for every alloc path,
  proving untrusted sizes are bounded before allocation;
- full corpus minimization and panic/timeout triage;
- whole-safe-facade fuzzing across iterators, builders, callbacks, formatting,
  cancellation, state transitions, capacity/resource failure, unavailable
  devices, and denied privileges;
- Kani-style bounded proofs for selected normalization, parser, replay-window,
  budget, and state-transition properties with explicit model limits;
- remediated superlinear or unbounded paths.

Verification:

- continuous structure-aware fuzzing, allocation-failure injection, worst-case
  benchmarks, memory limits, and arbitrary-input runs.

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
- safe-wrapper length/alignment/discriminant/ownership/lifetime/kernel-size
  validation;
- sanitizer/Miri coverage, MMIO volatile/alignment/order/endian/reset review,
  and remediated findings.

Verification:

- supported host/architecture matrix, fault injection, kernel ABI checks, and
  focused platform pentest.

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
- every supported feature combination and published crate package check;
- documented unsupported privileged capabilities.

Verification:

- CI/cross builds, host tests, no allocator/no_std links, package dry-runs,
  semver feature checks, and docs.rs configurations.

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
  cross-language range behavior documented;
- task, protocol, deployment, migration, incident, and hardware guides.

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
