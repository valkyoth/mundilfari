# Mundilfari Implementation Plan

Status: architecture baseline for `v0.1.0`

This plan converts the final decisions in [IDEA.md](IDEA.md) into an
implementation architecture. The detailed version-by-version order lives in
[RELEASE_PLAN.md](RELEASE_PLAN.md). When the two documents differ, the later
reviewed release-plan change controls implementation order; neither document
overrides a normative protocol specification.

## 1. Mission

Mundilfari implements time representation, transfer, synchronization,
discipline, verification, and evidence across software, networks, hardware,
radio, GNSS-derived observations, industrial systems, and precision timing.

The project must make easy work easy without hiding expert controls:

- one-shot local or remote time observations;
- long-running trusted application clocks;
- embedded fixed-storage clients;
- time clients and servers;
- packet inspection and generation;
- a privilege-separated synchronization daemon;
- hardware timestamp, PHC, PPS, and signal capture;
- source consensus, servo, and holdover;
- timestamp-evidence generation and verification;
- conformance, simulation, fuzzing, and hardware-lab use.

The project does not claim literal knowledge of every proprietary or lost
protocol. Its completeness contract is the reviewed registry in
[PROTOCOLS.md](PROTOCOLS.md): every public, legitimately accessible, stable
time protocol in scope by the baseline date is either implemented before
`1.0.0`, consumed through an explicit reviewed upstream boundary, or carries
an explicit blocked/unavailable status and non-claim.

## 2. Non-Negotiable Boundaries

### 2.1 Generic time, not GNSS interpretation

Navheim determines time from satellite-navigation signals, navigation
messages, receiver protocols, corrections, and receiver timing outputs.
Mundilfari consumes Navheim's validated result as one clock source.

Mundilfari does not decode GNSS frames, NMEA, RTCM, RINEX, gpsd, or vendor
receiver protocols. It does not resolve native GNSS weeks or eras, interpret
transmitted UTC models, calculate satellite or receiver clock corrections,
verify OSNMA/QZNMA, assess GNSS health, or assign GNSS meaning to a receiver
PPS edge. It also has no position, velocity, pseudorange, ephemeris, RTK, PPP,
geodesy, or receiver-navigation API.

One optional published crate, `mundilfari-navheim`, maps the stable Navheim
timing event API into Mundilfari observations. It is implemented only after
Navheim is built and publishes a reviewed stable boundary. The detailed
contract is [NAVHEIM_INTEGRATION.md](NAVHEIM_INTEGRATION.md).

This dependency is intentionally introduced in the final feature phase.
Mundilfari completes every generic and non-Navheim protocol, source-engine,
servo, application, and product-security milestone first. Only conformance
closure, system-wide audits, release candidates, and `1.0.0` follow the
companion phase.

### 2.2 First-party time semantics

Mundilfari implements itself:

- exact time and duration domains;
- protocol-neutral epochs, eras, rollover, calendars, scales, and leap
  seconds;
- uncertainty, quality, provenance, and clock correlation;
- bounded wire parsing and encoding for every Mundilfari-owned time protocol;
- protocol validation, state machines, timers, clients, and servers;
- NTP filtering, selection, combining, poll control, and Khronos behavior;
- NTS-KE records, exporter contexts, cookies, and NTP extension construction;
- PTP messages, datasets, BMCA, port state machines, profiles, and monitoring;
- generic PPS capture, IRIG, radio, media, industrial, and non-GNSS space
  time;
- exact, fail-closed mapping of Navheim timing evidence in the companion crate;
- consensus, servo, holdover, virtual clocks, and discipline policy;
- security decisions specific to time and each protocol.

Mundilfari does not rebuild generic infrastructure merely to claim zero
dependencies. A reviewed dependency may supply TLS, X.509, generic
cryptographic primitives, a required AEAD, OS ABI declarations, or another
mature non-time facility.

Dependencies that replace the project's purpose remain forbidden: general
time/date models, NTP/PTP implementations, generic parser combinators used
instead of first-party bounded wire code, and hidden runtime or serialization
defaults. Navheim is the deliberate GNSS implementation boundary, but only
`mundilfari-navheim` may depend on it.

### 2.3 Capability and authority tiers

Published crates declare one capability tier:

| Tier | Environment | Expected work |
| --- | --- | --- |
| Core | `no_std`, no allocation | domains, arithmetic, wire codecs, fixed state machines |
| Alloc | `no_std` + `alloc` | owned messages, dynamic source sets, evidence chains |
| Standard | `std` | safe clocks, sockets, DNS, files, TLS adapters, applications |
| Device | explicit platform features | PHC/PPS, hardware timestamps, raw links, device discovery |
| Discipline | separate crate/process | system, PHC, or oscillator modification through authorization handles |

Protocol crates default to the Core tier whenever the protocol permits it:

```toml
[features]
default = []
alloc = []
std = ["alloc"]
udp = ["std"]
dns-system = ["std"]
rustls = ["std", "dep:rustls"]
linux-timestamping = ["std"]
linux-phc-read = ["std"]
linux-clock-adjust = ["std"]
client = []
server = []
```

Features are additive. No feature silently enables a privileged action,
insecure fallback, historical protocol, active draft, network runtime, or
system-clock modification. A feature reports that code was compiled; it never
asserts that a device exists, a process is authorized, or a source is healthy.
Runtime capability reports distinguish `Compiled`, `Available`, `Authorized`,
and `Healthy`, with reason-bearing failure states.

## 3. Crate Architecture

### 3.1 Shared crates

The final IDEA discussion deliberately reduces the original proliferation of
tiny foundation crates:

```text
mundilfari
├── mundilfari-core
├── mundilfari-engine
└── mundilfari-platform
```

`mundilfari-core` owns common time types, calendars, scales, leap data models,
uncertainty, provenance, bounded containers, wire cursors, checksums, common
transport traits, and clock traits.

`mundilfari-engine` owns multi-source consensus, source diversity,
clock-filter building blocks, servos, holdover, trusted virtual clocks,
discipline policy, and runtime-neutral orchestration.

`mundilfari-platform` owns safe native sockets, DNS adapters, timestamps, raw
links, serial and capture adapters, PHC, PPS, platform clock access, and
clock-control wrappers. It remains unsafe-free.

Small OS-family-specific `mundilfari-platform-*-sys` crates own only necessary
FFI, syscall, ancillary-layout, volatile MMIO, or intrinsic boundaries. They
are not facade re-exports, never contain protocol policy, and are covered by a
machine-readable unsafe inventory. Clock discipline lives behind a separate
authorization boundary and ultimately a minimal helper process.

`mundilfari` is a facade. It provides stable re-exports, easy builders,
protocol selection, common reports, and optional application-facing helpers.
It is never the implementation home for a large protocol.

### 3.2 Protocol crates

Each independently standardized protocol or tightly coupled family receives a
focused crate. Shared wire layouts are split only when multiple independently
useful protocol engines need them. For example:

```text
mundilfari-ntp-wire
├── mundilfari-sntp
├── mundilfari-ntp
└── mundilfari-nts
```

NTS remains one protocol crate internally divided into records, negotiation,
exporter context, cookies, extensions, client, server, AEAD provider, and
optional Rustls integration. It is not fragmented into adapter microcrates.

PTP wire formats and the general engine may be split because profiles and
inspection tools need the shared codec independently:

```text
mundilfari-ptp-wire
├── mundilfari-ptp
├── mundilfari-gptp
├── mundilfari-ptp-telecom
├── mundilfari-ptp-power
├── mundilfari-ptp-media
└── mundilfari-white-rabbit
```

### 3.3 Navheim companion crate

After Navheim's serious stable timing release and after all
Navheim-independent Mundilfari feature work:

```text
navheim                 mundilfari-core
   \                         /
    +--- mundilfari-navheim -+
                 |
          mundilfari-engine
```

Navheim owns independent GNSS types and never depends on Mundilfari.
`mundilfari-navheim` depends on both projects, preserves all upstream evidence,
and may optionally integrate `mundilfari-platform` generic PPS capture.
Mundilfari's core, engine, platform, facade, and protocol crates never depend
on Navheim.

The companion maps observations, model changes, ambiguity, gaps,
discontinuities, invalidations, and security transitions. It cannot decode or
reinterpret GNSS. Navheim is absent from every default feature graph.

This is the final feature-bearing crate phase. CGGTTS follows the adapter
evidence mapping within that same phase because its GNSS common-view and
all-in-view inputs are supplied by Navheim. No later milestone adds protocol
scope.

### 3.4 Repository-only packages

The following stay `publish = false` and may require Rust `1.97.1`:

- `mundilfari-xtask`;
- release and repository validators;
- fuzz drivers and corpus minimizers;
- simulators used only by this repository;
- packet/hardware lab binaries;
- interoperability harnesses;
- benchmark, fixture-import, and standards-audit programs;
- daemon packaging helpers.

A testkit is published only if downstream users need stable public fixtures or
conformance helpers. Otherwise it remains repository-only.

### 3.5 Dependency direction

```text
core domains and bounded wire utilities
                 ↓
        protocol codecs/state
                 ↓
 platform transports and profile adapters
                 ↓
 consensus/servo/orchestration engine
                 ↓
  facade, CLI, daemon, C/WASM interfaces
```

Enforced rules:

- core never depends on protocol, platform, or facade crates;
- protocol wire modules never depend on OS code;
- protocol crates never depend on the facade;
- generic crypto adapters do not own time-protocol decisions;
- safe platform crates do not contain unsafe or protocol validation policy;
- only narrowly scoped `mundilfari-platform-*-sys` crates may contain
  registered unsafe code;
- the engine consumes validated observations, not untrusted packets;
- only `mundilfari-navheim` may depend on Navheim;
- an upstream invalidation must withdraw the corresponding engine observation;
- experimental drafts cannot leak draft-only public types into stable crates;
- profiles depend on base protocol engines, never the reverse;
- dependency cycles and out-of-layer edges fail the local gate.

## 4. Canonical Time Model

The canonical model is not `std::time::SystemTime`.

### 4.1 Continuous instant

`AtomicInstant` uses signed seconds and normalized attoseconds on a documented
continuous origin:

```rust
pub struct AtomicInstant {
    seconds: i128,
    attoseconds: u64,
}
```

All constructors preserve the invariant
`0 <= attoseconds < 1_000_000_000_000_000_000`, and `seconds` is the
mathematical floor of the represented value, including for negative instants.
Thus negative one-half second is represented as `(-1, 5e17)`. Fields remain
private, arithmetic and normalization are checked with wide intermediates,
and public serialization never freezes the Rust memory layout.

### 4.2 Native representation

Decoding preserves both native and normalized forms:

```rust
pub struct ProtocolTimestamp<R> {
    raw: R,
    normalized: AtomicInstant,
    exact: RationalInstant,
    error: Interval<AtomicInstant>,
    rounding: RoundingMode,
}
```

NTP binary fractions, PTP scaled nanoseconds, broadcast counters, and
device-specific epochs are not destructively rounded on parse. The rational
quantum and lower/upper residual bounds are retained because many binary and
scaled fractions are not integral attoseconds. Full instants are never
flattened into `i128` attoseconds. A resolved Navheim native GNSS instant is
mapped without truncation by the companion; it is not parsed from GNSS wire
data here.

### 4.3 Explicit scale and context

UTC, TAI, UT1, POSIX, NTP, PTP, GPS, Galileo, BeiDou, GLONASS, terrestrial,
and coordinate time scales remain distinct. Conversion uses explicit
operations under one immutable, versioned `ConversionContext`; it is not a
general path-search graph that may mix model generations. NTP is an epoch/wire
encoding with UTC semantics, PTP may distribute its defined timescale or an
arbitrary timescale, GLONASS is not treated as a fixed-offset continuous
scale, and UT1 or relativistic coordinate scales require named admitted
models and uncertainty. UTC before 1972 has an explicit non-claim until a
historical frequency-offset model is admitted.

Mundilfari keeps generic scale identifiers and versioned conversion context so
GNSS-derived observations can be compared with other clocks. Navheim
independently resolves native GNSS values; disagreement between its result and
Mundilfari's admitted scale/leap model is visible and fail-closed.

UTC can represent leap second 60. Negative leap seconds are structurally
supported. POSIX conversion returns a typed `Unique`, `Ambiguous`, or
`Nonexistent` outcome before an explicit repeat, clamp, reject, or smear policy
is applied. Smears carry provider/profile, window, function, model generation,
and invertibility limitations. A smear is never labeled true UTC.

### 4.4 Era resolution

Truncated or wrapping Mundilfari protocol timestamps require a caller-visible
`EraContext`. Ambiguous RFC 868, NTP, PTP, media, broadcast, uptime, and
mission epoch values fail rather than silently choosing the nearest era.
Navheim alone resolves truncated GNSS weeks/days/eras. The companion accepts
resolved evidence or rejects the observation.

### 4.5 Observation, not magic timestamp

A usable reading contains:

- an earliest/latest interval;
- a preferred estimate only when policy permits one;
- scale and realization identity;
- monotonic capture correlation;
- local offset and optional network delay;
- resolution, precision, uncertainty, age, stability, traceability, leap, and
  holdover state;
- authentication class separate from measured or advertised accuracy;
- source generation, protocol, authority, path, raw-observation hash, and
  warnings.

`query_once()` performs acquisition and returns a bounded `TimeEstimate`.
`TrustedClock::now()` performs no network I/O and reads an already
synchronized virtual application clock. Mobile and browser defaults are
application clocks, not system discipline. Every C, WASM, Java/Kotlin, Swift,
database, `time_t`, and JavaScript boundary rejects out-of-range narrowing.

## 5. Protocol Implementation Template

Each protocol crate is divided by responsibility:

```text
src/
├── lib.rs
├── constants.rs
├── wire.rs
├── message.rs
├── decode.rs
├── encode.rs
├── validate.rs
├── state.rs
├── client.rs
├── server.rs
├── policy.rs
├── error.rs
└── std_support.rs
```

Only relevant files are created. No non-generated Rust source file may exceed
500 lines; review for splitting begins near 300 lines.

### 5.1 Parse, validate, authorize

The stages are separate:

1. structural parse preserves original bytes and unknown fields;
2. semantic validation applies the exact revision and errata;
3. protocol-state validation applies expected peer, nonce, sequence, timer,
   replay, and resource policy;
4. source policy decides whether an observation may reach consensus;
5. discipline policy decides whether a result may influence a clock.

Forensic decoding never grants clock authority.

Where useful, distinct types enforce the progression from raw bytes through
parsed, semantically valid, association-valid, authenticated, observed,
consensus, and discipline-proposal states. Forensic and compatibility values
do not implement the trait accepted by consensus. Runtime `trusted: bool`
flags are not substitutes for these type boundaries.

### 5.2 Borrowed and bounded

The primary decoder borrows input, performs no allocation, validates lengths
before arithmetic or slicing, preserves unknown extensions, and records exact
error offsets. Encoders write to caller-owned buffers and report required
length without partial semantic success.

Decode modes are explicit: `Strict`, `Compatible`, and `Forensic`. Strict is
default. Compatibility deviations are individually documented. Forensic
values cannot enter discipline state.

### 5.3 I/O-neutral state machines

Protocols consume platform-neutral datagram, stream, raw-link, serial, edge,
sample, CAN, FlexRay, GATT, entropy, clock, and hardware-clock traits.
Canonical engines use explicit polling and timers. `Future` adapters use
`core::future`; Mundilfari does not require Tokio or another runtime. Every
timer, request, transmit timestamp, crypto operation, and hardware completion
carries an association generation token. Each poll accepts explicit monotonic
time, input, and a deterministic work budget, then emits bounded actions.

## 6. Security Architecture

### 6.1 Threat separation

The model distinguishes:

- malformed input from semantically false time;
- authenticated identity from source accuracy;
- packet integrity from packet delay;
- one source from genuinely diverse upstreams;
- UTC from POSIX, monotonic, smeared, or local-network time;
- syntactic evidence from externally certified conformance;
- clock observation from permission to modify a clock.

Consensus policy states its mathematical fault assumptions: admitted source
count `n`, maximum faulty diversity groups `f`, required interval coverage,
freshness and path-delay bounds, network-adversary reach, and whether correct
source intervals are assumed to contain true time. Source weights cannot
override the quorum. An indistinguishable malicious majority is an explicit
residual risk, not a Byzantine-resilience claim.

### 6.2 Resource governance

Every untrusted operation has explicit limits for bytes, fields, nesting,
state entries, outstanding requests, certificates, cookies, work, timers,
CPU-expensive verification, responses, logs, and evidence.

Limits required by a protocol are not confused with local deployment quotas.
Local resource exhaustion is not reported as peer cryptographic invalidity.

### 6.3 Generic security dependencies

Before the first dependency is admitted, a versioned review records:

- current release and official source;
- license and MSRV;
- maintenance and security history;
- enabled and disabled features;
- transitive and native-code graph;
- `no_std`/`alloc`/`std` impact;
- exact responsibility boundary;
- public-type leakage;
- update and replacement plan;
- known limitations and test evidence.

Rustls supplies only TLS to NTS-KE. Mundilfari still constructs and validates
NTS records, ALPN expectations, exporter contexts, negotiated algorithms,
cookies, directional keys, extension fields, replay state, and failure policy.

### 6.4 Privilege separation

The future daemon design is:

```text
unprivileged source workers
            ↓
unprivileged validation and consensus
            ↓
bounded authenticated local IPC
            ↓
minimal clock/PHC discipline helper
```

Privileged requests are typed and bounded. The helper never accepts arbitrary
paths, pointers, ioctl numbers, syscalls, packet bytes, or shell commands.
The engine emits a bounded `DisciplineProposal`; policy may turn it into a
short-lived authorized request, and the helper independently enforces phase,
frequency, slew, step, generation, and expiry bounds.

The helper is a dedicated executable with no protocol dependencies. It uses a
pre-opened socketpair or fixed local endpoint, verifies peer credentials,
accepts fixed-version and fixed-maximum-length messages, rejects replayed
sequences and stale monotonic expiries, operates only on pre-opened allowlisted
clock handles, drops privileges and sandboxes syscalls after initialization,
and appends an audit result for every accepted or rejected request. Raw capture
and clock discipline use separate authority where the OS permits it.

## 7. Platform Plan

Linux is the first full-feature reference implementation. Windows, BSD, and
macOS receive native adapters, not Linux emulation. Android and iOS support
library-safe capabilities within their application sandboxes. Protocol cores
avoid Unix-only types so Aesynx can later implement the same traits.

Platform code is staged:

1. clock and transport traits;
2. safe standard sockets and monotonic/realtime clocks;
3. software timestamp capture;
4. isolated OS-binding admission;
5. ancillary-data parsing and truncation/alignment tests;
6. raw ICMP and Ethernet;
7. hardware timestamp configuration;
8. PHC/PPS/RTC access;
9. bounded system and hardware clock adjustment;
10. per-platform interoperability and privilege tests.

Accuracy is never inferred from API availability.

Hardware samples retain raw device timestamps, origin class, device identity
and generation, monotonic/system cross timestamps, measured cross-clock error,
resolution, advertised precision, calibration, and asymmetry inputs. Core
traits use HAL-like typed clock/register operations rather than Unix file
descriptors. Linux PHC uses the kernel PTP-clock and timestamping interfaces;
MMIO is a distinct embedded adapter with volatile, alignment, endian,
ownership, ordering, and reset invariants.

## 8. Standards Governance

The repository begins with a checksum-locked source baseline:

- exact RFC Editor bytes, URLs, review roles, and milestone assignments in
  `rfc/`;
- public metadata and checksum pins for every non-RFC family in `standards/`;
- all non-RFC document bytes in ignored `standards/private/`, including public
  drafts, so uncertain redistribution can never leak to GitHub or crates.io.

The common gate validates both registries and the RFC byte set without network
access. Fetch commands are explicit maintainer operations, use fixed HTTPS
allowlists, verify pinned checksums, and never run from builds or tests.

Before implementation, every protocol records:

- publisher, identifier, title, revision, date, and status;
- normative/informative classification;
- official source and verified errata;
- local hash where a licensed copy is lawfully held;
- redistribution restrictions;
- implemented and excluded clauses;
- official vectors and conformance source;
- last review date and draft pin.

Every admitted normative reference is followed recursively. Its ledger record
names the consuming requirement, exact reviewed revision/hash, disposition,
owning crate or external provider boundary, milestone, and rationale.
References used only for registries, procedures, syntax, or transports remain
explicit; updates and obsoletes do not disappear from the audit trail. An
unclassified transitive reference blocks the consuming implementation.

Specification and implementation state are independent. The registry
distinguishes stable, historic, active-draft, monitored-proposal, licensed,
partially documented, historical-evidence-only, implementation-blocked,
unavailable, and proprietary-undocumented sources. It separately records
access, redistribution, implementation, and conformance state.

Conformance claims use independently evidenced levels:

- `WireComplete`: exact bounded encode/decode and field validation;
- `BehavioralComplete`: required protocol state and error behavior;
- `OperationalComplete`: required transports, deployment behavior, and
  interoperability;
- `ConformanceValidated`: applicable official or recognized conformance suite
  has passed.

No level is inferred from another. Acquiring a standard proves none of them.
Family/bundle entries are discovery aids only: before implementation they are
expanded into exact documents, revisions, amendments, corrigenda,
interpretations, profiles, registries, and verified errata.

Licensed standards are not committed without redistribution permission.
Implementation is based on legitimate normative access, not random summaries
or reverse-engineered field guesses.

Source admission alone is not semantic review. `v0.2.0` completes the
versioned clause and errata disposition model. Thereafter, each implementation
milestone must bind its included/excluded requirements and verified errata to
the exact source hash before code is accepted. `identifier-review`,
`revision-review`, missing manual acquisitions, and RFC 1119's text-only
catalog notice are hard milestone blockers.

The binding is enforced for every production Rust source file by
`compliance/IMPLEMENTATION_EVIDENCE.json`. A source file cannot enter a
published crate until it has exactly one implementation-unit record and the
record pins the reviewed implementation file's SHA-256. Every record names its
governing requirements and locators, and every requirement links to one or
more concrete tests whose functions exist. Protocol, format, and integration
units additionally name exact RFC/external-source identifiers, reviewed
SHA-256 values, clauses, errata dispositions, and the requirements they
govern. The offline common gate rejects missing or changed implementation
files, unknown sources, changed public hashes, unlinked requirements, and
missing tests.

This mechanical gate proves traceability, not correctness. Reviewers must
still compare behavior to every applicable normative clause, assess test
adequacy, run negative/property/fuzz/simulation/interoperability/conformance
work appropriate to the milestone, and complete its exact-commit pentest.

Drafts use revision-specific experimental features and namespaces. A final RFC
or standard becomes a distinct revision; stored draft packets are never
reinterpreted silently.

## 9. Testing Strategy

Every implemented unit has positive, boundary, malformed, state, replay,
timeout, rollover, leap, resource, round-trip, and regression tests.
Applicable cases are recorded as requirement-linked test evidence; an omitted
category needs an explicit inapplicability rationale in the milestone review.

Protocol completion additionally requires:

- official positive and negative vectors;
- parser no-panic fuzzing;
- property and invariant tests;
- deterministic simulation of delay, jitter, loss, reorder, duplication,
  asymmetry, drift, steps, malicious sources, restarts, and holdover;
- cross-endian and no_std builds;
- differential and interoperability tests against independent implementations;
- supported OS and target checks;
- hardware-in-loop evidence where the claim depends on hardware;
- WCET, stack-use, and deterministic work-budget evidence for fixed-capacity
  industrial, automotive, and bare-metal engines;
- changed-scope pentest and remediation before the tag.

External test programs and fuzz engines may be CI tools without becoming
runtime dependencies. Miri, sanitizers, and Kani claims name precisely what
was modeled or executed; they do not imply proof of a kernel, driver, DMA,
MMIO device, or unmodeled hardware.

## 10. Release And Documentation Discipline

Every release includes:

- a single reviewable goal;
- bounded deliverables;
- release-specific verification;
- exact official source revisions;
- dependency and SBOM evidence;
- release notes and known limitations;
- an implementation stop before tagging;
- exact-commit pentest, remediation, retest, and permanent PASS report.

Before `1.0.0`, independent reviewer identity and attestations, protected
release refs, reproducible archives, artifact provenance, signatures, and
archive/SBOM/hash reproduction become release gates. No ISO 26262, IEC 61508,
IEC 62443, Common Criteria, FIPS, or comparable certification is claimed
without its separate required traceability, tool qualification, safety
manuals, assessment, and integration evidence.

The root README and `crates/mundilfari/README.md` remain byte-identical.
Published protocol crates use the common Mundilfari header and their own
accurate scope/status README. Repository-only crates may link to root
documentation instead.

`1.0.0` is the first serious production release. It is not tagged while any
stable registry entry is silently missing, a default protocol has unresolved
high/critical findings, claimed no_std/OS support lacks builds, privileged
discipline lacks pentesting, precision lacks hardware evidence, or draft APIs
leak into stable surfaces.

## 11. Review Integration And Version Ownership

The July 2026 gap review strengthens the existing roadmap without replacing
its broader pre-1.0 completeness contract:

| Concern | Owning versions |
| --- | --- |
| Floor-normalized instants, wide math, rational residuals | `v0.5.0`, `v0.7.0`, `v0.9.0`, gate `v0.17.0` |
| Immutable scale contexts, POSIX outcomes, smear identity | `v0.11.0`–`v0.13.0`, gate `v0.17.0` |
| Type-state, generation tokens, work budgets | `v0.22.0`–`v0.25.0`, gate `v0.29.0` |
| Runtime capability truth and safe/sys platform split | `v0.30.0`–`v0.40.0`, final review `v0.161.0` |
| Normative dependency closure and conformance vocabulary | `v0.2.0`, final review `v0.165.0` |
| Per-source requirement and test evidence enforcement | `v0.3.0`, every common gate |
| Documented non-GNSS vendor extensions | `v0.53.0`–`v0.53.1`, final review `v0.165.0` |
| NTP fault model, delay defense, bounded servers | `v0.57.0`–`v0.71.0` |
| NTS assurance, pool key establishment, and secret lifecycle | `v0.72.0`–`v0.81.0` |
| PTP revision admission, trust boundary, measured accuracy | `v0.91.0`–`v0.108.0` |
| Deterministic industrial/automotive safety non-claims | `v0.109.0`–`v0.125.0` |
| Cross-family fault model, bounded servos, holdover | `v0.133.0`–`v0.136.0` |
| Truthful facade, application clocks, bindings | `v0.137.0`–`v0.145.0` |
| Privilege-separated helper and audit evidence | `v0.142.0`, `v0.146.0`–`v0.148.0` |
| Unsafe, targets, reproducibility, signed review closure | `v0.158.0`–`v1.0.0` |

The review's proposed narrower replacement matrix is not adopted. The
existing registry contract, Navheim-last feature order, per-milestone
verification and pentest exits, hardware evidence, and full production
admission sequence remain mandatory.
