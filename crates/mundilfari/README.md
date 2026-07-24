<p align="center">
  <b>Security-first, no_std-first time protocols for Rust.</b><br>
  Exact time semantics, bounded protocol engines, and independently pentested releases on the path to production.
</p>

<div align="center">
  <a href="https://crates.io/crates/mundilfari">Crates.io</a>
  |
  <a href="https://docs.rs/mundilfari">Docs.rs</a>
  |
  <a href="https://github.com/valkyoth/mundilfari/blob/main/docs/RELEASE_PLAN.md">Release Plan</a>
  |
  <a href="https://github.com/valkyoth/mundilfari/blob/main/docs/threat-model.md">Threat Model</a>
  |
  <a href="https://github.com/valkyoth/mundilfari/blob/main/SECURITY.md">Security</a>
</div>

<br>

<p align="center">
  <a href="https://github.com/valkyoth/mundilfari">
    <img src="https://raw.githubusercontent.com/valkyoth/mundilfari/main/.github/images/mundilfari.webp" alt="Mundilfari Rust time protocol framework">
  </a>
</p>

# Mundilfari

Mundilfari is a security-first Rust framework for time representation,
transfer, synchronization, discipline, verification, and timestamp evidence.
It is being built in small, independently reviewable releases toward a
complete time-protocol stack rather than claiming protocol or accuracy support
before evidence exists.

The project owns the time-specific work: epochs, time scales, leap seconds,
uncertainty, wire formats, validation, state machines, clock algorithms,
source selection, servos, profiles, and protocol security policy. Mature
generic cryptography, TLS, and operating-system binding crates may be admitted
only behind narrow reviewed boundaries where rebuilding them would reduce
security.

Version `0.1.0` is a repository and architecture foundation. It does not yet
provide a network time client, clock discipline, protocol parser, or production
time source.

## Scope Boundary

Mundilfari owns generic time and clock behavior. Navheim determines time from
GNSS.

Navheim will decode satellite-navigation messages and receiver protocols,
resolve native GNSS eras and weeks, interpret transmitted UTC/leap models,
apply satellite and receiver clock corrections, assess signal and receiver
health, verify navigation authentication, and determine the GNSS meaning of a
receiver PPS/time mark.

Mundilfari will consume that validated evidence through one optional
`mundilfari-navheim` companion crate. Mundilfari retains generic atomic and
civil time types, named GNSS scale identifiers, independent scale-model
validation, physical PPS capture, source consensus, servos, holdover, and
clock-discipline policy. It will not contain a second GPS, Galileo, GLONASS,
BeiDou, QZSS, NavIC, NMEA, RTCM, gpsd, or vendor-receiver decoder.

Navheim is planned and will be completed first. The companion crate is not
implemented or buildable in `v0.1.0`; its work starts only after Navheim
publishes a reviewed stable GNSS timing API.

The roadmap keeps that dependency at the end of feature development. Every
Navheim-independent protocol, generic source boundary, engine, servo, and
application milestone is completed first. The Navheim companion and CGGTTS
then form the final feature phase, followed only by whole-system hardening,
conformance closure, release candidates, and `1.0.0`.

## Planned Uses

- dependency-light `no_std` codecs and state machines;
- embedded clocks and fixed-storage time clients;
- Linux, Windows, BSD, macOS, Android, and iOS applications;
- servers, websites, observability systems, and distributed databases;
- an unprivileged synchronization daemon with a minimal privileged helper;
- NTP, SNTP, NTS, PTP, gPTP, White Rabbit, Navheim-provided GNSS time, PPS,
  IRIG, radio, broadcast, industrial, automotive, wireless, and space timing;
- trusted timestamp evidence, packet inspection, conformance testing, and
  hardware timing laboratories;
- future Aesynx integration through platform-neutral core traits.

## Workspace

| Crate | Published | Environment | Responsibility |
| --- | --- | --- | --- |
| `mundilfari` | crates.io | `no_std` by default | Stable facade and curated re-exports |
| `mundilfari-core` | crates.io | `no_std`, no allocation | Time domains, bounded wire utilities, common traits |
| `mundilfari-engine` | crates.io | `no_std` by default | Consensus, servo, holdover, and orchestration foundations |
| `mundilfari-platform` | crates.io | `no_std` core; opt-in `std` | OS, transport, hardware timestamp, PPS, and clock adapters |
| `xtask` | repository only | Rust `1.97.1` | Contributor and release automation |

Protocol families become focused crates when their implementation milestone
starts. Crates used by downstream applications are published to crates.io;
release automation, fuzz drivers, hardware-lab programs, and repository checks
stay private with `publish = false`.

After Navheim's stable timing API exists, `mundilfari-navheim` becomes an
optional published integration crate depending on Navheim, `mundilfari-core`,
and `mundilfari-engine`. Neither the Mundilfari facade nor its default graph
depends on Navheim.

## Capability Status

Legend: 🟢 available for the stated scope, 🟡 foundation only, 🔴 planned.

| Capability | Status | Current scope |
| --- | --- | --- |
| Rust workspace and facade | 🟢 Available | Four focused published crates plus a repository-only task runner |
| `no_std` default graph | 🟢 Available | No default external runtime dependencies |
| Rust compatibility | 🟢 Policy active | MSRV `1.90.0`; development pinned to stable `1.97.1` |
| Security and release controls | 🟢 Available | CI, dependency policy, release metadata, pentest handoff, SBOM tooling |
| Standards source baseline | 🟢 Available | 67 checksum-locked RFCs; 52 external-source records; restricted bytes remain local-only |
| Implementation evidence gate | 🟢 Available | Every production source maps governing requirements to concrete tests; protocol work also pins exact sources, clauses, and errata |
| Time model | 🟡 Foundation only | Module and crate boundaries are reserved; semantics begin after `v0.1.0` |
| Navheim GNSS integration | 🔴 Blocked on upstream plan | One optional companion crate after Navheim's stable timing release |
| Protocol codecs and clients | 🔴 Planned | Implemented in small versions recorded in the release plan |
| Clock discipline and daemon | 🔴 Planned | No clock modification code exists in `v0.1.0` |
| Production readiness | 🔴 Planned | Requires complete conformance, audits, hardware evidence, and `v1.0.0` admission |

## Install

The initial crate is not yet published. After the first audited release:

```toml
[dependencies]
mundilfari = { version = "0.1.0", default-features = false }
```

For the smallest foundation:

```toml
[dependencies]
mundilfari-core = { version = "0.1.0", default-features = false }
```

## Rust Version Support

The crate MSRV is Rust `1.90.0`. Release development is pinned to Rust
`1.97.1`, and the release gate checks every stable compiler line through the
pinned toolchain. The online preflight verifies that the pin remains the
current stable patch release without raising the MSRV.

| Rust | Role | Required result |
| --- | --- | --- |
| `1.90.0` | Minimum supported Rust version | Workspace check and tests |
| `1.91.0`, `1.91.1` | Supported stable line | Workspace check |
| `1.92.0` | Supported stable line | Workspace check |
| `1.93.0`, `1.93.1` | Supported stable line | Workspace check |
| `1.94.0`, `1.94.1` | Supported stable line | Workspace check |
| `1.95.0` | Supported stable line | Workspace check |
| `1.96.0`, `1.96.1` | Supported stable line | Workspace check |
| `1.97.0` | Supported stable line | Workspace check |
| `1.97.1` | Pinned stable development and release toolchain | Full release gate |

Repository-only binaries and test/hardware tooling may use the pinned Rust
`1.97.1` toolchain. Published libraries must preserve the `1.90.0` MSRV unless
a future major-version policy explicitly changes it.

## Security Model

Mundilfari treats every time input as untrusted. A syntactically valid time is
not necessarily accurate, authenticated, fresh, traceable, or safe for clock
discipline.

Security defaults include:

- parsing separated from semantic validation and discipline authority;
- bounded input, work, memory, nesting, and state;
- checked arithmetic and explicit era/leap context;
- no silent protocol downgrade or unauthenticated clock modification;
- authentication represented separately from accuracy and uncertainty;
- privilege separation for future system-clock and hardware-clock changes;
- `unsafe` forbidden in current crates and isolated later when platform FFI
  genuinely requires it;
- exact official specification revisions and verified errata recorded before
  implementation;
- immutable GitHub Action pins, current tool checks, RustSec and license/source
  policy, SBOM evidence, and a pentest before every tag.

Report vulnerabilities privately as described in
[SECURITY.md](https://github.com/valkyoth/mundilfari/blob/main/SECURITY.md).

## Dependency Policy

The current default graph has no third-party runtime dependencies.
Mundilfari will not depend on crates that replace its purpose, including
general time models or NTP/PTP implementations. Navheim is the deliberate
upstream for GNSS interpretation, but only `mundilfari-navheim` may depend on
it; the core, engine, platform, facade, and unrelated protocol crates may not.

Generic dependencies such as Rustls, a required AEAD implementation, audited
signature primitives, `libc`, or `windows-sys` may be admitted later only when:

- the functionality is not time-protocol logic;
- the current crates.io release, license, maintenance, MSRV, feature, native
  code, and transitive graph have been reviewed;
- the dependency is optional where the `no_std` core does not require it;
- a narrow Mundilfari-owned trait or adapter keeps protocol semantics local;
- threat-model, SBOM, audit, and replacement implications are documented;
- dedicated tests prove the admitted behavior and failure mode.

See [Supply-Chain Security](https://github.com/valkyoth/mundilfari/blob/main/docs/supply-chain-security.md).

## Platform Direction

Pure protocol logic must stay portable. Platform support is introduced behind
separate adapters:

| Platform | Day-one architecture promise |
| --- | --- |
| Linux | Reference full-feature platform for sockets, timestamps, PHC, PPS, and discipline |
| Windows | Native sockets, high-resolution clocks, and bounded clock-control adapter |
| BSD | Socket, `kqueue`, clock, and timestamp adapters without Linux assumptions |
| macOS | Native socket/clock support and Apple platform testing |
| Android | Library-safe time/protocol use; privileged controls remain platform-policy dependent |
| iOS | Library-safe time/protocol use within Apple sandbox restrictions |
| Aesynx | No dependency on Unix types in protocol cores; future native adapter can implement the same traits |

Capability availability will be documented honestly per target. Compiling a
packet codec never implies that a platform can open raw sockets, access timing
hardware, or discipline its system clock.

## Development

Use the pinned toolchain:

```bash
cargo +1.97.1 test --workspace --all-features
scripts/checks.sh
```

Networked release maintenance:

```bash
scripts/check_latest_tools.sh
cargo deny check
cargo audit
scripts/generate-sbom.sh --check
```

## Documentation

- [Implementation Plan](https://github.com/valkyoth/mundilfari/blob/main/docs/IMPLEMENTATION_PLAN.md)
- [Release Plan](https://github.com/valkyoth/mundilfari/blob/main/docs/RELEASE_PLAN.md)
- [Requirements Traceability](https://github.com/valkyoth/mundilfari/blob/main/docs/REQUIREMENTS_TRACEABILITY.md)
- [Implementation Evidence Gate](https://github.com/valkyoth/mundilfari/blob/main/compliance/README.md)
- [Protocol Registry](https://github.com/valkyoth/mundilfari/blob/main/docs/PROTOCOLS.md)
- [Standards Provenance](https://github.com/valkyoth/mundilfari/blob/main/docs/STANDARDS.md)
- [RFC Reference Corpus](https://github.com/valkyoth/mundilfari/blob/main/rfc/README.md)
- [External Standards Registry](https://github.com/valkyoth/mundilfari/blob/main/standards/README.md)
- [Threat Model](https://github.com/valkyoth/mundilfari/blob/main/docs/threat-model.md)
- [Navheim Integration Boundary](https://github.com/valkyoth/mundilfari/blob/main/docs/NAVHEIM_INTEGRATION.md)
- [Crate Version Matrix](https://github.com/valkyoth/mundilfari/blob/main/docs/CRATE_VERSION_MATRIX.md)
- [Release Runbook](https://github.com/valkyoth/mundilfari/blob/main/docs/release-runbook.md)
- [Toolchain Policy](https://github.com/valkyoth/mundilfari/blob/main/docs/toolchain-policy.md)
- [Modularity Policy](https://github.com/valkyoth/mundilfari/blob/main/docs/modularity-policy.md)
- [Original Architecture Discussion](https://github.com/valkyoth/mundilfari/blob/main/docs/IDEA.md)

## License

Licensed under either of:

- Apache License, Version 2.0
- MIT License

at your option.
