#!/usr/bin/env sh
set -eu

mode="${1:-check}"
if [ "$mode" != "check" ]; then
    echo "usage: scripts/validate-modularity-policy.sh check" >&2
    exit 2
fi

violations="$(
    find crates tools scripts -type f \
        \( -name '*.rs' -o -name '*.py' -o -name '*.sh' \) \
        ! -path '*/target/*' \
        -exec wc -l {} \; |
        awk '$1 > 500 { print }'
)"
if [ -n "$violations" ]; then
    echo "Code files exceed 500 lines:" >&2
    echo "$violations" >&2
    exit 1
fi

for crate in mundilfari mundilfari-core mundilfari-engine mundilfari-platform; do
    test -f "crates/$crate/Cargo.toml"
    test -f "crates/$crate/README.md"
    test -f "crates/$crate/src/lib.rs"
done

grep -q 'mundilfari-core.workspace = true' crates/mundilfari-engine/Cargo.toml
grep -q 'mundilfari-core.workspace = true' crates/mundilfari-platform/Cargo.toml
grep -q 'mundilfari-engine.workspace = true' crates/mundilfari/Cargo.toml
! grep -q 'mundilfari-engine' crates/mundilfari-core/Cargo.toml
! grep -q 'mundilfari-platform' crates/mundilfari-core/Cargo.toml
! grep -q 'mundilfari-platform' crates/mundilfari-engine/Cargo.toml
! grep -q 'mundilfari-engine' crates/mundilfari-platform/Cargo.toml
! grep -q 'linux-clock-adjust' docs/IMPLEMENTATION_PLAN.md
grep -q 'Foundational instant/duration interval algebra' docs/modularity-policy.md
grep -q 'Hard-bound conditions are immutable' docs/modularity-policy.md
grep -q 'core `CanonicalIdentityV1` kernel exclusively defines' docs/modularity-policy.md
grep -q 'schema wraps it, crypto providers may reproduce it' docs/modularity-policy.md
grep -q 'non-authoritative `UnverifiedBoundDerivation` recipes' docs/modularity-policy.md
grep -q 'mandatory generative lifetime-branded arena handle' docs/modularity-policy.md
grep -q 'fallible bounded alloc' docs/modularity-policy.md
grep -q 'Generations never wrap' docs/modularity-policy.md
grep -q 'read lease/frozen snapshot' docs/modularity-policy.md
grep -q 'fallible complete-derivation comparisons' docs/modularity-policy.md
grep -q 'infallible semantic' docs/modularity-policy.md
grep -q 'Core owns `BorrowedHardBoundClaim`' docs/modularity-policy.md
grep -q '`OwnedHardBoundClaim`' docs/modularity-policy.md
grep -q '`OwnedHardBoundClaimSet`' docs/modularity-policy.md
grep -q 'single/multi-root promotion' docs/modularity-policy.md
grep -q 'new-owner compaction' docs/modularity-policy.md
grep -q 'Promotion adds no authority' docs/modularity-policy.md
grep -q 'source-arena-independent' docs/modularity-policy.md
grep -q 'engine-storage lifetime' docs/modularity-policy.md
grep -q 'kind-parameterized engine handle' docs/modularity-policy.md
grep -q 'canonical multi-root verification order' docs/modularity-policy.md
grep -q 'authoritative successful prefix' docs/modularity-policy.md
grep -q 'original configured membership' docs/modularity-policy.md
grep -q 'accepted-bound interval contributors' docs/modularity-policy.md
grep -q 'retained/invalidated/absent prior-state' docs/modularity-policy.md
grep -q '`CompleteMemberStatus` and `AbortMemberDiagnostic` are disjoint' docs/modularity-policy.md
grep -q 'cannot enter quorum' docs/modularity-policy.md
grep -q '`BatchAdmissionState`, exact-support `ConsensusAuthority`' docs/modularity-policy.md
grep -q 'conservative validity, and proof-bearing admitted monotonic-correlation' docs/modularity-policy.md
grep -q 'Provider registration alone grants no proof' docs/modularity-policy.md
grep -q 'immutable paired capture anchors' docs/modularity-policy.md
grep -q 'engine-owned RAII `RefreshReservationGuard`' docs/modularity-policy.md
grep -q 'timeout-independent supersession' docs/modularity-policy.md
grep -q '`SupersededNoInstall`' docs/modularity-policy.md
grep -q 'Async wrappers finish' docs/modularity-policy.md
grep -q 'guard across `Poll::Pending`' docs/modularity-policy.md
grep -q '`CommitCoveredRefresh` adds the' docs/modularity-policy.md
grep -q 'reviewed remaining-work bound' docs/modularity-policy.md
grep -q '`UntrustedMonotonicCorrelationCandidate` structure' docs/modularity-policy.md
grep -q '`AdmittedMonotonicDomainCorrelation`' docs/modularity-policy.md
grep -q '`PublishedAuthoritySnapshotId`' docs/modularity-policy.md
grep -q 'cannot extend arena lifetimes' docs/modularity-policy.md
grep -q 'External condition identifiers decode only to unresolved' docs/modularity-policy.md
grep -q '`UnverifiedBoundDerivationRecord`' docs/modularity-policy.md
grep -q 'directly decodes the opaque verified engine type' docs/modularity-policy.md
grep -q 'Canonical condition resolution grants no runtime trust' docs/modularity-policy.md
grep -q 'bounded `VerifiedBoundDerivation` construction' docs/modularity-policy.md
grep -q 'snapshot-consistent current' docs/modularity-policy.md
grep -q 'evidence assessment, and `PolicyAcceptedHardBound` construction' docs/modularity-policy.md
grep -q 'per-atom evidence-origin, integrity, authority' docs/modularity-policy.md
grep -q 'derived transitive leaves' docs/modularity-policy.md
grep -q 'Generic interval quorum, falseticker rejection' docs/modularity-policy.md
grep -q 'Platform clock traits own `read_interval()`' docs/modularity-policy.md
grep -q 'scalar counters conservatively' docs/modularity-policy.md
grep -q 'Facade strict APIs require an engine-issued current accepted bound' docs/modularity-policy.md
grep -q 'Strict virtual-clock' docs/modularity-policy.md
grep -q 'Linearization-time results expose' docs/modularity-policy.md
grep -q 'type-distinct through-completion results require' docs/modularity-policy.md
grep -q 'Leap-candidate structure and pure validation live in core' docs/modularity-policy.md
grep -q 'Core raw leap-model replacement is isolated' docs/modularity-policy.md
grep -q 'Raw EOP and scale-offset snapshots are likewise isolated' docs/modularity-policy.md
grep -q 'platform implementations emit only those claims' docs/modularity-policy.md
grep -q 'provider-neutral verifier alone creates opaque `ArtifactIntegrityEvidence`' docs/modularity-policy.md
grep -q '`ConfiguredPlatformTrustEvidence` for non-cryptographic OS trust' docs/modularity-policy.md
grep -q 'depends on platform; facade composes' docs/modularity-policy.md
grep -q 'Protocol crate feature sets contain no clock-adjustment' docs/modularity-policy.md
grep -q 'canonical pre-daemon policy-ceiling' docs/modularity-policy.md
grep -q 'unavailable atomics are not' docs/modularity-policy.md
grep -q 'Secret-memory APIs report redaction' docs/modularity-policy.md
