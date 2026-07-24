#!/usr/bin/env sh
set -eu

cargo fmt --all --check
scripts/check_shell_syntax.sh
scripts/check_doc_links.sh
scripts/verify-rfcs.sh
python3 scripts/test-rfc-sources.py
scripts/verify-standard-sources.py
python3 scripts/test-standard-sources.py
python3 scripts/check_release_plan.py
python3 scripts/test-release-plan.py
scripts/test-check-latest-tools.sh

if ! cmp -s README.md crates/mundilfari/README.md; then
    echo "README.md and crates/mundilfari/README.md must remain identical" >&2
    diff -u README.md crates/mundilfari/README.md >&2 || true
    exit 1
fi

scripts/validate-release-metadata.sh
scripts/validate-modularity-policy.sh check
scripts/validate-security-policy.sh
scripts/release_crates.py --check
python3 scripts/test-release-crates.py
python3 scripts/test-sbom-compare.py
scripts/test-release-readiness.sh
scripts/generate-sbom.sh --check

cargo check --workspace --all-features
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace --all-features
RUSTDOCFLAGS="-D warnings" cargo doc --workspace --all-features --no-deps
cargo check --manifest-path tools/xtask/Cargo.toml

cargo package -p mundilfari-core --allow-dirty
cargo package -p mundilfari-engine --allow-dirty \
    --config 'patch.crates-io.mundilfari-core.path="crates/mundilfari-core"'
cargo package -p mundilfari-platform --allow-dirty \
    --config 'patch.crates-io.mundilfari-core.path="crates/mundilfari-core"'
cargo package -p mundilfari --allow-dirty \
    --config 'patch.crates-io.mundilfari-core.path="crates/mundilfari-core"' \
    --config 'patch.crates-io.mundilfari-engine.path="crates/mundilfari-engine"' \
    --config 'patch.crates-io.mundilfari-platform.path="crates/mundilfari-platform"'
