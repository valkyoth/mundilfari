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
