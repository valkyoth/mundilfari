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
- Competing clock discipliners, administrators, hypervisors, or kernel/device
  facilities changing a target outside Mundilfari's control loop.
- Forked, cloned, checkpoint-restored, or VM-restored execution replaying
  inherited requests, entropy, sessions, timers, or clock state.
- Dependency, registry, CI, action, toolchain, standards-source, or release
  supply-chain attackers.
- Callers providing incorrect crypto, entropy, TLS, clock, or transport
  implementations behind a trait.
- Callers treating compiled Cargo features as proof of runtime permission,
  device availability, source health, or clock-discipline authority.

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
- remote time-data transport/authentication to candidate-data admission;
- packet authentication to delay/asymmetry risk;
- claimed clock quality to measured quality;
- platform timestamps to correct packet identity;
- ordinary process to privileged helper;
- compiled platform code to runtime availability, authorization, and health;
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
| Malicious majority or Sybil diversity | explicit `n`/`f` fault assumptions, provenance/assurance/expiry for operator/upstream/path/site claims, conservative unknown correlation, split result, no impossible Byzantine claim |
| Policy or membership changes race consensus | atomic policy/membership generations, stale pending/result invalidation, exact generations in downstream evidence |
| Delay/asymmetry attack | maximum delay/root distance, multi-path comparison, assumption-labeled delay history, topology policy, uncertainty growth |
| Downgrade | pinned protocol policy; no silent NTS-to-NTP or secure-to-legacy fallback |
| Amplification | bounded response ratio, validation before response, rate and work limits |
| Era/rollover confusion | explicit context and ambiguity errors |
| Leap or scale confusion | typed scales, versioned leap data, explicit POSIX/smear policy |
| False or conflicting leap injection | source-neutral candidates, authority-classified evidence, diversity/quorum and conflict policy, opaque admitted handoff, precommit generation/expiry/withdrawal recheck, and consistent publication; one authenticated source is insufficient |
| Leap admission-to-commit race | raw candidates cannot publish the default clock; the admitted handoff binds candidate/evidence/policy/membership/decision generations and typed expiry, and commit linearizes revalidation with publication |
| Smear policy changes leap truth | source smear behavior remains evidence; only admitted UTC evidence determines a leap, while local smear/step policy controls presentation |
| Clock rollback | monotonic guard, default no backward step, virtual application clocks |
| Monotonic-domain confusion | typed suspend/rate/scope/process/machine/namespace/generation identity; cross-domain deadline/elapsed rejection |
| Fork/checkpoint replay | process/machine lifecycle generations invalidate requests, entropy/nonces, handles, timers, rate limits, helper sessions and TrustedClock state |
| Excessive clock change | startup-only step policy, slew/frequency limits, faulted state |
| Loss of sources | holdover state with growing uncertainty and bounded recovery |
| Retracted or invalid evidence remains active | generic identified withdrawal/discontinuity events, reserved invalidation capacity, generation propagation through filter/consensus/servo/clock/audit |
| Statistical confidence presented as guaranteed time | distinct hard/statistical types, named confidence/model, explicit conversion policy, error-budget provenance |
| Provisional or lossy interval types diverge before EOP | one source-neutral interval kernel with exact included/excluded/unbounded endpoints and non-interchangeable hard-claim/statistical wrappers precedes era, fraction, and EOP; trusted estimates remain finite and no domain quantum emulates exclusion |
| Hard-bound logic is strengthened, weakened, or substituted | immutable bounded content-addressed condition language; intersection=`All`, union/hull=`Any`, conversion adds prerequisites, consensus uses reviewed threshold/fault rules; sound-only rewrites and typed generation/rule/collision/capacity failures |
| Claim/recipe digest depends on unstable or ambiguous encoding | one early domain-separated canonical identity profile binds type/units/scale/normalization/endpoints/operation/condition/schema; fixed algorithm plus structural collision comparison; Rust hash/layout/serde/debug inputs are forbidden |
| Early claim transformation discards material needed for verification | every hard claim contains a typed lifetime-brand/generation/domain-bound handle into a bounded canonical derivation DAG; root and transforming interval/era/fraction/scale/UTC/POSIX/uncertainty/observation operations fail unless the complete recipe is stored |
| Recipe handle is dropped, reused, or confused across stores/domains | mandatory generative lifetime-branded handles, nonwrapping generations, caller-owned/fallible bounded arenas, typed heterogeneous edges, canonical import/reinterning, and geometry-only API exclusion fail closed |
| Destroyed arena or wrapped generation validates a stale handle | arena identity is never an address/caller label; invariant fresh brands prevent same-storage ABA, generation exhaustion faults or requires a new brand, and drop/recreate plus near-exhaustion state machines are foundation gates |
| Arena-dependent equality or hashing hides stale handles/collisions | distinct geometry and canonical conditional-claim comparisons plus fallible lease-backed complete-derivation comparison; no infallible semantic `Eq`/`Hash`, and digest maps preserve structural collision buckets |
| Eviction or import races derivation traversal | immutable read leases/frozen pinned snapshots exclude mutation, writes require exclusivity, arena input is materialized before callbacks, and brand/generations are rechecked before issuance |
| Borrowed claim forces self-reference, leaked storage, or forged `'static` lifetime | separate borrowed and fallible owned forms; canonical atomic promotion into bounded frozen ownership; no handle copying, lifetime extension, `Box::leak`, or hidden global owner; compile-fail escape tests |
| Dropping an unverified source arena invalidates or corrupts an accepted token | successful engine promotion creates source-arena-independent proof/token state containing canonical identities and invalidation generations; hosted state is owned and no_std state is inline or uses an explicit checked engine-storage lifetime/brand/generation; drop before completion creates nothing, while later evidence/policy/lifecycle expiry still revokes |
| Repeated single-root promotion duplicates shared DAGs or pins unbounded batch state | bounded atomic `try_promote_set` canonicalizes several roots into one frozen owner, reports per-root and unique totals, coalesces duplicates, retains immutable storage only within declared limits, and reclaims only through bounded new-owner compaction |
| Attacker-controlled batch order or mid-batch failure selects which roots gain authority | canonical root/member ordering, one bounded generation snapshot, shared-node-once verification and failure fan-out, root-local evidence isolation, complete stable accounting, and typed complete-membership witness; cancellation, global exhaustion, snapshot change, or invariant failure globally aborts and mints no proof/token prefix |
| FFI child outlives or races destruction of its arena context | context owns promoted/frozen arena and engine state, child lifetime/retention and close invalidation are explicit, Rust borrows last for one call, and every destruction order/concurrent close path is tested |
| Serialized assumption identity gains authority | external values decode unresolved; exact digest/namespace/schema/rule/content or trusted immutable registry generation must resolve before a condition/hard claim; rollback, collision, noncanonical input, and cache poisoning fail closed |
| Serialized or restored derivation regains authority | bytes decode only as `UnverifiedBoundDerivationRecord`; the opaque verified type has no deserialize path and current engine inputs/rules/models/source/lifecycle state must completely reverify the bounded recipe |
| Canonical condition is mistaken for current truth | separate bounded runtime `ConditionAssessment` over exact evidence/generations with supported/contradicted/indeterminate/expired/withdrawn status; only engine policy constructs an opaque accepted hard bound |
| Supported condition is reused to justify an invented narrower interval | opaque engine `VerifiedBoundDerivation` recomputes or verifies exact root evidence or every derived input/operation/rounding/model/condition/output digest before acceptance |
| Assessment combines evidence from incompatible moments | capture one complete bounded assessor/provider/rule/evidence/policy generation vector, evaluate callbacks unlocked, atomically recheck, and issue assessment plus any accepted token at one linearization point; change retries boundedly or returns indeterminate |
| Configured adversary assumption masquerades as evidence | every atom preserves independent origin/integrity/authority/lineage axes and derived results retain complete transitive leaf bases through policy acceptance, estimates, and facade diagnostics |
| Condition support disappears downstream | reserved lifecycle invalidation rotates assessment generation and rejects stale consensus/leap/servo/estimator/holdover/proposal/clock tokens before use or synchronized labeling |
| Platform scalar/coarse monotonic read understates deadline expiry | clock traits require provider-owned bounded intervals with domain/resolution/method/latency/rate provenance; hosted, PHC, architectural, browser, and embedded adapters conservatively inflate or report strict authority unavailable |
| Linearization authority is mislabeled valid through caller return | default strict result carries `observed_at` and `valid_until` and claims only the sampled linearization interval; distinct through-completion authority requires current reviewed WCET capability and margin |
| Cached synchronized label survives its deadline | every strict read samples the deadline's exact monotonic domain and fails closed at/after upper-edge expiry, after reset/domain failure, or when suspend cannot be covered or invalidated, without relying on a writer or timer |
| Facade erases conditional trust basis | strict path requires a current accepted bound and read-side deadline check; diagnostic path exposes condition, verified-derivation status, atom support basis, assessment, reasons, assurance, deadline, and non-claims; no `is_trusted` boolean |
| GNSS spoofing or bad upstream evidence | preserve Navheim health/authentication/integrity/provenance, honor invalidation, compare independent clock families |
| Radio spoofing | source fusion, propagation checks, signal quality, independent corroboration |
| PTP manipulation | authenticated mechanism or trusted boundary/corroboration for strict discipline, topology identity, correction/delay monitoring, redundant grandmasters and paths |
| Timestamp misassociation | packet identity, sequence, error-queue, ancillary bounds, drop detection |
| Torn concurrent clock snapshot | generation-consistent publication of leap/EOP/scale-offset/conversion/clock components, explicit memory model, model checking, bounded read latency |
| Persisted-state corruption or rollback | early canonical bounded schema, torn-write detection, authenticated integrity where required, explicit rollback capability, no strong freshness claim from mutable local state/key |
| Repeated bounded discipline abuse | helper-local cumulative phase/frequency windows, rate/settling limits, independent policy ceiling, session/domain binding, fault latch, bounded fail-closed audit |
| Servo integrates an unapplied proposal | correlated actual-actuation feedback, target generation, residual/quantization handling, anti-windup, missing-feedback fault |
| Competing clock adjustment | explicit discipline ownership capability, independent external-change detection, target-generation discontinuity, proposal invalidation, servo reacquisition |
| Privilege escalation | protocol-free minimal helper consuming the pre-daemon canonical policy ceiling/audit contract, peer credentials, expiry/replay/session/generation checks, allowlisted handles, independent numerical bounds, syscall sandbox, audit |
| Crypto provider misuse or exhausted key | early protocol-neutral provider contract, provider assurance, atomic per-key usage limits, fail-closed entropy/rekey/exhaustion |
| Secret disclosure or overstated memory protection | redaction, bounded lifetime, controlled exposure, and capability-qualified zeroization/page-lock/core-dump/hardware/external-key reports; unsupported or failed protections remain explicit non-claims |
| Weak entropy | OS/hardware entropy trait; fail closed; no time/PID/address fallback |
| Dependency compromise | minimal optional graph, deny/audit, SBOM, immutable pins, admission review |
| Specification drift | official revision registry, errata review, draft isolation, source hashes |
| Malicious or partial time-data update | explicit provider authorization, bounded caller-serialized verify/stage/compare/commit, competing-writer control, rollback/withdrawal/expiry state, current model retained on failure, and later consistent concurrent publication |
| Authenticated but unauthorized conversion data | opaque EOP/scale-offset admission proofs separately bind verifier-issued artifact evidence and configured source authority; raw or wrong-role signed data cannot publish the default clock |
| Retrieval metadata is mistaken for integrity evidence | platform/custom adapters emit only untrusted `RetrievalClaim`; engine-private verification checks admitted verifier provider generation/capability, digest, attestation/signature, freshness, and rollback before opaque `ArtifactIntegrityEvidence`; callback output is not a trusted boolean |
| Artifact integrity is mistaken for source authority | a correctly signed wrong-role artifact retains integrity evidence but fails separate configured family/role admission; non-cryptographic OS trust uses distinct `ConfiguredPlatformTrustEvidence` and is not called verified or proven |
| Admission authority leaks into core/platform | raw structures and untrusted retrieval claims remain core-owned; platform emitters have no verification/admission power; engine-private constructors consume only core values without a platform dependency; facade cannot create a second verification or admission path |
| Circular remote time-data bootstrap | a candidate never validates the transport, certificate, signature time, or credential context that delivered itself; require an admitted signer/pin or HTTPS under already admitted time, preserve redirect authority, and route offline/manual ingestion through the same pipeline |
| Certificate midpoint acceptance | concrete verifier returns immutable whole-chain/revocation evidence for interval-valued temporal validity; scalar `UnixTime`, midpoint, or preferred projection cannot satisfy strict validation |
| Stale retained TLS/NTS credentials after trust change | stable policy generation plus immutable temporal evidence/horizon and relevant time-model/lifecycle generations; explicit invalidate, revalidate, or bounded-continuation action |
| Credential-context churn from normal clock refinement | context identity references immutable validation evidence rather than the live clock interval; only expiry or relevant policy, revocation, rollback, model, or lifecycle change rotates/revalidates it |
| Cross-service credential-state reuse | service context binds concrete reference identity, endpoint authority, SNI/ALPN policy, presented chain, and temporal evidence |
| Opaque resumption PSK bypasses credential policy | typed `ResumptionCredentialGeneration` binds service context, provider-held handle/generation, TLS/cipher/hash compatibility, ticket identity/key generation, age/use/expiry/replay, lifecycle, and secret/persistence capabilities; missing enforcement disables resumption |
| Resumption reuses connection/exporter state | a revalidated resumption credential authorizes only the resumed transition; every full/resumed handshake creates fresh connection, exporter, and NTS association generations, including resumption without a resent chain |
| Retained credential outlives a safe horizon | layer-owned horizons compose monotonically from service chain/revocation/identity/trust/time-model through resumption ticket/PSK, connection, exporter/key usage, and association/cookie policy; worst-case upper-time/correlation/oscillator/holdover/suspend conversion applies, and missing/invalid deadlines force revalidation or rejection |
| Deep canonical-schema exhaustion | maximum depth/item counts, iterative or bounded recursion, common non-resettable work budget, stable tag namespaces |
| False audit tamper-evidence claim | strict sequence/gap records, domain and TAI/model generations, append-only distinct from chained/sealed/witnessed tamper evidence |
| Configuration rollback or secret leakage | provenance/integrity/rollback generation, staged atomic activation, opaque secret references, independent helper ceiling |
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
- No consensus algorithm can protect against an indistinguishable malicious
  majority outside its stated `n`, `f`, diversity, and interval assumptions.
- `no_std` does not imply determinism, bounded execution, or security.
- OS and hardware timestamps can be wrong, reordered, transformed, or
  associated with the wrong packet.
- Navheim authentication evidence does not eliminate RF relay, receiver
  compromise, adapter mapping faults, or a compromised Navheim dependency.
- Mundilfari cannot independently repair a bad GNSS interpretation; it can
  reject, withdraw, cross-check, diversify, and refuse clock authority.
- Clock steps can break certificates, databases, logs, leases, schedulers, and
  distributed systems even when the new time is more accurate.
- A nondecreasing application-clock projection cannot always remain both
  available and truthful after bad future time; Mundilfari may freeze,
  catch down, remove its preferred estimate, or fault while truth bounds move.
- External standards and certification suites may be inaccessible or licensed.
- A dependency-minimal design reduces one risk class but concentrates review
  responsibility in first-party code.
- Miri, sanitizers, and bounded model checking do not prove unmodeled kernel,
  driver, DMA, MMIO, network, or physical-clock behavior.

## `v0.1.0` Non-Claims

The foundation contains no time parser, network client, cryptographic
operation, source selection, servo, platform FFI, hardware access, or clock
modification. It is not a usable trusted-time implementation.
