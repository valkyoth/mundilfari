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
grep -q 'External condition identifiers decode only to unresolved' docs/modularity-policy.md
grep -q 'Canonical condition resolution grants no runtime trust' docs/modularity-policy.md
grep -q 'bounded `VerifiedBoundDerivation` construction' docs/modularity-policy.md
grep -q 'snapshot-consistent current' docs/modularity-policy.md
grep -q 'evidence assessment, and `PolicyAcceptedHardBound` construction' docs/modularity-policy.md
grep -q 'per-atom support basis remains visible' docs/modularity-policy.md
grep -q 'Generic interval quorum, falseticker rejection' docs/modularity-policy.md
grep -q 'Facade strict APIs require an engine-issued current accepted bound' docs/modularity-policy.md
grep -q 'Strict virtual-clock' docs/modularity-policy.md
grep -q 'enforce the exact monotonic-domain deadline' docs/modularity-policy.md
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
