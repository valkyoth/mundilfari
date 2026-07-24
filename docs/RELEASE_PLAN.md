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
v0.N.P       scoped correction for milestone N
v1.0.0-rc.N exact production candidate
v1.0.0       first serious production-ready release
```

## Release Principles

Every release requires:

- one clear definition of done;
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
- status classes for stable, historic, draft, licensed, partial, and
  unavailable specifications;
- schema validation and duplicate identifier/revision rejection;
- public completeness and legitimate-access policy.

Verification:

- registry round trips, malformed schema corpus, duplicate/conflict tests, and
  comparison with `PROTOCOLS.md`.

Exit criteria:

- every initial registry entry has a status and roadmap assignment;
- `v0.2.0 implementation stop reached. Run pentest for this exact commit.`

### v0.3.0 - Security And Engineering Policy

Status: planned.

Goal: turn the threat model and coding rules into enforced repository policy.

Deliverables:

- parser, panic, arithmetic, allocation, logging, secret, unsafe, and
  discipline-authority policies;
- dependency-layer and 500-line validators;
- protocol claim, accuracy claim, and conformance claim checks;
- security-review templates for standards and dependencies.

Verification:

- policy validator unit fixtures covering every accepted and rejected case;
- deliberate layer, file-size, feature, and unsafe violations fail closed.

Exit criteria:

- policy drift is detected locally before protocol implementation begins;
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

- signed seconds plus normalized attoseconds;
- checked instant/duration arithmetic and ordering;
- documented origin and no implicit `SystemTime` conversion.

Verification:

- invariant, ordering, negative-date, extreme-range, and arithmetic tests.

Exit criteria:

- one continuous internal timeline exists without erasing native wire values;
- `v0.7.0 implementation stop reached. Run pentest for this exact commit.`

### v0.8.0 - Epoch And Era Framework

Status: planned.

Goal: make epoch identity and rollover resolution explicit.

Deliverables:

- typed epochs, custom epoch identifiers, and bounded `EraContext`;
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

- binary, decimal, scaled-nanosecond, and rational fraction adapters;
- caller-selected rounding and returned quantization interval;
- raw representation retention.

Verification:

- exhaustive reduced-width fractions, official protocol examples, halfway
  rounding, maximum precision, and monotonicity tests.

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

### v0.11.0 - Time Scales

Status: planned.

Goal: represent UTC, TAI, UT1, POSIX, PTP, NTP, and named GNSS scales
distinctly without interpreting GNSS messages.

Deliverables:

- stable scale identifiers and conversion graph;
- explicit leap, Earth-orientation, and GNSS-offset contexts used to
  cross-check externally resolved observations;
- missing-data and stale-data failures.

Verification:

- graph path tests, forbidden implicit conversions, stale table rejection, and
  cross-scale published examples.

Exit criteria:

- public APIs cannot confuse scale identity with epoch encoding;
- `v0.11.0 implementation stop reached. Run pentest for this exact commit.`

### v0.12.0 - UTC And Leap Seconds

Status: planned.

Goal: model UTC including positive and possible negative leaps.

Deliverables:

- UTC civil values capable of representing second 60;
- versioned leap table, provenance, activation, and hash;
- leap announcement and conflict model.

Verification:

- every historical leap boundary, second 60, invalid leap dates, table
  replacement, rollback, and negative-leap synthetic tests.

Exit criteria:

- leap handling is explicit and no UTC value is forced through POSIX rules;
- `v0.12.0 implementation stop reached. Run pentest for this exact commit.`

### v0.13.0 - POSIX And Smear Policy

Status: planned.

Goal: define honest POSIX/UTC conversion behavior.

Deliverables:

- `PosixInstant`, ambiguity errors, repeat/clamp/reject policies;
- typed smear profiles and inverse conversion limitations;
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
- checked intersection, union, expansion, containment, and midpoint policy;
- empty/disjoint/saturated results.

Verification:

- interval algebra properties, extremes, asymmetry, empty sets, and rounding.

Exit criteria:

- network and physical observations need not pretend to be exact instants;
- `v0.14.0 implementation stop reached. Run pentest for this exact commit.`

### v0.15.0 - Quality Authentication And Provenance

Status: planned.

Goal: define the complete protocol-neutral observation model.

Deliverables:

- resolution, precision, age, stability, traceability, leap, and holdover;
- authentication class separate from advertised/measured/verified accuracy;
- source, protocol, authority, path, raw hash, capture, warnings, and reading.

Verification:

- construction invariants, redacted debug output, non-substitution type tests,
  and no trusted-boolean API.

Exit criteria:

- callers can distinguish authentic, accurate, traceable, and merely formatted;
- `v0.15.0 implementation stop reached. Run pentest for this exact commit.`

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

### v0.17.0 - Foundation Security Gate

Status: planned.

Goal: audit the complete time model before protocols depend on it.

Deliverables:

- arithmetic and conversion audit;
- Kani-style bounded proofs where useful;
- API and serialization stability review;
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
- no hidden heap use.

Verification:

- zero/full capacity, reuse, order, duplicate, removal, and model comparison.

Exit criteria:

- untrusted lengths cannot create attacker-sized allocations;
- `v0.21.0 implementation stop reached. Run pentest for this exact commit.`

### v0.22.0 - Borrowed Packet Pattern

Status: planned.

Goal: standardize lossless parse/validate/encode APIs.

Deliverables:

- borrowed packet references, unknown-field iterators, owned opt-in forms;
- strict/compatible/forensic modes;
- caller-owned encoder contract.

Verification:

- unknown preservation, forensic non-authority, exact round trips, and
  insufficient-output atomicity.

Exit criteria:

- protocol crates share one security-reviewed API shape;
- `v0.22.0 implementation stop reached. Run pentest for this exact commit.`

### v0.23.0 - Poll And Timer State Machines

Status: planned.

Goal: define runtime-neutral bounded protocol execution.

Deliverables:

- explicit poll context, actions, timers, deadlines, cancellation, and budgets;
- no executor or wall-clock assumption;
- deterministic state transition tracing.

Verification:

- exhaustive small state machines, cancellation races, timer wrap, duplicate
  wake, and budget exhaustion.

Exit criteria:

- protocol engines can run in embedded, simulator, and hosted environments;
- `v0.23.0 implementation stop reached. Run pentest for this exact commit.`

### v0.24.0 - Transport And Clock Traits

Status: planned.

Goal: freeze platform-neutral I/O and clock contracts.

Deliverables:

- datagram, stream, raw-link, serial, edge, sample, CAN, and clock traits;
- receive/send metadata and timestamp quality;
- entropy and hardware-clock traits without fallback implementations.

Verification:

- in-memory transports, error propagation, timestamp identity, short I/O, and
  capability compile tests.

Exit criteria:

- protocol crates do not expose OS socket or file types;
- `v0.24.0 implementation stop reached. Run pentest for this exact commit.`

### v0.25.0 - Work And Resource Budgets

Status: planned.

Goal: enforce operation-wide resource accounting.

Deliverables:

- non-copyable byte, item, nesting, work, allocation, and response budgets;
- child reservations without reset or double release;
- local exhaustion distinct from protocol invalidity.

Verification:

- conservation properties, nested operations, cancellation, adversarial
  complexity, and exhaustion outcome tests.

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
- API stability and code-size review;
- fuzz corpus and complexity-oracle report.

Verification:

- full arbitrary-input campaign, MSRV/no_std matrix, and independent review.

Exit criteria:

- shared foundations are approved for untrusted protocol input;
- `v0.29.0 implementation stop reached. Run pentest for this exact commit.`

## Phase 3: Platform Foundations

### v0.30.0 - Standard Clock Adapters

Status: planned.

Goal: expose safe monotonic and realtime clocks on supported hosted platforms.

Deliverables:

- Linux, Windows, BSD, and macOS adapters;
- resolution/capability reporting and explicit platform errors;
- Android/iOS library-safe support.

Verification:

- host matrix, monotonic nondecrease, conversion bounds, suspend documentation,
  and mock fault tests.

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
- isolated safe wrappers and replacement boundaries.

Verification:

- ABI size/alignment checks, supported target builds, cargo-deny/audit, and
  forbidden dependency leakage tests.

Exit criteria:

- generic ABI code is reviewed without entering core or wire crates;
- `v0.33.0 implementation stop reached. Run pentest for this exact commit.`

### v0.34.0 - Linux Raw Transports

Status: planned.

Goal: implement raw ICMP and Ethernet transport foundations.

Deliverables:

- bounded raw socket configuration and link metadata;
- capability/permission errors and interface binding;
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
- transmit error-queue association and kernel drop indicators.

Verification:

- synthetic every-byte truncation, alignment variants, multiple messages,
  unknown controls, reorder, and live loopback tests.

Exit criteria:

- no truncated or mismatched ancillary record becomes a valid timestamp;
- `v0.35.0 implementation stop reached. Run pentest for this exact commit.`

### v0.36.0 - Hardware Timestamp Configuration

Status: planned.

Goal: configure and inspect NIC timestamp capabilities safely.

Deliverables:

- reviewed Linux ioctl/netlink adapter;
- interface capability discovery and exact applied-policy reporting;
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

- PHC capability/read and supported cross-timestamp methods;
- phase/frequency adjustment traits with strict bounds;
- device identity and hotplug handling.

Verification:

- mock ioctl corpus, live PHC tests, overflow, stale device, concurrency, and
  cross-timestamp uncertainty checks.

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

Verification:

- synthetic sequence wrap, missed edge, timeout, live PPS, hot unplug, and
  timestamp correlation tests.

Exit criteria:

- physical edges become observations without inventing civil time;
- `v0.38.0 implementation stop reached. Run pentest for this exact commit.`

### v0.39.0 - System Clock Adjustment

Status: planned.

Goal: implement bounded platform clock-control adapters.

Deliverables:

- Linux, Windows, BSD, and macOS supported slew/step/frequency operations;
- explicit capabilities and policy-required authorization token;
- no default backward or post-startup step.

Verification:

- mock kernel faults, bounds, authorization compile tests, isolated VM tests,
  rollback refusal, and degraded capability.

Exit criteria:

- no protocol parser or client can directly modify a system clock;
- `v0.39.0 implementation stop reached. Run pentest for this exact commit.`

### v0.40.0 - Platform And Privilege Security Gate

Status: planned.

Goal: audit platform FFI, raw I/O, timestamps, hardware clocks, and adjustment.

Deliverables:

- unsafe inventory, ABI review, permission model, and privilege-separation plan;
- resolved critical/high platform findings;
- supported-target capability matrix.

Verification:

- host CI, sanitizers/Miri where applicable, syscall fault injection, live
  hardware subset, and focused pentest.

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

### v0.53.0 - Legacy And Format Security Gate

Status: planned.

Goal: audit legacy protocols and time representations.

Deliverables:

- downgrade/non-authority review and complete format clause maps;
- parser/resource fuzz reports;
- resolved critical/high findings and compatibility non-claims.

Verification:

- full legacy/format corpus, differential implementations, no_std/MSRV matrix,
  and focused pentest.

Exit criteria:

- legacy support cannot silently authorize clock changes;
- `v0.53.0 implementation stop reached. Run pentest for this exact commit.`

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

### v0.56.0 - NTP Extensions And MAC Framing

Status: planned.

Goal: implement updated extension-field and legacy MAC framing.

Deliverables:

- applicable RFC 7821/7822/8573 registry and update behavior;
- unknown extension preservation and criticality;
- ambiguity resolution between extensions and legacy MACs.

Verification:

- official examples, length/alignment/padding, duplicate fields, ambiguous
  tails, every truncation, and round trips.

Exit criteria:

- extension parsing follows all incorporated NTP updates;
- `v0.56.0 implementation stop reached. Run pentest for this exact commit.`

### v0.57.0 - SNTP Client

Status: planned.

Goal: deliver a strict single-shot SNTP client engine.

Deliverables:

- request construction, origin matching, four-timestamp delay/offset;
- version/mode/stratum/leap/root-distance/era validation;
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
- no response policy for suspicious requests.

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
- monotonic timers.

Verification:

- RFC examples, reach transitions, loss/reorder, clock steps, poll boundaries,
  stale samples, and simulator traces.

Exit criteria:

- source state is deterministic and restart-safe;
- `v0.59.0 implementation stop reached. Run pentest for this exact commit.`

### v0.60.0 - Intersection And Falseticker Rejection

Status: planned.

Goal: implement interval intersection and candidate admission.

Deliverables:

- correctness interval construction, intersection, survivor count, and
  falseticker evidence;
- bounded source cardinality and tie behavior;
- no source weighting yet.

Verification:

- published algorithm examples, Byzantine groups, disjoint/split intervals,
  identical endpoints, permutations, and property tests.

Exit criteria:

- malicious outliers cannot enter the survivor set by simple averaging;
- `v0.60.0 implementation stop reached. Run pentest for this exact commit.`

### v0.61.0 - Clustering Combining And Diversity

Status: planned.

Goal: select and combine survivors under diversity policy.

Deliverables:

- clustering, system-peer choice, combining, and uncertainty output;
- operator, network, path, geography, protocol, authority, and upstream
  correlation attributes;
- split-brain result.

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

- source lifecycle, burst, poll adaptation, reachability, selection, and
  combined reading;
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

- RFC 9327 mode 6 codec/state and applicable MIB/YANG mappings;
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

### v0.70.0 - Experimental NTP Revisions

Status: planned.

Goal: implement exact pinned NTPv5 and NTP-over-PTP drafts experimentally.

Deliverables:

- revision-named codecs/state, feature gates, and wire identity;
- client/server scope only where the exact draft defines it;
- no stable type leakage or automatic negotiation.

Verification:

- draft vectors, revision mismatch, unknown fields, migration fixtures,
  malformed corpus, and available draft implementation interop.

Exit criteria:

- active drafts remain isolated and cannot change stable NTP semantics;
- `v0.70.0 implementation stop reached. Run pentest for this exact commit.`

### v0.71.0 - NTP Family Security Gate

Status: planned.

Goal: complete NTP-family conformance, interoperability, and security review.

Deliverables:

- RFC/update/errata clause maps and protocol capability matrix;
- differential simulator and implementation report;
- resolved critical/high parser, state, selection, server, and downgrade issues.

Verification:

- official vectors, chrony/ntpd/ntpsec matrix, fuzz/soak/Byzantine campaigns,
  host/no_std/MSRV matrix, and focused pentest.

Exit criteria:

- unauthenticated NTP is feature-complete but never mislabeled secure;
- `v0.71.0 implementation stop reached. Run pentest for this exact commit.`

## Phase 6: NTS Roughtime And Secure Bootstrap

### v0.72.0 - Generic Security Dependency Policy

Status: planned.

Goal: admit the minimum generic security boundary needed for secure time.

Deliverables:

- current Rustls, crypto-provider, AEAD, certificate, entropy, and
  secret-container reviews;
- exact feature/transitive/native/MSRV/license inventories;
- provider traits that expose no time-protocol semantics.

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
- exact exporter label/context and directional key derivation requests;
- endpoint, algorithm, cookie, shutdown, and transcript policy.

Verification:

- RFC transcript cases, wrong/missing ALPN, TLS downgrade, exporter context
  bytes, partial records, duplicate negotiation, and mock session failures.

Exit criteria:

- the state machine cannot accept an unauthenticated or wrong-protocol session;
- `v0.74.0 implementation stop reached. Run pentest for this exact commit.`

### v0.75.0 - Rustls NTS-KE Adapter

Status: planned.

Goal: integrate reviewed Rustls TLS 1.3 for NTS-KE.

Deliverables:

- client/server adapter behind `std` and `rustls` features;
- application-provided crypto provider and trust configuration;
- certificate-time bootstrap policy without disabling validity checks.

Verification:

- Rustls interop, wrong identity, expired/not-yet-valid chain, trust anchor,
  ALPN, TLS version, close, fragmentation, and provider matrix tests.

Exit criteria:

- Rustls supplies TLS only; all NTS behavior remains Mundilfari-owned;
- `v0.75.0 implementation stop reached. Run pentest for this exact commit.`

### v0.76.0 - NTS AEAD And Extension Protection

Status: planned.

Goal: implement NTS-protected NTP extension construction.

Deliverables:

- provider-backed mandatory AES-SIV-CMAC-256;
- unique identifier, cookie, placeholders, authenticator/encrypted extension;
- associated data, nonce, padding, directional key, and NAK policy.

Verification:

- RFC and AEAD vectors, tamper at every region, nonce/padding boundaries,
  wrong direction/key, unknown encrypted fields, and constant-time failure
  review.

Exit criteria:

- generic AEAD code never decides NTS field meaning or ordering;
- `v0.76.0 implementation stop reached. Run pentest for this exact commit.`

### v0.77.0 - NTS Client And Cookie Jar

Status: planned.

Goal: deliver a complete bounded NTS client.

Deliverables:

- NTS-KE plus protected NTP orchestration;
- fixed-capacity cookie jar, generation, endpoint, expiry, use, and replenish;
- replay/failure/rekey state and persistence boundary.

Verification:

- public server interop, cookie exhaustion/reuse prevention, replay, server
  restart, key rotation, endpoint migration, tamper, and long simulation.

Exit criteria:

- an authenticated observation retains separate delay/accuracy uncertainty;
- `v0.77.0 implementation stop reached. Run pentest for this exact commit.`

### v0.78.0 - NTS Server

Status: planned.

Goal: deliver NTS-KE and protected NTP server operation.

Deliverables:

- cookie construction/key rotation, stateless validation where applicable;
- bounded expensive-work admission and rate limits;
- rekey overlap, NAK, algorithm, endpoint, and certificate policy.

Verification:

- independent client interop, flood/amplification, invalid-cookie CPU budget,
  key rotation/restart, certificate rotation, replay, and malformed records.

Exit criteria:

- unauthenticated traffic cannot force unbounded crypto or response work;
- `v0.78.0 implementation stop reached. Run pentest for this exact commit.`

### v0.79.0 - Roughtime

Status: planned.

Goal: implement the exact pinned Roughtime protocol revision.

Deliverables:

- request/server codecs, nonce linkage, Merkle path, delegation, signature,
  midpoint/radius interval, and chain evidence;
- provider-backed signatures and pinned server identities;
- revision-specific experimental namespace until finalized.

Verification:

- official/reference vectors, tag/length/duplicate errors, nonce mismatch,
  Merkle/signature/delegation failure, radius bounds, chain inconsistency, and
  server interop.

Exit criteria:

- Roughtime yields authenticated intervals and never steps a clock directly;
- `v0.79.0 implementation stop reached. Run pentest for this exact commit.`

### v0.80.0 - Secure Time Bootstrap

Status: planned.

Goal: resolve certificate validation when civil time is initially untrusted.

Deliverables:

- pinned Roughtime/NTS key, provisioned interval, hardware clock, persisted
  interval plus monotonic elapsed, and SPKI-pin policies;
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
- secret lifecycle and side-channel review;
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
- explicit provider and conformance non-claims.

Verification:

- missing/contradictory evidence, stale provider, unknown scale, malicious
  uncertainty, source replacement, and custom no_std provider fixtures.

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

### v0.89.0 - Physical Source Fusion And Spoof Monitoring

Status: planned.

Goal: compare generic externally validated observations, PPS, IRIG, radio, and
local oscillators securely without requiring Navheim.

Deliverables:

- inconsistency, propagation, delay, health, authentication, and common-mode
  source models;
- preserved provider health, spoof/meaconing evidence, and invalidations;
- no automatic trust solely from physical origin.

Verification:

- mixed simulator/hardware attacks, common antenna/reference, delayed
  authenticated external evidence, radio spoof, oscillator fault, and
  split-brain cases.

Exit criteria:

- physical source authentication and path-delay risk remain separate;
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

### v0.91.0 - PTP Wire Formats

Status: planned.

Goal: implement IEEE 1588-2008/2019 wire formats and shared TLVs.

Deliverables:

- all event/general messages, headers, timestamp fields, correction, ports,
  sequence, flags, and required TLVs;
- unknown TLV preservation and exact revision identity;
- borrowed decode/caller-owned encode.

Verification:

- licensed vectors, every message/TLV/truncation/alignment, reserved fields,
  maximum correction, arbitrary input, and round trips.

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
- software/hardware timestamp quality and sequence identity;
- asymmetry/negative-delay warnings.

Verification:

- licensed examples, reorder/loss/duplicate, wrong sequence/source, correction
  overflow, delayed transmit timestamp, asymmetry, and simulator runs.

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
  message mutation, and independent PTP implementation interop.

Exit criteria:

- ordinary-clock behavior satisfies the selected revision clause map;
- `v0.96.0 implementation stop reached. Run pentest for this exact commit.`

### v0.97.0 - Boundary Clock

Status: planned.

Goal: implement bounded multiport boundary-clock behavior.

Deliverables:

- per-port datasets/state, one selected parent, downstream master behavior;
- topology loop and domain protection;
- cross-port timestamp/servo coordination.

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
- bounded management datasets and YANG mapping;
- remote mutation authorization disabled by default.

Verification:

- licensed vectors, unknown/critical TLVs, targeting, fragmentation, access
  denial, amplification/work limits, and management interop.

Exit criteria:

- unauthenticated management cannot alter live clock state;
- `v0.100.0 implementation stop reached. Run pentest for this exact commit.`

### v0.101.0 - PTP Hardware And Servo Integration

Status: planned.

Goal: integrate hardware timestamps, PHC, and PTP-oriented servo/holdover.

Deliverables:

- timestamp quality admission, PHC/system target choice, cross timestamps;
- bounded phase/frequency servo and holdover uncertainty;
- calibration and asymmetry inputs.

Verification:

- hardware NIC/PHC lab, timestamp loss/reorder, oscillator drift, grandmaster
  changes, cable asymmetry, long holdover, and fault injection.

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

### v0.104.0 - Power Media And Fronthaul Profiles

Status: planned.

Goal: implement power, broadcast/media, AES67, and fronthaul timing profiles.

Deliverables:

- IEEE C37.238, IEC/IEEE 61850-9-3, SMPTE ST 2059-2, AES67, 802.1CM, and
  applicable O-RAN timing;
- exact licensed parameters, identities, TLVs, intervals, and quality;
- no media or power-control functionality outside timing.

Verification:

- licensed vectors/conformance, equipment interoperability, wrong profile,
  domain collision, topology, grandmaster switch, and long soak.

Exit criteria:

- every profile claim names its exact revision and evidence;
- `v0.104.0 implementation stop reached. Run pentest for this exact commit.`

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
- explicit accuracy non-claims.

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

- revision-specific messages/state/security associations;
- integration with NTS provider boundaries and PTP identities;
- no stable profile leakage or silent activation.

Verification:

- draft vectors, revision mismatch, replay, key rotation, delay attack
  residuals, malformed security TLVs, and available interop.

Exit criteria:

- experimental authentication never implies delay-attack immunity;
- `v0.107.0 implementation stop reached. Run pentest for this exact commit.`

### v0.108.0 - PTP Family Security And Hardware Gate

Status: planned.

Goal: complete PTP profile conformance, hardware evidence, and security review.

Deliverables:

- revision/profile clause maps and support matrix;
- delay/topology/threat and accuracy evidence report;
- resolved critical/high parser, state, FFI, timestamp, servo, and profile issues.

Verification:

- linuxptp/vendor matrix, official suites, multi-NIC/grandmaster/switch lab,
  fuzz/simulator/soak, target matrix, and focused pentest.

Exit criteria:

- precision claims are bounded by actual measured configurations;
- `v0.108.0 implementation stop reached. Run pentest for this exact commit.`

## Phase 9: Industrial Automotive Wireless Media And Space

### v0.109.0 - BACnet And DNP3 Time

Status: planned.

Goal: implement timing services of BACnet and DNP3.

Deliverables:

- time/date, synchronization, delay, and timestamped-event objects assigned by
  licensed revisions;
- surrounding transport/application traits;
- no complete BACnet/DNP3 stack claim.

Verification:

- licensed vectors, malformed objects, sequence/delay, rollover, event order,
  simulator and independent stack interop.

Exit criteria:

- both crates expose timing only and preserve application context;
- `v0.109.0 implementation stop reached. Run pentest for this exact commit.`

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

### v0.112.0 - Industrial Ethernet Timing

Status: planned.

Goal: implement EtherCAT, PROFINET, CIP Sync, Sercos, and POWERLINK timing.

Deliverables:

- separately scoped licensed distributed-clock/time services;
- cycle/frequency/time-of-day correlation and quality;
- integration with PTP/gPTP only where normative.

Verification:

- licensed vectors, industrial simulators/equipment, cycle wrap, source loss,
  jitter, wrong profile, and topology changes.

Exit criteria:

- no crate claims surrounding motion/control protocol completeness;
- `v0.112.0 implementation stop reached. Run pentest for this exact commit.`

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
- exact licensed revisions;
- automotive safety non-claims.

Verification:

- licensed vectors, sequence/replay, gateway paths, bus loss, rate drift,
  malformed messages, and automotive simulator interop.

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

### v0.117.0 - Zigbee Matter And LoRaWAN Time

Status: planned.

Goal: implement timing services for Zigbee, Matter, and LoRaWAN.

Deliverables:

- exact time clusters/services and LoRaWAN DeviceTime request/answer;
- GPS/UTC scale identity, precision, network authority, replay, and transport
  boundary;
- no complete IoT stack.

Verification:

- licensed vectors, replay/counter, rollover, unauthorized writer, network
  delay, sleep/rejoin, malformed payload, and ecosystem interop.

Exit criteria:

- low-power network time retains scale and security provenance;
- `v0.117.0 implementation stop reached. Run pentest for this exact commit.`

### v0.118.0 - Wi-Fi TSF FTM TSCH And 6TiSCH

Status: planned.

Goal: implement wireless clock synchronization and ranging-time correlations.

Deliverables:

- TSF/FTM timing fields and 802.15.4 TSCH/6TiSCH timing services;
- local clock domain/correlation types, rollover, slot identity, and quality;
- no ranging/position calculation.

Verification:

- licensed vectors, counter wrap, AP/coordinator changes, delayed frames,
  slot drift, malicious time source, and simulator/device captures.

Exit criteria:

- local wireless clocks are not mislabeled civil UTC;
- `v0.118.0 implementation stop reached. Run pentest for this exact commit.`

### v0.119.0 - WirelessHART ISA100 And Thread Time

Status: planned.

Goal: implement timing portions of WirelessHART, ISA100, and Thread.

Deliverables:

- network time, slots, synchronization updates, source/quality, and loss state;
- accessible licensed profiles and transport boundaries;
- no general mesh stack.

Verification:

- licensed vectors, coordinator loss, slot/counter wrap, delayed/replayed
  updates, partition/merge, malformed frames, and simulator interop.

Exit criteria:

- deterministic network timing retains partition and authority state;
- `v0.119.0 implementation stop reached. Run pentest for this exact commit.`

### v0.120.0 - Cellular NITZ And 5G Time

Status: planned.

Goal: implement cellular network time and 5G reference-time mappings.

Deliverables:

- NITZ civil/zone fields and applicable 5G timing/reference information;
- source/network identity, uncertainty, replay/age, and correction policy;
- no modem or radio-access stack.

Verification:

- licensed/public vectors, zone/DST, stale network, roaming, replay, malformed
  fields, leap/scales, and modem captures.

Exit criteria:

- unauthenticated network civil time remains visibly low trust;
- `v0.120.0 implementation stop reached. Run pentest for this exact commit.`

### v0.121.0 - SMPTE MIDI AES And Broadcast Time

Status: planned.

Goal: implement SMPTE/MIDI/AES time and RDS/DVB/ATSC/ISDB timing.

Deliverables:

- frame/drop-frame, sample, broadcast civil time, offsets, quality, and
  clock-correlation types;
- exact licensed revisions and transport boundaries;
- wall time distinct from media counters.

Verification:

- licensed vectors, frame-rate/drop-frame boundaries, discontinuities,
  wraparound, signal loss, malformed fields, and equipment/file interop.

Exit criteria:

- frame and sample positions never become UTC without correlation;
- `v0.121.0 implementation stop reached. Run pentest for this exact commit.`

### v0.122.0 - RTP MPEG DASH HLS And SCTE Timing

Status: planned.

Goal: implement packet/media/web presentation timing and wall-clock correlation.

Deliverables:

- RTP/RTCP correlation, MPEG PTS/DTS/PCR, DASH/HLS/SCTE timing constructs;
- wrap/discontinuity, clock identity, capture, and synchronization metadata;
- no media codec/player implementation.

Verification:

- RFC/licensed vectors, counter wrap, discontinuity, jitter/reorder, wrong
  sender mapping, manifest extremes, and reference tool interop.

Exit criteria:

- media timeline and civil timeline stay type-distinct;
- `v0.122.0 implementation stop reached. Run pentest for this exact commit.`

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

- binding/coverage semantics, protected/unprotected header policy, token chains;
- exact licensed ETSI scope and algorithm policy;
- unknown critical field handling.

Verification:

- RFC/licensed vectors, coverage substitution, duplicate headers, wrong
  countersignature, malformed chains, algorithm downgrade, and interop.

Exit criteria:

- evidence is cryptographically bound to the intended object and context;
- `v0.129.0 implementation stop reached. Run pentest for this exact commit.`

### v0.130.0 - X9.95 Authenticode And OpenTimestamps

Status: planned.

Goal: implement remaining registry timestamp evidence families.

Deliverables:

- legitimately licensed ANSI X9.95 profile;
- Authenticode timestamp compatibility;
- OpenTimestamps generation/verification and calendar proof handling.

Verification:

- licensed/public vectors, cross-protocol confusion, digest/nonce/policy
  mismatch, calendar equivocation, malformed proofs, and ecosystem interop.

Exit criteria:

- each evidence family retains its own trust and renewal semantics;
- `v0.130.0 implementation stop reached. Run pentest for this exact commit.`

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

### v0.133.0 - Generic Source Consensus

Status: planned.

Goal: combine validated observations from different protocol families.

Deliverables:

- normalization, uncertainty expansion, correlated groups, supported interval,
  authentication/diversity policy, split-brain, and evidence;
- bounded sources and stable result ordering;
- no clock change authority.

Verification:

- NTP/NTS/Roughtime/PTP/generic-external/radio mixed simulations, Byzantine
  coalitions, common upstreams, partitions, stale sources, and interval
  properties. Navheim is represented only by protocol-neutral fixtures here.

Exit criteria:

- cross-protocol consensus reports synchronized, rough, split, insufficient,
  or unsafe explicitly;
- `v0.133.0 implementation stop reached. Run pentest for this exact commit.`

### v0.134.0 - PLL FLL And Hybrid Servo

Status: planned.

Goal: implement bounded fixed-point software clock servos.

Deliverables:

- step-only test, slew, PLL, FLL, and hybrid control;
- phase/frequency limits, panic thresholds, startup/recovery policy;
- explicit measurement uncertainty and target capability.

Verification:

- analytical traces, drift/noise/step/loss simulations, saturation, numerical
  stability, reference implementation comparison, and property tests.

Exit criteria:

- servos cannot issue out-of-policy adjustments;
- `v0.134.0 implementation stop reached. Run pentest for this exact commit.`

### v0.135.0 - PTP And Kalman-Style Servo

Status: planned.

Goal: implement high-rate phase/frequency estimation for precision clocks.

Deliverables:

- PTP-oriented servo and bounded fixed-point Kalman-style estimator;
- covariance/uncertainty, outlier, delay/asymmetry, and reset behavior;
- no floating-point requirement in no_std core.

Verification:

- recorded PHC traces, simulated oscillator/noise models, numerical extremes,
  convergence, malicious delay, and independent estimator comparison.

Exit criteria:

- estimator uncertainty grows honestly when assumptions fail;
- `v0.135.0 implementation stop reached. Run pentest for this exact commit.`

### v0.136.0 - Holdover Models

Status: planned.

Goal: implement oscillator holdover and uncertainty growth.

Deliverables:

- age/frequency/stability/temperature observation model;
- configurable oscillator classes and conservative fallback;
- source loss/recovery state and persisted calibration provenance.

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
- monotonic nonrollback reads, uncertainty, UTC/POSIX conversion policy;
- persistence and restart bootstrap boundary.

Verification:

- concurrent reads, clock rollback, system step, suspend/restart, leap/smear,
  holdover, split-brain, and monotonicity properties.

Exit criteria:

- applications can read trusted time without a network request per event;
- `v0.137.0 implementation stop reached. Run pentest for this exact commit.`

### v0.138.0 - Easy Blocking APIs

Status: planned.

Goal: expose safe one-shot application APIs.

Deliverables:

- local clock, SNTP, NTP, NTS, Roughtime, TIME, and selected source builders;
- explicit protocol/security defaults, timeout, endpoint, and report;
- no silent fallback or automatic system-clock change.

Verification:

- compile examples, error ergonomics, feature combinations, local simulators,
  public interop, timeout/cancel, and misuse compile tests.

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
- representative SNTP/NTP/PTP/generic-external/IRIG examples;
- embedded transport integration guide.

Verification:

- zero/minimum/maximum capacity, stack-size reports, no allocator link,
  embedded targets, examples, and compile-fail overflow cases.

Exit criteria:

- Level A protocol use is practical and documented;
- `v0.140.0 implementation stop reached. Run pentest for this exact commit.`

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

- unprivileged workers/consensus, typed authenticated local IPC, minimal helper;
- bounded slew/step/leap/PHC commands, startup-only step policy, audit records;
- Linux reference plus supported platform service designs.

Verification:

- IPC fuzzing, command authorization, compromised-worker simulation, socket/file
  permissions, restart, downgrade, service sandbox, VM clock tests, and soak.

Exit criteria:

- daemon compromise outside the helper cannot issue arbitrary privileged calls;
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
- generated header and ABI compatibility policy;
- no unbounded allocation or Rust layout exposure.

Verification:

- C/C++ consumers on Linux/Windows/macOS, null/length/alias misuse, ABI layout,
  symbol version, sanitizer, and fuzz tests.

Exit criteria:

- invalid foreign input cannot unwind across or corrupt the ABI;
- `v0.144.0 implementation stop reached. Run pentest for this exact commit.`

### v0.145.0 - WASM And Browser-Safe APIs

Status: planned.

Goal: expose safe browser-compatible time parsing and evidence verification.

Deliverables:

- core conversions, RFC 3339/IXDTF/TZif, packet inspection, Roughtime and
  timestamp-evidence verification;
- caller-provided JavaScript transport hooks;
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

- API/feature/capability truth review;
- privilege, IPC, config, C/WASM, observability, and cross-protocol threat
  reports;
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

- exact native-scale and TAI mapping with checked arithmetic;
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

Goal: make Navheim invalidation and discontinuity authoritative downstream.

Deliverables:

- artifact/generation/sequence identity and explicit source withdrawal;
- stale-model, receiver-reset, outage, backward-step, security-transition, and
  replacement handling;
- bounded backpressure that cannot silently drop invalidation.

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

### v0.156.0 - Navheim Interoperability And Security Gate

Status: planned.

Goal: approve the complete companion boundary before GNSS may influence a
clock.

Deliverables:

- full stable Navheim event coverage and version-compatibility report;
- independent scale/leap model disagreement evidence;
- resolved critical/high conversion, invalidation, PPS, downgrade, and
  dependency-direction findings.

Verification:

- Navheim replay/simulator/receiver matrix, all companion fuzz/property
  suites, no_std/MSRV/feature graphs, long-duration timing, hardware PPS, and
  focused pentest.

Exit criteria:

- GNSS clock use is evidence-backed without any duplicated GNSS decoder;
- `v0.156.0 implementation stop reached. Run pentest for this exact commit.`

### v0.157.0 - CGGTTS Interchange

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
- full corpus minimization and panic/timeout triage;
- remediated superlinear or unbounded paths.

Verification:

- continuous structure-aware fuzzing, worst-case benchmarks, memory limits, and
  arbitrary-input runs.

Exit criteria:

- no known attacker-controlled unbounded work or memory remains;
- `v0.160.0 implementation stop reached. Run pentest for this exact commit.`

### v0.161.0 - Unsafe FFI And Platform Review

Status: planned.

Goal: complete full-workspace unsafe and platform audit.

Deliverables:

- every unsafe block/invariant/caller audit;
- ABI drift, ancillary parsing, PHC/PPS, raw socket, and clock-control review;
- sanitizer/Miri coverage and remediated findings.

Verification:

- supported host/architecture matrix, fault injection, kernel ABI checks, and
  focused platform pentest.

Exit criteria:

- no undocumented unsafe or unchecked privileged boundary remains;
- `v0.161.0 implementation stop reached. Run pentest for this exact commit.`

### v0.162.0 - Crypto TLS And Side-Channel Review

Status: planned.

Goal: independently audit every generic crypto/TLS consumer and secret path.

Deliverables:

- dependency/provider/algorithm inventory and update check;
- transcript, exporter, AEAD, signature, certificate, entropy, cookie, and
  secret lifecycle review;
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
- documented measured accuracy envelopes and failures.

Verification:

- environmental drift, network partitions, grandmaster/source changes, disk
  faults, suspend/reboot, leap/rollover simulation, and hardware measurements.

Exit criteria:

- every precision/holdover claim has reproducible evidence;
- `v0.163.0 implementation stop reached. Run pentest for this exact commit.`

### v0.164.0 - Supported Target And no_std Closure

Status: planned.

Goal: close the advertised compiler, platform, and feature matrix.

Deliverables:

- Rust `1.90.0..=1.97.1`, Linux, Windows, BSD, macOS, Android, iOS, embedded,
  WASM, and future-Aesynx readiness report;
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
- all accessible stable entries complete and blocked entries justified.

Verification:

- official publisher/source comparison, hashes, clause maps, and independent
  completeness review.

Exit criteria:

- no known accessible stable-baseline protocol is silently omitted;
- `v0.165.0 implementation stop reached. Run pentest for this exact commit.`

### v0.166.0 - API Documentation And Semver Freeze

Status: planned.

Goal: freeze production public APIs and documentation.

Deliverables:

- all public items documented with security invariants and examples;
- semver/feature/public dependency review;
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
- complete audit, pentest, conformance, hardware, provenance, and SBOM bundle.

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
