# Mundilfari Threat Model

Status: repository-foundation baseline

This document is updated before each security-sensitive protocol or platform
capability is admitted. A passing test suite does not make a source accurate,
authenticated, traceable, fresh, or safe for clock discipline.

## Assets

- Correct time arithmetic, scale, epoch, era, leap, and calendar meaning.
- Integrity and availability of protocol parsing and state machines.
- Accurate uncertainty, quality, provenance, and authentication reporting.
- Exact preservation and timely withdrawal of Navheim GNSS timing evidence.
- Trusted monotonic-to-civil clock correlation.
- Source-selection, consensus, servo, and holdover state.
- NTS cookies, exporter keys, TLS credentials, and signing material.
- System, hardware, virtual, and application clock integrity.
- Privileged helper authority and local IPC.
- Standards, fixtures, release artifacts, SBOMs, and dependency integrity.
- Operator privacy: queried sources and high-resolution timing can reveal
  location, topology, behavior, or device identity.

## Adversaries

- Off-path attackers injecting guessed replies.
- On-path attackers delaying, replaying, dropping, reordering, or modifying
  otherwise authenticated packets.
- Malicious, compromised, misconfigured, or mutually correlated time servers.
- Attackers controlling DNS, routing, proxies, relays, switches, or local
  networks.
- Malicious protocol clients attempting amplification or resource exhaustion.
- GNSS and radio spoofers, jammers, meaconers, and replay transmitters.
- Faulty receivers, oscillators, NICs, drivers, switches, grandmasters, or
  environmental sensors.
- Local unprivileged users attacking daemon IPC or file/socket permissions.
- Compromised unprivileged workers trying to abuse a privileged helper.
- Dependency, registry, CI, action, toolchain, standards-source, or release
  supply-chain attackers.
- Callers providing incorrect crypto, entropy, TLS, clock, or transport
  implementations behind a trait.

## Trust Boundaries

```text
untrusted bytes or signal
        ↓
structural parse
        ↓
semantic validation under exact specification revision
        ↓
association/state/replay validation
        ↓
source policy and diversity classification
        ↓
interval consensus
        ↓
servo observation
        ↓
discipline authorization
        ↓
privileged clock change
```

Additional boundaries:

- native protocol timestamp to normalized atomic time;
- continuous time to UTC, POSIX, local civil, or smeared time;
- monotonic time to persisted civil evidence;
- TLS authentication to NTS time-protocol authorization;
- packet authentication to delay/asymmetry risk;
- claimed clock quality to measured quality;
- platform timestamps to correct packet identity;
- ordinary process to privileged helper;
- third-party dependency to Mundilfari-owned semantics;
- Navheim timing event to `mundilfari-navheim` observation and invalidation;
- licensed normative document to independently written implementation.

## Threats And Baseline Controls

| Threat | Controls |
| --- | --- |
| Malformed packet or signal | bounded parser, checked arithmetic, no unchecked slicing, exact offsets, fuzzing |
| Parser CPU/memory denial | byte/field/depth/work budgets, fixed capacity, no attacker-sized allocation |
| Off-path injection | unpredictable request state, origin matching, address/port policy, authentication |
| Replay | nonces, sequence/origin matching, replay windows, monotonic state, used-cookie tracking |
| Malicious source | diverse sources, interval consensus, Khronos, maximum offset and uncertainty |
| Delay/asymmetry attack | multi-path comparison, delay history, topology policy, uncertainty growth |
| Downgrade | pinned protocol policy; no silent NTS-to-NTP or secure-to-legacy fallback |
| Amplification | bounded response ratio, validation before response, rate and work limits |
| Era/rollover confusion | explicit context and ambiguity errors |
| Leap or scale confusion | typed scales, versioned leap data, explicit POSIX/smear policy |
| Clock rollback | monotonic guard, default no backward step, virtual application clocks |
| Excessive clock change | startup-only step policy, slew/frequency limits, faulted state |
| Loss of sources | holdover state with growing uncertainty and bounded recovery |
| GNSS spoofing or bad upstream evidence | preserve Navheim health/authentication/integrity/provenance, honor invalidation, compare independent clock families |
| Radio spoofing | source fusion, propagation checks, signal quality, independent corroboration |
| PTP manipulation | topology identity, correction/delay monitoring, redundant grandmasters and paths |
| Timestamp misassociation | packet identity, sequence, error-queue, ancillary bounds, drop detection |
| Privilege escalation | minimal helper, typed commands, authenticated bounded IPC, least privilege |
| Secret disclosure | redaction, bounded lifetime, controlled exposure, admitted clearing |
| Weak entropy | OS/hardware entropy trait; fail closed; no time/PID/address fallback |
| Dependency compromise | minimal optional graph, deny/audit, SBOM, immutable pins, admission review |
| Specification drift | official revision registry, errata review, draft isolation, source hashes |
| False precision claim | measurement uncertainty and hardware evidence required |

## Security Modes

### Strict

- authenticated sources required for discipline;
- no downgrade or historical protocol;
- strong source diversity;
- bounded time changes;
- full certificate/identity validation;
- experimental drafts disabled;
- no clock modification without explicit capability.

### Balanced

- authenticated sources preferred;
- unauthenticated observations may corroborate but cannot independently
  authorize a large correction;
- configured private PTP may be accepted under explicit network policy.

### Compatibility

- explicitly selected legacy behavior may run;
- every insecure result is visibly marked;
- clock discipline still requires separate authorization.

### Forensic

- malformed, reserved, unknown, and historical data may be inspected;
- no value receives trust or clock authority automatically;
- no clock modification.

## Residual Risks

- Memory safety does not guarantee correct time or protocol logic.
- Authentication does not prevent malicious endpoints, delay, relay, or
  compromised authorities.
- Multiple hostnames may share one operator, route, oscillator, or upstream.
- `no_std` does not imply determinism, bounded execution, or security.
- OS and hardware timestamps can be wrong, reordered, transformed, or
  associated with the wrong packet.
- Navheim authentication evidence does not eliminate RF relay, receiver
  compromise, adapter mapping faults, or a compromised Navheim dependency.
- Mundilfari cannot independently repair a bad GNSS interpretation; it can
  reject, withdraw, cross-check, diversify, and refuse clock authority.
- Clock steps can break certificates, databases, logs, leases, schedulers, and
  distributed systems even when the new time is more accurate.
- External standards and certification suites may be inaccessible or licensed.
- A dependency-minimal design reduces one risk class but concentrates review
  responsibility in first-party code.

## `v0.1.0` Non-Claims

The foundation contains no time parser, network client, cryptographic
operation, source selection, servo, platform FFI, hardware access, or clock
modification. It is not a usable trusted-time implementation.
