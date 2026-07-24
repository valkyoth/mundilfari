# Navheim GNSS Timing Integration Boundary

Status: planned architecture; Navheim is not yet implemented.

## Decision

Navheim determines time from GNSS signals, navigation messages, receiver
protocols, corrections, and receiver timing outputs. Mundilfari decides how
that result participates in a clock system alongside NTP, NTS, PTP, radio,
generic PPS, hardware clocks, and local oscillators.

Mundilfari does not build a second partial GNSS stack.

The integration is postponed until Navheim has completed and independently
reviewed its stable GNSS timing observation/event API. No speculative Navheim
dependency, compatibility shim, or copied provisional type is added to the
current workspace.

## Ownership

Navheim owns:

- GPS, Galileo, GLONASS, BeiDou, QZSS, NavIC, and SBAS message interpretation;
- NMEA 0183, NMEA 2000, RTCM, RINEX, gpsd, and receiver/vendor protocols;
- native GNSS epochs, truncated weeks, eras, days, and rollover resolution;
- transmitted UTC corrections, leap announcements, and inter-system offsets;
- satellite and receiver clock corrections and time-only solutions;
- satellite, signal, message, receiver, and model health;
- OSNMA, QZNMA, navigation authentication, spoofing, jamming, and replay
  evidence;
- the GNSS meaning of receiver time marks, PPS edges, and frequency outputs;
- receiver-message association, cable/antenna/receiver delay, quantization,
  uncertainty, integrity, freshness, invalidation, and provenance;
- GNSS common-view and all-in-view time-transfer primitives.

Mundilfari owns:

- generic continuous, atomic, UTC, POSIX, monotonic, and civil-time types;
- generic identifiers for GPS, Galileo, BeiDou, GLONASS, and future scales;
- independently versioned leap and scale-offset models used for cross-checking;
- generic physical PPS/GPIO/serial/hardware edge capture and frequency
  counting;
- protocol-neutral `TimeObservation`, uncertainty, provenance, and source
  traits;
- comparison of GNSS with NTP, NTS, PTP, radio, PHC, and local oscillators;
- source consensus, servos, holdover after GNSS expires, and virtual clocks;
- system-clock, PHC, or oscillator discipline policy and privileged changes.

Mundilfari may understand what GPS Time means without decoding the satellite
frame that carried it. Independent scale/leap validation is a security
cross-check, not a second GNSS interpretation pipeline.

TWSTFT and other communication-satellite time-transfer protocols remain
Mundilfari work because they are not GNSS navigation systems. Mundilfari may
also own the CGGTTS interchange codec, but it consumes Navheim's already
validated common-view/all-in-view evidence and never computes the GNSS
solution. Any feature that uses GNSS receiver or navigation semantics instead
comes from Navheim.

## Dependency Direction

The dependency graph is strictly consumer-owned:

```text
navheim                 mundilfari-core
   \                         /
    \                       /
     +-- mundilfari-navheim --+
                 |
          mundilfari-engine
```

- Navheim never depends on Mundilfari.
- Mundilfari core, engine, platform, facade, and protocol crates never depend
  on Navheim.
- `mundilfari-navheim` depends on both projects and may optionally use
  `mundilfari-platform` for generic PPS capture integration.
- The facade's default feature graph never enables Navheim.
- One adapter covers every constellation supported by Navheim.

The companion crate is intended for crates.io because downstream users need
the stable adapter. Repository-only interoperability, simulator, hardware-lab,
and compatibility-test binaries remain unpublished.

## Upstream Admission Gate

Implementation of `mundilfari-navheim` may start only when all of these are
true:

1. Navheim has a published, reviewed release with stable GNSS timing
   observation and event APIs.
2. Its stable contract includes explicit invalidation, capture-domain
   identity, reason-bearing absence, uncertainty contributions, health,
   authentication, integrity, and provenance.
3. Navheim's MSRV, license, features, transitive graph, unsafe surface, and
   release evidence have passed Mundilfari dependency admission.
4. Exact compatible Navheim releases are recorded and tested.
5. Navheim remains useful without Mundilfari and has no reverse dependency.

Navheim's current plan places the first stable timing API in its later roadmap,
with security and invalidation work following it. Because Navheim will be
built first, Mundilfari waits for the complete reviewed boundary rather than
implementing against an intermediate provisional shape.

## Adapter Contract

`mundilfari-navheim` consumes Navheim timing events and:

- converts exact resolved instants without truncation;
- preserves native scale identity and reports conversion-model disagreement;
- maps asymmetric uncertainty without creating false precision;
- preserves capture clock domain, generation, and PPS correlation;
- preserves health, authentication, signal-authenticity, integrity, freshness,
  and provenance as separate properties;
- rejects unresolved, ambiguous, stale, unhealthy, or policy-disallowed
  evidence;
- withdraws previously accepted observations after a Navheim invalidation;
- never grants clock-discipline authority by parsing or conversion alone.

It must not decode navigation frames, resolve weeks, reinterpret receiver
quality, verify OSNMA, guess PPS labels, or rebuild a receiver protocol.

## PPS Flow

PPS responsibilities remain split:

```text
Mundilfari generic physical edge capture
                    +
Navheim receiver message/time-mark and GNSS semantics
                    |
                    v
        Navheim correlated timing evidence
                    |
                    v
      mundilfari-navheim observation mapping
                    |
                    v
 Mundilfari consensus and clock-use policy
```

Mundilfari records physical edge sequence, timestamp, clock domain, capture
uncertainty, missing pulses, and device errors. Navheim determines which GNSS
instant the receiver says that edge represents and whether the association is
healthy. The adapter preserves both evidence sets.

## Generic Providers Remain Supported

Mundilfari's protocol-neutral source API accepts externally constructed
validated observations without Navheim. This permits timing appliances,
vendor SDKs, custom embedded receivers, recorded laboratory sources, and other
applications to participate without a mandatory GNSS dependency.

Such providers do not gain a GNSS conformance claim. They must supply explicit
scale, uncertainty, capture-domain, health, freshness, authentication,
integrity, and provenance evidence required by the selected discipline policy.

## Verification

The companion release requires:

- compile and feature matrices proving Navheim is absent from default graphs;
- exact conversion, overflow, rounding, and scale-model disagreement tests;
- every Navheim observation, absence, invalidation, discontinuity, and security
  event mapped or rejected explicitly;
- delayed authentication and later invalidation tests;
- PPS/message reorder, loss, reset, rollover, leap, and delay-budget fixtures;
- cross-version compatibility tests against admitted Navheim releases;
- no_std/no-allocation tests wherever both upstream and adapter APIs permit;
- independent receiver, replay, simulator, and hardware timing evidence;
- a focused pentest covering dependency direction and trust preservation.
