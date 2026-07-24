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
radio, GNSS timing, industrial systems, and precision timing.

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
`1.0.0` or carries an explicit blocked/unavailable status and non-claim.

## 2. Non-Negotiable Boundaries

### 2.1 Time, not navigation

Mundilfari owns GNSS timing only. It may decode or preserve non-time fields
needed to validate the containing message, but it does not expose positioning,
velocity, altitude, pseudorange, ephemeris navigation, RTK, PPP, geodesy, map,
route, or receiver-navigation APIs. Those belong to Navheim.

Timing crate names make this explicit:

- `mundilfari-gps-time`;
- `mundilfari-galileo-time`;
- `mundilfari-beidou-time`;
- `mundilfari-glonass-time`;
- `mundilfari-nmea0183-time`;
- `mundilfari-nmea2000-time`;
- `mundilfari-rtcm-time`.

### 2.2 First-party time semantics

Mundilfari implements itself:

- exact time and duration domains;
- epochs, eras, rollover, calendars, scales, and leap seconds;
- uncertainty, quality, provenance, and clock correlation;
- bounded wire parsing and encoding for every time protocol;
- protocol validation, state machines, timers, clients, and servers;
- NTP filtering, selection, combining, poll control, and Khronos behavior;
- NTS-KE records, exporter contexts, cookies, and NTP extension construction;
- PTP messages, datasets, BMCA, port state machines, profiles, and monitoring;
- GNSS timing, PPS correlation, IRIG, radio, media, industrial, and space time;
- consensus, servo, holdover, virtual clocks, and discipline policy;
- security decisions specific to time and each protocol.

Mundilfari does not rebuild generic infrastructure merely to claim zero
dependencies. A reviewed dependency may supply TLS, X.509, generic
cryptographic primitives, a required AEAD, OS ABI declarations, or another
mature non-time facility.

Dependencies that replace the project's purpose remain forbidden: general
time/date models, NTP/PTP implementations, NMEA time parsers, generic parser
combinators used instead of first-party bounded wire code, and hidden runtime
or serialization defaults.

### 2.3 `no_std` first

Published crates declare one capability level:

| Level | Environment | Expected work |
| --- | --- | --- |
| A | `no_std`, no allocation | domains, arithmetic, wire codecs, fixed state machines |
| B | `no_std` + `alloc` | owned messages, dynamic source sets, evidence chains |
| C | `std` | sockets, files, DNS, threads, trust stores, applications |
| D | privileged platform | raw sockets, PHC/PPS, hardware timestamps, clock discipline |

Protocol crates default to Level A whenever the protocol permits it:

```toml
[features]
default = []
alloc = []
std = ["alloc"]
client = []
server = []
```

Features are additive. No feature silently enables a privileged action,
insecure fallback, historical protocol, active draft, network runtime, or
system-clock modification.

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

`mundilfari-platform` owns native sockets, DNS adapters, timestamps, raw links,
serial and capture adapters, PHC, PPS, platform clock access, system-clock
adjustment, and narrowly isolated unsafe/FFI.

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

### 3.3 Repository-only packages

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

### 3.4 Dependency direction

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
- platform crates do not contain protocol validation policy;
- the engine consumes validated observations, not untrusted packets;
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
`attoseconds < 1_000_000_000_000_000_000`. Arithmetic is checked. Conversions
return rounding and quantization evidence.

### 4.2 Native representation

Decoding preserves both native and normalized forms:

```rust
pub struct ProtocolTimestamp<R> {
    raw: R,
    normalized: AtomicInstant,
    quantization: Duration,
    rounding: RoundingDirection,
}
```

NTP binary fractions, PTP scaled nanoseconds, GPS weeks, broadcast counters,
and device-specific epochs are not destructively rounded on parse.

### 4.3 Explicit scale and context

UTC, TAI, UT1, POSIX, NTP, PTP, GPS, Galileo, BeiDou, GLONASS, terrestrial,
and coordinate time scales remain distinct. Scale conversion requires the
appropriate versioned leap, Earth-orientation, and GNSS-offset context.

UTC can represent leap second 60. Negative leap seconds are structurally
supported. POSIX conversion requires an explicit repeat, clamp, reject, or
smear policy. A smear is never labeled true UTC.

### 4.4 Era resolution

Truncated or wrapping timestamps require a caller-visible `EraContext`.
Ambiguous RFC 868, NTP, GPS week, PTP, media, broadcast, uptime, and mission
epoch values fail rather than silently choosing the nearest era.

### 4.5 Observation, not magic timestamp

A usable reading contains:

- an earliest/latest interval;
- an estimated instant;
- monotonic capture correlation;
- local offset and optional network delay;
- resolution, precision, uncertainty, age, stability, traceability, leap, and
  holdover state;
- authentication class separate from measured or advertised accuracy;
- source, protocol, authority, path, raw-observation hash, and warnings.

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
`core::future`; Mundilfari does not require Tokio or another runtime.

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

## 8. Standards Governance

Before implementation, every protocol records:

- publisher, identifier, title, revision, date, and status;
- normative/informative classification;
- official source and verified errata;
- local hash where a licensed copy is lawfully held;
- redistribution restrictions;
- implemented and excluded clauses;
- official vectors and conformance source;
- last review date and draft pin.

Licensed standards are not committed without redistribution permission.
Implementation is based on legitimate normative access, not random summaries
or reverse-engineered field guesses.

Drafts use revision-specific experimental features and namespaces. A final RFC
or standard becomes a distinct revision; stored draft packets are never
reinterpreted silently.

## 9. Testing Strategy

Every implemented unit has positive, boundary, malformed, state, replay,
timeout, rollover, leap, resource, round-trip, and regression tests.

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
- changed-scope pentest and remediation before the tag.

External test programs and fuzz engines may be CI tools without becoming
runtime dependencies.

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

The root README and `crates/mundilfari/README.md` remain byte-identical.
Published protocol crates use the common Mundilfari header and their own
accurate scope/status README. Repository-only crates may link to root
documentation instead.

`1.0.0` is the first serious production release. It is not tagged while any
stable registry entry is silently missing, a default protocol has unresolved
high/critical findings, claimed no_std/OS support lacks builds, privileged
discipline lacks pentesting, precision lacks hardware evidence, or draft APIs
leak into stable surfaces.
